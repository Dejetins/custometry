---
doc_id: CONTRACT-ANALYTICAL-AUTHORING-001
title: Governed population and analytical authoring contract
doc_version: 36
product_spec_version: 0.11.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [FILTER-013, FILTER-017, SEGMENT-029, SEGMENT-034, PIVOT-001, PARAM-001, COMPARE-011, ANALYTICAL-DOC-014, REPORT-015, REPORT-016, V1-AC-055, V1-AC-062, METRIC-030, METRIC-031, METRIC-032, METRIC-033, METRIC-034, METRIC-035, REPORT-018, REPORT-019]
status: accepted
acceptance_basis: owner-approved-product-requirements-2026-09-05-and-workspace-amendment-2026-09-20
proof_boundary:
  label: target-contract-with-bounded-ms004-s03-api-persistence
  exclusions: [complete-workspace-runtime-acceptance, browser-proof, release-authority]
---

# Governed population and analytical authoring contract

## Authority and scope

On 2026-09-05 the owner approved incorporating the segmentation and reporting
ideas from the [capability discovery](../architecture/planning/product-capability-discovery-2026-09-05.md)
into the project requirements. The
[machine blueprint](../../custometry-technical-blueprint-ru.md) owns normative
meaning; the [human mirror](../../custometry-technical-blueprint-human-ru.md)
and [UI requirements](../../custometry-ui-blueprint-ru.md) carry the same scope.
This contract connects that accepted intent to existing context ownership,
version transitions and implementing-ticket proof. It does not claim that
these target DTOs, editors or evaluators exist in production.

The scope is customer populations and compact analytical documents in B2C
retail. Product, store, receipt, line and event relationships can participate
in customer rules. Additional Product/Store membership types and new PDF/standalone HTML formats remain separate scope decisions. The owner-selected 2026-09-17 amendment adds bounded monitoring goals bound to configured metrics (METRIC-029); a general planning engine remains outside that addition.
B2B sales objects, activation and SaaS are not added. Forecasting remains on
hold until explicit owner resumption. Existing release labels and forecasting
obligations are preserved; the first external release scenario is undecided.

## Adoption and source allocation

Candidate labels are research references, not new execution IDs. All new
requirements are allocated to the v1 target; bounded internal subsets may be
implemented earlier without claiming the full feature or release complete.

| Accepted capability | Research references | Normative source | Observable acceptance |
|---|---|---|---|
| Related-object conditions and explicit absence | S01 | FILTER-013, FILTER-016, FILTER-017 | V1-AC-055; TEST-INV-102 |
| Behavioral sequences and scoped aggregates | S02, S03 | FILTER-014, FILTER-015, FILTER-018 | V1-AC-055; TEST-INV-102, TEST-INV-103 |
| Customer entity envelope and curated lists | S04 customer-first seam, S05 | SEGMENT-029, SEGMENT-030 | V1-AC-056; TEST-INV-104 |
| Set composition and dependency freshness | S06 | SEGMENT-031, SEGMENT-032 | V1-AC-056; TEST-INV-105 |
| Inclusion explanations and population health | S07, S10 | SEGMENT-033, SEGMENT-037; existing SEGMENT-023 through SEGMENT-028 | V1-AC-056, V1-AC-062 |
| Selection-time, event-time and fixed cohorts | S08 | SEGMENT-034, SEGMENT-035 | V1-AC-057; TEST-INV-106 |
| Exploration to exact set or reusable rule | S09 | SEGMENT-036, REPORT-015 | V1-AC-061; TEST-INV-110 |
| Compact authoring and reading | R01 | ANALYTICAL-DOC-014, ANALYTICAL-DOC-015 | V1-AC-058, V1-AC-059; TEST-INV-112 |
| Matrix semantics and cohort cell states | R02, R08 | PIVOT-001 through PIVOT-006 | V1-AC-058; TEST-INV-107 |
| Parameterized templates and explicit interactions | R03, R07 | PARAM-001 through PARAM-005 | V1-AC-059; TEST-INV-108 |
| Previous/custom period and population comparison | R04 | COMPARE-011 through COMPARE-013 | V1-AC-060; TEST-INV-109 |
| Guided draft measures | R05 | BLOCK-BUILDER-009; existing MetricRegistry lifecycle | V1-AC-059 plus metric contract tests |
| Evidence drill-through and analytical reuse | R06, R10 | REPORT-015, SEGMENT-036; existing Research/Methodology contracts | V1-AC-061; TEST-INV-110 |
| Semantic revision explanation | R09 | REPORT-016, REPORT-017 | V1-AC-062; TEST-INV-111 |

R11 remains an optional later target-input product decision. R12's existing
Web/email/XLSX snapshot parity remains required; its proposed additional formats
are not adopted. S04 does not activate non-customer memberships. These are the
explicitly optional expansions in the research, separate from the accepted
core ideas; they are not hidden prerequisites for report authoring.

## Ownership and dependency direction

This extends the [bounded-context map](../architecture/bounded-context-map.md)
and the established analytical-document/segment direction in
[ADR-0006](../adr/0006-analytical-document-retail-product-and-time-aware-segmentation.md).
It creates no new service, generic shared kernel or independent query engine.

| Owner | Target responsibility | Public dependency and invariant |
|---|---|---|
| Semantic Model | Published relationship/field/metric versions, cardinality, units, null/return rules, history compatibility | Supplies authorized immutable catalogs and compatibility decisions; does not calculate segment membership |
| Analytics | Normalized population expression/plan, collections/revisions, composition, snapshots/history, SelectionArtifact, PivotSpec/PivotResult, comparisons and evidence projections | Reads semantic contracts, DQ completeness and immutable artifacts; owns calculations and explanation from the same evaluator |
| Digital Journey & Marketing Measurement | Event definitions, deterministic identity and event/journey projections | Supplies declared versioned event projections; Analytics does not read private measurement tables or infer an unavailable event history |
| Presentation & Reports | Document templates/instances, control bindings, layout/density, effective context, root/page snapshots and diff presentation | Resolves public Analytics results into one snapshot; no browser aggregation or second workbook runtime |
| Methodology & Research | Analytical method templates, cases and evidence-linked findings | Retains its template/content lifecycle; uses the same parameter schema and Presentation publication port |
| Identity & Workspace | Effective object/row/field/member/export policy | Rechecked at validation, resolution, commit, read, explanation, drill-through and export; old snapshots never bypass current access |
| Execution Control | Resource admission, jobs, cancellation, dependency scheduling and reuse | Runs the normalized owner plan with versioned limits and existing outbox/fencing; does not implement business operators |
| Data Documentation, Ingestion, Artifact Lifecycle | Governed file admission, identity input artifacts and immutable payload lifecycle | Reuse existing safe-file/PII contracts; curated import does not create customer facts or introduce an arbitrary upload endpoint |

The client sends a typed draft, receives validation/capability/cost feedback,
then explicitly commits a normalized definition or requests an evaluation.
Analytics resolves exact dependencies under current policy and submits work
through Execution Control. Publication commits the complete immutable result
and metadata through existing owner transactions and artifact visibility rules.
Presentation pins that result when publishing a document. Autosave, mode
switching and dragging already resolved blocks do not initiate computation.

## Contract boundaries to preserve before implementation

**Population language.** Blueprint section 6.5 specifies legacy filter v1 and
the v2 node/scope envelope. Boolean groups, correlated existence, scoped
aggregate comparisons, sequence steps and population references are typed
variants. A related line condition is evaluated inside its receipt scope;
independent existence conditions can match different receipts. Empty complete
collections, field NULL and incomplete-history `unknown` are distinct. NOT does
not turn unknown into certified absence. Negative windows need completeness
evidence in the authorized universe, not merely an empty local result.

All windows resolve to half-open intervals with pinned calendar/timezone and
knowledge-as-of. Equal timestamps do not establish strict event order by
default. Validated alternative ordering needs explicit versioned semantics;
arrival order is not an implicit substitute. Capabilities and versioned resource
policy bound depth, fan-out, sequence length, cells and compute. Unsupported
nodes fail before execution. Flat customer-feature evaluation remains a valid
subset of the shared planner.

**Population identity.** Definitions, mutable drafts, immutable collection
revisions, evaluations, membership snapshots, history revisions and consumer
bindings are distinct. Customer membership retains the existing snapshot plus
canonical-customer key. An entity discriminator is added to the public envelope;
it does not rewrite historical keys or introduce B2B objects. Following a
definition version means following its evaluations, never silently accepting a
new definition version. Set composition rejects cycles and cross-entity or
incompatible-universe operands. Every run stores exact resolved operand IDs.

**Membership time.** Snapshot resolution and membership-time basis are separate
axes. Selection-time applies one selected set across the analysis period. A
fixed cohort pins its origin set. Event-time uses immutable effective intervals
and an explicit property-history/knowledge policy. Scheduled evaluations may
support stepwise effective-from-evaluation intervals; they cannot claim exact
continuous membership between observations. History gaps remain unknown.
Corrections create a new history revision without altering prior reports.

**Matrix and parameters.** Analytics owns grouping, totals, cohort age,
denominators and cell states. Presentation owns size, ordering of already
resolved projections, pinned columns, accessible formatting and mode-specific
controls. Changing grouping or measure semantics creates a new result;
changing density does not. Typed parameters target allowlisted inputs through
explicit mappings. Defaults, overrides and resolved relative periods enter
semantic identity; no mapping may weaken locked/security scope. New template
versions require an explicit instance upgrade with a draft diff.

**Comparison and explanation.** TimeComparisonSpec v2 adds previous/custom
period modes without reinterpreting v1. Population comparison is an orthogonal
binding. A cell's evidence projection preserves its exact result, semantic key,
metric, window and population context. Raw detail requires separate grants.
Saving a set uses the full authorized result, not visible rows or a sample;
conversion to a reusable rule is offered only when lossless. Semantic diff
reports known input/definition/policy changes and mixed or unknown attribution
when their effects cannot be isolated. It is not a causal decomposition engine.

The [source data adaptation contract](./source-data-adaptation-contract.md)
extends these existing trust dependencies with DQ-INPUT-004/007 and INGEST-018:
complete delivery does not prove complete business history, unresolved customer
rekey is not a proven merge, and source corrections/reassignment recompute affected
future evaluations without rewriting saved memberships or report snapshots.
DATA-MAP-004 through DATA-MAP-006 make derived SP child channels shared typed
dimensions. Unknown child classification and degraded population coverage remain
visible in filters, totals, exclusions, explanation and export.

## Compatibility assessment and transition conditions

Baseline: the pre-adoption local blueprint/contract contents inspected on
2026-09-05, with existing shared checkout changes preserved. The earlier remote
research snapshot remains historical evidence. This change writes documentation,
generated requirement references and UI capability coverage only. No executable
API schema, serializer, database migration, worker or browser implementation is
changed. Current runtime behavior therefore has **none** impact from this patch.

The following assessments concern the specified future transitions, not
observed deployment behavior:

| Surface / consumer direction | Before to target | Classification and required action |
|---|---|---|
| Old filter/comparison consumer receiving new payload in its old envelope | Boolean field nodes / LY enum to relational nodes / expanded enum | **breaking-change** if sent as the same supported version: old shapes cannot represent the new meaning. Version dispatch and capability negotiation are required; unsupported clients receive an explicit error, never stripped nodes or substituted modes |
| New evaluator reading old definitions and snapshots | Existing v1 payloads to version-aware readers | **unknown** until reader/normalizer tests prove original semantics, IDs and hashes. Keep v1 readers; migration may create a new definition with origin lineage, never mutate an old publication |
| Existing customer membership key | Snapshot plus canonical customer to typed customer envelope | **unknown** for actual DTO/persistence consumers until implementing-ticket inspection. Target preserves the old key; an entity envelope is not evidence of safe migration |
| New collections/history/templates/pivots persisted for old readers | No assumed support to new versioned object/result variants | **unknown** until schemas, supported mixed-version readers and rollback are specified. Activate writers only after compatible readers and schema deployment; do not delete or downconvert new objects during rollback |
| Request/reuse identity and surviving jobs | Old normalized inputs to scopes/windows/dependencies/parameters/history-aware inputs | **unknown** until producer/consumer and queued-job proof. Version the normalizer/namespace, pin exact dependencies, prevent cross-version cache collisions and preserve old artifact references |
| UI capability manifest | Existing IDs/paths to additional requirement references on six existing capabilities | **compatible-change** for the current coverage schema: object shape and route identities remain unchanged. Static route/schema validation is required; the additional coverage does not prove UI behavior |

Canonical `latest_successful_by_definition_version` reconciles an older
shortened spelling in the blueprint example. It preserves the existing
SEGMENT-021 meaning. A legacy alias reader must be tested if persisted consumers
use that spelling; changing serialized old bytes or hashes is not authorized.

The implementing ticket must enumerate actual serializers/readers, accepted
versions, queued jobs and migration order before changing a wire or persisted
contract. New-client/old-server and old-client/new-server failures must be
explicit and actionable. If rollback cannot read newly created variants,
disable new writes and retain the compatible reader or forward-fix; do not
promise downgrade compatibility without proof. Existing history is retained.
Schema and reader preparation precede dependent UI activation.

## Acceptance witnesses and bounded implementation order

Use synthetic retail fixtures. These examples constrain business meaning;
they are required later evidence, not tests executed by this documentation task.

1. Customer A buys product X online and Y offline; B buys X offline. A fails
   the same-receipt X/offline rule but passes independent X and offline rules.
   Adding duplicate line joins does not multiply members or receipt revenue.
2. No event in an incomplete 60-day observation window is unknown, not proven
   absence. Reverse-order and equal-timestamp sequence cases are deterministic.
3. A customer enters a segment midmonth. Selected-set, fixed-origin and
   event-time totals differ intentionally; late corrections preserve old results.
4. Concurrent curated append and replace conflict visibly rather than losing
   members. Repeated import submission is idempotent. Revoked or failed upstream
   populations cannot produce a falsely current downstream set.
5. Groups with ratios 10/20 and 90/100 have total 100/120, not the average of
   displayed percentages. Distinct and semi-additive totals remain correct with
   pagination, collapse, transposition and top-N; suppressed and immature cells
   remain distinguishable from zero and cannot be inferred from totals.
6. Changing a template parameter affects only declared compatible targets;
   changing density leaves business identity unchanged. Linked-instance upgrade
   creates a draft while the old publication and personal views remain intact.
7. Cell drill-through preserves source context but denies raw rows without a
   member grant. Exact-set saving covers all authorized members; unsupported
   rule conversion does not approximate silently.
8. Identical semantic inputs produce no business diff. Changed data and changed
   definitions are separate reported categories; inseparable effects remain
   mixed/unknown and inaccessible versions disclose no metadata.

The recommended provider order is customer correlated rules with an authorized
preview/snapshot/explanation, then a compact matrix report with typed controls,
then collections/composition/comparisons/exploration/diff. Sequences and
event-time reporting require actual event/history providers and their proof.
These are outcomes for ordinary tickets, not a new execution ledger or a full
feature implementation authorization. Shared identity/data-policy/execution
integration can continue independently under its existing scope.

Each implementing slice needs the applicable contract, real database/artifact,
API authorization and browser/keyboard evidence. Resource budgets, privacy
thresholds and retained history require explicit versioned policy, not invented
numeric defaults. Public acceptance still requires all applicable criteria;
the forecasting hold prevents an unsupported full-release claim.

## Documentation verification record — 2026-09-05

The synchronized delta contains 35 feature requirements, 11 test invariants and
eight v1 acceptance criteria. Machine/human coverage is 1,195 indexed IDs; the
new criteria are V1-AC-055 through V1-AC-062. The frozen September 4 audit and
coverage JSON are unchanged and are not regenerated as a current status ledger.

Observed repository checks after `source scripts/activate-toolchain.sh`:

- `uv run --locked python -m tools.custometry_quality.validate_blueprints`: pass;
- `uv run --locked python -m tools.custometry_quality.generate_requirement_index --check`: pass;
- `uv run --locked python -m tools.custometry_quality.generate_docs_index --check`: pass, 37 contributor documents;
- `uv run --locked python -m tools.custometry_quality.check_docs_links`: pass;
- `uv run --locked python -m tools.custometry_quality.validate_route_registry`: pass, 117 routes and 22 cross-surface capabilities; no route added;
- `uv run --locked python -m tools.check --scope local`: pass;
- `git diff --check`: pass.

The generators were run in write mode only for their owned requirement and
contributor indexes, then checked. Static checks verify synchronization,
references, schema/route coverage and local source gates. No new behavioral test
suite, application implementation, API or persistence migration, browser run,
performance benchmark, release or external publication is part of this change.
The next safe step is to prepare bounded implementation tickets with actual
provider/consumer schemas and the acceptance witnesses above.

## Implemented bounded sales result (MS-003-S02)

The accepted [MS-003 plan](../architecture/planning/milestones/MS-003/plan.md)
TECH-03/04 has a bounded implementation through `AnalyticsService.run_sales_report`
and `get_sales_report`. [S02 evidence](../../.codex/delivery/evidence/MS-003/MS-003-S02/report.md)
records exact real dataset, metric and result identities. This does not implement
the full authoring/MetricRegistry target above.

`POST /api/analytics/sales-reports/v1` accepts the published dataset UUID, inclusive
UTC `starts_on`/`ends_on` (default 2025-01-01..2025-11-30), optional authorized
`store_id`, and `comparison` (`none` or `previous_year_same_dates`). At most 366
dates are accepted. Completed/EUR eligibility is immutable and returned as locked;
product/category/brand/customer and arbitrary filter controls are rejected.
Definitions, labels, formats and ratio references come from the Semantic-owned
[sales metric definitions](../../packages/semantic_model/application/sales_metrics.py);
this document does not duplicate their formulas.

`GET /api/analytics/sales-reports/v1/{result_id}` verifies current session,
workspace, owner and effective permission identity, then verifies the exact
committed result artifact. It neither recalculates nor reads the source. The
versioned response's totals, complete bounded `daily` table/chart data, comparison,
metric versions, Calendar artifact, six bindings and Result Trust are one immutable
payload. Empty values are `null` with `no_eligible_receipts`; missing/incomplete
Calendar dates are explicit. Comparisons with incomplete declared coverage or an
unmappable leap-day boundary are unavailable. Calendar completeness is an imported
declaration, not proof of historical dimension completeness or observed daily sales.

The actor's currently resolved permission set enters identity; policy changes
separate computation and deny reuse of prior-policy results. The first profile
uses workspace-visible Store values; no row-scoped store grant designer is claimed.
Source hashes are verified even for repeated computation requests. Saved-result
reads require the result artifact, without a live source dependency. Corrupt or
missing artifacts never cause fallback to another version. S03 must intersect its
own document permissions with this result owner port and pin the returned manifest,
metric/calendar/quality/policy references; it must not query Analytics private tables.

[OpenAPI](../../packages/contracts/openapi/analytics.openapi.json),
[request schema](../../packages/contracts/schemas/sales-report-request.schema.json)
and [generated client](../../packages/contracts/src/analytics-client.ts) are checked
by `tests/contract/analytics`. Regenerate with `uv run --locked python -m
packages.contracts.generate_sales_client`. The client uses the existing DTO renderer
and bounded input-aware methods, because the Foundation HTTP generator supports
only operations without inputs. Existing `/analytics/results` consumers and stored
v1 results retain their contracts. The new client is exported as `salesReports`.


## Implemented bounded draft composition (MS-003-S03)

[MS-003 TECH-05/06/08](../architecture/planning/milestones/MS-003/plan.md) now has a
Presentation-owned implementation: the common `AnalyticalDocumentCompositionV1`
subset, one `workbook_report` template, immutable versions and root/page preview
manifests. [S03 evidence](../../.codex/delivery/evidence/MS-003/MS-003-S03/report.md)
records actual PostgreSQL, artifact and session/API proof. It does not claim full
composition editing, publication, sharing, refresh, rendering or UI readiness.

The independent [reports OpenAPI](../../packages/contracts/openapi/reports.openapi.json)
and [generated client](../../packages/contracts/src/reports-client.ts) are exported
as `draftReports`. The API base is `/api/reports`; collection paths end in `/`.
Every mutation explicitly supplies `contract_version: "draft-report/v1"`, uses the
S01 session adapter and requires Origin/CSRF for browser cookies. Reads return
`Cache-Control: no-store`. Ownership and `report.read` intersect `analysis.read`
and the result owner's current policy; saving also requires `report.manage`.
Installation administration alone grants none of these document capabilities.
Filtering precedes list pagination/counts; denied entries cannot contribute counts.
Missing/corrupt results do not produce partially populated library responses.

1. Explicit Apply uses the S02 compute endpoint. `POST /prepare` consumes its exact
   result ID and persists a canonical line ChartSpec, system BrandProfile and
   CompanyPack, returning their complete typed projections and exact ID/hash pairs.
   These are real Presentation records. Local system tokens are packaged in the
   Presentation adapter with their source hash; CompanyPack pins S02 metric versions,
   units and formats. Arbitrary visual options, unknown IDs, content drift and
   incompatible result/default bindings cannot enter a save.
2. `POST /` creates and saves a report with `expected_revision: 0`; creation identity
   is derived from workspace, actor and idempotency key. `POST /{id}/versions` saves
   another immutable version against the expected current revision. A repeated key
   returns its exact original version; a changed request with that key or a stale
   revision returns 409. Title and resolved result are editable; node IDs are stable.
3. `GET /{id}` resolves the latest saved version once. `GET /{id}/snapshots/{sid}`
   opens the exact owned draft preview, optionally checking `version_id`, `page_id`
   and `block_id` query UUIDs. A mismatched locator returns 404. Both paths recheck the
   result owner, reference hashes and actual root/page/result artifact bytes. They
   never calculate, fetch source directories, resolve new metric/default versions,
   or substitute another snapshot.

The root pins the full immutable S02 result, six entity bindings, Calendar,
relationship/policy identities, QualityReport, orphan-item limitation, parameters,
metrics/units/grain/schema, author and system defaults. Chart/table consume `daily`;
comparison uses `comparison.daily` with same-date previous-year alignment. The line
spec is renderer-neutral; compiler and actual renderer output belong to S04. Locale
switching may format the same values; it cannot change their business identity.

Artifact Lifecycle commits result-dependent page and root manifests before the
Presentation transaction inserts a version and atomically switches latest. Failures
before the switch preserve the prior complete draft. Unreferenced immutable artifacts
can remain after failed/concurrent saves; this slice does not implement orphan cleanup.
Missing bytes return `ARTIFACT_MISSING`, integrity failures `ARTIFACT_CORRUPT`, and
unavailable storage `STORAGE_UNAVAILABLE`. No error includes local paths or data.

The additive `0011_presentation_drafts` migration follows actual `0010_sales_report`.
Existing migrations and prior-feature records remain unchanged. Run migrations before
activating the new API; older servers do not implement these new endpoints. Downgrade
with saved documents fails closed. Recovery after writes uses the retained owned
pre-upgrade PostgreSQL backup and unchanged immutable artifacts, or forward repair;
no lossless document downgrade is promised.

A credential-free client example after a real session and explicit S02 computation:

```typescript
const reports = new draftReports.DraftReportClient("/api/reports");
const refs = await reports.prepare({contract_version: "draft-report/v1", result_id}, csrf);
const saved = await reports.create({
  contract_version: "draft-report/v1", result_id, title: "Retail report",
  expected_revision: 0, idempotency_key: crypto.randomUUID(),
  chart_spec: refs.chart_spec.reference,
  brand_profile: refs.brand_profile.reference,
  company_pack: refs.company_pack.reference,
}, csrf);
const exact = await reports.preview(saved.report_id, saved.snapshot_id);
```

`csrf` is the current session value in memory, never a committed credential. Regenerate
with `uv run --locked python -m packages.contracts.generate_reports_client`.
`tests/contract/presentation` checks provider/OpenAPI/schema/client parity;
`tests/unit/presentation` checks composition and request invariants;
`tests/integration/presentation` proves the isolated real database/artifact boundary.

## Bounded analyst discovery and Web consumer (MS-003-S04)

The [owner-authorized context extension](../../.codex/delivery/evidence/MS-003/MS-003-S04/owner-context-authorization-20260915.md)
adds `GET /api/analytics/sales-report-context/v1`. It requires `analysis.read` and
`analysis.run` before discovering published `retail-report/v1` versions through
Semantic's public port. It reads only the integrity-checked Store artifact through
Artifact's existing sales port. The projection returns dataset/version labels,
Store IDs/labels, a default period and locked eligibility/currency. It neither
computes sales nor exposes connection secrets, raw paths, other workspaces or
customer/product directories. Missing or corrupt Store bytes fail closed.
[Analytics OpenAPI](../../packages/contracts/openapi/analytics.openapi.json) and
the generated `reportSales` DTO namespace bind this additive contract.

The [Web source contract](../architecture/ui/custometry-web-implementation-source-contract-v1.md)
records the bounded route capability inventory. Its ECharts 6.1.0 SVG adapter
verifies canonical reference hashes, CompanyPack/BrandProfile bindings and the
closed line ChartSpec before compiling. Chart and accessible current/prior tables
consume the same immutable server series; locale does not change value identity.
The native pilot document applies its original Web palette, axes and adaptive
legend through a typed presentation port after validating those references; persisted
BrandProfile values and ChartSpec/data identities are not rewritten.
CAS conflict preserves unsaved input. Session expiry/revocation clears protected
query state, including late-response races. Exact preview validates its page and
retains the S02 item-attribution limitation and eligible receipt totals.
No new persistence schema or permission grant is introduced by this extension.

## Metric worksets and monitoring goals: target amendment

The [Mindbox interaction atlas](../architecture/ui/references/mindbox-metrics-2026-09-17/README.md), revision 1, binds owner-selected target METRIC-025…029 and CHART-021 to observed screenshots. Existing MetricVersion, MetricGroupVersion, Saved View, TimeComparisonSpec and ComparisonArtifact remain the semantic anchors. A configured metric card and an ordered workset are conceptual presentation requirements, not a new service or an approved persistence schema. A monitoring goal is distinct from a target-action definition and forecast.

