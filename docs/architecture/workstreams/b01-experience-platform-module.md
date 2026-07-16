---
artifact_kind: module_definition
staged_schema_version: 1
workstream_id: B01
doc_id: MODULE-B01-EXPERIENCE-PLATFORM
title: B01 Experience Platform module definition
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: experience-platform
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
status: initial
proof_boundary:
  label: planned-experience-platform-boundary
  exclusions:
    - implemented-browser-journeys
    - penpot-authority-confirmation
    - domain-context-readiness
---

# B01 Experience Platform — module definition

> This definition precedes B01 execution. It defines ownership and contracts; it
> is not browser evidence, a Penpot authority record, or proof that planned
> routes are implemented.

## Identity

- bounded owner: Experience Platform;
- primary composition root: `apps/web`;
- shared contracts: `packages/contracts`, `packages/localization`,
  `packages/chart_compiler_ts`;
- contributor documentation boundary: `docs-site`, `/docs`, and `/help`;
- release scope: product foundation through `v1_target`;
- requirement authority: every row whose `primary_workstream` is `B01` in
  `docs/architecture/program/requirement-matrix.json`;
- upstream: W00 repository contracts and canonical product/UI blueprints;
- downstream: every product workstream that exposes a browser journey.

## Purpose and non-goals

B01 provides one stable, accessible, localized, route-backed Web workspace into
which later contexts integrate without inventing their own shell, state,
navigation, filter, motion, Help, or design-token conventions.

Non-goals:

- implementing business calculations or persistence owned by later contexts;
- treating mock data, static screens, screenshots, or Penpot frames as product
  readiness;
- storing business metrics in React components or chart adapters;
- adding a second production chart engine;
- confirming or changing the canonical Penpot file in this workstream
  preparation task.

## Ubiquitous language

| Term | Meaning | Not the same as |
|---|---|---|
| Experience Platform | Shared Web shell and interaction contracts | A business bounded context |
| Route registry | Versioned route identity, path, role and Help mapping | Router implementation alone |
| System surface | 403, 404, session, maintenance or upgrade state | Domain empty state |
| Focus / Explore | Route-backed expanded reportable block | Nested modal |
| Result Trust | User-visible result provenance and limitation summary | Generic success badge |
| Frost | Current design direction and semantic token profile | Permission to hardcode raw colors |
| Contract-generated mock | Adapter generated from the same versioned contract as the client | Manually invented fixture shape |

## Domain and state model

The Experience Platform is deliberately thin. It owns interaction and
presentation state, not analytical truth.

- `WorkspaceRoute`: stable route ID, path template, required capability,
  permission scope, Help target, title key and return-to-origin behavior.
- `ShellState`: workspace selection, sidebar expansion, command surface,
  locale/format/timezone presentation preferences and notification affordance.
- `NavigationIntent`: origin route, target route, browser-history behavior,
  unsaved-change guard and restoration anchor.
- `SystemSurface`: stable reason code, safe user explanation, allowed action and
  retry/return target.
- `FocusContext`: parent block identity, inherited filters, local draft
  filters, interaction state and return location.
- `MotionPolicy`: named transition, duration range, reduced-motion behavior and
  forbidden effects.

Invariants:

- route identity is locale-neutral and workspace-aware;
- browser Back and Escape return from Focus to the originating block;
- shell, sidebar and topbar remain stable across route transitions;
- authorization is not implemented through client-side hiding;
- a route cannot silently fall back to another workspace;
- local Focus filters do not alter the parent report until explicit apply;
- reduced-motion removes translate, scale, bounce, shimmer and continuous chart
  animation while retaining concise status feedback.

## Use cases and contracts

| Command/query/event | Actor/caller | Contract owner | Errors/versioning |
|---|---|---|---|
| Resolve workspace route | Browser router | `packages/contracts` | unknown route, forbidden, workspace mismatch |
| Change shell preference | Authenticated user | Experience Platform API contract | optimistic concurrency, locale-neutral codes |
| Search commands/routes/help | Authenticated user | Experience Platform + documentation index | permission-filtered results |
| Enter/leave Focus | Reportable block | route registry + presentation contract | invalid origin, stale block, forbidden artifact |
| Guard dirty navigation | Draft-owning screen | shared navigation guard | stay, discard, save-and-continue |
| Resolve system surface | API/client error mapper | shared error contract | stable reason/action codes |
| Load Help context | Route or field Help action | visibility-aware Help index | missing/forbidden content fails closed |

