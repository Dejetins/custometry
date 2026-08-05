---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W21-FIGMA-MASTER-ELEMENTS-INDEX
status: superseded
workstream_id: W21
summary: Create the Custometry Figma Master Elements Index frame that turns the UI blueprint, route registry, roles, states, and design-standard requirements into a traceable design-system coverage contract before detail maps or screens are produced.
requirement_ids: [WEB-ARCH-003, WEB-ARCH-005, WEB-ARCH-006, THEME-001, THEME-002, THEME-003, THEME-005, THEME-008, MOTION-001, MOTION-002, MOTION-003, MOTION-011, MOTION-012, A11Y-001, A11Y-003]
blockers: []
supersession_reason: The accepted contract-compiled UI prototyping plan replaces the index-first separate-agent workflow with a slice-first restricted manifest, deterministic renderer, read-back audit, and reproducibility pilot on UI-AN-003; W21-CONTRACT-COMPILED-UI-PILOT is the executable successor.
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-surface-contracts.json
start_probe:
  boundary: internal Figma platform agent workspace and the existing Custometry platform web ui Figma file
  read_only_check: confirm the Figma-side agent can open https://www.figma.com/design/ghv0Cv3ddqMvv3zFVvR22p/Custometry-platform-web-ui, locate or create exactly one Master Elements Index frame, and return file identity plus exportable review artifacts; Codex must not use Figma MCP for writes in this ticket
  stop_on: [unavailable, identity_mismatch, state_drift]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W21-FIGMA-MASTER-ELEMENTS-INDEX.md
    - .codex/delivery/evidence/W21-FIGMA-MASTER-ELEMENTS-INDEX.md
    - .codex/agents/generated/w21-figma-master-elements-index/**
    - custometry-ui-blueprint-ru.md
    - docs/architecture/ui/custometry-linear-ui-migration-registry-v1.json
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - apps/**
    - packages/**
    - migrations/**
    - deploy/**
    - .codex/delivery/graphs/**
    - .codex/delivery/evidence/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: [prompt-manager, product-design:audit]
  commands:
    - calculate the ordered SHA-256 fingerprint of every context source before releasing the Figma-agent prompt and repeat it before acceptance
    - create or update only the repository-local prompt artifact for the internal Figma platform agent
    - require the internal Figma agent to return file URL or key, index frame node ID, index frame export, machine-readable index report, duplicate audit, clipping/overlap audit, and planned detail-map coverage
    - verify the index traces primitives, capabilities, overlays, system states, route families, required states, role/access boundaries, requirement IDs, and future detail maps without creating product screens
    - verify no duplicate index frame exists and no element or map is marked accepted without product-owner approval
    - record the canonical Figma file identity and accepted index boundary in the allowed UI blueprint and migration registry paths
    - uv run python -m tools.custometry_quality.validate_blueprints
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - git diff --check
  proof_boundary: accepted-internal-figma-agent-master-elements-index-frame-with-codex-review-handoff
  evidence_target: .codex/delivery/evidence/W21-FIGMA-MASTER-ELEMENTS-INDEX.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W21-FIGMA-MASTER-ELEMENTS-INDEX.md]
---

# Outcome

The existing Custometry Figma file contains exactly one dedicated Master
Elements Index frame that records stable primitive IDs, detail-map IDs, route
and surface coverage, required states, role/access boundaries, product-review
status, and next design slices. It is a design-system coverage contract, not a
screen mockup.

# Non-goals

- Do not create full product screens, detailed maps, route frames, or a complete
  prototype in this ticket.
- Do not use Codex or repository MCP tools to mutate Figma in this ticket.
- Do not change product semantics, route identity, backend code, runtime code,
  REST/SSE contracts, persistence, or W10 historical evidence.
- Do not mark any primitive, map, or screen `accepted` without explicit
  product-owner approval.
- Do not copy Linear branding, product entities, private assets, source code,
  or undocumented authorization behavior.

# Work and repair boundary

Own the prompt, handoff, and review boundary for the Figma-side Master Elements
Index. The internal Figma platform agent owns creation or update of the single
index frame in the existing Figma file. Detail maps and screens are recorded as
planned or review items only and must not be created unless a later ticket
authorizes that slice.

# Acceptance evidence

Evidence records the prompt artifact path, exact context-source fingerprint,
Figma file identity or URL, index frame node ID, returned inventory, duplicate
audit, clipping/overlap audit, primitive/map/status coverage, required fixes or
waivers, known non-runtime limits, and the next safe detail-map prompt.
