---
artifact_kind: delivery_spec
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
status: accepted
---

# Custometry Linear-workspace UI transition specification

## Problem and outcome

Custometry needs an authenticated Web application with measurable Linear-like
visual and behavioral fidelity while retaining Custometry routes, B2C retail
semantics, permissions, analytical contracts, branding, ECharts boundary,
REST/SSE APIs, and all backend delivery plans.

The accepted W27 responsive HTML candidate proves the first Sales visual and
interaction direction. The remaining transition must turn that candidate into
one reusable repository-owned UI foundation without copying screen markup or
introducing a second design source.

## Accepted decisions

- Only the Web UI is replatformed. FastAPI, PostgreSQL, Valkey, workers,
  artifacts, REST/SSE, domain boundaries, and W11-W17 remain unchanged.
- The frontend baseline is React + TypeScript + Vite + MobX + TanStack Query +
  styled-components + semantic CSS tokens.
- The four shipped base themes are exactly `abyss`, `graphite`, `frost`, and
  `paper`. `graphite` is the UI default; `paper` is the static render default.
- Inter Variable is self-hosted and versioned. Custometry brand assets and
  white-label overrides remain project-owned.
- Historical design inventories and earlier editor artifacts are truthful
  evidence only. They are not current generation or implementation inputs.
- W27's accepted responsive HTML candidate is the sole visual source for the
  first reusable `UI-AN-003` foundation slice.
- Current UI delivery is code-first and slice-first: product contracts → typed
  components and manifests → responsive browser candidate → browser validation
  → explicit product-owner acceptance → production integration.
- Reusable decisions are promoted into `packages/ui-foundation`, stable code
  identities, versioned component/icon/token registries, screen manifests, and
  a browser-rendered catalog.
- Catalog, review screens, and product routes render the same component
  implementation. Screenshots remain evidence rather than downstream source.
- The first runtime golden slice is Sales Analytics with route-backed
  Focus/Explore. It must exercise filters, period and `vs LY`, compact metric
  groups, chart/table switching, detail surfaces, Result Trust, keyboard,
  history, four themes, and real API projections.
- Migration is route-bounded and reversible. The existing shell remains a
  fallback until browser and performance evidence accepts the replacement.
- Product-owner decisions place Search and Notifications in the sidebar utility
  area, Help and the user menu in its footer, retain Products as a dedicated
  Analytics route, require expanded/collapsed/hidden/resizable sidebar states,
  and combine dataset/version with trust/freshness in one result-level trigger.

## Current authority and supersession

Authoritative inputs are:

- `custometry-technical-blueprint-ru.md` and its human mirror;
- `custometry-ui-blueprint-ru.md`;
- executable route and surface registries;
- accepted W03-W10 historical evidence;
- W27 accepted HTML/browser evidence;
- `docs/architecture/ui/custometry-contract-compiled-ui-prototyping-plan-v1.md`;
- existing API and backend delivery graph.

`W18-WEB-FOUNDATIONS-APPLICATION-SHELL` remains superseded. The blocked W28
external synchronization unit is also superseded by the accepted HTML-first
decision. Neither ticket is an active delivery dependency.

## Compatibility

| Surface | Classification | Decision |
| --- | --- | --- |
| Backend/API/persistence | `none` | Existing plans and runtime contracts remain authoritative. |
| Frontend dependencies | `breaking-change` before first stable Web release | MobX and styled-components remain the accepted baseline. |
| Theme IDs | `breaking-change` before first stable consumer | Exactly four current IDs remain. |
| Routes and stable UI IDs | `none` | Identity is preserved. |
| Accepted Sales browser behavior | `compatible-change` | Componentized rebuild must preserve the W27 visual and interaction boundary. |
| UI component/render contracts | `breaking-change` before stable consumer | Repository code identities and DOM receipts replace legacy external identities. |
| Browser behavior | `breaking-change with fallback` | Route-level cutover and rollback protect migration. |
| Reports/charts | `compatible-change` | ChartSpec remains theme-neutral; the renderer supports the four accepted IDs. |

## Delivery graph

The executable graph is
`.codex/delivery/graphs/custometry-linear-workspace-ui-transition-v1.json`.
One ready ticket is one execution unit.

1. W19 completes reference, motion, geometry, keyboard, accessibility, and
   four-theme evidence.
2. W20 proves frontend architecture, state boundaries, reversible mount, typed
   REST/SSE adapters, and benchmark harness.
3. W21 records the historical contract-compiled UI process pilot.
4. W24-W27 produce and explicitly accept the responsive `UI-AN-003` HTML
   candidate.
5. W29 extracts the accepted tokens/components, establishes the registry and
   catalog, rebuilds Sales Overview, proves browser equivalence, and renders
   Focus/Explore as a second reuse composition.
6. W22 consumes the accepted W29 code foundation to implement the production
   application shell behind the reversible route boundary.
7. W23 connects the real Sales Analytics Focus/Explore golden slice.

Later screens follow the same contract → component/manifest → browser candidate
→ browser QA → product acceptance sequence. The shared foundation grows only
through accepted vertical slices. W11-W17 may continue in parallel whenever
path ownership is disjoint.

## Proof boundary

The W29 boundary is repository components, schemas, manifests, catalog output,
DOM provenance, and real-browser evidence. Source tests do not prove responsive
layout, accessibility, visual equivalence, or performance. W22 and W23 require
their own browser and performance evidence on declared local hardware.

## Non-goals

- No backend, API, persistence, migration, or deployment change.
- No speculative all-route component library.
- No copied screen markup as a reuse strategy.
- No claim that HTML review proves production data, authorization, performance,
  recovery, release, or deployment readiness.
