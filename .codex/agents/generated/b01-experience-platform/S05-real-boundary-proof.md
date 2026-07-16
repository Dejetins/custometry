---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b01-s05-experience-platform-real-boundary-proof
scope: "Produce fresh Full Stack and real-browser evidence for B01 routes, shell, locale, system surfaces, docs/help, accessibility, reduced motion, responsive behavior, guards, Focus return, restart, and cleanup on the supported local runtime."
spec_version: 0.8.2-draft
requirement_ids: [A11Y-001, A11Y-002, A11Y-003, A11Y-004, A11Y-005, A11Y-006, A11Y-007, A11Y-008, A11Y-009, A11Y-010, AC-028, AC-029, HELP-001, HELP-002, HELP-003, HELP-004, I18N-001, I18N-002, I18N-003, I18N-004, I18N-005, I18N-006, I18N-007, I18N-008, I18N-009, I18N-010, I18N-011, MOTION-001, MOTION-002, MOTION-003, MOTION-004, MOTION-005, MOTION-006, MOTION-007, MOTION-008, MOTION-009, MOTION-010, MOTION-011, MOTION-012, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, UX-JOURNEY-001, UX-JOURNEY-002, UX-JOURNEY-006, V1-AC-007, V1-AC-017, V1-AC-018]
language:
  implementation: en
  repository_artifacts: en
  user_completion_report: ru
context_sources:
  always_read:
    - path: AGENTS.md
      why: repository and evidence contract
    - path: .codex/AGENTS.md
      why: real-boundary and browser proof rules
    - path: docs/architecture/workstreams/b01-experience-platform-plan.md
      why: required browser matrix and exclusions
    - path: docs/architecture/development-runtime-contract.md
      why: mandatory S05 Full Stack boundary, development override rejection, and proof limits
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
      why: sole execution-state authority
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/S04-web-integration.md
      why: nearest accepted implementation and browser-smoke evidence
  task_entrypoints:
    - path: apps/web
      why: production-mode local Web runtime
    - path: docs-site
      why: local docs/help runtime
    - path: docs/architecture/program/requirement-matrix.json
      why: exact browser and acceptance evidence obligations
    - path: compose.yaml
      why: canonical disposable Full Stack topology
    - path: deploy/compose/bootstrap.sh
      why: supported Full Stack lifecycle entrypoint
skill_routing:
  - skill: browser-qa-evidence
    role: primary
    use_when: capturing real browser flows, screenshots, console/network, responsive, and accessibility smoke
  - skill: playwright
    role: companion
    use_when: running deterministic browser journeys through the repository wrapper
  - skill: ui-ux-pro-max
    role: companion
    use_when: interpreting density, hierarchy, motion, responsive, and accessibility findings
change_ownership:
  owned_paths: [docs/architecture/workstreams/b01-experience-platform-stage-reports/S05-real-boundary-proof.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md, narrowly scoped B01 fixes required by failed proof]
  foreign_exclusions: [new product features, downstream services, broad redesign, Penpot mutation, other workstream artifacts, commit, push, merge, deploy]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [docs/architecture/workstreams/b01-experience-platform-stage-reports/S05-real-boundary-proof.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md]
  possible_secondary_touches: [narrow B01 implementation/test/docs fixes directly required by browser proof]
  expected_deletions: []
validation_strategy:
  depth: runtime
  acceptance_surfaces: [clean disposable Full Stack Compose, migration and readiness, Edge/Web/API paths, restart and cleanup, production-mode browser journeys, en/ru, docs/help, system states, responsive and 200 percent zoom, keyboard and accessibility smoke, reduced motion, console and network]
  evidence_target: docs/architecture/workstreams/b01-experience-platform-stage-reports/S05-real-boundary-proof.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b01-full-stack-browser
  exclusions: [real downstream domain correctness, final WCAG audit by itself, production deployment, recovery, performance SLO, firewall/CNI, supply chain, canonical Penpot authority]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B01
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b01-experience-platform-plan.md
  prompt_pack_dir: .codex/agents/generated/b01-experience-platform
  stage_ledger: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
  stage_id: S05
  predecessor_gate:
    stage_id: S04
    allowed_statuses: [accepted, superseded]
  state_preconditions:
    - S04 is accepted or explicitly superseded in the ledger.
    - The ledger is active, current stage is S05, and only S05 has next_allowed true.
    - Production-mode Web and docs/help assets build from a clean dependency activation.
    - The supported container engine, Full Stack lifecycle, browser tooling, and evidence directories are healthy and safely owned.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b01-experience-platform
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S06
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Produce fresh Full Stack and real-browser evidence that the B01 Experience
Platform works through the canonical disposable Compose topology on the
supported local runtime. Exercise migration/readiness, Edge/Web/API paths,
restart and cleanup together with the canonical route and history model,
stable Frost shell, sidebar states, system surfaces, en/ru, docs/help,
unsaved-change guards, responsive density, 200% zoom/reflow, keyboard paths,
focus restoration, reduced motion, and route-backed Focus return. Inspect
console and network behavior and distinguish mock-backed presentation from real
downstream readiness.

