---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b01-s04-experience-platform-web-integration
scope: "Compose the Frost Web shell, shared components, representative route-backed flows, system surfaces, docs/help, navigation guards, and Focus shell from accepted B01 contracts and adapters."
spec_version: 0.8.2-draft
requirement_ids: [A11Y-001, A11Y-002, A11Y-003, A11Y-004, A11Y-005, A11Y-006, A11Y-007, A11Y-008, A11Y-009, A11Y-010, AC-028, AC-029, HELP-001, HELP-002, HELP-003, HELP-004, I18N-001, I18N-002, I18N-003, I18N-004, I18N-005, I18N-006, I18N-007, I18N-008, I18N-009, I18N-010, I18N-011, MOTION-001, MOTION-002, MOTION-003, MOTION-004, MOTION-005, MOTION-006, MOTION-007, MOTION-008, MOTION-009, MOTION-010, MOTION-011, MOTION-012, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, THEME-001, THEME-002, THEME-003, THEME-004, THEME-005, THEME-006, THEME-007, THEME-008, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, UX-JOURNEY-001, UX-JOURNEY-002, UX-JOURNEY-006]
language:
  implementation: en
  repository_artifacts: en
  user_completion_report: ru
context_sources:
  always_read:
    - path: AGENTS.md
      why: repository implementation and Git discipline
    - path: .codex/AGENTS.md
      why: browser, validation, and evidence rules
    - path: docs/architecture/workstreams/b01-experience-platform-plan.md
      why: UI scope and proof boundary
    - path: docs/architecture/development-runtime-contract.md
      why: Fast Loop Web integration, optional Hybrid escalation, and production rejection rules
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
      why: sole execution-state authority
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/S03-adapters.md
      why: accepted adapter and generation state
  task_entrypoints:
    - path: apps/web
      why: Web composition root
    - path: docs-site
      why: local documentation and Help surfaces
    - path: docs/architecture/workstreams/b01-experience-platform-module.md
      why: UI ownership and non-goals
skill_routing:
  - skill: ui-ux-pro-max
    role: primary
    use_when: implementing hierarchy, density, tokens, components, responsive layout, motion, and accessibility
  - skill: product-design:index
    role: companion
    use_when: checking user flows and composed product experience without creating a new design authority
  - skill: contract-impact-analysis
    role: companion
    use_when: implementation exposes browser-contract drift
