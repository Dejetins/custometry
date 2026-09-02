from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Protocol
from uuid import UUID, uuid5

from psycopg import Connection

from packages.artifacts.domain.model import ArtifactManifest, ArtifactWriteRequest
from packages.artifacts.infrastructure.local import LocalArtifactStore
from packages.artifacts.infrastructure.postgres import PostgresArtifactRepository
from packages.contracts.data_pipeline import DataPipelineFailure, InjectedCrash
from packages.data_quality.application.service import default_retail_rules, evaluate_quality
from packages.data_quality.infrastructure.postgres import PostgresQualityRepository
from packages.execution.infrastructure.postgres import PostgresExecutionRepository
from packages.ingestion.domain.model import ExtractionBatchRequest, RETAIL_OBJECTS
from packages.ingestion.infrastructure.postgres import PostgresIngestionRepository
from packages.semantic_model.application.service import build_retail_publication
from packages.semantic_model.infrastructure.postgres import PostgresSemanticRepository


Connect = Callable[[], Connection[Any]]


class RetailConnector(Protocol):
    def begin_extraction_session(self, *, workspace_id: UUID, source_system_id: UUID) -> Any: ...

    def extract(
        self,
        *,
        session: Any,
        schema_name: str,
        object_name: str,
        columns: tuple[str, ...],
        limit: int,
    ) -> tuple[dict[str, object], ...]: ...

    def close_extraction_session(self, session: Any, outcome: str) -> Any: ...


@dataclass(frozen=True, slots=True)
class PipelineRunResult:
    batch_id: UUID
    state: str
    artifact_manifests: tuple[ArtifactManifest, ...]
    quality_report_id: UUID | None
    quality_decision: str | None
    semantic_dataset_version_id: UUID | None
    candidate_upper_watermark: datetime | None
    reused: bool = False


