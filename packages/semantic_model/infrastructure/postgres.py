from __future__ import annotations

from typing import Any
from uuid import UUID

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

    @staticmethod
    def get(cursor: Any, *, workspace_id: UUID, version_id: UUID) -> dict[str, object]:
        cursor.execute(
            """SELECT bindings, capability_matrix, impact_summary, request_hash
                          FROM semantic_dataset_versions
                          WHERE workspace_id = %s AND id = %s AND status = 'published'""",
            (workspace_id, version_id),
        )
        row = cursor.fetchone()
        if row is None:
            from packages.contracts.data_pipeline import DataPipelineFailure

            raise DataPipelineFailure("SEMANTIC_DATASET_NOT_FOUND")
        return {
            "bindings": row[0],
            "capability_matrix": row[1],
            "impact_summary": row[2],
            "request_hash": row[3],
        }
