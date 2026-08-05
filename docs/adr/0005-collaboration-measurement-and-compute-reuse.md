---
doc_id: ADR-0005
title: Collaboration, digital measurement, and content-addressed compute reuse
doc_version: 1
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [GOAL-014, GOAL-015, GOAL-016, DIGITAL-001, ATTRIBUTION-001, UNIT-ECON-001, ASSUMPTION-001, MATERIALIZE-001, COLLAB-001, WATCH-001]
status: accepted
proof_boundary:
  label: requirements-architecture-and-market-pattern-audit
  exclusions: [provider-connector-validation, persistence-migration, runtime-performance, browser-acceptance, causal-validity, production-readiness]
---

# ADR-0005: Collaboration, digital measurement, and content-addressed compute reuse

- status: `accepted`;
- date: `2026-08-05`;
- decision owner: `product owner`;
- requirement IDs: `GOAL-014`, `GOAL-015`, `GOAL-016`, `DIGITAL-001`,
  `ATTRIBUTION-001`, `UNIT-ECON-001`, `ASSUMPTION-001`, `MATERIALIZE-001`,
  `COLLAB-001`, `WATCH-001`;
- supersedes/superseded by: none.

## Context

Custometry already specifies immutable local Parquet landing/mart/result
artifacts, content hashes, node cache identity, incremental partitions, and
Polars/DuckDB execution. It does not yet provide an aggregate-aware reuse
planner, single-flight behavior, off-peak materialization policy, asset
adoption telemetry, social collaboration beyond comments, or canonical
web/app/marketing measurement joined to offline retail facts.

The product owner requires requester/executor collaboration, comments, views,
likes without ratings, administrator adoption statistics, maximal avoidance of
duplicate computation, and a foundation for web/app acquisition and unit
economics. This is a product-capability and target-architecture change; it does
not select a visual direction or start the UI design program.

## Comparable-product pattern audit

The audit uses official product documentation as pattern evidence, not feature
parity or proof that any pattern is implemented in Custometry.

