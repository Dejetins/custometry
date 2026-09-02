from __future__ import annotations

from collections.abc import Callable
from typing import Any
from uuid import UUID, uuid4

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from packages.contracts.data_pipeline import DataPipelineFailure
from packages.execution.domain.model import ExecutionClaim


Connect = Callable[[], Connection[Any]]


class PostgresExecutionRepository:
    def __init__(self, connect: Connect) -> None:
        self._connect = connect

    def claim(self, *, workspace_id: UUID, batch_id: UUID) -> ExecutionClaim:
        attempt_id = uuid4()
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute(
                """
                INSERT INTO execution_claims
                  (batch_id, workspace_id, attempt_id, fencing_token, state)
                VALUES (%s, %s, %s, 1, 'running')
                ON CONFLICT (batch_id) DO UPDATE SET
                  attempt_id = EXCLUDED.attempt_id,
                  fencing_token = execution_claims.fencing_token + 1,
                  state = 'running', updated_at = CURRENT_TIMESTAMP
                RETURNING fencing_token
                """,
                (batch_id, workspace_id, attempt_id),
            )
            row = cursor.fetchone()
            cursor.execute(
                """
                UPDATE ingestion_batches SET state = 'extracting',
                  attempt_count = attempt_count + 1, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND state <> 'committed'
                """,
                (batch_id,),
            )
        assert row is not None
        return ExecutionClaim(batch_id, attempt_id, int(row["fencing_token"]))

    @staticmethod
    def verify(cursor: Any, claim: ExecutionClaim) -> None:
        cursor.execute(
            """
            SELECT attempt_id, fencing_token, state FROM execution_claims
            WHERE batch_id = %s FOR UPDATE
            """,
            (claim.batch_id,),
        )
        row = cursor.fetchone()
        if (
            row is None
            or UUID(str(row[0])) != claim.attempt_id
            or int(row[1]) != claim.fencing_token
            or str(row[2]) != "running"
        ):
            raise DataPipelineFailure("STALE_FENCING_TOKEN")

    @staticmethod
    def finish(cursor: Any, claim: ExecutionClaim, *, state: str) -> None:
        cursor.execute(
            """
            UPDATE execution_claims SET state = %s, updated_at = CURRENT_TIMESTAMP
            WHERE batch_id = %s AND attempt_id = %s AND fencing_token = %s
            """,
            (state, claim.batch_id, claim.attempt_id, claim.fencing_token),
        )
        if cursor.rowcount != 1:
            raise DataPipelineFailure("STALE_FENCING_TOKEN")

    def mark_failed(self, claim: ExecutionClaim) -> None:
        with self._connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE execution_claims SET state = 'failed', updated_at = CURRENT_TIMESTAMP
                WHERE batch_id = %s AND attempt_id = %s AND fencing_token = %s
                """,
                (claim.batch_id, claim.attempt_id, claim.fencing_token),
            )

    @staticmethod
    def enqueue(
        cursor: Any,
        *,
        workspace_id: UUID,
        aggregate_id: UUID,
        command_type: str,
        payload: dict[str, object],
    ) -> None:
        cursor.execute(
            """
            INSERT INTO data_pipeline_outbox
              (id, workspace_id, aggregate_type, aggregate_id, command_type, payload, state)
            VALUES (%s, %s, 'extraction_batch', %s, %s, %s, 'pending')
            ON CONFLICT (aggregate_id, command_type) DO NOTHING
            """,
            (uuid4(), workspace_id, aggregate_id, command_type, Jsonb(payload)),
        )
