---
doc_id: ARCH-SYSTEM-DESIGN-001
title: Custometry Target System Design
doc_version: 18
product_spec_version: 0.11.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [ARCH-PRINCIPLE-001, GOAL-011, GOAL-012, GOAL-013, GOAL-014, GOAL-015, GOAL-016, GOAL-017, GOAL-018, ANALYTICAL-DOC-001, BLOCK-BUILDER-001, PRODUCT-ANALYTICS-001, UC-017, UC-018, UC-020, UC-021, UC-022, UC-023, UC-024, UC-025, UC-026, UC-027, UC-028, UC-029, CONNECTOR-001, DIGITAL-001, ATTRIBUTION-001, UNIT-ECON-001, ASSUMPTION-001, MATERIALIZE-001, COLLAB-001, WATCH-001, METHOD-001, METHOD-009, METRIC-009, METRIC-017, DISCOUNT-001, PVM-001, RBAC-009, RBAC-010, RBAC-011, RBAC-019, RBAC-020, RBAC-027, REPORT-003, REPORT-012, ROUTE-001, ROUTE-012, OUTLIER-001, SEGMENT-001, SEGMENT-019, FILTER-013, SEGMENT-034, PIVOT-001, PARAM-001, REPORT-016, THEME-001, WEB-ARCH-001, WEB-ARCH-002, WEB-ARCH-004, WEB-PERF-001, WEB-PERF-005, PRIVATE-FUTURE-001]
status: accepted
proof_boundary:
  label: accepted-v1-target-architecture
  exclusions: [implementation-readiness, runtime-readiness, browser-readiness, recovery-readiness, performance-readiness, release-readiness]
---

# Custometry - Target System Design

## Document status and authority

This document projects the normative Custometry product specification
`0.11.0-draft` into an implementable target architecture. It defines ownership,
dependency direction, integration contracts, trust boundaries, consistency,
failure semantics, compatibility, and proof seams. It does not repeat every
product requirement and does not replace:

1. `custometry-technical-blueprint-ru.md`, the normative machine specification;
2. `custometry-technical-blueprint-human-ru.md`, its synchronized explanatory mirror;
3. `custometry-ui-blueprint-ru.md`, the derived UI and interaction contract;
4. `bounded-context-map.md`, the detailed DDD ownership and dependency policy.

The target is a self-hosted, multi-workspace B2C retail analytics platform. The
implementation form through `v1_target` is a modular monolith deployed on one
server with Docker Compose. Architecture statements are accepted design, not
evidence that a component, route, connector, or workflow already exists.

This Markdown file is the sole maintained System Design source. Derived binary
copies are not versioned because they add a second synchronization surface
without an independent product, delivery, or acceptance use case. A PDF or
DOCX may be generated on demand for a specific external handoff, but it is an
ephemeral export and never an architecture authority or acceptance dependency.

**Execution priority, 2026-09-05:** Forecasting is on hold until explicit owner
resumption. Its target boundaries below are retained; they do not authorize
forecast-specific work or block independent reports/segments. The first
external release scenario remains undecided.

## 1. Outcome, scope, and non-goals

Custometry standardizes analytical work that is otherwise fragmented across
Excel files, notebooks, personal formulas, and repeated ad hoc requests. The
platform must let governed data become reusable metrics, analyses, research,
segments, forecasts, dashboards, reports, and decisions while preserving the
method, filters, versions, quality, permissions, and evidence behind each
result.

The `v1_target` architecture includes:

- local accounts, multiple workspaces, role and object access management;
- a versioned organization tree, primary department assignments, scoped
  leadership, department data policies, cross-department grants, analytical
  resource ownership, and privacy-safe People & Creators views;
- CSV/XLSX template import plus PostgreSQL, Microsoft SQL Server,
  MySQL/MariaDB, and ClickHouse source connectors;
- catalog, semantic model, metrics, metric groups, number formats, filters,
  Data Guides, data quality, ingestion, immutable artifacts, and pipelines;
- customer and sales analytics, governed population/outlier treatment,
  rule/bucket/stratified/exact-K KMeans segmentation,
  cohort/lifecycle/basket/channel analysis, component discount/cap and
  price-volume-mix analysis, product/category hierarchy, assortment,
  inventory/availability, pricing/markdown, ABC/XYZ and lifecycle analytics,
  governed custom analysis,
  Promotion Journal, and forecasting;
- Methodology Registry with explicit availability, metric certification/proxy
  quality, Methodology Packs, representativeness and robustness contracts,
  Analysis Cases, Research Workspace, reviewed findings and decisions,
  and reusable analytical products;
- collaboration around dashboard/report/research assets with requester and
  executor roles, anchored comments, likes, subscriptions, permission-filtered
  activity, privacy-safe adoption statistics, and metric watches, without
  ratings or employee rankings;
- canonical web/app journeys, marketing touches and spend/cost facts,
  deterministic identity linkage, governed attribution and unit economics,
  and versioned targets/budgets/scenarios joined to offline retail facts;
- content-addressed materialization and aggregate-aware reuse over local
  Parquet, with single-flight execution, partition invalidation, off-peak
  precompute, and priority isolation for interactive work;
- one analytical-document composition and root/page snapshot path for compact
  dashboards, multi-page workbook reports and narrative research, including
  notes, data annotations, discussions, page/filter scopes, lazy active-page
  projection, user-initiated email, CSV/Parquet where allowed, and universal
  XLSX as the final v1 functional increment;
- white-label Brand Profiles and Company Packs without customer-specific code
  forks or images;
- local documentation at `/docs` and permission-aware help at `/help`;
- CPU-only execution with detected/admin-capped cores and observable progress,
  ETA, cancellation, and recovery semantics.

The following are outside the public `v1_target`:

- B2B account/opportunity/contract ontology;
- SaaS control plane, managed customer-data path, Kubernetes, multi-host
  execution, or cloud distribution;
- Yandex Metrica runtime integration, OIDC runtime, and arbitrary destination
  connectors;
- public activation orchestration, reverse ETL marketplace, commercial
  entitlement implementation, or private distribution roadmap;
- arbitrary user code and notebooks inside the production runtime;
- GPU computation, ECharts-GL/WebGL, Dash, or Plotly as a core dependency.

## 2. Architectural decisions