| Product pattern | Comparable evidence | Custometry decision |
|---|---|---|
| Asset discussion and contextual collaboration | [Power BI comments](https://learn.microsoft.com/en-us/power-bi/explore-reports/end-user-comment) bind comments to reports/visuals and current filter context; [Tableau site settings](https://help.tableau.com/current/server/en-us/sites_add.htm) cover comments, mentions, shared content, and data-driven alerts | adopt exact-version/block comments, mentions, follows and safe context; add one boolean like; reject ratings/leaderboards |
| Adoption and content-usage analytics | [Power BI usage metrics](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-usage-metrics), [Tableau Admin Insights](https://help.tableau.com/current/online/en-us/adminview_insights.htm), [Looker System Activity](https://cloud.google.com/looker/docs/system-activity-dashboards), [Sigma Usage](https://help.sigmacomputing.com/docs/usage-overview), and [Metabase Usage Analytics](https://www.metabase.com/docs/latest/usage-and-performance-tools/usage-analytics) expose views, users, content activity, query/performance or resource patterns | adopt meaningful/unique/repeat views, comments, likes, subscriptions, freshness and trend with workspace scoping and suppressed installation aggregates |
| Scheduled refresh and precomputed extracts | [Tableau publishing](https://help.tableau.com/current/server/en-us/publish.htm) and [performance guidance](https://help.tableau.com/current/server/en-us/perf_guidelines.htm) distinguish extracts, schedules, cache and off-peak work | adopt after-ingestion/off-peak refresh with separate interactive/precompute/maintenance resource lanes |
| Aggregate-aware and reusable computation | [Looker aggregate awareness](https://cloud.google.com/looker/docs/aggregate_awareness) selects efficient aggregate tables; [Looker caching and datagroups](https://cloud.google.com/looker/docs/caching-and-datagroups) coordinate cache/PDT rebuild with source changes; [Sigma materializations](https://help.sigmacomputing.com/docs/manage-materializations) expose materialization state and last-good behavior; [Metabase caching](https://www.metabase.com/docs/latest/configuring-metabase/caching) supports scheduled/adaptive refresh | adopt exact-compatible artifact selection, content-addressed identity, single-flight, partition invalidation, explicit last-good semantics and measured avoided work |
| Governed user-entered assumptions | [Sigma input tables](https://help.sigmacomputing.com/docs/intro-to-input-tables) provide governed typed input without overwriting source systems | adopt versioned targets, budgets, cost allocations and scenarios; reject arbitrary source/advertising writeback |
| Content impact and scheduled observation | [Looker content validation](https://cloud.google.com/looker/docs/content-validation), [Looker alerts](https://cloud.google.com/looker/docs/creating-alerts), [Metabase subscriptions](https://www.metabase.com/docs/latest/dashboards/subscriptions), and [Superset alerts/reports](https://superset.apache.org/docs/configuration/alerts-reports/) show dependency checks and data-driven notification patterns | adopt metric watches with pinned specs, dedup/cooldown, access recheck and no activation |
| Product-event taxonomy and identity | [Amplitude Data](https://amplitude.com/docs/data/data-overview), its [tracking plans](https://amplitude.com/docs/data/create-tracking-plan), and [identity model](https://amplitude.com/docs/get-started/identify-users) show governed event definitions and anonymous-to-known identity handling | adopt versioned event taxonomy, deterministic identity linkage, anonymous coverage, late/restated events and consent/retention contracts |
| Retail web/app journey | [GA4 ecommerce events](https://support.google.com/analytics/answer/12200568?hl=en-EN) cover product/promotion/cart/checkout/purchase/refund behavior; [GA4 sessions](https://support.google.com/analytics/answer/9191807?hl=en-EN) retain campaign/referrer context | adopt a retail event pack and session policy, but keep source/provider semantics and sampling limitations explicit |
| Cross-channel identity and attribution | [Adobe Customer Journey Analytics stitching](https://experienceleague.adobe.com/en/docs/analytics-platform/using/stitching/overview) and [attribution models](https://experienceleague.adobe.com/en/docs/analytics-platform/using/cja-workspace/attribution/models) show person-level stitching and multiple credit-allocation models; [AppsFlyer in-app events](https://support.appsflyer.com/hc/en-us/articles/115005544169-In-app-events-Overview) and [cost aggregation](https://support.appsflyer.com/hc/en-us/articles/207040526-ROI360-cost-aggregation-overview) connect post-install behavior, spend, ROI/ROAS and acquisition metrics | adopt deterministic model comparison, spend/cost facts, CAC/CPI/CPA, ROAS/ROI, LTV/margin/payback with coverage/residuals; defer probabilistic/algorithmic attribution and keep attribution non-causal |

The selected differentiator is not a clone of a BI tool. It is a governed retail
operating loop: digital acquisition and product behavior join offline sales and
returns; metrics, costs and assumptions remain versioned; every reusable result
can become a reviewed analytical product, a collaboration object and a metric
watch, while shared immutable materializations prevent repeated work across
Web, email, XLSX and API consumers.

## Decision criteria

1. Avoid duplicate computation before optimizing individual kernels.
2. Preserve single-server, self-hosted, local-first and modular-monolith
   constraints through `v1_target`.
3. Keep collaboration useful without employee ranking or surveillance.
4. Make identity, attribution, cost and unit-economics assumptions explainable
   and reproducible.
5. Separate attribution from causal inference and notification from activation.
6. Add provider adapters only after canonical contracts and support matrices.

## Options

| Option | Benefits | Costs/risks | Fit |
|---|---|---|---|
| Extend current Analytics/Research tables and add a generic cache | fewer packages initially | couples social privacy, marketing identity and compute lifecycle; invalidation remains unsafe | rejected |
| Add separate microservices and object storage now | independent deployment/scale | violates the current single-server operational target and expands recovery/trust cost without evidence | rejected |
| Add two business contexts and a cross-context materialization capability inside the modular monolith | clear ownership, local operational fit, reusable artifacts, future adapter seams | adds contracts, migrations and proof obligations | accepted |

## Decision

1. Add `Collaboration & Adoption` as owner of participant bindings, comments,
   mentions, likes, subscriptions, meaningful views, activity feed, adoption
   aggregates and metric watches. A participant binding is not access. Ratings,
   dislikes, employee leaderboards and popularity-only ranking are prohibited.
2. Add `Digital Journey & Marketing Measurement` as owner of the canonical
   event/touch/spend/cost model, deterministic identity-link observations,
   attribution and unit-economics specs/results, governed assumptions,
   funnels and journey projections. Provider claims remain separate from
   independently observed facts; attribution is not causal evidence.
3. Keep materialization as a capability spanning existing contexts rather than
   a technology bounded context: Semantic Model owns logical compatibility,
   Execution Control owns definitions/planning/single-flight/invalidation and
   resource lanes, and Artifact Lifecycle owns committed Parquet artifacts,
   dependencies, authorization, retention and eviction.
4. Keep PostgreSQL as control-plane truth, local Parquet as durable bulk and
   materialization truth, and Valkey/process memory as bounded ephemeral
   coordination/cache only. Do not add a remote object store, new deployable
   service or cloud control plane through this decision.
5. Add deterministic first/last/linear/position/time-decay/same-touch
   attribution and governed CAC/CPI/CPA, ROAS/ROI, LTV, contribution-margin and
   payback contracts. Algorithmic attribution, probabilistic identity,
   campaign activation, causal incrementality and arbitrary external writeback
   remain out of scope until separate evidence and authority exist.

## Consequences

- Reused data is an immutable authorized artifact, not an opaque time-based
  cache entry. This costs more metadata and invalidation design but makes reuse
  explainable and safe across consumers.
- Collaboration telemetry needs minimization, retention, suppression and
  permission rechecks; it cannot be reconstructed by querying raw Audit.
- Provider integrations become adapters behind canonical contracts. Their
  sampling, attribution model, timezone, currency, retention and API limits
  must be declared individually.
- Unit economics can be compared and certified without claiming one universal
  definition. Cost ladders, cohort maturity, refunds and allocation residuals
  stay visible.
- Current UI inventory is incomplete for these capabilities. The future G1
  atlas must add their screen families; no routes or visual design are invented
  by this ADR.

## Contract impact and migration

Repository consumer search finds only current route/surface permission and
comment inventory plus the empty ChartSpec Foundation seam; there are no
Python domain implementations, migrations, generated API clients, persisted
materialization consumers or runtime provider adapters to migrate today.

| Contract dimension | Classification for this change | Required implementation consequence |
|---|---|---|
| Product/semantic requirements | `compatible-change` target addition | publish `0.10.0-draft`; preserve existing metric/report semantics |
| Public API behavior | `compatible-change` target addition; no runtime mutation now | add versioned endpoints/events only through implementing specs and generated clients |
| Port contracts | `compatible-change` additions plus `breaking-change` logical owner move for comments | introduce owner ports first; migrate comment callers from Research to Collaboration with a compatibility adapter if a consumer appears |
| DTO schemas | `unknown` until implementing specifications | inventory generated clients/serializers and classify required/enum/default changes before implementation |
| Persisted schemas | `compatible-change` additive target; no migration executed | new owner schemas/tables/indexes and explicit up/down/data migration proof are required |
| Configuration/defaults | `compatible-change` target addition | version privacy, freshness, lane, retention, attribution, currency and cost policies; fail closed when absent where specified |
| Request hash/cache/persistence identity | `breaking-change` target semantics for any unversioned cache | replace with policy/spec/input/version/backend-aware reuse identity; never dual-read unsafe legacy entries |
| Service auth/timeout/retry/error | `compatible-change` with stricter authorization rechecks | define stable forbidden/stale/blocked codes, bounded waits and single-flight/reconciliation semantics |
| External side effects | `compatible-change` notification addition; activation remains `none` | watches need idempotency/dedupe/cooldown/access recheck; no campaign/source writeback |
| Logs/metrics/audit/redaction | `compatible-change` additions | add minimized adoption/reuse/coverage telemetry and redacted lifecycle events without content/PII leakage |
| Alerts/runbooks | `compatible-change` target addition | add materialization freshness/waste/lane and watch-delivery triggers/runbooks before release |
| Benchmark/rollout gates | `compatible-change` but mandatory evidence expansion | cold/warm/hot/concurrent/invalidation/lanes and digital reconciliation become release evidence |
| Browser-visible behavior | `unknown` until `ui-design-program` | pre-G0 delta only; routes, frontend stack and visuals remain unresolved under ADR-0004 |

Rollback stops new publication and planner selection, preserves immutable
facts/results/discussions/audit, and never reactivates policy-incompatible cached
bytes. A later rollback after stable consumers requires schema, API, event and
generated-client compatibility evidence.

## Verification and proof boundary

Current proof is limited to official-document pattern research, synchronized
normative/human requirements, accepted ownership/dependency design, generated
requirement index, documentation links and static repository gates.

Implementation acceptance requires, at minimum:

- database/API/browser proof for comments, idempotent likes, view deduplication,
  feed filtering, revocation and administrator privacy scopes;
- concurrent same-key tests showing one execution, exact aggregate selection,
  partition invalidation, last-good behavior and lane isolation;
- representative cold/warm/hot/invalidation benchmarks with avoided work and
  resource consumption, not only latency;
- connector fixtures and reconciliations for event/touch/spend/cost grain,
  identity coverage, refunds, FX, attribution residuals and unit-economics
  metric certification;
- security/privacy/retention/recovery proof at PostgreSQL, Parquet, Valkey,
  worker and browser boundaries.

No runtime performance, provider correctness, causal validity or UI acceptance
is claimed by this ADR.

## Re-evaluation triggers

- one server cannot meet measured interactive SLOs after reuse and capacity
  controls, requiring a new multi-host/object-storage ADR;
- deterministic identity coverage is insufficient and probabilistic matching
  is proposed;
- algorithmic attribution, incrementality experiments or external activation
  enter product scope;
- adoption privacy regulation or customer policy requires a stricter default;
- the UI program G1 atlas changes the capability boundary rather than only its
  presentation.
