---
doc_id: ARCH-BOUNDED-CONTEXT-MAP-001
title: Custometry bounded context map
doc_version: 9
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [ARCH-PRINCIPLE-001, GOAL-014, GOAL-015, GOAL-016, UC-025, UC-026, UC-027, UC-028, UC-029, CONNECTOR-001, DIGITAL-001, ATTRIBUTION-001, UNIT-ECON-001, MATERIALIZE-001, COLLAB-001, WATCH-001, METHOD-001, METHOD-009, METRIC-009, METRIC-017, DISCOUNT-001, PVM-001, RBAC-002, RBAC-013, RBAC-019, RBAC-020, RBAC-027, REPORT-003, REPORT-012, OUTLIER-001, SEGMENT-001]
status: accepted
proof_boundary:
  label: target-ownership-dependency-and-integration-policy
  exclusions: [implemented-import-boundaries, persistence-migrations, runtime-integration-proof]
---

# Custometry Bounded Context Map

## Purpose and interpretation

This map establishes DDD ownership, permitted integration directions, public
ports, consistency rules, and trust handoffs for the `0.10.0-draft` modular
monolith. It elaborates the normative product blueprint without introducing new
product requirements. `system-design.md` supplies the overall target flows;
this document answers who owns each decision and how contexts may collaborate.

A context is an ownership and change boundary, not a process or container.
Contexts share the `v1_target` deployment and control PostgreSQL but do not
share private domain objects, repositories, tables, or write paths.

## 1. Contexts, ownership, and rationale

| Context | Package(s) | Owns | Does not own | Boundary rationale |
|---|---|---|---|---|
| Identity & Workspace | `identity_access` | users, principals, local auth, memberships, roles, OrgUnit structures, primary memberships, scoped leadership, department data policies, cross-department grants, resource ownership bindings, contributor activity projections, object/data ceilings, workspaces, sessions, API tokens, policy decisions | report definitions, source secrets, business data, raw employee analytics, notification content | authorization, organization scope, ownership, and tenancy have independent security/lifecycle rules |
| Connection Catalog | `connection_catalog` | connection versions, secret-reference metadata, source capabilities, source catalog snapshots, connector health | secret values, extracted rows, ingestion watermarks, semantic mappings | source configuration/metadata change independently from extraction |
| Semantic Model | `semantic_model` | datasets, entity/field mappings, joins, metrics/certification, metric groups, NumberFormatSpec, DiscountPolicyVersion, filters, capabilities, logical aggregate-compatibility rules | physical extraction, fitted attribution/decomposition results, report layout, comments | analytical meaning, pricing policy, and reusable numeric semantics require immutable versions |
| Data Documentation | `data_documentation` | Data Guides, FileImportTemplateVersion, validation/publication lifecycle, safe documentation projections | arbitrary source files, ingestion state, report narrative | governed explanation and intake shape are independently published contracts |
| Ingestion | `ingestion` | extraction specs, batches, source consistency observations, schema observations, watermark intents/commits, landing manifests | connection secrets, semantic definitions, DQ waivers | restartable source reads and watermark correctness form one consistency boundary |
| Artifact Lifecycle | `artifacts` | staging/commit visibility, manifests, hashes, authorization, retention/eviction, orphan cleanup, dependency references between immutable artifacts | business meaning, aggregate compatibility, run orchestration, report definition | immutable bulk data and Parquet materializations need atomic visibility and lifecycle independent of producers |
| Execution Control | `execution` | pipelines, schedules, materialization definitions, reuse planning, single-flight claims, partition invalidation coordination, resource lanes, commands, runs/node attempts, outbox, leases/fencing, retry/cancellation, reconciliation, progress | domain calculation semantics, terminal artifact contents | durable coordination, reuse and recovery are shared execution policy, not business logic |
| Data Quality | `data_quality` | rule versions, QualityReport, drift, remediation, waivers, gate/readiness decisions | semantic definitions, source extraction, analytical result identity | quality evidence and exception lifecycle have separate authority |
| Analytics | `analytics_core`, `analytics_customer`, `analytics_sales` | AnalysisSpec, result identity/manifests, PopulationTreatmentSpecVersion and diagnostics, bucket/stratification specifications, segment/model versions, membership snapshots, discount attribution/reconciliation and PVM specs/results, customer/sales analytics, comparisons, migrations | methodology review, reusable discount-policy meaning, report layout, forecasts, promotion facts, DQ rule authority | analytical population, transformations, calculations, pricing decompositions, and segmentation evolve together under reproducibility contracts |
| Methodology & Research | `methodology_research` | AnalysisMethodVersion availability/robustness/representativeness, MethodologyPack, AnalysisCase, ResearchDocumentVersion, FindingVersion, DecisionRecord, AnalyticalProduct | result calculation, report rendering, comments/reactions/views, metric certification ownership, object-access policy source of truth | methods, evidence review, narrative and findings form a knowledge lifecycle independent of social/adoption telemetry |
| Collaboration & Adoption | `collaboration_adoption` | requester/executor/owner/reviewer bindings, anchored comments, mentions, likes, asset subscriptions, meaningful-view events, permission-filtered activity feed, privacy-safe adoption aggregates, metric watches | report/research content, access grants, employee ratings, operational notification delivery, raw audit | collaboration and product-adoption telemetry have privacy, retention and moderation lifecycles distinct from authored analytical knowledge |
| Digital Journey & Marketing Measurement | `digital_marketing_analytics` | digital event taxonomy, sessions, marketing touchpoints/spend/cost facts, deterministic identity-link observations, attribution specs/results, unit-economics specs/results, governed assumptions and journey/funnel projections | source connector credentials, canonical offline receipt meaning, campaign activation, causal truth without evidence | cross-channel identity, spend reconciliation, attribution and cost economics change together and require a dedicated privacy/provenance boundary |
| Promotion Journal | `promotion_journal` | immutable promotion versions, planned/actual windows, channel/customer scope, audience bindings | causal attribution, segment calculation, chart rendering | business event history is descriptive input with its own lifecycle/ownership |
| Forecasting | `forecasting` | forecast specs, series/features, temporal backtests, model registry, predictions, intervals, monitoring | source ingestion, generic analytics, chart rendering | temporal validation/model lifecycle needs specialized invariants |
| Presentation & Reports | `presentation`, `chart_compiler_ts` | ChartSpec, dashboards, report definitions/snapshots, report/dashboard access-policy bindings, BrandProfile, CompanyPack, render metadata | analytical calculation, mail transport, comments/reactions/views, raw source rows | cross-channel composition and corporate identity require deterministic presentation versions |
| Report Delivery | `report_delivery` | sender/domain policies, verified sender reference, email delivery/attempt state, encrypted reconciliation handles | operational notifications, report definition, SMTP secret values | user email has external unknown-state and policy semantics separate from notifications |
| Notifications | `notifications` | inbox projections, preferences, acknowledgement/resolution, operational delivery state | user report email, source domain events, report snapshots | operational communication has different audiences, severity, and lifecycle |
| Audit | `audit` | append-only redacted events, retention, authorized query projections | business aggregate state, secrets, raw PII, complete provider payloads | tamper-resistant accountability must not depend on mutable domain tables |

