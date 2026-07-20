---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
ticket_id: W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT
status: accepted
workstream_id: W09
summary: Synchronize the organization hierarchy, department access and ownership, and privacy-safe People & Creators capability across product, UI, architecture, executable routes, surface coverage, and localization without modifying Penpot or runtime code.
requirement_ids: [UC-028, UC-029, RBAC-019, RBAC-020, RBAC-021, RBAC-022, RBAC-023, RBAC-024, RBAC-025, RBAC-026, RBAC-027, RBAC-028, TEST-INV-076, TEST-INV-077, TEST-INV-078, TEST-INV-079, TEST-INV-080, TEST-INV-081, TEST-INV-082, TEST-INV-083, TEST-INV-084, TEST-INV-085, TEST-INV-086, TEST-INV-087, TEST-INV-088, V1-AC-037, V1-AC-038, V1-AC-039, V1-AC-040, V1-AC-041, V1-AC-042, V1-AC-043]
blockers: [W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/agents/iteration_report_template.md
  - .codex/agents/spec_template.md
  - .codex/agents/ticket_template.md
  - .codex/delivery/specs/organization-department-access-and-contributor-insights.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/system-design.md
  - docs/architecture/bounded-context-map.md
  - docs/contracts/ui-route-contract.md
  - docs/contracts/ui-surface-contract.md
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-route-contracts.schema.json
  - packages/contracts/routes/ui-surface-contracts.json
  - packages/contracts/routes/ui-surface-contracts.schema.json
  - packages/localization/locales/en/route-titles.json
  - packages/localization/locales/ru/route-titles.json
  - .codex/delivery/tickets/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
  - .codex/delivery/evidence/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
change_scope:
  allowed_write_paths:
    - .codex/agents/iteration_report_template.md
    - .codex/agents/spec_template.md
    - .codex/agents/ticket_template.md
    - .codex/delivery/specs/organization-department-access-and-contributor-insights.md
    - .codex/delivery/tickets/W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT.md
    - .codex/delivery/evidence/W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT.md
    - .codex/delivery/tickets/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
    - README.md
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - docs/README.md
    - docs/architecture/README.md
    - docs/architecture/system-design.md
    - docs/architecture/bounded-context-map.md
    - docs/contracts/ui-route-contract.md
    - docs/contracts/ui-surface-contract.md
    - docs/generated/requirement-index.json
    - docs-site/docs/index.md
    - docs-site/docs/install/local.md
    - docs-site/docs/install/network-boundary.md
    - docs-site/docs/user-guide/foundation.md
    - docs-site/docs/ru/index.md
    - docs-site/docs/ru/install/local.md
    - docs-site/docs/ru/install/network-boundary.md
    - docs-site/docs/ru/user-guide/foundation.md
    - packages/contracts/routes/ui-routes.json
    - packages/contracts/routes/ui-route-contracts.json
    - packages/contracts/routes/ui-surface-contracts.json
    - packages/contracts/tests/routes.test.ts
    - packages/localization/locales/en/route-titles.json
    - packages/localization/locales/ru/route-titles.json
    - packages/localization/tests/parity.test.ts
  forbidden_write_paths:
    - apps/**
    - plugins/**
    - deploy/**
    - migrations/**
    - packages/**/src/**
    - .codex/delivery/tickets/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/tickets/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
    - .codex/delivery/evidence/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
    - .codex/delivery/tickets/W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT.md
    - .codex/delivery/evidence/W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT.md
    - .codex/delivery/tickets/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: []
  commands:
    - confirm W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION is accepted with passed evidence at canonical Penpot revision 181
    - uv run python -m tools.custometry_quality.validate_blueprints
    - uv run python -m tools.custometry_quality.generate_requirement_index --check
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
    - uv run python -m tools.custometry_quality.check_i18n_parity
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.check_docs_links
    - uv run python -m tools.custometry_quality.generate_docs_index --check
    - uv run --locked pytest -q tests/tooling/test_static_quality_tools.py -k 'blueprint or route_registry or delivery_ticket or i18n'
    - uv run python -m tools.check --scope local
    - uv run python -m tools.check --scope ci
    - pnpm check
    - git diff --check
  proof_boundary: static-organization-access-ownership-contributor-product-ui-architecture-and-executable-contract-synchronization
  evidence_target: .codex/delivery/evidence/W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence:
  - .codex/delivery/evidence/W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT.md
---

# Outcome

Product `0.9.3-draft` and UI `0.6.3-draft` define one governed organization
tree, primary-department assignment model, explicit leadership scope,
department data/access policy, bounded cross-department grants, durable resource
ownership, and privacy-safe People & Creators experience. The static contract
adds six route identities, two reusable capabilities, localization, and
acceptance invariants while preserving W08's accepted Penpot revision `181` as
the visual baseline.

# Non-goals

- Do not modify Penpot, create browser UI, implement persistence/API/policy
  evaluation, build activity projections, or add migrations.
- Do not infer data or employee-activity access from a functional administrator
  role, job title, or organization membership alone.
- Do not add employee ranking, productivity scoring, login surveillance, raw
  audit browsing, HR decisions, HRIS/SCIM/OIDC synchronization, matrix
  reporting, physical per-department dataset duplication, or B2B hierarchy.
- Do not claim runtime, browser, accessibility-runtime, authorization,
  persistence, migration, performance, recovery, or release proof.

# Work and repair boundary

Synchronize the normative machine blueprint and human mirror, UI workflow,
architecture ownership and ports, six-route identity/execution registry,
surface/use-case coverage, EN/RU route titles, generated requirement/docs
indexes, and repository version references. Keep Identity, Organization &
Access inside the modular monolith rather than creating a new deployable
service. Counts and activity projections must be described as authorization-
filtered before aggregation and pagination. Audit remains accountability
evidence and is not an employee analytics database.

The six routes remain `penpot_status: backlog` until W10 proves their visual
implementation. Existing 110 route frames, 25 overlays, and 5 system surfaces
remain the W08 baseline; W09 changes the target route inventory to 116 without
claiming the six new frames exist in Penpot.

# Acceptance evidence

- Machine and human blueprints share product version `0.9.3-draft` and the same
  complete requirement-ID set.
- The executable registry contains exactly 116 routes, 25 overlays, 5 system
  surfaces, 22 cross-surface capabilities, and 29 use-case bindings; exactly
  six routes are the W10 Penpot backlog.
- Route identity, execution policy, EN/RU localization, surface coverage, and
  JSON Schema validation agree for all six new routes.
- Architecture assigns organization/access/ownership decisions to Identity,
  Organization & Access and exposes only privacy-safe contributor projections
  to Presentation & Reports.
- Static validators, generated indexes, focused tests, local/CI profiles, pnpm
  checks, and whitespace checks pass. No Penpot or runtime proof is claimed.
