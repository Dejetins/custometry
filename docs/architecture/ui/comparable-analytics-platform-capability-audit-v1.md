---
doc_id: ARCH-UI-CAPABILITY-AUDIT-001
title: Comparable analytics platform capability audit
doc_version: 2
product_spec_version: 0.10.0-draft
ui_spec_version: 0.8.0-draft
visibility: internal
ship: false
owner: product-architecture
requirement_ids: [GOAL-014, GOAL-015, GOAL-016, GOAL-017, GOAL-018, ANALYTICAL-DOC-001, BLOCK-BUILDER-001, COLLAB-001, SEGMENT-001, PRODUCT-ANALYTICS-001, WATCH-001]
status: accepted_research_evidence
proof_boundary:
  label: official-documentation-pattern-audit
  exclusions: [feature-parity, visual-authority, implementation-readiness, runtime-performance, browser-acceptance, causal-validity]
---

# Comparable analytics platform capability audit

> Current-use boundary: this accepted research is supporting pattern evidence.
> Current UI work uses accepted requirements, applicable architecture and
> visual sources, and ordinary scoped implementation proof. Forecast-related
> capabilities remain target requirements under the owner's hold; this research
> does not authorize forecasting work or select an external release scenario.

## Purpose and method

This audit records product and interface patterns that should inform the next
Custometry implementation. It uses official vendor documentation as evidence that a
pattern is established and useful; it does not treat another product's feature
list, navigation, composition, or visual language as target authority.

The review focuses on the owner's accepted problem: one governed retail
analytics platform must support broad analytical documents, repeatable
authoring, comments and findings, reusable time-aware segments, offline and
digital journeys, unit economics, product/category/inventory analysis, and
administrative adoption and performance controls.

The final interactive target pilot now owns demonstrated composition,
interaction, and visual language. This audit preserves capability requirements
and comparative rationale, not a separate visual authority. Ordinary
implementation tickets resolve missing screens, routes, and responsive states.

## Pattern audit and Custometry response