## 2. Areas that are not bounded contexts

| Area | Role and constraint |
|---|---|
| `apps/*` | delivery/process composition roots; wire contexts and adapters but own no business rules |
| `contracts` | narrow shared kernel of IDs, version primitives, envelopes, trace metadata, and the three-layer UI identity/execution/surface schemas; no domain service or generic utility layer |
| `localization` | locale catalogs and formatting adapters; domain identity/calculation remains locale neutral |
| `plugin_sdk` | trusted extension compatibility boundary; does not own connector or destination state |
| `chart_compiler_ts` | deterministic ChartSpec compiler shared by Web/static rendering; never calculates analytical values |
| `plugins/*` | trusted source/outbound adapters implementing owner ports; never owners of product state |
| Edge/Web/API/worker processes | runtime composition and trust surfaces; not domain contexts |
| Brand assets | immutable validated artifacts referenced by Presentation; not executable templates or a separate brand service |
| Future activation boundary | public non-goal/port placeholder only; no public context, runtime, routes, or package implementation through v1 |

## 3. Dependency rules

### 3.1. Compile-time

1. Domain code imports only its own domain and the narrow shared kernel.
2. Application code imports its own domain and ports owned by its context.
3. An adapter imports the owner port and the technical library it encapsulates.
4. `apps/*` import application contracts and adapters only for composition.
5. A context cannot import another context's private domain/application module.
6. Provider-owned DTOs/events live with the provider public contract. Generic
   cross-context types enter `packages/contracts` only when they contain no
   business ownership.
7. TypeScript Web uses generated clients plus the versioned UI identity,
   execution, and surface coverage contracts; it never imports backend
   persistence or domain objects.
8. Source/destination plugins depend on port/SDK contracts and do not reverse
   the dependency into core packages.
9. `chart_compiler_ts` consumes validated ChartSpec only. It cannot import
   Analytics, Forecasting, Semantic Model, or report persistence.
