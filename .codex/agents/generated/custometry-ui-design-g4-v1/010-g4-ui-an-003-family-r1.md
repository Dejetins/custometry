---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: G4@FAM-ROUTE-WORKSPACE-OVERVIEW-BROWSE-FOCUS-CAPABLE-FOCUS-r1
gate_id: G4
target_id: FAM-ROUTE-WORKSPACE-OVERVIEW-BROWSE-FOCUS-CAPABLE-FOCUS@r1
title: Prove the UI-AN-003 representative family with real Apache ECharts
execution_mode: manual_sequential
goal_artifact_required: false
current_stage: G4@FAM-ROUTE-WORKSPACE-OVERVIEW-BROWSE-FOCUS-CAPABLE-FOCUS-r1

prompt_pack_execution:
  plan_doc: /Users/daniildegtyarev/Projects/Custometry/.codex/delivery/ui-design-programs/custometry-v1/ui-design-program.json
  prompt_pack_dir: /Users/daniildegtyarev/Projects/Custometry/.codex/agents/generated/custometry-ui-design-g4-v1
  stage_ledger: /Users/daniildegtyarev/Projects/Custometry/.codex/delivery/ui-design-programs/custometry-v1/g4-stage-ledger.md
  selected_ticket: /Users/daniildegtyarev/Projects/Custometry/.codex/delivery/tickets/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md
  iteration_report_template: /Users/daniildegtyarev/Projects/Custometry/.codex/agents/iteration_report_template.md

context:
  always_read:
    - AGENTS.md
    - .codex/AGENTS.md
    - .codex/delivery/tickets/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md
    - .codex/delivery/ui-design-programs/custometry-v1/g4-stage-ledger.md
    - .codex/delivery/ui-design-programs/custometry-v1/g4-chart-rendering-policy-owner-acceptance-r5.json
  task_entrypoints:
    - .codex/delivery/ui-design-programs/custometry-v1/ui-design-program.json
    - packages/contracts/ui-design/ui-an-003.manifest.v1.json
    - apps/web/src/sales-overview-prototype/SalesOverviewPrototype.tsx
  conditional_bundles:
    - condition: Exact route, state, role, or permission identity cannot be resolved from the program pointers.
      sources:
        - packages/contracts/routes/ui-routes.json
        - packages/contracts/routes/ui-route-contracts.json
    - condition: Before changing the chart compiler, renderer dependency, or chart-type compatibility contract.
      sources:
        - custometry-technical-blueprint-ru.md
        - packages/chart_compiler_ts/src/index.ts
        - apps/web/package.json
    - condition: Accepted pilot provenance or current browser-source hashes do not reconcile.
      sources:
        - .codex/delivery/evidence/W27-UI-AN-003-HTML-CONTRACT-COMPLETION.md
        - .codex/delivery/evidence/assets/W28-UI-AN-003-FIGMA-SYNCHRONIZATION/browser-reference-receipt.json
    - condition: Before changing visual implementation styles.
      sources:
        - apps/web/src/sales-overview-prototype/sales-overview-prototype.css
    - condition: Before assembling terminal ticket evidence.
      sources:
        - .codex/agents/iteration_report_template.md
  consult_if_needed:
    - custometry-ui-blueprint-ru.md
    - docs/architecture/system-design.md
    - docs/architecture/ui/linear-workspace-ui-transition-standard-v1.md

required_literals:
  - CUSTOMETRY-UI-DESIGN-PROGRAM-V1
  - G4@FAM-ROUTE-WORKSPACE-OVERVIEW-BROWSE-FOCUS-CAPABLE-FOCUS-r1
  - UI-AN-003
  - CP-ROUTE-BROWSE-AN-VW
  - CHART-004
  - CHART-020
  - CHART-021
  - CHART-022
  - CHART-023
  - web-min-768
  - web-standard-1440
  - web-wide-1920
  - web-max-2560
  - mobile_scope: unauthorized
required_keywords:
  - plan_doc
  - prompt_pack_dir
  - stage_ledger
  - manual_sequential
  - goal_artifact_required=false
  - current_stage
  - Next stage allowed
  - validation_strategy
  - file_manifest
  - foreign_changes_excluded
  - ChartSpec
  - Apache ECharts
  - available_chart_types
  - Data Grid
  - owner decision

skills:
  primary: staged-plan-runner
  companions:
    - ui-design-program
    - contract-impact-analysis
    - better-ui
    - better-layout
    - better-accessibility
    - browser-qa-evidence
    - playwright-cli

