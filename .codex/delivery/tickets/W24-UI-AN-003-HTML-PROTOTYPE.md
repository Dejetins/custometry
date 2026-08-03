---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W24-UI-AN-003-HTML-PROTOTYPE
status: accepted
workstream_id: W24
summary: Reproduce the accepted UI-AN-003 Graphite Figma screen as an isolated local browser prototype for precise product-owner review without claiming production Sales Analytics behavior.
requirement_ids: [WEB-ARCH-003, WEB-ARCH-006, THEME-001, THEME-005, THEME-008, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, FILTER-001, FILTER-002, FILTER-003, FILTER-004, FILTER-010, COMPARE-001, COMPARE-002, COMPARE-003, CHART-001, CHART-002, CHART-006, A11Y-001, A11Y-003]
blockers: [W21-CONTRACT-COMPILED-UI-PILOT]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/delivery/tickets/W21-CONTRACT-COMPILED-UI-PILOT.md
  - .codex/delivery/evidence/W21-CONTRACT-COMPILED-UI-PILOT.md
  - custometry-ui-blueprint-ru.md
  - packages/contracts/ui-design/ui-an-003.manifest.v1.json
  - packages/contracts/ui-design/visual-decisions.ui-an-003.v1.json
  - apps/web/package.json
start_probe:
  boundary: accepted Figma product node 40:536 in MXfxuhSFpIczbUtFmOSyPp
  read_only_check: fetch design context and confirm the 1440 by 900 Graphite Sales overview identity before source mutation
  stop_on: [unavailable, identity_mismatch, state_drift]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W24-UI-AN-003-HTML-PROTOTYPE.md
    - .codex/delivery/evidence/W24-UI-AN-003-HTML-PROTOTYPE.md
    - .codex/delivery/evidence/assets/W24-UI-AN-003-HTML-PROTOTYPE/**
    - apps/web/src/App.tsx
    - apps/web/index.html
    - apps/web/src/sales-overview-prototype/**
    - apps/web/tests/sales-overview-prototype.test.tsx
    - apps/web/public/ui-an-003-prototype/**
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - packages/contracts/**
    - packages/ui-foundation/**
    - packages/localization/**
    - apps/api/**
    - migrations/**
    - deploy/**
    - docs/**
    - .codex/delivery/graphs/**
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills: [figma:figma-design-to-code, product-design:image-to-code, product-design:design-qa, browser-qa-evidence, playwright-cli]
  commands:
    - source scripts/activate-toolchain.sh
    - pnpm --filter @custometry/web lint
    - pnpm --filter @custometry/web typecheck
    - pnpm --filter @custometry/web test
    - pnpm --filter @custometry/web build
    - run the isolated prototype at 1440 by 900 and compare its browser screenshot against Figma node 40:536
    - exercise chart/data switching context inspector visibility filter context menu and compact share actions without real side effects
    - inspect browser console and run a 1024 px responsive smoke
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: browser-rendered-local-ui-an-003-graphite-review-prototype-matched-to-accepted-figma-node-40-536
  evidence_target: .codex/delivery/evidence/W24-UI-AN-003-HTML-PROTOTYPE.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W24-UI-AN-003-HTML-PROTOTYPE.md]
---

# Outcome

The accepted Graphite Sales overview screen is available as an isolated local
HTML/React prototype at the canonical Sales route with
`?view=html-prototype`, preserving the current fallback and architecture spike.

# Non-goals

- Do not implement W22 production shell or W23 Sales Analytics integration.
- Do not call real APIs, persist product data, send email, create a share link,
  export data, or claim backend authorization.
- Do not change the accepted Figma source or normative product contracts.

# Work and repair boundary

Add one isolated prototype component, exact source assets, a query-gated mount
in `App.tsx`, and focused tests. Repair visual or interaction mismatches only
inside the declared prototype paths and rerun invalidated browser evidence.

# Acceptance evidence

Evidence contains the exact Figma and browser screenshots at 1440 by 900,
normalized visual comparison findings, interaction checks, console status,
responsive smoke, source checks, and explicit local-prototype exclusions.