10. Brand/locale adapters resolve presentation assets and strings after domain
    values are calculated; domain packages never depend on a theme or locale.

### 3.2. Runtime

- Every workspace call carries resolved `workspace_id`, actor, effective policy
  version, organization scope, trace identity, and contract version.
- Authorization is evaluated before protected fetch/action and re-evaluated by
  workers before source, artifact, render, export, or external delivery access.
- A write path belongs to exactly one context. Other contexts submit an owner
  command or consume a public projection/event.
- Synchronous calls are used for immediate request decisions; durable handoffs
  and external effects use outbox/events and idempotent consumers.
- Every delivery path assumes duplicates. Failures are explicit degraded,
  blocked, failed, or unknown states; empty data is never a silent substitute.
- Public projections include version, lineage, policy scope, and freshness.
- Cache identities include workspace and effective policy version; cached denied
  metadata is never returned after revoke.

## 4. Public port and projection catalog

| Owner | Public contract/port | Consumers | Key invariant |
|---|---|---|---|
| Identity & Workspace | `AuthorizationDecisionPort` | all protected contexts and apps | deny before fetch; no existence leak; policy version included |
| Identity & Workspace | actor/workspace/brand/locale projection | Web, Presentation, Notifications | installation role does not imply workspace membership |
| Identity & Workspace | organization structure/membership/leadership command and query ports | Admin Web, policy engine, Audit | exactly one active primary department/team; no hard delete; optimistic versioning |
| Identity & Workspace | department data policy, cross-department grant, ownership, and effective-access explanation ports | protected contexts, admin/member UI | bounded allow never exceeds functional/PII ceilings; deny wins |
| Identity & Workspace | privacy-safe ContributorActivityProjection | Organization/People Web, Presentation search | only visible resources and redacted aggregates; no raw Audit/ranking/score |
| Connection Catalog | versioned connection snapshot and connector capability projection | Ingestion, Semantic Model, operator UI | secret value/DSN never leaves adapter boundary |
| Data Documentation | published import-template projection | file intake, Ingestion, UI | exact media/sheet/column/type/limit version is pinned |
| Data Documentation | permission-aware Data Guide projection | Web Help, Reports, XLSX | safe labels only; no secret, denied PII, or raw query |
| Semantic Model | immutable semantic contract | Analytics, Forecasting, DQ, Research, Presentation | dataset/metric/filter/capability versions are explicit |
| Semantic Model | NumberFormatSpec/MetricGroup projection | Presentation, email, XLSX | raw typed value remains authoritative and ordering is stable |
| Semantic Model | metric certification/value-origin projection | Analytics, Research, Presentation | published lifecycle does not imply verified/canonical; proxy coverage and evidence stay explicit |
| Semantic Model | effective DiscountPolicy projection | Ingestion mapping, DQ, Analytics, Presentation | component catalog/stacking/precedence/accounting/cap/returns are immutable and interval-resolved |
| Ingestion | landing artifact commit request | Artifact Lifecycle | staging is invisible; watermark advances only after durable commit |
| Artifact Lifecycle | `ArtifactCommitPort` and authorized artifact reference | all bulk producers/consumers | manifest/hash/PII/lineage are immutable; access rechecked |
| Execution Control | command/task/status/progress ports | executable contexts, API, Web, operators | outbox, attempt identity, lease/fencing, reconciliation |
| Execution Control | materialization/reuse planner and single-flight claim ports | Analytics, Forecasting, Digital Measurement, Presentation | exact-compatible fresh artifact is reused; same-key work has one fenced publisher |
| Data Quality | pinned QualityReport/readiness projection | Semantic Model, Analytics, Forecasting, Presentation | missing/failed evidence is visible, never silently skipped |
| Analytics | reportable result and segment snapshot ports | Research, Presentation, Forecasting inputs where declared | result identity pins inputs/spec/code/filter/policy |
| Analytics | population-treatment specification/diagnostic ports | analytical routes, segment builder, Research, Presentation | method/action/fitted parameters/reference population/sensitivity and affected-row artifact identity are explicit |
| Analytics | segmentation definition/model/assignment ports | analytical routes, Research, Presentation, Execution Control | rule/bucket/strata/KMeans specs and immutable membership identity are versioned; fit and assignment are distinct |
| Analytics | discount component/reconciliation/cap diagnostic ports | analytical routes, Research, Presentation | line/component grain, policy, attribution mode, coverage, breach and result identity are pinned |
| Analytics | PVM specification/result port | analytical routes, Research, Presentation | formula order and price/volume/mix/assortment/residual reconcile to observed delta |
| Methodology & Research | published method/finding/research/product projections | Analytics orchestration, Presentation, search/help | discussion cannot become a finding; evidence/limitations are pinned |
| Methodology & Research | method availability and MethodologyPack projection | Analytics capability, Semantic Model CompanyPack, UI/help | future/unsupported methods never appear runnable; robustness and representativeness requirements are versioned |
| Collaboration & Adoption | participant/comment/reaction/subscription/feed ports | authorized Web, Notifications, Audit | exact resource version and current access are required; participant role never grants access |
| Collaboration & Adoption | adoption and watch projections | Workspace Admin, aggregate Installation Admin, asset viewers | meaningful views are deduplicated; cross-workspace data is suppressed and aggregate-only |
| Digital Journey & Marketing Measurement | event/touch/spend/cost intake contracts | governed connectors, file intake, Ingestion | taxonomy, grain, identity, consent, currency and provenance are pinned |
| Digital Journey & Marketing Measurement | attribution/unit-economics/journey result ports | Research, Presentation, watches | attributed is not causal; model/cost/identity versions and residuals are explicit |
| Promotion Journal | immutable promotion overlay projection | Analytics, Presentation, Forecasting feature binding | descriptive range only; audience/window version pinned |
| Forecasting | forecast artifact/model/readiness projections | Presentation, Research | temporal ordering and spec/model identity are required |
| Presentation & Reports | ReportSnapshot/ChartSpec/render request ports | Web, renderer, Report Delivery, XLSX | one resolved snapshot across all channels; no DOM scraping |
| Presentation & Reports | object-access binding command/query | Identity policy evaluation, admin UI | administrative access grant is independent of authoring/publish |
| Presentation & Reports | resolved BrandProfile/CompanyPack projection | Web, email, XLSX, docs renderer | validated local assets and immutable versions only |
| Report Delivery | `ReportDeliveryPort` | API/Web, execution worker | verified user sender, domain/DLP checks, unknown-state reconciliation |
| Notifications | event intake/inbox/preference ports | all contexts, Web, operational adapters | recheck access before display/delivery; report email excluded |
| Audit | redacted append/query ports | all mutating contexts, admin UI | failure policy decided before side effect; secrets/raw PII forbidden |

