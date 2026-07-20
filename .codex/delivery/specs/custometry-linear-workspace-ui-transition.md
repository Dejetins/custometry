---
artifact_kind: delivery_spec
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
status: accepted
---

# Custometry Linear-workspace UI transition specification

## Problem and outcome

Custometry has an accepted and extensive Penpot `0.6.3` baseline, executable
route contracts, and a provisional React foundation ticket, but those artifacts
precede the decision to adopt the shared Linear-workspace frontend baseline.
Executing the old foundation ticket would encode a single-theme Frost shell and
would make the later replatform more expensive.

The target is an authenticated Custometry application with maximum measurable
Linear-like visual and behavioral fidelity while retaining Custometry routes,
B2C retail semantics, permissions, analytical contracts, branding, ECharts
boundary, REST/SSE APIs, and all backend delivery plans.

## Accepted decisions

- Only the Web UI is replatformed. FastAPI, PostgreSQL, Valkey, workers,
  artifacts, REST/SSE, domain boundaries, and W11-W17 remain unchanged.
- The frontend baseline is React + TypeScript + Vite + MobX + TanStack Query +
  styled-components + CSS semantic tokens.
- The four shipped base themes are exactly `abyss`, `graphite`, `frost`, and
  `paper`. `graphite` is the UI default; `paper` is the static render default.
- Inter Variable is self-hosted and versioned. Custometry brand assets and
  white-label overrides remain project-owned.
- The accepted W10 Penpot inventory is historical evidence and the route/surface
  identity baseline. It is not evidence of the new design or browser runtime.
- Penpot vNext reuses stable Custometry route IDs and product requirements but
  replaces foundations, shell, theme matrix, density, motion, and interaction
  grammar under an explicitly new accepted version.
- The first runtime golden slice is Sales Analytics with route-backed
  Focus/Explore. It must exercise filters, period and `vs LY`, compact metric
  groups, chart/table switching, detail surfaces, Result Trust, keyboard,
  history, four themes, and real API projections.
- Migration is route-bounded and reversible. The existing shell remains a
  fallback until browser and performance evidence accepts the replacement.

## Current authority and supersession

The following remain authoritative inputs:

- `custometry-technical-blueprint-ru.md` and its human mirror;
- `custometry-ui-blueprint-ru.md` for route inventory and domain UX after its
  `0.7.0` transition delta;
- executable route and surface registries;
- accepted W03-W10 evidence;
- existing API and backend delivery graph.

`W18-WEB-FOUNDATIONS-APPLICATION-SHELL` is superseded because its Frost-only
foundation and old design guard conflict with this accepted transition. Its
scope is replaced by the W19-W23 graph. Supersession does not claim that W18 was
implemented or accepted.

## Compatibility

| Surface | Classification | Decision |
|---|---|---|
| Backend/API/persistence | `none` | Existing plans and runtime contracts remain authoritative. |
| Frontend dependencies | `breaking-change` before first stable Web release | Add MobX and styled-components; local state ownership changes. |
| Theme IDs | `breaking-change` before first stable consumer | `slate` and `sand` are removed; no runtime migration is required because no stable report/theme consumer exists yet. |
| Routes and stable UI IDs | `compatible-change` | Identity is preserved; visual composition and shell change. |
| Penpot | `new accepted target required` | W10 remains evidence; vNext must be separately accepted. |
| Browser behavior | `breaking-change with fallback` | Route-level cutover and rollback protect migration. |
| Reports/charts | `compatible contract change` | ChartSpec remains theme-neutral; renderer allows the four accepted IDs. |

## Delivery graph

The executable graph is
`.codex/delivery/graphs/custometry-linear-workspace-ui-transition-v1.json`.
One ready ticket is one execution unit.

1. W19 completes missing reference, motion, geometry, keyboard, accessibility,
   and four-theme evidence without changing product code or Penpot.
2. W20 proves the frontend architecture, state boundaries, reversible mount,
   typed REST/SSE adapters, and benchmark harness.
3. W21 creates and accepts Penpot vNext foundations and representative states.
4. W22 implements the production application shell behind the reversible route
   boundary and collects browser/performance evidence.
5. W23 implements the real Sales Analytics Focus/Explore golden slice.

Later route-cluster tickets are created from measured W23 results rather than
prewriting speculative implementation instructions. W11-W17 may continue in
parallel whenever path ownership is disjoint.

## Reference and proof boundary

The shared standard and manifest are under `docs/architecture/ui/`. The current
archive is a sufficient dark-shell input, not complete acceptance evidence.
W19 must close or explicitly waive every `missing_required_evidence` item before
W20 or Penpot vNext starts.

Penpot acceptance cannot prove browser behavior. Source tests cannot prove
performance. W22 and W23 therefore require real-browser traces and measurements
on declared local hardware, separating client overhead, REST/SSE latency, and
render time.

## Non-goals

- No Node.js backend, GraphQL, Temporal, WebSocket sync framework, cloud
  platform, or public-site redesign.
- No change to Custometry domain scope, roles, data contracts, computation,
  analytics methodology, reports, email, XLSX, or chart semantics.
- No copying Linear branding, text, source code, proprietary assets, or product
  entities.
- No deletion of accepted evidence or silent mutation of historical Penpot
  claims.
