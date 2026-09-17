"""Presentation-owned versioned references, documents and exact draft snapshots."""

from alembic import op

revision = "0011_presentation_drafts"
down_revision = "0010_sales_report"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE presentation_references (
            id uuid NOT NULL, workspace_id uuid NOT NULL REFERENCES identity_workspaces(id),
            owner_principal_id uuid NOT NULL REFERENCES identity_principals(id),
            kind text NOT NULL CHECK(kind IN ('chart_spec','brand_profile','company_pack')),
            content_hash varchar(64) NOT NULL, payload jsonb NOT NULL,
            PRIMARY KEY(workspace_id, owner_principal_id, id)
        );
        CREATE TABLE presentation_documents (
            id uuid PRIMARY KEY, workspace_id uuid NOT NULL REFERENCES identity_workspaces(id),
            owner_principal_id uuid NOT NULL REFERENCES identity_principals(id),
            revision integer NOT NULL DEFAULT 0 CHECK(revision >= 0), latest_version_id uuid
        );
        CREATE INDEX presentation_documents_owner ON presentation_documents(workspace_id, owner_principal_id);
        CREATE TABLE presentation_versions (
            id uuid PRIMARY KEY, document_id uuid NOT NULL REFERENCES presentation_documents(id),
            revision integer NOT NULL CHECK(revision > 0), snapshot_id uuid NOT NULL UNIQUE,
            idempotency_key uuid NOT NULL, request_hash varchar(64) NOT NULL,
            payload jsonb NOT NULL,
            UNIQUE(document_id, revision), UNIQUE(document_id, idempotency_key),
            UNIQUE(document_id, id)
        );
        ALTER TABLE presentation_documents ADD CONSTRAINT presentation_latest_version
            FOREIGN KEY(id, latest_version_id) REFERENCES presentation_versions(document_id, id);
    """)


def downgrade() -> None:
    # Written documents require a pre-upgrade backup or forward repair, never deletion.
    op.execute("""DO $$ BEGIN
        IF EXISTS(SELECT 1 FROM presentation_versions) THEN
            RAISE EXCEPTION 'PRESENTATION_FORWARD_REPAIR_OR_PREUPGRADE_BACKUP_REQUIRED';
        END IF;
    END $$;
    ALTER TABLE presentation_documents DROP CONSTRAINT presentation_latest_version;
    DROP TABLE presentation_versions;
    DROP TABLE presentation_documents;
    DROP TABLE presentation_references;
    """)
