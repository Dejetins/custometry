"""Create the privacy-safe contributor activity projection.

Revision ID: 0007_contributor_projection
Revises: 0006_analytics_projection
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0007_contributor_projection"
down_revision: str | None = "0006_analytics_projection"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "identity_contributor_projection_events",
        sa.Column("event_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "workspace_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("identity_workspaces.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "principal_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("identity_principals.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("event_type", sa.String(length=48), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resource_type", sa.String(length=20), nullable=True),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("safe_resource_title", sa.String(length=200), nullable=True),
        sa.Column("display_name", sa.String(length=160), nullable=True),
        sa.Column("title", sa.String(length=120), nullable=True),
        sa.Column("title_visible", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "contribution_labels",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "expertise_domains",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "projected_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "event_type IN ('profile.published', 'resource.created', "
            "'resource.published', 'resource.materially_updated', "
            "'resource.maintained', 'collaboration.coauthored', "
            "'collaboration.reviewed', 'collaboration.resolved')",
            name="ck_contributor_event_allowlist",
        ),
        sa.CheckConstraint(
            "(event_type = 'profile.published' AND resource_type IS NULL "
            "AND resource_id IS NULL AND safe_resource_title IS NULL "
            "AND display_name IS NOT NULL) OR "
            "(event_type <> 'profile.published' AND resource_type IS NOT NULL "
            "AND resource_id IS NOT NULL AND safe_resource_title IS NOT NULL "
            "AND display_name IS NULL AND title IS NULL)",
            name="ck_contributor_event_redacted_shape",
        ),
        sa.CheckConstraint(
            "resource_type IS NULL OR resource_type IN ('dashboard', 'report', 'research')",
            name="ck_contributor_event_resource_type",
        ),
    )
    op.create_index(
        "ix_contributor_events_workspace_principal_time",
        "identity_contributor_projection_events",
        ["workspace_id", "principal_id", "occurred_at"],
    )

    op.create_table(
        "identity_contributor_profiles",
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("principal_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("display_name", sa.String(length=160), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=True),
        sa.Column("title_visible", sa.Boolean(), nullable=False),
        sa.Column("contribution_labels", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("expertise_domains", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("projection_version", sa.String(length=64), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["workspace_id", "principal_id"],
            ["identity_memberships.workspace_id", "identity_memberships.principal_id"],
            ondelete="CASCADE",
        ),
    )

    op.create_table(
        "identity_contributor_activity_buckets",
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("principal_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("resource_type", sa.String(length=20), primary_key=True),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("activity_date", sa.Date(), primary_key=True),
        sa.Column("safe_resource_title", sa.String(length=200), nullable=False),
        sa.Column("created_count", sa.Integer(), nullable=False),
        sa.Column("published_count", sa.Integer(), nullable=False),
        sa.Column("materially_updated_count", sa.Integer(), nullable=False),
        sa.Column("maintained_count", sa.Integer(), nullable=False),
        sa.Column("coauthored_count", sa.Integer(), nullable=False),
        sa.Column("reviewed_count", sa.Integer(), nullable=False),
        sa.Column("resolved_count", sa.Integer(), nullable=False),
        sa.Column("last_activity_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("projection_version", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(
            ["workspace_id", "principal_id"],
            ["identity_memberships.workspace_id", "identity_memberships.principal_id"],
            ondelete="CASCADE",
        ),
        sa.CheckConstraint(
            "created_count >= 0 AND published_count >= 0 "
            "AND materially_updated_count >= 0 AND maintained_count >= 0 "
            "AND coauthored_count >= 0 AND reviewed_count >= 0 "
            "AND resolved_count >= 0",
            name="ck_contributor_bucket_nonnegative",
        ),
    )
    op.create_index(
        "ix_contributor_buckets_workspace_principal_date",
        "identity_contributor_activity_buckets",
        ["workspace_id", "principal_id", "activity_date"],
    )

    op.create_table(
        "identity_contributor_projection_state",
        sa.Column(
            "workspace_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("identity_workspaces.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("projection_version", sa.String(length=64), nullable=False),
        sa.Column("event_count", sa.Integer(), nullable=False),
        sa.Column("rebuilt_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("event_count >= 0", name="ck_contributor_state_event_count"),
    )


def downgrade() -> None:
    op.drop_table("identity_contributor_projection_state")
    op.drop_table("identity_contributor_activity_buckets")
    op.drop_table("identity_contributor_profiles")
    op.drop_table("identity_contributor_projection_events")
