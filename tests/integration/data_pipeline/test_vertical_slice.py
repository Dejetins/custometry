from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from datetime import UTC, datetime, timedelta, tzinfo
from pathlib import Path
from typing import Protocol, cast
from uuid import UUID, uuid4

import pyarrow.parquet as pq  # pyright: ignore[reportMissingTypeStubs]
import pytest
import plugins.connector_postgresql.adapter as connector_adapter

from apps.worker_data import DataPipelineRunner
from packages.artifacts import LocalArtifactStore
from packages.contracts.data_pipeline import DataPipelineFailure
from packages.contracts.data_pipeline import InjectedCrash
from packages.contracts.source_intake import SourceIntakeFailure
from packages.data_quality.domain.model import QualityWaiver
from packages.data_quality.infrastructure.postgres import PostgresQualityRepository
from packages.execution.infrastructure.postgres import PostgresExecutionRepository
from packages.ingestion.domain.model import ExtractionBatchRequest
from packages.ingestion.infrastructure.postgres import PostgresIngestionRepository
from packages.connection_catalog.domain.model import ExtractionSession
from plugins.connector_postgresql.adapter import PostgreSQLConnector
from tests.integration.data_pipeline.conftest import DataPipelineRuntime


class ParquetMetadata(Protocol):
    num_rows: int


read_parquet_metadata = cast(
    Callable[[Path], ParquetMetadata], getattr(pq, "read_metadata")
)


def request(
    runtime: DataPipelineRuntime, *, source_system_id: UUID | None = None
) -> ExtractionBatchRequest:
    source_id = source_system_id or uuid4()
    return ExtractionBatchRequest(
        batch_id=uuid4(),
        workspace_id=runtime.workspace_id,
        connection_id=runtime.create_connection(source_id),
        source_system_id=source_id,
        semantic_dataset_id=uuid4(),
        idempotency_key=f"retail-full-{uuid4()}",
    )


def active_product_waiver(runtime: DataPipelineRuntime) -> QualityWaiver:
    waiver = QualityWaiver(
        waiver_id=uuid4(),
        workspace_id=runtime.workspace_id,
        rule_id="receipt_item.product.reference",
        status="active",
        expires_at=datetime.now(UTC) + timedelta(hours=1),
        approved_by=runtime.actor_id,
        reason_code="DEMO_FIXTURE_KNOWN_MISSING_PRODUCT",
    )
    PostgresQualityRepository(runtime.connect).save_waiver(waiver)
    return waiver


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class RecordingConnector:
    def __init__(self, delegate: PostgreSQLConnector) -> None:
        self.delegate = delegate
        self.begin_count = 0
        self.extracted_objects: list[str] = []
        self.outcomes: list[str] = []

    def begin_extraction_session(
        self, *, workspace_id: UUID, source_system_id: UUID
    ) -> ExtractionSession:
        self.begin_count += 1
        return self.delegate.begin_extraction_session(
            workspace_id=workspace_id, source_system_id=source_system_id
        )

    def extract(
        self,
        *,
        session: ExtractionSession,
        schema_name: str,
        object_name: str,
        columns: tuple[str, ...],
        limit: int,
    ) -> tuple[dict[str, object], ...]:
        self.extracted_objects.append(object_name)
        return self.delegate.extract(
            session=session,
            schema_name=schema_name,
            object_name=object_name,
            columns=columns,
            limit=limit,
        )

    def close_extraction_session(
        self, session: ExtractionSession, outcome: str
    ) -> ExtractionSession:
        self.outcomes.append(outcome)
        return self.delegate.close_extraction_session(session, outcome)