change_ownership:
  owned_paths: [apps/web/**, B01-owned UI packages and component tests, docs-site B01 surfaces, docs/architecture/workstreams/b01-experience-platform-stage-reports/S04-web-integration.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md]
  foreign_exclusions: [downstream business UI implementations, real service behavior, Penpot mutation, other workstream ledgers, commit, push, merge, deploy]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [B01 Web shell/components/routes identified by S01-S03, their component and integration tests, docs/architecture/workstreams/b01-experience-platform-stage-reports/S04-web-integration.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md]
  possible_secondary_touches: [B01 contracts/adapters for verified compatible fixes, docs/help content and indexes]
  expected_deletions: []
validation_strategy:
  depth: browser
  acceptance_surfaces: [component states, representative route flows, responsive layout, keyboard interaction, accessibility smoke, local docs/help, console and network smoke]
  evidence_target: docs/architecture/workstreams/b01-experience-platform-stage-reports/S04-web-integration.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b01-composed-web-integration
  exclusions: [complete S05 browser matrix, real downstream domain correctness, canonical Penpot authority, product milestone acceptance, deployment]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B01
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b01-experience-platform-plan.md
  prompt_pack_dir: .codex/agents/generated/b01-experience-platform
  stage_ledger: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
  stage_id: S04
  predecessor_gate:
    stage_id: S03
    allowed_statuses: [accepted, superseded]
  state_preconditions:
    - S03 is accepted or explicitly superseded in the ledger.
    - The ledger is active, current stage is S04, and only S04 has next_allowed true.
    - Generated client/mock, route, localization, docs/help, error, and asset adapters pass focused integration checks.
    - Mock-backed surfaces are visibly disclosed and cannot be mistaken for real downstream readiness.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b01-experience-platform
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S05
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Compose a usable Frost Experience Platform from the accepted B01 core and
adapters. Implement the stable shell, expanded and collapsed navigation,
topbar, compact page context, shared components, loading/status patterns,
system surfaces, route/history guards, local docs/help, and a representative
route-backed Focus shell. Demonstrate representative interactions in a real
local browser without overclaiming downstream product behavior.

## Non-goals

- Do not implement real analytics, forecasting, customers, data, reports,
  pipelines, operations, or administration domain behavior.
- Do not replace contract-generated mocks with hand-authored fake data.
- Do not complete the full S05 browser matrix in this integration stage.
- Do not introduce a second chart engine, Dash, Plotly core dependency, or
  WebGL.
- Do not mutate or treat Penpot as runtime authority.

## Verified current context

- Fact: S03 adapters and generated mocks passed their narrower integration
  boundary.
- Fact: the Frost theme is a semantic token system, not a set of per-screen
  color values.
- Fact: compact KPI/context groups must preserve alignment and leave useful
  space for data.
- Fact: the sidebar uses icons plus labels when expanded and accessible icons
  only when collapsed.
- Fact: shell/sidebar/topbar remain stable across route changes; main content
  uses a short fade and keeps previous data during refresh.
- Fact: Focus is a route-backed application surface, not a nested modal.
- Fact: S04 normally runs in Fast Loop with explicit generated-mock
  disclosure; a real-API claim requires Hybrid evidence and cannot be inferred
  from Vite or mocked browser behavior.

## Context acquisition

Read S03 evidence and the accepted component/route contracts. Inspect the
current Web composition root, CSS/token conventions, component test harness,
browser command, docs/help serving path, and mock disclosure. Use current
source-backed requirements; screenshots may guide visual comparison but cannot
override the contracts. If an exact visual decision depends on unconfirmed
Penpot authority, implement the semantic contract and record the deferred
design-file reconciliation.

## Requirements

### Must

- Implement semantic Frost foundations and bind components to tokens rather
  than raw visual constants.
- Implement a stable shell with workspace selector, command/search surface,
  Help, notifications affordance, user menu, and responsive behavior.
- Implement expanded sidebar with icons and labels and collapsed sidebar with
  the same icons, accessible names/tooltips, stable order, active state, and
  `180–220 ms` non-bouncing transition.
- Implement compact page header/context for title, route identity, period,
  `vs LY`, applied filter summary, and actions without excessive vertical air.
- Implement aligned compact KPI groups and shared table/chart containers; do
  not reserve permanent space for optional Result Trust detail.
- Implement buttons, inputs, tabs, menus, popovers, drawers, dialogs, banners,
  statuses, loading, progress, skeleton, tables, pagination, and empty/error
  states with accepted states and keyboard behavior.
- Implement route navigation with stable shell and `120–160 ms` main-content
  fade, retained prior data on refresh, and no full-screen slide.
- Implement tabs, drawers, dialogs, popovers, and safe chart/container motion
  within accepted ranges; implement reduced-motion substitutions.
- Implement 403, 404, session-expired, maintenance, and upgrade-required
  surfaces with safe actions and no metadata leakage.
- Implement unsaved-change guard and deterministic return/cancel behavior.
- Implement local `/docs` and permission-aware `/help` with contextual links,
  search, keyboard access, and visibility-safe missing/forbidden states.
- Implement en/ru switching and locale formatting without changing route or
  object IDs.
- Implement a representative Focus shell with inherited filters, local draft
  controls, Apply/Reset/Undo affordances, Result Trust/export slots,
  Chart/Data-table switch contract, and return-to-origin behavior using
  contract-backed placeholder content only.
- Implement explicit development/mock disclosure that cannot appear in an
  accepted production build.
- Add component and integration tests for anatomy, states, keyboard behavior,
  locale, reduced motion, responsive density, routes, guards, system surfaces,
  docs/help, and Focus shell.

### Should

- Keep dense business surfaces scannable at supported desktop widths.
- Preserve layout height during loading and refresh.
- Use one coherent icon family with local assets, accessible naming, and
  license provenance.
- Prefer native semantics before ARIA and avoid focus traps outside true modal
  dialogs.

## Forbidden actions

- Do not use absolute-positioned per-screen fixes for shared layout.
- Do not hide button text through clipping or misalign labels and icons.
- Do not animate data changes in a way that implies values changed differently
  from the underlying result.
- Do not use hover-only access to information.
- Do not ship remote assets, raw tokens, secrets, denied metadata, or
  development mock banners in production mode.
- Do not implement authorization solely by hiding UI.
- Do not infer publish, deploy, or release authority.

## Work plan and stop gates

1. Verify S03 acceptance, selected runtime mode, local commands, package
   boundaries, and exact owned component/surface manifest.
2. Implement Frost tokens and representative shared components with tests.
3. Assemble shell, navigation, page context, and responsive density.
4. Implement routes, history, guards, system surfaces, docs/help, locale, and
   mock disclosure.
5. Implement Focus shell and return-to-origin using contract-backed content.
6. Add motion/reduced-motion and loading/refresh behavior.
7. Run component, type, lint, route, localization, docs, accessibility, and
   focused integration tests.
8. Start the local Web/docs runtime and run representative browser smoke with
   console/network inspection.
9. When a real API boundary is claimed, run the corresponding Hybrid browser
   flow; otherwise label the entire flow as generated-mock Fast Loop evidence.
10. Verify development/mock disclosure is rejected by a production build.
11. Write S04 evidence, then update the ledger and unlock only S05 if accepted.

Stop on inaccessible keyboard flow, unstable layout, route/history failure,
metadata leak, remote asset, console/network error, mock/real ambiguity,
unresolved contract drift, or a design-file dependency outside authority.

## Contracts and side effects

Authorized side effects are local package/build caches, local Web/docs
processes, and test/browser artifacts in approved temporary locations. No
external service, persistent product database, user email, deployment, or
design-tool mutation is authorized. Any browser-visible contract correction is
classified and reconciled with S01–S03 before acceptance.

## Validation and evidence

- Run focused component, integration, type, lint, route, localization, docs,
  token, contract, and DDD checks.
- Build production-mode Web and docs/help assets with remote-network use
  disabled.
- Run representative browser flows for shell/sidebar, route changes, locale,
  guard, each system surface, docs/help, and Focus return.
- Inspect console errors, failed requests, unexpected external requests,
  accessible names, keyboard order, focus restoration, and reduced motion.
- Capture responsive evidence for supported desktop and tablet widths and 200%
  zoom smoke, but reserve complete matrix acceptance for S05.
- Record exact commands, artifacts, screenshots, console/network observations,
  selected mode, escalation decision, mock/real proof boundary, and file
  manifest in
  `docs/architecture/workstreams/b01-experience-platform-stage-reports/S04-web-integration.md`.

## Acceptance criteria

- [ ] Frost tokens and representative components are reusable, aligned, dense,
      responsive, and state-complete.
- [ ] Expanded/collapsed sidebar, stable shell, page context, routes, guards,
      system surfaces, docs/help, locale, and Focus shell work locally.
- [ ] Motion durations and reduced-motion substitutions match contracts.
- [ ] Keyboard, focus, semantics, and basic reflow checks pass.
- [ ] No remote asset, denied metadata, unsafe storage, console error, or
      unexpected network request is observed.
- [ ] Mock-backed content is explicitly bounded and cannot be confused with
      real service readiness.
- [ ] Focused gates pass and S04 records its incomplete S05 proof boundary.
- [ ] Ledger transition occurs before handoff and only S05 is unlocked.

## Result and handoff

Report status, UI/component/route files, contract impact, browser smoke
evidence, responsive and accessibility observations, console/network results,
file manifest, blockers, residual risks, and exclusions. Hand off S05 only
after accepted S04 evidence and ledger synchronization.