| Area | Accepted decision | Consequence |
|---|---|---|
| Product form | Self-hosted multi-workspace B2C retail platform | Tenant and policy scope are installation/workspace/object, not SaaS account hierarchy |
| Application form | Modular monolith through `v1_target` | Contexts share deployment and PostgreSQL but own code, tables, write paths, and public contracts |
| UI delivery | UI-first, contract-backed vertical slices | A visible route is not accepted until the same contract reaches real API/data or artifact evidence |
| Authenticated frontend | ADR-0007 pins the responsive-Web frontend stack and ownership boundaries for current Web implementation | Client presentation state stays separate from authoritative API/event state |
| UI execution route | Current Web implementation follows the ticket-first source contract and accepted target pilot | Current code is not automatically conformant; the removed G-program is not an execution route |
| Presentation system | Semantic, accessible, brand-aware tokens are owned by the accepted Web frontend platform and `packages/ui-foundation` | The target pilot owns demonstrated visual and interaction choices; production conformance remains ticketed work |
| Data truth | PostgreSQL control state plus immutable Parquet/other artifacts | Valkey, browser state, and task delivery cannot determine terminal truth |
| Data compute | Polars/DuckDB/NumPy-first CPU execution; Numba only for measured kernels | Browser, chart library, and XLSX renderer do not perform analytical reduction |
| Compute reuse | Content-addressed materializations with aggregate-aware planning and single-flight | Equivalent work is reused; invalidation is partition-scoped and precompute cannot starve interactive work |
| Analytical documents | Presentation-owned `AnalyticalDocumentCompositionV1` with dashboard, workbook-report, and narrative-research profiles | One hierarchy/filter/root-page snapshot path serves Web/email/XLSX without merging domain lifecycles or creating a new service |
| Large-document execution | Permission-filtered page index, active-page mount, bounded prefetch and block/page reuse | The 100-by-30 envelope is benchmarked; production hard limits follow evidence and versioned resource policy |
| Product analytics | Semantic hierarchy/assortment meaning, ingestion-owned source facts, Analytics-owned results | Category history is versioned; missing inventory is not zero; basic ABC/XYZ is V1 target |
| Collaboration | Separate Collaboration & Adoption context | Requester/executor/comments/likes/views/follows are permission-aware; ratings and employee leaderboards are prohibited |
| Digital measurement | Canonical event/touch/spend/cost facts plus versioned attribution and unit-economics specs | Provider claims stay distinct, identity coverage is explicit, and attributed is never silently causal |
| Jobs | Transactional outbox, at-least-once tasks, leases/fencing, reconciliation | Duplicate delivery is expected; every side effect needs an idempotency identity |
| Visualization | Product-owned `ChartSpec`, compiled to ECharts | Raw ECharts options, callbacks, code, URLs, and remote assets are rejected |
| Report composition | One immutable `ReportSnapshot` for Web/email/XLSX | Export does not scrape the DOM or recalculate hidden channel-specific metrics |
| Population treatment | Versioned `PopulationTreatmentSpecVersion` with quantile, IQR, and MAD methods | Treatment is reproducible, disclosed, sensitivity-testable, and distinct from data-quality correction |
| Segmentation | Reusable definition, time-bound run, immutable snapshot, and explicit consumer binding | Exact as-of belongs to the run/snapshot; report/research pin exact snapshots; live dashboard latest-successful resolves to an exact ID |
| Discount economics | Receipt-line component fact plus effective `DiscountPolicyVersion` | Promotion, loyalty, bonus redemption, other, commercial discount, customer benefit, recognized revenue, stacking, cap, and attribution quality remain explicit and reproducible |
| PVM | Versioned, exactly reconciled decomposition with explicit order | Price, volume, mix, assortment, and residual cannot be hidden chart calculations or causal claims |
| Metric trust | Certification and value origin are separate from definition lifecycle | Published candidate/proxy values cannot appear canonical/direct without review and disclosure |
| Method availability | `native_v1`, `template_v1`, `future_extension`, or `unsupported` | Future causal/uplift/anomaly/decision contracts are discoverable without becoming runnable claims |
| Organization model | Functional roles, organization membership, and scoped leadership are independent | Company structure does not create role explosion or implicit PII/business-data authority |
| Effective access | Role and workspace permission intersect with organization, department data, object, row/column, and PII policies; deny wins | Cross-department grants can only add a bounded allow inside existing ceilings |
| Contributor insights | A redacted aggregate projection is separate from append-only Audit | People & Creators cannot become raw employee surveillance, ranking, or productivity scoring |
| UI surfaces | Compact route identity, executable route policy, and complete UI surface coverage are separate contracts | URL identity remains stable; route policy evolves independently; every UI-visible use case must bind to a route, overlay, system surface, or reusable capability |
| Branding | Versioned BrandProfile and CompanyPack | Customer identity changes by validated configuration, not code fork |
| Distribution | Public self-host core only | Future activation/commercial implementation remains outside the public repository and public package graph |
| First platform | Mac M5 Max / 36 GB, followed by separate Linux VM proof on the same host | Other architectures and production hardening require separate evidence |

## 3. Dependency direction and composition

```text
browser / CLI / scheduler / worker entrypoint
                    |
                    v
            inbound adapter / app
                    |
                    v
           application use cases
                    |
                    v
              domain model
                    | owns outbound ports
                    v
        infrastructure adapter implementation
```

`apps/*` are composition roots. `packages/*` contain domain/application code
and the ports owned by each context. Adapters implement those ports and are
wired only at composition roots. Domain/application code does not import Web
frameworks, queue libraries, SQL drivers, filesystem implementations, or
another context's private tables.

Contexts may share a PostgreSQL deployment but never a generic shared-table
model. Cross-context reads use a public projection or query port. Cross-context
writes use an owner command or versioned event. A database foreign key may
enforce integrity but does not grant another context mutation authority.

The shared kernel is intentionally narrow: stable identifiers, locale-neutral
primitive contracts, version primitives, trace metadata, and the common error
envelope. Metrics, filters, access rules, research objects, charts, reports,
and connector semantics remain owned by their contexts.

## 4. Bounded contexts and ownership

The target has eighteen bounded contexts.

| Context | Primary ownership | Public architectural role |
|---|---|---|
| Identity & Workspace | principals, local auth, memberships, roles, organization units/assignments/leadership, department data policies, cross-department grants, resource ownership, contributor-activity projections, sessions, API tokens | resolves actor/workspace/organization/object/data ceilings before protected work |
| Connection Catalog | connection definitions, secret references, source capabilities, catalog snapshots | exposes versioned, non-secret source metadata and connector policy |
| Semantic Model | datasets, entity/field mappings, joins, metrics, certification evidence, metric groups, number formats, discount policies, product/category hierarchy and assortment-scope semantics, filters, capabilities | supplies immutable analytical meaning, hierarchy history, component/policy semantics, and presentation-neutral numeric semantics |
| Data Documentation | Data Guides and file-import templates | supplies governed documentation and typed CSV/XLSX intake contracts |
| Ingestion | extract specifications, watermarks, batches, schema observations, inventory/availability/price/planned-assortment source facts | converts approved source snapshots into committed landing artifacts |
| Artifact Lifecycle | manifests, hashes, authorization, retention/eviction, dependency references, staging/commit visibility | owns immutable bulk-result and Parquet-materialization identity and access decisions |
| Execution Control | pipelines, schedules, materialization definitions/reuse planning/single-flight, resource lanes, runs, node attempts, outbox, leases, cancellation, reconciliation | coordinates every asynchronous, reuse, or restart-sensitive operation |
| Data Quality | rules, reports, drift, remediation, waivers | produces visible quality evidence and gates downstream readiness |
| Analytics | analysis and normalized block specifications, result manifests, population-treatment specifications/diagnostics, bucket/stratification specifications, segment definitions/runs/snapshots/bindings, discount-component attribution/reconciliation results, PVM specifications/results, customer/sales/product/category/assortment/inventory analytics | produces bounded, reproducible reportable results, comparisons, pricing/product economics, and governed analytical populations |
| Methodology & Research | methods with availability/robustness/representativeness contracts, Methodology Packs, cases, research documents, findings, decisions, analytical products | turns ad hoc questions into reviewed, reusable knowledge with pinned evidence and prevents future methods from masquerading as implemented |
| Collaboration & Adoption | participant bindings, document/page/block/data discussions and replies, mentions, resolve/reopen and re-anchor provenance, likes, subscriptions, meaningful views, feed, adoption aggregates, metric watches | supplies permission-safe collaboration and usage evidence without becoming employee scoring or authored report content |
| Digital Journey & Marketing Measurement | event taxonomy, sessions, touches, spend/cost, identity-resolution artifacts, campaign normalization, journey/conversion and cost-reconciliation versions, attribution, unit economics, governed assumptions, funnels/journeys | joins digital acquisition behavior to governed offline retail facts with explicit identity/provenance/causality limits |
| Promotion Journal | promotion versions, planned/actual windows, channel/client scope | supplies descriptive `range_timeline` overlays and promotion context |
| Forecasting | series/features, forecast specs, backtests, models, predictions, monitoring | produces temporally valid forecasts and readiness/degradation evidence |
| Presentation & Reports | AnalyticalDocumentVersion/CompositionV1, root/page snapshots, notes/annotations, ChartSpec, dashboard/report lifecycle projections, object access bindings, branding, rendered metadata | composes governed results for interactive and static channels through one composition/snapshot path |
| Report Delivery | sender/domain policies, delivery attempts, reconciliation | owns user-initiated email as a recoverable external side effect |
| Notifications | preferences, in-app events, operational channel deliveries | projects domain/operational events without becoming report email |
| Audit | append-only redacted events and authorized projections | records security and business mutations without secrets or raw PII |

Detailed packages, ports, permitted relationships, and consistency rules are in
`bounded-context-map.md`.

## 5. Roles, authorization, and information boundaries

Roles are default permission bundles, not hard-coded navigation branches.
Effective permission is the union of explicit grants bounded by installation,
workspace, organization, department data, object, row/column, PII, export, and
separation-of-duties ceilings. A deny at any boundary wins. Functional role,
primary organization assignment, and leadership scope are independent.

