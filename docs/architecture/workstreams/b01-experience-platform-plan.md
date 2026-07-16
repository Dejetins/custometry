---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B01
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b01-experience-platform-module.md
plan_doc: docs/architecture/workstreams/b01-experience-platform-plan.md
prompt_pack_dir: .codex/agents/generated/b01-experience-platform
stage_ledger: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
execution_mode: goal_driven
hard_dependencies: [W00]
soft_dependencies: []
stage_ids: [S00, S01, S02, S03, S04, S05, S06]
release_milestones: [product_foundation, vertical_alpha, public_mvp, v1_target]
spec_version: 0.8.2-draft
requirement_ids:
  - A11Y-001
  - A11Y-002
  - A11Y-003
  - A11Y-004
  - A11Y-005
  - A11Y-006
  - A11Y-007
  - A11Y-008
  - A11Y-009
  - A11Y-010
  - AC-028
  - AC-029
  - GAP-021
  - GAP-034
  - GAP-035
  - GAP-046
  - HELP-001
  - HELP-002
  - HELP-003
  - HELP-004
  - I18N-001
  - I18N-002
  - I18N-003
  - I18N-004
  - I18N-005
  - I18N-006
  - I18N-007
  - I18N-008
  - I18N-009
  - I18N-010
  - I18N-011
  - MOTION-001
  - MOTION-002
  - MOTION-003
  - MOTION-004
  - MOTION-005
  - MOTION-006
  - MOTION-007
  - MOTION-008
  - MOTION-009
  - MOTION-010
  - MOTION-011
  - MOTION-012
  - RISK-010
  - ROUTE-001
  - ROUTE-002
  - ROUTE-003
  - ROUTE-004
  - ROUTE-005
  - ROUTE-006
  - ROUTE-007
  - ROUTE-008
  - ROUTE-009
  - ROUTE-010
  - ROUTE-011
  - ROUTE-012
  - SYS-UI-001
  - SYS-UI-002
  - SYS-UI-003
  - SYS-UI-004
  - SYS-UI-005
  - TEST-INV-022
  - TEST-INV-023
  - TEST-INV-042
  - TEST-INV-050
  - TEST-INV-051
  - THEME-001
  - THEME-002
  - THEME-003
  - THEME-004
  - THEME-005
  - THEME-006
  - THEME-007
  - THEME-008
  - UI-DENSITY-001
  - UI-DENSITY-002
  - UI-DENSITY-003
  - UI-SHELL-001
  - UI-SHELL-002
  - UI-SHELL-003
  - UX-JOURNEY-001
  - UX-JOURNEY-002
  - UX-JOURNEY-006
  - V1-AC-007
  - V1-AC-017
  - V1-AC-018
---

# B01 Experience Platform — Plan

## Identity and authority

- program/workstream: `custometry-v1 / B01`;
- bounded owner: Experience Platform;
- accepted authority: the normative product blueprints, canonical program
  plan, B01 module definition, requirement matrix, accepted development
  runtime contract, and accepted W00 proof;
- current proof boundary: this is an initial plan with executable prompts, not
  evidence that any browser journey, route, accessibility behavior, or Penpot
  surface exists;
- activation rule: B01 remains dormant until W00 is accepted, the preparation
  set passes independent review, the user authorizes activation, and
  `.codex/PLANS.md` registers this exact trio;
- branch rule: use one short-lived `codex/b01-experience-platform` branch for
  the whole workstream unless the user explicitly changes the workflow;
- execution rule: one Codex Goal owns the active B01 S00–S06 iteration; each
  stage remains separately ledger-authorized, validation and the ledger update
  precede handoff, and the Goal continues only after re-reading an explicit
  successor unlock.

## Objective and non-goals

Deliver a maintainable Frost Experience Platform: semantic design tokens and
components, a workspace-aware route registry and stable application shell,
generated contract mocks, system surfaces, local `/docs` and `/help`, complete
English/Russian localization structure, accessibility, reduced motion, and
real-browser evidence. Later bounded contexts must be able to integrate through
versioned contracts without rebuilding navigation, filters, Help, loading,
error, or interaction conventions.

Non-goals:

- implementing analytics, forecasting, customer, data, reporting, execution,
  identity, or operations domain behavior;
- accepting hand-authored mock payloads as API contract evidence;
- treating screenshots or design frames as runtime acceptance;
- confirming, selecting, or mutating the canonical Penpot file;
- introducing Dash, Plotly, another production chart engine, or WebGL;
- publishing, deploying, or claiming product-foundation completion.

## Current-state fact ledger

