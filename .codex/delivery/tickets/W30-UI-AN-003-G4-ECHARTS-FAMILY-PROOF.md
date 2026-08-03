---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF
status: ready
workstream_id: W30
summary: Prove the UI-AN-003 G4 representative family across all required states, roles, locales, themes, and responsive-Web anchors using real Apache ECharts through ChartSpec and the shared compiler, a source-backed chart-type selector, and a separate accessible Data Grid.
requirement_ids: [ROUTE-004, THEME-001, THEME-005, THEME-008, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, UI-SHELL-004, UI-SHELL-005, UI-SHELL-006, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, UI-DENSITY-004, CHART-004, CHART-020, CHART-021, CHART-022, CHART-023, FOCUS-001, FOCUS-002, FOCUS-003, FOCUS-004, FOCUS-005, FOCUS-006, FOCUS-007, FOCUS-008, FOCUS-009, FOCUS-010, A11Y-001, A11Y-003, A11Y-008]
blockers: []
plan_doc: .codex/delivery/ui-design-programs/custometry-v1/ui-design-program.json
prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g4-v1
stage_ledger: .codex/delivery/ui-design-programs/custometry-v1/g4-stage-ledger.md
stage_instance_id: G4@FAM-ROUTE-WORKSPACE-OVERVIEW-BROWSE-FOCUS-CAPABLE-FOCUS-r1
iteration_report_template: .codex/agents/iteration_report_template.md
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/delivery/ui-design-programs/custometry-v1/ui-design-program.json
  - .codex/delivery/ui-design-programs/custometry-v1/g4-stage-ledger.md
  - .codex/delivery/ui-design-programs/custometry-v1/g4-chart-rendering-policy-owner-acceptance-r5.json
  - packages/contracts/ui-design/ui-an-003.manifest.v1.json
  - apps/web/src/sales-overview-prototype/SalesOverviewPrototype.tsx
  - .codex/agents/iteration_report_template.md
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md
    - .codex/delivery/evidence/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md
    - .codex/delivery/evidence/assets/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF/**
    - .codex/delivery/ui-design-programs/custometry-v1/screen-contracts/ui-an-003/**
    - .codex/delivery/ui-design-programs/custometry-v1/evidence/g4-fam-workspace-overview-browse-focus-r1/**
    - .codex/delivery/ui-design-programs/custometry-v1/g4-owner-review-ui-an-003-r1.md
    - .codex/delivery/ui-design-programs/custometry-v1/g4-stage-ledger.md
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
  proof_skills: [staged-plan-runner, ui-design-program, contract-impact-analysis, better-ui, better-layout, better-accessibility, browser-qa-evidence, playwright-cli]
  commands:
    - verify accepted CUSTOMETRY-UI-DESIGN-PROGRAM-V1 revision 5 source hashes exact triad links and the pending unclaimed ledger instance before writes
    - test the exact count of JSON screen contracts under .codex/delivery/ui-design-programs/custometry-v1/screen-contracts/ui-an-003 is 144
    - pass the deterministic sorted list of all 144 JSON screen-contract files to validate_ui_design_program.py under screen_contract_ready
    - python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/ui_design_tool.py preflight
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
evidence: []
---

# Outcome

The exact G4 stage
`G4@FAM-ROUTE-WORKSPACE-OVERVIEW-BROWSE-FOCUS-CAPABLE-FOCUS-r1` proves
`UI-AN-003` as the representative for its accepted family hypothesis. The
delivery unit creates 144 exact state/role/locale/theme screen-contract
revisions, each declaring all four accepted responsive-Web anchors. Actual
Apache ECharts output is compiled from validated `ChartSpec`; the visible
chart-type selector is limited to a deterministic compatibility result for the
current dataset profile and report type; the accessible table remains a
separate product Data Grid.

The accepted program revision, this ready ticket, the sole stage prompt, the
stage ledger, and `.codex/agents/iteration_report_template.md` are the complete
execution-authority chain. `staged-plan-runner` must claim the pending stage
before any write.

# Non-goals

- Do not expand the representative result to `UI-DATA-020`, `UI-DQ-001`, any
  other family, G5, or G6.
- Do not add mobile anchors, mobile navigation, or mobile-specific
  composition. `mobile_scope` remains `unauthorized`.
- Do not change normative product requirements, routes, permissions, metric
  semantics, backend APIs, persistence, exports, deployment, or production
  data flows.
- Do not use ECharts `dataView` as the product table and do not accept a mock
  SVG/CSS/Canvas chart as ECharts proof.
- Do not commit, push, publish, merge, release, or deploy while executing this
  ticket.

# Work and repair boundary

Use only the `change_scope.allowed_write_paths`. Preserve accepted revision-5
hashes and historical W27/W28 evidence. Keep dependency direction
`ChartSpec -> shared compiler -> ECharts adapter`; browser state must not
calculate authoritative metrics or elevate permissions.

The compatibility rules must return an ordered `available_chart_types` and
default for the exact dataset profile and report type. If current authoritative
sources cannot support that mapping, write a bounded owner proposal inside the
stage evidence, record a truthful blocker in the sole ledger, and stop before
implementation or acceptance. Do not fill the gap with a generic chart list.

# Acceptance evidence

Terminal evidence follows `.codex/agents/iteration_report_template.md` and
records the accepted program and ticket identities; exact source, contract,
implementation, dependency, fixture, browser, and receipt hashes; the 144
screen-contract count; all four anchors; actual ECharts/ChartSpec/compiler
output; compatibility and user-selection behavior; separate Data Grid and
chart/table toggle behavior; accessibility and keyboard results; console and
network observations; foreign-change separation; commands and observed
results; exclusions; blockers; and residual risk.

The family is not accepted until generated screen-acceptance receipts and the
explicit owner decision named by the G4 prompt exist. Missing owner acceptance
keeps `Next stage allowed: false` and prevents G5.