| Role | Default responsibility | Explicit boundary |
|---|---|---|
| Installation Administrator | installation lifecycle, workspaces, plugins, backup, global policy and suppressed aggregate platform-adoption/capacity statistics | no workspace titles, asset titles, identities, person-level usage, business data or PII without membership |
| Workspace Administrator | membership/roles, connections, workspace policy, report/dashboard access, allowed brand assignment and scoped aggregate-first adoption | no analytical authoring, publication, or PII by default; person-level adoption requires explicit privacy policy |
| Data Steward | catalog, mapping, metrics, methods, Data Guides, data quality | PII, export, waiver approval, and publication remain distinct grants |
| Analyst | analyses, research, metrics/methods, segments, dashboards, reports, requester/executor collaboration, watches, send/export | cannot manage connections, secrets, memberships, roles, or object access grants |
| ML Analyst | forecast/advanced analysis plus permitted analytical authoring | no administrative or PII authority by role alone |
| Operator | runs, retries/cancellation, runtime diagnostics | cannot silently read business data or report content |
| Viewer | explicitly granted non-PII reports/dashboards, comments, likes, follows, activity feed and metric watches | no raw PII, arbitrary artifact download, member export, authoring, or compute |

Authorization occurs before list aggregation, pagination, resource fetch, cache
reuse, preview, render, download, send, and worker access. A denied response
must not reveal the resource title, existence, count, facet, cached content, or
comment thread. Cache and idempotency identities include workspace and effective
policy version. PostgreSQL RLS is defense in depth, not a replacement for the
central policy service.

PII access is a separate purpose-, scope-, and expiry-bound grant available
only under the role ceiling defined by the product specification. Branding,
report authoring, report access administration, report sending, XLSX export,
and comment moderation are independent permissions.

### 5.1 Organization, ownership, and contributor privacy

Identity & Workspace owns the organization model inside the existing modular
monolith. This is not a new deployable service. `OrgUnit` is an effective-dated
workspace tree with `company`, `division`, `department`, and `team` nodes,
inactive/merged lifecycle, and successor mapping. Each active member has
exactly one primary department or team assignment. A leadership assignment
names its unit, whether descendants are included, effective dates, and reason;
it is not a global role.

The authorization decision is computed from these inputs:

```text
functional permission
  AND active workspace membership
  AND organization scope
  AND DepartmentDataPolicyVersion
  AND resource ObjectAccessPolicy
  AND row/column/PII ceilings
  MINUS explicit denies
```

`CrossDepartmentGrant` is an allow-only, reasoned, effective-dated and
expiring exception over a bounded subject/resource/data/action scope. It does
not change the member's primary department and cannot exceed functional or PII
ceilings. This target follows RESOLVED-040 and V1-AC-040. The current grant
API/persistence still permits a null expiry; enforcement needs an explicit
consumer and existing-grant migration decision before changing that boundary.
No default numeric lifetime or indefinite exception is implied.
Every list, count, search, facet, aggregation, pagination, cache hit,
and object action applies the same effective policy before producing output.

Creator and owner are separate. Personal drafts remain principal-owned. New
published reports and dashboards default to the author's primary department;
legacy publications migrate as `workspace_legacy` until audited assignment.
Transfer or deactivation immediately terminates the old department scope,
re-evaluates grants, preserves historical creator attribution, and creates
deterministic handover work for published resources without an active owner.

People & Creators reads `ContributorActivityProjection`, a privacy-safe read
model fed by allowlisted, redacted domain events. It exposes only resources the
viewer can discover and aggregate activity to a safe grain for self, scoped
leaders, or explicit grantees. Raw Audit events, hidden-object counts, peer
rankings, leaderboards, percentiles, and productivity scores are prohibited.
Workspace administration authority does not imply activity, business-content,
or PII read authority.

## 6. Target runtime and trust boundaries

The Foundation runtime is deliberately smaller than the target. The default
Foundation core contains Edge, Web, API, and control PostgreSQL; the demo
profile adds a separate synthetic source PostgreSQL. Valkey, scheduler,
orchestrator, outbox dispatcher, reconciler, workers, report renderer, and mail
delivery appear only when a real vertical slice owns them.

```text
user browser
    | loopback by default; LAN only by explicit policy
    v
Edge infrastructure adapter
    | edge_to_web: Edge + Web only
    v
Web
    | web_to_api: Web + API only
    v
API
    |
    +-- internal control network -------------------------------+
    |  PostgreSQL | Valkey | scheduler | orchestrator          |
    |  outbox-dispatcher | reconciler | scoped workers         |
    +-----------------------------------------------------------+
                  |
                  +-- local immutable artifact store

worker-data   -- allowlisted source egress --> configured source only
worker-report -- allowlisted mail egress   --> configured transport only
Notifications -- v1 allowlisted email/HTTPS webhook egress --> versioned operational endpoint only
update job    -- allowlisted update egress --> approved release origin only
```

Edge is an infrastructure ingress adapter with only read-only installation TLS
key/chain credentials, no domain state and a fixed Web upstream. It is not a
bounded context or product microservice. Issuance/renewal stays outside Edge;
other credentials and certificate-acquisition egress remain forbidden under
ADR-0002 doc_version 2 and runtime contract doc_version 8. Compose does not provide a portable ingress-only network
primitive on Docker Desktop: host publishing requires a non-internal transport
network that may retain ambient outbound routing. Foundation proves separate
`edge_to_web` and `web_to_api` adjacency and negative egress for Web/API; a
fixed Edge upstream is not a firewall. Strict Edge egress denial is a separate
production-hardening gate using a target host firewall or CNI-equivalent policy.

Source, report mail, operational notification email/webhook, update, plugin,
and future identity adapters are distinct trust boundaries. Each has explicit
destination allowlists, secret references, timeouts, retry classes, redaction,
and unknown-state reconciliation. Notifications owns operational delivery;
Report Delivery owns user-initiated report email. Operational email/webhook
adapters are required only for v1 under NOTIFY-008 through NOTIFY-011; public
MVP remains in_app-only. Their process/network composition must preserve the
SEC-006 and no-arbitrary-egress boundaries. Browser
renderers and static chart rendering operate without network asset fetches.

## 7. Primary end-to-end flows

### 7.1. Bootstrap and workspace branding

1. Installation bootstrap uses a host-controlled one-time token over the configured
   protected origin, with local access by default and explicitly configured LAN access.
   It creates one initial account with installation administration and disclosed roles
   in the first workspace; Identity owns the reviewed bootstrap grants. Other workspace
   and PII access are never automatic.
2. The administrator creates a workspace and assigns a permitted CompanyPack
   and BrandProfile version.
3. Identity & Workspace resolves membership, role grants, locale, timezone,
   policy ceilings, and the effective brand binding.
4. Presentation resolves only validated local assets and semantic tokens.
5. Login, Web shell, email, reports, XLSX, and shipped documentation use the
   same pinned corporate identity; publication and rollback are audited.

Brand packages never contain executable templates, remote assets, secrets, or
customer code. A workspace override creates a new version and does not mutate
the installation-approved source pack.

### 7.2. Source onboarding and governed data publication

1. Workspace administration selects PostgreSQL, MSSQL, MySQL/MariaDB,
   ClickHouse, or a published CSV/XLSX template.
2. Connection Catalog validates non-secret configuration and stores only a
   secret reference. Database access is read-only and capability/version aware.
3. CSV/XLSX intake validates media type, sheets, columns, types, locale parsing,
   size/row limits, formulas/macros, duplicates, and rejected rows against an
   immutable `FileImportTemplateVersion`.
4. Ingestion pins acquisition/trigger/readiness policy and the connection/template
   version, resolves compatible source-generation evidence, then stages the declared
   scope under its consistency mode. Daily full rebuilds without row change markers
   use complete-snapshot reconciliation, not a recent-sales watermark shortcut.
5. Artifact Lifecycle commits complete landing manifests/hashes. The control
   transaction advances the successful ingestion checkpoint only with all required
   validation results; a received notification or file part cannot advance it.
6. Data Quality validates schema, duplicates/conflicts, coverage, freshness,
   reconciliation and business rules. Governed remediation can yield an explicit
   degraded eligible subset while preserving canonical invariants.
7. Semantic Model publishes immutable mappings, metrics, formats, filters, and
   capabilities only with visible validation and downstream impact.
8. Data Guide publication exposes safe source labels, grain, definitions,
   quality, limitations, and lineage without DSNs, hosts, secrets, or denied PII.

