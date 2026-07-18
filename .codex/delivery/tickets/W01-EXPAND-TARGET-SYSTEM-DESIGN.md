---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.0-draft
ticket_id: W01-EXPAND-TARGET-SYSTEM-DESIGN
status: accepted
workstream_id: W01
summary: Project product specification 0.9.0 into the target architecture, a complete bounded-context dependency map, an executable 96-route contract, and a visually verified System Design DOCX.
requirement_ids: [ARCH-PRINCIPLE-001, METHOD-001, CONNECTOR-001, REPORT-003, REPORT-012, METRIC-010, RBAC-002, RBAC-006, RBAC-009, RBAC-010, RBAC-011, RBAC-013, RBAC-014, RBAC-015, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, PRIVATE-FUTURE-001, PRIVATE-FUTURE-002, PRIVATE-FUTURE-005]
blockers: []
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/system-design.md
  - docs/architecture/bounded-context-map.md
  - packages/contracts/routes/ui-routes.json
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W01-EXPAND-TARGET-SYSTEM-DESIGN.md
    - .codex/delivery/evidence/W01-EXPAND-TARGET-SYSTEM-DESIGN.md
    - custometry-ui-blueprint-ru.md
    - docs/architecture/README.md
    - docs/architecture/system-design.md
    - docs/architecture/bounded-context-map.md
    - docs/architecture/custometry-foundation-system-design.docx
    - docs/architecture/custometry-system-design.docx
    - docs/contracts/README.md
    - docs/contracts/ui-route-contract.md
    - docs/README.md
    - packages/contracts/routes/ui-routes.json
    - packages/contracts/routes/ui-route-contracts.json
    - packages/contracts/routes/ui-route-contracts.schema.json
    - tools/custometry_quality/validate_route_registry.py
    - tests/tooling/test_static_quality_tools.py
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
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
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.check_docs_links
    - uv run python -m tools.check --scope local
    - render the canonical DOCX and inspect every page image
  proof_boundary: target-architecture-route-contract-and-docx-static
  evidence_target: .codex/delivery/evidence/W01-EXPAND-TARGET-SYSTEM-DESIGN.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W01-EXPAND-TARGET-SYSTEM-DESIGN.md]
---

# Outcome

The accepted architecture projects the complete 0.9.0 product boundary into
DDD ownership, cross-context flows, security and distribution boundaries. A
schema-validated executable route contract covers every canonical UI route and
the companion DOCX is regenerated from the Markdown source and visually clean.

# Non-goals

- Do not implement product routes, APIs, persistence, workers, connectors, or renderers.
- Do not claim browser, database, Compose, recovery, performance, release, or deployment readiness.
- Do not add a standing plan, ledger, prompt pack, cloud topology, or public activation runtime.

# Work and repair boundary

Expand only the accepted architecture and route-contract surfaces. Keep the
compact route identity registry stable and add a separate executable contract
when this avoids coupling runtime URL identity to screen policy metadata.
Compatible validator, schema, documentation, and DOCX repairs are allowed
inside the declared paths; rerun every invalidated static check and the visual
render gate.

# Acceptance evidence

- System Design covers the material 0.9.0 contexts, flows, trust boundaries,
  compatibility, migration, rollback, and proof limits without duplicating the
  normative blueprint.
- The bounded-context map has explicit ownership and dependency rules for
  methodology/research, object access/comments, branding/company packs,
  formatting, imports, reporting, delivery, notifications, and audit.
- All 96 route-level pages have one schema-valid executable route contract
  consistent with the identity registry, UI blueprint roles, localization, and
  Penpot synchronization status.
- Focused validators and the grouped local gate pass.
- The regenerated System Design DOCX contains the complete target design and
  every rendered page passes visual inspection.
