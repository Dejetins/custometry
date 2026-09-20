"""Add fiscal-calendar versions and personal report storage without rewriting snapshots."""

import hashlib
import json
from uuid import UUID, uuid5
from alembic import op
from sqlalchemy import text

revision = "0012_metric_workspace"
down_revision = "0011_presentation_drafts"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE presentation_documents ADD COLUMN creator_principal_id uuid
            REFERENCES identity_principals(id);
        UPDATE presentation_documents SET creator_principal_id=owner_principal_id;
        ALTER TABLE presentation_documents ALTER COLUMN creator_principal_id SET NOT NULL;
        ALTER TABLE presentation_documents ADD CONSTRAINT presentation_document_scope UNIQUE(workspace_id,id);
        CREATE FUNCTION presentation_preserve_creator() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
            IF TG_OP='INSERT' THEN
                NEW.creator_principal_id := COALESCE(NEW.creator_principal_id,NEW.owner_principal_id);
            ELSIF NEW.creator_principal_id IS DISTINCT FROM OLD.creator_principal_id THEN
                RAISE EXCEPTION 'PRESENTATION_CREATOR_IMMUTABLE';
            END IF;
            RETURN NEW;
        END $$;
        CREATE TRIGGER presentation_creator_guard BEFORE INSERT OR UPDATE ON presentation_documents
            FOR EACH ROW EXECUTE FUNCTION presentation_preserve_creator();
        ALTER TABLE presentation_versions ADD COLUMN contract_version text NOT NULL
            DEFAULT 'draft-report/v1' CHECK(contract_version IN ('draft-report/v1','configured-report/v2'));
        ALTER TABLE analytics_sales_reports ADD COLUMN contract_version text NOT NULL
            DEFAULT 'sales-report/v1' CHECK(contract_version IN ('sales-report/v1','metric-workspace/v2'));
        CREATE TABLE presentation_saved_views (
            id uuid PRIMARY KEY, workspace_id uuid NOT NULL,
            owner_principal_id uuid NOT NULL REFERENCES identity_principals(id),
            document_id uuid NOT NULL, revision integer NOT NULL DEFAULT 0 CHECK(revision>=0),
            latest_version_id uuid,
            FOREIGN KEY(workspace_id,document_id) REFERENCES presentation_documents(workspace_id,id),
            UNIQUE(id,document_id), UNIQUE(workspace_id,id)
        );
        CREATE INDEX presentation_saved_views_owner ON presentation_saved_views(workspace_id,owner_principal_id,document_id);
        CREATE TABLE presentation_saved_view_versions (
            id uuid PRIMARY KEY, saved_view_id uuid NOT NULL, document_id uuid NOT NULL,
            revision integer NOT NULL CHECK(revision>0), document_version_id uuid NOT NULL,
            idempotency_key uuid NOT NULL, request_hash varchar(64) NOT NULL CHECK(request_hash ~ '^[0-9a-f]{64}$'),
            payload jsonb NOT NULL,
            FOREIGN KEY(saved_view_id,document_id) REFERENCES presentation_saved_views(id,document_id),
            FOREIGN KEY(document_id,document_version_id) REFERENCES presentation_versions(document_id,id),
            UNIQUE(saved_view_id,revision), UNIQUE(saved_view_id,idempotency_key), UNIQUE(saved_view_id,id)
        );
        ALTER TABLE presentation_saved_views ADD CONSTRAINT presentation_saved_view_latest
            FOREIGN KEY(id,latest_version_id) REFERENCES presentation_saved_view_versions(saved_view_id,id);
        CREATE TABLE semantic_business_calendar_versions (
            id uuid PRIMARY KEY, workspace_id uuid NOT NULL REFERENCES identity_workspaces(id),
            content_hash varchar(64) NOT NULL CHECK(content_hash ~ '^[0-9a-f]{64}$'),
            profile_json jsonb NOT NULL, created_by uuid REFERENCES identity_principals(id),
            created_at timestamptz NOT NULL DEFAULT now(), previous_version_id uuid,
            idempotency_key uuid, request_hash varchar(64), default_revision integer NOT NULL CHECK(default_revision>=0),
            UNIQUE(workspace_id,id), UNIQUE(workspace_id,idempotency_key), UNIQUE(workspace_id,default_revision),
            FOREIGN KEY(workspace_id,previous_version_id) REFERENCES semantic_business_calendar_versions(workspace_id,id),
            CHECK((default_revision=0 AND created_by IS NULL AND previous_version_id IS NULL AND idempotency_key IS NULL AND request_hash IS NULL)
                OR (default_revision>0 AND created_by IS NOT NULL AND previous_version_id IS NOT NULL AND idempotency_key IS NOT NULL AND request_hash IS NOT NULL AND request_hash ~ '^[0-9a-f]{64}$'))
        );
        CREATE TABLE semantic_workspace_calendar_defaults (
            workspace_id uuid PRIMARY KEY REFERENCES identity_workspaces(id),
            revision integer NOT NULL CHECK(revision>=0), version_id uuid NOT NULL,
            FOREIGN KEY(workspace_id,version_id) REFERENCES semantic_business_calendar_versions(workspace_id,id)
        );
        CREATE FUNCTION semantic_calendar_immutable() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN RAISE EXCEPTION 'BUSINESS_CALENDAR_VERSION_IMMUTABLE'; END $$;
        CREATE TRIGGER semantic_calendar_version_guard BEFORE UPDATE OR DELETE ON semantic_business_calendar_versions
            FOR EACH ROW EXECUTE FUNCTION semantic_calendar_immutable();
    """)
    # Frozen migration payload/identity: never import an evolving runtime model here.
    profile = {
        "schema_version": "business-calendar/v1",
        "kind": "month_based",
        "fiscal_year_start_month": 1,
        "fiscal_year_start_day": 1,
        "year_label": "end_year",
        "timezone": "UTC",
        "week_start": "monday",
    }
    raw = json.dumps(profile, sort_keys=True, separators=(",", ":"))
    content_hash = hashlib.sha256(raw.encode()).hexdigest()
    connection = op.get_bind()
    for row in connection.execute(text("SELECT id FROM identity_workspaces")):
        workspace = UUID(str(row[0]))
        version = uuid5(workspace, "business-calendar/v1/initial-january")
        values = {"workspace": workspace, "version": version, "profile": raw, "hash": content_hash}
        connection.execute(
            text("""INSERT INTO semantic_business_calendar_versions
            (id,workspace_id,content_hash,profile_json,default_revision)
            VALUES (:version,:workspace,:hash,CAST(:profile AS jsonb),0)"""),
            values,
        )
        connection.execute(
            text("INSERT INTO semantic_workspace_calendar_defaults VALUES (:workspace,0,:version)"),
            values,
        )


def downgrade() -> None:
    op.execute("""DO $$ BEGIN
        IF EXISTS(SELECT 1 FROM presentation_versions WHERE contract_version='configured-report/v2')
          OR EXISTS(SELECT 1 FROM analytics_sales_reports WHERE contract_version='metric-workspace/v2')
          OR EXISTS(SELECT 1 FROM presentation_saved_views)
          OR EXISTS(SELECT 1 FROM semantic_business_calendar_versions WHERE default_revision>0) THEN
            RAISE EXCEPTION 'METRIC_WORKSPACE_FORWARD_REPAIR_OR_PREUPGRADE_BACKUP_REQUIRED';
        END IF;
    END $$;
    DROP TABLE semantic_workspace_calendar_defaults;
    DROP TABLE semantic_business_calendar_versions;
    DROP FUNCTION semantic_calendar_immutable();
    ALTER TABLE presentation_saved_views DROP CONSTRAINT presentation_saved_view_latest;
    DROP TABLE presentation_saved_view_versions;
    DROP TABLE presentation_saved_views;
    ALTER TABLE analytics_sales_reports DROP COLUMN contract_version;
    ALTER TABLE presentation_versions DROP COLUMN contract_version;
    DROP TRIGGER presentation_creator_guard ON presentation_documents;
    DROP FUNCTION presentation_preserve_creator();
    ALTER TABLE presentation_documents DROP CONSTRAINT presentation_document_scope;
    ALTER TABLE presentation_documents DROP COLUMN creator_principal_id;
    """)