The [source data adaptation contract](../contracts/source-data-adaptation-contract.md)
allocates INGEST-008 through INGEST-020, DATA-MAP-001 through DATA-MAP-007,
IDENTITY-006 through IDENTITY-008 and DQ-INPUT-001 through DQ-INPUT-008. Platform
pull, source push and notification-triggered pull use the same governed path.
Transport completeness is independent of business-history completeness. Source
rekey uncertainty, old corrections, reassignment and absence policy remain
visible; validated changes update affected old/new projections, preserving prior
published results. String flags and SP/is_lk channel rules compile through the
shared semantic model. No new service or second ingestion truth is introduced.

Yandex Metrica remains a future connector boundary. Reporting API and Logs API
would require different capability, provenance, sampling/privacy, and freshness
contracts; no credential UI or runtime dependency is active in v1.

### 7.3. Governed research to analytical product

1. An Analyst opens an `AnalysisCase` with a business question, intended
   decision, owner, audience, priority, and due date.
2. The case pins an approved `AnalysisMethodVersion`, dataset/metric versions,
   filters, history requirements, quality checks, and limitations. An explicitly
   marked unregistered method is permitted only with review and limitation.
3. Analytics produces immutable result artifacts with result identity derived
   from inputs, normalized filters, comparison, code/specification, and policy.
4. The Research Workspace composes narrative, metric groups, charts, tables,
   methodology, Result Trust, findings, and conclusions from those artifacts.
5. A `FindingVersion` pins evidence, scope/filters, strength, limitations,
   author, and reviewers. A comment cannot become a finding automatically.
6. Review publishes an immutable research version and optional dashboard,
   report, segment, forecast, or saved analysis through Presentation ports.
7. Collaboration & Adoption ties comments, mentions, likes and subscriptions to
   a specific authorized resource version/snapshot and block; access revocation
   hides the thread, reaction, feed event and future notification.
8. A decision record links accepted findings and follow-up without mutating the
   underlying analytical evidence.

This flow is the architectural replacement for one-off notebook/Excel analysis:
the output is reusable, searchable, permission-aware, and reproducible.

### 7.4. Analytics, comparison, promotions, and forecasting

Every reportable analysis uses a versioned `AnalysisSpec`, immutable source
artifacts, semantic/filter versions, DQ evidence, and `TimeComparisonSpec`.
Comparable prior-year behavior is a universal result contract, not local chart
logic. Both periods independently pass history, quality, permission, currency,
and definition checks.

Promotion Journal supplies immutable descriptive time ranges by channel and
audience/client scope. Its `range_timeline` overlay does not claim causal lift;
causal or experimental conclusions require an explicit approved methodology.

Forecasting owns time-series construction, features, temporal backtests, model
registry, prediction intervals, monitoring, and degradation. It consumes pinned
semantic/DQ/artifact references and publishes forecast artifacts; it cannot
silently read Analytics private tables or rewrite observed actuals.

#### 7.4.1. Component discount, cap, and price-volume-mix

1. Semantic Model publishes ReceiptItem field roles and an immutable effective
   `DiscountPolicyVersion`: component catalog, attribution bindings, stacking
   matrix, precedence, accounting treatment, base-price/cap definition,
   tolerance, returns, and breach actions.
2. Ingestion preserves source values. Data Quality validates field coverage,
   reconciliation, impossible stacking, and historical cap breaches; it never
   silently clamps a sale or invents a missing component.
3. Analytics normalizes promotion, loyalty, bonus redemption, and other rows in
   a line-grain component fact. Bonus accrual remains outside this fact.
   Commercial discount, customer benefit, and recognized net revenue are
   distinct measures with explicit attribution mode and coverage.
4. Historical cap violations remain immutable evidence and may degrade/block
   trusted analysis by policy. Simulation or prescriptive publication above the
   cap is rejected before artifact commit.
5. Promotion Journal can supply an optional exact `PromotionVersion` reference
   and descriptive overlay. A date overlap alone never creates sale-level promo
   attribution or a causal claim.
6. A versioned PVM specification pins method/order, periods, product identity,
   metrics, currency, returns, assortment/missing-price policy, and tolerance.
   Price, volume, mix, assortment, and residual must reconcile to observed
   change before a trusted result is committed.
7. Presentation consumes reportable component/PVM result ports and exposes
   policy, attribution, coverage, breaches, formula order, residual, and
   limitations through Result Trust, email, and XLSX. It does not recalculate
   or reattribute browser data.

Semantic Model owns reusable field/metric/policy meaning. Analytics owns fitted
attribution diagnostics, decomposition specifications/results, and result
identity. Data Quality owns evidence, not business reclassification. Promotion
Journal owns event context, not observed sale mechanics. Methodology & Research
owns evidence-strength guidance and future-method availability, not result
calculation.

#### 7.4.2. Governed population treatment and segmentation

1. An analysis or segmentation pins an eligible population, feature versions,
   filter policy, DQ evidence, PII ceiling, and a versioned
   `PopulationTreatmentSpecVersion`.
2. Quantile, IQR, or MAD treatment is fitted on the declared reference
   population. The default action is `flag`; `exclude` and `winsorize` require
   explicit author intent and preserve affected-row diagnostics.
3. The same fitted bounds are reused for current and `vs LY` comparison periods
   unless the specification explicitly declares a different governed policy.
   This prevents the comparison population from drifting through independently
   fitted thresholds.
4. The platform previews counts, shares, metric deltas, protected/high-value
   cohort impact, and minimum-population warnings before publication. Outlier
   treatment remains an analytical choice, not an automatic DQ correction.
5. A versioned segmentation definition uses the declared rule, RFM, bucket,
   KMeans, curated, or composition method. KMeans keeps an explicit final K.
   Stratified distribution is a DistributionArtifact within AnalysisVersion
   by default; explicitly saving a selected cell creates a segment definition
   with source lineage (SEGMENT-007/010). Bucket and stratum boundaries,
   inclusivity, null/overflow policy, labels, and ordering are deterministic.
6. KMeans pins feature order, transformations, scaling, missing-value policy,
   requested `K`, initialization, seed, implementation version, fitted model,
   quality diagnostics, and empty/small-cluster behavior. Training and later
   assignment are distinct operations.
7. Publication commits immutable definition/model and membership snapshots with
   lineage. Reports, research, email, and XLSX expose the treatment/method/model
   identity, population impact, and limitations through Result Trust.

Heavy previews and fits use Execution Control and Artifact Lifecycle. The Web
client configures and visualizes them but does not fit bounds or clusters.

### 7.4.3. Relational populations and compact analytical authoring

The owner-approved 2026-09-05 requirements extend the existing Analytics and
Presentation responsibilities through the
[governed authoring contract](../contracts/analytical-authoring-contract.md).
FILTER-013 through FILTER-018 define typed relationship scopes, aggregates,
sequences, unknown/completeness semantics and bounded backend plans.
SEGMENT-029 through SEGMENT-037 add customer collections/composition,
inclusion explanation, selection/event/fixed-cohort time and evidence-linked
selection. Existing customer snapshot keys and immutable history are retained.

Analytics owns PivotSpec/PivotResult, correct full-population totals and cohort
cell states. Presentation owns compact table-first composition, parameter
bindings, explicit reader/explorer/author modes and semantic-diff presentation;
the producer owns the result evidence behind the diff. Parameters and expanded
period/population comparisons enter normalized identity, while density and
already resolved display order do not. Related-object filtering never becomes
an arbitrary join or browser calculation. Digital Measurement supplies public
event projections; generic Execution controls work and does not own operators.

Old definitions remain readable under their original schema. New filter and
comparison modes require version dispatch, resolved dependency identity and
reader-before-writer rollout. The contract records unknown runtime/persistence
compatibility, rollback constraints and synthetic acceptance witnesses; none
is inferred complete from documentation. The implementation order is bounded
customer rules and a compact matrix report, followed by dependent capabilities.
Temporal sequences and event-time reporting wait for real history providers.

### 7.5. Dashboard, report, email, and XLSX

1. Presentation composes stable chapters, pages, sections, and typed blocks
   into one `AnalyticalDocumentVersion`; dashboard, workbook-report, and
   narrative-research are profiles, not separate block engines.
2. The common builder compiles guided or advanced authoring into one normalized
   block definition after capability, permission, trust, cost, freshness, and
   reuse preflight.
