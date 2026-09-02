"""Create governed analytics projections and immutable result metadata.

Revision ID: 0006_analytics_projection
Revises: 0005_data_pipeline
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0006_analytics_projection"
down_revision: str | None = "0005_data_pipeline"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        CREATE VIEW analytics_semantic_artifact_projections AS
        SELECT
          dataset.id AS semantic_dataset_version_id,
          dataset.workspace_id,
          binding.value ->> 'entity' AS entity,
          (binding.value ->> 'artifact_id')::uuid AS artifact_id,
          manifest.relative_uri,
          manifest.content_hash,
          batch.source_system_id,
          quality.decision AS quality_decision,
          dataset.capability_matrix
        FROM semantic_dataset_versions AS dataset
        CROSS JOIN LATERAL jsonb_array_elements(dataset.bindings) AS binding(value)
        JOIN artifact_manifests AS manifest
          ON manifest.id = (binding.value ->> 'artifact_id')::uuid
         AND manifest.workspace_id = dataset.workspace_id
         AND manifest.state = 'committed'
        JOIN ingestion_batches AS batch
          ON batch.id = manifest.producer_batch_id
         AND batch.workspace_id = dataset.workspace_id
         AND batch.state = 'committed'
        JOIN data_quality_reports AS quality
          ON quality.id = dataset.quality_report_id
         AND quality.workspace_id = dataset.workspace_id
        WHERE dataset.status = 'published'
        """
    )
    op.create_table(
        "analytics_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "workspace_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("identity_workspaces.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "owner_principal_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("identity_principals.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "semantic_dataset_version_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("semantic_dataset_versions.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("result_type", sa.String(length=24), nullable=False),
        sa.Column("request_hash", sa.String(length=64), nullable=False),
        sa.Column("policy_hash", sa.String(length=64), nullable=False),
        sa.Column("response_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("storage_uri", sa.String(length=240), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("byte_size", sa.BigInteger(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.UniqueConstraint("workspace_id", "request_hash", name="uq_analytics_result_request"),
        sa.UniqueConstraint("workspace_id", "storage_uri", name="uq_analytics_result_storage"),
        sa.CheckConstraint(
            "result_type IN ('sales', 'customer', 'rfm')",
            name="ck_analytics_result_type",
        ),
        sa.CheckConstraint(
            "byte_size > 0 AND length(content_hash) = 64 AND length(request_hash) = 64 AND length(policy_hash) = 64",
            name="ck_analytics_result_identity",
        ),
    )
    op.create_index(
        "ix_analytics_visible_results",
        "analytics_results",
        ["workspace_id", "owner_principal_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_analytics_visible_results", table_name="analytics_results")
    op.drop_table("analytics_results")
    op.execute("DROP VIEW analytics_semantic_artifact_projections")
