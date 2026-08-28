"""Create the permission-filtered in-app notification projection.

Revision ID: 0009_notifications
Revises: 0008_execution_control
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0009_notifications"
down_revision: str | None = "0008_execution_control"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


SEVERITIES = "'info','warning','critical'"
CATEGORIES = (
    "'run','data_quality','data_freshness','forecast','schedule','system','security','admin'"
)


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
        "notification_source_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_owner", sa.String(length=128), nullable=False),
        sa.Column("source_type", sa.String(length=128), nullable=False),
        sa.Column("source_version", sa.Integer(), nullable=False),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("resource_type", sa.String(length=128), nullable=False),
        sa.Column("resource_id", sa.String(length=128), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("message_code", sa.String(length=80), nullable=False),
        sa.Column("message_parameters", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("group_key", sa.String(length=128), nullable=False),
        sa.Column("deep_link_route_id", sa.String(length=64), nullable=True),
        sa.Column("deep_link_parameters", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("trace_id", sa.String(length=128), nullable=True),
        sa.Column("resolved", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "projected_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint("source_version >= 1", name="ck_notification_event_version"),
        sa.CheckConstraint(f"severity IN ({SEVERITIES})", name="ck_notification_event_severity"),
        sa.CheckConstraint(f"category IN ({CATEGORIES})", name="ck_notification_event_category"),
    )
    op.create_index(
        "ix_notification_events_workspace_time",
        "notification_source_events",
        ["workspace_id", "occurred_at"],
    )

    op.create_table(
        "notification_inbox_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("recipient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("recipient_policy_version", sa.String(length=128), nullable=False),
        sa.Column("preference_reference", sa.String(length=128), nullable=True),
        sa.Column(
            "latest_event_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("notification_source_events.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("source_owner", sa.String(length=128), nullable=False),
        sa.Column("source_type", sa.String(length=128), nullable=False),
        sa.Column("resource_type", sa.String(length=128), nullable=False),
        sa.Column("resource_id", sa.String(length=128), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("message_code", sa.String(length=80), nullable=False),
        sa.Column("message_parameters", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("group_key", sa.String(length=128), nullable=False),
        sa.Column("source_event_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("deep_link_route_id", sa.String(length=64), nullable=True),
        sa.Column("deep_link_parameters", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("trace_id", sa.String(length=128), nullable=True),
        sa.Column("resolved", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("dismissed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revision", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("freshness", sa.String(length=16), nullable=False, server_default="fresh"),
        _created_at(),
        _updated_at(),
        sa.UniqueConstraint(
            "workspace_id", "recipient_id", "group_key", name="uq_notification_recipient_group"
        ),
        sa.CheckConstraint(f"severity IN ({SEVERITIES})", name="ck_notification_item_severity"),
        sa.CheckConstraint(f"category IN ({CATEGORIES})", name="ck_notification_item_category"),
        sa.CheckConstraint("source_event_count >= 1", name="ck_notification_event_count"),
        sa.CheckConstraint("revision >= 1", name="ck_notification_revision"),
        sa.CheckConstraint(
            "freshness IN ('fresh','stale','degraded')", name="ck_notification_freshness"
        ),
    )
    op.create_index(
        "ix_notification_recipient_time",
        "notification_inbox_items",
        ["recipient_id", "occurred_at"],
    )
    op.create_index(
        "ix_notification_recipient_unread",
        "notification_inbox_items",
        ["recipient_id", "read_at", "dismissed_at", "resolved"],
    )

    op.create_table(
        "notification_item_events",
        sa.Column(
            "notification_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("notification_inbox_items.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "event_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("notification_source_events.id", ondelete="RESTRICT"),
            primary_key=True,
        ),
    )

    op.create_table(
        "notification_idempotency",
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("route", sa.String(length=64), primary_key=True),
        sa.Column("idempotency_key", sa.String(length=128), primary_key=True),
        sa.Column("payload_hash", sa.String(length=64), nullable=False),
        sa.Column("response_notification_id", postgresql.UUID(as_uuid=True), nullable=False),
        _created_at(),
    )

    op.create_table(
        "notification_audit_outbox",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("action", sa.String(length=40), nullable=False),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "notification_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("notification_inbox_items.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("reason_code", sa.String(length=80), nullable=False),
        sa.Column("request_id", sa.String(length=128), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "action IN ('notification.acknowledged','notification.dismissed')",
            name="ck_notification_audit_action",
        ),
    )


def downgrade() -> None:
    op.drop_table("notification_audit_outbox")
    op.drop_table("notification_idempotency")
    op.drop_table("notification_item_events")
    op.drop_index("ix_notification_recipient_unread", table_name="notification_inbox_items")
    op.drop_index("ix_notification_recipient_time", table_name="notification_inbox_items")
    op.drop_table("notification_inbox_items")
    op.drop_index("ix_notification_events_workspace_time", table_name="notification_source_events")
    op.drop_table("notification_source_events")