This addition changes target requirements only: no endpoint, schema, migration,
current capability or historical milestone binding is introduced. The owner
resolved the product choices on 2026-09-20 in
[WS-003 2.0.0](../architecture/planning/directions/DIR-004/workstreams/WS-003.md#owner-decisions-and-next-child).
The next selected L3 fixes the exact schemas, versioning/CAS, calendar/comparison
projection and goal-calculation methods before executable prompts. Preserve
server-owned calculations and the Apply/Save/immutable-preview boundary.

### Owner-selected behavior — 2026-09-20

METRIC-030…035 and REPORT-018/019, requirements revision `2026-09-20.1`, add:

- Six date grains: day, week, month, quarter, half-year and year, with one
  calendar/timezone policy and matching chart/table identity.
- Both minimum-achievement and maximum-limit goals; absolute values and relative
  changes against an explicit baseline. The report creator selects the mode in
  report configuration; report use cannot switch that definition.
- One-off and recurring goals. Each occurrence has an exact period and rule
  version; recurrence creates periods, not an implicit calculation schedule.
- Goal context is pinned at creation. Only the report creator can change its
  definition, with immutable change history. Reader filters never change it.
- Manual recomputation, final assessment after period end with sufficient data,
  and explicit revised calculations for corrected closed periods. Optional run
  rate is a separate estimate, never the final actual or an automatic achievement.
- Creator-only report authoring, including shared-set definition and settings.
  Functional permissions remain necessary but do not substitute for creator
  identity. Administrators still manage access separately; department ownership
  and handover do not turn another principal into the report's creator.
- Shared-set readers inherit report/data access. Personal display settings stay
  pinned until an explicit update/reset; current permissions are still enforced.

The report creator owns report composition and goal policy. A non-creator can
use the exposed filters and permitted personal display controls without mutating
that definition. Existing personal presentation choices under METRIC-021/022 do
not authorize new shared cards, metric formulas, target changes or goal modes.
An authorized independent report copy has its own creator and lineage; this is
not a way to edit the original. If the original creator loses access, no silent
administrator/content-editor fallback is selected by this decision.

### Technical rules to settle in the selected L3

The following are engineering recommendations, not additional owner approvals or
implemented guarantees. Resolve and pin them before the affected child executes.

| Boundary | Proposed rule and reason | Child / proof needed |
|---|---|---|
| Calendar and alignment | Reuse the current UTC basis for the receipt scenario; ISO Monday–Sunday weeks. The 2026-09-20 owner correction requires a versioned workspace financial calendar: quarter/half-year/year boundaries follow the pinned calendar or fiscal basis, not hard-coded January. Clip edge buckets to the requested interval and expose partial coverage. Preserve `previous_year_same_dates`: map baseline days to current-day buckets, including weeks, rather than silently selecting ISO-week alignment | C01; leap day, year crossing, partial buckets and six grains; daily v1 remains readable |
| Aggregation | Sum valid additive components; recompute average receipt as period revenue / period receipt count. Missing data, zero and no eligible rows retain metric policy. Include grain/calendar policy and effective context in result identity | C01; reconciliation of chart, table and full-period totals |
| Relative goal | Pin author-selected baseline policy and resolved value for each occurrence. For the initial positive-baseline subset, derive target `B * (1 + change_percent / 100)` and evaluate the selected lower/upper comparator on actuals. A zero, negative or missing baseline is unavailable under this proposed method, not a fabricated percentage | C02; baseline eligibility and target unit checks; future signed-base methods require explicit methodology |
| Progress | Lower-bound progress may show actual / positive target, including overachievement. Upper-bound display shows used limit and remaining/exceeded amount; smaller usage is not labeled worse achievement. A valid nonpositive target can still be compared in its native units; the percentage display is unavailable unless a specific method is defined | C02; both directions, ratios, zero/missing inputs and temporary versus final status |
| Recurrence | Prefer calendar-aligned periods from a creator-configured versioned rule, with deterministic occurrence identity. Materialize required occurrences idempotently through existing application/execution seams; do not add a new scheduling engine. Period creation must not refresh an old actual or rewrite a closed occurrence | C02; boundary crossings, duplicate requests, changed rules and manual calculation |
| Run rate | For eligible additive totals, propose `actual for elapsed complete calendar days / elapsed days * total period days`. Require a nonempty, contiguous complete elapsed interval. Show coverage and the constant-pace assumption. Do not scale average-receipt ratios with that formula; an unsupported metric shows unavailable until its method is selected | C02; missing days, zero elapsed time, additive versus ratio metrics. No seasonality, model training or confidence interval is implied |
| Manual calculation and access | Execution permission and result publication remain separate from changing definitions. A recomputation cannot change a goal rule, report policy or stored snapshot in place; preserve earlier results and creator attribution | C02/C03; request authorization, explicit correction and exact result lineage |

### Compatibility impact and required follow-through

Baseline: repository requirements and bounded report code at
`7ef3c072a527627991036150d25e87adbbf8e60b`; candidate: this target amendment.

| Surface / consumer | Before → after | Classification / evidence and next action |
|---|---|---|
| Report authoring policy | An edit-capable author could be admitted by the previous ANALYTICAL-DOC-015 target; another principal's `report.manage` now cannot authorize editing the creator's report | `breaking-change` to the earlier target guarantee. REPORT-018 narrows report authoring only; preserve access administration and other document profiles. C01/C03 must test creator plus permissions, and denied non-creators including administrators |
| Time/result and goal contracts | Bounded daily sales results → selected grains and versioned goal/baseline/recurrence projections | `unknown` until C01/C02 select wire schemas, readers and migrations. Do not reinterpret stored daily artifacts or promise old binaries understand new documents |
| Existing local report runtime | This amendment changes documents only; current ReportService remains owner-scoped with permission checks | `none` for deployed behavior in this authoring unit; no runtime authorization, migration or browser proof is claimed |
| Historical execution | MS-001…003 plans/prompts/journals remain at their recorded source basis | `none` for execution state; MS-003 S05/S06 stay deferred, and this amendment creates no new pack |

Acceptance must include all twelve selected decisions, creator/non-creator cases,
saved-result continuity, and separate final actual/run-rate states. Local checks
of these documents cannot certify the eventual mixed-version runtime transition.

### Company financial calendar — owner correction, 2026-09-20

METRIC-030, requirements revision `2026-09-20.2`, requires the financial calendar
in base company/workspace settings. The accepted product correction supersedes
the January-only recommendation above; it does not accept a wire schema or the
whole L3. Semantic Model owns versioned calendar meaning/defaults, Identity checks
settings permissions, Analytics resolves buckets, and Presentation pins the version.
Imported Calendar coverage remains distinct. Existing reports/results never follow
a changed default silently. The original report-adoption UX described here was
superseded by the 2026-09-22 owner correction below.

[MS-004 0.2.0](../architecture/planning/milestones/MS-004/plan.md)
selects the initial month-based fiscal profile, endpoint/persistence contracts,
labels, current-versus-pinned behavior, migration and proof. Its technical design was accepted by the owner on 2026-09-20
(MS-004/DEC-01); this does not establish implemented wire contracts. C02 goal periods must pin the same calendar version; neither goal
rules nor the separate fiscal-period comparison mode are implemented by this amendment.

Acceptance navigation (2026-09-20): MS-004 0.2.0 decisions and expectations
accepted by the owner; see MS-004/DEC-01. Editorial registration only, no runtime
change or execution authorization; broader MAP/L1 reviews remain open.


## MS-004 S01 implemented foundation

The accepted [MS-004 plan](../architecture/planning/milestones/MS-004/plan.md)
remains the design authority. S01 implements the following bounded foundation;
its [stage evidence](../../.codex/delivery/evidence/MS-004/MS-004-S01/report.md)
records actual local checks. The journal alone records stage acceptance.

- Strict `configured-report/v2`, composition schema 2, ChartSpec `2.0.0`,
  `metric-workspace/v2`, `card-comparison/v1` and `saved-view/v1` types live in
  `packages/contracts/presentation/workspace.py` and
  `packages/contracts/analytics/workspace.py`. Existing v1 models/routes are
  unchanged; union readers dispatch by the explicit discriminator. Stable legacy
  IDs and copy helpers preserve MetricVersion references without formula cloning.
- The common composition retains pages, sections, blocks, source/access and brand
  bindings. Personal configuration and complete per-card bindings extend that
  document. Saved View query context is separate from display; reader overrides
  cannot carry definition or calendar-adoption fields. Runtime authorization,
  registry lookup, complete Apply/Save and reader projection remain S02/S03 work.
- Calendar contracts are in `packages/contracts/semantic`; application and
  PostgreSQL adapters are Semantic-owned. `business-calendar/v1` supports a
  month-based year beginning on day 1, start month 1–12, start/end year labels,
  UTC and ISO Monday weeks. `end_year` and January are the initial defaults.
  Unsupported profiles/unknown fields fail validation.
- `GET /api/semantic/workspace-calendar/v1`, exact
  `GET /api/semantic/workspace-calendar/v1/versions/{version_id}?content_hash=...`
  and `POST /api/semantic/workspace-calendar/v1/versions` are mounted. Identity
  resolves the current active principal, membership, workspace and permissions
  on every call, including replay. GET requires `workspace.read`; POST requires
  `workspace.manage` plus the existing browser Origin/CSRF checks. Report author
  or `report.manage` alone is insufficient. Exact foreign-workspace versions
  return 404. Stale revision/key-body mismatch returns 409; invalid profile 422.
- A default update locks its workspace pointer, inserts an immutable version and
  moves the pointer in one transaction. Same-key/body replay returns its original
  version and revision even after later updates. Request identity includes actor;
  another actor cannot reuse the key as their own response. Hashes cover canonical
  profile bytes. Pinned versions remain readable and are never relabeled.
- System initialization uses UUIDv5(workspace, `business-calendar/v1/initial-january`)
  and revision 0 with `created_by:null` (explicit system attribution). Human-created
  versions have a principal, previous version, request hash and idempotency key.
  Migration backfills existing workspaces; Identity API bootstrap/workspace creation
  invokes the same idempotent public Semantic provision operation. An authorized
  first read also recovers interrupted initialization or an old writer's new
  workspace. It cannot replace an existing default; no cross-context table access
  or distributed transaction is introduced.

`python -m packages.contracts.generate_workspace_client` uses the existing
Pydantic/OpenAPI/TypeScript renderer to generate the versioned schemas and
`workspace-contracts.ts` / `workspace-calendar-client.ts`. The workspace OpenAPI
file is a **component catalogue with no paths**, not an advertised unimplemented
API. `WorkspaceCalendarClient` uses base URL `/api/semantic`; report/Analytics v2
routes remain unmounted pending S03's current-access proof. Contract tests check
all generated bytes against providers. The legacy generator/output is unchanged.

The 1 MiB raw configuration bound is exposed by `parse_configuration`; S03
v2 HTTP adapters invoke the raw-body bound before parsing. Typed validation
also checks the normalized definition, 20 worksets, 50 cards per workset, 200
cards total, 1000 unique store IDs, at most 366 inclusive days, unique IDs and
selection ownership. Server registry/access resolution, historical deleted-ID
non-reuse, truthful limit error mapping and result verification are implemented by the S03 consumers described below. A valid DTO is not proof of those runtime checks.

The S01 foundation alone did not establish calculation, report v2 save/read,
settings UI, shared worksets, goals or full METRIC-022 conformance. The following
section records the subsequent S02 calculation boundary.


## MS-004 S02 calculation and immutable result boundary

`WorkspaceAnalyticsService` implements D03–D05 of the unchanged accepted plan.
It consumes public Semantic/calendar and Artifact ports and a required
`WorkspaceAccessPort`. Its caller must provide a trusted current dataset projection,
never an HTTP-supplied policy fingerprint or allowed-store set. S03 owns the actual
Identity/report object adapter and public activation; no v2 route was mounted at S02 acceptance.
The service checks the actor/dataset/permission projection before work and rechecks
it before returning reused or newly persisted results.

`WorkspaceRunRequest` resolves null inheritance, explicit empty sets and the
common/local/allowed intersection. Unknown and explicitly denied stores fail.
Identity partitions by workspace, actor, policy/scope, dataset publication, all six
source bindings, registered component definitions, pinned business calendar, exact
period, grain and alignment. Card IDs, labels, ordering and presentation settings
are excluded. Batch Apply groups equivalent contexts and returns separate card
bindings; concurrent work uses existing artifact admission and PostgreSQL winner
uniqueness, with no single-flight service or cross-actor reuse claim.

The v2 envelope now includes exclusive natural/effective ends, clipped flags,
calendar pins, financial indices, daily registered components and separate expected,
Calendar-present, declared-complete, observed-day and receipt counts. Inclusive
input dates are projected onto UTC receipt-header grain. Weeks remain ISO Monday;
month arithmetic determines fiscal quarters/halves/years. Clipping is independent
of completeness. Empty values are null; eligible zero revenue remains zero. Ratios
are recomputed from summed components, using a local Decimal precision of 38 and
canonical non-exponent strings; display formatting never changes raw values.

Temporal projection stores exact current-to-prior-date mapping and baseline date
sets. A current Feb 29 without a predecessor blocks that bucket and total delta;
unaffected buckets may compare. An unmapped prior leap day is excluded with an
explicit disclosure. Both comparison sides carry their own coverage. Absolute and
relative deltas are server values; zero baseline only blocks the relative delta.
Pair comparisons retain separate unit/format/result references. Cross-unit deltas
are unavailable; period, grain, calendar or definition-basis incompatibility blocks
a combined chart. The comparison artifact references admitted result artifacts;
chart/table/tooltip consumers use the same typed projections. Temporal right-side
`context` is the aligned current axis; `baseline_dates` names the actual prior dates.

`WorkspaceArtifactStore` admits deterministic immutable JSON using existing
manifests/dependencies and verifies exact content on reuse/read. Analytics records
`contract_version=metric-workspace/v2` in the S01 migration's discriminator; existing
v1 calculation and artifact formats are unchanged. Missing/corrupt input or output
fails explicitly. No output files are repaired silently or treated as zero data.

The S02 `custometry_api.analytics.workspace_router` factory exposes bounded
result/context/catalog/comparison adapters only when explicitly composed with read
and run dependencies. At S02 acceptance it was absent from `create_app`. S03 now supplies current
object/data access plus CSRF for mutations and advertises the composed paths
in workspace OpenAPI. Regenerate the existing schema and
TypeScript outputs after envelope changes with `generate_workspace_client`.

Local intake/SQL/artifact evidence is recorded in
[S02 report](../../.codex/delivery/evidence/MS-004/MS-004-S02/report.md).
It does not establish saved-report transactions, real v2 public authorization,
browser behavior, release readiness or owner acceptance of the milestone.


## MS-004 S03 guarded API and configured report persistence

S03 composes report routes under `/api/reports/v2` and direct Analytics routes
under `/api/analytics/metric-workspace/v2` (the proxy adds `/api`). Request-scoped
adapters reauthenticate through Identity and consume its public `ResourceAccessPort`;
Presentation and Analytics do not query Identity's private tables. Functional
permissions, object grants and current data ceilings intersect; creator identity
is an additional immutable requirement for report definition writes. This also
protects existing v1 mutations and lists. Authorized readers see the explicitly
pinned v1 base, not the creator's personal v2 overlay; their own Saved Views have
independent identity, CAS and access checks. Filtering precedes list pagination.

The bounded data projection supports `store:<id>` row scopes and intersects
applicable layers with admitted Store membership. Unknown row expressions and
column restrictions fail closed. Unbound legacy reports retain their actual
creator's existing exact-read/update access through a server-verified stored v1
result binding; previous bindings prevent treating revoked resources as unbound.
That internal projection has no arbitrary-owner HTTP endpoint. Direct Analytics
consumers require ordinary current data authorization. A reader cannot silently
narrow an exact snapshot, but may explicitly Apply an authorized narrower query.

Apply returns verified bindings, chart references, chart payloads and immutable
comparison projections without changing the saved document. Explicit
`reuse_result_ids` selects verification-only creator Apply for display/selection
changes with `analysis.read`; new calculation requires `analysis.run`. Equivalent
contexts keep distinct card IDs. Reusing a richer temporal result for an already
available non-temporal display does not trigger calculation. GET never computes.

Save checks the complete definition, including inactive worksets, stable IDs and
historically retired IDs, all result/query bindings, registry/calendar references,
comparison bytes and chart payloads. A single transaction commits report and
companion view revisions and latest pointers after artifact admission and a final
current-access check. Report and view revisions both participate in CAS. The v2
semantic idempotency hash excludes the key itself; same-key/same-body retry returns
its stored revision only after current access and dependency verification.

v1 exact snapshots retain their original payloads. Upgraded latest v1 reads and
writes return `REPORT_VERSION_UPGRADE_REQUIRED`; clients must use v2. The outer
editor envelope supplies current capabilities rather than treating stored snapshot
capabilities as authorization. Workspace defaults never replace a report's pinned
calendar. The existing versioned API can express an explicit revision; the report
UI no longer offers calendar adoption under the 2026-09-22 correction.

Generated `workspace-client.ts`, `workspace-contracts.ts` and OpenAPI include
editor, exact snapshot, Apply/Save and own-view routes. Existing report/Analytics
clients are regenerated from the mounted applications. See the
[S03 report](../../.codex/delivery/evidence/MS-004/MS-004-S03/report.md) for actual
API/PostgreSQL/artifact proof and the [recovery boundary](report-refresh-serving-recovery-contract.md#ms-004-s03-atomic-report-and-view-recovery).
S04 implements the bounded Web integration described below; S05 owns integrated acceptance.
The pinned draft base is not a published default: full METRIC-022 published-default
reset, shared-version adoption, publication and release are not claimed.


## MS-004 S04 Web consumption

The native report workspace consumes the S03 v2 contracts for personal worksets,
exactly three registered metric definitions, repeated independent cards, ordering,
copy and common/local store restrictions. `null` retains inheritance and `[]`
remains explicitly empty. Display selection, order and labels do not change the
business query; changed context/grain/calendar requires explicit Apply. Save is
separate and uses verified result bindings in card order, including inactive sets.

Reader presentation state belongs to its selected own Saved View, including its
query, calendar pin, representation and immutable result scope. Existing verified
bindings support display-only Save without `analysis.run`; a legacy base without
workspace bindings first needs an authorized Apply to produce those bindings.
Private author worksets are not exposed as a shared reader definition.

Workspace fiscal settings remain administrative and versioned. Report creators
can explicitly adopt the current default; readers cannot rebase report policy.
The chart, table and Focus render server values, temporal deltas and exact bucket
dates. Different units retain separate axes; no browser metric arithmetic is used.
See [S04 evidence](../../.codex/delivery/evidence/MS-004/MS-004-S04/report.md) and
[the Web source contract](../architecture/ui/custometry-web-implementation-source-contract-v1.md#ms-004-s04-native-workspace-integration).
Final integrated and owner acceptance remain S05.


## MS-004 S05 comparison-preserving personal views

A newly saved personal view includes its immutable `CardComparisonV1` when its
selection needs one. It is admitted from verified existing results before the
view transaction. GET verifies the selected card/result/metric/unit/format
identities, current dependency access and comparison manifest; it never performs
source aggregation or creates a replacement comparison. Display-only view Save
remains possible without report-run authorization under unchanged data policy.

The optional `comparison` field is omitted when absent, preserving older payload
serialization and companion-view hashes without a migration rewrite. Old strict
extra-forbid readers reject new comparison-bearing payloads: upgrade readers and
generated clients before these writes; forward repair remains the supported
recovery direction. Older views retain exact values; no browser arithmetic fills
a missing pair comparison. An explicit Apply/Save obtains the verified projection.

Chart, table, tooltip and Focus consume identical server values/deltas/reasons.
Temporal labels include prior-year identity and exact mapped date ranges; fiscal
labels retain their actual current date range. Initial inspector focus is set
when the native iframe portal mounts, with keyboard traversal and return checks.
See [S05 integrated evidence](../../.codex/delivery/evidence/MS-004/MS-004-S05/report.md)
and its compatibility assessment. The canonical journal records execution and
finished-result owner acceptance; source synchronization alone is not acceptance.

## Company calendar correction — 2026-09-22

METRIC-030 revision `2026-09-22.1` requires once-only administrator configuration
in company settings, stable afterwards; calendar years remain universal. Reports
must not expose financial-year setup, current/pinned version controls or adoption.
Date filters, six grains and calendar/fiscal analytical basis remain available.
The [owner amendment](../../.codex/delivery/evidence/MS-004/MS-004-S05/owner-correction-2026-09-22.md)
supersedes only affected MS-004 D04/D08/AC-11 report UI clauses, preserving immutable
plan, prompt and historical proof. The settings page and API enforcement of
once-only setup are deferred; existing version-update endpoints retain compatibility
and are not claimed to satisfy that lifecycle. Internal result/calendar identity,
exact snapshots and authorization remain unchanged. No automatic report rebasing.

## Native configured report creation (W40)

Owner-authorized on 2026-10-03: the new and saved report paths share the configured
editor. [W40 ticket](../../.codex/delivery/tickets/W40-WORKSET-CATALOGUE-INTERACTIONS.md)
and [evidence](../../.codex/delivery/evidence/W40-WORKSET-CATALOGUE-INTERACTIONS/report.md#unified-creation-and-editing-2026-10-03)
own this bounded follow-up; no milestone state is changed.

- `POST /api/reports/v2/new/prepare` resolves an authorized dataset, pinned default
  calendar, presentation references and a blank/sales definition. References may
  be registered, but no document, document version or Saved View is created.
- `POST /api/reports/v2/new/apply` accepts creator mode at revision zero and uses
  the same calculation/binding verification as saved documents. It cannot target
  an existing report or change creator attribution.
- `POST /api/reports/v2/new/versions` accepts expected report/view revisions zero.
  One transaction creates the document, first configured version and companion
  Saved View. Document identity is stable through retry; creator is checked
  against the authenticated actor, never inferred from client attribution alone.
  The locked repository replay check handles overlapping requests. Changed
  payload under the same key is `IDEMPOTENCY_CONFLICT`; other stale creates are
  revision conflicts. Dataset/object/functional rights and CSRF are rechecked.

Native personal drafts have `base_snapshot_ref: null`. Migrated v1 reports retain
their exact non-null legacy base reference and original reader behavior. Native
personal worksets are not a published/shared document: non-creators cannot read
the personal overlay merely by receiving an object grant. A published native
reader projection and shared worksets remain outside this bounded follow-up, as
for the existing configured personal-overlay flow. This does not claim REPORT-019
completion. The UI still marks shared-workset capability unavailable.

Compatibility: old stored v1/v2 documents remain readable by the new server. New
endpoints are additive for existing clients; all repository generated TypeScript
clients are regenerated for the nullable base reference. An older server/client
that requires a non-null legacy base cannot read newly created native documents.
Thus rollback after native writes requires retaining the new reader or restoring
a pre-write backup; this local change does not establish mixed-version rollout
or production rollback readiness. No SQL schema migration or backfill is required.

## Composer foundation (MS-005 / C01)

The owner accepted WS-004 C01–C11 and delegated sequential technical continuation
on 2026-10-07. [Authority](../../.codex/delivery/evidence/WS-004/owner-continuation-2026-10-07.md)
changes the approval workflow for this scope, not product holds or publication rights.

[ComposerDefinitionV1](../../packages/contracts/presentation/composer.py) is an
unmounted `analytical-authoring/v1` contract foundation: stable ordered hierarchy,
closed chart/table bindings to the existing retail Analytics provider, typed grid
placement and presentation. Its input fingerprint is a grouping hint, never an
authorization or final result-cache identity. Legacy v1/v2 DTOs remain unchanged.
This does not implement a general writer, arbitrary providers or browser authoring.

The [complete clause inventory](../../.codex/delivery/evidence/MS-005/MS-005-S01/requirement-audit.md)
separates implemented subsets from missing proof/providers. The [transition design](../../.codex/delivery/evidence/MS-005/MS-005-S01/composer-design.md)
selects versioned reader/write/view dispatch, existing repository ownership,
creator/CAS/replay invariants and disposable migration/rollback proof for C02.
Existing migration 0012 restricts persisted contract_version values: new-format
writes need schema expansion and real migration evidence before activation.
Forecasting hold, shared-set ownership and later XLSX sequence are preserved.


## Composer vertical slice (MS-006 / C02)

[MS-006 v0.1.0](../architecture/planning/milestones/MS-006/plan.md) mounts the
C01 foundation through `/api/reports/composer/v1`. Definitions use
`analytical-authoring/v1`; immutable persisted draft responses use
`composed-report/v1`. The additive 0014 migration follows current 0013 and admits
that discriminator in the existing Presentation tables. It never rewrites old
payloads; downgrade refuses while new rows exist. Retain a compatible reader
after new writes. Only owned disposable migrations have been exercised.

Prepare, selected-block Apply, definition Save, editor/latest, exact snapshot and
block-result reads use request-scoped public Identity/Analytics/Artifacts ports.
Save validates references and persists graph/layout without calculation. Optional
result references are verified against exact block queries. Pending blocks remain
pending; reopening fetches saved results without Apply. Normalized result identity
and reuse remain Analytics-owned. Creator checks, current object/data permission,
CAS, identical-key replay and atomic latest-pointer updates remain mandatory.
Capabilities expose implemented workbook/chart/table/interactive support and
current edit/run permission. New documents never pass through old DTO readers or
writers unnoticed. Existing reports keep their original editor and stored bytes.

The browser entry is the report library's charts/tables document option on existing
report routes with `view=composer`. The common builder chooses subject/product,
metric/grain and supported store/period inputs. Per-block settings, result loading,
error/retry and selection are independent; duplicate inputs have fresh IDs.
Rendering reuses the established WorkspacePlot/WorkspaceTable path through typed
per-block projection. It adds no second arithmetic engine or ECharts option builder.
Full compiler convergence and other providers remain later WS-004 outcomes.

[Observed verification](../../.codex/delivery/evidence/MS-006/MS-006-S01/verification.md)
records real owned PostgreSQL/API/browser proof and failures/repairs. The
[canonical journal](../../.codex/delivery/ledgers/MS-006.md) alone determines
technical acceptance; this contract appendix does not preaccept the stage.
No full multi-profile, shared publication/view, forecasting, pivot, performance or
release claim follows from this bounded implementation.

## C03 hierarchy and presentation authoring — 2026-10-07

[MS-007](../architecture/planning/milestones/MS-007/plan.md) extends the same personal
composition path with chapter/page/section/block hide/lock and copy-origin metadata.
Absent added metadata remains absent on serialization, preserving older snapshot
payloads and idempotency hashes; explicit false/null is retained. Existing closed
schema validation, creator/current-source checks, immutable snapshots and CAS/replay
remain in force. Presentation locks are authoring safety, never ACL grants.

All three presentation profiles use the same graph and chart/table renderer. This
is profile composition support, not Research lifecycle, live Dashboard refresh,
publication or full content-provider acceptance. Workbook creator-only semantics
remain enforced for all current personal compositions. New fields evolve the
unpublished composer v1 in lockstep with generated clients; an old C02-only writer
is not claimed to support new node metadata. Existing released legacy v1/v2 routes
retain explicit format dispatch and their original payloads.

Pure graph transactions implement chapters, page groups, nested sections, stable
move/reorder/resize, independent copies with source-node and optional snapshot
lineage, hide/lock/unlock and delete. Grid uses twelve bounded columns with rejected
overlap; flow/narrative preserve logical order. Density and profile/layout changes
never enter Analytics identity. Compatible copied blocks reuse verified results.

Undo/Redo retains at most 50 transient authoring steps until acknowledged Save;
this history bound does not cap document pages or blocks. Local draft revision
increments for edits/history, while Save records the immutable durable revision.
Undo does not rewrite saved history. Reconciliation preserves draft/history under
fresh actor checks; actual access reset clears them. Removing the active page by
Undo moves navigation to a surviving page and preserves Redo.

The viewer mounts only the active authorized page. Search, grouped tabs and an
all-pages selector handle overflow, keyboard navigation and exact snapshot/page
links. Hidden nodes are omitted from the reader surface but remain author-manageable;
hiding is not a security or metadata-concealment boundary. Pointer drop and menu
commands share the same validation. See the [canonical journal](../../.codex/delivery/ledgers/MS-007.md)
for actual acceptance, and [verification](../../.codex/delivery/evidence/MS-007/MS-007-S01/verification.md)
for bounded proof; C10 retains full scale and accessibility qualification.

## C04 foundation: pure supported-provider scopes — MS-008-S01

[MS-008](../architecture/planning/milestones/MS-008/plan.md) introduces standalone
`composer-scopes/v1` and `store-filter/v1` contracts. S01 does not mount them in
an API or change existing stored composer payloads. S02 owns reader-before-writer
admission, current authorization, normalized Analytics identity and UI integration.
The full C04 outcome remains open for missing general provider capabilities.

The Store expression belongs to the Semantic public contract. It pins the semantic
dataset version and `authorized-store-set/v1` rule, and supports typed `store_in`,
AND, OR and NOT only. This is a lossless adapter to existing Store selections, not
the general FilterExpression v2 registry/evaluator. Unknown fields, channels, SQL,
relationships and other unsupported nodes are rejected, never dropped. Existing
Store provider value/cardinality constraints apply. Empty IN means empty set;
nonempty AND intersects, OR unions, and NOT complements only the provider-resolved
authorized Store universe. Every branch validates its values even if another branch
already determines the result. Mandatory source/system selections intersect outside
the expression and cannot be weakened by NOT/OR/replacement. The adapter operates
on dimension-ID sets, never business rows, and is not a substitute for the missing
safe-pushdown/Polars/DuckDB general provider.

Structural resolution follows document, chapter, page, outer-to-inner sections,
then block. Within a target, unique explicit filter order is used. Each replacement
names exact active ancestor bindings that explicitly allow replacement and are not
locked. Other ancestry, source and trusted constraints remain intersected. Replacing
an already overridden binding is invalid. Context fields (period, grain, calendar
reference/basis, temporal alignment) inherit independently; explicit child override
records the prior origin as overridden. Locked context fields reject overrides.
No implicit default introduces a new comparison mode.

Linked targets broadcast the binding's own expression directly; they do not copy a
source block's entire context or propagate implicitly through other links. Applicable
ancestry filters run first, then additional directly linked bindings in binding-ID
order; each binding is applied once. Linked bindings only intersect. Hierarchy plus
link edges must form a DAG, with valid scope kinds and block destinations. This
explicit non-transitive binding contract is not the C05 interaction dispatcher.

The resolver returns effective query inputs, active typed filters, applied/overridden/
locked/linked provenance and a dependency hash. Canonical Boolean child order and
Store values preserve meaning; active dependency IDs/schema/rule/dataset are pinned,
while title, density and grid placement are excluded. No-scope resolution leaves the
old query exact with no new digest. A filter cannot silently cross dataset versions.
S02 must derive and carry this digest through real normalized result/cache/snapshot
identity; the standalone field alone is not proof of that integration.

Pure S01 tests do not establish live access, API behavior, estimated rows, general
catalog/facets, windows/populations or unsupported comparison modes. Those remain
provider dependencies and separate acceptance obligations in the parent plan.


## C04 foundation: mounted scope and pair boundaries — MS-008-S02

The optional `scopes` envelope is admitted in composer definitions. Omitted fields
remain omitted; old unscoped input fingerprints and immutable snapshots retain
meaning. Authorable retail inputs reject a client-supplied provider `scope` field.
Presentation derives each selected block's effective query and dependencies;
Analytics independently applies current authorized Store universe and mandatory
source restrictions before normalizing `workspace-scope/v1` identity. The new
`scope_hash` is present only for scoped queries. Preflight, Apply, Save verification
and exact snapshot result reads use that same effective query.

`POST /composer/v1/preflight` resolves one selected block without calculating;
`POST /composer/v1/validate` validates the entire authoring draft. Current provider
capabilities explicitly cover Store/date, Boolean Store sets, existing calendar
and temporal modes, pair comparison, locked metric eligibility and reuse state.
Resource estimate is explicitly unavailable. Saved-snapshot block preflight uses
read authorization and cannot grant editing. Unrelated block semantic failures do
not prevent selected-block Apply/preflight, including with persisted locks. Global
graph validity and immutable persisted constraints still apply to every command.
Persisted locked filter bindings cannot change; context locked fields cannot change
or unlock, and surviving blocks cannot escape inherited locks by moving.

The optional `pair` selects two distinct existing block IDs. Explicit
`POST /composer/v1/compare` verifies current effective inputs, result artifacts,
report Store ceiling and dataset compatibility before calling the existing public
Analytics comparison port. The optional saved `comparison` is an immutable
`card-comparison/v1` artifact bound to exact selected blocks, metrics and results.
Save and read verify it without recalculating comparison values. Changed inputs or
results invalidate browser pair state; incompatible periods/grains/calendars/units
retain server reason codes and unavailable/descriptive status. The browser formats
server values without computing deltas, totals or alignment.

Editor scope drafts support inherited period/grain/calendar basis/temporal mode,
Store selection/NOT, explicit allowed ancestor replacement and direct linked targets.
General nested Boolean expressions received from a compatible author are preserved
but not flattened by this bounded editor. Scope changes validate without Apply;
Undo/Redo, copy and deletion preserve scope graph semantics. Copies receive fresh
local binding IDs, retain incoming direct constraints locally and do not copy
outgoing external side effects. Removing a pair member removes its pair selection.
Read-only snapshots expose the saved pair and effective-context inspector.

This is the supported-provider foundation, not full C04 acceptance. General field
registry/facets, relationships/sequences/aggregates, windows/populations, general
safe-pushdown provider and expanded comparison modes remain unresolved dependencies.
See [MS-008 plan](../architecture/planning/milestones/MS-008/plan.md) and
[canonical journal](../../.codex/delivery/ledgers/MS-008.md) for acceptance authority.

## Persisted Receipt filters — MS-011

The [mounted flat-filter contract](columnar-filter-execution-contract.md)
adds optional `receipt-filter/v1` inputs to composer queries. The immutable
composer definition carries the full typed expression and registry version; the
result identity pins its current provider/policy dependencies. Old absent-filter
queries retain their wire shape and normalized values. This is a Receipt provider
subset; it does not close the remaining C04 or later workstream outcomes.

## Receipt hierarchy — MS-012

`composer-scopes/v2` adds `receipt_filters` alongside unchanged Store and context
bindings. Every Receipt binding names a dataset, pinned registry/expression, target,
order and explicit link/replacement/lock rules. V1 reads retain their serializer and
resolver behavior; omitted legacy version defaults to v1. Older readers reject v2.
No downgrade drops Receipt expressions. Rollback requires preserving the v2 bytes
until a compatible reader is available; no data migration rewrites stored snapshots.

Receipt scopes follow the existing document/chapter/page/outer-to-inner section/block
ancestry and direct-link DAG. An explicit replacement must name an active ancestor
which allows replacement, uses the same dataset and registry, and constrains only
the same single field. Compound conditions on that one field may be replaced as a
unit; conditions spanning different fields cannot be represented as field replacement.
Store and Receipt bindings cannot replace each other. Locked inputs remain identical
and surviving blocks cannot escape them through structural moves. Current provider
permissions and mandatory source ceilings intersect outside all authorable conditions.

Presentation combines active Receipt conditions and the block-local input using AND,
then sends the effective query through the existing current-authorized provider. It
cannot silently skip an incompatible dataset/registry. Active Receipt dependencies
participate in normalized identity; upgrading the envelope alone leaves a block with
no applicable Receipt condition unchanged. Layout changes remain outside identity.
Copying a block preserves local and incoming direct constraints under fresh binding
IDs; outgoing links do not start targeting original peers from the copy. Pruning
and lock protection apply to both collections.

The shared field editor keeps draft conditions separate from scope settings. Updating
an entire scope validates the candidate on the server before committing the authoring
state; calculating affected blocks remains explicit. The effective inspector shows
the resolved Receipt expression and applied/overridden/locked/linked origins. Existing
Store controls preserve v2 fields when editing their own bindings.

See [MS-012 plan](../architecture/planning/milestones/MS-012/plan.md) and its
[canonical journal](../../.codex/delivery/ledgers/MS-012.md) for acceptance. This bounded
integration does not establish relational/aggregate/sequence/population semantics,
full Focus behavior, expanded temporal comparison, scale budgets or production delivery.


## Explicit previous/custom period comparison — MS-013

Optional `time_comparison` in workspace input and inherited context carries
`time-comparison-settings/v2`. It is mutually exclusive with a non-none legacy
alignment; an inherited legacy override clears new settings, and an inherited new
setting clears legacy alignment. Both controls share the same persisted lock boundary.
An explicit v2 `none` masks ancestors; absent context inherits. Existing absent-field
queries/results retain serialization and hashes, and older readers reject new fields.

Analytics resolves `previous_period` by explicit complete-calendar-bucket count or
local-date duration, and `custom_period` by its explicit inclusive range. Full-bucket
mode rejects unaligned ranges before Run. The current pinned UTC/Monday/month-based
calendar provider resolves actual dates (including leap and fiscal boundaries), with
half-open instants, duration and overlap disclosed. It does not claim other calendar
profiles or DST behavior. No automatic per-day normalization changes registered metrics.

`time-comparison-artifact/v2` is embedded in the existing immutable result manifest;
it binds both periods, exact evaluated dates, ordinal bucket pairs, coverage/reasons,
metric/dataset/calendar/filter/policy/request identity and a content hash. Both sides
use the same current-authorized input projection. Exclude suppresses incomplete deltas;
explicit-partial exposes observed deltas with reasons; comparable-elapsed-days uses
the shared leading complete prefix. Missing observations remain unavailable, zero
baseline suppresses only relative change, and unmatched buckets retain a missing side.

The block editor distinguishes inheritance from an explicit local choice. Explicit
changes write block-level context overrides; unrelated edits preserve existing base
query/context precedence, including legacy inputs and persisted locks.
The composer edits these settings per block or inherited context and displays actual
ranges, values and server deltas in tables/charts. It never labels these modes as
previous-year comparison. Save/reopen uses existing verification and immutable result
references. No new database or migration is introduced. Reader-before-writer rollout
must preserve new payloads until compatible readers are available after rollback.

See [MS-013 plan](../architecture/planning/milestones/MS-013/plan.md) and its
[canonical journal](../../.codex/delivery/ledgers/MS-013.md). This contributes only the
current provider boundary; full C04/C05–C11 and production delivery remain unclaimed.


## Explicit previous-year policies — MS-014

The mounted v2 temporal settings also accept previous-year same-date, complete
calendar-aligned, ISO-week-aligned, fiscal-period and comparable-elapsed-date modes.
Applicable leap/ISO53 policy is explicit; irrelevant policies are rejected. New
fields remain omitted for MS-013 previous/custom/none inputs and resolved artifacts,
so their prior bytes/values/hashes remain unchanged. The old `alignment` path retains
its exact prior behavior and is never silently upgraded to a new policy.

Date-mapped modes store every current date, its prior date or null, exclusion flag
and reason. Exclude removes unmatched leap/ISO53 dates from the compared current set;
merge-with-Feb28 groups both current dates, including across weekly boundaries, and
counts baseline Feb28 once. ISO mode uses ISO year/week/weekday, with no fallback
from week53 to week52. Explicit partial preserves unmapped current dates with missing
baseline coverage. A missing provider calendar map fails preflight. Full calendar/
fiscal modes use complete month/quarter/half/year buckets shifted twelve months;
they preserve actual leap bucket size and require the matching calendar basis.

Comparable elapsed-year mode requires the elapsed policy and evaluates the leading
complete mapped prefix on both sides. Empty mapping is an unavailable artifact;
no fake baseline envelope or zero is invented. Current totals remain distinct from
the explicitly disclosed evaluated comparison dates. UI tables/charts consume the
same backend paired buckets, date mapping and reason codes; expanded details expose
exclusions. Comparison policy/identity and both-period access rules remain pinned.

The builder distinguishes inherit and explicit local calendar basis as well as
comparison. Changed basis is a block-context override; unchanged base/context and
locked ancestor semantics survive ordinary edits. Scope validation enforces locks.

[MS-014 plan](../architecture/planning/milestones/MS-014/plan.md) and
[canonical journal](../../.codex/delivery/ledgers/MS-014.md) bind proof. The mounted
provider remains UTC/month-based; other profiles/DST, population comparisons,
export-channel parity and all remaining workstream assertions retain required proof.


## MS-015 pinned month-based time-zone calendars

[MS-015 v0.1.0](../architecture/planning/milestones/MS-015/plan.md) adds opt-in
`business-calendar/v2` without rewriting v1 UTC profiles or saved references.
Semantic accepts IANA-name settings and resolves package `tzdata==2026.3` TZif bytes
through its infrastructure port. Stored profiles contain bounded base64 rules,
SHA256 and package version. Calendar content identity includes those bytes. Public
update input rejects supplied TZif fields. Replay checks actor-bound original request
identity before loading rules, so a committed response remains replayable without
the rule provider. Existing row lock, expected revision and immutable JSON storage
remain; no migration is needed. Invalid zones return CALENDAR_TIMEZONE_UNAVAILABLE.

Analytics parses the stored bytes in memory, assigns receipt instants to local dates,
and resolves half-open midnight boundaries with earliest-instant repeated-midnight
policy. Nonexistent midnight/skipped dates return LOCAL_DATE_BOUNDARY_UNAVAILABLE;
interior dates are checked too. UTC instant subtraction records actual 23/25-hour
elapsed durations separately from local date count, with LOCAL_DAY_DURATION_VARIES.
Raw metrics are not normalized. Data-as-of stays UTC; registered Receipt date filters
retain UTC meaning. Source Calendar declares UTC dates: a local date has coverage only
if every intersecting UTC source day exists, and completeness only if all are complete.
COVERAGE_INTERSECTING_UTC_SOURCE_DAYS discloses this conservative basis.

The initial MS-015 report-mounted settings and explicit version-adoption controls
violated METRIC-030 and the already accepted 2026-09-22 correction. MS-016 supersedes
that UI/lifecycle, preserving the valid pinned-rule math and historical evidence.
New blocks use the configured default internally; existing blocks retain their pins.
Rendered results show zone and comparison UTC boundaries/elapsed hours.

The proof boundary is local published retail/month-based calendars. Other calendar
families, explicit provider calendar maps and population providers remain subsequent
C04 obligations; no complete COMPARE capability or production claim follows here.


## MS-016 once-only company setup and MS-015 correction

[MS-016](../architecture/planning/milestones/MS-016/plan.md) restores METRIC-030.
Its current evidence supersedes MS-015's setup/adoption conformance claims; consumed
MS-015 artifacts remain historical functional observations. The calendar section
is mounted only in UI-ADMIN-004 `/w/:workspaceKey/settings/policies`, gated by current
matching workspace and workspace.manage. Other workspace policy sections are not
claimed implemented. Reports expose no financial-year setup, version selector or
adoption command. Existing-block editing retains source pins without fetching the
current calendar. Internal new-block default resolution remains an authoring input.

The Semantic update endpoint intentionally rejects new writes after first setup.
Revision0 denotes system initialization; any positive revision denotes configured,
including older multi-version workspaces. Under the pointer row lock it checks
actor-bound idempotent replay, expected revision, then once-only state. A new request
after setup returns409 CALENDAR_ALREADY_CONFIGURED, even for the same profile. Exact
replay returns the original response; version reads and retained results are unchanged.
Concurrent first writes produce one success and one conflict. No migration/backfill,
reset endpoint or automatic rebasing. This is an explicit breaking write-policy change
required by the existing owner decision, not a new interpretation of old payloads.
The former 2026-09-22 API/settings deferral is resolved only for this calendar section.


## MS-017 correlated execution foundation (unmounted)

[MS-017](../architecture/planning/milestones/MS-017/plan.md) adds Semantic
FilterRelationshipVersion and Analytics relational-filter-execution/v2. Scoped
Boolean/predicate/exists/not_exists nodes pin node/scope IDs, parent and child scope,
entity, relationship version and field/registry versions. A child conjunction tests
one row; independent exists may match different rows. Root membership never expands.
V1 flat readers/meaning remain unchanged and reject correlated payloads explicitly.

Trusted grants carry current entity ceilings/immutable artifacts and authorized-scope
completeness hashes. The compiler emits only fixed identifiers and typed parameters.
Observed true match is sufficient for exists; otherwise incomplete history or an
unknown observed predicate yields unknown. Complete known absence yields false.
NOT/AND/OR use three-valued logic. Unknown is excluded from confirmed IDs and counted.
The real retail publication's business_history_completeness=unknown and quarantined
items are not certified absence; mounting a provider must honor that evidence.

The real DuckDB adapter shares the bounded hash-verified Parquet reader and restricted
connection with v1. It equally partitions total byte/row admission across entities
(conservative for skew), retaining any stricter per-input row/byte cap. Compound
execution obeys the minimum global/per-input node, depth, value, memory, thread and
timeout allowances; every input resource policy is also fingerprinted. It validates
scopes/versions/depth/node/correlation limits before
decode, and checks unique row IDs, parent-key cardinality, child references, fan-out
and estimated work before membership. Identity keys may not depend on unknown
property-history flags. Estimate version is sum-input-rows-times-correlations/v1;
this is a resource estimate, not a latency guarantee. Runtime deadline/cancellation
interrupt native work and cleanup closes the connection. Current grants are checked
again before delivery. Identity pins canonical Boolean tree, all entity/relationship/
artifact/coverage/policy/resource versions and actor/workspace/dataset.

This foundation has no new mounted endpoint, UI, result persistence or complete
FILTER capability claim. Genuine provider/catalog/preview/authoring integration is
required next; aggregates, sequences and population nodes remain subsequent work.


## MS-018 published receipt/item catalog and preview

[MS-018](../architecture/planning/milestones/MS-018/plan.md) mounts the genuine
published retail Receipt→ReceiptItem edge through current Identity, Semantic and
Artifact public ports. Semantic validates exact published keys/relationship policy
and exposes a bounded field allowlist, including decimal quantity (scale3) and item
amount/price (scale2). Root registry extends v1 receipt fields without changing them.
Child identity is the current retail profile's globally unique receipt_item_id/line_id.
No current product/customer attributes are backdated into event-time history.

The v2 reader accepts decimal128 storage with equal scale and narrower/equal precision,
widening safely to the logical18-digit type. This addresses Arrow's value-inferred
storage precision; it never narrows, rounds or changes scale. The mode enters v2
identity. V1 still requires exact physical schema and retains its existing hashes.

Only `/composer/v1/filters/v2/{dataset_id}/catalog` and `/filters/v2/preview` are
mounted. Workspace/actor/root Receipt are server-bound; strict receipt-filter/v2
cannot be passed to a v1 reader. Preview returns exact confirmed/false/unknown/
authorized counts and limitation codes, never membership IDs or artifact paths.
Catalog supports localized field/ID/type search and declares policy/relationship
versions. A child scope inherits its correlated parent's mandatory store ceiling;
namespace ceilings remain independent of author Boolean logic. No child-root query
or unscoped item facet is exposed. Catalog GET bypasses request authentication memo
at each authorization boundary so a revoked session cannot receive the catalog.

The publisher's transport-complete, quarantined, business-history-unknown evidence
is hashed and always remains uncertified absence under this provider contract.
Observed matches are confirmed; unresolved absence stays unknown and is disclosed
as RELATIONSHIP_HISTORY_INCOMPLETE. Even a future accounting flag cannot silently
upgrade this current provider's completeness meaning.

Proof uses owned disposable source/control PostgreSQL, genuine intake/publication/
manifest admission, real Parquet/DuckDB and authenticated HTTP, compared with
independent source SQL. This does not prove report persistence, editor/facets, browser
flows or deployment. Those follow next; remaining C04/C05–C11 are still required.


## MS-019 correlated report authoring and stored selection evidence

[MS-019](../architecture/planning/milestones/MS-019/plan.md) extends receipt_filter
with an explicit receipt-filter/v2 branch. Unchanged v1 input/result bytes omit new
optional fields. Old readers reject the new branch/evidence instead of dropping nodes.
Preview, facets and calculation share the same bounded normalized scoped executor.

Published compatibility_registry_versions pin the legacy Receipt field registry.
A mixed hierarchy may lift v1 root predicates only with that explicit validated
reference; field versions/null semantics remain unchanged. All-v1 composition keeps
its previous canonical payload. Each binding gets deterministic node/child-scope
rebasing, so repeated source trees remain independent and same-item conjunction
stays correlated. Request-local composition IDs exclude presentation block/source IDs;
a title change or duplicate with the same inherited bindings reuses the exact query.
The base predicate uses a reserved namespace distinct from UUID scope bindings.
Child-field coincidence never authorizes replacing an entire
correlated constraint; replacement remains one compatible root field. Current
provider checks reject invented/stale compatibility refs. Existing links, ancestor
checks and persisted locks remain enforced.

V2 facets return only bounded counts/search over confirmed matching roots. Root
fields count matching receipts; item fields count observed authorized positions
inside those receipts. Child namespaces and correlated parent store ceilings apply
before aggregation and pagination. Extra facet work is included in admission's work
estimate. Facets do not certify completeness or expose a child-root query surface.

The editor retains v1 drafts and explicitly adds receipt-item conditions to enter v2.
Same-item groups, independent exists, not_exists, AND/OR/NOT, stable IDs, readable
expression, preview, reset/undo and cancellation are distinct from applied settings.
The mounted catalog/facets remain server-authorized. During server validation,
opening another new block is disabled; the prior response cannot close that editor.

A v2 result stores optional receipt-selection-evidence/v2: confirmed/false/unknown/
authorized counts across the authorized dataset, filter identity and limitation codes.
Metric values use confirmed members in the requested period. The count scope is
explicitly distinct from that period. Unknown membership is disclosed in result
trust and temporal/pair comparison; valid observed-subset comparisons are descriptive.
Save/reopen preserves evidence and immutable identity; current authorization still
applies. Calendar coverage is not mislabeled as membership completeness.

The stage journal and final evidence own acceptance. This does not waive aggregate,
sequence, population nodes, remaining C04/C05–C11, or the once-only company calendar
policy established by MS-016. No production delivery follows from local browser proof.


## MS-020 scoped count and ratio execution foundation

[MS-020](../architecture/planning/milestones/MS-020/plan.md) adds an explicit
aggregate-filter-execution/v1 capability to the existing isolated DuckDB executor.
Existing receipt-filter/v2 and relational-filter-execution/v2 readers/schema remain
unchanged and reject aggregate nodes. No API/editor silently advertises new support.

Semantic FilterCountVersion pins relationship, child grain/field versions, unit,
null/empty/returns policy and versioned window field. CountInput binds that exact
published definition to trusted authorized observation coverage, observation-as-of,
knowledge-as-of and evidence hash. All enter identity. Count uses the child's unique
row ID grain; count_distinct supports up to four typed fields. Known nulls are either
excluded or propagate unknown by explicit definition; unavailable properties always
remain unknown. Current row ceilings apply before any count or distinct operation.

This first window capability is utc_date/v1: published date fields with explicit
half-open midnight UTC timestamp boundaries, no host-clock or timezone inference.
Parent- or child-date windows are supported. Observation/knowledge cutoffs preserve
exact aware UTC publication instants, including microseconds, without rounding.
Coverage must include the full requested
window and the relationship must certify completeness for the authorized child set.
A complete empty count is zero; incomplete observations or unknown eligible rows
produce unknown. No retail transport or quarantined history is upgraded to complete.

Scoped operands compare compatible units across separately pinned windows; count
ratios pin numerator, denominator and zero-denominator unknown policy. Comparisons
use exact bounded DECIMAL cross-products, never floating division. Every count adds
correlation/work cost and validated child scope; existing byte/row/node/depth/value,
fanout, timeout, cancellation and final authorization checks remain. Numeric policy
bounds cap admitted rows at one billion for this capability; scalar decimal values
are bounded before SQL. SQL identifiers are generated and values parameterized.

This is an unmounted foundation verified with actual synthetic admitted Parquet and
DuckDB. Genuine published provider/HTTP/editor/Save integration follows. Registered
financial metric operands, intraday/relative/calendar windows, sequences/populations
and remaining C04/C05–C11 remain required; there is no full FILTER-014 claim.


## MS-021 published aggregate report authoring

[MS-021](../architecture/planning/milestones/MS-021/plan.md) mounts explicit
receipt-filter/v3 and /composer/v1/filters/v3 catalog/preview/facets. Existing v1/v2
readers keep their schemas and refuse aggregate nodes. Current generated consumers
understand all three; no saved-payload migration occurs.

Semantic's public retail aggregate projection reads its own immutable publication
created_at and observed receipt-date bounds. It pins exact UTC snapshot cutoffs and
registered observed-item-row/distinct-product count policies to the genuine published
Receipt→ReceiptItem edge. These are all-observed-row counts under explicit predicates,
not certified financial measures. Invalid/missing/future metadata blocks the capability.
If a publication includes its current UTC day, count coverage stops at that day's
start while preserving exact as-of. Earlier closed days remain available; a snapshot
containing only its publication day has no count definitions and a localized
no-closed-day capability explanation. No empty or future coverage is invented.
Current retail history stays incomplete; transport/accounting flags cannot certify
absence or exact counts. Aggregate-only membership therefore remains unknown, while
Boolean alternatives can independently confirm members through published root fields.

The aggregate access composition first reuses current Identity/Artifact admission,
then validates the public count projection against those same entity bindings,
registries, relationships and compatibility reference. Final access revalidation
includes aggregate definitions, observations and evidence. HTTP root/workspace/actor
are server-bound; no arbitrary completeness, joins, IDs or storage paths are exposed.
Catalog delivery reauthenticates even for GET; cookie mutations require current CSRF.

Hierarchy combines v1/v2/v3 using the published legacy bridge and exact matching
registries. Rebase only request-local node/correlation scope IDs inside count and
ratio operands; leave policy/field versions and window cutoffs unchanged. Base uses
a reserved namespace independent of presentation IDs. Aggregate constraints never
qualify for single-root-field replacement. Existing links/locks/result reuse remain.

The existing editor explicitly adds count conditions, chooses registered count or
distinct-product definitions, row predicates, fixed half-open UTC-date windows,
scalar/scoped/right-window comparisons and ratios with independently scoped operands.
Readable policy, units, snapshot cutoffs and incomplete-history disclosure accompany
draft/applied/preview states in RU/EN. No client calculation or inferred calendar
basis is introduced. Current backend validates Preview and Apply; reset/undo and
cancellation preserve the parent definition until explicit apply.

Apply/Save/reopen use the existing immutable report and receipt-selection evidence;
unknown counts never become zero metric totals. This mounted increment does not
complete financial operands, relative/intraday windows, sequences/populations or all
remaining C04/C05–C11. The stage journal and final evidence own actual acceptance.


## MS-022 behavioral sequence execution foundation

[MS-022 plan0.1.1](../architecture/planning/milestones/MS-022/plan.md) adds explicit
sequence-filter-execution/v1 on the existing relational executor. The repaired
S01-R1 journal instance preserves the erroneous pre-implementation S01 as blocked
history; neither the historical plan nor its claim is retroactively accepted.

Semantic event definitions pin relationship, entity, row meaning, native UTC time
field version and null/observation policy. Trusted grants carry exact observation/
knowledge cutoffs, coverage and completeness evidence. Native timestamp(us,UTC)
columns are admitted from the same hash-verified Parquet bytes under existing size,
row and schema ceilings. They use a separate provider-owned projection; old flat
registry/value DTOs stay unchanged. No string parsing, timezone guessing, float
conversion or row-wise Python event evaluation occurs.

Each sequence has up to8 ordered steps on one declared parent→event edge. Positive
steps require strict increasing event time and inclusive min/max elapsed gaps from
the preceding positive step; identical times never gain order from IDs. Negative
steps name that preceding anchor and a half-open offset interval strictly after
it. A later positive occurs at or beyond the preceding negative interval end.
All events remain within the overall half-open window. Explicit same-property/
session bindings compare compatible versioned fields across named positive steps;
NULL or unavailable properties remain unknown.

Fixed windows preserve exact UTC instants. Relative windows pin publication
observation-as-of, elapsed microsecond offsets and exact resolved bounds under
publication_observation_as_of_elapsed_utc/v1. Both kinds validate cutoffs against
current trusted evidence. This does not claim local-calendar-relative semantics.

SQL uses generated identifiers and bound values, applies authorized child ceilings
before event candidates, and correlates each path/absence test to its declared
parent. Known positive witnesses may confirm a sequence with incomplete history.
Absence requires the full interval, relationship and event coverage; unavailable
time/properties or incomplete observations cannot certify it. Missing observations
that could hide a path conservatively yield unknown. Boolean NOT retains unknown.
Only root membership and coverage are returned, never event payloads.

In addition to existing node/depth/value/correlation, byte/row/memory/deadline,
fanout/cancellation and final authorization recheck, a pre-join estimate sums
parent_rows × max(1, child_fanout)^(positive_steps + has_negative_step) × total_steps.
The additional power accounts for negative probes per positive candidate; both fields
in a property binding must explicitly allow equality. The estimator version is
pinned in sequence-grant identity. The current evidence/hash/meaning, event-time
version, resolved window, anchor policy and effective rights also participate.
Old schemas reject sequence nodes; identities without sequence grants retain their
old payload. This foundation changes no HTTP, saved report or browser capability.
Actual synthetic trusted Parquet/DuckDB proof is distinct from the following genuine
published event provider and editor work. Full FILTER-015/C04 and C05–C11 remain open.


## MS-023 published customer event preview

[MS-023](../architecture/planning/milestones/MS-023/plan.md) adds the genuine published
Customer→Receipt event provider and separately versioned customer-event-filter/v1,
customer-event-catalog/v1 and customer-event-preview/v1. Composer HTTP exposes
`/filters/customer-events/v1/{dataset}/catalog` and `/filters/customer-events/v1/preview`;
old receipt filter endpoints/payloads keep their roots and schemas. Generated clients
include the new methods, but no report editor/persistence integration is implied.

Semantic owns the immutable projection: current Customer identity (no PII attributes),
Receipt and ReceiptItem, exact artifact hashes and namespace, nullable Customer→Receipt
and nonnullable Receipt→ReceiptItem meanings. Observed receipts use their native recorded
UTC receipt_datetime; these are published rows, not inferred lifecycle or status-change
events. Exact publication created_at pins observation/knowledge cutoffs; partial current
UTC days support native events even when date-based count windows have no closed day.
Current-only dimensions and unavailable historical event classification remain explicit.
Neither accounting nor successful intake certifies business history or absence.

The additive nullable relationship DTO admits a receipt with null customer_id as
unlinked while still requiring its namespace key. Unknown nonnull references and
partial/missing required keys fail. The old relationship DTO remains strict. Unlinked
rows have no parent fanout; their bytes/rows still count toward input/work ceilings.

Current Identity and immutable Artifact admission produce a separate trusted root
restriction: published customers having at least one authorized observed receipt.
SQL enforces that mandatory semijoin independently of the user expression, with receipt
store ceilings before root counting and sequence evaluation. It does not enumerate
customer IDs in Python or expose memberships in HTTP. Customer records with no authorized
observed receipt are outside this explicitly named universe, not claimed absent from
the complete customer population. Child item predicates inherit the correlated receipt
scope. Nullable policy, root restriction, registry/event versions, exact evidence and
current rights enter identity; final grant changes prevent delivery.

Catalog GET requires current analysis.read and reauthenticates before delivery; preview
also requires analysis.run and the resource run action. Cookie POST requires CSRF.
Workspace, actor and root Customer come from the server; typed requests cannot provide
access grants, history completeness or storage paths. Preview returns counts/coverage
and the explicit universe policy only. Genuine PostgreSQL/source/publication/Artifact/
Identity/DuckDB/HTTP proof is separate from forthcoming saved receipt-cohort projection
and mounted sequence authoring. Full Customer universe/population policies, FILTER-015,
remaining C04 and C05–C11 stay required.


## MS-024 receipt customer-history membership

[MS-024](../architecture/planning/milestones/MS-024/plan.md) introduces explicit
receipt-filter/v4 and cohort-filter-execution/v1. S01 provides genuine published
catalog, count-only preview and receipt/item facets at `/filters/v4`; saved report
ReceiptSelection and mounted sequence authoring are S02 obligations, not S01 claims.

A CustomerEventMembership leaf follows the pinned unique Customer→Receipt parent
and evaluates the nested sequence in the authorized observed-customer universe.
Its truth selects all authorized receipts of that customer, including receipts outside
the history window. Metric period is independent. Valid anonymous nullable references
remain unknown, also under NOT; nonnull orphans and missing required namespace keys
fail preflight. HTTP returns receipt counts and explicit universe/history limitations,
never raw Customer IDs. Customer facets and Receipt customer-reference facets are
rejected. A trusted facet allowlist derives from the verified old receipt/item
projection; catalog exposes its field IDs and identity pins the allowlist.

Each leaf has its own uncorrelated AS MATERIALIZED Customer CTE over the same admitted
immutable tables. Scalar unique-parent lookup preserves receipt grain. Global node,
scope/step identity, depth, correlation and parameter limits include all nested plans.
Prelude parameters precede main expression/ceiling and facet values. Cohort admission
charges both general/materialization work and the sum of sequence fanout estimates;
no repeated-customer optimization or wider resource allowance is assumed. Actual
DuckDB EXPLAIN and Parquet/provider tests establish the stated boundary.

The trusted provider verifies old receipt/item public registry fields, artifacts,
relationships and counts against the enriched customer-event projection. v4 preserves
receipt_registry_versions and promoted_registry_sets; every offered source map must
match that exact bridge, while v1 compatibility keeps its explicit legacy registry UUID.
Bridge/universe/event/source pins and current policy enter identity. Old schemas keep
their meaning and reject new nodes. Current Identity/store ceilings, Artifact admission,
CSRF, cancellation and final authorization recheck still apply. After the registry
bridge read, the provider resolves current Identity again without additional metadata
IO and compares the policy revision before delivering its grant. No historical event
classification, certified absence or full Customer population is inferred.


### MS-024 saved scopes and mounted sequence authoring

S02 admits v4 in saved ReceiptSelection and report projection. Mixed v1/v2/v3/v4
scopes preserve locks, exact registry origins and event/window/field bindings; only
local node/scope/step references are rebased. Absent optional v2/v3 legacy UUIDs do
not invalidate an exact registry bridge; conflicting supplied pins still fail.
Membership leaves cannot replace ancestor field constraints. Copy/title changes
preserve query identity, and old readers reject v4 without semantic downgrade.

The RU/EN editor provides positive/negative event ordering, fixed or publication-
relative UTC windows with exact microseconds, gap bounds and published property
bindings. Explicit Apply, Reset and Undo preserve draft boundaries; invalid visible
durations prevent submitting a stale valid value. Receipt/item facets omit customer
identifiers. Saved coverage separates confirmed, unknown and nonmatching receipts
from the independent metric period. No session provider or certified absence is
invented. A read-only actor may verify saved results with current analysis.read;
Apply and filter execution still require analysis.run. Genuine disposable API and
browser checks establish persistence/read/run behavior, not production delivery.

The owner boundary now stops after this stage: see the
[stop record](../../.codex/delivery/evidence/WS-004/owner-stop-after-current-stage-2026-10-07.md).
Remaining C04 and C05–C11 are not waived or started by this closure.


### Integrated report canvas (W42, 2026-10-10)

The owner-selected [W42 canvas](../../.codex/delivery/tickets/W42-COMPOSER-INTEGRATED-CANVAS.md)
uses `grid_columns: 24`; omitted values retain legacy 12-column semantics and
serialization. The editor converts legacy geometry in its draft, without rewriting
immutable snapshots. New snapshots may contain source-free `text` and `filter`
blocks alongside analytical chart/table blocks. Content blocks require no result.
All blocks share identity, ordering, placement, history and scoped locks.

A store control explicitly names analytical targets on the same semantic dataset.
Its selected stores intersect existing local/inherited restrictions; null adds no
restriction and an empty list matches no stores. Current authorization validates
the control dataset and selected stores, and effective queries remain subject to
Identity ceilings. Targeted result identity includes the control selection.

Compatibility: new readers accept old snapshots. Old readers cannot consume the
new block variants or 24-column geometry; deploy matching API/client versions
together. This is a local integration, not production rollout evidence.
See [verification and limitations](../../.codex/delivery/evidence/W42-COMPOSER-INTEGRATED-CANVAS/report.md).

W42 continuation: `metric` is a source-bound block using analytical totals and the same result/access contracts as charts and tables. `presentation.chart_type` selects line/bar; omission preserves legacy snapshot serialization. Local filter changes automatically calculate missing effective results. Metric and chart-style additions require coordinated API/client rollout; no immutable historical snapshots are rewritten.

Prepared reads (W42 reload correction, 2026-10-11): metadata-only scope preflight
uses the existing verified Store identity projection for queries without receipt
filters. Full calculation and receipt-filter provider paths are unchanged. Current
access, calendar, normalization and saved-result verification remain authoritative;
no raw-history decode is needed to normalize an unfiltered saved block's scope.

W42 visual inspector (2026-10-11): `presentation` additionally accepts optional
`description`, `show_title`, and typed `visual` settings. New fields are omitted
when absent in historical documents, preserving legacy serialization. Formatting
is excluded from analytical query identity; results are reused when only visual
settings change. The shared TypeScript chart compiler maps typed settings, never
stored JavaScript or raw ECharts options. Explicit combo blocks may display several
registered metrics from one source, retaining current/comparison pairs. Other
blocks continue to display only their bound metric. Server totals remain the
source of metric/gauge values; tables retain coverage evidence.

Compatibility is directional: new readers accept old data (`compatible-change`);
old strict readers reject new fields/types (`breaking-change` for rollback after
new writes). API and Web must be updated together; no historical snapshot rewrite
or new database migration is required. The chart catalog declares unsupported data
shapes explicitly; this continuation does not add hierarchy, graph, geographic,
distribution, pivot, or event-range providers or prove export-renderer parity.


### Empty block titles (2026-10-13)

BlockPresentation.title may be empty, with the existing 200-character maximum.
This permits title removal without deleting the block or its content. Document
and page title requirements are unchanged. Deploy updated validators/readers
before sending empty block titles; old validators reject those values.