## Non-goals

- Do not add new features or broadly redesign during proof.
- Do not claim real business data, authorization, analytics, forecasting, or
  downstream service correctness from generated mocks.
- Do not claim a full formal WCAG conformance audit from automated checks.
- Do not replace the required Full Stack lifecycle with Vite, Hybrid,
  production-build-only, or previously captured evidence.
- Do not run production deployment, recovery, performance, firewall/CNI, or
  supply-chain acceptance.
- Do not mutate Penpot.

## Verified current context

- Fact: S04 acceptance means the composed Web implementation passed narrower
  component and representative integration checks.
- Fact: browser-visible behavior requires real browser, console, network,
  responsive, locale, and interaction observations.
- Fact: screenshots alone cannot prove route history, keyboard behavior,
  accessibility semantics, metadata privacy, or network isolation.
- Fact: retained-data refresh and reduced-motion behavior must be observed
  without inventing value changes.
- Fact: S05 requires the canonical Full Stack topology; no development
  override, bind mount, reload command, or development credential may enter
  the acceptance composition.
- Assumption to verify: the disposable runtime uses the current built source,
  isolated owned state, and no stale development server, volume, or asset
  cache.

## Context acquisition

Verify source revision, dependency activation, image/build identity, Compose
configuration, project and volume ownership, ports, browser version,
viewport/device scale, locale, timezone, color preferences, and reduced-motion
settings. Start from clean disposable Full Stack state. Read S04 evidence and
derive a journey matrix that maps each requirement family to a runtime or
browser observation and artifact. Inspect mock disclosure and test routes
before running journeys.

## Requirements

### Must

- Prove the canonical Full Stack composition parses without any development
  override, source bind mount, reload/debug command, mock flag, mutable release
  image, development credential, or non-Edge host-published core port.
- Prove migration, dependency readiness, actual loopback Edge URL,
  `Edge -> Web`, `Web -> API`, direct `Edge -> API` denial, and the required
  Foundation negative-egress behavior before browser acceptance.
- Prove clean startup from isolated owned state, one controlled restart with
  preserved expected state, bounded shutdown, and post-run cleanup of the
  disposable project resources.
- Prove direct and in-app navigation for representative global, installation,
  workspace, docs/help, system, and Focus routes.
- Prove immutable workspace identity, safe query handling, deep links,
  Back/Forward, workspace switch, unknown route, forbidden route, and no denied
  metadata in title, breadcrumbs, command search, Help, or network payloads.
- Prove expanded and icon-only collapsed sidebar state, accessible labels and
  tooltips, persistence, active state, stable order, and no text blur/bounce.
- Prove shell/topbar stability and bounded main-content fade during route
  changes.
- Prove unsaved-change stay/discard/save-and-continue behavior and restoration.
- Prove 403, 404, session expired, maintenance, and upgrade-required surfaces
  show safe copy, actions, scope/timing where allowed, and bounded refresh.
- Prove en/ru parity for representative journeys, locale-neutral URLs/IDs,
  formatting, fallback, pluralization, and missing-key diagnostics.
- Prove local `/docs` and permission-aware `/help` search, route/field context,
  offline assets, keyboard access, valid links, and forbidden/missing behavior.
- Prove Focus open, direct-link fallback, inherited/system/locked filter
  visibility, local draft Apply/Reset/Undo, Chart/Data-table state continuity,
  close, Escape, and browser Back return to route/block/scroll/focus origin.
- Prove component keyboard paths, visible focus, semantic names/roles, non-hover
  access, skip/navigation behavior, dialog focus trap only where appropriate,
  and no keyboard trap.
- Prove supported desktop/tablet widths, compact density, long translated text,
  and 200% zoom/reflow without clipped actions or lost content.
- Prove normal and reduced-motion variants; reduced mode removes translate,
  scale, bounce, shimmer, and continuous chart animation.
- Prove first-load versus refresh behavior, retained data/reserved layout,
  freshness/loading status, and no flying table rows.
- Inspect browser console for errors/warnings and network for failures,
  unexpected external requests, secrets, denied metadata, and remote assets.
- Record screenshots or traces for representative states, plus textual evidence
  for behavior screenshots cannot prove.
- Rerun focused checks after any proof fix and rerun every invalidated journey.

### Should

- Use deterministic seeded contract fixtures and stable selectors.
- Capture accessibility tree or semantic snapshots for critical surfaces.
- Check one high-contrast or forced-colors smoke path if supported.
- Record approximate observed transition timing without treating visual timing
  as performance SLO evidence.