## 5. Primary relationships

| Caller | Owner/callee contract | Form | Consistency and failure rule |
|---|---|---|---|
| Any protected use case | Identity & Workspace | synchronous authorization | deny before fetch/action; denied resource metadata is not disclosed |
| Web route guard | Identity & Workspace + executable route contract | synchronous policy resolution | role hint is discoverability only; API authorization remains mandatory |
| UI composition/audit tooling | route identity + execution + surface coverage contracts | static resolution and generation | every product use case resolves to valid route/overlay/system/capability IDs; current route count is not a ceiling |
| Identity & Workspace | Audit | outbox event for membership/role/grant/session mutation | record actor/scope/diff without secret/token value |
| Organization administration | Identity & Workspace | versioned owner commands with ETag/If-Match | invalid hierarchy, overlapping primary assignments, or stale version fails atomically |
| People & Creators query | Identity & Workspace | policy-filtered contributor projection | self/leader/grantee scopes differ; hidden resources and counts are omitted before aggregation |
| Presentation publication/transfer | Identity & Workspace | ownership binding and handover command | creator attribution remains immutable; published default owner is primary department; deactivation fails closed |
| Any cross-department consumer | Identity & Workspace | bounded grant/effective-access decision | grant expiry/revoke invalidates cache and never expands role/PII ceiling |
| Connection Catalog | Audit | outbox event | connection/secret-reference changes recorded without DSN/secret |
| File intake | Data Documentation | pinned template query | unknown sheets/columns, macros/formulas, limits, or type violations reject safely |
| Ingestion | Connection Catalog | versioned connection snapshot | rotation cannot change a running batch; secret resolved only in adapter |
| Ingestion | Artifact Lifecycle | staging plus atomic commit port | no artifact visibility before manifest/hash commit |
| Ingestion | Execution Control | task/progress/terminal command | watermark commit and terminal state reconcile after restart |
| Ingestion | Data Quality | artifact/schema event | new batch triggers required checks; failure remains visible |
| Data Quality | Semantic Model + Artifacts | pinned references | reproducible report; missing input blocks/fails, never becomes empty success |
| Semantic Model | Data Quality | validation/readiness query | publication capability includes current DQ/freshness evidence |
| Semantic Model | Audit | outbox event for publish/deprecate | immutable version and downstream impact recorded |
| Analytics | Semantic Model + DQ + Artifacts | versioned query/reference | result identity includes inputs, spec, code, filters, comparison, policy |
| Analytics population treatment | Semantic Model + DQ + Artifacts | pinned eligible population plus versioned fit/diagnostic artifact | treatment is not a DQ correction; current and `vs LY` share fitted policy unless explicitly versioned otherwise |
| Analytics segmentation | Semantic Model + DQ + Artifacts | pinned features/treatment/model/membership artifacts | boundaries, order, null policy, transforms, scaling, K, seed, model and assignment versions are explicit |
| Analytics discount economics | Semantic Model + DQ + Artifacts | effective policy plus line/component/source facts and immutable diagnostics | no unknown-as-zero, implicit allocation, hidden stacking, historical clamp, or unaudited residual attribution |
| Analytics PVM | Semantic Model + Artifacts | pinned metrics/product identity/period/currency/returns/method | decomposition must reconcile before trusted commit; drill-down preserves parent totals |
| Analytics | Promotion Journal | immutable overlay input | promotion overlap is descriptive; causal claim requires methodology |
| Analytics | Execution Control + Artifacts | reuse-plan/task plus result commit | exact-compatible result is reused; concurrent same-key work coalesces; committed result immutable |
| Forecasting | Semantic Model + DQ + Artifacts | pinned series/feature references | temporal order/model/spec identity and degradation are explicit |
| Forecasting | Execution Control | train/backtest/predict task | cancel/retry/reconcile preserve attempt and model lineage |
| Methodology & Research | Semantic Model + Analytics + Forecasting | pinned method/result/evidence references | research publication preserves exact versions and limitations |
| Methodology & Research | Presentation & Reports | publication port | research may produce dashboard/report without mutating result identity |
| Methodology & Research | Identity & Workspace | resource/block access decision | findings/search respect object/data/PII ceilings |
| Collaboration & Adoption | Identity & Workspace + Presentation/Research | current access and exact resource projection | deny before feed/count/thread; participant binding never expands policy |
| Collaboration & Adoption | Notifications | comment/mention/watch event | recipient access is rechecked before notification projection |
| Collaboration & Adoption | Audit | redacted lifecycle events | body/PII is excluded where policy requires; free discussion remains distinct from reviewed finding |
| Digital Journey & Marketing Measurement | Semantic Model + Ingestion + Artifacts | pinned digital/offline facts and identity/cost specs | join grain/cardinality/coverage reconcile; missing spend is not zero |
| Digital Journey & Marketing Measurement | Execution Control + Artifacts | reuse-plan/task plus result commit | attribution/journey/unit-economics results are immutable and same-key compute coalesces |
| Digital Journey & Marketing Measurement | Methodology & Research | evidence-strength contract | descriptive attribution cannot be relabelled causal or incremental |
| Presentation & Reports | Analytics/Forecasting/DQ/Promotions | reportable result ports | resolved snapshot pins all sources, comparison, quality, lineage, PII |
| Presentation & Reports | Semantic Model | metric format/group projection | channel formatting uses one version; raw value unchanged |
| Presentation & Reports | Identity & Workspace | access/effective-policy query | report/dashboard grant does not exceed source/row/PII permissions |
| Presentation & Reports | Artifact Lifecycle | rendered artifact commit | render output gets manifest/hash/renderer/version/retention |
| CompanyPack resolution | Semantic Model + Methodology & Research + Data Documentation | versioned approved-pack references | overrides create new versions; source pack remains immutable |
| BrandProfile resolution | localization + artifact assets | adapter/projection | only validated local assets/tokens; safe system fallback on failure |
| Report Delivery | Presentation & Reports | immutable ReportSnapshot/rendered artifacts | cannot recalculate or use mutable draft/DOM state |
| Report Delivery | Identity & Workspace | sender/report/source/PII/domain permission decisions | checks repeat before render and before submit |
| Report Delivery | Execution Control | delivery task/unknown reconciliation | blind retry after unknown provider result is forbidden |
| Report Delivery | Audit | redacted outcome event | recipient/sender policy versions and hashes only; no full body/list |
| Notifications | domain events + Identity & Workspace | outbox/event projection | permission rechecked before inbox/channel delivery |
| All mutating use cases | Audit | append command/outbox | audit failure policy determined before business side effect |

