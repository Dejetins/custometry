---
doc_id: CUSTOMETRY-CONTRACT-COMPILED-UI-PROTOTYPING-PLAN-V1
title: Custometry HTML-first UI prototyping and reuse plan v1
doc_version: 2
product_spec_version: 0.9.4-draft
visibility: internal
ship: false
owner: architecture
requirement_ids:
  - WEB-ARCH-003
  - WEB-ARCH-005
  - WEB-ARCH-006
  - THEME-001
  - THEME-002
  - THEME-003
  - THEME-005
  - THEME-008
  - UI-SHELL-001
  - UI-SHELL-002
  - UI-SHELL-003
  - UI-SHELL-004
  - UI-SHELL-005
  - UI-SHELL-006
  - UI-DENSITY-001
  - UI-DENSITY-002
  - UI-DENSITY-003
  - UI-DENSITY-004
  - A11Y-001
  - A11Y-003
  - A11Y-008
status: accepted
proof_boundary:
  label: repository-owned-html-first-ui-foundation-and-browser-acceptance-process
  exclusions:
    - backend-runtime-readiness
    - production-data-integration
    - all-route-ui-coverage
    - release-readiness
---

# Custometry HTML-first UI prototyping and reuse plan v1

## Decision and authority

The product owner accepted this HTML-first direction on 2026-08-02. Current UI
design and implementation use repository-owned CSS tokens, typed React/HTML
components, machine-readable registries, screen manifests, and real-browser
evidence. An external visual editor is not a source of truth, acceptance gate,
or delivery dependency.

Historical external-editor artifacts remain immutable evidence of earlier
pilots. They are not published, synchronized, imported, or supplied to future
executors. The accepted `UI-AN-003` browser candidate from W27 is the sole
visual source for the first reusable code foundation.

Product capabilities, routes, permissions, data meaning, actions, and required
states remain owned by the normative product blueprints and executable route
and surface contracts. This decision changes UI delivery mechanics only.

## Outcome

The product owner reviews responsive browser output. Codex and frontend
engineers build new candidates only from versioned repository-owned components
and declared screen manifests. The same components power the catalog, review
screens, and later production routes, eliminating a translation step between
accepted design and implementation.

The first proof succeeds when:

- accepted W27 visual decisions are represented by semantic tokens and reusable
  typed components;
- the Sales Overview candidate is rebuilt from registered components without
  copying the original screen markup;
- DOM provenance, accessibility structure, geometry, themes, locales, and
  screenshots pass the declared browser gates;
- Focus/Explore is rendered as a second composition from the same registry,
  proving reuse rather than one-screen reconstruction.

## Source-of-truth ownership

| Decision surface | Authoritative owner | Consumer |
| --- | --- | --- |
| Product semantics, routes, permissions, actions, required states | Normative blueprints and route/surface contracts | Screen contracts and tests |
| Accepted visual direction for the first slice | W27 HTML candidate and browser evidence | Token/component extraction only |
| Colors, typography, spacing, radii, focus, status, chart roles | Versioned semantic CSS token contract | Components, catalog, screens, production UI |
| Component anatomy, props, variants, states, slots, accessibility | Versioned component registry plus typed implementation | Catalog and screen renderer |
| Icons | Registered icon identity and implementation mapping | Components only |
| Screen composition | Versioned schema-valid screen manifest | Deterministic React/HTML renderer |
| Visible inventory | Browser-rendered component catalog | Product and engineering review |
| Candidate acceptance | Immutable browser receipt plus product decision | Exact accepted revision lookup |
| Runtime behavior and data | Production code plus browser/API evidence | Runtime acceptance only |

## Target architecture and dependency direction

```text
product and route contracts
        ↓
accepted visual decisions
        ↓
semantic CSS tokens
        ↓
typed reusable components + stable component IDs
        ↓
component registry + screen manifest schemas
        ↓
component catalog and product screen renderer
        ↓
DOM audit + accessibility checks + browser screenshots
        ↓
product-owner acceptance receipt
        ↓
production integration with real adapters and data
```

Dependency rules:

- tokens depend on no component or screen;
- reusable components depend on tokens and stable icon mappings only;
- screen compositions depend on registered components, never on catalog pages;
- the catalog imports production components and fixtures; production code never
  imports catalog fixtures;
- manifests contain component IDs, props, slots, actions, state, locale, theme,
  and viewport, but no arbitrary markup or raw visual values;
- the renderer rejects unknown components, props, variants, actions, tokens,
  or raw unregistered visible markup;
- accepted screenshots are evidence, not reusable source input.

## Stable component identity and provenance

Every rendered component has a stable registry ID, semantic version, and DOM
provenance. The browser output exposes normalized metadata such as:

```html
<section
  data-ui-component="analytics.trend-panel"
  data-ui-variant="comparison"
  data-ui-revision="v1"
>
  ...
</section>
```

The registry declares allowed props, variants, states, slots, actions,
accessibility names, required tokens, implementation symbol, maturity, and
content constraints. A content hash or version replaces editor-generated
component keys. A rendered screen receipt records the registry, token,
manifest, renderer, locale, theme, viewport, and source revision.

## Component catalog

The repository-owned catalog is interactive browser documentation, not a
parallel implementation. It renders the same components used by screens and
must cover:

- semantic colors, typography, spacing, radii, elevation, focus, status, and
  chart roles;
- primitives and controls;
- shell and navigation patterns;
- analytical KPI, chart/data, breakdown, Context, Result Trust, and
  Focus/Explore patterns;
- default, hover, focus, pressed, selected, disabled, loading, empty, failed,
  stale, and reduced-motion states when applicable;