| Type | Fact, assumption, proposal, or unknown | Source/evidence | Consequence |
|---|---|---|---|
| Fact | The product blueprints define canonical routes, Frost, compact density, motion, system surfaces, Focus/Explore, en/ru, accessibility, `/docs`, and `/help`. | normative blueprints and requirement index | S00/S01 must translate these into versioned contracts without changing product meaning. |
| Fact | The B01 module owns presentation and navigation state, not analytical truth. | B01 module definition | Domain metrics, filters, result identity, and persistence remain owned by later workstreams. |
| Fact | ECharts is the only v1 Web chart engine, behind product-owned `ChartSpec`. | normative blueprint | B01 may provide presentation slots and adapter seams but does not add another chart dependency. |
| Fact | Focus/Explore is route-backed and returns to route, block, scroll, and focus origin. | `ROUTE-006`, `V1-AC-017` | It cannot be implemented as a nested full-screen modal. |
| Fact | Repository artifacts are English by default; public product help is bilingual. | repository instructions | Source identifiers remain locale-neutral and catalogs must have parity. |
| Fact | Development has four explicit proof modes: `fast-loop`, `hybrid`, `full-stack`, and `release`. Fast Loop is partially implemented, Hybrid is target-only, Full Stack exists for the Foundation surface, and no accepted release bundle exists. | [development runtime contract](../development-runtime-contract.md) | B01 must own the Fast Loop Web/mock experience, disclose mock versus real mode, and escalate real integration and acceptance evidence instead of overclaiming host behavior. |
| Assumption | W00 provides reproducible Node, pnpm, uv, Docker, and M3 Pro Foundation evidence before activation. | hard dependency | Missing or stale W00 proof blocks S00. |
| Unknown | The exact canonical Penpot file and write authority are intentionally deferred. | user decision | Repository-local contracts and implementation can proceed; Penpot mutation must stop. |
| Unknown | Stable API schemas from B03–B10 do not yet exist. | program order | Use generated mocks from explicit provisional schemas and reconcile each consumer later. |

## Dependencies and milestones

| Dependency | Type | Required state/evidence | Failure behavior |
|---|---|---|---|
| `W00` | hard | accepted Foundation proof, reproducible package-manager activation, valid repository gates, and current runtime envelope | keep B01 dormant and every stage `next_allowed: false` |

Release contribution:

- `product_foundation`: shell, route registry, tokens/components, generated
  mocks, system surfaces, docs/help, i18n, and accessibility baseline;
- `vertical_alpha`: stable slots and interaction contracts for the first real
  reportable slice;
- `public_mvp`: complete route/history, system-state, Help, locale, responsive,
  and accessibility behavior for public-MVP journeys;
- `v1_target`: full route-backed Focus/Explore and final cross-context
  reconciliation without changing result identity.

## Requirement allocation

| Requirement family | Owning stages | Acceptance evidence |
|---|---|---|
| `THEME-*`, `UI-DENSITY-*`, `UI-SHELL-*` | `S01`–`S05` | semantic token contract, component states, responsive/density browser evidence |
| `ROUTE-*`, `SYS-UI-*` | `S01`–`S05` | route manifest, guards/history/deep-link tests, browser Back/Forward/Escape and system-state flows |
| `HELP-*`, `I18N-*` | `S01`, `S03`–`S05` | metadata validation, local docs/help integration, en/ru parity, forbidden-content negatives |
| `MOTION-*` | `S01`–`S05` | transition matrix, reduced-motion policy, computed-style and browser-timing evidence |
| `A11Y-*` | `S01`–`S05` | semantic, keyboard, screen-reader, reflow, contrast, focus, and reduced-motion evidence |
| `UX-JOURNEY-001`, `UX-JOURNEY-002`, `UX-JOURNEY-006` | `S00`, `S01`, `S04`, `S05` | route-backed journeys across onboarding, primary shell use, and Help/system recovery |
| `AC-028`, `AC-029`, `V1-AC-007`, `V1-AC-017`, `V1-AC-018` | `S04`–`S06` | real-browser acceptance, offline/local docs behavior, route registry, en/ru, and accessibility |
| `GAP-021`, `GAP-034`, `GAP-035`, `GAP-046`, `RISK-010`, `TEST-INV-*` | `S00`–`S06` | explicit decisions, negative tests, contract identity checks, and residual-risk disposition |

## DDD target and contracts

B01 is a composition and presentation platform with a framework-independent
policy core:

- route, Help, localization, motion, system-surface, and Focus state contracts
  are plain versioned data;
- React components consume application ports and do not query business
  persistence directly;