class DataPipelineRunner:
    def __init__(
        self,
        *,
        connector: RetailConnector,
        connect: Connect,
        artifact_store: LocalArtifactStore,
        fault_checkpoint: str | None = None,
    ) -> None:
        self._connector = connector
        self._connect = connect
        self._artifact_store = artifact_store
        self._fault_checkpoint = fault_checkpoint
        self._ingestion = PostgresIngestionRepository(connect)
        self._execution = PostgresExecutionRepository(connect)
        self._quality = PostgresQualityRepository(connect)

    def _committed(self, request: ExtractionBatchRequest) -> PipelineRunResult | None:
        with self._connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT state, quality_report_id, semantic_dataset_version_id,
                       candidate_upper_watermark
                FROM ingestion_batches WHERE id = %s
                """,
                (request.batch_id,),
            )
            row = cursor.fetchone()
        if row is None or str(row[0]) != "committed":
            return None
        return PipelineRunResult(
            batch_id=request.batch_id,
            state="committed",
            artifact_manifests=(),
            quality_report_id=UUID(str(row[1])),
            quality_decision="persisted",
            semantic_dataset_version_id=UUID(str(row[2])),
            candidate_upper_watermark=row[3],
            reused=True,
        )

    def run(self, request: ExtractionBatchRequest) -> PipelineRunResult:
        batch = self._ingestion.prepare(request)
        committed = self._committed(request)
        if committed is not None:
            return committed
        claim = self._execution.claim(workspace_id=request.workspace_id, batch_id=request.batch_id)
        session: Any | None = None
        try:
            session = self._connector.begin_extraction_session(
                workspace_id=request.workspace_id, source_system_id=request.source_system_id
            )
            if str(session.consistency_mode) != batch.consistency_mode:
                raise DataPipelineFailure("CONSISTENCY_MODE_CHANGED")
            rows_by_semantic_entity: dict[str, tuple[dict[str, object], ...]] = {}
            for specification in RETAIL_OBJECTS:
                rows = self._connector.extract(
                    session=session,
                    schema_name="retail",
                    object_name=specification.source_object,
                    columns=specification.columns,
                    limit=100_000,
                )
                rows_by_semantic_entity[specification.semantic_entity] = tuple(
                    sorted(rows, key=lambda item: item[specification.primary_key])
                )
            self._connector.close_extraction_session(session, "committed")
            session = None
            receipts = rows_by_semantic_entity["Receipt"]
            candidate_upper = max(item["updated_at"] for item in receipts)
            if not isinstance(candidate_upper, datetime):
                raise DataPipelineFailure("INVALID_CANDIDATE_WATERMARK")
            self._ingestion.freeze_candidate(batch_id=request.batch_id, candidate=candidate_upper)

            manifests: list[ArtifactManifest] = []
            for specification in RETAIL_OBJECTS:
                artifact_id = uuid5(request.batch_id, specification.semantic_entity)
                manifests.append(
                    self._artifact_store.write_parquet(
                        ArtifactWriteRequest(
                            artifact_id=artifact_id,
                            workspace_id=request.workspace_id,
                            batch_id=request.batch_id,
                            entity=specification.semantic_entity,
                            pii_class=specification.pii_class,
                        ),
                        rows_by_semantic_entity[specification.semantic_entity],
                    )
                )
            if self._fault_checkpoint == "after_artifact_commit":
                raise InjectedCrash("INJECTED_CRASH_AFTER_ARTIFACT_COMMIT")

            now = datetime.now(UTC)
            entity_aliases = {
                "customers": rows_by_semantic_entity["Customer"],
                "receipts": rows_by_semantic_entity["Receipt"],
                "receipt_items": rows_by_semantic_entity["ReceiptItem"],
                "products": rows_by_semantic_entity["Product"],
            }
            rules = default_retail_rules()
            report = evaluate_quality(
                workspace_id=request.workspace_id,
                batch_id=request.batch_id,
                rows_by_entity=entity_aliases,
                rules=rules,
                waivers=self._quality.active_waivers(workspace_id=request.workspace_id, now=now),
                now=now,
            )
            publication = None
            if report.allows_publication:
                publication = build_retail_publication(
                    semantic_dataset_id=request.semantic_dataset_id,
                    workspace_id=request.workspace_id,
                    batch_id=request.batch_id,
                    quality_report_id=report.report_id,
                    quality_decision=report.decision,
                    artifact_ids={item.entity: item.artifact_id for item in manifests},
                    artifact_hashes={item.entity: item.content_hash for item in manifests},
                    row_counts={item.entity: item.row_count for item in manifests},
                    violation_counts={item.rule_id: item.count for item in report.violations},
                )

            with (
                self._connect() as connection,
                connection.transaction(),
                connection.cursor() as cursor,
            ):
                PostgresExecutionRepository.verify(cursor, claim)
                PostgresArtifactRepository.record(cursor, tuple(manifests))
                PostgresQualityRepository.record(
                    cursor, report, {rule.rule_id: rule.version for rule in rules}
                )
                if publication is None:
                    PostgresIngestionRepository.fail_quality(
                        cursor, batch_id=request.batch_id, quality_report_id=report.report_id
                    )
                    PostgresExecutionRepository.enqueue(
                        cursor,
                        workspace_id=request.workspace_id,
                        aggregate_id=request.batch_id,
                        command_type="data_quality.failed",
                        payload={"quality_report_id": str(report.report_id)},
                    )
                    PostgresExecutionRepository.finish(cursor, claim, state="failed")
                else:
                    PostgresSemanticRepository.publish(cursor, publication)
                    PostgresIngestionRepository.commit_batch(
                        cursor,
                        request=request,
                        candidate_upper=candidate_upper,
                        artifact_ids=tuple(item.artifact_id for item in manifests),
                        quality_report_id=report.report_id,
                        semantic_dataset_version_id=publication.semantic_dataset_version_id,
                    )
                    PostgresExecutionRepository.enqueue(
                        cursor,
                        workspace_id=request.workspace_id,
                        aggregate_id=request.batch_id,
                        command_type="semantic_dataset.published",
                        payload={
                            "semantic_dataset_version_id": str(
                                publication.semantic_dataset_version_id
                            ),
                            "quality_report_id": str(report.report_id),
                        },
                    )
                    PostgresExecutionRepository.finish(cursor, claim, state="succeeded")
            return PipelineRunResult(
                batch_id=request.batch_id,
                state="committed" if publication else "failed",
                artifact_manifests=tuple(manifests),
                quality_report_id=report.report_id,
                quality_decision=report.decision,
                semantic_dataset_version_id=(
                    publication.semantic_dataset_version_id if publication else None
                ),
                candidate_upper_watermark=candidate_upper,
            )
        except Exception as exc:
            if session is not None:
                try:
                    self._connector.close_extraction_session(session, "aborted")
                except Exception:
                    pass
            stable_code = getattr(exc, "code", None)
            code = stable_code if isinstance(stable_code, str) else type(exc).__name__
            self._ingestion.mark_failed(batch_id=request.batch_id, error_code=str(code))
            self._execution.mark_failed(claim)
            raise
