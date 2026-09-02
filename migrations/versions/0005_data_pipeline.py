"""Create ingestion, artifact, DQ, semantic, and execution state.

Revision ID: 0005_data_pipeline
Revises: 0004_source_intake
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0005_data_pipeline"
down_revision: str | None = "0004_source_intake"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _created_at() -> sa.Column[sa.DateTime]:
    return sa.Column(
        "created_at",
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )


def _updated_at() -> sa.Column[sa.DateTime]:
    return sa.Column(
        "updated_at",
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.text("CURRENT_TIMESTAMP"),
    )


def upgrade() -> None:
    op.create_table(
        "ingestion_batches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "workspace_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("identity_workspaces.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "connection_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("source_connections.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("source_system_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("semantic_dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False),
        sa.Column("state", sa.String(length=24), nullable=False),
        sa.Column("consistency_mode", sa.String(length=40), nullable=False),
        sa.Column("lower_watermark", sa.DateTime(timezone=True)),
        sa.Column("candidate_upper_watermark", sa.DateTime(timezone=True)),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_code", sa.String(length=80)),
        sa.Column(
            "landing_artifact_ids",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("quality_report_id", postgresql.UUID(as_uuid=True)),
        sa.Column("semantic_dataset_version_id", postgresql.UUID(as_uuid=True)),
        _created_at(),
        _updated_at(),
        sa.UniqueConstraint("workspace_id", "idempotency_key", name="uq_ingestion_idempotency"),
        sa.CheckConstraint(
            "state IN ('created', 'extracting', 'failed', 'committed', 'cancelled')",
            name="ck_ingestion_batch_state",
        ),
        sa.CheckConstraint(
            "consistency_mode IN ('repeatable_read', 'database_snapshot', "
            "'source_checkpoint', 'best_effort_validated')",
            name="ck_ingestion_consistency_mode",
        ),
        sa.CheckConstraint("attempt_count >= 0", name="ck_ingestion_attempt_count"),
    )
    op.create_index(
        "ix_ingestion_workspace_source_state",
        "ingestion_batches",
        ["workspace_id", "source_system_id", "state"],
    )
    op.create_table(
        "ingestion_watermarks",
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_system_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("stream_name", sa.String(length=120), primary_key=True),
        sa.Column("last_successful_watermark", sa.DateTime(timezone=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        _updated_at(),
        sa.CheckConstraint("version >= 1", name="ck_ingestion_watermark_version"),
    )
    op.create_table(
        "execution_claims",
        sa.Column(
            "batch_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("ingestion_batches.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("attempt_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("fencing_token", sa.BigInteger(), nullable=False),
        sa.Column("state", sa.String(length=20), nullable=False),
        _created_at(),
        _updated_at(),
        sa.CheckConstraint("fencing_token > 0", name="ck_execution_fencing_token"),
        sa.CheckConstraint(
            "state IN ('running', 'succeeded', 'failed', 'cancelled')",
            name="ck_execution_claim_state",
        ),
    )
    op.create_table(
        "artifact_manifests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "producer_batch_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("ingestion_batches.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("artifact_type", sa.String(length=60), nullable=False),
        sa.Column("entity", sa.String(length=60), nullable=False),
        sa.Column("relative_uri", sa.String(length=200), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("row_count", sa.BigInteger(), nullable=False),
        sa.Column("byte_size", sa.BigInteger(), nullable=False),
        sa.Column("schema_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("pii_class", sa.String(length=20), nullable=False),
        sa.Column("state", sa.String(length=20), nullable=False),
        _created_at(),
        sa.UniqueConstraint("producer_batch_id", "entity", name="uq_artifact_batch_entity"),
        sa.UniqueConstraint("workspace_id", "relative_uri", name="uq_artifact_relative_uri"),
        sa.CheckConstraint("row_count >= 0 AND byte_size > 0", name="ck_artifact_sizes"),
        sa.CheckConstraint("state = 'committed'", name="ck_artifact_state"),
    )
    op.create_table(
        "artifact_dependencies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "parent_artifact_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("artifact_manifests.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "child_artifact_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("artifact_manifests.id", ondelete="CASCADE"),
            nullable=False,
        ),
        _created_at(),
        sa.UniqueConstraint(
            "parent_artifact_id", "child_artifact_id", name="uq_artifact_dependency"
        ),
    )
    op.create_table(
        "data_quality_waivers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rule_id", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("approved_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("reason_code", sa.String(length=80), nullable=False),
        _created_at(),
        sa.CheckConstraint("status IN ('active', 'revoked')", name="ck_dq_waiver_status"),
    )
    op.create_index(
        "ix_dq_waiver_workspace_rule", "data_quality_waivers", ["workspace_id", "rule_id"]
    )
    op.create_table(
        "data_quality_reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "batch_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("ingestion_batches.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("decision", sa.String(length=30), nullable=False),
        sa.Column("rule_versions", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("violations", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("applied_waiver_ids", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False),
        _created_at(),
        sa.CheckConstraint(
            "decision IN ('passed', 'passed_with_waivers', 'failed')",
            name="ck_dq_report_decision",
        ),
    )
    op.create_index(
        "ix_dq_report_workspace_batch", "data_quality_reports", ["workspace_id", "batch_id"]
    )
    op.create_table(
        "semantic_dataset_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("semantic_dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column(
            "quality_report_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("data_quality_reports.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("bindings", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("capability_matrix", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("impact_summary", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("request_hash", sa.String(length=64), nullable=False),
        _created_at(),
        sa.UniqueConstraint("semantic_dataset_id", "version", name="uq_semantic_dataset_version"),
        sa.UniqueConstraint("workspace_id", "request_hash", name="uq_semantic_request_hash"),
        sa.CheckConstraint("status = 'published'", name="ck_semantic_status"),
    )
    op.create_table(
        "data_pipeline_outbox",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("aggregate_type", sa.String(length=40), nullable=False),
        sa.Column("aggregate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("command_type", sa.String(length=80), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("state", sa.String(length=20), nullable=False),
        sa.Column("delivery_attempts", sa.Integer(), nullable=False, server_default="0"),
        _created_at(),
        _updated_at(),
        sa.UniqueConstraint("aggregate_id", "command_type", name="uq_data_pipeline_outbox"),
        sa.CheckConstraint(
            "state IN ('pending', 'publishing', 'published', 'superseded')",
            name="ck_data_pipeline_outbox_state",
        ),
    )


def downgrade() -> None:
    op.drop_table("data_pipeline_outbox")
    op.drop_table("semantic_dataset_versions")
    op.drop_index("ix_dq_report_workspace_batch", table_name="data_quality_reports")
    op.drop_table("data_quality_reports")
    op.drop_index("ix_dq_waiver_workspace_rule", table_name="data_quality_waivers")
    op.drop_table("data_quality_waivers")
    op.drop_table("artifact_dependencies")
    op.drop_table("artifact_manifests")
    op.drop_table("execution_claims")
    op.drop_table("ingestion_watermarks")
    op.drop_index("ix_ingestion_workspace_source_state", table_name="ingestion_batches")
    op.drop_table("ingestion_batches")
