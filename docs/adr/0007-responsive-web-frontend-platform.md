---
doc_id: ADR-0007
title: Responsive Web frontend platform and ownership boundaries
doc_version: 1
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [WEB-ARCH-001, WEB-ARCH-002, WEB-ARCH-003, WEB-ARCH-004, WEB-ARCH-005, WEB-ARCH-006]
status: accepted
proof_boundary:
  label: g0-frontend-platform-selection-and-boundary-design
  exclusions: [frontend-implementation, browser-acceptance, accessibility-conformance, measured-performance, runtime-readiness, release-readiness]
---

# ADR-0007: Responsive Web frontend platform and ownership boundaries

- status: `accepted`;
- date: `2026-08-06`;
- decision owner: product-owner delegation in `CUSTOMETRY-UI-DESIGN-PROGRAM-V2` G0;
- supersedes/superseded by: resolves the target-stack decision deferred by ADR-0004; no successor.

## Context

The V2 UI-program brief authorizes G0 to establish the target Web platform,
frontend dependency direction, design-system ownership, route/permission/
localization/state/data ownership, responsive anchors, visual inheritance,
rollout boundary, and proof obligations. The complete product scope is a
self-hosted B2C retail analytics and forecasting platform with governed data,
analytical documents, collaboration, segmentation, digital measurement,
product and inventory analytics, operations, and administration.

The accepted RU/EN HTML pilot is a hash-pinned visual-language and analytical-
density anchor only. It does not select frontend technology or exact screen
composition. The current `apps/web` stack and `packages/ui-foundation` are
implementation evidence, not automatic target authority. This decision selects
their useful, version-pinned seams deliberately after comparing them with the
accepted product and platform-baseline requirements.

## Decision criteria

1. Preserve technology-neutral backend and domain contracts, workspace
   isolation, permission rechecks, and safe URL/history semantics.
2. Keep server-authoritative state separate from reversible browser
   presentation state and drafts.
3. Support a product-owned, versioned semantic token and component system with
   no arbitrary customer CSS, HTML, JavaScript, remote font, or runtime style
   injection.
4. Support RU/EN and pseudo-locale stress, keyboard operation, visible focus,
   reduced motion, responsive Web, large analytical documents, and truthful
   Result Trust.
5. Permit a recoverable, wave-based migration without deleting the current
   fallback before real browser and API evidence exists.

## Options

| Option | Benefits | Costs and risks | Fit |
|---|---|---|---|
| Keep the frontend target technology-neutral through G6 | defers commitment | blocks reproducible component, adapter, build, testing, and implementation handoff contracts | rejected |
| Adopt the current stack implicitly | lowest document churn | violates `WEB-ARCH-001` and silently treats implementation evidence as authority | rejected |
| Select the current compatible seams explicitly, narrow their ownership, and preserve a compatibility boundary | reuses pinned repository capabilities while making authority, dependency direction, rollback, and proof explicit | requires removal or isolation of code that violates the new boundaries | accepted |

## Decision

### Platform and version ownership

The target responsive-Web client uses the repository lockfile as the version
source and pins this initial platform identity:

- React `19.1.0` and React DOM `19.1.0` for view composition;
- TypeScript `5.8.3` for browser and shared presentation contracts;
- Vite `6.3.5` plus `@vitejs/plugin-react` `4.5.2` for the reproducible build;
- React Router DOM `7.6.2` for route composition over product-owned route
  identity and history contracts;
- TanStack React Query `5.81.5` as the sole generic server-state cache,
  invalidation, refetch, and request-lifecycle owner;
- MobX `6.13.7` and `mobx-react-lite` `4.1.0` only for explicitly scoped
  presentation state or resumable draft coordination that is not duplicated in
  the query cache; local component state remains the default for local UI state;
- styled-components `6.1.19` as the component styling adapter behind
  product-owned semantic tokens and components;
- i18next `25.2.1`, react-i18next `15.5.3`, and the product localization package
  for presentation lookup and locale-aware browser formatting;
