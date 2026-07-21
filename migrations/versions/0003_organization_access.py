"""Create organization hierarchy, policy, grants, ownership, and handover state.

Revision ID: 0003_organization_access
Revises: 0002_identity_auth
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003_organization_access"
down_revision: str | None = "0002_identity_auth"
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
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    op.drop_constraint(
        "ck_identity_membership_status", "identity_memberships", type_="check"
    )
    op.create_check_constraint(
        "ck_identity_membership_status",
        "identity_memberships",
        "status IN ('active', 'suspended', 'departed')",
    )

    op.create_table(
        "organization_units",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "workspace_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("identity_workspaces.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("key", sa.String(length=80), nullable=False),
        sa.Column("current_version", sa.Integer(), nullable=False, server_default="1"),
        *_timestamps(),
        sa.UniqueConstraint("workspace_id", "key", name="uq_organization_unit_key"),
        sa.CheckConstraint("current_version >= 1", name="ck_organization_unit_version"),
    )
    op.create_table(
        "organization_unit_versions",
        sa.Column(
            "org_unit_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("organization_units.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("version", sa.Integer(), primary_key=True),
        sa.Column("kind", sa.String(length=20), nullable=False),
        sa.Column(
            "parent_org_unit_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("organization_units.id", ondelete="RESTRICT"),
            nullable=True,
        ),
        sa.Column("display_name", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "successor_org_unit_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("organization_units.id", ondelete="RESTRICT"),
            nullable=True,
        ),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "kind IN ('company', 'division', 'department', 'team')",
            name="ck_organization_unit_kind",
        ),
        sa.CheckConstraint(
            "status IN ('active', 'inactive', 'merged')",
            name="ck_organization_unit_status",
        ),
        sa.CheckConstraint("version >= 1", name="ck_organization_unit_version_positive"),
        sa.CheckConstraint(
            "effective_to IS NULL OR effective_to > effective_from",
            name="ck_organization_unit_effective_range",
        ),
    )
    op.create_index(
        "ix_organization_unit_versions_parent",
        "organization_unit_versions",
        ["parent_org_unit_id", "status"],
    )
    op.execute(
        """
        WITH roots AS (
          INSERT INTO organization_units
            (id, workspace_id, key, current_version, created_at, updated_at)
          SELECT gen_random_uuid(), w.id, 'company', 1, w.created_at, w.updated_at
          FROM identity_workspaces AS w
          RETURNING id, workspace_id, created_at
        )
        INSERT INTO organization_unit_versions
          (org_unit_id, version, kind, parent_org_unit_id, display_name, status,
           effective_from, created_by, created_at)
        SELECT r.id, 1, 'company', NULL, w.name, 'active', r.created_at,
               (
                 SELECT m.principal_id
                 FROM identity_memberships AS m
                 LEFT JOIN identity_role_assignments AS a
                   ON a.workspace_id = m.workspace_id
                  AND a.principal_id = m.principal_id
                  AND a.role = 'workspace_owner'
                 WHERE m.workspace_id = r.workspace_id
                 ORDER BY (a.role IS NOT NULL) DESC, m.created_at, m.principal_id
                 LIMIT 1
               ),
               r.created_at
        FROM roots AS r
        JOIN identity_workspaces AS w ON w.id = r.workspace_id
        """
    )

    op.create_table(
        "organization_primary_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("principal_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "org_unit_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("organization_units.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "needs_department_assignment",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "effective_period",
            postgresql.TSTZRANGE(),
            sa.Computed(
                "tstzrange(effective_from, COALESCE(effective_to, 'infinity'::timestamptz), '[)')",
                persisted=True,
            ),
            nullable=False,
        ),
        sa.Column("assigned_by", postgresql.UUID(as_uuid=True), nullable=False),
        *_timestamps(),
        sa.ForeignKeyConstraint(
            ["workspace_id", "principal_id"],
            ["identity_memberships.workspace_id", "identity_memberships.principal_id"],
            ondelete="CASCADE",
        ),
        sa.CheckConstraint(
            "effective_to IS NULL OR effective_to > effective_from",
            name="ck_organization_primary_effective_range",
        ),
    )
    op.execute(
        """
        ALTER TABLE organization_primary_assignments
        ADD CONSTRAINT ex_organization_primary_no_overlap
        EXCLUDE USING gist (
          workspace_id WITH =,
          principal_id WITH =,
          effective_period WITH &&
        )
        """
    )
    op.create_index(
        "ix_organization_primary_unit_period",
        "organization_primary_assignments",
        ["org_unit_id", "effective_from", "effective_to"],
    )
    op.execute(
        """
        INSERT INTO organization_primary_assignments
          (id, workspace_id, principal_id, org_unit_id, effective_from,
           needs_department_assignment, assigned_by, created_at, updated_at)
        SELECT gen_random_uuid(), m.workspace_id, m.principal_id, u.id, m.created_at,
               TRUE, m.principal_id, m.created_at, m.updated_at
        FROM identity_memberships AS m
        JOIN organization_units AS u
          ON u.workspace_id = m.workspace_id AND u.key = 'company'
        WHERE m.status = 'active'
        """
    )

    op.create_table(
        "organization_leadership_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("principal_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "org_unit_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("organization_units.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("scope_mode", sa.String(length=20), nullable=False),
        sa.Column("permissions", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("reason", sa.String(length=500), nullable=False),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("assigned_by", postgresql.UUID(as_uuid=True), nullable=False),
        *_timestamps(),
        sa.ForeignKeyConstraint(
            ["workspace_id", "principal_id"],
            ["identity_memberships.workspace_id", "identity_memberships.principal_id"],
            ondelete="CASCADE",
        ),
        sa.CheckConstraint(
            "scope_mode IN ('unit', 'subtree', 'workspace')",
            name="ck_organization_leadership_scope",
        ),
        sa.CheckConstraint("length(reason) > 0", name="ck_organization_leadership_reason"),
        sa.CheckConstraint(
            "effective_to IS NULL OR effective_to > effective_from",
            name="ck_organization_leadership_effective_range",
        ),
    )

    op.create_table(
        "organization_department_policies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "workspace_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("identity_workspaces.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "org_unit_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("organization_units.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("current_version", sa.Integer(), nullable=False, server_default="1"),
        *_timestamps(),
    )
    op.create_table(
        "organization_department_policy_versions",
        sa.Column(
            "policy_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("organization_department_policies.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("version", sa.Integer(), primary_key=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("allowed_actions", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("row_scope_refs", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("column_policy_refs", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("pii_allowed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("include_descendants", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("published_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint(
            "status IN ('draft', 'published', 'deprecated')",
            name="ck_organization_policy_status",
        ),
        sa.CheckConstraint(
            "effective_to IS NULL OR effective_to > effective_from",
            name="ck_organization_policy_effective_range",
        ),
    )

    op.create_table(
        "organization_cross_department_grants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subject_type", sa.String(length=20), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "target_org_unit_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("organization_units.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("resource_type", sa.String(length=80), nullable=True),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("actions", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("reason", sa.String(length=500), nullable=False),
        sa.Column("issued_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        *_timestamps(),
        sa.CheckConstraint(
            "subject_type IN ('principal', 'org_unit')",
            name="ck_organization_grant_subject_type",
        ),
        sa.CheckConstraint("length(reason) > 0", name="ck_organization_grant_reason"),
        sa.CheckConstraint(
            "(resource_type IS NULL) = (resource_id IS NULL)",
            name="ck_organization_grant_resource_pair",
        ),
        sa.CheckConstraint(
            "expires_at IS NULL OR expires_at > effective_from",
            name="ck_organization_grant_effective_range",
        ),
    )
    op.create_index(
        "ix_organization_grant_subject_target",
        "organization_cross_department_grants",
        ["workspace_id", "subject_id", "target_org_unit_id"],
    )

    op.create_table(
        "organization_resource_ownership_bindings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "workspace_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("identity_workspaces.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("resource_type", sa.String(length=80), nullable=False),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("creator_principal_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_type", sa.String(length=20), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("allowed_actions", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("required_row_scope_refs", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "required_column_policy_refs",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("requires_pii", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("effective_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("effective_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("bound_by", postgresql.UUID(as_uuid=True), nullable=False),
        *_timestamps(),
        sa.CheckConstraint(
            "owner_type IN ('principal', 'org_unit', 'workspace_legacy')",
            name="ck_organization_ownership_type",
        ),
        sa.CheckConstraint(
            "effective_to IS NULL OR effective_to > effective_from",
            name="ck_organization_ownership_effective_range",
        ),
    )
    op.create_index(
        "uq_organization_current_resource_owner",
        "organization_resource_ownership_bindings",
        ["workspace_id", "resource_type", "resource_id"],
        unique=True,
        postgresql_where=sa.text("effective_to IS NULL"),
    )
    op.create_index(
        "ix_organization_ownership_creator",
        "organization_resource_ownership_bindings",
        ["workspace_id", "creator_principal_id", "effective_to"],
    )

    op.create_table(
        "organization_ownership_handover_tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("workspace_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("resource_type", sa.String(length=80), nullable=False),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("principal_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("reason", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="open"),
        sa.Column("successor_org_unit_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint(
            "workspace_id",
            "resource_type",
            "resource_id",
            "principal_id",
            "reason",
            name="uq_organization_handover_work",
        ),
        sa.CheckConstraint(
            "status IN ('open', 'resolved')", name="ck_organization_handover_status"
        ),
    )


def downgrade() -> None:
    op.drop_table("organization_ownership_handover_tasks")
    op.drop_table("organization_resource_ownership_bindings")
    op.drop_table("organization_cross_department_grants")
    op.drop_table("organization_department_policy_versions")
    op.drop_table("organization_department_policies")
    op.drop_table("organization_leadership_assignments")
    op.drop_table("organization_primary_assignments")
    op.drop_table("organization_unit_versions")
    op.drop_table("organization_units")
    op.drop_constraint(
        "ck_identity_membership_status", "identity_memberships", type_="check"
    )
    op.execute(
        """
        UPDATE identity_memberships
        SET status = 'suspended', updated_at = CURRENT_TIMESTAMP
        WHERE status = 'departed'
        """
    )
    op.create_check_constraint(
        "ck_identity_membership_status",
        "identity_memberships",
        "status IN ('active', 'suspended')",
    )