| Established pattern | Official evidence | Accepted Custometry response | Deliberate non-copy |
|---|---|---|---|
| Multi-page analytical workbooks with mixed blocks | [Sigma workbooks](https://help.sigmacomputing.com/docs/workbooks-overview) organize tables, pivots, charts, controls, text, layouts, and tabbed containers across one or more pages; [Power BI report projects](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report) persist page metadata, order, and active-page state; [Tableau stories](https://help.tableau.com/current/pro/desktop/en-us/stories.htm) arrange sequenced analytical points | define one versioned `AnalyticalDocument` composition for dashboard, workbook/report, and research profiles, with ordered tabs/pages, nested layout, blocks, page limits expressed as tested capacity rather than an artificial small cap, and immutable published snapshots | no Sigma, Power BI, Tableau, or spreadsheet clone; no promise of literal infinity; no fixed KPI-chart-table layout |
| Reusable saved analytical state | [Power BI bookmarks](https://learn.microsoft.com/en-us/power-bi/explore-reports/end-user-bookmarks) preserve report page and analytical state and distinguish report and personal bookmarks | provide versioned personal and shared Custom Views with explicit owner, visibility, document-version compatibility, filters, parameters, sort, drill, page, and selected-segment bindings | no silent mutation of a published view and no ambiguous "latest" state |
| Narrative guidance, provenance, and trust beside results | [Tableau Data Guide](https://help.tableau.com/current/pro/desktop/en-us/data_guide.htm) places explanations and data details near a dashboard; Tableau stories add an intentional analytical sequence | keep Result Trust continuously available and separate author notes, annotations, discussions, and promoted findings; bind every claim to exact document, result, block, and filter context | narrative text cannot certify a metric, hide stale data, or become causal evidence |
| Contextual collaboration around analytical assets | [Power BI comments](https://learn.microsoft.com/en-us/power-bi/explore-reports/end-user-comment) support report and visual comments with current report context; [Tableau site settings](https://help.tableau.com/current/server/en-us/sites_add.htm) expose comments, mentions, sharing, and alert controls | support exact-anchor comments, replies, mentions, resolution, follows, requester/executor roles, one boolean like per document version, and permission-aware activity | no ratings, dislikes, employee leaderboards, or popularity-only discovery |
| Reusable cohorts with visible dependencies and time movement | [Amplitude cohorts](https://amplitude.com/docs/analytics/create-cohorts) define reusable behavioral populations; its cohort dependency view exposes where cohorts are used, while interval cohorts show membership over time | separate `SegmentDefinition`, scheduled/manual `SegmentRun`, immutable `SegmentSnapshot`, membership, overlap/movement, trend, and `Used By`; bind analyses to explicit evaluation window and snapshot policy | no hidden recalculation under the same identity and no mutable membership treated as historical truth |
| Governed funnels, paths, and product-behavior views | [Amplitude Analytics](https://amplitude.com/docs/analytics) combines funnels, retention, journeys, cohorts, dashboards, and notebooks; [Journeys](https://amplitude.com/docs/analytics/charts/journeys/journeys-understand-paths) examines behavior before and after selected events; its [funnel semantics](https://amplitude.com/docs/analytics/charts/funnel-analysis/funnel-analysis-how-amplitude-computes) make ordering and conversion rules explicit | add canonical retail journeys across acquisition, web/app behavior, store and e-commerce sale, return, and retention; make sequence, window, denominator, identity coverage, attribution, and sampling semantics inspectable | no opaque provider funnel and no attribution-to-causation leap |
| Shared analytical workspaces for digital product behavior | [Amplitude product analytics](https://amplitude.com/docs/analytics/product-analytics) supplies common overview, onboarding, feature-engagement, and retention workflows with reusable filters and segmentation | provide curated digital-acquisition, journey, funnel, retention, unit-economics, and identity-quality views using the same metrics, segments, trust, documents, and builder as retail analysis | digital product behavior does not replace retail product/category/assortment/inventory analytics; those remain distinct semantic families |
| Administrative content adoption and system-performance insight | [Power BI usage metrics](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-usage-metrics) report views, viewers, and page activity; [Looker System Activity](https://cloud.google.com/looker/docs/system-activity-dashboards) exposes content usage, query history, and instance/database performance; [Sigma usage](https://help.sigmacomputing.com/docs/usage-overview) exposes adoption and query/resource patterns | separate Adoption from Analytical Performance: administrators can see meaningful/unique/repeat use, active users, comments, likes, subscriptions, unused/stale content, freshness, queueing, cache/materialization hit, avoided work, and resource pressure under privacy thresholds | no individual productivity score and no raw surveillance feed presented as adoption quality |
| Precomputation and aggregate-aware reuse | [Looker aggregate awareness](https://cloud.google.com/looker/docs/aggregate_awareness) selects compatible aggregate tables; [Looker caching and datagroups](https://cloud.google.com/looker/docs/caching-and-datagroups) tie reuse to source-change policies; [Sigma materializations](https://help.sigmacomputing.com/docs/manage-materializations) expose materialization state | reuse only exact-compatible content-addressed immutable Parquet artifacts; coordinate single-flight work, partition invalidation, last-good fallback, after-ingestion/off-peak refresh, and separate interactive/precompute/maintenance lanes | no TTL-only cache as correctness authority and no reuse across incompatible policy, metric, grain, tenant, access, or backend identity |
| Guided self-service authoring | Sigma's workbook element model and Power BI's multi-page reports show that broad authoring works best when pages and analytical elements share one composition model | use one step-based builder for table, pivot, chart, KPI, text, control, image, and approved custom block: subject/metric, grain/dimensions, filters/segments, visualization, trust preflight, placement, preview, and publish | no arbitrary code execution, ungoverned SQL, or bypass around certified metrics and access policy |

## Accepted capability package

The cross-product audit supports the following product package; each item is
already represented in the synchronized normative blueprints.

1. **One analytical-document kernel.** Dashboards, workbook-like reports, and
   research use the same versioned composition, publication, snapshots,
   comments, trust, export, watch, and adoption model, while retaining distinct
   lifecycle profiles where their business meaning differs.
2. **Wide but governed composition.** The target capacity is at least 100 pages
   and 30 blocks per page under the defined authoring, rendering, export, and
   navigation benchmark. Tabs, grouped pages, page search, outline navigation,
   deep links, and keyboard access prevent a large document from becoming one
   endless vertical canvas.
3. **A universal authoring path.** Analysts use a stable, predictable sequence
   for tables, pivots, charts, KPIs, and narrative blocks. Certification,
   authorization, freshness, grain, segment bindings, and cost estimates are
   checked before publication.
4. **Collaboration without employee scoring.** Requester/executor roles,
   comments, replies, mentions, exact anchors, annotations, findings, follows,
   views, and likes support work around an analytical product. Ratings,
   leaderboards, and popularity-only discovery are explicitly excluded.
5. **Time-aware reusable segments.** Definitions, runs, snapshots, membership,
   schedules, comparisons, movement, trends, and dependencies are visible and
   reusable across analytical documents, campaigns, watches, and forecasts.
6. **Complete retail measurement foundation.** Sales, returns, customers,
   stores, channels, promotions, forecasts, digital acquisition, web/app
   journeys, costs, unit economics, products, hierarchy, assortment,
   availability, inventory, price, and category analysis share governed
   dimensions and reconciliation contracts.
7. **Reuse-first performance and honest operations.** Materializations, exact
   compatibility, single-flight execution, prewarming, off-peak scheduling,
   admission control, and separate resource lanes prevent repeated work.
   Administrative screens expose both adoption and analytical performance.

## Explicitly rejected scope

- feature parity with any audited product;
- copying vendor navigation, component styling, workbook layout, or pricing
  tiers;
- ratings, dislikes, employee ranking, and popularity as a quality signal;
- arbitrary notebooks, user code, or ungoverned SQL in the product surface;
- probabilistic identity, algorithmic attribution, causal incrementality, and
  advertising activation without separate evidence and owner authority;
- mobile-specific information architecture without explicit authorization;
- claims that requirements, static gates, or an HTML pilot prove runtime,
  browser, accessibility, export, recovery, or performance readiness.

## Implementation handoff

Use the normative machine/human and UI blueprints, the preserved target pilot,
ADR-0005, ADR-0006, ADR-0007, and the relevant capability rationale here when
scoping ordinary implementation tickets. The table above does not authorize
arbitrary route names, a new frontend stack, or a direct copy of a comparable
platform. No G-program or exhaustive design-evidence layer is required.