## 6. Population treatment and segmentation dependency rules

Analytics owns population-treatment and segmentation semantics because they
change analytical population, result identity, and reproducibility. Data
Quality owns evidence about invalid, missing, stale, or inconsistent data; it
does not silently exclude statistically unusual but valid observations.
Semantic Model owns metric/field meaning and reusable transformations, while an
Analytics specification pins the exact feature set and treatment application.

`PopulationTreatmentSpecVersion` records method (`quantile`, `iqr`, or `mad`),
parameters, scope, grouping, reference population, action (`flag`, `exclude`,
or `winsorize`), fitted bounds/statistics, null policy, implementation version,
and diagnostic artifact references. The same fitted treatment applies to
current and prior-year comparison populations by default. Publication requires
visible sensitivity evidence, including counts/shares and affected metric,
protected-cohort, and high-value-customer impact.

Rule, bucket, and stratified segmentation pin deterministic boundaries,
inclusivity, null/overflow policy, labels, ordering, target allocation, and
tie-breaking. Exact-K KMeans additionally pins feature order, transforms,
scaling, missing-value policy, requested K, initialization, seed, implementation
version, fitted model, cluster diagnostics, and empty/small-cluster behavior.
Fit and assignment are separate commands. Published definition/model and
membership snapshots are immutable artifacts; later assignment never mutates a
historical snapshot.