- Lucide React `0.515.0` as the pinned general icon adapter, with the accepted
  baseline able to require exact product-owned assets for icons not covered by
  the library;
- Playwright `1.52.0`, Vitest `3.2.4`, and Testing Library for browser,
  component, and contract proof. Their presence does not itself prove a gate.

Changing a pinned major version, server-state owner, routing identity model,
styling adapter, icon source, or build tool requires a compatibility review and
an accepted replacement decision. Patch/minor updates still follow the
repository dependency and evidence gates.

### Dependency direction and module ownership

The target dependency direction is:

```text
apps/web composition root
    -> route/shell/screen composition
        -> presentation use cases and local draft state
            -> typed inbound browser ports
                -> API/SSE/generated-client adapters
                    -> existing application/API contracts

packages/ui-foundation
    -> semantic tokens, themes, icons/assets adapters, primitives,
       shared components, interaction and accessibility contracts

packages/contracts + packages/localization
    -> route/API/event identities and locale-neutral messages/catalog contracts
```

`apps/web` composes; it does not own domain calculations, permission truth,
terminal run/report/delivery state, persistence, reconciliation, or source data.
Presentation use cases may produce reversible optimistic feedback but must
reconcile to the typed server result. Domain/application packages do not import
React, router, query, MobX, styled-components, browser storage, or DOM APIs.

Typed browser ports own the stable client-facing command/query/event shapes.
Transport adapters own HTTP/SSE mechanics, authentication/session headers,
workspace context, cancellation, stable error mapping, backoff, and redaction.
The server repeats authorization before data fetch and side effects; role hints,
hidden controls, route guards, and `workspaceKey` never authorize an action.

TanStack Query owns server snapshots and invalidation. MobX or React state may
own focus origin, open panels, drafts, selection, reversible preview state, and
local preferences, but may not mirror the full query cache or manufacture a
persisted/terminal result. Browser storage is limited to allowlisted
presentation preferences and opaque safe return references; it excludes PII,
secrets, raw filters, authorization decisions, and authoritative results.

ChartSpec and analytical document DTOs remain product-owned renderer-neutral
contracts. Chart, table, canvas, document, and static-renderer implementations
are adapters. Backend CPU calculations and immutable artifacts remain
authoritative.

### Design system and visual authority

`packages/ui-foundation` owns the target semantic-token registry, theme
identity, component and interaction contracts, exact icon/asset adapters,
accessibility primitives, and responsive component behavior. `apps/web` may
compose these primitives and define screen-local layouts but may not fork token
semantics or introduce unversioned customer CSS/HTML/JavaScript.

The V2 platform baseline is the inheritance target. Its current `paper` visual
authority inherits only the accepted pilot scope: calm professional character,
compact analytical density, concise KPI/context chrome, visible Result Trust,
Focus/Explore character, and RU/EN content stress. Exact pilot composition,
fixed KPI-chart-table order, full IA, source code, private assets, and historical
Penpot decisions remain excluded.

### Route, localization, permission, state, and data ownership

- `packages/contracts/routes/ui-routes.json` owns stable route identity and URL;
- `ui-route-contracts.json` owns current executable route policy and guards;
- `ui-surface-contracts.json` owns current coverage evidence;
- the UI-program intake and later G1 atlas own complete target surface
  inventory without mutating the current manifests as a shortcut;
- `packages/localization` owns RU/EN catalogs and locale-neutral message keys;
- backend/application policy owns effective authorization and denial reasons;
- product bounded contexts own definitions, snapshots, results, lifecycles, and
  data meaning; the client receives typed projections;
- the browser owns only presentation, navigation, focus, draft, and reversible
  interaction state explicitly assigned above.

### Responsive Web boundary