3. Publication resolves hierarchy, effective filter scopes, segment bindings,
   required block artifacts, locale/timezone, brand, theme, and renderer into
   one atomic root snapshot with page manifests. ReportSnapshot remains a
   compatibility/report-lifecycle projection over that root.
4. A viewer receives an authorized page index and mounts only the active page;
   bounded prefetch cannot count as adoption or reveal denied metadata.
5. Web, accessible data-table alternatives, email, and XLSX consume the same
   root/page snapshots and result artifacts. DOM scraping, channel-specific
   calculations, and dual-write composition are forbidden.
6. ECharts is the only v1 Web chart engine. Email uses PNG produced by a
   network-disabled SSR SVG pipeline. XLSX uses a lossless native chart when
   possible and the same PNG fallback otherwise, always retaining typed data.
7. User email is an explicit authenticated action. Sender identity, recipient
   domain allowlist, report/source access, PII/DLP policy, and transport
   authorization are rechecked before render and submit.
8. Unknown provider result enters reconciliation; blind retry is forbidden.
9. Universal XLSX preflight checks Excel limits, memory/temp disk, sheet count,
   charts, and final size. It produces README, Contents, Summary, typed data
   sheets, charts, and Metadata/Lineage without silent truncation.
10. README derives from the snapshot, Data Guide, Methodology Registry, and safe
   catalog metadata and explains purpose, freshness, filters, comparison,
   metrics/groups, grain, quality, limitations, lineage, author, and versions.

`NumberFormatSpec` and `MetricGroupVersion` are shared contracts across Web,
email, chart labels, and XLSX. Computation uses raw typed values. Compact display
never converts a non-zero percentage into visible zero, and XLSX data cells stay
numeric with native formats and an accessible path to full precision.

### 7.6. Asynchronous execution and recovery

1. API persists the command/run and outbox intent in one PostgreSQL transaction.
2. Dispatcher delivers a versioned task with workspace, actor, policy, input,
   resource profile, attempt, and idempotency identity.
3. Worker acquires a lease/fencing token, writes staging artifacts, and emits
   bounded progress, ETA/confidence, heartbeat, and safe status.
4. Artifact commit and terminal run state become authoritative only through
   durable manifests and PostgreSQL state transitions.
5. Reconciler repairs lost delivery, expired leases, orphan staging, aggregate
   state, and external unknown outcomes.
6. UI preserves the previous result during refresh and shows freshness/loading
   at the affected block; cancellation is an explicit state transition.

### 7.7. Materialization and compute reuse

1. A consumer submits a normalized semantic/result specification, policy
   version and immutable input hashes to Execution Control.
2. Semantic Model confirms exact aggregate compatibility; the planner selects
   the smallest fresh authorized artifact when one exists.
3. A miss acquires a single-flight claim by reuse key. Concurrent identical
   requests wait for the same fenced execution instead of duplicating work.
4. The worker uses Polars/DuckDB over local Parquet, then Artifact Lifecycle
   atomically commits the result, manifest, hashes and dependency references.
5. Source correction or policy/spec/code change invalidates only affected
   partitions/descendants; policy revoke blocks reuse even if bytes remain.
6. Predictable heavy refresh runs after ingestion or in configured off-peak
   windows. Interactive, precompute and maintenance lanes have explicit
   priority and bounded fairness.
7. Web, email, XLSX and API consume the same immutable artifact. Last-good
   serving is explicit and exposes freshness/revalidation/limitation.

### 7.7.1. Scheduled document refresh and prepared serving

The owner-approved 2026-09-06 amendment is allocated in
[Report refresh, prepared serving and recovery, version 1](../contracts/report-refresh-serving-recovery-contract.md).
Every supported document profile has a refresh setting; new working reports
and dashboards default to after-ingestion, while research/pinned publications
remain manual/pinned. A due occurrence without fresh compatible data persists
as waiting demand. Pending work coalesces without losing final input changes.

Presentation owns stable document/definition/snapshot/current references and
refresh intent; Execution Control owns schedules and execution through public
ports. Artifact Lifecycle owns durable placement and committed manifests.
No third publication authority or independent report scheduler is introduced.
A complete new root is published with policy/definition revision, fencing and
monotonic generation checks, so an older late completion cannot regress current.
An active viewer explicitly adopts updates; new ordinary opens resolve current
and historical links retain exact snapshots.

Result integrity, freshness and refresh attempt state remain separate. A failed
refresh can coexist with an authorized valid last-good snapshot. Prepared reads
serve bounded active-page values, with no equivalent source-history rescan.
The mixed-load target includes up to 50 active authors and 100 viewers plus
background refresh under shared CPU/memory/IO admission. Numeric latency and
freshness budgets, hardware and data volume remain unresolved acceptance inputs.

### 7.8. Cross-channel acquisition and unit economics

1. Governed connectors/imports publish versioned web/app events, sessions,
   marketing touches, spend and business-cost facts with taxonomy, consent,
   currency, time and provider provenance.
2. Digital Measurement applies only deterministic, versioned identity links;
   anonymous and unresolved traffic remains measurable without forced merge.
3. Digital facts join canonical offline purchases/refunds through an explicit
   grain/key/time/cardinality and reconciliation contract.
4. Attribution pins model, windows, conversion, touch eligibility and identity
   version. Provider-reported, platform and independently observed credit remain
   separate; attribution is not causal or incremental evidence.
5. Unit-economics specifications publish governed CAC/CPI/CPA, ROAS/ROI, LTV,
   contribution-margin and payback results with cost allocation, FX, cohort,
   maturity, refunds, residuals and certification status.
6. Targets, budgets, allocations and scenarios are immutable reviewed inputs;
   they never overwrite actuals or authorize campaign/source writeback.

### 7.9. Product, category, assortment, and inventory analytics

1. Ingestion commits versioned inventory, availability, price, and planned
   assortment source facts without converting missing values to zero.
2. Semantic Model publishes the effective product hierarchy, assignments,
   store clusters, and assortment-scope meaning for the requested time.
3. Analytics pins that hierarchy version or an explicit rebase and produces
   reconciled category/SKU, assortment, sell-through, inventory-turnover,
   stockout/availability, ABC/XYZ, pricing/markdown, lifecycle, affinity, and
   descriptive-substitution results.
4. Zero sales cannot prove stockout; substitution cannot become a causal claim;
   missing required facts produce capability blockers with the next data input.
5. Presentation consumes the same result projection through the common block
   contract, so product analysis can be reused in documents, forecasts, and
   segment definitions without copying computation.

## 8. Canonical contracts and ports