validation_strategy:
  proof_boundary: Exact UI-AN-003 screen-contract coverage and observed same-environment browser, geometry, raster, accessibility, keyboard, console, and network evidence at the four accepted responsive-Web anchors; no production API, persistence, performance, release, deployment, G5, G6, or mobile proof.
  evidence_target: .codex/delivery/ui-design-programs/custometry-v1/evidence/g4-fam-workspace-overview-browse-focus-r1/
  iteration_report_target: .codex/delivery/evidence/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md
  commands:
    - python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_ui_design_program.py --profile program_ready --project-root /Users/daniildegtyarev/Projects/Custometry .codex/delivery/ui-design-programs/custometry-v1/ui-design-program.json
    - test "$(find .codex/delivery/ui-design-programs/custometry-v1/screen-contracts/ui-an-003 -type f -name '*.json' | wc -l | tr -d ' ')" = 144
    - find .codex/delivery/ui-design-programs/custometry-v1/screen-contracts/ui-an-003 -type f -name '*.json' | LC_ALL=C sort | xargs python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_ui_design_program.py --profile screen_contract_ready --project-root /Users/daniildegtyarev/Projects/Custometry
    - python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/ui_design_tool.py preflight
    - source scripts/activate-toolchain.sh && uv run python -m tools.check --scope local

file_manifest:
  expected_touch_zones:
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
  foreign_changes_excluded: true

safety:
  invention_policy: forbidden
  unknown_policy: record_and_block
  mobile_scope: unauthorized
  agent_self_acceptance: prohibited
---

# Task

Execute only
`G4@FAM-ROUTE-WORKSPACE-OVERVIEW-BROWSE-FOCUS-CAPABLE-FOCUS-r1` from the
accepted `CUSTOMETRY-UI-DESIGN-PROGRAM-V1` revision `5`. Prove representative
screen `UI-AN-003` for this family. Do not expand the accepted family decisions
to `UI-DATA-020` or `UI-DQ-001`; those remain downstream work.

Execution authority is ready ticket
`W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF`. Use
`.codex/agents/iteration_report_template.md` for its terminal evidence. The
prompt does not authorize writes outside that ticket.

## Context / Current State

- Program revision `5` is accepted under `validation_profile: program_ready`.
- The family reuse status is still `hypothesis`; G4 may confirm or reject it
  only from representative evidence.
- W27 is accepted historical HTML composition evidence for `UI-AN-003` and the
  workspace shell values it actually exercised. It does not prove real ECharts
  rendering or the new `768`, `1920`, and `2560` anchors.
- Coverage profile `CP-ROUTE-BROWSE-AN-VW` requires nine states
  (`first_loading`, `ready`, `refreshing`, `empty`, `partial`, `forbidden`,
  `failed`, `stale`, `dependency_unavailable`), roles `AN|VW`, locales
  `en|ru`, themes `abyss|graphite|frost|paper`, and one four-anchor
  responsive-Web viewport set.
- The supported Web range is `768..2560` CSS px with exact anchors
  `768x900`, `1440x900`, `1920x1080`, and `2560x1440`. Widths outside that
  range are out of mandatory coverage. `mobile_scope` remains `unauthorized`.

## Requirements

1. Run a read-only pre-write guard. Verify the accepted program identity,
   source hashes, exact triad links, pending unclaimed ledger row, cleanly
   separable foreign changes, and current pilot/manifest identities. Stop on
   drift instead of rewriting accepted evidence.
2. Create one exact screen-contract revision for every required
   `state x role x locale x theme` tuple for `UI-AN-003`; each contract uses
   the same exact four-anchor responsive-Web set. Do not collapse the current
   144 coverage tuples or omit a state because two renders look alike.
3. Populate every material visible value from an allowed provenance kind.
   Preserve accepted G3 shell, typography, density, assets, layout constraints,
   range, anchors, and mobile boundary. New responsive or visual values without
   eligible provenance require a proposal for owner review and block dependent
   acceptance.
4. Replace the historical chart substitute with actual Apache ECharts through
   validated product-owned `ChartSpec` and the shared
   `packages/chart_compiler_ts` boundary. Select and pin an official supported
   ECharts core version from current primary-source package evidence; do not
   infer a version from memory. Use only tree-shakable allowlisted SVG/Canvas
   renderer modules. Do not add ECharts-GL, WebGL, Plotly, Dash, raw ECharts
   option input, executable callbacks, remote assets, or browser analytical
   reduction.
5. Resolve `available_chart_types`, their order, and the default from exact
   versioned compatibility rules for the authorized dataset profile and report
   type. The user must see the selected type and be able to choose any
   compatible type without silently changing source, filters, comparison,
   grain, measures, permissions, or Result Trust. If authoritative sources do
   not determine the mapping, create a bounded owner proposal and stop; do not
   assume generic time-series alternatives.
6. Keep the accessible data-table alternative as a separate product Data Grid.
   ECharts `dataset` may feed charts but ECharts `dataView` must not implement
   the table surface. Preserve keyboard access, header associations, explicit
   local overflow, sorting/filtering announcements, and the chart/table toggle.