- API clients and development mocks are generated from the same versioned
  OpenAPI/JSON Schema examples;
- generated-mock and real-API modes are explicit, observable development
  states rather than hidden environment behavior;
- browser state is not authorization, execution truth, or durable result state;
- later contexts integrate through public contracts and slots, not imports of
  B01 internals;
- raw color, spacing, typography, route, error, and translation literals do not
  bypass their registries.

Initial contract impact is `compatible-change` because no stable product
consumer exists. Once route IDs, token names, preference DTOs, Help IDs, system
codes, or Focus semantics are consumed, removal or meaning change becomes
`breaking-change` unless migrated.

## Stage plan

| Stage | Outcome | Entry gate | Exit evidence | Stop gate |
|---|---|---|---|---|
| `S00` | Freeze repository/UI inventory, requirement routing, ownership, provisional consumers, runtime-mode facts, risks, and exact file manifest. | W00 accepted; B01 activated | discovery report, contract-impact map, implementation slices, mode/escalation map, browser matrix, and unresolved decisions | missing W00 proof, unknown ownership, unsafe mixed-file scope, release/dev topology ambiguity, or Penpot-dependent decision blocks |
| `S01` | Freeze route, token, component, motion, system-surface, Help, i18n, accessibility, generated-mock, mock/real runtime configuration, and Focus contracts. | `S00 accepted` | schemas/examples, compatibility rules, design-token/component catalog, route and state matrices, API/mock plan, and development-mode disclosure contract | ambiguous route identity, auth leakage, inaccessible interaction, unversioned mock, hidden runtime mode, or hidden Penpot authority blocks |
| `S02` | Implement and test framework-independent policy/application core. | `S01 accepted` | unit/property tests for route resolution, navigation restoration, filters/presentation identity boundaries, localization, motion, system surfaces, and preference state | browser/framework coupling in core, locale-dependent IDs, authorization in UI state, or unstable identity blocks |
| `S03` | Implement adapters and composition seams. | `S02 accepted` | generated client/mock parity, route/help/docs/localization adapters, SSR-safe token/component infrastructure, failure mapping, and integration tests; Hybrid integration is used only for real stateful seams owned by downstream contexts | hand-authored contract drift, hidden mock/real selection, remote runtime dependency, unsafe storage/logging, or adapter ownership leakage blocks |
| `S04` | Assemble the Frost shell and representative route-backed flows. | `S03 accepted` | real app shell, expanded/icon-only sidebar, topbar, page header, docs/help, system surfaces, navigation guards, Focus shell, responsive and accessibility tests in Fast Loop, plus Hybrid browser flows when a real API boundary is claimed | domain fake presented as real, hidden mode, unstable layout, missing keyboard path, or inaccessible local docs blocks |
| `S05` | Produce fresh real-browser evidence on the supported Full Stack local runtime. | `S04 accepted` | clean disposable Compose plus en/ru journeys, deep links/history, sidebar persistence, system states, guards, docs/help, Focus return, responsive/reflow, a11y, reduced motion, console/network, restart, and cleanup evidence | stale bundle, development override in the acceptance topology, metadata leak, remote asset, console/network failure, keyboard trap, or unproved required journey blocks |
| `S06` | Reconcile requirements, contracts, docs, rollback, and independent acceptance. | `S05 accepted` | traceability, cold-review verdict, fixed blockers, grouped gates, ledger completion, and milestone contribution statement | any missing/stale browser evidence, unresolved requirement, docs drift, or review blocker prevents completion |

## UI, route, and motion contract

The first implementation iteration must preserve these cross-release rules:

- expanded sidebar shows icons and labels; collapsed sidebar keeps stable,
  accessible icons and tooltips;
- shell, sidebar, and topbar remain stable while main content uses a short
  `120–160 ms` fade;
- sidebar transition is `180–220 ms`, drawers `200–240 ms`, dialogs
  `160–200 ms`, popovers `100–140 ms`, and tab indicators `120–160 ms`;
- reduced motion removes translate, scale, bounce, shimmer, and continuous
  chart animation while retaining concise fade/status feedback;
- page routes are workspace-aware, locale-neutral, allowlisted, deep-linkable,
  and protected by permission and unsaved-change guards;
- Focus/Explore is a route-backed full-viewport surface; Back, Escape, and
  Close restore route, block, scroll, and focus with a deterministic direct-link
  fallback;
- refresh preserves prior data and reserved layout; first-load skeletons do not
  become continuous shimmer;
- system surfaces include 403, 404, session expired, maintenance, and upgrade
  required with safe actions and no denied metadata;
