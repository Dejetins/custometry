"""Bounded identity maintenance and transactional invalidation hints."""

from alembic import op
import sqlalchemy as sa

revision = "0013_identity_lifecycle"
down_revision = "0012_metric_workspace"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""CREATE FUNCTION identity_notify_change() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN PERFORM pg_notify('custometry_identity_changed', 'invalidate'); RETURN NULL; END $$""")
    # Use catalog discovery for this bounded set of Identity-owned table names;
    # schema versions may retain historical organization naming.
    op.execute("""DO $$ DECLARE t record; BEGIN
      FOR t IN SELECT tablename FROM pg_tables WHERE schemaname='public'
      AND (tablename IN ('identity_principals','identity_memberships','identity_workspaces','identity_role_assignments')
           OR tablename LIKE 'organization_%') LOOP
       EXECUTE format('CREATE TRIGGER identity_invalidation AFTER INSERT OR UPDATE OR DELETE ON %I FOR EACH STATEMENT EXECUTE FUNCTION identity_notify_change()',t.tablename);
      END LOOP;
    END $$""")
    op.execute("""CREATE TRIGGER identity_session_invalidation AFTER UPDATE OF revoked_at, absolute_expires_at ON identity_sessions
      FOR EACH STATEMENT EXECUTE FUNCTION identity_notify_change()""")
    op.create_index(
        "ix_identity_sessions_cleanup", "identity_sessions", ["absolute_expires_at", "id"]
    )
    op.create_index(
        "ix_identity_audit_cleanup",
        "identity_audit_events",
        ["occurred_at", "id"],
        postgresql_where=sa.text("action LIKE 'session.%' OR action LIKE 'password.%'"),
    )
    op.create_index("ix_identity_refresh_session", "identity_refresh_history", ["session_id"])
    op.create_table(
        "identity_maintenance_state",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("last_completed_at", sa.DateTime(timezone=True)),
        sa.Column("sessions_deleted", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column("events_deleted", sa.BigInteger(), nullable=False, server_default="0"),
    )
    op.execute("INSERT INTO identity_maintenance_state (id) VALUES (1)")


def downgrade():
    op.drop_table("identity_maintenance_state")
    op.drop_index("ix_identity_refresh_session", table_name="identity_refresh_history")
    op.drop_index("ix_identity_audit_cleanup", table_name="identity_audit_events")
    op.drop_index("ix_identity_sessions_cleanup", table_name="identity_sessions")
    op.execute("DROP FUNCTION identity_notify_change() CASCADE")