7. Freeze deterministic fixture data, clock, locale, timezone, theme, reduced
   motion, font bundle, asset bundle, ChartSpec, compatibility-policy version,
   dataset profile, and renderer build identity. Record hashes needed to make
   source and implementation captures comparable.
8. At every declared anchor and required coverage tuple, verify required
   regions, geometry, computed styles, page overflow, declared local scroll,
   ECharts output, selector state, data-table alternative, focus/reading order,
   keyboard behavior, accessibility, console, and network. Use exactly one
   browser mechanic selected by `browser-qa-evidence` and route terminal
   mechanics through `playwright-cli`.
9. Produce generated per-anchor visual QA receipts and one generated all-anchor
   screen-acceptance receipt per exact screen revision. Never type a passing
   receipt or hand-edit generated evidence.
10. After automatic gates pass, create
    `.codex/delivery/ui-design-programs/custometry-v1/g4-owner-review-ui-an-003-r1.md`
    with exact source, contract, implementation, fixture, browser, receipt, and
    artifact hashes. Request an explicit owner decision for the exact screen
    revisions. Do not accept the family or allow G5 on the owner's behalf.
11. Assemble
    `.codex/delivery/evidence/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md`
    from `.codex/agents/iteration_report_template.md`, preserving the exact
    ticket proof boundary and observed results.
12. Update only the existing stage ledger after validation and before the final
    report. Preserve a truthful terminal blocker when owner acceptance or any
    gate-required value is absent. Never create another execution-state file.

# Context acquisition protocol

Read `always_read`, then the four `task_entrypoints`. Open a conditional bundle
only when its condition is true and record why the context expanded. Use
`consult_if_needed` only for a named blocker, contract conflict, or failing
gate. Stop when touched paths, contracts, proof, and blockers are known.

# Reading manifest

- Baseline context: eight files maximum before conditional expansion.
- Route registries are pointer-resolution sources, not documents to restate.
- Historical W27/W28 files are evidence only; they do not override revision 5.
- Do not read or revive W18; it is superseded.

# Work plan

1. Claim the exact pending stage and ready ticket through `staged-plan-runner`
   and perform the
   pre-write guard.
2. Resolve contract inputs and any blocking compatibility/visual decisions.
3. Implement the bounded real-ECharts representative candidate and separate
   Data Grid behavior within the expected touch zones.
4. Generate and validate all exact screen contracts.
5. Capture browser/geometry/accessibility evidence and compare rasters at all
   four anchors for every required tuple.
6. Assemble generated receipts and the owner-review artifact.
7. Update the sole stage ledger with status, evidence, file manifest, residual
   risk, and handoff.

# Acceptance criteria

- The accepted revision-5 hashes and owner evidence remain unchanged.
- All 144 required state/role/locale/theme screen revisions validate under
  `screen_contract_ready` and declare the exact four responsive-Web anchors.
- Actual Apache ECharts output is observed through the shared ChartSpec
  compiler boundary; no mock chart is accepted as renderer proof.
- Available/default chart types and user selection are source-backed and
  deterministic for the current dataset/report profile.
- The separate Data Grid alternative, chart/table toggle, accessibility, and
  keyboard behavior pass at every anchor.
- Every required per-anchor receipt and all-anchor screen acceptance is
  generated, hash-linked, and passing before owner review.
- No unresolved G4-required field is hidden. Missing owner acceptance keeps
  `Next stage allowed: false`.
- No mobile artifact, G5/G6 work, production API/persistence/export behavior,
  deployment, commit, push, or publication is performed.

# Implementation constraints

- Preserve product contracts, routes, permissions, roles, business states,
  metrics, and dataset semantics; reference them instead of copying them into a
  new truth source.
- Keep dependency direction `ChartSpec -> shared compiler -> ECharts adapter`.
  UI stores may not compute authoritative metrics or elevate permissions.
- Use accepted semantic tokens and component contracts. Do not broaden the
  chart policy, table engine policy, or component API beyond this family
  without a source-backed contract and compatibility classification.
- Do not loosen geometry or raster tolerances to obtain a pass.
- Do not edit generated screenshots, receipts, or acceptance artifacts by
  hand.
- Preserve foreign changes and stop if an expected touch cannot be safely
  separated.

# Quality gates

Run the exact commands in `validation_strategy`, plus the capture, comparison,
receipt assembly, focused component tests, and browser checks selected by the
required proof skills. A green source/local check does not replace observed
browser, raster, accessibility, console, or network evidence.

# Final output

Report created, modified, and deleted files; every path outside expected touch
zones with a reason; foreign changes excluded; commands and observed results;
all contract and receipt counts; source revisions/hashes; responsive anchors;
ECharts/ChartSpec/compiler and chart-type-selection evidence; Data Grid
evidence; mobile scope; unresolved blockers; owner decision still required;
ledger update; residual risks; and the exact value of `Next stage allowed`.