Execution Control owns asynchronous progress, cancellation, leases, retry, and
reconciliation. Artifact Lifecycle owns atomic diagnostic/model/membership
visibility. Presentation and Research consume public projections and disclose
treatment/model identity and limitations through Result Trust; they cannot
re-fit or change membership.

### 6.1. Discount economics and methodology trust dependency rules

Semantic Model owns stable component roles, metric definitions/certification,
and effective `DiscountPolicyVersion` because these meanings must be reused by
every analysis and channel. It resolves non-overlapping effective intervals and
publishes component catalog, source binding, stacking/precedence, bonus
accounting treatment, cap/base/tolerance/rounding, returns, and breach rules.
It does not fit residual attribution or calculate a report result.

Ingestion preserves raw mapped values. Data Quality owns coverage,
reconciliation, impossible combination, and historical cap-breach evidence. A
quality action may degrade or block trusted analysis but cannot clamp or rewrite
canonical sales. Promotion Journal may provide an exact version reference and
descriptive time context; date overlap alone is not sale-level promotion
evidence.

Analytics owns normalized line/component facts, attribution diagnostics,
component/total ratios, overlap/depth/cap result artifacts, and versioned PVM
specifications/results. It commits only after grain-safe aggregation and declared
tolerance reconciliation. A simulated cap violation blocks publication;
historical violations remain visible evidence. Current and `vs LY` pin the same
policy/method by default, while policy drift creates a different result identity
and explicit comparability warning.

Methodology & Research owns method availability, evidence-strength ceiling,
robustness/representativeness expectations, and MethodologyPack composition. It
does not own metric certification (Semantic Model) or execute Analytics private
calculations. `future_extension` and `unsupported` entries are documentation and
capability states, never worker bindings. Presentation consumes only public
projections and exposes attribution mode, coverage, policy, cap, PVM order,
residual, certification, and limitations through Result Trust and exports.

## 7. CompanyPack and branding dependency rules

Presentation & Reports owns BrandProfile and CompanyPack identity, validation,
publication, binding, and rollback because they define cross-channel corporate
presentation. It does not take ownership of the domain objects included in a
pack.

A CompanyPack contains versioned references to installation-approved assets and
domain packs:

- `BrandProfileVersion` owned by Presentation;
- `MetricGroupVersion` and default `NumberFormatSpec` owned by Semantic Model;
- `MethodologyPack` entries owned by Methodology & Research;
- optional approved `DiscountPolicyVersion` binding owned by Semantic Model;
- file-import templates and Data Guide templates owned by Data Documentation;
- localization catalogs resolved through the localization adapter.

Installation approval records allowed references. Workspace assignment resolves
an immutable CompanyPack version. A workspace override creates a new version in
the owning context and a new pack binding; it never mutates the approved source.
Executable templates, remote assets, secrets, and customer code are prohibited.

## 8. Organization, object access, collaboration, and audit dependency rules

Identity & Workspace owns organization structures and policy composition; no
new Organization bounded context or deployable microservice is introduced.
Functional roles, one primary OrgUnit assignment, and scoped leadership remain
separate aggregates. `DepartmentDataPolicyVersion` constrains dataset, row,
column, and PII scope. `CrossDepartmentGrant` adds only a bounded, reasoned,
effective-dated allow within the existing role/PII ceilings. The authorization
port intersects these layers with the resource policy and applies deny before
fetch, count, search, aggregation, pagination, caching, or action.

Presentation & Reports owns report/dashboard definitions and access-policy
bindings but does not own organization truth. On publication it asks Identity
to create a department-default `ResourceOwnershipBinding`. Creator identity is
immutable; owner may transfer. A member transfer/deactivation closes the prior
scope and produces handover work through owner commands/events. Legacy
published resources migrate to `workspace_legacy` until audited assignment.