- all button labels, text baselines, separators, compact KPI groups, and
  responsive grids use shared component geometry rather than per-screen fixes.

## Validation and proof boundaries

Validation progresses from contracts to real browser and uses the runtime modes
without confusing their proof boundaries:

1. S00 records current Fast Loop commands, missing Hybrid capabilities, and the
   escalation expected for each B01 slice;
2. metadata, route, localization, docs visibility, and staged-work validators;
3. Fast Loop token/component and framework-independent policy tests;
4. generated client/mock parity and adapter integration tests, using Hybrid
   only when a real API or stateful boundary is claimed;
5. component/a11y tests for states and keyboard behavior;
6. built local Web runtime with real route navigation and explicit mock/real
   disclosure;
7. Full Stack browser journeys with console/network, responsive, zoom, locale,
   reduced-motion, restart, and cleanup evidence;
8. independent cold review and grouped repository gates.

Expected durable stage reports live under
`docs/architecture/workstreams/b01-experience-platform-stage-reports/`.
Screenshots may support browser evidence but never replace semantic,
interaction, console/network, or accessibility observations.

Explicit exclusions:

- canonical Penpot file selection or mutation;
- business-domain correctness;
- real B03–B13 adapters before their contracts exist;
- production deployment, recovery, firewall/CNI, performance, supply-chain, or
  full release readiness.

## Documentation continuity

B01 owns the implementation contract for local public `/docs` and authenticated
or permission-aware `/help`, but does not expose internal architecture, ADRs,
plans, prompts, ledgers, secrets, or raw runtime evidence. Any behavior change
updates the smallest authoritative English source and generated indexes.
Localized `docs-site/docs/ru/**` changes are allowed only for product-facing
copy and must remain semantically aligned with English.

The B01 implementation and stage evidence must remain synchronized with the
[development runtime contract](../development-runtime-contract.md). B01 does
not own `compose.dev.yaml`, stateful infrastructure lifecycle, release
composition, or production firewall/CNI policy.

## Risks and open decisions

| Risk/decision | Owner | Due stage | Mitigation or stop condition |
|---|---|---|---|
| Penpot authority is unresolved. | User/product design | separate discussion | no Penpot mutation or canonical-file claim; source-backed work may continue |
| Provisional mocks may drift from later services. | Contract owner | `S01`–consumer activation | generate from versioned schemas, mark provisional, and require parity reconciliation |
| Fast Loop behavior may be mistaken for real integration or release behavior. | B01 + QA | `S00`–`S06` | visible mock/real disclosure, explicit mode in evidence, Hybrid for real adapters, and Full Stack for S05 |
| Route and Help indexes may leak denied metadata. | B01 + B03 | `S01`, `S03`, `S05` | permission-filter server results and negative browser/API evidence |
| Frost tokens may become screen-specific constants. | B01 | `S01`–`S04` | semantic tokens, linting, component variants, and no raw-value bypass |
| Accessibility could be tested too late. | B01 | every stage | semantic/keyboard requirements in contracts, components, and real-browser gates |
| Local docs may accidentally ship internal files. | Documentation Platform | `S03`–`S06` | visibility metadata, allowlisted build, link/index validation, and negative tests |
| Browser evidence may overclaim downstream features. | B01 | `S04`–`S06` | explicit generated-mock banner and proof-boundary labels |

## Change ownership

Primary owned paths:

- `apps/web/**`;
- B01-owned UI packages and public contracts introduced through accepted S01;
- `docs-site/**` surfaces owned by B01;
- B01 module, plan, stage reports, ledger, and prompt pack;
- exact architecture/index entries affected by B01 truth.

Foreign or coordination-only paths:

- B02–B13 domain/application/adapters and their ledgers;
- W00 proof except read-only dependency verification;
- normative product blueprint meaning without explicit product authority;
- canonical Penpot file;
- unrelated dirty worktree changes.

If an owned change and a foreign change share a file and safe hunk separation
is not possible, stop rather than broad-stage, revert, or overwrite.

## Activation and completion

Activation requires:

1. accepted W00 Foundation proof;
2. the complete program preparation set passing local validators and cold
   review;
3. explicit user authorization;
4. `.codex/PLANS.md` registering B01 as the sole active workstream;
5. ledger state `active`, `current_stage: S00`, and only S00
   `next_allowed: true`.

Completion requires every S00–S06 stage to be accepted or explicitly
superseded with valid evidence, no unresolved required requirement or review
blocker, an accepted S05 browser boundary matching the final implementation,
and a completed ledger. B01 completion establishes only the Experience
Platform contribution, not product-foundation or product release acceptance.
