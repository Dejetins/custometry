---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W19-LINEAR-REFERENCE-COMPLETION
status: accepted
workstream_id: W19
summary: Complete the sanitized, reproducible Linear reference evidence needed to measure geometry, motion, keyboard behavior, accessibility structure, state continuity, and the four Custometry themes before design or runtime implementation begins.
requirement_ids: [WEB-ARCH-005, WEB-ARCH-006, WEB-PERF-001, WEB-PERF-002, THEME-001, THEME-008, A11Y-001, A11Y-003, MOTION-001, MOTION-012]
blockers: []
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/delivery/specs/custometry-linear-workspace-ui-transition.md
  - docs/architecture/ui/linear-workspace-ui-transition-standard-v1.md
  - docs/architecture/ui/linear-workspace-reference-manifest-v1.json
  - docs/architecture/ui/custometry-linear-ui-migration-registry-v1.json
  - custometry-ui-blueprint-ru.md
start_probe:
  boundary: user-supplied local Linear reference archive
  read_only_check: confirm that /Users/daniildegtyarev/Downloads/reference.zip exists and its SHA-256 is eb7b0ab070f64d553baafacefa90fdb2e87e51bc174c63db9af73bc77f8e41c2 before any capture or measurement work
  stop_on: [unavailable, identity_mismatch, state_drift]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W19-LINEAR-REFERENCE-COMPLETION.md
    - .codex/delivery/evidence/W19-LINEAR-REFERENCE-COMPLETION.md
    - docs/architecture/ui/linear-workspace-reference-manifest-v1.json
    - docs/architecture/ui/linear-workspace-reference-measurements-v1.md
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - apps/**
    - packages/**
    - deploy/**
    - migrations/**
    - .codex/delivery/tickets/W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE.md
    - .codex/delivery/graphs/**
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills: [browser-qa-evidence, playwright]
  commands:
    - verify the archive and every existing screenshot hash without committing third-party captures or authentication state
    - capture or derive the missing command palette, focus order, sidebar resize, route, pane, modal, popover, loading, stale, error, forbidden, and session-expired evidence with viewport and scale metadata
    - record sanitized accessibility snapshots, component geometry, motion timings, and explicit evidence gaps or waivers
    - validate that no cookies, tokens, raw browser state, account data, third-party screenshots, or recordings are tracked
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - git diff --check
  proof_boundary: sanitized-reproducible-linear-reference-measurements-and-evidence-gap-closure
  evidence_target: .codex/delivery/evidence/W19-LINEAR-REFERENCE-COMPLETION.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W19-LINEAR-REFERENCE-COMPLETION.md]
---

# Outcome

Custometry has a sanitized and reproducible reference pack sufficient to make
the Linear-fidelity target measurable before Penpot or production UI work.

# Non-goals

- Do not copy Linear assets, wording, source code, authorization behavior, or
  product entities.
- Do not change Penpot, product code, routes, backend contracts, or requirements.
- Do not commit screenshots, recordings, cookies, tokens, or browser profiles.

# Work and repair boundary

Hash all inputs, record exact viewport/scale and measured geometry, describe
observable interaction sequences, and capture sanitized Playwright/ARIA and
performance observations where the authenticated reference session permits it.
Every missing item is either closed or explicitly waived with impact before the
ticket may be accepted.

# Acceptance evidence

Terminal evidence identifies inputs, hashes, browser/build metadata, captured
states, measurements, redaction, remaining waivers, and the exact boundary that
the reference pack can and cannot prove.
