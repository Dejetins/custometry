"""Create durable operator execution-control state.

Revision ID: 0008_execution_control
Revises: 0007_contributor_projection
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "0008_execution_control"
down_revision: str | None = "0007_contributor_projection"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


RUN_STATES = "'CREATED','VALIDATING','QUEUED','RUNNING','CANCELLING','SUCCEEDED','FAILED','CANCELLED','PARTIAL'"
ATTEMPT_STATES = "'PENDING','READY','RUNNING','RETRY_WAIT','SUCCEEDED','FAILED','CANCELLED'"


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
        "execution_runs",
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
        sa.Column("execution_kind", sa.String(length=64), nullable=False),
        sa.Column("lane", sa.String(length=64), nullable=False),
        sa.Column("safe_title", sa.String(length=200), nullable=False),
        sa.Column("safe_trace_id", sa.String(length=128), nullable=True),
        sa.Column("state", sa.String(length=20), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("partial_policy", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("retry_of_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("retry_mode", sa.String(length=20), nullable=True),
        sa.Column("policy_version", sa.String(length=128), nullable=False),
        sa.Column("last_request_id", sa.String(length=128), nullable=False),
        _created_at(),
        _updated_at(),
        sa.ForeignKeyConstraint(["retry_of_id"], ["execution_runs.id"], ondelete="RESTRICT"),
        sa.CheckConstraint(f"state IN ({RUN_STATES})", name="ck_execution_run_state"),
        sa.CheckConstraint("revision >= 1", name="ck_execution_run_revision"),
        sa.CheckConstraint(
            "retry_mode IS NULL OR retry_mode IN ('failed_nodes','full_rerun')",
            name="ck_execution_run_retry_mode",
        ),
    )
    op.create_index(
        "ix_execution_runs_workspace_state_created",
        "execution_runs",
        ["workspace_id", "state", "created_at"],
    )
    op.create_index(
        "ix_execution_runs_workspace_owner_created",
        "execution_runs",
        ["workspace_id", "owner_principal_id", "created_at"],
    )

    op.create_table(
        "execution_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("execution_runs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("state", sa.String(length=20), nullable=False),
        sa.Column("fencing_token", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column("retry_of_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("worker_id", sa.String(length=128), nullable=True),
        sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancellation_requested", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("failure_code", sa.String(length=80), nullable=True),
        sa.Column("observed_limit", sa.BigInteger(), nullable=True),
        sa.Column("configured_limit", sa.BigInteger(), nullable=True),
        sa.Column("safe_remediation", sa.String(length=240), nullable=True),
        _created_at(),
        _updated_at(),
        sa.ForeignKeyConstraint(["retry_of_id"], ["execution_attempts.id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("run_id", "attempt_number", name="uq_execution_attempt_number"),
        sa.CheckConstraint(f"state IN ({ATTEMPT_STATES})", name="ck_execution_attempt_state"),
        sa.CheckConstraint("attempt_number >= 1", name="ck_execution_attempt_number"),
        sa.CheckConstraint("fencing_token >= 0", name="ck_execution_attempt_fencing"),
        sa.CheckConstraint(
            "(failure_code IS NULL AND observed_limit IS NULL AND configured_limit IS NULL "
            "AND safe_remediation IS NULL) OR "
            "(state = 'FAILED' AND failure_code = 'RESOURCE_LIMIT_EXCEEDED' "
            "AND observed_limit IS NOT NULL AND configured_limit IS NOT NULL "
            "AND observed_limit > configured_limit AND safe_remediation IS NOT NULL)",
            name="ck_execution_attempt_resource_breach",
        ),
    )
    op.create_index(
        "ix_execution_attempts_workspace_state_lease",
        "execution_attempts",
        ["workspace_id", "state", "lease_expires_at"],
    )

    op.create_table(
        "execution_transition_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("execution_runs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("attempt_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("previous_state", sa.String(length=20), nullable=True),
        sa.Column("new_state", sa.String(length=20), nullable=False),
        sa.Column("actor_or_service", sa.String(length=128), nullable=False),
        sa.Column("reason_code", sa.String(length=500), nullable=False),
        sa.Column("request_id", sa.String(length=128), nullable=False),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index(
        "ix_execution_history_workspace_run_time",
        "execution_transition_history",
        ["workspace_id", "run_id", "occurred_at"],
    )

    op.create_table(
        "execution_outbox",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "run_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("execution_runs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("attempt_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("command_type", sa.String(length=40), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("state", sa.String(length=20), nullable=False),
        sa.Column("delivery_attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("available_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_error_code", sa.String(length=80), nullable=True),
        _created_at(),
        _updated_at(),
        sa.UniqueConstraint(
            "run_id", "attempt_id", "command_type", name="uq_execution_outbox_command"
        ),
        sa.CheckConstraint(
            "state IN ('pending','publishing','published','superseded')",
            name="ck_execution_outbox_state",
        ),
        sa.CheckConstraint("delivery_attempts >= 0", name="ck_execution_outbox_attempts"),
    )
    op.create_index(
        "ix_execution_outbox_pending",
        "execution_outbox",
        ["state", "available_at"],
    )

    op.create_table(
        "execution_idempotency",
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("route", sa.String(length=80), primary_key=True),
        sa.Column("idempotency_key", sa.String(length=128), primary_key=True),
        sa.Column("payload_hash", sa.String(length=64), nullable=False),
        sa.Column("response_run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "execution_reconciliation_findings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("attempt_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("finding_code", sa.String(length=80), nullable=False),
        sa.Column("repair_action", sa.String(length=80), nullable=False),
        sa.Column("request_id", sa.String(length=128), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "run_id", "attempt_id", "finding_code", "request_id",
            name="uq_execution_reconciliation_finding",
        ),
    )


def downgrade() -> None:
    op.drop_table("execution_reconciliation_findings")
    op.drop_table("execution_idempotency")
    op.drop_index("ix_execution_outbox_pending", table_name="execution_outbox")
    op.drop_table("execution_outbox")
    op.drop_index("ix_execution_history_workspace_run_time", table_name="execution_transition_history")
    op.drop_table("execution_transition_history")
    op.drop_index("ix_execution_attempts_workspace_state_lease", table_name="execution_attempts")
    op.drop_table("execution_attempts")
    op.drop_index("ix_execution_runs_workspace_owner_created", table_name="execution_runs")
    op.drop_index("ix_execution_runs_workspace_state_created", table_name="execution_runs")
    op.drop_table("execution_runs")