## Forbidden actions

- Do not patch expected screenshots or fixtures to hide a real defect.
- Do not disable console, network, accessibility, locale, or reduced-motion
  checks to obtain green evidence.
- Do not use a stale dev server, cached bundle, or previously captured artifact
  as fresh proof.
- Do not add `compose.dev.yaml`, host-only application processes, or persistent
  developer volumes to make the Full Stack proof pass.
- Do not print secrets, cookies, authorization headers, raw local storage, or
  private provider payloads.
- Do not claim mocked permissions are server authorization proof.
- Do not expand into downstream feature implementation.
- Do not infer commit, push, deploy, or release authority.

## Work plan and stop gates

1. Verify S04 acceptance, source/image/runtime identity, container and browser
   tool health, isolated project ownership, and evidence locations.
2. Validate the canonical composition and prove that no development override
   or convenience setting is present.
3. Build and start clean disposable Full Stack Compose, run migration/readiness
   and positive/negative network-path probes, and record the actual Edge URL.
4. Run route/history/workspace/system-state journeys in English through Edge.
5. Repeat representative journeys in Russian and validate formatting/parity.
6. Run sidebar, guard, docs/help, Focus return, loading/refresh, and mock
   disclosure journeys.
7. Run keyboard, semantic, responsive, long-text, 200% zoom, and reduced-motion
   matrix.
8. Inspect console/network and capture screenshots, traces, and textual
   observations.
9. Restart the owned Full Stack runtime, verify expected state/readiness and a
   representative browser path, then shut it down and verify cleanup.
10. Fix only narrow B01 defects, rerun focused gates, and repeat affected
   journeys.
11. Write S05 evidence, then update the ledger and unlock only S06 if accepted.

Stop on stale runtime, failed build/migration/readiness, development override
or foreign/persistent state in the acceptance topology, failed required network
path, restart or cleanup failure, missing browser capability, metadata or
secret leak, unexpected external request, inaccessible required journey,
unrestored focus/history, clipped critical action, reduced-motion violation,
unresolved console/network error, or a required flow that depends on unbuilt
downstream truth.

## Contracts and side effects

Authorized effects are repository-owned disposable containers, networks,
volumes, local build/cache state, browser sessions, test data generated from
accepted contracts, and stage-owned evidence artifacts. Use bounded loopback
ports, unique project identity, and verified cleanup. Do not access real user
accounts or external services. Any implementation fix that changes contract,
URL, default, storage, image, topology, or visible behavior must be classified;
runtime/browser evidence predating the fix is stale for the affected path.

## Validation and evidence

- Run the repository Compose lifecycle and browser QA workflows against the
  same actual disposable Full Stack runtime, or record why a repository
  wrapper must be corrected before proof can continue.
- Run focused Web/component/integration tests plus route, localization, docs,
  contract, DDD, type, lint, and staged-work checks after fixes.
- Capture source/image/Compose/runtime/browser identity, commands, project and
  actual URL, migration/readiness/network probes, restart result, viewports,
  locale, motion setting, screenshots/traces, semantic observations,
  console/network results, and cleanup post-conditions.
- Write durable evidence to
  `docs/architecture/workstreams/b01-experience-platform-stage-reports/S05-real-boundary-proof.md`.
- State explicit exclusions: real B03–B13 behavior, production deployment,
  formal full WCAG conformance, recovery, performance SLO, firewall/CNI,
  supply-chain, Penpot, and final release.

## Acceptance criteria

- [ ] All required route/history/workspace/system-state journeys pass on the
      current disposable Full Stack runtime through Edge.
- [ ] Canonical composition, migration/readiness, required network paths,
      restart, shutdown, and owned-resource cleanup pass with no development
      override or persistent foreign state.
- [ ] Sidebar, shell, guards, docs/help, Focus return, loading/refresh, and mock
      disclosure behave as contracted.
- [ ] Representative en/ru journeys and formatting/parity checks pass.
- [ ] Keyboard, focus, semantic, responsive, 200% zoom, and reduced-motion
      evidence has no unresolved required defect.
- [ ] Console/network inspection has no unexplained error, failed request,
      external asset, secret, or denied metadata.
- [ ] Every screenshot/trace is tied to source/runtime state and supported by
      textual behavioral evidence.
- [ ] Any fix has focused regression checks and refreshed affected journeys.
- [ ] Proof boundaries and downstream mock limitations are explicit.
- [ ] Ledger transition occurs before handoff and only S06 is unlocked.

## Result and handoff

Report status, image/Compose/runtime/browser identity, lifecycle and network
evidence, journey matrix, artifacts, console/network observations,
accessibility/responsive/motion findings, contract impact, fixes, file
manifest, blockers, residual risks, exclusions, cleanup post-condition, and
exact ledger transition. Hand off S06 only with fresh accepted S05 evidence.