Identity consumes allowlisted redacted domain events to maintain
`ContributorActivityProjection`. Audit remains append-only accountability and
is not queried as an employee-analytics store. People & Creators may show only
visible resources and safe activity aggregates to self, scoped leaders, or
explicit grantees. Rankings, leaderboards, productivity scores, peer
percentiles, hidden counts, and raw event feeds are prohibited.

Identity & Workspace owns generic principals, grants, policy ceilings, and the
authorization engine. Presentation owns the report/dashboard access-policy
resource and submits versioned grant/revoke commands through an administrative
port. Collaboration & Adoption owns comments, participant bindings, reactions,
subscriptions, meaningful views, activity feed and adoption aggregates. Every
read/write resolves authorization from Identity against the exact resource
version/snapshot and optional block; a requester/executor binding never grants
that authorization. Methodology & Research continues to own reviewed findings
and narrative, not discussion telemetry.

Access revocation immediately prevents thread/feed discovery and notification
delivery. Comments and likes do not enter immutable reports by default. An
approved discussion summary becomes a separately reviewed/versioned report or
research block. Adoption is aggregate-first, never a rating or productivity
score, and installation-wide views suppress small groups and identities. Audit
records object-access and collaboration lifecycle without body content when
policy requires redaction.

## 8.1. Materialization and compute-reuse dependency rules

Semantic Model owns logical compatibility: grain, dimensions, metrics, filters,
assumptions and aggregation rules. Execution Control owns immutable
materialization definitions, reuse-key normalization, aggregate-aware planning,
single-flight claims, refresh scheduling, partition invalidation coordination,
and interactive/precompute/maintenance resource lanes. Artifact Lifecycle owns
the committed Parquet artifact, manifest/hash, authorization, dependency
references, retention and eviction.

PostgreSQL remains control-plane truth; local Parquet remains durable bulk and
materialization truth; Valkey and process memory hold only bounded ephemeral
locks, pointers and small results. Web, email, XLSX and API consumers request the
same semantic/result artifact. A policy change invalidates authorization even
when bytes remain present, and last-good serving is allowed only by an explicit
freshness policy with a visible limitation.

## 8.2. Digital measurement dependency rules

Digital Journey & Marketing Measurement owns canonical web/app events,
sessions, marketing touches, spend/cost facts, attribution and unit-economics
specifications/results, governed assumptions, funnels and journey projections.
It consumes offline retail facts and reusable metric meaning only through
Semantic Model/Ingestion/Artifact public contracts. Provider reports remain
separate from independently observed facts; deterministic identity links are
versioned and consent-aware, and ambiguous matches remain unresolved.

Attribution models describe credit allocation, not causality. Algorithmic
attribution, probabilistic identity, campaign activation and arbitrary external
writeback remain future capabilities. Shared cost allocation exposes residuals,
and every result pins time, currency, FX, identity, cost and model versions.

## 9. Import-template and connector dependency rules

Data Documentation owns the published file shape because it is a governed
human/machine contract and can be versioned with its guide. Connection Catalog
owns the connection mode and source metadata. Ingestion owns physical parsing,
batch consistency, rejected-row artifact production, and watermarks. Data
Quality owns rules applied to committed intake; Semantic Model owns mapping from
typed source fields to business entities/metrics.

Database connectors implement a Connection Catalog/Ingestion port and use an
anti-corruption layer for identifier quoting, decimals, timezone, source
versions, consistency, and pushdown capabilities. Connector-specific DTOs do
not escape into domain packages. Yandex Metrica remains a future adapter
boundary and does not create an active public context or credential route.

## 10. Report, formatting, and export dependency rules

Semantic Model owns what a metric means, its group/order, and its display
contract. It also owns metric certification/value origin and reusable discount
policy semantics. Analytics/Forecasting own typed raw values and result
identity; Analytics owns component attribution and PVM diagnostics.
Presentation resolves those values into ReportSnapshot blocks and ChartSpec.
Static renderers, Report Delivery, and XLSX are adapters/consumers; they cannot
override calculations, grouping, units, compact thresholds, or precision.
They also cannot relabel a proxy as direct, clamp a breach, infer promotion from
timeline overlap, or recompute PVM with another order.

XLSX rendering remains an adapter behind `XlsxRendererPort`, not a separate
bounded context, because it owns no durable business lifecycle. It commits the
result through Artifact Lifecycle and execution status through Execution
Control. Report Delivery is a context because email policy, sender identity,
attempts, provider unknown state, reconciliation, and retention form an
independent durable lifecycle.

