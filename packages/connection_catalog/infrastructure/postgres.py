"""PostgreSQL persistence adapter for non-secret connection metadata."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
import hashlib
import json
from typing import Any
from uuid import UUID, uuid4

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from packages.connection_catalog.domain.model import CatalogObject, ConnectionDefinition


Connect = Callable[[], Connection[Any]]


class PostgresConnectionRepository:
    def __init__(self, connect: Connect) -> None:
        self._connect = connect

    def create(self, definition: ConnectionDefinition, *, actor_id: UUID) -> None:
        with self._connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO source_connections
                  (id, workspace_id, source_system_id, connector_id, profile_ref,
                   secret_ref, display_name, status, created_by, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    definition.connection_id,
                    definition.workspace_id,
                    definition.source_system_id,
                    definition.connector_id,
                    definition.profile_ref,
                    definition.secret_ref,
                    definition.display_name,
                    definition.status,
                    actor_id,
                    definition.created_at,
                    definition.created_at,
                ),
            )
            cursor.execute(
                """
                INSERT INTO source_intake_audit_events
                  (id, workspace_id, actor_id, action, resource_type, resource_id, metadata)
                VALUES (%s, %s, %s, 'source.connection.created', 'connection', %s, %s)
                """,
                (
                    uuid4(),
                    definition.workspace_id,
                    actor_id,
                    str(definition.connection_id),
                    Jsonb({"connector_id": definition.connector_id}),
                ),
            )

    def get(self, *, workspace_id: UUID, connection_id: UUID) -> ConnectionDefinition | None:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, workspace_id, source_system_id, connector_id, profile_ref,
                       secret_ref, display_name, status, created_at
                FROM source_connections WHERE workspace_id = %s AND id = %s
                """,
                (workspace_id, connection_id),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        return ConnectionDefinition(
            connection_id=UUID(str(row["id"])),
            workspace_id=UUID(str(row["workspace_id"])),
            source_system_id=UUID(str(row["source_system_id"])),
            connector_id="postgresql",
            profile_ref=str(row["profile_ref"]),
            secret_ref=str(row["secret_ref"]),
            display_name=str(row["display_name"]),
            status=str(row["status"]),  # type: ignore[arg-type]
            created_at=row["created_at"],
        )

    def save_catalog(
        self,
        *,
        workspace_id: UUID,
        connection_id: UUID,
        objects: tuple[CatalogObject, ...],
        actor_id: UUID,
        at: datetime,
    ) -> UUID:
        snapshot_id = uuid4()
        payload = [
            {
                "schema_name": item.schema_name,
                "object_name": item.object_name,
                "object_type": item.object_type,
                "columns": list(item.columns),
            }
            for item in objects
        ]
        fingerprint = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        with self._connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO source_catalog_snapshots
                  (id, workspace_id, connection_id, schema_fingerprint, object_count,
                   catalog, created_by, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    snapshot_id,
                    workspace_id,
                    connection_id,
                    fingerprint,
                    len(payload),
                    Jsonb(payload),
                    actor_id,
                    at,
                ),
            )
        return snapshot_id
