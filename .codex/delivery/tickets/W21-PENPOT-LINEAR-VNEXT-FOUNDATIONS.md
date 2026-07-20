---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W21-PENPOT-LINEAR-VNEXT-FOUNDATIONS
status: draft
workstream_id: W21
summary: Create and accept a separate Custometry Penpot vNext file for the four-theme Linear-workspace foundations, shell, representative components, states, resizable panels, and Sales Analytics golden slice without rewriting W10 evidence.
requirement_ids: [WEB-ARCH-003, WEB-ARCH-005, WEB-ARCH-006, THEME-001, THEME-002, THEME-003, THEME-005, THEME-008, MOTION-001, MOTION-002, MOTION-003, MOTION-011, MOTION-012, A11Y-001, A11Y-003]
blockers: [W19-LINEAR-REFERENCE-COMPLETION, W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/delivery/specs/custometry-linear-workspace-ui-transition.md
  - .codex/delivery/tickets/W19-LINEAR-REFERENCE-COMPLETION.md
  - .codex/delivery/tickets/W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/ui/linear-workspace-ui-transition-standard-v1.md
  - docs/architecture/ui/linear-workspace-reference-manifest-v1.json
  - docs/architecture/ui/custometry-linear-ui-migration-registry-v1.json
start_probe:
  boundary: Penpot MCP and the separately named Custometry Web UI Linear Workspace v0.7 file
  read_only_check: confirm Penpot availability and determine whether the exact vNext file exists; never write to the W10 canonical historical file
  stop_on: [unavailable, identity_mismatch, state_drift]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W21-PENPOT-LINEAR-VNEXT-FOUNDATIONS.md
    - .codex/delivery/evidence/W21-PENPOT-LINEAR-VNEXT-FOUNDATIONS.md
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
  proof_skills: [penpot-design-delivery]
  commands:
    - calculate the ordered SHA-256 fingerprint of every context source before the first Penpot write and repeat it before acceptance
    - create or update only the separately identified vNext Penpot file and stop on concurrent revision drift
    - inspect every target foundation component representative frame theme state and changed region at useful zoom
    - validate stable Custometry UI IDs no duplicate or orphan target IDs component references panel constraints button alignment and four-theme representative coverage
    - record the canonical vNext file ID and terminal revision in the allowed UI blueprint and migration registry paths
    - uv run python -m tools.custometry_quality.validate_blueprints
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - git diff --check
  proof_boundary: accepted-separate-penpot-vnext-four-theme-linear-workspace-foundations-and-golden-slice-design
  evidence_target: .codex/delivery/evidence/W21-PENPOT-LINEAR-VNEXT-FOUNDATIONS.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

A new Penpot file—not the historical W10 artifact—defines the implementable
four-theme foundations, shell, component states, responsive panel constraints,
and representative Sales Analytics composition for the runtime transition.

# Non-goals

- Do not change product semantics, route identity, backend code, or W10 evidence.
- Do not claim browser, runtime accessibility, API, or performance readiness.

# Work and repair boundary

Create Foundations, Components, Patterns, Shell, state matrices, resizable
sidebar/detail surfaces, and the representative theme/accessibility/motion
frames needed by W22 and W23. Preserve Custometry branding and domain copy.

# Acceptance evidence

Evidence records exact file identity, start/end revisions, source fingerprint,
frame/component inventory, visual inspection, known non-runtime limits, and the
implementation handoff for W22.