def test_real_postgresql_to_filesystem_dq_semantic_publication_is_idempotent(
    tmp_path: Path, data_pipeline_runtime: DataPipelineRuntime
) -> None:
    manifest = json.loads(Path("tests/golden/retail-demo-manifest.json").read_text())
    active_product_waiver(data_pipeline_runtime)
    batch_request = request(data_pipeline_runtime)
    store = LocalArtifactStore((tmp_path / "artifacts").resolve())
    connector = RecordingConnector(data_pipeline_runtime.connector)
    runner = DataPipelineRunner(
        connector=connector,
        connect=data_pipeline_runtime.connect,
        artifact_store=store,
    )

    result = runner.run(batch_request)

    assert result.state == "committed"
    assert result.quality_decision == "passed_with_waivers"
    assert result.semantic_dataset_version_id is not None
    assert connector.begin_count == 1
    assert connector.extracted_objects == ["customers", "receipts", "receipt_items", "products"]
    assert connector.outcomes == ["committed"]
    counts = {item.entity: item.row_count for item in result.artifact_manifests}
    assert counts == {
        "Customer": manifest["expected_counts"]["customers"],
        "Receipt": manifest["expected_counts"]["receipts"],
        "ReceiptItem": manifest["expected_counts"]["receipt_items"],
        "Product": manifest["expected_counts"]["products"],
    }
    for artifact in result.artifact_manifests:
        path = store.resolve(artifact.relative_uri)
        assert path.is_file()
        assert file_sha256(path) == artifact.content_hash
        metadata = read_parquet_metadata(path)
        assert metadata.num_rows == artifact.row_count

    replay = runner.run(batch_request)
    assert replay.state == "committed"
    assert replay.reused is True
    with data_pipeline_runtime.connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT count(*) FROM artifact_manifests WHERE producer_batch_id = %s",
            (batch_request.batch_id,),
        )
        assert cursor.fetchone() == (4,)
        cursor.execute(
            "SELECT count(*) FROM semantic_dataset_versions WHERE id = %s",
            (result.semantic_dataset_version_id,),
        )
        assert cursor.fetchone() == (1,)
        cursor.execute(
            "SELECT count(*) FROM data_pipeline_outbox WHERE aggregate_id = %s",
            (batch_request.batch_id,),
        )
        assert cursor.fetchone() == (1,)


def test_forced_crash_does_not_advance_watermark_and_retry_reuses_artifacts(
    tmp_path: Path, data_pipeline_runtime: DataPipelineRuntime
) -> None:
    active_product_waiver(data_pipeline_runtime)
    batch_request = request(data_pipeline_runtime)
    store = LocalArtifactStore((tmp_path / "artifacts").resolve())
    crashing = DataPipelineRunner(
        connector=data_pipeline_runtime.connector,
        connect=data_pipeline_runtime.connect,
        artifact_store=store,
        fault_checkpoint="after_artifact_commit",
    )

    with pytest.raises(InjectedCrash, match="INJECTED_CRASH_AFTER_ARTIFACT_COMMIT"):
        crashing.run(batch_request)
    orphan_hashes = {path.name: file_sha256(path) for path in (store.root / "objects").iterdir()}
    assert len(orphan_hashes) == 4
    with data_pipeline_runtime.connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT state, error_code, candidate_upper_watermark FROM ingestion_batches WHERE id = %s",
            (batch_request.batch_id,),
        )
        row = cursor.fetchone()
        assert row is not None
        state, error_code, candidate = cast(tuple[str, str, datetime | None], row)
        assert state == "failed"
        assert error_code == "INJECTED_CRASH_AFTER_ARTIFACT_COMMIT"
        assert candidate is not None
        cursor.execute(
            "SELECT count(*) FROM ingestion_watermarks WHERE source_system_id = %s",
            (batch_request.source_system_id,),
        )
        assert cursor.fetchone() == (0,)
        cursor.execute(
            "SELECT count(*) FROM artifact_manifests WHERE producer_batch_id = %s",
            (batch_request.batch_id,),
        )
        assert cursor.fetchone() == (0,)

    retry = DataPipelineRunner(
        connector=data_pipeline_runtime.connector,
        connect=data_pipeline_runtime.connect,
        artifact_store=store,
    ).run(batch_request)
    assert retry.state == "committed"
    assert {
        path.name: file_sha256(path) for path in (store.root / "objects").iterdir()
    } == orphan_hashes
    with data_pipeline_runtime.connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT attempt_count FROM ingestion_batches WHERE id = %s", (batch_request.batch_id,)
        )
        assert cursor.fetchone() == (2,)
        cursor.execute(
            "SELECT fencing_token, state FROM execution_claims WHERE batch_id = %s",
            (batch_request.batch_id,),
        )
        assert cursor.fetchone() == (2, "succeeded")


