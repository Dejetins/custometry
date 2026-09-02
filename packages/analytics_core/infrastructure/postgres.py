from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb

from packages.contracts.analytics import (
    AnalyticsFailure,
    PublishedSemanticProjection,
    SemanticArtifactBinding,
)


class PostgresAnalyticsRepository:
    def __init__(self, connect: Callable[[], Connection[Any]]) -> None:
        self._connect = connect

    def get_published_projection(
        self, *, workspace_id: UUID, semantic_dataset_version_id: UUID
    ) -> PublishedSemanticProjection:
        with self._connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT entity, artifact_id, relative_uri, content_hash, source_system_id,
                       quality_decision, capability_matrix
                FROM analytics_semantic_artifact_projections
                WHERE workspace_id = %s AND semantic_dataset_version_id = %s
                ORDER BY entity
                """,
                (workspace_id, semantic_dataset_version_id),
            )
            rows = cursor.fetchall()
        if not rows:
            raise AnalyticsFailure("SEMANTIC_DATASET_NOT_FOUND")
        return PublishedSemanticProjection(
            semantic_dataset_version_id=semantic_dataset_version_id,
            workspace_id=workspace_id,
            quality_decision=str(rows[0][5]),
            capability_matrix=dict(rows[0][6]),
            bindings=tuple(
                SemanticArtifactBinding(
                    entity=str(row[0]),
                    artifact_id=UUID(str(row[1])),
                    relative_uri=str(row[2]),
                    content_hash=str(row[3]),
                    source_system_id=UUID(str(row[4])),
                )
                for row in rows
            ),
        )

    def find_by_request_hash(
        self, *, workspace_id: UUID, request_hash: str
    ) -> dict[str, object] | None:
        with self._connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT response_payload FROM analytics_results WHERE workspace_id = %s AND request_hash = %s",
                (workspace_id, request_hash),
            )
            row = cursor.fetchone()
        return None if row is None else dict(row[0])

    def save(self, record: Mapping[str, object]) -> None:
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor() as cursor,
        ):
            cursor.execute(
                """
                INSERT INTO analytics_results
                  (id, workspace_id, owner_principal_id, semantic_dataset_version_id,
                   result_type, request_hash, policy_hash, response_payload, storage_uri,
                   content_hash, byte_size)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (workspace_id, request_hash) DO NOTHING
                """,
                (
                    record["id"],
                    record["workspace_id"],
                    record["owner_principal_id"],
                    record["semantic_dataset_version_id"],
                    record["result_type"],
                    record["request_hash"],
                    record["policy_hash"],
                    Jsonb(record["response_payload"]),
                    record["storage_uri"],
                    record["content_hash"],
                    record["byte_size"],
                ),
            )

    def get_visible(
        self, *, workspace_id: UUID, principal_id: UUID, result_id: UUID
    ) -> dict[str, object]:
        with self._connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT response_payload FROM analytics_results
                WHERE id = %s AND workspace_id = %s AND owner_principal_id = %s
                """,
                (result_id, workspace_id, principal_id),
            )
            row = cursor.fetchone()
        if row is None:
            raise AnalyticsFailure("NOT_FOUND")
        return dict(row[0])

    def list_visible(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        offset: int,
        limit: int,
    ) -> tuple[tuple[dict[str, object], ...], int]:
        with self._connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT response_payload, count(*) OVER ()
                FROM analytics_results
                WHERE workspace_id = %s AND owner_principal_id = %s
                ORDER BY created_at DESC, id
                OFFSET %s LIMIT %s
                """,
                (workspace_id, principal_id, offset, limit),
            )
            rows = cursor.fetchall()
        return tuple(dict(row[0]) for row in rows), (0 if not rows else int(rows[0][1]))