The initial supported responsive-Web width range is `768..1920` CSS pixels.
Anchor viewports are `768x1024`, `1024x768`, `1440x900`, and `1920x1080`.
Breakpoints are content-driven; components prefer container queries. The
accepted baseline preserves navigation identity, reading order, primary
outcomes, permission boundaries, data meaning, keyboard access, Result Trust,
and safe recovery at every anchor. Bounded tables, timelines, and canvases may
scroll locally; whole-page horizontal scrolling is not the primary strategy.

Widths below `768` are outside the accepted G0 Web range. This does not create
mobile-specific information architecture, mobile application scope, or a
device-class product promise. Widths above `1920` use a maximum content-width
policy while the shell remains stable.

### Rollout and rollback

Implementation is wave-based behind route- or surface-level compatibility
seams. Each wave preserves accepted deep links, Back/Forward, refresh, focus
return, workspace isolation, permission failure, and current fallback behavior.
The old route implementation or adapter seam is removed only after that wave
has current browser, accessibility-smoke, real-API/fixture, responsive, and
measured-performance evidence required by the later handoff.

The migration does not dual-write domain state. A rollback selects the last
accepted browser composition and adapter set while preserving server contracts,
new immutable artifacts, audit, and published versions. A baseline or visual-
authority replacement restarts at G0 under UI-program change control.

## Consequences

- The current stack becomes target authority only through this decision, not
  because code already exists.
- `@custometry/ui-foundation` must evolve from a small current implementation
  into the versioned baseline adapter without treating its four historical
  theme IDs as accepted target themes. The G0 baseline selects only its declared
  current theme identity; other themes require source-backed baseline revision.
- Any current code that mixes query/server state with MobX presentation state,
  performs authorization in the browser, or bypasses typed adapters must be
  isolated or migrated before handoff.
- No production UI is implemented by this ADR or G0.

## Contract impact and migration

| Boundary | Classification | Required consequence |
|---|---|---|
| Browser build/runtime dependencies | compatible target selection before stable target consumer | pin lockfile identity; upgrades require normal dependency evidence |
| Route identity and URLs | no change | preserve existing IDs and canonical URLs; later additions are versioned |
| API, DTO, event, domain, and persistence | none for G0 | implementation tickets classify each later change independently |
| Client state ownership | breaking for any code that duplicates server truth | migrate per wave; keep compatibility adapters until proof closes |
| Design tokens/components/themes | breaking target authority reset | bind to V2 baseline; historical theme IDs are not accepted automatically |
| Permission behavior | compatible with stricter boundary | browser hints remain non-authoritative; server denial wins |
| Responsive range | new compatible target contract | prove all anchors later; no mobile-specific IA |
| Rollback | additive recovery contract | preserve previous browser composition and typed server seams per wave |

## Verification obligations

- lockfile and license/SBOM evidence for the selected dependencies, fonts,
  icons, and assets;
- static dependency checks proving domain/application packages do not import
  browser/framework infrastructure;
- route/history/workspace and generated-client contract checks;
- query-cache versus presentation-state ownership tests;
- real browser proof for keyboard/focus, RU/EN/pseudo-locale, zoom/reflow,
  reduced motion, anchor viewports, error/denial/recovery, and large documents;
- real API or isolated contract fixtures for authorization, cancellation,
  invalidation, SSE/event state, and terminal-state reconciliation;
- measured client/network/API/render and cold/warm/cache performance evidence
  on declared hardware before implementation handoff.

G0 static and schema validation proves only that these ownership and rollout
boundaries are explicit and internally consistent. It does not prove browser
behavior, WCAG conformance, API enforcement, performance, runtime, security
hardening, release, or production readiness.

## Re-evaluation triggers

- accepted G3 foundations or G4 family work demonstrates that the selected
  component/styling or state boundary cannot satisfy the baseline;
- measured large-document or chart behavior requires a new renderer boundary;
- a stable API/generated-client contract makes the current adapter shape
  incompatible;
- mobile-specific IA or application scope is explicitly authorized;
- a baseline, visual authority, or supported Web range is replaced.
