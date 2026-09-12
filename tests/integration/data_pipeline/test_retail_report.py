from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

import pyarrow.parquet as pq  # pyright: ignore[reportMissingTypeStubs]
import pytest

from apps.worker_data.vertical_slice import DataPipelineRunner, RetailConnector
from packages.artifacts.infrastructure.local import LocalArtifactStore
from packages.contracts.data_pipeline import DataPipelineFailure, InjectedCrash
from packages.ingestion.domain.model import ExtractionBatchRequest
from packages.semantic_model.infrastructure.postgres import PostgresSemanticRepository
from tests.integration.data_pipeline.conftest import DataPipelineRuntime


def read_rows(path: Path) -> list[dict[str, Any]]:
    read_table = cast(Any, pq).read_table
    table = read_table(path)
    return cast(list[dict[str, Any]], table.to_pylist())


def request_for(runtime: DataPipelineRuntime) -> ExtractionBatchRequest:
    source = uuid4()
    return ExtractionBatchRequest(
        uuid4(),
        runtime.workspace_id,
        runtime.create_connection(source),
        source,
        uuid4(),
        "retail-report/v1:" + str(uuid4()),
        "retail-report/v1",
    )


def test_real_six_table_publication_replay_and_integrity(
    data_pipeline_runtime: DataPipelineRuntime, tmp_path: Path
) -> None:
    runtime = data_pipeline_runtime
    request = request_for(runtime)
    store = LocalArtifactStore(tmp_path)
    runner = DataPipelineRunner(
        connector=runtime.connector, connect=runtime.connect, artifact_store=store
    )
    result = runner.run(request)
    assert result.state == "committed"
    manifests = {m.entity: m for m in result.artifact_manifests}
    assert len(manifests) == 13
    counts = {
        "Customer": 1000,
        "Product": 120,
        "Receipt": 5000,
        "ReceiptItem": 14995,
        "Store": 20,
        "Calendar": 1830,
    }
    for entity, count in counts.items():
        assert manifests[entity].row_count == count
        assert manifests["Raw" + entity].row_count == (15000 if entity == "ReceiptItem" else count)
    quarantine = read_rows(store.resolve(manifests["QuarantineReceiptItem"].relative_uri))
    assert len(quarantine) == 5
    assert all(
        r["product_id"] == 999999 and r["reason"] == "receipt_item.product.reference"
        for r in quarantine
    )
    receipts = read_rows(store.resolve(manifests["Receipt"].relative_uri))
    items = read_rows(store.resolve(manifests["ReceiptItem"].relative_uri))
    assert all(
        r["source_system_id"] == "northwind-retail" and isinstance(r["receipt_id"], str)
        for r in receipts
    )
    assert any(r["customer_id"] is None for r in receipts)
    assert len({(r["source_system_id"], r["receipt_id"], r["line_id"]) for r in items}) == 14995
    with runtime.connect() as c:
        row = c.execute(
            "SELECT bindings, impact_summary, capability_matrix FROM semantic_dataset_versions WHERE id=%s",
            (result.semantic_dataset_version_id,),
        ).fetchone()
        assert row is not None
        assert len(row[0]) == 6
        assert len(row[1]["relationships"]) == 5
        assert row[1]["quality_accounting"]["gate"] == "allow_degraded"
        assert row[1]["quality_accounting"]["denominator"] == 15000
        assert row[2]["basket"] == "degraded"
        report = c.execute(
            "SELECT violations, applied_waiver_ids FROM data_quality_reports WHERE id=%s",
            (result.quality_report_id,),
        ).fetchone()
        assert report is not None
        assert report[1] == []
        assert report[0][-1]["details"]["quarantined_count"] == 5
    with runtime.connect() as c, c.cursor() as cursor:
        with pytest.raises(DataPipelineFailure, match="SEMANTIC_DATASET_NOT_FOUND"):
            assert result.semantic_dataset_version_id is not None
            PostgresSemanticRepository.get(
                cursor, workspace_id=uuid4(), version_id=result.semantic_dataset_version_id
            )
    replay = runner.run(request)
    assert (
        replay.reused and replay.semantic_dataset_version_id == result.semantic_dataset_version_id
    )
    assert {m.content_hash for m in replay.artifact_manifests} == {
        m.content_hash for m in result.artifact_manifests
    }
    with pytest.raises(DataPipelineFailure, match="BATCH_REQUEST_IDENTITY_MISMATCH"):
        runner.run(replace(request, semantic_dataset_id=uuid4()))
    store.resolve(manifests["Receipt"].relative_uri).write_bytes(b"corrupt")
    with pytest.raises(DataPipelineFailure, match="ARTIFACT_INTEGRITY_FAILED"):
        runner.run(request)


