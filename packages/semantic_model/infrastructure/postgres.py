from __future__ import annotations

from typing import Any

from psycopg.types.json import Jsonb

from packages.semantic_model.domain.model import SemanticDatasetPublication


class PostgresSemanticRepository:
    @staticmethod
    def publish(cursor: Any, publication: SemanticDatasetPublication) -> None:
        cursor.execute(
            """
            INSERT INTO semantic_dataset_versions
              (id, semantic_dataset_id, workspace_id, version, status, quality_report_id,
               bindings, capability_matrix, impact_summary, request_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (workspace_id, request_hash) DO NOTHING
            """,
            (
                publication.semantic_dataset_version_id,
                publication.semantic_dataset_id,
                publication.workspace_id,
                publication.version,
                publication.status,
                publication.quality_report_id,
                Jsonb(
                    [
                        {
                            "entity": binding.entity,
                            "artifact_id": str(binding.artifact_id),
                            "primary_key": binding.primary_key,
                            "field_roles": binding.field_roles,
                        }
                        for binding in publication.bindings
                    ]
                ),
                Jsonb(publication.capability_matrix),
                Jsonb(publication.impact_summary),
                publication.request_hash,
            ),
        )
