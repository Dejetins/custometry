from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from psycopg.types.json import Jsonb

from packages.artifacts.domain.model import ArtifactManifest


class PostgresArtifactRepository:
    @staticmethod
    def record(cursor: Any, manifests: tuple[ArtifactManifest, ...]) -> None:
        for manifest in manifests:
            cursor.execute(
                """
                INSERT INTO artifact_manifests
                  (id, workspace_id, producer_batch_id, artifact_type, entity, relative_uri,
                   content_hash, row_count, byte_size, schema_json, pii_class, state)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'committed')
                ON CONFLICT (id) DO UPDATE SET
                  content_hash = EXCLUDED.content_hash,
                  row_count = EXCLUDED.row_count,
                  byte_size = EXCLUDED.byte_size
                WHERE artifact_manifests.content_hash = EXCLUDED.content_hash
                """,
                (
                    manifest.artifact_id,
                    manifest.workspace_id,
                    manifest.batch_id,
                    manifest.artifact_type,
                    manifest.entity,
                    manifest.relative_uri,
                    manifest.content_hash,
                    manifest.row_count,
                    manifest.byte_size,
                    Jsonb({"version": manifest.schema_version, "columns": manifest.columns}),
                    manifest.pii_class,
                ),
            )
            if cursor.rowcount != 1:
                raise RuntimeError("ARTIFACT_MANIFEST_CONFLICT")

    @staticmethod
    def add_dependency(cursor: Any, *, parent_id: object, child_id: object) -> None:
        cursor.execute(
            """
            INSERT INTO artifact_dependencies (id, parent_artifact_id, child_artifact_id)
            VALUES (%s, %s, %s) ON CONFLICT (parent_artifact_id, child_artifact_id) DO NOTHING
            """,
            (uuid4(), parent_id, child_id),
        )

    @staticmethod
    def for_batch(
        cursor: Any, *, workspace_id: UUID, batch_id: UUID
    ) -> tuple[ArtifactManifest, ...]:
        cursor.execute(
            """SELECT id, entity, artifact_type, relative_uri, content_hash,
                          row_count, byte_size, schema_json, pii_class FROM artifact_manifests
                          WHERE workspace_id = %s AND producer_batch_id = %s AND state = 'committed'
                          ORDER BY entity""",
            (workspace_id, batch_id),
        )
        return tuple(
            ArtifactManifest(
                UUID(str(r[0])),
                workspace_id,
                batch_id,
                str(r[1]),
                str(r[2]),
                str(r[3]),
                str(r[4]),
                int(r[5]),
                int(r[6]),
                tuple(r[7]["columns"]),
                str(r[8]),
                int(r[7]["version"]),
            )
            for r in cursor.fetchall()
        )
