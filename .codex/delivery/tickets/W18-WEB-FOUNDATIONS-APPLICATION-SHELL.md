---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W18-WEB-FOUNDATIONS-APPLICATION-SHELL
status: superseded
workstream_id: W18
summary: Replace the provisional Foundation shell with the reusable Frost Web foundation and production-shaped application shell that resolves the accepted route registry honestly, renders required system presentation states, and is proven in a real browser without claiming domain or authorization runtime.
requirement_ids: [THEME-002, I18N-001, I18N-002, I18N-005, I18N-009, I18N-010, A11Y-001, A11Y-003, A11Y-008, A11Y-009, A11Y-010, ROUTE-001, ROUTE-004, ROUTE-009, ROUTE-012, MOTION-001, MOTION-002, MOTION-003, MOTION-011, MOTION-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, HELP-001, HELP-002, HELP-003, HELP-004]
blockers: [W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION]
supersession_reason: The Frost-only shell and W10 design guard predate the accepted Linear-workspace frontend baseline, four-theme registry, separate Penpot vNext target, reversible route boundary, and measured performance contract; W19-W23 replace this unexecuted scope.
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/system-design.md
  - docs/architecture/development-operating-model.md
  - docs/architecture/development-runtime-contract.md
  - docs/contracts/ui-route-contract.md
  - docs/contracts/ui-surface-contract.md
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-surface-contracts.json
  - packages/localization/locales/en/foundation.json
  - packages/localization/locales/ru/foundation.json
  - packages/localization/locales/en/route-titles.json
  - packages/localization/locales/ru/route-titles.json
  - apps/web/src/App.tsx
  - apps/web/src/styles.css
  - apps/web/tests/app.test.tsx
  - tests/e2e/foundation.spec.ts
  - .codex/delivery/tickets/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
  - .codex/delivery/evidence/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
start_probe:
  boundary: accepted canonical Penpot source file 7cd71457-8d32-8044-8008-549f83bb4645 at W10 terminal revision 213
  read_only_check: confirm the exact file ID and revision 213 before loading design regions or preparing browser implementation; perform no Penpot write
  stop_on: [unavailable, identity_mismatch, state_drift]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W18-WEB-FOUNDATIONS-APPLICATION-SHELL.md
    - .codex/delivery/evidence/W18-WEB-FOUNDATIONS-APPLICATION-SHELL.md
    - apps/web/**
    - packages/localization/**
    - tests/e2e/**
    - tests/accessibility/**
    - tests/localization/**
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - docs/**
    - packages/contracts/**
    - packages/chart_compiler_ts/**
    - apps/api/**
    - apps/worker_data/**
    - packages/identity_access/**
    - packages/connection_catalog/**
    - packages/ingestion/**
    - packages/data_quality/**
    - packages/semantic_model/**
    - packages/analytics_core/**
    - packages/analytics_customer/**
    - packages/analytics_sales/**
    - plugins/**
    - migrations/**
    - deploy/**
    - compose.yaml
    - compose.dev.yaml
    - scripts/dev
    - .codex/delivery/graphs/**
    - .codex/delivery/tickets/W11-HYBRID-DEVELOPMENT-RUNTIME.md
    - .codex/delivery/evidence/W11-HYBRID-DEVELOPMENT-RUNTIME.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: []
  commands:
    - confirm W10 is accepted with passed terminal evidence at canonical Penpot revision 213 and inspect only the accepted Foundations, shell, C01-C17, responsive, state, and motion source regions needed by this ticket
    - source scripts/activate-toolchain.sh
    - pnpm --filter @custometry/web lint
    - pnpm --filter @custometry/web typecheck
    - pnpm --filter @custometry/web test
    - pnpm --filter @custometry/web build
    - pnpm --filter @custometry/localization test
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uv run python -m tools.custometry_quality.check_i18n_parity
    - run the ticket-owned Playwright shell suite against host Vite with deterministic contract mocks at 1440, 1024, 820, and 390 CSS pixels
    - inspect fresh browser screenshots and traces for expanded collapsed and narrow navigation, en and ru, 200 percent zoom, reduced motion, keyboard-only operation, generic system surfaces, route history, focus restoration, clipping, overlap, horizontal overflow, console errors, page errors, and failed same-origin requests
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: browser-rendered-frost-foundations-application-shell-and-system-presentation-with-contract-mocks
  evidence_target: .codex/delivery/evidence/W18-WEB-FOUNDATIONS-APPLICATION-SHELL.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W18-WEB-FOUNDATIONS-APPLICATION-SHELL.md]
---

# Outcome

The Web has one reusable Frost foundation and application shell rather than a
monolithic provisional Foundation page. Public/auth, global, installation, and
workspace route families resolve through the accepted registry; shell,
sidebar, topbar, navigation, Help entry, system presentation states, route
transition, focus, responsive behavior, and en/ru presentation are reusable by
later vertical UI tickets. Unimplemented domain routes remain explicitly
planned and never impersonate real data or authorization.

# Non-goals

- Do not implement Sales, Customer, RFM, charts, filters, Focus/Explore,
  onboarding behavior, data grids, domain forms, or any other business route.
- Do not implement authentication, authorization decisions, API endpoints,
  persistence, ingestion, analytics, email/XLSX, or runtime infrastructure.
- Do not change route identity, product requirements, executable route/surface
  contracts, backend packages, Penpot, or the single Frost v1 design scope.
- Do not claim all 116 route pages, system policy enforcement, runtime
  accessibility, Compose, release, or production readiness from component
  rendering alone.

# Work and repair boundary

Refactor the existing `apps/web` Foundation shell into small typed foundations,
shell, navigation, feedback, and system-surface modules. Use semantic Frost
tokens, Inter-compatible bundled/fallback typography, and the accepted Lucide
icon mapping. Expanded navigation uses icon plus label; collapsed and tablet
navigation use the same icons without letter abbreviations and retain
localized accessible names and tooltips. The shell does not remount between
workspace routes. Main content alone uses the accepted bounded route fade;
sidebar and reduced-motion variants follow the accepted motion matrix.

The browser implementation may use deterministic contract mocks only when it
visibly and structurally remains a development/test boundary. Generic 403,
404, session-expired, maintenance, and upgrade-required presentation must not
claim that backend policy or lifecycle enforcement exists. Preserve the
current shipped local documentation and Help behavior. Repair discovered
in-scope shell defects and rerun every invalidated browser, localization, and
static check.

# Acceptance evidence

- Terminal evidence records the exact Penpot source identity/revision inspected,
  changed modules, test commands, browser matrix, screenshot/trace locations,
  redaction, observations, and verdict.
- Fresh real-browser evidence covers expanded, collapsed, tablet, and narrow
  navigation; route title/current-location behavior; 404 plus the other generic
  system presentation variants; Help; en/ru; keyboard-only focus; 200% zoom;
  reduced motion; and return/history behavior.
- No inspected viewport has clipped controls, unintended overlap, button-label
  misalignment, hidden navigation without a restore control, horizontal page
  overflow, console/page errors, or unexpected failed same-origin requests.
- Planned routes remain honest placeholders. Browser proof does not establish
  real authorization, API, persistence, analytics, Compose, release, or
  production accessibility behavior.