| Boundary | Owner and rule |
|---|---|
| Browser to API | OpenAPI, stable error envelope, generated TypeScript client, bounded pagination/sort/filter allowlists |
| UI route identity | `ui-routes.json` owns ID, canonical path, title key, release, and route implementation lifecycle metadata |
| UI route execution | `ui-route-contracts.json` owns family, shell, guards, roles/permissions, state and history profiles, dirty/focus behavior, source requirements, and design synchronization |
| UI surface coverage | `ui-surface-contracts.json` owns the current route/overlay/system/capability inventory, route-decision policy, legacy design provenance, and exact `UC-001...UC-029` bindings; it is not the future all-screen atlas |
| Analytical-document composition | Presentation-owned schema-v2 hierarchy, filter scopes, normalized block references, root/page manifests, and active-page projection; no generic shared kernel or dual-write |
| Segment evaluation | Analytics-owned reusable definition, time-bound run/evaluation, immutable snapshot, and explicit pinned/latest-successful binding; member access remains separate |
| Product analytics | Semantic hierarchy/assortment contracts plus ingestion facts and Analytics result ports; history, missingness, and reconciliation are explicit |
| Organization | `OrganizationStructureVersion`, membership/leadership assignments, department data policies, cross-department grants, ownership bindings, and effective-access explanation ports owned by Identity & Workspace |
| Contributor insights | Redacted `ContributorActivityProjection` owned by Identity & Workspace; Audit is an input event source, never the employee-analytics query store |
| UI contract validation | Portable JSON Schemas plus the repository validator enforce route parity, permission/localization integrity, surface references, and complete product use-case coverage |
| Draft mutation | ETag/`If-Match`; stale mutation returns the current revision conflict |
| Repeatable command | workspace/actor/route-scoped idempotency key plus payload hash |
| Long operation | `202 Accepted`, run/operation ID, status URL; no HTTP wait for heavy compute |
| Execution delivery | versioned task/event, at-least-once, attempt identity, lease/fencing, retry classification, reconciliation |
| Compute reuse | normalized reuse key, logical compatibility decision, single-flight claim, immutable dependency graph, freshness/serving policy and resource lane |
| Source connector | versioned `SourceConnector` port with read-only policy, capabilities, consistency, limits, secret reference, and integration evidence |
| Bulk result | immutable artifact manifest/hash/schema/grain/key/lineage/PII; bounded JSON is control metadata only |
| Metric presentation | versioned NumberFormatSpec and MetricGroupVersion; formatting never changes analytical identity |
| Metric trust | lifecycle-independent certification record plus direct/policy-derived/residual origin, coverage, reference evidence, replacement, and limitations |
| Discount policy | immutable effective `DiscountPolicyVersion`; component catalog, stacking/precedence, accounting, cap, rounding, returns, and breach behavior |
| Discount result | line/component fact plus reconciliation/coverage/cap diagnostic ports; no implicit zero, clamp, or Promotion-Journal inference |
| Price-volume-mix | versioned method/order and exactly reconciled price/volume/mix/assortment/residual result port |
| Research | immutable method/result/finding bindings; discussion is owned by a separately authorized collaboration context |
| Collaboration/adoption | exact asset/version/block binding, idempotent like state, meaningful-view semantics, permission-filtered feed, privacy-safe aggregates and versioned watch |
| Digital measurement | versioned event/touch/spend/cost/identity/attribution/unit-economics/assumption contracts; provider, observed and causal claims remain distinct |
| Population treatment | versioned PopulationTreatmentSpec, fitted parameters, action, diagnostics, sensitivity result, and stable comparison policy |
| Segmentation | versioned rule/bucket/stratification/cluster specification plus immutable model and membership snapshot identities |
| Visualization | validated product-owned ChartSpec; compiler adapters reject code, callbacks, raw options, and network assets |
| Report | immutable ReportSnapshot pins data/result/presentation/brand/locale identities before rendering |
| Email | ReportDeliveryPort with sender/domain policy, idempotent submit, durable encrypted locator, and unknown-state reconciliation |
| XLSX | XlsxRendererPort with deterministic preflight, typed sheets, universal README, openability/fidelity gates |
| External side effect | explicit adapter, destination allowlist, secret reference, timeout/retry classes, audit, and unknown-state rule |

The UI contract set has three layers. The compact identity registry protects
stable URL/localization consumers. The executable route manifest carries page
policy without bloating that identity layer. The surface coverage manifest
prevents a false-completeness result where two route lists agree but a product
use case has no designable surface. Single atomic manifests were selected over
per-route files so agents and validators can load and cross-check the complete
navigation and coverage graph without directory traversal.

## 9. Route and Web execution model

The current inventory contains 117 route-level pages, 25 typed overlays, and 5
system surfaces, including planned UI-AN-015 Products. W03-W10 evidence records
the earlier `116/25/5` boundary and is preserved as historical provenance. It is not an accepted target, a complete
product coverage model, a visual authority, or browser/authorization runtime proof.
A standalone route is required for a durable/versioned lifecycle, deterministic
deep link, independent Back/refresh/dirty/recovery semantics, or sufficiently
complex permission boundary. Transient confirmations and inspectors remain
overlays; repeated governed behavior remains a shared capability.

Routes belong to four families: public/auth, global user, installation, and
workspace. Workspace resources use `/w/:workspaceKey/*`; `workspaceKey` is an
immutable opaque locator and never authorization proof.

The route contract resolves each page to:

- canonical path and family;
- application shell and navigation group;
- allowed role hints and required permission alternatives;
- authentication, workspace membership, capability, object access, and
  installation/workspace policy guards;
- safe query/history behavior, deep-link policy, and `returnTo` handling;
- required first-load, empty, ready, refreshing, partial, forbidden, failed,
  stale, and dependency-unavailable states as applicable;
- dirty-draft navigation guard and Focus/Explore return-to-origin behavior;
- source requirement IDs and the authoritative UI blueprint row;
- route implementation lifecycle metadata and legacy design-provenance status.

Role hints control discoverability but never authorize data. The API repeats
policy checks before fetch/action. Forbidden functions are hidden or explained
without disabled-control ambiguity; denied resource metadata is never cached or
rendered. Route changes preserve the shell, update title/breadcrumb/location,
and restore declared focus/scroll. Safe query state is allowlisted; raw PII,
secrets, source values, and unredacted filters never enter the URL.

Focus/Explore is route-backed through an allowlisted `focus` key, not a nested
modal. Close, Escape, and Back restore origin route, block, scroll, and keyboard
focus. Dirty editors guard sidebar navigation, workspace switch, browser Back,
reload, and close with Stay/Discard/Save Draft where supported.

### 9.1. Product-wide Web UI target boundary

ADR-0007 pins the current responsive-Web frontend stack, package ownership,
state/query boundaries, styling system, and browser evidence expectations for
ticketed production implementation. Current implementation work follows
`docs/architecture/ui/custometry-web-implementation-source-contract-v1.md` and
one ready ticket at a time.

The final interactive pilot in `docs/architecture/ui/target-pilot/` is the
accepted target UI concept, including its demonstrated composition and
behavior. The G-program was removed by owner decision on 2026-09-04; its
historical record remains recoverable through `ui-program-retirement.md`.
Existing production UI and backend contracts are preserved. Conformance and
remaining product coverage are subsequent ordinary implementation tickets.

The technology-neutral browser dependency direction remains:

```text
screen + route + shell composition
        |
        +--> presentation/client state
        |      navigation, drafts, focus origin, local preferences,
        |      reversible optimistic feedback
        |
        +--> typed server-state/API/event adapter
               authoritative snapshots, invalidation, cancellation
                        |
                        v
                 existing application/API contracts
```

The browser cannot authorize an action, manufacture terminal run/report/
delivery state, persist a domain result, or replace reconciliation. The chosen
frontend stack must keep this dependency direction, consume versioned typed
contracts, preserve workspace isolation and safe URL/history semantics, and
resolve theme/white-label presentation through accepted semantic tokens and
validated assets.

The current `117` routes, `25` overlays, `5` system surfaces, and `22`
cross-surface capabilities are current-state inventory evidence, not the future
all-screen atlas or a permanent ceiling. Historical Penpot metadata remains
traceability only and cannot close a current design or browser gate.

Performance evidence must separate input feedback, client dispatch,
network/API wait, response/event-to-paint, and final interaction latency.
Journey performance budgets require the applicable accepted baseline and
measured evidence. This does not discard the still-normative motion token and
duration requirements in product blueprint section 15.10 (MOTION-001..012);
changing those obligations requires an explicit synchronized product decision.
Historical design thresholds alone do not create new performance authority.

## 10. Persistence, versioning, and consistency

PostgreSQL is authoritative for identities, policies, definitions, versions,
runs, schedules, reuse/dependency metadata, outbox, delivery state, and audit.
Valkey carries tasks, ephemeral locks, single-flight coordination and bounded
small caches only. Bulk facts, marts, materializations and results are immutable
local Parquet/derived artifacts with manifests and hashes.

Published datasets, semantic definitions, methods, findings, dashboards,
reports, brands, company packs, organization structures, department data
policies, ownership bindings, templates, population-treatment specifications,
segment definitions/models/membership snapshots, forecast models, and promotion
windows are immutable versions. Participant bindings/history, watch definitions,
event taxonomies, attribution/unit-economics specifications, governed assumption
tables and materialization definitions follow the same version/pinning rules.
Discount policies, certification records,
component-attribution/reconciliation results, PVM specifications, and PVM
results follow the same version/pinning rules. Editing creates a draft/revision; publication
creates a new version and downstream impact. Archive/deprecation preserves
lineage and replacement references. Closing a case or deleting a comment does
not mutate published evidence.

State transitions that must remain atomic use one context-owned PostgreSQL
transaction. Cross-context durable handoff uses outbox/event delivery. A
consumer records idempotency and must tolerate duplicates. Strong consistency
is used for permission and publication decisions; projections expose explicit
freshness for search, impact, notification, and read models.

