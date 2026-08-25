"""Create governed connection catalog and file-import template state.

Revision ID: 0004_source_intake
Revises: 0003_organization_access
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0004_source_intake"
down_revision: str | None = "0003_organization_access"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _timestamps() -> tuple[sa.Column[sa.DateTime], sa.Column[sa.DateTime]]:
    return (
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )


def upgrade() -> None:
    op.create_table(
        "source_connections",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "workspace_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("identity_workspaces.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("source_system_id", postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column("connector_id", sa.String(length=40), nullable=False),
        sa.Column("profile_ref", sa.String(length=80), nullable=False),
        sa.Column("secret_ref", sa.String(length=80), nullable=False),
        sa.Column("display_name", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        *_timestamps(),
        sa.UniqueConstraint("workspace_id", "display_name", name="uq_source_connection_name"),
        sa.CheckConstraint("connector_id = 'postgresql'", name="ck_source_connector_id"),
        sa.CheckConstraint(
            "status IN ('active', 'disabled', 'archived')", name="ck_source_connection_status"
        ),
    )
    op.create_index(
        "ix_source_connections_workspace_status",
        "source_connections",
        ["workspace_id", "status"],
    )
    op.create_table(
        "source_catalog_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "connection_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("source_connections.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("schema_fingerprint", sa.String(length=64), nullable=False),
        sa.Column("object_count", sa.Integer(), nullable=False),
        sa.Column("catalog", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint("object_count >= 0", name="ck_source_catalog_object_count"),
    )
    op.create_index(
        "ix_source_catalog_workspace_connection",
        "source_catalog_snapshots",
        ["workspace_id", "connection_id", "created_at"],
    )
    op.create_table(
        "file_import_templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "workspace_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("identity_workspaces.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("current_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        *_timestamps(),
        sa.CheckConstraint("current_version >= 1", name="ck_file_template_current_version"),
    )
    op.create_table(
        "file_import_template_versions",
        sa.Column(
            "template_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("file_import_templates.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("version", sa.Integer(), primary_key=True),
        sa.Column("revision", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
        sa.Column("accepted_media_types", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("allowed_sheet_names", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("required_sheet_names", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("columns", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("row_limit", sa.Integer(), nullable=False),
        sa.Column("file_size_limit", sa.Integer(), nullable=False),
        sa.Column("decimal_separator", sa.String(length=1), nullable=False),
        sa.Column("date_format", sa.String(length=80), nullable=False),
        sa.Column("error_policy", sa.String(length=40), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "status IN ('draft', 'published', 'deprecated', 'archived')",
            name="ck_file_template_status",
        ),
        sa.CheckConstraint("version >= 1 AND revision >= 1", name="ck_file_template_version"),
        sa.CheckConstraint("row_limit > 0", name="ck_file_template_row_limit"),
        sa.CheckConstraint("file_size_limit > 0", name="ck_file_template_size_limit"),
        sa.CheckConstraint("decimal_separator IN ('.', ',')", name="ck_file_template_decimal"),
        sa.CheckConstraint(
            "error_policy IN ('reject_file', 'reject_rows_with_report')",
            name="ck_file_template_error_policy",
        ),
    )
    op.create_table(
        "source_intake_audit_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "workspace_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("identity_workspaces.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("resource_type", sa.String(length=80), nullable=False),
        sa.Column("resource_id", sa.String(length=120), nullable=False),
        sa.Column(
            "metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index(
        "ix_source_intake_audit_workspace_created",
        "source_intake_audit_events",
        ["workspace_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_source_intake_audit_workspace_created", table_name="source_intake_audit_events"
    )
    op.drop_table("source_intake_audit_events")
    op.drop_table("file_import_template_versions")
    op.drop_table("file_import_templates")
    op.drop_index("ix_source_catalog_workspace_connection", table_name="source_catalog_snapshots")
    op.drop_table("source_catalog_snapshots")
    op.drop_index("ix_source_connections_workspace_status", table_name="source_connections")
    op.drop_table("source_connections")
