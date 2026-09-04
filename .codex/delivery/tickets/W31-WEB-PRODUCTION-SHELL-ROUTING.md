---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W31-WEB-PRODUCTION-SHELL-ROUTING
status: accepted
workstream_id: W31
summary: Replace the provisional Web entry point with the production application shell, route-registration seam, and truthful system presentation surfaces used by later feature tickets.
requirement_ids: [WEB-ARCH-003, WEB-ARCH-004, WEB-ARCH-005, WEB-ARCH-006, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, RBAC-002, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, A11Y-001, A11Y-003, A11Y-008, I18N-001, I18N-002, I18N-005]
blockers: []
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - docs/architecture/ui/custometry-web-implementation-source-contract-v1.md
  - custometry-technical-blueprint-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/adr/0007-responsive-web-frontend-platform.md
  - docs/contracts/ui-route-contract.md
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-surface-contracts.json
  - apps/web/src/App.tsx
  - apps/web/src/styles.css
  - packages/ui-foundation/src/index.ts
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W31-WEB-PRODUCTION-SHELL-ROUTING.md
    - .codex/delivery/evidence/W31-WEB-PRODUCTION-SHELL-ROUTING.md
    - apps/web/src/app/shell/**
    - apps/web/src/app/router/**
    - apps/web/src/app/system-surfaces/**
    - apps/web/src/app/routes/feature-route-contract.ts
    - apps/web/src/app/routes/feature-route-loader.ts
    - apps/web/src/app/index.ts
    - apps/web/src/App.tsx
    - apps/web/src/styles.css
    - apps/web/tests/app-shell/**
    - packages/ui-foundation/**
    - packages/localization/locales/en/foundation.json
    - packages/localization/locales/ru/foundation.json
    - packages/localization/locales/en/route-titles.json
    - packages/localization/locales/ru/route-titles.json
    - tests/e2e/web-shell/**
    - tests/accessibility/web-shell/**
  forbidden_write_paths:
    - .codex/delivery/ui-design-programs/custometry-v2/**
    - .codex/agents/generated/custometry-ui-design-g0-v2/**
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - packages/contracts/routes/**
    - apps/api/**
    - migrations/**
    - deploy/**
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills: [contract-impact-analysis, better-accessibility, browser-qa-evidence, playwright-cli]
  commands:
    - source scripts/activate-toolchain.sh && pnpm --filter @custometry/ui-foundation lint && pnpm --filter @custometry/ui-foundation test
    - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web lint && pnpm --filter @custometry/web test && pnpm --filter @custometry/web build
    - source scripts/activate-toolchain.sh && pnpm --filter @custometry/localization test
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uv run python -m tools.custometry_quality.check_i18n_parity
    - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-shell/playwright.config.ts
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: production-web-shell-route-resolution-and-system-presentation-in-a-real-browser-with-contract-fixtures
  evidence_target: .codex/delivery/evidence/W31-WEB-PRODUCTION-SHELL-ROUTING.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W31-WEB-PRODUCTION-SHELL-ROUTING.md]
---

> Source update, 2026-09-04: the G-program was removed. Historical acceptance
> and evidence remain unchanged; they do not prove conformance to the final
> target pilot. Any new work requires its own ready ticket and the current
> Web implementation source contract. Forbidden historical paths remain guards.

# Outcome

`UI-CAP-001` and `UI-SYS-001` through `UI-SYS-005` have a production React
shell and stable feature-route registration seam. Auth, global, workspace,
setup, focus, and system profiles preserve route identity, history, localized
labels, authorization-state presentation, and keyboard focus without treating
frontend fixtures as backend authorization.

# Non-goals

- Do not implement a domain feature page, API, authentication decision,
  persistence, analytics computation, or production deployment.
- Do not restore the removed G-program or certify its historical stages.
- Do not add mobile-specific navigation or claim full WCAG conformance.

# Work and repair boundary

Refactor the provisional `App.tsx` into production shell, router, navigation,
feedback, and system-surface modules. Add one typed, lazy feature-registration
contract that later tickets can satisfy with disjoint route modules; the shell
must not require each feature ticket to edit a central mutable registry.
Preserve existing accepted tokens/components where they meet the current
contract and repair only in-scope shell defects. Preserve the current
Foundation, Help, planned-surface, prototype, or an equivalent compatibility
seam; do not remove the last fallback at this ticket's proof boundary. The
ticket-owned Playwright config must start and stop host Vite through `webServer`,
discover only W31 specs, and run desktop projects at 768x1024 and 1920x1080.

# Acceptance evidence

Focused tests prove route/profile resolution, history/Back/refresh, current
navigation, focus restoration, and fixture honesty. Canonical Playwright CLI
evidence observes critical shell and system states at 768 and 1920 CSS px in
RU and EN, keyboard-only use, 200% zoom, reduced motion, console/page errors,
failed same-origin requests, clipping, overlap, and horizontal overflow. The
report explicitly excludes backend policy, API, persistence, Compose, release,
production accessibility, publication, and deployment readiness.