### 10.1. Publication durability and coherent recovery

REPORT-REFRESH-001 through REPORT-REFRESH-007, ARTIFACT-COMMIT-001 through
ARTIFACT-COMMIT-003 and OPS-009/010 are allocated in the
[version 1 refresh/recovery contract](../contracts/report-refresh-serving-recovery-contract.md).
Durable immutable file placement precedes PostgreSQL publication. Unknown
commit outcomes and orphan cleanup reconcile through owner ports with fencing,
reference and retention checks; rename alone is not power-loss evidence.
Cross-context handoffs do not become direct private-table transactions.

V1 keeps one local live artifact volume while supporting coherent backup
outside the primary server. The administrator configures the daily-evening
time/timezone, destination and retention. A restore point binds PostgreSQL,
referenced artifacts, keys and deployment metadata; restore proof reproduces
exact snapshots. A configured schedule does not establish a successful copy,
a numeric RPO/RTO or observed recovery. Fault and restore drills remain required.

## 11. CPU, performance, and capacity

All analytical, forecasting, reduction, static rendering, and XLSX workloads
execute on CPU. The platform detects available cores and uses the effective
minimum of detected capacity, installation cap, workspace policy, queue limit,
and operation request. The administrator may reduce capacity but cannot exceed
detected/declared safe limits.

Vectorized Polars/DuckDB/NumPy-first paths are the default. Quantile/IQR/MAD
diagnostics, bucket/stratum assignment, feature transforms, and KMeans fitting
must use bounded vectorized CPU paths and reproducible benchmarks. Numba is permitted
only for measured numeric kernels with reproducible correctness and performance
evidence. Python object loops, browser computation, or chart-library aggregation
cannot be called optimized merely by convention; benchmarks and representative
profiles establish the claim.

Heavy operations require preflight for rows, columns, artifacts, memory, temp
disk, cores, queue, estimated duration, and output limits. Progress has phase,
processed/total where meaningful, ETA with confidence, heartbeat, cancellation,
and stable terminal errors. Normal demo and benchmark profiles remain separate.

Performance begins with avoiding work, not only accelerating kernels. The
planner reuses the smallest exact-compatible materialization, coalesces
concurrent same-key demand, refreshes predictable heavy artifacts after
ingestion/off-peak, and invalidates dependency partitions incrementally. Its
telemetry records hit/miss, coalescing, avoided scans/bytes/CPU, wasted
precompute, refresh latency, staleness and eviction. Benchmarks separately cover
cold, warm, hot, concurrent same-key, invalidation and resource-lane contention;
a static architecture claim is not runtime performance proof.

## 12. Reliability, security, and operations

- Every external side effect defines authority, destination, idempotency,
  timeout, retry classes, unknown state, reconciliation, retention, metrics,
  audit, and redaction.
- Liveness, dependency readiness, application readiness, data readiness, and
  business-enabled status are distinct signals.
- Secrets enter through files/references only and never URLs, logs, traces,
  diagnostics, manifests, Data Guides, XLSX README, or examples.
- Previews, list/count/search, exports, chart data, and logs apply policy and PII
  redaction before pagination/aggregation or serialization.
- Markdown, email HTML, ChartSpec, file uploads, workbook cells, plugins, source
  identifiers, and archive paths have explicit injection/sandbox limits.
- Backup/restore, migrations, browser flows, connector compatibility,
  accessibility, recovery, performance, supply chain, and release have separate
  evidence gates.
- Operator actions do not grant silent business-data access; support access is
  explicit, time-bound, purpose-bound, and audited.
- Screenshot fidelity is not browser or performance evidence. Authenticated
  golden slices require real-browser interaction, accessibility, console,
  network, and measured response-to-paint proof on the declared hardware.
- No client-side store or cache becomes authority for server state, access
  decisions, versions, or freshness. A typed API/event adapter remains the
  server-state seam independent of the selected frontend stack.

## 13. Documentation, distribution, and private boundary

Markdown in Git is the authoring source. The ordinary installation publishes
only allowlisted user/install documentation under `docs-site/docs/**`. MkDocs
Material serves offline-capable `/docs`; authenticated `/help` uses the same
generated, permission-aware index plus permitted Data Guides. Architecture,
ADRs, tickets, evidence, prompts, and journals are excluded from the customer
installation.

The current distribution model is self-host only. The launcher downloads
digest-pinned images/assets, verifies them, and starts the supported topology.
An air-gap export, updater, public registry, signing/provenance, and additional
platform packaging may be added later without introducing a managed customer
data plane.

The public repository contains only the future activation boundary and safety
properties necessary for compatibility with immutable SegmentSnapshot and
identity contracts. Destination code, commercial entitlements, pricing,
private roadmap, and private delivery artifacts must live in separately
access-controlled storage. `.private/` is ignored only as defense in depth and
is not a confidentiality control. Public report email/XLSX/CSV/Parquet delivery
must never depend on a private activation package or license heartbeat.

## 14. Dependency-ordered implementation direction

This is a dependency constraint, not a standing program plan:

1. repository, security, runtime, documentation, route, and contract Foundation;
2. identity/workspace policy, connectors/templates, artifacts, execution, DQ,
   semantic model, organization/access foundation, and deterministic demo data;
3. reportable analytics with universal comparison, governed population
   treatment, reusable segment definitions/runs/snapshots, product hierarchy and
   inventory/availability facts, deterministic bucket/stratified segmentation,
   component discount reconciliation/cap/PVM, Result Trust, charts/tables, and
   complete route/browser states;
4. materialization/reuse planner, methodology availability/packs, metric
   certification/proxy quality, representativeness/robustness,
   common analytical-document schema-v2 and root/page snapshots,
   research/findings, notes/annotations/discussions, collaboration/adoption/
   watches, dashboards/access, product/category/assortment analytics,
   organization/People projections and ownership handover, promotions,
   forecasting, report composition, branding, and email;
5. canonical digital events/touches/spend/cost, versioned identity resolution,
   campaign/journey/cost reconciliation, attribution, unit economics, governed
   assumptions, journey/funnel results and acquisition-scope separation,
   pipeline builder, exact-K KMeans segmentation, operational hardening,
   connector matrix, recovery, capacity, accessibility, and supply-chain proof;
6. universal XLSX only after reportable block contracts and snapshot semantics
   are stable;
7. final v1 acceptance at real browser/API/PostgreSQL/artifact/Compose/recovery/
   performance/release boundaries.

One ready delivery ticket remains one execution unit. A specification is added
only when behavior or proof remains unresolved; plans, ledgers, and reusable
prompts are exceptional rather than standing inventory.

## 15. Compatibility, migration, and rollback

