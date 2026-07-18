---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.0-draft
ticket_id: W02-RECONCILE-UI-SURFACE-CONTRACT
status: accepted
workstream_id: W02
summary: Reconcile every UI-visible 0.9.0 requirement with an explicit route, overlay, system surface, or cross-surface capability and prepare one ready Penpot architecture delta audit ticket.
requirement_ids: [UC-015, UC-017, UC-018, UC-019, UC-020, UC-021, UC-022, UC-023, UC-024, METRIC-009, METRIC-014, METHOD-001, RESEARCH-001, DASHBOARD-001, REPORT-001, XLSX-001, BRAND-001, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012]
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
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-surface-contracts.json
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W02-RECONCILE-UI-SURFACE-CONTRACT.md
    - .codex/delivery/evidence/W02-RECONCILE-UI-SURFACE-CONTRACT.md
    - .codex/delivery/tickets/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - docs/README.md
    - docs/architecture/README.md
    - docs/architecture/bounded-context-map.md
    - docs/architecture/system-design.md
    - docs/architecture/custometry-system-design.docx
    - docs/contracts/README.md
    - docs/contracts/ui-route-contract.md
    - docs/contracts/ui-surface-contract.md
    - docs/generated/requirement-index.json
    - packages/contracts/routes/ui-routes.json
    - packages/contracts/routes/ui-route-contracts.json
    - packages/contracts/routes/ui-route-contracts.schema.json
    - packages/contracts/routes/ui-surface-contracts.json
    - packages/contracts/routes/ui-surface-contracts.schema.json
    - packages/localization/locales/en/route-titles.json
    - packages/localization/locales/ru/route-titles.json
    - tools/custometry_quality/validate_route_registry.py
    - tests/tooling/test_static_quality_tools.py
  forbidden_write_paths:
    - apps/**
    - plugins/**
    - deploy/**
    - migrations/**
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: []
  commands:
    - uv run pytest -q tests/tooling/test_static_quality_tools.py -k route_registry
    - uv run pytest -q tests/tooling/test_static_quality_tools.py
    - uv run ruff check tools/custometry_quality/validate_route_registry.py tests/tooling/test_static_quality_tools.py
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
    - uv run python -m tools.custometry_quality.validate_blueprints
    - uv run python -m tools.custometry_quality.generate_requirement_index --check
    - uv run python -m tools.custometry_quality.generate_docs_index --check
    - uv run python -m tools.custometry_quality.validate_delivery_contract
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.check_docs_links
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: static-ui-route-surface-traceability-and-ready-audit-handoff
  evidence_target: .codex/delivery/evidence/W02-RECONCILE-UI-SURFACE-CONTRACT.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence:
  - .codex/delivery/evidence/W02-RECONCILE-UI-SURFACE-CONTRACT.md
---

# Outcome

The 0.9.0 UI baseline has no silent route-count ceiling. Every UI-visible use
case and required interaction is traceable to a canonical route, overlay,
system surface, or cross-surface capability, with explicit rationale for
route-backed versus transient behavior. A separate ready ticket can execute
the Penpot delta audit without making unresolved product or route decisions.

# Non-goals

- Do not edit Penpot, generate frames, or claim design synchronization.
- Do not implement Web routes, API handlers, persistence, workers, or exports.
- Do not change normative product scope or create a standing plan, ledger,
  prompt pack, or platform Goal.
- Do not preserve the previous 96-route count merely to match the existing
  Penpot baseline.

# Work and repair boundary

Audit the normative product use cases and UI requirements against every
browser-visible surface. Add route-backed pages only when a durable entity,
bookmark/history contract, notification/audit deep link, or complex independent
permission boundary requires them. Keep transient actions as typed overlays and
reusable behavior as cross-surface capability contracts. Extend static
validators so list parity alone cannot be reported as complete coverage.

# Acceptance evidence

- Every `UC-001...UC-024` has one or more explicit UI surface bindings or an
  explicit non-UI rationale.
- Every route, overlay, system surface, and cross-surface capability in the UI
  blueprint has a machine-readable identity and requirement binding.
- Route additions are synchronized across identity, execution, localization,
  documentation, schemas, and validators.
- The Penpot audit ticket names the canonical file ID, immutable sources,
  permitted writes, stop conditions, complete coverage matrix, and acceptance
  evidence without treating the current frame count as a ceiling.
- Focused validators, JSON Schema checks, documentation links, the grouped
  local gate, and an independent cold review pass.
