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


class PostgresSalesSemanticRepository:
    """Provider-owned publication projection; caller resolves current actor policy."""

    def __init__(self, connect: Any) -> None:
        self._connect = connect

    def sales_projection(self, *, workspace_id: UUID, version_id: UUID) -> dict[str, Any]:
        from packages.contracts.analytics import AnalyticsFailure
        from packages.semantic_model.application.sales_metrics import definitions

        with self._connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """SELECT bindings, capability_matrix, impact_summary, quality_report_id,
                          request_hash FROM semantic_dataset_versions
                   WHERE workspace_id = %s AND id = %s AND status = 'published'""",
                (workspace_id, version_id),
            )
            row = cursor.fetchone()
            if row is None:
                raise AnalyticsFailure("SEMANTIC_DATASET_NOT_FOUND")
            if row[2].get("profile") != "retail-report/v1":
                raise AnalyticsFailure("SALES_PROFILE_REQUIRED")
            metrics = definitions()
            for metric in metrics:
                cursor.execute(
                    """INSERT INTO semantic_sales_metric_versions(id, content_hash, definition)
                       VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING""",
                    (metric["version_id"], metric["content_hash"], Jsonb(metric)),
                )
                cursor.execute(
                    "SELECT definition FROM semantic_sales_metric_versions WHERE id=%s",
                    (metric["version_id"],),
                )
                if cursor.fetchone()[0] != metric:
                    raise AnalyticsFailure("METRIC_VERSION_CONFLICT")
            return {
                "bindings": [
                    {**b, "content_hash": row[2]["artifact_hashes"][b["entity"]]} for b in row[0]
                ],
                "capabilities": row[1],
                "summary": row[2],
                "quality_report_id": str(row[3]),
                "publication_hash": row[4],
                "metrics": metrics,
            }
