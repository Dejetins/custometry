from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any
from uuid import UUID

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from packages.contracts.data_pipeline import DataPipelineFailure
from packages.ingestion.domain.model import ExtractionBatchRequest, ExtractionBatchState


Connect = Callable[[], Connection[Any]]


class PostgresIngestionRepository:
    def __init__(self, connect: Connect) -> None:
        self._connect = connect

    def prepare(self, request: ExtractionBatchRequest) -> ExtractionBatchState:
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute(
                """
                SELECT last_successful_watermark FROM ingestion_watermarks
                WHERE workspace_id = %s AND source_system_id = %s AND stream_name = 'retail.receipts'
                """,
                (request.workspace_id, request.source_system_id),
            )
            watermark_row = cursor.fetchone()
            lower = watermark_row["last_successful_watermark"] if watermark_row else None
            cursor.execute(
                """
                INSERT INTO ingestion_batches
                  (id, workspace_id, connection_id, source_system_id, semantic_dataset_id,
                   idempotency_key, state, consistency_mode, lower_watermark)
                VALUES (%s, %s, %s, %s, %s, %s, 'created', 'repeatable_read', %s)
                ON CONFLICT (workspace_id, idempotency_key) DO NOTHING
                """,
                (
                    request.batch_id,
                    request.workspace_id,
                    request.connection_id,
                    request.source_system_id,
                    request.semantic_dataset_id,
                    request.idempotency_key,
                    lower,
                ),
            )
            cursor.execute(
                """
                SELECT id, state, lower_watermark, candidate_upper_watermark, consistency_mode
                FROM ingestion_batches WHERE workspace_id = %s AND idempotency_key = %s
                """,
                (request.workspace_id, request.idempotency_key),
            )
            row = cursor.fetchone()
        assert row is not None
        if UUID(str(row["id"])) != request.batch_id:
            raise DataPipelineFailure("BATCH_IDEMPOTENCY_ID_MISMATCH")
        return ExtractionBatchState(
            batch_id=request.batch_id,
            state=str(row["state"]),
            lower_watermark=row["lower_watermark"],
            candidate_upper_watermark=row["candidate_upper_watermark"],
            consistency_mode=str(row["consistency_mode"]),
        )

    def freeze_candidate(self, *, batch_id: UUID, candidate: datetime) -> None:
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute(
                """
                SELECT candidate_upper_watermark FROM ingestion_batches WHERE id = %s FOR UPDATE
                """,
                (batch_id,),
            )
            row = cursor.fetchone()
            if row is None:
                raise DataPipelineFailure("BATCH_NOT_FOUND")
            frozen = row["candidate_upper_watermark"]
            if frozen is not None and frozen != candidate:
                raise DataPipelineFailure("SOURCE_BOUNDS_CHANGED")
            cursor.execute(
                """
                UPDATE ingestion_batches SET candidate_upper_watermark = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (candidate, batch_id),
            )

    def mark_failed(self, *, batch_id: UUID, error_code: str) -> None:
        with self._connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE ingestion_batches SET state = 'failed', error_code = %s,
                  updated_at = CURRENT_TIMESTAMP WHERE id = %s AND state <> 'committed'
                """,
                (error_code, batch_id),
            )

    @staticmethod
    def commit_batch(
        cursor: Any,
        *,
        request: ExtractionBatchRequest,
        candidate_upper: datetime,
        artifact_ids: tuple[UUID, ...],
        quality_report_id: UUID,
        semantic_dataset_version_id: UUID,
    ) -> None:
        cursor.execute(
            """
            INSERT INTO ingestion_watermarks
              (workspace_id, source_system_id, stream_name, last_successful_watermark, version)
            VALUES (%s, %s, 'retail.receipts', %s, 1)
            ON CONFLICT (workspace_id, source_system_id, stream_name) DO UPDATE SET
              last_successful_watermark = EXCLUDED.last_successful_watermark,
              version = ingestion_watermarks.version + 1,
              updated_at = CURRENT_TIMESTAMP
            """,
            (request.workspace_id, request.source_system_id, candidate_upper),
        )
        cursor.execute(
            """
            UPDATE ingestion_batches SET state = 'committed', error_code = NULL,
              landing_artifact_ids = %s, quality_report_id = %s,
              semantic_dataset_version_id = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (
                Jsonb([str(item) for item in artifact_ids]),
                quality_report_id,
                semantic_dataset_version_id,
                request.batch_id,
            ),
        )

    @staticmethod
    def fail_quality(cursor: Any, *, batch_id: UUID, quality_report_id: UUID) -> None:
        cursor.execute(
            """
            UPDATE ingestion_batches SET state = 'failed', error_code = 'DQ_GATE_FAILED',
              quality_report_id = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s
            """,
            (quality_report_id, batch_id),
        )