| Surface | Classification | Migration and rollback |
|---|---|---|
| Product specification projection | compatible before first stable consumer | architecture docs can roll back together only if normative requirements remain represented elsewhere |
| Authenticated frontend target | accepted responsive-Web platform | ADR-0007 pins the current stack; rollback requires a replacement ADR while preserving backend contracts and the last accepted browser boundary |
| Presentation registry | accepted current platform ownership | `packages/ui-foundation` owns current tokens, primitives, components, and responsive behavior; target-pilot conformance changes migrate through versioned implementation tickets |
| Dashboard/research/report composition shapes | breaking target schema-v2 change | add common composition DTO and legacy read adapters, backfill stable hierarchy IDs, move new drafts to v2, and prohibit dual-write or lossy rollback |
| Report snapshot | compatible first migration step | add root/page manifests while preserving legacy reads; all channels switch together before retiring the old resolved-block projection |
| Organization/access persistence | compatible target addition before stable consumers | create versioned units/assignments/policies/grants/ownership/projection tables, backfill one primary department, migrate legacy publications to `workspace_legacy`, and fail closed until invariants pass |
| Organization/People routes | additive current-inventory evidence | the six route IDs remain in current route contracts; future implementation tickets complete unshown states while preserving accepted target-pilot composition, product meaning and stable route compatibility |
| Discount component/policy/PVM contracts | compatible target addition before persistence consumers | rollback disables new publication/UI capability but preserves imported source fields and pinned immutable results; later schema migration requires owner-context up/down proof |
| Metric certification/method availability | compatible target addition | lifecycle remains intact; rollback hides the new projection but cannot relabel or delete historical evidence |
| Population-treatment contracts | compatible target addition | versioned specs/results migrate atomically; rollback disables new publication but preserves pinned results |
| Segment membership identity | breaking persistence/key migration | backfill stable segment snapshot IDs, keep a legacy-reference map and all historical memberships, and resolve pinned/latest bindings explicitly |
| New Methodology & Research context | compatible target addition | create owner package/tables/contracts before consumers; rollback disables unpublished capability but preserves immutable published references |
| Collaboration & Adoption context | compatible target addition | migrate existing comment ownership before new reactions/views; rollback disables new projections but preserves discussion and audit history |
| Digital Journey & Marketing Measurement context | compatible target addition | add canonical contracts before provider adapters; rollback stops new publication but preserves immutable event/spend/result lineage |
| Product/category/inventory facts and analytics | compatible target addition | add hierarchy/fact/result contracts before surfaces; rollback stops new publications but preserves imported facts and pinned history |
| Materialization/reuse contracts | compatible target addition before persisted consumers | invalidate by versioned reuse identity; rollback disables planner reuse but never treats stale or policy-incompatible bytes as valid |
| Executable route contract | compatible addition; future schema changes versioned | identity registry stays v2; route contract starts v1, requires one-to-one validation, and must support deterministic schema migration |
| UI surface coverage contract | compatible target addition; future schema changes versioned | use-case bindings and route/overlay/component rationale migrate atomically; rollback cannot remove the only UI coverage for a normative use case |
| Existing route URLs | no change | renamed stable paths later require redirects, deprecation, telemetry, bookmark migration, and rollback |
| Object access/comments | compatible target addition | access policy version and comment thread binding migrate before UI exposure; revoke fails closed |
| BrandProfile/CompanyPack | compatible target addition | system/default identity remains fallback; invalid or revoked version rolls back to last valid pinned version |
| Number formats/metric groups | compatible target addition | raw typed values remain unchanged; clients migrate to versioned display contracts and can fall back to safe system formats |
| CSV/XLSX template import | compatible connector addition | template version pins accepted shape; rollback stops new intake without deleting committed artifacts |
| Public/private distribution split | compatible restriction | public package/SBOM/route graph gates reject private implementation; rollback cannot expose private artifacts |
| System Design publication format | compatible documentation simplification | keep Markdown as the sole maintained source; generate non-authoritative presentation exports only for a named external handoff |

No runtime or persistence migration is claimed by this documentation increment.
Every implementing ticket must classify API, schema, configuration, identity,
cache, side effect, browser, migration, rollback, and performance impact against
the then-current consumers.

The retired Linear/Penpot direction and removed G-program are not alternative
implementation paths. Current Web execution is ticket-first, using the accepted
target pilot, product/UI requirements, and ADR-0007. The cleanup does not claim
that the working frontend already matches the concept or implements all screens.

## 16. Proof boundaries and acceptance

This document records accepted architecture and declared traceability to product
specification `0.11.0-draft`; its existence does not prove internal consistency.
Static validation establishes only the checks actually observed, such as:

- route identity/execution/surface-contract/schema/localization/UI-blueprint parity and exact product use-case bindings;
- requirement IDs and documentation links;
- declared package/dependency rules;
- discount/methodology ownership, port, and executable UI binding agreement;
- collaboration/digital-measurement/materialization ownership and requirement parity;
- organization/access/ownership/contributor-projection ownership and complete
  route/capability binding agreement;
- absence of maintained binary mirrors that could drift from the Markdown
  architecture authority.

It does not prove implemented routes, permission enforcement, database schema,
connector compatibility, browser behavior, chart/email/XLSX fidelity, Compose
runtime, recovery, performance, security hardening, supply chain, or release.
Those require observation at their real boundaries.

The primary architectural risks are:

1. treating a generated mock or planned route as implemented product behavior;
2. letting the shared PostgreSQL deployment become cross-context table access;
3. allowing role hints or workspaceKey to replace authorization;
4. diverging calculations/formatting between Web, email, and XLSX;
5. turning comments into unreviewed findings or descriptive promotion overlap
   into causal inference;
6. introducing customer forks through branding or private code into the public
   package graph;
7. claiming ingress-only Edge networking from Compose where it is not portable;
8. starting XLSX or advanced pipelines before report/result contracts stabilize;
9. silently removing high-value or protected populations as “outliers” without
   visible sensitivity evidence;
10. changing bucket boundaries, KMeans seed/features, or assignment semantics
    without a new immutable version and stable membership identity.
11. averaging row discount rates, double-counting stacked components, clamping
    historical breaches, or presenting residual attribution as direct evidence;
12. publishing a non-reconciled PVM or advertising a future methodology as a
    runnable v1 capability.
13. encoding departments into roles or allowing a cross-department grant to
    exceed role/PII ceilings;
14. exposing hidden members/resources through contributor counts or treating
    raw Audit as an employee-analytics database;
15. losing published-resource ownership or retaining old department access
    after a member transfer or deactivation.
16. turning adoption into employee ranking or leaking hidden activity through
    installation-wide counts;
17. serving stale or unauthorized cache entries after policy/source changes, or
    allowing precompute to starve interactive work;
18. over-merging digital identities, treating missing spend as zero, or
    presenting attributed revenue as causal incrementality.

## 17. Considered alternatives

| Decision | Rejected alternative | Reason |
|---|---|---|
| Three-layer UI contract set | put identity, policy, and coverage in `ui-routes.json` | couples lightweight consumers to policy churn and still cannot express complete route/overlay/system/capability coverage cleanly |
| One route contract file | one file per route | makes atomic coverage, ordering, schema migration, and agent loading harder without a current ownership benefit |
| Modular monolith | microservices from the start | raises deployment, failure, migration, and observability cost before independent scale/release boundaries exist |
| Product Methodology/Research context | leave research as dashboard prose | cannot govern methods, evidence, findings, review and reusable analytical products |
| Collaboration inside Research/Audit | store comments, views and likes with findings or query raw Audit | couples mutable social/privacy telemetry to immutable knowledge and enables accidental surveillance/ranking |
| Content-addressed Parquet materialization | recompute every request or use an unversioned generic cache | repeated work, unsafe invalidation and cross-channel drift remain unavoidable |
| Canonical digital measurement context | calculate CAC/ROAS directly from provider dashboards | provider models, identity, cost allocation, refunds and offline retail grain cannot be reconciled reproducibly |
| Versioned branding | customer-specific fork/image | fragments upgrades, security fixes, validation, and support |
| One ReportSnapshot | channel-specific report builders | permits hidden recalculation and semantic drift across Web/email/XLSX |
| Local artifacts through v1 | early object storage/multi-host | expands trust, recovery, and deployment surface before single-host correctness is proven |
| ECharts through ChartSpec | raw ECharts options or Dash/Plotly core | weakens security, portability, email/XLSX parity, and product ownership of visual semantics |
| Governed treatment specification | ordinary hidden report filter for outliers | cannot reproduce fitted bounds, disclose impact, protect `vs LY` comparability, or distinguish analysis policy from DQ correction |
| Exact-K KMeans in v1 | automatic-K, GMM, HDBSCAN, Isolation Forest, or arbitrary clustering core | keeps the first model explainable, reproducible, CPU-bounded, and aligned with an explicit requested group count while preserving future extension ports |
| Effective discount policy plus normalized component fact | one customer-specific wide formula or mutable cap setting | preserves company configurability, temporal reproducibility, reconciliation, and extension without a fork |
| Explicit certification and method availability | infer trust from published status or hide future methods | keeps definition lifecycle separate from evidence strength and prevents roadmap claims from becoming runtime claims |
| Organization assignments plus functional roles | create a role per department/manager combination | avoids role explosion and keeps permission, hierarchy, and leadership independently versioned |
| Redacted contributor projection | query raw Audit for People & Creators | prevents surveillance-oriented leakage and gives the product an explicit privacy/aggregation contract |


## Installation and bootstrap amendment — 2026-09-06

The owner accepted [WS-001](planning/directions/DIR-006/workstreams/WS-001.md)
`1.0.0`: M5 Max/36 GB and bounded Linux VM targets, Edge TLS-only credentials,
guided prebuilt installation, explicit first-account roles and no required
experimental-data migration. The existing modular monolith and domain ownership
remain. These are target contracts; runtime code, migrations and browser
implementation are separate milestone work.
