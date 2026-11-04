"""Admit versioned composed reports; preserve all existing immutable payloads."""
from alembic import op

revision = "0014_composer_reports"
down_revision = "0013_identity_lifecycle"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE presentation_versions DROP CONSTRAINT presentation_versions_contract_version_check;
        ALTER TABLE presentation_versions ADD CONSTRAINT presentation_versions_contract_version_check
          CHECK(contract_version IN ('draft-report/v1','configured-report/v2','composed-report/v1'));
    """)


def downgrade() -> None:
    op.execute("""DO $$ BEGIN
      IF EXISTS(SELECT 1 FROM presentation_versions WHERE contract_version='composed-report/v1') THEN
        RAISE EXCEPTION 'COMPOSER_FORWARD_REPAIR_OR_PREUPGRADE_BACKUP_REQUIRED';
      END IF;
    END $$;
    ALTER TABLE presentation_versions DROP CONSTRAINT presentation_versions_contract_version_check;
    ALTER TABLE presentation_versions ADD CONSTRAINT presentation_versions_contract_version_check
      CHECK(contract_version IN ('draft-report/v1','configured-report/v2'));
    """)
