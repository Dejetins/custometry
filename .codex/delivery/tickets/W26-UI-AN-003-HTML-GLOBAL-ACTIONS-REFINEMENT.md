---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT
status: accepted
workstream_id: W26
summary: Refine only the isolated UI-AN-003 HTML review prototype so the context toggle is permanently global and sidebar search and notification actions are borderless until hover.
requirement_ids: [WEB-ARCH-003, WEB-ARCH-006, THEME-001, THEME-005, THEME-008, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, A11Y-001, A11Y-003]
blockers: [W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/delivery/tickets/W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT.md
  - .codex/delivery/evidence/W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT.md
  - custometry-ui-blueprint-ru.md
  - apps/web/src/sales-overview-prototype/SalesOverviewPrototype.tsx
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT.md
    - .codex/delivery/evidence/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT.md
    - .codex/delivery/evidence/assets/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT/**
    - apps/web/src/sales-overview-prototype/SalesOverviewPrototype.tsx
    - apps/web/src/sales-overview-prototype/sales-overview-prototype.css
    - apps/web/tests/sales-overview-prototype.test.tsx
  forbidden_write_paths:
    - apps/web/src/App.tsx
    - apps/web/index.html
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - packages/contracts/**
    - packages/ui-foundation/**
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
  proof_skills: [better-layout, better-ui, browser-qa-evidence, playwright-cli]
  commands:
    - source scripts/activate-toolchain.sh
    - pnpm --filter @custometry/web lint
    - pnpm --filter @custometry/web typecheck
    - pnpm --filter @custometry/web test
    - pnpm --filter @custometry/web build
    - verify default hover open closed and restored states at 1440 by 900 in a fresh Playwright session
    - measure global action axes sidebar action geometry and default versus hover paint in the browser DOM
    - inspect browser console and requests and run a 1024 by 768 responsive smoke
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.validate_delivery_contract
    - uv run python -m tools.custometry_quality.validate_repository_layout
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: browser-rendered-local-ui-an-003-global-action-refinement-matched-to-product-owner-browser-annotations
  evidence_target: .codex/delivery/evidence/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence:
  - .codex/delivery/evidence/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT.md
---

# Outcome

The context toggle remains in one fixed global-header position in both panel
states, never appears inside the inspector, and the sidebar Search and
Notifications actions are visually borderless until interaction.

# Non-goals

- Do not mutate Figma, the application route gate, normative sources, shared
  UI contracts, APIs, persistence, email, export, or other screens.

# Work and repair boundary

Change only the prototype component, its local CSS, focused tests, and W26
evidence. Preserve all W25 content, chart/table axes, inspector row geometry,
and review-only side-effect behavior.

# Acceptance evidence

Browser evidence must prove a stable global context-toggle bounding box before
and after hide/restore, its absence from the inspector, borderless default and
visible hover states for Search and Notifications, the notification's 4 px
left shift, unchanged action axes and spacing, clean console/network state, and
the 1024 px smoke.