Generated TypeScript clients and mocks are downstream artifacts of versioned
OpenAPI/JSON Schema examples. They do not become an independent contract.

## Data ownership

B01 owns only browser-facing preferences and route/navigation metadata assigned
to it by the control-plane schema. It does not own domain datasets, analytical
results, report snapshots, customer data or artifact payloads.

- all workspace-scoped state carries `workspace_id`;
- user preferences carry actor identity and optimistic revision;
- route and localization IDs are locale-neutral;
- no raw PII is stored in route state, browser logs, Help queries or analytics;
- browser storage is not an authorization or durable execution source;
- server-side state migrations require backward-compatible defaults and a
  rollback path.

## Ports and adapters

| Port owner | Adapter | Trust/auth | Failure behavior |
|---|---|---|---|
| Experience Platform | generated API client | authenticated workspace actor | stable forbidden/degraded/expired state |
| Experience Platform | contract-generated mock adapter | development only | explicit mock banner and parity checks |
| Documentation Platform | local MkDocs/index adapter | visibility-aware server contract | fail closed on invalid metadata |
| Presentation | ChartSpec Web adapter | validated bounded input | reject unsupported/unsafe spec |
| Browser shell | route registry adapter | permission/capability projection | no hidden fallback route |
| Browser shell | localization adapter | complete en/ru catalogs | English fallback without localizing IDs |

No adapter may make arbitrary Internet requests. Remote fonts, CDN assets and
runtime-loaded scripts are outside the accepted local/offline boundary.

## UI and documentation

Owned surfaces include:

- sign-in and first-run shell integration points;
- workspace shell, icon-and-label expanded sidebar, icon-only collapsed
  sidebar and stable topbar;
- route-backed page header, compact period/comparison/filter context and
  shared actions;
- system surfaces for forbidden, missing, session expiry, maintenance and
  upgrade requirement;
- Focus / Explore routes, drawers, dialogs, menus, tabs and navigation guards;
- keyboard-shortcuts and contextual Help surfaces;
- local `/docs` and permission-aware `/help`;
- responsive desktop/tablet behavior and density rules.

Acceptance requires English/Russian parity, keyboard and screen-reader paths,
WCAG 2.2 AA checks, reduced motion, visible focus, safe text scaling, stable
layout, and real-browser console/network inspection.

## Operations

- route resolution, client contract mismatch, Help resolution and system-state
  counts are observable with locale-neutral codes;
- logs exclude tokens, query values, raw PII and browser storage;
- client failures expose trace/request IDs safe for support;
- static assets are bundled and content-addressed;
- browser performance budgets distinguish first load from retained-data refresh;
- rollback preserves the previous compatible route/client bundle.

## Fixtures and acceptance

- deterministic route registry fixtures for allowed, forbidden, missing and
  workspace-mismatch cases;
- en/ru localization parity and missing-key negatives;
- responsive and density fixtures;
- reduced-motion and keyboard-only journeys;
- contract-generated mock versus real-client schema parity;
- browser flows for shell persistence, sidebar collapse, Back/Escape,
  unsaved-change guards, `/docs`, `/help` and system surfaces;
- accessibility smoke plus manual checks for the core journeys;
- no acceptance claim from Penpot or screenshots alone.

The B01 plan maps these outcomes through S00–S06 and identifies the exact
browser, contract and documentation evidence required at each exit.

## Contract impact

Initial B01 contracts are additive and therefore `compatible-change` while no
stable product consumer exists. Once route IDs, error codes, preference schema,
Help mappings or navigation semantics are published, changes require an
explicit compatibility and migration assessment.

## Open decisions and blockers

- Penpot access, canonical file ID and design-file authority are intentionally
  deferred to a separate user discussion and are not an activation blocker for
  source-backed S00 discovery.
- The runtime font bundle must be selected and hashed before B01 S01 can freeze
  rendering contracts.
- Product-policy values for `OPEN-007` and `OPEN-008` are owned by B05 and B06,
  not B01.
