---
doc_id: CONTRACT-ANALYTICAL-AUTHORING-001
title: Governed population and analytical authoring contract
doc_version: 7
product_spec_version: 0.11.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [FILTER-013, FILTER-017, SEGMENT-029, SEGMENT-034, PIVOT-001, PARAM-001, COMPARE-011, ANALYTICAL-DOC-014, REPORT-015, REPORT-016, V1-AC-055, V1-AC-062]
status: accepted
acceptance_basis: owner-approved-product-requirements-2026-09-05
proof_boundary:
  label: target-contract-and-requirement-traceability
  exclusions: [implemented-api-schema, persistence-migration, runtime-compatibility, browser-proof, release-authority]
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
in customer rules. Additional Product/Store membership types, general manual
targets and new PDF/standalone HTML formats remain separate scope decisions.
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