## 11. PostgreSQL ownership model

One PostgreSQL deployment does not imply one schema owner. Every migration,
table, repository, and write path has exactly one context owner. Recommended
physical schemas or table prefixes mirror the package owner. Transaction-local
workspace/policy context and PostgreSQL RLS may add defense in depth after the
application policy is evaluated.

Cross-context foreign keys are allowed only as documented integrity contracts.
They never grant mutation rights or justify direct repository imports. Read
models may denormalize public projections when they preserve source version,
lineage, policy scope, and explicit freshness. An owner event/outbox record is
the only supported way to keep a cross-context projection current.

## 12. Consistency and failure matrix

| Decision | Required consistency | Failure behavior |
|---|---|---|
| authorization before protected fetch/action | synchronous strong decision against current policy version | deny safely; no resource leak or stale-cache fallback |
| organization structure/membership publication | Identity owner transaction plus audit/outbox intent | stale/invalid hierarchy or overlapping primary assignment rejects atomically; previous version remains active |
| cross-department grant/revoke | strong policy write plus effective-policy cache invalidation | expiry/revoke fails closed; consumer never keeps broader stale access |
| contributor activity projection | eventual redacted event projection with explicit freshness | stale marker allowed; raw Audit fallback and hidden-count approximation forbidden |
| member transfer/deactivation handover | strong old-scope termination plus durable ownership handover events | access closes immediately; unresolved ownership is visible/blocked, creator history preserved |
| publish immutable definition/method/report/brand/template | owner transaction plus audit/outbox intent | publication fails atomically; draft remains available |
| artifact visibility | staging plus atomic manifest/hash commit | staging remains invisible and is reconciled/cleaned |
| extraction watermark | commit only after source-consistent artifact visibility | retry from prior durable watermark; never skip unseen rows silently |
| task delivery | at-least-once with idempotency and lease/fencing | duplicate safe; expired/lost work reconciled |
| comment/notification | owner commit plus event projection | comment remains authoritative; delayed notification exposes freshness |
| treatment/segmentation publication | Analytics owner transaction plus immutable artifact commits and audit/outbox intent | publication fails atomically; draft and prior published versions remain available |
| discount-policy publication | Semantic Model owner transaction plus impact/audit/outbox | overlapping effective interval or invalid stacking/cap policy rejects publication; prior version remains available |
| discount/PVM result commit | Analytics immutable artifact commit after DQ/reconciliation | mismatch, unknown policy, simulated cap breach, or unresolved residual blocks trusted visibility; source facts remain unchanged |
| metric certification/method availability | owner-context immutable evidence/version transaction | failed review leaves prior certification/availability intact and cannot mutate metric/method history |
| report render/export | immutable snapshot plus asynchronous artifact commit | stable failed/blocked state; no partial artifact visibility |
| email submit | persisted idempotency/reconciliation handle before external effect | unknown state reconciles; no blind retry |
| company pack resolution | immutable references across owner contexts | invalid binding rejected; last valid/system fallback remains available |
| search/impact projection | eventual with explicit freshness/version | stale indicator; never bypass current authorization |

## 13. Rules for changing the map

- A new bounded context requires an independent ownership, volatility, trust,
  failure, or lifecycle rationale; a new page or directory is insufficient.
- Extracting a service before `v1_target` requires an ADR establishing an
  independent scale, trust, failure, or release boundary.
- Moving ownership is a contract change with consumer inventory, schema/data
  migration, compatibility window, rollback, and proof at the real boundary.
- A new cross-context read requires a public query/projection contract; a new
  write requires an owner command/event. Direct private-table access is not a
  temporary shortcut.
- Shared-kernel additions require proof that no context owns the semantics.
- `check_ddd_boundaries` enforces declared imports. Exceptions require a named
  owner, rationale, expiry/review trigger, and an explicit migration path.

## 14. Acceptance of an implementing module

Before implementation, the responsible specification or vertical ticket names:

- purpose, non-goals, vocabulary, owner context, and package path;
- aggregates, invariants, commands, queries, events, and state transitions;
- owned tables/artifacts and public ports/projections;
- upstream/downstream dependencies from this map;
- permission, workspace, object, row/data, PII, and audit behavior;
- idempotency, retry, cancellation, reconciliation, and retention;
- routes, states, accessibility, localization, and design-contract references;
- fixtures and real proof boundary, including migration and rollback.

The artifact choice and execution authority follow
`development-operating-model.md` and Global Delivery Contract v1. This map is
not a ticket backlog and does not prove an implementation exists.
