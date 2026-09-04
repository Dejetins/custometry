---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF
status: superseded
workstream_id: W30
summary: Prove the UI-AN-003 G4 representative family across all required states, roles, locales, themes, and responsive-Web anchors using real Apache ECharts through ChartSpec and the shared compiler, a source-backed chart-type selector, and a separate accessible Data Grid.
requirement_ids: [ROUTE-004, THEME-001, THEME-005, THEME-008, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, CHART-004, FOCUS-001, FOCUS-002, FOCUS-003, FOCUS-004, FOCUS-005, FOCUS-006, FOCUS-007, FOCUS-008, FOCUS-009, FOCUS-010, A11Y-001, A11Y-003, A11Y-008]
blockers: []
supersession_reason: The previous revision 5 design workflow and its G4 family hypothesis are retired. Current UI work follows the accepted target pilot and ordinary implementation tickets; this historical unit must not execute.
iteration_report_template: .codex/agents/iteration_report_template.md
context_sources:
  - docs/architecture/ui/ui-program-retirement.md
  - AGENTS.md
  - .codex/AGENTS.md
  - packages/contracts/ui-design/ui-an-003.manifest.v1.json
  - apps/web/src/sales-overview-prototype/SalesOverviewPrototype.tsx
  - .codex/agents/iteration_report_template.md
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md
    - .codex/delivery/evidence/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md
    - .codex/delivery/evidence/assets/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF/**
    - packages/chart_compiler_ts/**
    - packages/contracts/ui-design/**
    - packages/ui-foundation/**
    - apps/web/package.json
    - apps/web/src/sales-overview-prototype/**
    - apps/web/tests/sales-overview-prototype.test.tsx
    - apps/web/tests/sales-overview-prototype/**
    - pnpm-lock.yaml
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - docs/**
    - packages/contracts/routes/**
    - packages/localization/**
    - apps/api/**
    - apps/worker_data/**
    - packages/analytics_core/**
    - packages/analytics_customer/**
    - packages/analytics_sales/**
    - migrations/**
    - deploy/**
    - .codex/delivery/graphs/**
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills: [contract-impact-analysis, better-ui, better-layout, better-accessibility, browser-qa-evidence, playwright-cli]
  commands:
    - source scripts/activate-toolchain.sh
    - pnpm --filter @custometry/web lint
    - pnpm --filter @custometry/web typecheck
    - pnpm --filter @custometry/web test
    - pnpm --filter @custometry/web build
    - run focused ChartSpec compiler compatibility selector and Data Grid tests
    - capture fresh browser geometry raster accessibility keyboard console and network evidence for all required tuples at 768x900 1440x900 1920x1080 and 2560x1440
    - uv run python -m tools.custometry_quality.validate_blueprints
    - uv run python -m tools.custometry_quality.generate_requirement_index --check
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.validate_delivery_contract
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: exact-ui-an-003-g4-screen-contract-plus-four-anchor-browser-raster-accessibility-keyboard-console-network-evidence-with-real-echarts
  evidence_target: .codex/delivery/evidence/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md]
---

# Outcome

This ticket remains `superseded` and must not execute. The G4 proof was never
performed. Its retained scope, commands, and evidence metadata above describe
the abandoned execution unit, not current permission to write or run a stage.

On 2026-09-04 the owner authorized removal of the G-program materials.
Unavailable skill routes and stage-validator commands were removed during
publication reconciliation; this does not change the historical verdict.
The historical plan, prompt, ledger, and screen-contract paths are recoverable
from commit `d5f8aa29f83be90a0b3871ff2c886d48fc020901`; see
[the retirement record](../../../docs/architecture/ui/ui-program-retirement.md).
The corresponding terminal evidence remains a historical supersession record,
not proof against the final target pilot. No ticket status or product
requirement changes through this cleanup.

# Non-goals

Do not execute the historical commands, restore the G-program, change
production code, or infer new implementation acceptance.

# Acceptance evidence

The linked terminal evidence records supersession only. No G4/browser
acceptance is claimed; original sources remain recoverable from Git.
