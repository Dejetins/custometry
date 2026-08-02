---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W27-UI-AN-003-HTML-CONTRACT-COMPLETION
status: accepted
workstream_id: W27
summary: Complete the accepted UI-AN-003 HTML review candidate and align the normative shell, route, trust, focus, coverage, and HTML-first prototyping contracts with the product-owner decisions.
requirement_ids: [WEB-ARCH-003, WEB-ARCH-006, THEME-001, THEME-005, THEME-008, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, UI-SHELL-004, UI-SHELL-005, UI-SHELL-006, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, UI-DENSITY-004, FOCUS-001, FOCUS-002, FOCUS-003, FOCUS-004, FOCUS-005, FOCUS-006, FOCUS-007, FOCUS-008, FOCUS-009, FOCUS-010, A11Y-001, A11Y-003, A11Y-008, ROUTE-004]
blockers: [W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/delivery/tickets/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT.md
  - .codex/delivery/evidence/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/ui/linear-workspace-ui-transition-standard-v1.md
  - .codex/delivery/specs/custometry-contract-compiled-ui-prototyping-pilot.md
  - apps/web/src/sales-overview-prototype/SalesOverviewPrototype.tsx
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W27-UI-AN-003-HTML-CONTRACT-COMPLETION.md
    - .codex/delivery/evidence/W27-UI-AN-003-HTML-CONTRACT-COMPLETION.md
    - .codex/delivery/evidence/assets/W27-UI-AN-003-HTML-CONTRACT-COMPLETION/**
    - .codex/delivery/specs/custometry-contract-compiled-ui-prototyping-pilot.md
    - .codex/delivery/specs/custometry-linear-workspace-ui-transition.md
    - .codex/delivery/graphs/custometry-linear-workspace-ui-transition-v1.json
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - docs/architecture/ui/linear-workspace-ui-transition-standard-v1.md
    - packages/contracts/routes/ui-routes.json
    - packages/contracts/routes/ui-route-contracts.json
    - packages/contracts/routes/ui-surface-contracts.json
    - packages/localization/locales/en/route-titles.json
    - packages/localization/locales/ru/route-titles.json
    - docs/generated/requirement-index.json
    - apps/web/src/sales-overview-prototype/SalesOverviewPrototype.tsx
    - apps/web/src/sales-overview-prototype/sales-overview-prototype.css
    - apps/web/tests/sales-overview-prototype.test.tsx
  forbidden_write_paths:
    - packages/contracts/ui-design/**
    - packages/ui-foundation/**
    - apps/web/src/App.tsx
    - apps/web/index.html
    - apps/api/**
    - migrations/**
    - deploy/**
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills: [better-layout, better-ui, better-accessibility, browser-qa-evidence, playwright-cli]
  commands:
    - source scripts/activate-toolchain.sh
    - pnpm --filter @custometry/web lint
    - pnpm --filter @custometry/web typecheck
    - pnpm --filter @custometry/web test
    - pnpm --filter @custometry/web build
    - uv run python -m tools.custometry_quality.validate_blueprints
    - uv run python -m tools.custometry_quality.generate_requirement_index
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uv run python -m tools.custometry_quality.check_i18n_parity
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.validate_delivery_contract
    - verify desktop shell expanded collapsed hidden and resized states at 1440 by 900 in a fresh Playwright session
    - verify focus chart focus data focus breakdown result-trust drawer help and user-menu states in a fresh Playwright session
    - verify 1024 by 768 compact layout without CSS zoom overflow or overlapping controls
    - inspect browser console and requests for the exercised states
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: browser-rendered-local-ui-an-003-html-contract-completion-plus-repository-owned-normative-contract-validation
  evidence_target: .codex/delivery/evidence/W27-UI-AN-003-HTML-CONTRACT-COMPLETION.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence:
  - .codex/delivery/evidence/W27-UI-AN-003-HTML-CONTRACT-COMPLETION.md
---

# Outcome

The accepted `UI-AN-003` direction is completed as a responsive HTML review
candidate with compact result trust, focus/explore routes, channel/store/product
breakdowns, a persistent accessible sidebar utility model, and explicit desktop,
collapsed, hidden, and resized navigation states. Normative sources describe the
same product-owner decisions and the reusable HTML-first review cycle.

# Non-goals

- Do not mutate Figma or Figma-specific manifests, components, variables, or
  accepted frames before the product owner accepts this HTML candidate.
- Do not implement ECharts, a command palette, typed filter expressions, a
  More-page-actions menu, or real share, email, download, and export side
  effects in this review slice.
- Do not claim production, API, persistence, accessibility-conformance, or
  release readiness from the isolated prototype.

# Work and repair boundary

Update only the named normative, route-contract, isolated prototype, focused
test, and W27 evidence paths. Preserve W24-W26 and the current Figma contracts
as truthful historical evidence. Figma synchronization is a later execution
unit that may begin only after explicit product-owner acceptance of W27.

# Acceptance evidence

Repository validation must prove mirrored requirements, route and localization
parity, and a valid delivery ticket. Focused tests and fresh browser evidence
must prove stable action axes and spacing at `1440 × 900`, non-scaled compact
behavior at `1024 × 768`, expanded/collapsed/hidden/resized sidebar states,
`aria-current` on Sales, distinct Sales and Forecasts icons, Help and user-menu
availability, chart/data trust persistence, trust-details disclosure,
URL-addressable focus chart/data/breakdown states, and channel/store/product
breakdown selection. Browser proof must also record console and request state.

# Product-owner acceptance

The product owner explicitly accepted the current HTML candidate on
2026-08-01. The terminal outcome is `pilot_passed`, the post-pilot decision is
`scale`, and
`http://127.0.0.1:5173/w/northwind-retail/analytics/sales?view=html-prototype`
is the accepted visual source for the next bounded Figma synchronization unit.
