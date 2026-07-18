---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.1-draft
ticket_id: W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT
status: accepted
workstream_id: W04
summary: Add one governed population-treatment and segmentation contract across product, UI, architecture, and executable UI surface manifests without changing the canonical route inventory or Penpot file.
requirement_ids: [UC-025, UC-026, OUTLIER-001, OUTLIER-002, OUTLIER-003, OUTLIER-004, OUTLIER-005, OUTLIER-006, OUTLIER-007, OUTLIER-008, OUTLIER-009, OUTLIER-010, OUTLIER-011, OUTLIER-012, SEGMENT-001, SEGMENT-002, SEGMENT-003, SEGMENT-004, SEGMENT-005, SEGMENT-006, SEGMENT-007, SEGMENT-008, SEGMENT-009, SEGMENT-010, SEGMENT-011, SEGMENT-012, SEGMENT-013, SEGMENT-014, SEGMENT-015, SEGMENT-016, SEGMENT-017, SEGMENT-018, TEST-INV-061, TEST-INV-062, TEST-INV-063, TEST-INV-064, TEST-INV-065, V1-AC-029, V1-AC-030, V1-AC-031]
blockers: []
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
  - .codex/delivery/evidence/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT.md
    - .codex/delivery/evidence/W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT.md
    - .codex/agents/spec_template.md
    - .codex/agents/ticket_template.md
    - .codex/agents/iteration_report_template.md
    - .gitignore
    - README.md
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - docs/architecture/README.md
    - docs/architecture/system-design.md
    - docs/architecture/bounded-context-map.md
    - docs/contracts/ui-route-contract.md
    - docs/contracts/ui-surface-contract.md
    - docs/generated/requirement-index.json
    - docs/README.md
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
    - packages/contracts/tests/routes.test.ts
    - packages/localization/tests/parity.test.ts
  forbidden_write_paths:
    - apps/**
    - plugins/**
    - deploy/**
    - migrations/**
    - packages/**/src/**
    - .codex/delivery/tickets/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
    - .codex/delivery/evidence/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
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
    - uv run python -m tools.check --scope local
    - pnpm check
    - git diff --check
  proof_boundary: static-product-ui-architecture-and-executable-contract-synchronization
  evidence_target: .codex/delivery/evidence/W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence:
  - .codex/delivery/evidence/W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT.md
---

# Outcome

Custometry specification `0.9.1-draft` and UI specification `0.6.1-draft`
define one reproducible workflow from population selection through governed
outlier treatment to rule, bucket, stratified, or KMeans segmentation. The
same versions, bounds, diagnostics, membership snapshots, permissions, and
Result Trust evidence are usable by analyses, research, segments, reports,
email, and XLSX. Executable UI contracts bind the behavior to existing routes
plus typed reusable surfaces without adding a route solely for a control.

# Non-goals

- Do not implement analytics, persistence, API, workers, browser UI, or exports.
- Do not edit Penpot or revise accepted W03 evidence for its fixed revision-124
  and repository-input snapshot.
- Do not add HDBSCAN, Gaussian Mixture, automatic K selection, Isolation Forest,
  or multivariate anomaly detection to the v1 implementation scope.
- Do not mutate canonical source data or canonical metric definitions through
  an outlier policy.

# Work and repair boundary

Extend the accepted draft specifications and architecture in place. Preserve
the 110-route identity inventory. Add one contextual data-treatment editor and
two cross-surface capabilities, and bind the new use cases to existing guided
analysis, Custom Builder, result, research, and segment routes. Treat W03 as
historical evidence: its fingerprint and Penpot findings remain true for its
captured baseline, while later Penpot work consumes this additive delta.

# Acceptance evidence

- Machine and human blueprints share the same product version and complete new
  requirement-ID set.
- UI workflow explains population, treatment, method, preview, publication,
  monitoring, privacy, accessibility, and non-route ownership.
- Route count and canonical paths remain unchanged; executable route sources
  and surface coverage resolve `UC-025` and `UC-026` exactly once.
- Architecture assigns Analytics ownership, ports, persistence, dependencies,
  compatibility, rollback, CPU/performance, and proof boundaries.
- `docs/architecture/system-design.md` is the sole maintained System Design
  source; generated binary mirrors are ignored, unversioned, and not required
  for acceptance.
- Focused schemas, validators, docs links, grouped local checks, and cold
  self-review pass.
