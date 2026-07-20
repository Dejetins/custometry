---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
ticket_id: W14-SOURCE-CONNECTION-FILE-IMPORT-KERNEL
status: draft
workstream_id: W14
summary: Implement governed PostgreSQL connection discovery and CSV/XLSX template intake against the deterministic retail source without exposing secrets or accepting ungoverned files.
requirement_ids: [UC-001, UC-002, CONNECTOR-001, CONNECTOR-002, CONNECTOR-003, CONNECTOR-004, CONNECTOR-005, CONNECTOR-006]
blockers: [W13-ORGANIZATION-ACCESS-CORE]
context_sources: [AGENTS.md, .codex/AGENTS.md, custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, docs/architecture/system-design.md, docs/architecture/bounded-context-map.md, tests/golden/retail-demo-manifest.json]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W14-SOURCE-CONNECTION-FILE-IMPORT-KERNEL.md, .codex/delivery/evidence/W14-SOURCE-CONNECTION-FILE-IMPORT-KERNEL.md, packages/connection_catalog/**, packages/data_documentation/**, plugins/connector_postgresql/**, plugins/connector_files/**, apps/api/src/custometry_api/connections/**, apps/api/src/custometry_api/imports/**, apps/api/src/custometry_api/main.py, apps/api/src/custometry_api/config.py, apps/api/pyproject.toml, packages/contracts/source_intake/**, packages/contracts/openapi/**, packages/contracts/schemas/**, packages/contracts/src/**, docs/contracts/contract-drift.json, pyproject.toml, uv.lock, migrations/versions/*_source_intake.py, deploy/demo-source/**, tests/golden/retail-demo-*, tests/contract/source_intake/**, tests/integration/source_intake/**]
  forbidden_write_paths: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/**, apps/web/**, plugins/connector_mssql/**, deploy/compose/compose.release.yaml]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: integration
  proof_skills: [backend-quality-gates]
  commands: [focused connector and file-template contract tests, real read-only PostgreSQL discovery preview and bounded extraction-session tests, malicious CSV/XLSX fixture rejection, secret and DSN redaction tests, deterministic retail fixture verification, migration lifecycle, DDD boundary and contract drift gates, uv run python -m tools.check --scope local, git diff --check]
  proof_boundary: governed-postgresql-and-template-file-source-intake
  evidence_target: .codex/delivery/evidence/W14-SOURCE-CONNECTION-FILE-IMPORT-KERNEL.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

An authorized workspace can test and inspect the isolated retail PostgreSQL
source and accept only published CSV/XLSX templates with deterministic,
redacted, bounded results.

# Non-goals

- Do not add MSSQL, MySQL, ClickHouse, Yandex, arbitrary SQL, browser UI, or
  downstream marts in this slice.

# Work and repair boundary

Own connection and governed file-intake contracts/adapters only. Secrets remain
references and source identities are immutable.

# Acceptance evidence

Requires real source integration, hostile-file rejection, deterministic fixture
proof, migration/contract checks, and no claim for downstream ingestion.
