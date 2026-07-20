---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
ticket_id: W17-PEOPLE-CONTRIBUTOR-ACTIVITY-PROJECTION
status: draft
workstream_id: W17
summary: Build the privacy-safe contributor activity projection and policy-filtered People API for self, scoped leader, explicit grantee, and ordinary authorized viewer variants.
requirement_ids: [UC-029, RBAC-022, RBAC-027, TEST-INV-085, TEST-INV-086, TEST-INV-087, TEST-INV-088, V1-AC-043]
blockers: [W13-ORGANIZATION-ACCESS-CORE, W16-SALES-CUSTOMER-RFM-API-PROJECTIONS]
context_sources: [AGENTS.md, .codex/AGENTS.md, .codex/delivery/specs/organization-department-access-and-contributor-insights.md, custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, docs/architecture/system-design.md, docs/architecture/bounded-context-map.md, packages/contracts/routes/ui-route-contracts.json]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W17-PEOPLE-CONTRIBUTOR-ACTIVITY-PROJECTION.md, .codex/delivery/evidence/W17-PEOPLE-CONTRIBUTOR-ACTIVITY-PROJECTION.md, packages/identity_access/**, packages/presentation/**, apps/api/src/custometry_api/people/**, apps/api/src/custometry_api/main.py, apps/api/src/custometry_api/config.py, apps/api/pyproject.toml, packages/contracts/people/**, packages/contracts/openapi/**, packages/contracts/schemas/**, packages/contracts/src/**, docs/contracts/contract-drift.json, pyproject.toml, uv.lock, migrations/versions/*_contributor_projection.py, tests/unit/contributor_projection/**, tests/contract/contributor_projection/**, tests/integration/contributor_projection/**]
  forbidden_write_paths: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, apps/web/**, packages/contracts/routes/**, packages/audit/**, deploy/**]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: api
  proof_skills: [backend-quality-gates]
  commands: [focused redaction aggregation and visibility property tests, real PostgreSQL projection rebuild and idempotency tests, authenticated People API variants for self leader grantee viewer and administrator, negative hidden title count PII raw audit ranking and cross-workspace tests, migration DDD contract and local gates, git diff --check]
  proof_boundary: privacy-safe-contributor-projection-and-policy-filtered-people-api
  evidence_target: .codex/delivery/evidence/W17-PEOPLE-CONTRIBUTOR-ACTIVITY-PROJECTION.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

The People API returns only access-filtered creator identity, visible resources,
and bounded activity aggregates appropriate to the caller's self, leadership,
grant, or ordinary-viewer scope.

# Non-goals

- Do not implement Web visuals, Penpot, raw Audit browsing, ranking, productivity
  scoring, HR decisions, or exact-login surveillance.

# Work and repair boundary

Build the allowlisted redacted projection from domain events through owner
ports. Audit remains accountability evidence and is not an employee analytics
database.

# Acceptance evidence

Requires real projection/API observations, rebuild/idempotency proof, exhaustive
negative privacy cases, migration and boundary gates, and no browser claim.
