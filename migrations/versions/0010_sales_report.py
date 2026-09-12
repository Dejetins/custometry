"""Add immutable registered sales metric and report metadata; preserve v1 results."""

from alembic import op

revision = "0010_sales_report"
down_revision = "0009_notifications"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE artifact_manifests ALTER COLUMN producer_batch_id DROP NOT NULL;
        CREATE TABLE semantic_sales_metric_versions (
            id uuid PRIMARY KEY, content_hash varchar(64) NOT NULL UNIQUE,
            definition jsonb NOT NULL
        );
        CREATE TABLE analytics_sales_reports (
            id uuid PRIMARY KEY,
            workspace_id uuid NOT NULL REFERENCES identity_workspaces(id),
            owner_principal_id uuid NOT NULL REFERENCES identity_principals(id),
            semantic_dataset_version_id uuid NOT NULL REFERENCES semantic_dataset_versions(id),
            request_hash varchar(64) NOT NULL,
            policy_hash varchar(64) NOT NULL,
            response_payload jsonb NOT NULL,
            UNIQUE(workspace_id, request_hash)
        );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE analytics_sales_reports; DROP TABLE semantic_sales_metric_versions")
    # Result artifacts retain lineage and cannot be deleted by a downgrade.
    op.execute("ALTER TABLE artifact_manifests ALTER COLUMN producer_batch_id SET NOT NULL")
