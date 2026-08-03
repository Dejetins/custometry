---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W22-WEB-LINEAR-APPLICATION-SHELL
status: draft
workstream_id: W22
summary: Implement the production-shaped four-theme Custometry application shell behind the accepted reversible route boundary with native-feeling navigation, command, resizable panel, system-state, localization, accessibility, and measured browser behavior.
requirement_ids: [WEB-ARCH-001, WEB-ARCH-002, WEB-ARCH-003, WEB-ARCH-004, WEB-ARCH-006, WEB-PERF-001, WEB-PERF-002, WEB-PERF-003, WEB-PERF-004, WEB-PERF-005, WEB-PERF-006, THEME-001, THEME-005, THEME-008, ROUTE-001, ROUTE-004, ROUTE-009, ROUTE-012, MOTION-001, MOTION-002, MOTION-003, MOTION-011, MOTION-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, HELP-001, HELP-002, HELP-003, HELP-004]
blockers: [W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE, W29-HTML-FIRST-UI-FOUNDATION]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/delivery/specs/custometry-linear-workspace-ui-transition.md
  - .codex/delivery/tickets/W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE.md
  - .codex/delivery/tickets/W29-HTML-FIRST-UI-FOUNDATION.md
  - docs/architecture/ui/custometry-contract-compiled-ui-prototyping-plan-v1.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/ui/linear-workspace-ui-transition-standard-v1.md
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W22-WEB-LINEAR-APPLICATION-SHELL.md
    - .codex/delivery/evidence/W22-WEB-LINEAR-APPLICATION-SHELL.md
    - apps/web/**
    - packages/ui-foundation/**
    - packages/localization/**
    - tests/e2e/**
    - tests/accessibility/**
    - tests/performance/**
    - package.json
    - pnpm-lock.yaml
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - docs/**
    - packages/contracts/**
    - apps/api/**
    - apps/worker_data/**
    - migrations/**
    - deploy/**
    - .codex/delivery/graphs/**
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills: [browser-qa-evidence, backend-performance-evidence, playwright-cli, product-design:audit]
  commands:
    - source scripts/activate-toolchain.sh
    - pnpm --filter @custometry/web lint
    - pnpm --filter @custometry/web typecheck
    - pnpm --filter @custometry/web test
    - pnpm --filter @custometry/web build
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uv run python -m tools.custometry_quality.check_i18n_parity
    - run the shell Playwright matrix for four themes representative desktop widths 200 percent zoom reduced motion keyboard command palette expanded collapsed and resized sidebar history system states Help and route fallback
    - run the repeatable client performance suite and report p50 p75 p95 dispatch acknowledgement paint INP long tasks and animation cadence on declared hardware
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: browser-rendered-four-theme-linear-custometry-shell-with-reversible-fallback-and-measured-client-performance
  evidence_target: .codex/delivery/evidence/W22-WEB-LINEAR-APPLICATION-SHELL.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

The stable authenticated shell behaves like fast native workspace software and
supports four themes, command/navigation, resizable panels, route/history,
localization, accessibility states, system surfaces, and a real rollback seam.

# Non-goals

- Do not implement domain route content, backend authorization, analytics,
  persistence, email/XLSX, or release/deployment.
- Do not remove the legacy fallback before acceptance.

# Work and repair boundary

Build the shell from W29's accepted semantic tokens, typed code components,
component registry, screen manifests, catalog, and browser receipts, keeping
MobX local and Query remote authority. Planned domain routes remain honest
placeholders.
Repair only shell/foundation defects inside owned paths and rerun invalidated
browser, accessibility, localization, and performance evidence.

# Acceptance evidence

Evidence includes fresh screenshots/traces, theme/viewport/keyboard matrices,
console/network results, W29 component provenance and accepted-browser-source
comparison, performance samples, exact fallback exercise, exclusions, and
remaining risks.