def test_required_dq_failure_blocks_watermark_until_active_waiver(
    tmp_path: Path, data_pipeline_runtime: DataPipelineRuntime
) -> None:
    batch_request = request(data_pipeline_runtime)
    store = LocalArtifactStore((tmp_path / "artifacts").resolve())
    runner = DataPipelineRunner(
        connector=data_pipeline_runtime.connector,
        connect=data_pipeline_runtime.connect,
        artifact_store=store,
    )

    failed = runner.run(batch_request)
    assert failed.state == "failed"
    assert failed.quality_decision == "failed"
    assert failed.semantic_dataset_version_id is None
    with data_pipeline_runtime.connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT count(*) FROM ingestion_watermarks WHERE source_system_id = %s",
            (batch_request.source_system_id,),
        )
        assert cursor.fetchone() == (0,)
        cursor.execute(
            "SELECT count(*) FROM semantic_dataset_versions WHERE workspace_id = %s",
            (batch_request.workspace_id,),
        )
        assert cursor.fetchone() == (0,)

    waiver = active_product_waiver(data_pipeline_runtime)
    recovered = runner.run(batch_request)
    assert recovered.state == "committed"
    assert recovered.quality_decision == "passed_with_waivers"
    with data_pipeline_runtime.connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT violations, applied_waiver_ids FROM data_quality_reports "
            "WHERE batch_id = %s ORDER BY created_at DESC LIMIT 1",
            (batch_request.batch_id,),
        )
        report_row = cursor.fetchone()
        assert report_row is not None
        violations, waiver_ids = cast(tuple[list[dict[str, object]], list[str]], report_row)
        product = next(
            item for item in violations if item["rule_id"] == "receipt_item.product.reference"
        )
        assert product["count"] == 5
        assert product["waived"] is True
        assert waiver_ids == [str(waiver.waiver_id)]
        cursor.execute(
            "SELECT capability_matrix, impact_summary FROM semantic_dataset_versions WHERE id = %s",
            (recovered.semantic_dataset_version_id,),
        )
        publication_row = cursor.fetchone()
        assert publication_row is not None
        capabilities, impact = cast(tuple[dict[str, str], dict[str, int]], publication_row)
        assert capabilities["products"] == "degraded"
        assert impact["product_reference_misses"] == 5


def test_stale_fencing_token_cannot_publish(data_pipeline_runtime: DataPipelineRuntime) -> None:
    batch_request = request(data_pipeline_runtime)
    PostgresIngestionRepository(data_pipeline_runtime.connect).prepare(batch_request)
    execution = PostgresExecutionRepository(data_pipeline_runtime.connect)
    stale = execution.claim(
        workspace_id=batch_request.workspace_id, batch_id=batch_request.batch_id
    )
    current = execution.claim(
        workspace_id=batch_request.workspace_id, batch_id=batch_request.batch_id
    )

    with pytest.raises(DataPipelineFailure, match="STALE_FENCING_TOKEN"):
        with (
            data_pipeline_runtime.connect() as connection,
            connection.transaction(),
            connection.cursor() as cursor,
        ):
            PostgresExecutionRepository.verify(cursor, stale)
    with (
        data_pipeline_runtime.connect() as connection,
        connection.transaction(),
        connection.cursor() as cursor,
    ):
        PostgresExecutionRepository.verify(cursor, current)
        PostgresExecutionRepository.finish(cursor, current, state="cancelled")


def test_expired_shared_session_cannot_publish(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    data_pipeline_runtime: DataPipelineRuntime,
) -> None:
    real_datetime = datetime

    class AdvancingDateTime(datetime):
        calls = 0

        @classmethod
        def now(cls, tz: tzinfo | None = None) -> datetime:
            cls.calls += 1
            observed = real_datetime.now(tz)
            return observed if cls.calls == 1 else observed + timedelta(minutes=10)

    monkeypatch.setattr(connector_adapter, "datetime", AdvancingDateTime)
    batch_request = request(data_pipeline_runtime)
    store = LocalArtifactStore((tmp_path / "artifacts").resolve())
    runner = DataPipelineRunner(
        connector=data_pipeline_runtime.connector,
        connect=data_pipeline_runtime.connect,
        artifact_store=store,
    )

    with pytest.raises(SourceIntakeFailure, match="EXTRACTION_SESSION_EXPIRED"):
        runner.run(batch_request)
    with data_pipeline_runtime.connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            "SELECT state, error_code FROM ingestion_batches WHERE id = %s",
            (batch_request.batch_id,),
        )
        assert cursor.fetchone() == ("failed", "EXTRACTION_SESSION_EXPIRED")
        cursor.execute(
            "SELECT count(*) FROM ingestion_watermarks WHERE source_system_id = %s",
            (batch_request.source_system_id,),
        )
        assert cursor.fetchone() == (0,)
        cursor.execute(
            "SELECT count(*) FROM artifact_manifests WHERE producer_batch_id = %s",
            (batch_request.batch_id,),
        )
        assert cursor.fetchone() == (0,)
        cursor.execute(
            "SELECT count(*) FROM semantic_dataset_versions WHERE semantic_dataset_id = %s",
            (batch_request.semantic_dataset_id,),
        )
        assert cursor.fetchone() == (0,)
    assert list((store.root / "objects").iterdir()) == []