@pytest.mark.parametrize("checkpoint", ["after_artifact_commit", "after_semantic_publication"])
def test_failed_real_publication_has_no_semantic_visibility(
    data_pipeline_runtime: DataPipelineRuntime, tmp_path: Path, checkpoint: str
) -> None:
    runtime = data_pipeline_runtime
    request = request_for(runtime)
    runner = DataPipelineRunner(
        connector=runtime.connector,
        connect=runtime.connect,
        artifact_store=LocalArtifactStore(tmp_path),
        fault_checkpoint=checkpoint,
    )
    with pytest.raises(InjectedCrash):
        runner.run(request)
    with runtime.connect() as c:
        semantic_count = c.execute(
            "SELECT count(*) FROM semantic_dataset_versions WHERE workspace_id=%s",
            (runtime.workspace_id,),
        ).fetchone()
        assert semantic_count is not None
        assert (
            semantic_count[0]
            == 0
        )
        batch_state = c.execute(
            "SELECT state FROM ingestion_batches WHERE id=%s", (request.batch_id,)
        ).fetchone()
        assert batch_state is not None
        assert (
            batch_state[0]
            == "failed"
        )


@pytest.mark.parametrize(
    "defect",
    ["duplicate_customer", "null_item_key", "unknown_product", "missing_store", "missing_receipt"],
)
def test_unexpected_critical_defects_block_real_intake(
    data_pipeline_runtime: DataPipelineRuntime, tmp_path: Path, defect: str
) -> None:
    runtime = data_pipeline_runtime

    class DamagedSource(RetailConnector):
        def begin_extraction_session(self, *, workspace_id: Any, source_system_id: Any) -> Any:
            return runtime.connector.begin_extraction_session(
                workspace_id=workspace_id, source_system_id=source_system_id
            )

        def close_extraction_session(self, session: Any, outcome: str) -> Any:
            return runtime.connector.close_extraction_session(session, outcome)

        def extract(
            self,
            *,
            session: Any,
            schema_name: str,
            object_name: str,
            columns: tuple[str, ...],
            limit: int,
        ) -> tuple[dict[str, object], ...]:
            rows = runtime.connector.extract(
                session=session,
                schema_name=schema_name,
                object_name=object_name,
                columns=columns,
                limit=limit,
            )
            entity = object_name
            if defect == "duplicate_customer" and entity == "customers":
                return rows + (dict(rows[0]),)
            targets = {
                "null_item_key": ("receipt_items", "receipt_item_id", None),
                "unknown_product": ("receipt_items", "product_id", 888888),
                "missing_store": ("receipts", "store_id", 888888),
                "missing_receipt": ("receipt_items", "receipt_id", 888888),
            }
            if defect in targets and entity == targets[defect][0]:
                _, field, value = targets[defect]
                return ({**rows[0], field: value},) + rows[1:]
            return rows

    request = request_for(runtime)
    result = DataPipelineRunner(
        connector=DamagedSource(),
        connect=runtime.connect,
        artifact_store=LocalArtifactStore(tmp_path),
    ).run(request)
    assert result.state == "failed"
    assert result.semantic_dataset_version_id is None
    assert len(result.artifact_manifests) == 6  # All raw input remains durable.
    with runtime.connect() as c:
        semantic_count = c.execute(
            "SELECT count(*) FROM semantic_dataset_versions WHERE workspace_id=%s",
            (runtime.workspace_id,),
        ).fetchone()
        assert semantic_count is not None
        assert (
            semantic_count[0]
            == 0
        )


def test_source_fingerprint_conflict_rejects_real_source(
    data_pipeline_runtime: DataPipelineRuntime, tmp_path: Path
) -> None:
    runtime = data_pipeline_runtime
    request = replace(request_for(runtime), source_fingerprint="0" * 64)
    with pytest.raises(DataPipelineFailure, match="SOURCE_FINGERPRINT_CHANGED"):
        DataPipelineRunner(
            connector=runtime.connector,
            connect=runtime.connect,
            artifact_store=LocalArtifactStore(tmp_path),
        ).run(request)
    with runtime.connect() as c:
        semantic_count = c.execute(
            "SELECT count(*) FROM semantic_dataset_versions WHERE workspace_id=%s",
            (runtime.workspace_id,),
        ).fetchone()
        assert semantic_count is not None
        assert (
            semantic_count[0]
            == 0
        )
