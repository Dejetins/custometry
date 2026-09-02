---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W16-SALES-CUSTOMER-RFM-API-PROJECTIONS
status: accepted
workstream_id: W16
summary: Produce governed sales, customer-base, and RFM reportable results with previous-year comparison, typed filters, compact metric groups, and policy-filtered API projections.
requirement_ids: [UC-004, UC-012, COMPARE-001, COMPARE-002, COMPARE-003, COMPARE-004, COMPARE-005, COMPARE-006, COMPARE-007, MART-GRAIN-001, MART-GRAIN-002, MART-GRAIN-003, MART-GRAIN-004, MART-GRAIN-005, MART-GRAIN-006, MART-GRAIN-007]
blockers: []
context_sources: [AGENTS.md, .codex/AGENTS.md, custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, docs/architecture/system-design.md, docs/architecture/bounded-context-map.md, packages/contracts/routes/ui-route-contracts.json]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W16-SALES-CUSTOMER-RFM-API-PROJECTIONS.md, .codex/delivery/evidence/W16-SALES-CUSTOMER-RFM-API-PROJECTIONS.md, packages/analytics_core/**, packages/analytics_sales/**, packages/analytics_customer/**, apps/api/src/custometry_api/analytics/**, apps/api/src/custometry_api/main.py, apps/api/src/custometry_api/config.py, apps/api/pyproject.toml, apps/api/Dockerfile, packages/contracts/analytics/**, packages/contracts/openapi/**, packages/contracts/schemas/**, packages/contracts/src/**, docs/contracts/contract-drift.json, pyproject.toml, uv.lock, migrations/versions/*_analytics_projection.py, tests/unit/analytics/**, tests/contract/analytics/**, tests/integration/analytics/**]
  forbidden_write_paths: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, apps/web/**, packages/contracts/routes/**, packages/forecasting/**, packages/report_delivery/**]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: api
  proof_skills: [backend-quality-gates]
  commands: [focused metric filter comparison and RFM property tests, golden analytical expectations against deterministic retail data, real PostgreSQL and artifact result integration, authenticated API contract and negative visibility tests, repeated-run identity and immutable manifest proof, DDD contract drift and local gates, git diff --check]
  proof_boundary: governed-sales-customer-rfm-reportable-result-and-api-projection
  evidence_target: .codex/delivery/evidence/W16-SALES-CUSTOMER-RFM-API-PROJECTIONS.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W16-SALES-CUSTOMER-RFM-API-PROJECTIONS.md]
---

# Outcome

Authorized consumers receive reproducible sales, customer, and RFM API results
with exact current/`vs LY` semantics, typed filters, ordered metrics, freshness,
quality, lineage, and no hidden-object count leakage.

# Non-goals

- Do not implement browser screens, forecasting, report email/XLSX, clustering,
  or causal inference.

# Work and repair boundary

Own analytical domain/application policies and API projections; reuse accepted
semantic/DQ/artifact/access ports and never query another context's private
tables.

# Acceptance evidence

Requires golden numerical expectations, property/invariant tests, real result
identity and API authorization evidence, and no browser claim.
