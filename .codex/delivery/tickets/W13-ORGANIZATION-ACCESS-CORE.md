---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
ticket_id: W13-ORGANIZATION-ACCESS-CORE
status: accepted
workstream_id: W13
summary: Implement organization hierarchy, primary department, scoped leadership, department policy, cross-department grants, resource ownership, transfer lifecycle, and effective-access decisions.
requirement_ids: [UC-028, RBAC-019, RBAC-020, RBAC-021, RBAC-022, RBAC-023, RBAC-024, RBAC-025, RBAC-026, RBAC-028, TEST-INV-076, TEST-INV-077, TEST-INV-078, TEST-INV-079, TEST-INV-080, TEST-INV-081, TEST-INV-082, TEST-INV-083, TEST-INV-084, V1-AC-037, V1-AC-038, V1-AC-039, V1-AC-040, V1-AC-041, V1-AC-042]
blockers: []
context_sources: [AGENTS.md, .codex/AGENTS.md, .codex/delivery/specs/organization-department-access-and-contributor-insights.md, custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, docs/architecture/system-design.md, docs/architecture/bounded-context-map.md, packages/contracts/routes/ui-route-contracts.json]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W13-ORGANIZATION-ACCESS-CORE.md, .codex/delivery/evidence/W13-ORGANIZATION-ACCESS-CORE.md, .codex/delivery/graphs/custometry-runtime-data-stream-v1.json, packages/identity_access/**, apps/api/Dockerfile, apps/api/src/custometry_api/organization/**, apps/api/src/custometry_api/main.py, apps/api/src/custometry_api/config.py, apps/api/pyproject.toml, packages/contracts/organization/**, packages/contracts/openapi/**, packages/contracts/schemas/**, packages/contracts/src/**, docs/contracts/contract-drift.json, pyproject.toml, uv.lock, migrations/versions/*_organization_access.py, tests/unit/organization_access/**, tests/contract/organization_access/**, tests/integration/organization_access/**]
  forbidden_write_paths: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/**, apps/web/**, deploy/**, .codex/delivery/tickets/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: api
  proof_skills: [backend-quality-gates]
  commands: [focused organization and authorization property tests, real PostgreSQL migration lifecycle, real authenticated API tests for hierarchy assignment leadership policy grant ownership transfer and effective-access explanation, negative cross-workspace hidden-count and PII-ceiling tests, uv run python -m tools.custometry_quality.check_ddd_boundaries, uv run python -m tools.custometry_quality.validate_migration_lifecycle, uv run python -m tools.check --scope local, git diff --check]
  proof_boundary: postgres-backed-organization-ownership-and-effective-access-api
  evidence_target: .codex/delivery/evidence/W13-ORGANIZATION-ACCESS-CORE.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W13-ORGANIZATION-ACCESS-CORE.md]
---

# Outcome

Authorized actors can manage a versioned organization tree and obtain
explainable deny-wins access decisions without role explosion or implicit
administrator, leader, or PII authority.

# Non-goals

- Do not implement People activity projections, Web visuals, Penpot, HRIS,
  SCIM, OIDC, rankings, or physical per-department data copies.

# Work and repair boundary

Extend the accepted Identity, Organization & Access context and public ports;
do not read another context's private tables.

# Acceptance evidence

Requires real PostgreSQL/API proof for hierarchy and lifecycle invariants,
negative access cases, migration rollback, redaction, and no browser claim.
