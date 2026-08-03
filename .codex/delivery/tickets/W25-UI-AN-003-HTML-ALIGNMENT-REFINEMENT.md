---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT
status: accepted
workstream_id: W25
summary: Refine only the isolated UI-AN-003 HTML review prototype so its compact context controls, action axes, notification placement, and chart metadata follow the product-owner browser annotations.
requirement_ids: [WEB-ARCH-003, WEB-ARCH-006, THEME-001, THEME-005, THEME-008, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, FILTER-001, FILTER-002, FILTER-003, FILTER-004, FILTER-010, CHART-001, CHART-002, CHART-006, A11Y-001, A11Y-003]
blockers: [W24-UI-AN-003-HTML-PROTOTYPE]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/delivery/tickets/W24-UI-AN-003-HTML-PROTOTYPE.md
  - .codex/delivery/evidence/W24-UI-AN-003-HTML-PROTOTYPE.md
  - custometry-ui-blueprint-ru.md
  - apps/web/src/sales-overview-prototype/SalesOverviewPrototype.tsx
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT.md
    - .codex/delivery/evidence/W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT.md
    - .codex/delivery/evidence/assets/W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT/**
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
    - verify the refined prototype at 1440 by 900 in a fresh Playwright session
    - measure shared control heights gaps and the More page actions to Hide context panel vertical axis in the browser DOM
    - exercise notifications context hide and restore compact filters share actions and chart metadata without real side effects
    - inspect browser console and requests and run a 1024 by 768 responsive smoke
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.validate_delivery_contract
    - uv run python -m tools.custometry_quality.validate_repository_layout
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: browser-rendered-local-ui-an-003-html-refinement-matched-to-product-owner-browser-annotations
  evidence_target: .codex/delivery/evidence/W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT.md]
---

# Outcome

The isolated HTML review prototype applies all six browser annotations while
preserving the current route, data, chart/table composition, and review-only
side-effect boundary.

# Non-goals

- Do not mutate Figma, normative product sources, shared UI contracts, the
  production application shell, API behavior, persistence, email, or export.

# Work and repair boundary

Change only the prototype component, its local CSS, focused tests, and W25
evidence. The sidebar owns search and notification actions; the chart owns the
compact trust/update summary; the inspector owns aligned page/share/view
groups and remains hideable with a persistent restore affordance.

# Acceptance evidence

Browser evidence must prove equal 32 px inspector action rows, consistent
intra-group gaps, the removal of Dataset and the standalone Result trust row,
the new group order, notification beside Search, aligned top-right global and
inspector actions, context restore behavior, clean console/network state, and
the 1024 px smoke.
