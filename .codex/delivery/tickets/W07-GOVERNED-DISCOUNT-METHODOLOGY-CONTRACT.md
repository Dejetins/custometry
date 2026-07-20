---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.2-draft
ticket_id: W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT
status: accepted
workstream_id: W07
summary: Add one governed discount-component, cap, price-volume-mix, metric-trust, and methodology-availability contract across product, UI, architecture, and executable UI manifests without adding a route or modifying Penpot.
requirement_ids: [UC-027, METRIC-017, METRIC-018, METRIC-019, METRIC-020, DISCOUNT-001, DISCOUNT-002, DISCOUNT-003, DISCOUNT-004, DISCOUNT-005, DISCOUNT-006, DISCOUNT-007, DISCOUNT-008, DISCOUNT-009, DISCOUNT-010, DISCOUNT-011, DISCOUNT-012, DISCOUNT-013, DISCOUNT-014, DISCOUNT-015, DISCOUNT-016, DISCOUNT-017, DISCOUNT-018, DISCOUNT-019, DISCOUNT-020, METHOD-009, METHOD-010, METHOD-011, METHOD-012, METHOD-013, METHOD-014, MART-GRAIN-008, PVM-001, PVM-002, PVM-003, PVM-004, PVM-005, PVM-006, TEST-INV-066, TEST-INV-067, TEST-INV-068, TEST-INV-069, TEST-INV-070, TEST-INV-071, TEST-INV-072, TEST-INV-073, TEST-INV-074, TEST-INV-075, V1-AC-032, V1-AC-033, V1-AC-034, V1-AC-035, V1-AC-036]
blockers: [W06-PENPOT-ANALYTICS-DENSITY-REPAIR]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/system-design.md
  - docs/architecture/bounded-context-map.md
  - docs/contracts/ui-route-contract.md
  - docs/contracts/ui-surface-contract.md
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-surface-contracts.json
  - .codex/delivery/tickets/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
  - .codex/delivery/evidence/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
change_scope:
  allowed_write_paths:
    - .codex/agents/iteration_report_template.md
    - .codex/agents/spec_template.md
    - .codex/agents/ticket_template.md
    - .codex/delivery/tickets/W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT.md
    - .codex/delivery/evidence/W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT.md
    - .codex/delivery/tickets/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
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
    - packages/contracts/routes/ui-route-contracts.json
    - packages/contracts/routes/ui-surface-contracts.json
  forbidden_write_paths:
    - apps/**
    - plugins/**
    - deploy/**
    - migrations/**
    - packages/**/src/**
    - packages/contracts/routes/ui-routes.json
    - packages/localization/**
    - .codex/delivery/tickets/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/tickets/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
    - .codex/delivery/evidence/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: []
  commands:
    - uv run python -m tools.custometry_quality.validate_blueprints
    - uv run python -m tools.custometry_quality.generate_requirement_index --check
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.check_docs_links
    - uv run python -m tools.custometry_quality.generate_docs_index --check
    - uv run python -m tools.check --scope local
    - pnpm check
    - git diff --check
  proof_boundary: static-discount-methodology-product-ui-architecture-and-executable-contract-synchronization
  evidence_target: .codex/delivery/evidence/W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence:
  - .codex/delivery/evidence/W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT.md
---

# Outcome

Product `0.9.2-draft` and UI `0.6.2-draft` define one company-configurable,
receipt-line discount workflow from mapping and effective policy through
component reconciliation, stacking/cap diagnostics, exact PVM, metric trust,
research, Result Trust, and export disclosure. Promotion, loyalty, bonus
redemption, other discount, commercial discount, customer benefit, and
recognized net revenue remain distinct. Metric certification and method
availability are explicit; future methods are not runnable claims.

# Non-goals

- Do not implement persistence, API, workers, analytics, browser UI, email,
  XLSX, migrations, or benchmark claims.
- Do not modify Penpot or rewrite W05/W06 historical evidence.
- Do not add a route/overlay, customer-specific code fork, marketing execution,
  automatic causal inference, or future causal/uplift/anomaly runtime.
- Do not hard-code the first-client 50% cap or stacking defaults in platform
  core; preserve them only as a versioned CompanyPack/policy example.

# Work and repair boundary

Extend the synchronized blueprints, target architecture, route execution
references, and surface coverage manifest in place. Preserve 110 route IDs, 25
overlays, and 5 system surfaces. Mark all 110 route frames as the accepted W05
Penpot baseline and record W06 revision 164 as the current visual predecessor.
Add `UI-CAP-020` and `UC-027` coverage without claiming the new content delta
is already present in Penpot.

# Acceptance evidence

- Machine and human blueprints share product version `0.9.2-draft` and the same
  complete 890 requirement IDs.
- UI version `0.6.2-draft` keeps 110 routes, 25 overlays, 5 systems, and adds
  exactly one twentieth reusable capability plus the twenty-seventh use-case
  binding.
- Architecture assigns reusable policy/certification to Semantic Model,
  diagnostics/PVM to Analytics, evidence to DQ, promotion context to Promotion
  Journal, method availability to Methodology & Research, and presentation to
  report adapters without cross-context private-table ownership.
- Historical cap breaches are immutable diagnostics; simulated breaches block
  publication; PVM reconciles exactly; proxy/partial/future states are visible.
- Static validators, schemas, docs links/indexes, local gate, pnpm gate, and
  whitespace checks pass. No runtime, browser, Penpot, analytical-correctness,
  performance, or release proof is claimed.