- `abyss|graphite|frost|paper`, `en|ru`, supported viewports, long-copy stress,
  and keyboard traversal.

Pseudo-states that cannot be captured reliably by pointer timing have explicit
catalog controls or deterministic test modes. Catalog-only controls and
fixtures are forbidden from production bundles.

## Screen manifests

A screen manifest identifies:

- surface and route identity;
- product state, role/persona, locale, theme, and viewport;
- exact token, component-registry, icon-registry, and renderer versions;
- ordered registered component instances;
- allowed props, slots, actions, bindings, and responsive state;
- required accessibility names and focus/return behavior;
- forbidden capabilities and deferred side effects.

The manifest cannot contain arbitrary visible HTML, raw colors, raw
typography, unregistered icons, unknown actions, or copied markup from an
accepted screen. Structural wrappers are limited to a small renderer-owned
allowlist.

## Eight-point transition

### 1. Stop the external-editor acceptance path

The previous synchronization unit is superseded. No acceptance, publication,
cross-file enablement, or further mutation is required. Exit: no active ticket,
graph edge, standard, blueprint, or agent route depends on an external editor.

### 2. Retain earlier artifacts only as history

Previously created unpublished assets and read-back evidence remain intact.
They are excluded from current source loading, generation, acceptance, and
implementation. Exit: history stays truthful without controlling new work.

### 3. Freeze the accepted HTML source

W27's exact browser candidate, state inventory, screenshots, and product-owner
decision are the sole visual source for `UI-AN-003`. Exit: one immutable source
revision and receipt are named; no later executor interprets older frames.

### 4. Extract tokens and reusable components

Reconcile the accepted candidate with `packages/ui-foundation`, then extract
semantic tokens and at least four real reusable component families. The first
slice must include enough structure to rebuild the accepted Sales Overview
without copied screen markup, including shell/navigation, analytical content,
Result Trust, and Focus/Explore seams. Exit: catalog states and focused tests
exist for every extracted family.

### 5. Establish registry and manifest schemas

Version component, icon, token, screen-manifest, and render-receipt contracts.
Replace legacy external identities with repository code identities, stable IDs,
versions, and digests. Negative tests reject raw markup, raw visual values,
unknown components/props/variants/actions, missing regions, invalid a11y names,
and version drift. Exit: the registry and one Sales manifest compile
deterministically.

### 6. Rebuild Sales Overview from registered components

Render the accepted Chart/Data, Result Trust, Sidebar, breakdown, responsive,
and interaction states from the new foundation. The original prototype remains
the visual reference but is not copied into the renderer. Exit: normalized DOM
provenance contains registered components only.

### 7. Prove structural and visual equivalence in the browser

Compare the rebuilt screen with W27 at `1440×900` and `1024×768`; exercise all
required states, four themes, Russian long copy, keyboard/focus, reduced motion,
console/network hygiene, clipping/overflow, and screenshot diff. Exit: one
durable machine receipt and product acceptance boundary with explicit runtime
exclusions.

### 8. Prove reuse with a second composition

Render the already accepted Sales Focus/Explore composition from the same
tokens, components, registry, and renderer. It introduces no new product
decision and uses synthetic review fixtures only. Exit: a second manifest and
browser receipt prove reuse without duplicated component markup.

## Acceptance and failure behavior

- Machine conformance, product decision, and implementation readiness are
  separate dimensions.
- Unknown registry references fail closed before rendering.
- Browser failures produce exact findings; they never degrade into screenshot
  approval alone.
- Repair is bounded by the executing ready ticket and reruns every invalidated
  check.
- A failed candidate does not mutate the accepted W27 reference.
- Product acceptance of the rebuilt candidate does not imply real API,
  authorization, persistence, chart-engine, accessibility-complete,
  performance, release, or deployment readiness.

## Compatibility classification

| Boundary | Classification | Consequence |
| --- | --- | --- |
| Backend, API, DTO, persistence, cache, service calls | `none` | No runtime or data contract changes |
| Route and product semantics | `none` | Existing identities and requirements remain authoritative |
| Accepted `UI-AN-003` browser behavior | `compatible-change` | Rebuild must remain visually and behaviorally equivalent at the declared review boundary |
| UI delivery and design-tool process | `breaking-change` before stable UI release | External-editor synchronization is removed from the active lifecycle |
| UI component and render contracts | `breaking-change` before stable consumer | Legacy external identities are replaced by code identities and versioned DOM receipts |
| W22 input boundary | `breaking-change` for the draft ticket | W22 consumes the accepted HTML-first foundation rather than editor indexes or maps |
| Historical evidence | `compatible-change` | Evidence is retained and excluded from active execution |

## Alternatives rejected

### Maintain two synchronized sources

Rejected because the accepted browser candidate and external composition would
duplicate ownership, add drift, and still require browser proof.

### Copy prototype markup into each new route

Rejected because it hides component identity, prevents governed reuse, and
makes visual consistency untestable.

### Build the complete all-route design system first

Rejected as speculative. The foundation grows only through accepted vertical
slices, beginning with Sales Overview and Focus/Explore.

## Rollout and rollback

The transition is additive and pre-release. Historical evidence is retained.
The W27 candidate remains the rollback visual reference until the componentized
rebuild passes browser equivalence. W22 cannot consume the new foundation until
the HTML-first foundation ticket is accepted. W23 remains behind W22 and the
real Sales API projection boundary.

## Proof boundary

The architecture decision is proven by documentation and contract validation
only. The implementation ticket must separately prove source correctness,
registry/schema conformance, real-browser DOM provenance, accessibility,
themes, locales, responsive geometry, visual equivalence, reuse, and residual
risk. No documentation-only gate proves the future browser implementation.
