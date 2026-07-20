---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
ticket_id: W12-IDENTITY-WORKSPACE-LOCAL-AUTH
status: draft
workstream_id: W12
summary: Implement the PostgreSQL-backed identity, workspace membership, local authentication, session, invitation, token, and functional-permission kernel through real API contracts.
requirement_ids: [AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, AUTH-006, AUTH-007, AUTH-008, AUTH-009, AUTH-010, AUTH-011, RBAC-001, RBAC-002, RBAC-003, RBAC-004, RBAC-005, RBAC-006, RBAC-007, RBAC-008, RBAC-009, RBAC-010, RBAC-011, RBAC-012, RBAC-013, RBAC-014, RBAC-015, RBAC-016, RBAC-017, RBAC-018]
blockers: [W11-HYBRID-DEVELOPMENT-RUNTIME]
context_sources: [AGENTS.md, .codex/AGENTS.md, custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, docs/architecture/system-design.md, docs/architecture/bounded-context-map.md, docs/architecture/development-runtime-contract.md, packages/contracts/openapi/foundation.openapi.json]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W12-IDENTITY-WORKSPACE-LOCAL-AUTH.md, .codex/delivery/evidence/W12-IDENTITY-WORKSPACE-LOCAL-AUTH.md, packages/identity_access/**, apps/api/src/custometry_api/identity/**, apps/api/src/custometry_api/main.py, apps/api/src/custometry_api/config.py, apps/api/pyproject.toml, packages/contracts/identity/**, packages/contracts/openapi/**, packages/contracts/schemas/**, packages/contracts/src/**, docs/contracts/contract-drift.json, pyproject.toml, uv.lock, migrations/versions/*_identity_workspace_auth.py, tests/unit/identity_access/**, tests/contract/identity_access/**, tests/integration/identity_access/**]
  forbidden_write_paths: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/**, apps/web/**, deploy/**, .codex/delivery/tickets/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: api
  proof_skills: [backend-quality-gates]
  commands: [focused identity unit and property tests, real PostgreSQL migration upgrade-repeat-downgrade-reupgrade, authenticated API contract tests for bootstrap invite login refresh revoke and workspace isolation, negative permission and cross-workspace tests, uv run python -m tools.custometry_quality.validate_migration_lifecycle, uv run python -m tools.custometry_quality.check_contract_drift, uv run python -m tools.custometry_quality.check_ddd_boundaries, uv run python -m tools.check --scope local, git diff --check]
  proof_boundary: postgres-backed-identity-workspace-local-auth-and-functional-authorization-api
  evidence_target: .codex/delivery/evidence/W12-IDENTITY-WORKSPACE-LOCAL-AUTH.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

Local users can bootstrap, authenticate, rotate/revoke sessions, accept scoped
invites, and operate only inside explicit workspace membership and functional
permission ceilings backed by real PostgreSQL state and stable API contracts.

# Non-goals

- Do not implement organization hierarchy, OIDC, business analytics, Penpot,
  or Web visual flows.

# Work and repair boundary

Own the Identity & Workspace domain/application kernel and its adapters. Keep
password/token secrets hash-only, fail closed, and preserve modular-monolith
dependency direction.

# Acceptance evidence

Requires real migration/API observations, negative tenant/permission cases,
session-reuse detection, redacted evidence, focused backend gates, and no
browser or release claim.
