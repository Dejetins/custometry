---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-004",
  "title": "Personal report worksets / Configured metric workspace",
  "version": "0.2.1",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-003",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-003.md",
    "version": "3.0.2"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "7ef3c072a527627991036150d25e87adbbf8e60b",
    "evidence_refs": [
      "docs/architecture/planning/milestones/MS-004/plan.md#current-state-evidence",
      "docs/architecture/planning/milestones/MS-004/plan.md#input-provenance"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:b874b966471a2b3a4103b14dcca6fb2488305409e37d46ae262b94c454dfba86",
      "ids": [
        "METRIC-021",
        "METRIC-022",
        "METRIC-025",
        "METRIC-026",
        "METRIC-027",
        "METRIC-028",
        "METRIC-030",
        "CHART-021",
        "COMPARE-013",
        "REPORT-018",
        "ANALYTICAL-DOC-015",
        "WEB-ARCH-003",
        "WEB-ARCH-004",
        "A11Y-001",
        "I18N-001"
      ]
    }
  ],
  "decision_refs": [
    "FRAME/DEC-03",
    "FRAME/DEC-06",
    "WS-003/DEC-01",
    "WS-003/DEC-02",
    "WS-003/DEC-04",
    "WS-003/DEC-13",
    "ADR-0006",
    "ADR-0007",
    "WS-003/DEC-16"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "stage_ledger": ".codex/delivery/ledgers/MS-004.md"
  }
}
---

# MS-004 — Personal report worksets

## Identity

L3 for **WS-003/C01**, version **0.2.1**, **accepted**. The accepted product
basis is WS-003 **3.0.0** (acceptance-navigation patch **3.0.1**), incorporating the owner financial-calendar correction
to accepted 2.0.0 scope; the earlier 2.0.1 change was editorial navigation only.
The owner has accepted C01 scope, C01 → C02 → C03 order and the requirement for
company financial-year settings. On 2026-09-20 the owner explicitly accepted
this L3 0.2.0, its decisions and expected outcomes (MS-004/DEC-01).
The owner subsequently authorized prompt-pack/journal preparation and technical-branch
synchronization. Product-stage execution and deployment remain unauthorized.
This plan follows the [L3 template](../../framework-v1/04-milestone-template.md).

### Input provenance

At authoring entry HEAD was `7ef3c072a527627991036150d25e87adbbf8e60b` and the
assigned worktree was clean. The read-only handoff manifest's 21 full documents
and patch were SHA-256 verified; `git apply --check` succeeded, the patch was
applied here, and every transferred file matched its manifest hash afterward.
Patch SHA-256: `c90ddb1b6d04f84e91b22be3a787008e049d0d7ef3c7267896aee40359725f77`.
Accepted WS-003 2.0.0 SHA-256:
`ce629472d8fa0712470d39c1ce3d5d6047d10a90726d35ce0e1269c096caf6a7`.
The source checkout and snapshot were not modified. Those 21 incoming changes
are inherited context; this plan and the explicitly described navigation edits
are this task's authorship. Neither incoming checks nor historic pilot evidence
are verification of C01 implementation.

### Source pins

| Source | Exact input / use |
|---|---|
| [Parent WS-003](../../directions/DIR-004/workstreams/WS-003.md) | Accepted scope 3.0.0, DEC-01…16; financial-calendar correction from the owner, other scope retained |
| [Framework](../../framework-v1/README.md) | 1.0.0, doc_version 2; L3 and owner checkpoints |
| [DIR-004](../../directions/DIR-004/direction.md), [MAP-001](../../project-map.md), [roadmap](../../development-roadmap-v1.md) | Inputs 2.2.0 / 2.2.0 / doc_version 19; navigation amendments below do not accept the broader sequence |
| [Machine blueprint](../../../../../custometry-technical-blueprint-ru.md), [human explanation](../../../../../custometry-technical-blueprint-human-ru.md), [UI blueprint](../../../../../custometry-ui-blueprint-ru.md) | requirements_revision 2026-09-20.2; normative clauses, explanations and surfaces respectively |
| [Authoring contract](../../../../contracts/analytical-authoring-contract.md) | doc_version 10; owner-selected behavior and technical recommendations. Decisions below select C01 rules; they do not pretend recommendations were accepted wire schemas |
| [Refresh/recovery contract](../../../../contracts/report-refresh-serving-recovery-contract.md) | version 2; exact immutable result, access and recovery boundaries |
| [Context map](../../../bounded-context-map.md), [ADR-0006](../../../../adr/0006-analytical-document-retail-product-and-time-aware-segmentation.md), [ADR-0007](../../../../adr/0007-responsive-web-frontend-platform.md) | doc_version 14 / 2 / 2; ownership, common composition, frontend boundaries |
| [Operating model](../../../development-operating-model.md), [runtime](../../../development-runtime-contract.md), [gates](../../../tooling-gates.md) | doc_version 20 / 5 / 22; local acceptance separate from packaging |
| [Web source contract](../../../ui/custometry-web-implementation-source-contract-v1.md), [pilot](../../../ui/target-pilot/README.md) | doc_version 12; preserved ru/source.html SHA-256 b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700 |
| [Composition](../../../ui/drafts/metric-workspace-v1/README.md), [binding](../../../ui/drafts/metric-workspace-v1/source-binding.json), [QA](../../../ui/drafts/metric-workspace-v1/design-qa.md), [overview](../../../ui/drafts/metric-workspace-v1/evidence/overview-1920.png) | doc_version 4; accepted initial composition and exact index.html/composition.js/composition.css hashes in binding; synthetic data only |
| [Mindbox atlas](../../../ui/references/mindbox-metrics-2026-09-17/README.md) | doc_version 5; saved interaction references, not a new shell or provider |

## 1. Result and boundaries

| Item | Definition |
|---|---|
| Before / after | One saved fixed revenue line and three fixed totals → within an existing report, creator creates/copies/selects/orders personal worksets and independent metric cards, applies effective context, compares, saves and reopens exact configuration/results |
| Included | Exactly net revenue, receipt count, average receipt; repeated instances; searchable catalog; keyboard ordering; common date/store and per-card store restrictions; six grains; same-dates previous-year and two-card descriptive comparison; Apply versus Save; RU/EN; empty/error/stale/access states; creator guard from the first new write path |
| Deferred | Goals (METRIC-029, METRIC-031…035), shared worksets/adoption/reset (REPORT-019 and shared parts of METRIC-025/027), additional metrics, reusable segment implementation, arbitrary formulas, publication/export, scheduled recomputation, Forecasting, installation/release |
| Preserved | Modular monolith, six-table PostgreSQL intake, registered MetricVersions, admitted artifacts, PostgreSQL truth, Identity, report snapshots/CAS/idempotency, native pilot and typed bridge, existing ECharts renderer and upstream libraries |
| Missing proof inputs | No current runtime inspected. Stage S05 must provision task-owned local data/identity and record admitted IDs/hashes; unavailable infrastructure blocks runtime acceptance, not this plan. No credentials or deployment target are assumed |
| Authority | Current unit: L3 documentation and reciprocal maintenance only. Owner plan acceptance and separately authorized pack/journal preparation precede execution. MS-003 S05/S06 remain deferred |

### Requirement allocation

| Clauses | C01 obligation and decision | Deferred remainder |
|---|---|---|
| METRIC-025, METRIC-026 | Ordered localized personal worksets, independent IDs, immutable metric references and visible effective context; D01–D03 | Shared scope C03; population/target-action selectors unavailable, not fake |
| METRIC-027 | Search exactly three metrics; add/copy/remove/order cards and sets; keyboard alternatives; bulk store preview and atomic apply of valid edits; D01/D08 | Shared save C03 |
| METRIC-028, CHART-021, COMPARE-013 | One-card temporal and two-card descriptive modes; server values/deltas, explicit axes/reasons; D04/D05 | Arbitrary comparison modes and statistical/causal claims |
| METRIC-030 | Six grains with pinned company fiscal/calendar basis, UTC receipt dates and component-based ratios; D04 | No additional grain |
| REPORT-018, ANALYTICAL-DOC-015 | Creator plus functional/object/data checks for report definition/settings; reader view controls do not mutate definition; D06 | Shared-set read/version policy C03 |
| METRIC-021/022, WEB-ARCH-003/004 | Personal Saved View semantics, query/presentation separation, actual native pilot; D01/D08 | Shared-version adoption C03 |
| A11Y-001, I18N-001 | Keyboard and visible focus, accessible complete table, truthful localized states in RU/EN; AC-08 | No claim of application-wide accessibility certification |

### Current-state evidence

All code observations below are static at the baseline commit, not freshly run tests.

| Claim ID | Capability | Observation / evidence | Gap and resolution |
|---|---|---|---|
| MS-004/EV-01 | Report shape | `code_observed`: [domain reports](../../../../../packages/presentation/domain/reports.py), `validate_result`, `line_spec`, `composition`: sales-report/v1, exactly three metrics, daily grain and one revenue line | S01/S03 introduce discriminated v2; do not weaken v1 validation |
| MS-004/EV-02 | Persistence | `code_observed`: [ReportService](../../../../../packages/presentation/application/reports.py), [repository](../../../../../packages/presentation/infrastructure/postgres.py), [migration 0011](../../../../../migrations/versions/0011_presentation_drafts.py): owner-scoped reads, JSONB version payloads, immutable artifact commits before transaction, CAS and idempotency | No worksets or general authorized-reader integration. S03 adds explicit creator and public access boundary |
| MS-004/EV-03 | API | `code_observed`: [DTOs](../../../../../packages/contracts/presentation/__init__.py), [router](../../../../../apps/api/src/custometry_api/reports/router.py): strict v1 request/response, prepare/create/version/exact-preview | S01 preserves old routes and introduces explicit v2 paths; generated schemas/clients updated together |
| MS-004/EV-04 | Analytics | `code_observed`: [calculation](../../../../../packages/analytics_core/application/sales_report.py), [request](../../../../../packages/contracts/analytics/sales_report.py), [service](../../../../../packages/analytics_core/application/service.py): ≤366 inclusive days, one store, UTC, daily totals, endpoint-date year shift, result owner/policy hash | S02 adds store sets, six grains, per-day alignment, component/coverage projections and normalized reuse; v1 remains intact |
| MS-004/EV-05 | Catalog/artifacts | `code_observed`: [sales metrics](../../../../../packages/semantic_model/application/sales_metrics.py), [artifact adapter](../../../../../packages/artifacts/infrastructure/sales.py): immutable definitions EUR / receipt / EUR/receipt, completed-EUR eligibility, six Parquet inputs, content integrity | Reuse definitions and artifact adapter; no formula copying or replacement data engine |
| MS-004/EV-06 | Access | `code_observed`: [organization service](../../../../../packages/identity_access/application/organization.py) `decide_access` and `filter_visible_resources`, [policy](../../../../../packages/identity_access/domain/organization.py): deny-wins functional/object/data decisions; reports currently do not call this path | S03 wires an explicit public access projection, not direct Identity table reads; creator is an additional immutable predicate |
| MS-004/EV-07 | Web | `code_observed`: [ReportWorkspace](../../../../../apps/web/src/features/reports/ReportWorkspace.tsx), [PilotDocument](../../../../../apps/web/src/features/reports/PilotDocument.tsx), [seams](../../../../../apps/web/src/features/reports/pilot/seams.json), [port](../../../../../apps/web/src/features/reports/pilot/port-prelude.js): saved native document, generated runtime and typed result bridge | S04 changes cards/context/chart/table/save in one integration; no replacement shell; prototype arrays never become runtime data |
| MS-004/EV-08 | Real data coverage | `code_observed`: [seed](../../../../../deploy/demo-source/init/030_seed.sql) receipts cycle over 731 days from 2024-01-01; Calendar 2020-12-28…2025-12-31, complete before 2025-12-01. [integration oracle](../../../../../tests/integration/analytics/test_sales_report.py) already asserts comparable Jan–Nov 2025/2024 and source-SQL parity | Existing seed is two-period, not 2025-only. It does not prove full-2025 coverage, all store/day combinations or six new grains. S02/S05 pin counts/ranges and add deterministic edge corpus |
| MS-004/EV-09 | Visual basis | `documented_only` plus inspected saved overview: [composition QA](../../../ui/drafts/metric-workspace-v1/design-qa.md), [historical native proof](../../../../../.codex/delivery/evidence/MS-003/MS-003-pilot-native/report.md) | Historical runtime and synthetic design proof are distinct; S05 needs new real browser evidence |

### Dependencies and shared boundaries

| Dependency ID | Provider + required version | Required output / consumer | Needed before / proof | Integration owner |
|---|---|---|---|---|
| MS-004/DEP-01 | WS-003 3.0.0 | Selected C01 scope / whole milestone | L3; verified snapshot and DEC-01/02/04/13 | Presentation |
| MS-004/DEP-02 | [DIR-002](../../directions/DIR-002/direction.md) 2.2.0 capability basis | Existing retail-report/v1 six-entity admission / S02, S05 | Calculation; real intake and committed manifest proof during execution | Data contribution in MS-004, no separate connector project |
| MS-004/DEP-03 | [DIR-003](../../directions/DIR-003/direction.md) 2.2.0 capability basis | Result/metric projections / S02→S03 | Save binding; SQL oracle and result contract proof | Analytics |
| MS-004/DEP-04 | [DIR-001](../../directions/DIR-001/direction.md) 2.2.0 capability basis | Current access decisions / S03→S04 | Any v2 API activation; creator + denial tests | Identity and Presentation through public ports |
| MS-004/DEP-05 | [DIR-005](../../directions/DIR-005/direction.md) 2.2.0 capability basis, UI composition v4 | Preserved source and Web integration / S04 | Browser; source mapping plus real interaction evidence | Web |
| MS-004/DEP-06 | [DIR-006](../../directions/DIR-006/direction.md) 2.2.0 capability basis, runtime v5 | Existing local hybrid mechanism / S05 | Real proof; isolated source/control PostgreSQL, artifact root and principals | Local integration |

DIR-004/MAP 2.3.0 add the owner fiscal-calendar correction; other direction
providers retain their earlier capability/version basis. These are contribution dependencies,
not prerequisites to finish all six directions. Hard graph is S01→S02→S03→S04→S05.
MS-003 S01–S04 are existing foundation evidence; its S05/S06 are not dependencies.

## 2. Implementation decisions

All MS-004/Dxx rules are **accepted L3 design decisions** under MS-004/DEC-01.
They constrain later authorized implementation; acceptance does not prove implemented
contracts or authorize stage execution. No new ADR is needed: ownership and dependency
direction remain those of ADR-0006/0007.

| ID / boundary | Current → selected target and reason | Alternative / consequence | Compatibility / proof |
|---|---|---|---|
| MS-004/D01 Configuration | Fixed composition → typed configured-report/v2 and composition schema 2, stable workset/card IDs and personal Saved View binding inside existing Presentation aggregate | Separate workset service or formula copies add lifecycles without need; rejected | New version; legacy read mapping and duplicate/copy/reopen tests |
| MS-004/D02 Storage | Existing document/version JSONB → additive v2 discriminator and Saved View tables, immutable creator attribution | Rewriting old snapshots destroys reproducibility; rejected | Additive migration, new-reader/old-data proof, restricted rollback |
| MS-004/D03 Effective context | One store/result → canonical intersected store set and exact per-card bindings; equal contexts reuse computation | Hashing card IDs would duplicate work; excluding policy would leak results | Versioned identity, disjoint/duplicate/revocation cases |
| MS-004/D04 Calendar | Daily only → versioned workspace fiscal settings, UTC/ISO weeks, pinned fiscal/calendar quarters/half-years/year, clipped buckets, per-day previous-year mapping | ISO-week remap silently changes comparison; rejected | New analytics version; edge-day/ratio SQL oracle |
| MS-004/D05 Comparison | One temporal line → typed one-card temporal or two-card descriptive projection and ChartSpec v2 | Browser deltas and invented cross-unit subtraction rejected | Strict pairs, units, unavailable reasons and table/tooltip parity |
| MS-004/D06 Access | Owner-only repository plus permissions → immutable creator guard and public current-access checks, separate view operation | report.manage/admin/department bypass violates REPORT-018 | Target author policy break is deliberate; actual v1 owner guarantee preserved |
| MS-004/D07 Consistency | One result snapshot → complete manifest set per Save, CAS/idempotency across whole revision | Per-card partial Save risks mixed snapshots; rejected | Fault injection before commit, retry and artifact integrity proof |
| MS-004/D08 Web | Fixed pilot surfaces → coherent workset/card/context/comparison/save integration in existing pilot and bridge | New similar shell or piecemeal visual polish creates rework; rejected | Source fidelity plus new browser/API proof |

### D01 — Configuration, API and domain ownership

Presentation owns report definition, analytical composition, workset/card instance
configuration, Saved Views, revisions and snapshot bindings. Semantic Model owns
MetricVersion and MetricGroupVersion; Analytics owns effective context, numeric
results and comparison artifacts; Artifact Lifecycle owns committed bytes and
manifests; Identity owns effective access. `apps/api` composes adapters. No context
queries another context's private tables.

Use strict discriminated contracts; unknown fields/versions fail validation.
New mounted paths under `/api/reports` are `/v2/{report_id}`, `/v2/{report_id}/apply`,
`/v2/{report_id}/versions`, `/v2/{report_id}/snapshots/{snapshot_id}` and
`/v2/{report_id}/saved-views` (POST/GET own), plus
`/v2/{report_id}/saved-views/{saved_view_id}/versions` (POST).
Register static `/v2` routes before legacy `/{report_id}` routes.
C01 starts with an existing report; creation remains the existing supported v1
path. Do not add a second report lifecycle. The v2 GET response exposes
`capabilities` for definition_edit, view_apply, saved_view_save and exact_preview.
These describe checked permissions, never replace server checks.

| Contract | Selected shape and invariants |
|---|---|
| `configured-report/v2` definition | `schema_version`, `report_id`, server-owned `creator_principal_id`, title (1–200 chars), immutable `semantic_dataset_version_id`; `common_context` with inclusive ISO dates and `store_ids: null \| string[]`; `grain: day\|week\|month\|quarter\|half_year\|year`; `calendar_ref:{version_id,content_hash}`, `calendar_basis:calendar\|fiscal`; `worksets: Workset[]`; `default_workset_id`; existing brand/company references |
| `Workset` | UUID `workset_id`, `name:{ru,en}` (each nonblank, ≤200), `visibility:personal`, server-bound owner principal; ordered `cards` array. Array position is canonical order; no conflicting numeric order field |
| `Card` | UUID `card_id`, `metric_ref:{metric_id,version_id,content_hash}`, `local_store_ids:null\|string[]`, `population_binding:null`, `target_action_binding:null`. Non-null latter bindings rejected as unsupported in C01. Metric label/unit/format come from registry; copy uses new instance IDs and the same metric reference |
| Identity | Client-generated UUIDv4 for unsaved instances, validated for uniqueness within report. Moving/editing preserves IDs; copy workset regenerates workset and every card ID, copy card regenerates card ID. Deleted IDs never reassigned. Copy remaps internal selection references to the new IDs; IDs do not imply authorization |
| `AnalysisSelection` | Tagged union `{mode:single,card_id,temporal:none\|previous_year_same_dates,display:series\|delta_trend}` or `{mode:pair,left_card_id,right_card_id,display:series}`; different card IDs required in pair; both in active workset |
| Apply request | `contract_version:configured-report/v2`, `base_revision`, definition candidate for creator, or restricted `view_override` for reader, plus selection. Reader override accepts only dates/stores/grain/selection/display over authorized base cards; rejects definition fields |
| Apply response | `configuration_hash`, normalized definition/view context, `bindings_by_card`, typed comparison, ChartSpec references, `base_revision`, access fingerprint and aggregate status; no durable report revision. Identity includes all worksets' cards needed for Save, not just the selected chart |
| Save request | `contract_version`, complete definition candidate, `expected_revision`, `expected_saved_view_revision`, UUID `idempotency_key`, and result/reference IDs from a successful Apply; server regenerates/validates hashes and exact bindings. Never trust client numbers, manifests, actor or policy hash |
| Save response | Existing report/revision/version/snapshot/author fields, strict composition v2, full configuration, all card bindings, personal Saved View version reference, complete root/page manifests. Decimal values remain canonical strings; locale is rendering only |

Bound resource policy for this slice: retain at most 366 inclusive current days;
maximum 20 worksets, 50 cards per workset, 200 total cards/report, 1000 unique store
IDs/request, and a 1 MiB JSON configuration body. These are accepted engineering
limits, not new product promises. Validate before calculation; return typed
`WORKSPACE_LIMIT_EXCEEDED` with the limit name and no partial mutation. Empty set
and zero-card worksets are valid and render onboarding; empty workset arrays have
null default/selection and no numeric bindings. No truncation or invented first card.
Input store IDs are strings ≤128 chars, unique after canonicalization.

**Saved View / MetricGroupVersion / AnalyticalDocument alignment.** A workset is
a versioned presentation override in the report's common AnalyticalDocument;
it is not a MetricGroupVersion or a new metric group registry. Explicit workset
headers and card order preserve the selected group boundaries. Existing immutable
MetricGroupVersion references, when present, remain unchanged. C01 does not create
new semantic groups. The report creator's personal workset configuration is saved
with the new document revision and an associated personal Saved View version in
the same Presentation transaction. Saved View is the existing conceptual object,
now given its bounded persistence implementation; do not invent ReaderDraft or
another competing view entity.

A Saved View binds owner, workspace, report ID, exact analytical-document version,
page/result scope and immutable version/revision. Its typed payload separates
`query_context` from `display` (active workset/card selection, order/visibility of
already authorized cards, representation, density). Creator definition Save may
include the complete workset configuration; reader Save view can store only
permitted overrides over an accessible base definition. Reader changes never
create/modify cards, formulas or report settings. Each view has its own revision
CAS and idempotency namespace; it does not bump the report revision. Apply of a
reader query still resolves a new server result. Display-only changes require
no compute. No automatic switch to a new document version is implemented.
The creator's companion Saved View has UUIDv5(report_id, `personal/<creator_id>`).
Its configuration is referenced by document version/hash, not maintained as a
second editable copy. Definition Save checks both expected report revision and
expected Saved View revision, then advances both atomically. Separate Save view
checks only view CAS and pins the existing document version; a subsequent report
Save with stale view revision returns `SAVED_VIEW_REVISION_CONFLICT`.

Private worksets are returned only to their owner; C01 creates no audience grants
and exposes no private workset to another report reader. Such a reader uses the
existing authorized base composition, adapted to stable cards, and their own
view. Shared worksets and their adoption/reset remain C03.
To make that boundary exact, the first v2 revision pins `base_snapshot_ref` to the
existing v1 base snapshot; later personal revisions retain that reference. Readers
of the base report receive that authorized base version and its actual revision,
not the creator's private v2 overlay. Exact private v2 snapshot requests from
non-owners return 404. Reader Apply/Save view bind that base document version and
its stable adapted cards. Base access still requires an existing explicit grant
and data access. This reference is ordinary snapshot lineage, not a new draft
entity, shared set or implicit publication. Updating a shared base belongs to C03;
C01 personal Save never silently updates what another reader sees.

**Public ports.** Extend `packages/contracts/presentation` with versioned request/
response/domain ports: `WorkspaceCalculator.apply(context, metric_refs, selection,
access)` implemented through Analytics, `WorkspaceResultReader.verify(binding,
access)`, existing `SnapshotArtifacts`, `ReportRepository` and `SavedViewRepository`.
Analytics owns `WorkspaceResultV2`/`CardComparisonV1` in
`packages/contracts/analytics`, reuses `SalesSemanticPort.sales_projection` and
`SalesArtifactPort`, and exposes `run_metric_workspace` / `get_metric_workspace`.
Add explicit `/api/analytics/metric-workspace/v2` run/get routes for that projection,
using the same service as report Apply; no duplicate calculations in Presentation.
Direct Analytics callers still receive Identity checks for dataset/result scope.
The strict `WorkspaceResultV2` envelope has `schema_version:metric-workspace/v2`,
`result_id`, `request_hash`, `policy_hash`, semantic dataset/publication reference,
`effective_context`, metric/component references, `buckets`, `totals`, `coverage`,
`comparison`, `lineage`, `trust` and committed `manifest`. Each bucket exposes the
D04 boundaries, per-metric decimal-or-null values and explicit state; totals use
the identical metric keys. Each `CardResultBinding` stores `card_id`, metric
version/hash, result ID/schema, manifest ID/hash, effective-context hash, bucket
projection, unit/format and readiness (`ready|no_data|comparison_unavailable`).
No failed state can be admitted as a saved binding. `ComparisonArtifact` carries
its own manifest and both parent result references; exact render projections use
those IDs, never mutable latest-result lookup.

The catalog/context endpoint v2 projects exactly the registered three definitions
and authorized stores with version/hash/unit/format/eligibility. Public result
projections carry source bindings, coverage, data-as-of and artifact references;
no source rows, private repository records or executable chart options cross ports.

### D02 — Persistence, legacy and recovery

Reuse `presentation_documents`, `presentation_versions`, `presentation_references`
and `analytics_sales_reports` JSONB payloads; do not add a workset table or data
service. Planned migration `0012_metric_workspace` follows observed head 0011
(recheck the head at execution; choose next free revision if it changed).

- Add `presentation_documents.creator_principal_id` nullable, backfill from the
  existing immutable owner field, validate then set NOT NULL with Identity FK.
  Add a DB trigger rejecting creator changes after insert. Do not reinterpret
  organization ownership transfer as creator transfer.
- Add `presentation_versions.contract_version text NOT NULL DEFAULT 'draft-report/v1'`
  constrained to the two supported report versions. Add analogous
  `analytics_sales_reports.contract_version` default `sales-report/v1` admitting
  `metric-workspace/v2`. Old JSON payloads and artifact bytes remain untouched.
- Add `presentation_saved_views(id UUID PK,workspace_id,owner_principal_id,document_id,
  revision INT >=0,latest_version_id UUID)` and
  `presentation_saved_view_versions(id UUID PK,saved_view_id,revision INT >0,
  document_version_id, idempotency_key UUID,request_hash CHAR(64),payload JSONB)`.
  FKs bind view→report and view-version→the same report's document version;
  uniqueness `(saved_view_id,revision)` and `(saved_view_id,idempotency_key)`;
  composite latest FK as for reports. Payload pins exact result/manifest scopes.
  Index own-view listing by workspace/owner/document. No shared audience column.
- Existing reference kinds suffice: ChartSpec v2 is discriminated by its payload
  version, not another registry. Analytics request hashes include contract version,
  so existing unique request identity remains usable.

New readers dispatch on version. v1 exact previews use the original strict
validator and original artifacts. A v2 editor projects a legacy report into one
personal workset with three stable cards: UUIDv5(report_id, `legacy/workset`) and
UUIDv5(report_id, `legacy/card/<metric_id>`). Context, metric refs, defaults and
daily result map without changing historical bytes. Selection defaults to revenue.
Opening requires no compute. The first edited Save requires explicit v2 Apply,
creates revision N+1 and new root/page artifacts; never backfills v2 values into
an old snapshot. New reader can open both exact snapshots afterward.

Old v1 API clients on the new server can still read/write v1 reports and exact v1
snapshots. Once latest is v2, v1 latest/update returns
`409 REPORT_VERSION_UPGRADE_REQUIRED`; it must not silently downgrade or filter
out the document. Old saved snapshot URLs remain valid subject to current access.
New Web against an old server shows unsupported capability, retains old preview,
and disables v2 edits. No old binary/new-data compatibility is promised.

Rollout order: migration → dual-version backend → regenerated v2 client/UI →
enable v2 writes after S03 contract/database proof. Before any v2 write, code can
roll back while additive schema remains. After v2 writes, keep a dual reader and
use forward repair; lossless old-binary rollback is unsupported. Downgrade rejects
any v2 report/result/Saved View records. A separately authorized recovery can
restore a coherent pre-upgrade PostgreSQL backup plus retained artifact set,
explicitly losing post-backup changes; it is not the normal edit undo mechanism.
The preserved `base_snapshot_ref` is also a root dependency and must remain
retained/authorized; reader views cannot outlive their actual artifact bindings.
No new backup tool, scheduler, queue, worker, outbox event or remote side effect.

### D03 — Effective context and reproducible identity

Normalize on the server in this order: authenticate/current access → resolve
pinned dataset and metric definitions → fixed completed-EUR eligibility → common
period/stores → local store restriction → materialize effective context.
`null` means inherit/all allowed; `[]` means explicitly empty, never all. Common
and local store sets are sorted/deduplicated; effective stores are their intersection
with the allowed dataset scope. Unknown IDs fail `STORE_NOT_AVAILABLE`; explicitly
denied IDs fail `FORBIDDEN` rather than silently disappearing. Disjoint valid sets
return `no_data/EMPTY_EFFECTIVE_SCOPE`, not an exception or broader query.
An inherited set and an explicit equivalent set share effective identity, while
the saved configuration retains the user's inheritance intent.

Canonical JSON uses sorted keys, UTF-8, no NaN/Infinity, ISO dates and sorted
sets; decimal values use normalized non-exponent strings. Hash this tuple:
`contract/calculation version, workspace, actor access partition, current policy
fingerprint, semantic dataset version/publication hash, six source artifact hashes,
source Calendar version, business-calendar version/hash and basis, metric version/hash plus ratio component versions, eligibility,
effective stores, exact dates, grain, calendar policy, comparison/alignment policy`.
Card/workset IDs, labels, ordering, locale, theme and chart selection are excluded.
Each card binding still has its own card ID/configuration hash and exact metric
projection. Thus repeated cards remain independently editable but equal normalized
contexts reuse the same result/artifact within the same access partition.

Batch Apply groups equal source/period/store/grain/alignment/access contexts once,
aggregates the registered component tuple once, and projects requested metric
versions; a changed card affects only its bindings. Persist immutable content-based
results through the existing uniqueness/winner/verification path. Do not claim
cross-user cache reuse: C01 partitions reuse by actor and policy. Repeated concurrent
requests may do duplicate CPU work but converge on one admitted result identity;
no new single-flight service. Policy fingerprints come from the public access
projection, include policy versions and allowed scope, and are rechecked on reuse.

### D04 — Calendar, aggregation and temporal comparison

The owner correction makes the fiscal year a **base company/workspace setting**,
not a card parameter. This replaces the January-only decision in L3 0.1.0.
Semantic Model already owns business-calendar meaning; Identity controls who may
change it. C01 includes the bounded settings API and form, not a full administration
programme. One calendar default per workspace represents the company for this
slice; no new legal-entity hierarchy or per-department calendar engine is introduced.

**Selected initial profile:** `business-calendar/v1`, `kind:month_based`,
`fiscal_year_start_month` integer 1…12, `fiscal_year_start_day:1`,
`year_label:start_year|end_year`, `timezone:UTC`, `week_start:monday`.
Timezone and week start follow the existing receipt metric UTC/ISO basis;
no timezone conversion option is introduced. Year label defaults to `end_year`;
January start is the Gregorian-compatible default. Month-based fiscal years cover
non-January starts without inventing 4-4-5/52-53-week or mid-month semantics.
Those calendars require a future explicit profile and are rejected as unsupported,
not approximated. The owner has not supplied a particular company's start month;
that is a runtime setting, not a planning blocker. UI explains the supported profile.

**Settings lifecycle and port:** Semantic Model owns immutable
`BusinessCalendarVersion` (UUID, workspace, content hash, typed profile, creator,
created-at, previous-version reference) and a workspace default pointer/revision.
Use `WorkspaceCalendarPort.get_default(workspace,actor)` / `get_version(ref,actor)` /
`update_default(profile,expected_revision,idempotency_key,actor)` through public
Semantic contracts. Add `GET /api/semantic/workspace-calendar/v1` and
`POST /api/semantic/workspace-calendar/v1/versions` plus exact-version GET.
GET requires workspace.read and current workspace access; POST requires
workspace.manage and current administrative object/access checks, CSRF and CAS.
`report.manage` or being a report creator alone does not authorize settings edits;
authorized administrators do not thereby gain report authoring rights.
Return strict version/ref/profile/revision DTOs; invalid profile →422, stale
revision/key mismatch →409, denied access →403. Same key/body replay returns its
original version after access recheck. No arbitrary JSON settings or new service.

The planned additive migration creates Semantic-owned
`semantic_business_calendar_versions(id,workspace_id,content_hash,profile_json,
created_by,created_at,previous_version_id,idempotency_key,request_hash)` and
`semantic_workspace_calendar_defaults(workspace_id PK,revision,version_id)`.
Version/default FKs enforce same-workspace identity; `(workspace_id,idempotency_key)`
is unique. Update default and insert immutable version in one Semantic transaction.
Backfill a deterministic January/UTC initial version per existing workspace;
workspace initialization invokes the same idempotent public provision operation
for new workspaces. Historical rows/snapshot/artifact bytes are untouched.
Deleting a referenced calendar is forbidden. Rollback rules for v2 writes in D02
include these tables and calendar references; before custom-setting writes, the
additive default may remain on old-code rollback, but old code must not be exposed
as supporting custom fiscal settings. After custom writes, use forward repair.

**Default versus pinned:** a newly configured report uses the current workspace
version and fiscal basis (January produces identical boundaries). Legacy report
adaptation pins the initial January version with `basis:calendar`; old snapshots
remain v1. An existing report retains its pin even when the administrator changes
the default. The editor shows current and pinned versions and offers explicit
creator-only adoption; preview affected labels/boundaries, then Apply and Save a
new report revision. Readers cannot adopt a new policy or change basis through
view overrides. There is no automatic recomputation, old-result relabeling or
retroactive rebase. Saved Views, comparisons and future goal periods pin the same
version/basis. A workspace default change during Apply–Save does not invalidate a
valid pinned result; implicit `latest` references are forbidden at Save.

**Bucket algorithm:** convert receipts to UTC dates and inclusive inputs to
`[start 00:00 UTC,end+1 day 00:00 UTC)`. Day, ISO Monday–Sunday week and calendar
month boundaries are unchanged. With `basis:calendar`, quarters start Jan/Apr/Jul/Oct,
half-years Jan/Jul, years Jan 1. With `basis:fiscal`, for date d find the most recent
first day of `fiscal_year_start_month` at or before d (F). Fiscal year is
`[F,F+12 months)`, half-year index is floor(month_offset/6)+1, quarter index is
floor(month_offset/3)+1. Bucket boundaries are F plus the respective 6- or 3-month
multiples. Date arithmetic uses months, not fixed 90/180/365-day durations.
FY label uses F.year for start_year, or `(F+12 months−1 day).year` for end_year.
For April start/end_year labels: FY2026 = 2025-04-01…2026-03-31, Q1 = Apr–Jun,
H1 = Apr–Sep. January's FY2025 still means Jan–Dec 2025.

Each bucket includes exact `bucket_start/end_exclusive`, clipped
`effective_start/end_exclusive`, `is_partial_bucket`, calendar version/basis,
fiscal year/quarter/half index when applicable, coverage and unit-bearing values.
Chart/table/Focus/tooltip show the same FY/Q/H labels **and actual dates**; a fiscal
label never hides the basis. Locale changes only translation/format. A clipped
bucket is not necessarily incomplete data: Calendar's completeness declaration
is independent of fiscal boundary policy. Keep both source Calendar artifact ID
and business-calendar version/hash in lineage; no rewrite of imported Calendar
is needed for a workspace setting. Retain daily components for aggregation.

Receipt count is distinct `(source_system_id,receipt_id)` at eligible header grain;
revenue is decimal sum of eligible header net amount. Average receipt is summed
revenue / distinct receipt count at the requested bucket or full period. Never
average daily averages; do not multiply rows through ReceiptItem/Customer/Product.
Current nonempty partial data may show observed values labeled partial; comparisons
need both sides complete. No eligible rows retains registered `empty_is_unavailable`
(null, not zero); actual zero revenue with eligible receipts remains zero. Every
bucket and total reports expected/calendar/declared-complete/observed days.

`previous_year_same_dates` maps each current date to the same month/day in year−1
**before** grouping, then assigns that baseline day to the current date's bucket.
Weekly values therefore use matching dates, not last year's ISO week number.
Fiscal buckets likewise group mapped baseline days by the current bucket under
its pinned calendar. This remains same-dates comparison, not the separate
`previous_year_fiscal_period` mode. A changed fiscal start/basis between two card
bindings gives `CALENDAR_MISMATCH`; explicitly reapply both to one policy before
comparison. Same-dates comparison never consults the current workspace default.
Persist exact current→baseline day mapping and original baseline dates/ranges;
label chart x-axis by current dates and identify alignment in tooltip/table.
Feb 29 with no same date has `LEAP_DAY_SAME_DATE_UNAVAILABLE`: do not clamp to Feb 28,
duplicate a day or silently omit it. The affected comparison bucket and full-period
delta are unavailable; unaffected complete buckets may compare. When current is
non-leap and prior is leap, prior Feb 29 has no mapped current day and is excluded
with `BASELINE_UNMAPPED_LEAP_DAY_EXCLUDED` disclosure. Baseline totals sum only the
mapped date set. Year-crossing weeks follow this mapping too. Missing/incomplete
calendar, unavailable values or mismatched metric/coverage basis block the affected
comparison; historical v1 endpoint behavior stays unchanged.

### D05 — Typed comparisons and rendering

`CardComparisonV1` contains mode, left/right card references (temporal right is the
same metric in mapped prior dates), result/artifact IDs, exact metric versions,
units/formats, current period, grain/business-calendar version/basis/alignment, per-bucket and total typed
values, coverage, `comparability_status`, deltas and reason codes. Analytics creates
and admits this immutable projection; Presentation binds it and compiles renderer-
neutral ChartSpec `2.0.0` with series/artifact/field references. Chart/table/Focus/
tooltips consume the same server values. ECharts receives compiled options only.

| Pair | Display / delta rule |
|---|---|
| Same metric/version, different cards/stores | Comparable periods, grain/calendar and coverage: one unit axis; absolute `left-right`; relative `(left-right)/abs(right)*100` if right is present and nonzero |
| Different registered metrics | All three catalog combinations may be shown descriptively with explicitly labeled separate axes (EUR, receipt, EUR/receipt). No cross-unit subtraction or percentage: `UNIT_MISMATCH` deltas unavailable; neither correlation nor causality claimed |
| Different dates/grain/calendar or incompatible metric definition basis | `PERIOD_MISMATCH`, `GRAIN_MISMATCH`, `CALENDAR_MISMATCH` or `METRIC_BASIS_MISMATCH`; no combined comparison chart. Retain independently labeled cards |
| Zero baseline | Absolute delta remains valid when both values exist; relative null with `ZERO_BASELINE`; no infinity |
| Missing/partial baseline/current | null deltas with `BASELINE_UNAVAILABLE`, `CURRENT_UNAVAILABLE` or `COVERAGE_INCOMPLETE`; no stale fallback |

The three metrics are not percentage metrics: no percentage-point output in C01.
A future percentage metric needs a separately admitted comparison rule.
Single-card temporal `delta_trend` renders server relative deltas with a labeled
percent axis; connector deltas likewise use server values. Pair mode does not
also show previous-year lines (avoid ambiguous four-series identity). Selection
changes never mutate metric definitions or trigger compute for an already verified
binding. Changing period/grain requires Apply.

### D06 — Creator guard and readers

For every definition Save and settings mutation, load immutable creator from
Presentation, require actor equality **and** `report.manage`, `report.read`,
`analysis.read`, existing object/workspace/data permissions and current access to
all bound inputs. Apply that guard on both v1 and v2 update routes; no admin,
report grant, department transfer or ownership transfer changes creator. Creator
revocation denies authoring too. Draft definition Apply requires the same author
checks plus `analysis.run`. Reader view Apply requires report read + analysis
read/run and object/data permission, without `report.manage`; pure authorized
snapshot reading/display requires read, not run. Never add run implicitly to a
viewer role. Creator checks are not inferred from a hidden button.

Add a public Identity access projection, implemented over existing organization
policy services, that resolves report/dataset resource ownership scope and returns
allowed/denied, policy fingerprint and permitted data scope. Presentation supplies
report identity/creator, never reads Identity tables. Preserve the explicit
principal-owned legacy access path for old unbound drafts; absent organization
binding is not a generic allow for another principal. Non-owner access requires an
actual existing report binding/grant and current dataset/artifact permission.
C01 adds no sharing UI or default grant. The adapter must deny unsupported row/
column restrictions it cannot express through the admitted source scope; it cannot
pretend full-data access. Existing deny-wins organization rules remain authoritative.

Result reads on behalf of an authorized reader use an Analytics-owned public
verification projection: check access to every dependency and whether stored
result scope is fully readable before returning exact bytes. Broader stored scope
must fail closed; a reader may explicitly Apply a permitted narrower query instead,
never receive a silently altered exact snapshot. Personal result/view IDs require
their owner. This replaces neither result policy checks nor private workset scope.
List filtering/counts occur before pagination; denied/private worksets are absent.
Recheck access before final Save commit, on replay, on every GET/Apply, and before
returning a computed result. Browser clears protected state after expiry/revocation
and discards late responses from obsolete auth/context generations. No automatic
retry of 401/403, no raw data in error details.

### D07 — Atomic publication, concurrency and failures

Apply can display per-card progress/errors, but returns `complete` only when every
requested binding is verified. Domain no-data/comparison-unavailable is a valid,
explicit result state and can be saved; failed/missing/corrupt bindings cannot.
Save requires matching definition hash for every card, including inactive worksets;
untouched exact bindings may be reused after verification. New calculation failure
keeps the old saved snapshot intact and visibly marks the current draft unapplied
or failed; old numbers are never labeled fresh. Empty configurations are saveable
without fabricated result artifacts.

Commit all immutable result/comparison/ChartSpec references, then page and root
artifacts, then atomically insert report version, creator Saved View version and
switch latest pointers in one Presentation PostgreSQL transaction. Existing orphan
artifact behavior remains: failed CAS/commit may leave unreferenced committed bytes,
but no visible partial report; cleanup belongs to Artifact Lifecycle. Saved View-only
writes use the same own-view transaction/verification rules. No report CAS split by card.

Lock current document, check current access/creator and expected revision, apply
existing idempotency protocol. Hash canonical complete semantic request including
contract version and result references, excluding the idempotency key. Same actor/
report/key and same hash returns the exact original revision after current access
recheck; changed hash gives `IDEMPOTENCY_CONFLICT`. Different key and stale revision
gives `REVISION_CONFLICT`. No auto-merge/rebase: preserve draft and offer reload or
explicit reapply against latest. A timeout after Save is reconciled by retrying the
same key/body or reading the exact saved response; never invent another save key.

| Failure | HTTP / safe behavior |
|---|---|
| Invalid strict DTO, unsupported field/grain/version | 422 typed validation; no compute or mutation |
| Unknown metric/store or incompatible request | 400 typed domain code; no silent substitution |
| Limit exceeded | 413 `WORKSPACE_LIMIT_EXCEEDED`; preserve draft |
| Auth/CSRF/access | 401 / 403; 404 for inaccessible resource locator; clear protected state |
| Revision/idempotency/policy changed during Apply–Save | 409 respective `REVISION_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `ACCESS_CONTEXT_CHANGED`; reauthorization needed, no partial commit |
| Missing/corrupt artifact | 409 `ARTIFACT_MISSING` / `ARTIFACT_CORRUPT`; exact snapshot unavailable; no recompute-on-read |
| Storage/database temporarily unavailable | 503 `STORAGE_UNAVAILABLE`; bounded explicit retry, old revision preserved |

Retain existing v1 error mapping. New v2 error envelopes include `code`, optional
card IDs and retryable flag; no filesystem paths, SQL, source rows or secrets.
Use existing request correlation and safe IDs for diagnostics; no new alerting
system or performance/SLO claim. S05 injects failure after artifact commit and
before latest-pointer update and verifies durable state after reconnect/restart.

### D08 — One UI integration boundary

Reuse `ReportWorkspace`, `PilotDocument`, `pilot/document.html`, generator/source
mapping, `runtime.ts`, prelude/epilogue, existing API client and chart renderer.
Edit maintained source/seams and regenerate derived runtime with the repository's
existing source mechanism; do not hand-edit generated output in isolation.
Accepted composition adds workset controls above independent card rail, common
context, visible local filter/inheritance, one main chart/table/Focus area and one
Set/Card/Chart inspector. Goals section is explicitly unavailable/hidden until C02;
shared save/audience actions until C03. No fictitious working control.

Implement these intersecting surfaces in S04 together: catalog + cards/order/copy,
context + six grains + Apply, comparison + axes/table/Focus, Save + exact reopen +
conflict/error/trust. Preserve dark surfaces, original shell/navigation/SVG language,
keyboard order controls and focus restoration. Local bulk edit previews affected
cards/incompatibilities before Apply; invalid changes do not partially apply.
Use existing query cache for server state and scoped draft/display state for local
edits; no duplicate general state store/framework. Save with unapplied query changes
requires Apply first; display-only save reuses verified bindings. RU/EN strings
live in actual localization paths, never change analytical identity.

### Compatibility impact matrix

Assessment is proposed, baseline above → this L3; no implemented runtime change in
this authoring task. Coverage: direct Python contracts/adapters/API, generated Web
client and stored report/result consumers. External clients are not enumerated;
no undocumented mixed-version guarantee is assumed.

| Surface / direction | Classification | Concrete guarantee / condition and proof |
|---|---|---|
| New server + old v1 report/client | `compatible-change` | Keep strict v1 schemas/routes/behavior until that report is upgraded; S01 contract parity and S03 legacy tests |
| Old v1 client + report upgraded to v2 | `breaking-change` | Old latest/update cannot represent worksets; explicit 409, no downgrade; preserved exact v1 snapshot endpoint |
| New server + old persisted snapshots | `compatible-change` | Dual reader and non-mutating adapter; artifact hashes unchanged; migration/reopen proof |
| Old binary + v2 data / downgrade | `breaking-change` | Unsupported discriminator/schema; forward repair or separately authorized coherent restore after v2 writes |
| Analytics/API DTO + public ports | `compatible-change` for retained v1; new v2 requires new consumer | Separate versions/paths, no enum widening of strict v1; typed schemas/client parity |
| Persisted control schema | `compatible-change` for new-reader/old-data | Additive columns/tables/backfill; no artifact rewrite; migration idempotence and creator FK/immutability tests |
| Creator policy vs earlier target edit grant | `breaking-change` | REPORT-018 supersedes generic author edit expectation; admin/grant/transfer cannot override. Existing owner-only runtime access is not broadened silently |
| Cache/result identity | `compatible-change` for v1 retention; isolated v2 namespace | Policy/calendar/grain/source pins; no reuse of v1 hash as v2 result; duplicate context/revocation proof |
| Browser behavior | `breaking-change` to fixed UI assumptions, intended product change | Card/selection/save semantics and six grains change; native shell preserved; S04/S05 tests |
| Deployment/config | `compatible-change` for new settings; `none` to topology/modes | Base fiscal-calendar setting/API is a new compatible versioned configuration contract; no new service/dependency/queue/scheduler; migrations and dual-version activation still required before use |
| External clients beyond repository | `unknown` | No inventory provided; version rejection is explicit. No release/mixed-fleet compatibility claim; inventory before any separately authorized rollout |

### Concrete C02/C03 extension seams

C02 must pin fiscal/calendar version and resolved occurrence boundaries; a workspace
calendar change never shifts existing goals or closed occurrences. C02 can bind an immutable goal definition to stable card ID **and copied metric/
effective-context references**, independent of later card edits, with its own rule
version and calculation history. C01 includes no goal columns, modes, recurrence,
run-rate mathematics or scheduler. C02 must design those under DEC-05…12; manual
actual recalculation and retained corrections stay separate from definition Save.

C03 can extend Workset's versioned visibility contract with shared scope and
Saved View's explicit base document/workset version adoption. C01 already pins
versions and maintains separate query/display state and business-calendar references; no automatic migration on
read. C03 reuses report/data readers and creator guard, not an audience list or
admin override. No generic extensible JSON blob or universal policy engine is
introduced as a speculative seam.

## 3. Work breakdown and ownership

These are future sequential stages, not execution status. Roles describe module
responsibility only; the owner has not selected agents or parallel work.

| Stage | Bounded result / input → output | Dependencies | Expected owned zones | Shared writer constraint / exit |
|---|---|---|---|---|
| MS-004-S01 | Contract and migration foundation: accepted L3 → strict v2 DTOs/schemas/ports, Semantic calendar settings/default provisioning, dual-read fixtures, additive migration and source documentation | Plan acceptance and separately prepared valid pack/entry authority | `packages/contracts/presentation`, `packages/contracts/analytics`, schemas/OpenAPI/generators/clients, `migrations/versions`, Semantic calendar contracts/service/storage/API, focused contract/unit/migration tests | One writer for schemas and generated clients. No v2 route activation until access/save service exists. Exit: strict unions, old-client parity, migration tests, exact decisions encoded without unresolved schema choices |
| MS-004-S02 | Real calculation: S01 schemas + six-table inputs → normalized contexts, fiscal/calendar bucket resolution, six grains, temporal/pair artifacts, dedupe and bounded edge corpus | S01 | `packages/analytics_core`, `packages/semantic_model/application/sales_metrics.py` only adapter needs (definitions unchanged), `packages/artifacts`, Analytics API/adapters and tests; task-owned fixture preparation | Analytics owns values/identity; no Presentation business calculation. Exit: real PostgreSQL/intake/artifact oracle for six grains and leap/ratio/empty cases, truthful coverage |
| MS-004-S03 | Durable configured workspace: S02 results → guarded Apply/Save/read and Saved View paths, complete snapshots, legacy continuity, CAS/recovery | S01–S02 | `packages/presentation`, public Identity access adapter/port and composition root, reports router, bounded result verification adapter, integration/access tests | One writer for report transaction/API. Exit: real DB/artifact atomicity, non-creator denial, reader view semantics, exact old/new reopen and retry proof; then activate v2 routes |
| MS-004-S04 | Complete native-pilot interaction: S03 API → bounded base-settings fiscal form plus workset/card/context/comparison/save integrated surfaces with RU/EN and source mapping | S03 | `apps/web/src/features/reports`, maintained pilot source/seams/generator outputs, report client integration, renderer adapter, locale keys, existing settings route/section for the bounded calendar form and focused Web tests | Single integration owner for bridge/chart/table/save; no parallel shell replacement. Exit: real API smoke plus focused tests, readable empty/error/stale states, goal/shared actions unavailable |
| MS-004-S05 | Local integrated acceptance and repair: S04 product → criterion-linked real source→API→browser evidence, legacy/recovery/access negatives and owner demonstration | S01–S04 | New MS-004 test/evidence fixtures and browser harness; narrow repairs in above zones and affected canonical docs | Preserve historical evidence/ledgers. Exit: AC-01…11 technical evidence complete and owner acceptance; no packaging or release gate implied |

S01's migration tests may run against isolated control PostgreSQL; S02 introduces
source intake proof; S03 adds real authorization/transaction tests; S04 can start
its browser smoke only after those APIs exist. S05 reuses unchanged earlier
boundary evidence and adds end-to-end evidence, not gratuitous full-suite repeats.

## 4. Acceptance and proof allocation

| Criterion | Requirement / observable acceptance | Stage | Check / environment | Required evidence / authority |
|---|---|---|---|---|
| MS-004/AC-01 | METRIC-025/026/027: create two sets, copy one, reorder cards/sets, duplicate revenue with same and different stores; stable IDs on edits, new IDs on copy, exactly three registry formulas | S02–S05 | Real API + PostgreSQL + browser; compare stored JSON/registry refs; keyboard sequence | IDs/hashes and redacted screenshots; technical then owner |
| MS-004/AC-02 | Local store never expands common scope; null versus empty preserved; inherited/equivalent explicit contexts share result while cards remain independent | S02/S03 | Normalization unit cases + real intake/API; common {1,2}, local {2,3}→{2}; disjoint→no_data; denied store fails | Canonical hashes/manifest and independent source SQL; technical |
| MS-004/AC-03 | METRIC-030: all six grains reconcile counts/revenue and recomputed ratio; complete versus clipped versus incomplete distinguished | S02/S05 | Real PostgreSQL source SQL oracle at receipt grain, unequal-count days, cross-week/month/quarter/half-year/year intervals with January/April/October start, both FY labels, ≤366-day bound | Bucket/totals oracle including average-of-averages counterexample; technical |
| MS-004/AC-04 | METRIC-028/CHART-021/COMPARE-013: positive 2025/2024 baseline, leap mapping, missing/partial/zero baseline, typed two-card axes and incompatibility reasons | S02/S04/S05 | Real two-period intake; browser compares chart/table/tooltip to artifact values; same/different metric pairs | Manifest/result IDs, numeric comparisons and screenshots; technical + owner interaction |
| MS-004/AC-05 | Apply changes displayed calculation only; Save atomically pins all cards/sets, config/defaults/references; reopen without compute uses exact bytes; empty set/report valid | S03/S05 | API + DB/artifact root + browser reload/service restart; inspect no compute-on-GET | Old/new hashes and revision/pointer assertions; technical |
| MS-004/AC-06 | Old v1 snapshot unchanged after v2 Save; new reader opens both; old client gets explicit upgrade error for v2 latest; migration/recovery restrictions enforced | S01/S03/S05 | Disposable PostgreSQL pre/post migration and strict old/new API contracts | Migration results, byte hashes and downgrade refusal; technical |
| MS-004/AC-07 | Creator-only definition writes; denied non-creator even with admin/manage/grant/department transfer; reader permitted view Apply/Save view cannot edit base; revoked actor denied on reuse/save/reopen | S03/S05 | Real principal sessions and Identity resource/data bindings; separate author, authorized reader, administrator; denied data-scope and other-workspace cases | 401/403/404/409 and unchanged revisions, private sets absent, reader own-view state; technical |
| MS-004/AC-08 | RU/EN, keyboard catalog/order/inspector, Escape/focus return, chart/table/Focus, all six grains, truthful goal/shared unavailable; native pilot retained | S04/S05 | Real browser 1920×1080, 768×1024, 400×900; accessible table and focus; console/network review | Redacted screenshots, source-map check and interaction evidence; technical + owner |
| MS-004/AC-09 | Competing Save yields one winning revision; same-key replay exact; changed-key/body conflict; card failure/corrupt/missing artifact/storage failure never switches partial latest or relabels stale values | S03/S05 | Real DB concurrency + fault injection before/after artifact commit and before transaction update; reconnect/restart; delayed browser response | Durable pointer/manifest assertions, safe errors and draft preservation; technical |
| MS-004/AC-11 | METRIC-030: authorized admin saves workspace fiscal default; analyst denied; two settings writes conflict; old report/results unchanged; creator explicitly adopts via Apply/Save; other workspace denied | S01–S05 | Real settings API/PostgreSQL + browser, workspace initialization and legacy backfill; exact old/new calendar hashes; January→April then October | Settings version/revision, pinned report identity, boundary/label oracle, no automatic compute; technical + owner |
| MS-004/AC-10 | Complete source→six-entity admission→registered metrics→result artifacts→saved report→browser demonstrated; accepted documentation synchronized; no false release closure | S05 | Existing hybrid mechanism with task-owned corpus/DB/artifacts, all criteria mapped to evidence and owner demonstration | One journal-linked closure evidence after authorization; owner acceptance required |

### Fixture and test mechanism

Do not execute these product checks during L3 authoring. At execution, use
[local runtime contract v5](../../../development-runtime-contract.md) and
`scripts/dev up --mode hybrid` for the existing local mechanism when required.
Do not launch an unowned stack or reuse another task's destructive fixture cleanup.
Existing `tests/integration/data_pipeline/conftest.py` requires protected test
password-file variables and skips without them; a skip is not acceptance.
The historical MS-003 fixture runners are read-only implementation examples;
create a new task-owned fixture runner in the new authorized test/evidence scope,
with separate control database/source schema/artifact root and cleanup boundaries.
Do not run their historical cleanup against a live development database.

The observed demo recipe already spans two years. Pin a `ms004-retail/v1` test
corpus using those real six PostgreSQL tables, deterministic generation and the
production connector/intake path. It must include 2024 and Jan–Nov 2025 complete
coverage for the positive case; a missing-prior-receipts case despite declared
Calendar coverage; a separate missing/incomplete Calendar case; zero net with
positive count; unequal receipt counts; disjoint stores; Feb 29 2024 versus 2023;
2025 versus leap-2024 mapped-date exclusion; year-crossing weeks; clipped quarter/
half-year/year buckets under January, April and October calendars; a full April–March fiscal year crossing Feb 29; settings CAS/permissions and explicit report adoption with old snapshot unchanged. Extend only task-owned fixture input, never production
MetricVersions or existing shared seed for convenience. Preserve Customer/Product
and ReceiptItem binding/quality limitations; no new metrics over them.

At intake record actual min/max receipt dates, eligible rows/store/day coverage,
Calendar complete intervals and all six admitted IDs/hashes. A seed formula or
historical test assertion is not actual runtime coverage. For positive comparison
assert non-null values and eligible receipts on both sides; a `comparable` flag
alone with null totals is insufficient. Source SQL oracle is independent of the
production aggregation helper and reads synthetic PostgreSQL data only.

Known focused commands (after `source scripts/activate-toolchain.sh`) are:

```bash
uv run --locked pytest -q tests/unit/presentation tests/contract/presentation
uv run --locked pytest -q tests/unit/analytics/test_sales_report_unit.py
uv run --locked pytest -q tests/integration/analytics/test_sales_report.py tests/integration/presentation
uv run --locked python -m packages.contracts.generate_reports_client
uv run --locked python -m tools.check --scope local
```

Expand focused test files with v2 cases in S01–S03; the existing commands alone
cannot establish unimplemented v2 acceptance. Run integration only with the
isolated runner's real DB/secret-file setup, and record non-skipped counts.
S04/S05 add a dedicated `tests/e2e/ms-004-workspace/playwright.config.ts` and real
API fixture using the maintained native-pilot harness pattern; planned command:
`corepack pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/ms-004-workspace/playwright.config.ts`.
That path is a future output, not a currently runnable check. The fixture must
use production APIs and real intake, not route interception or HTML arrays.
Runtime availability, source coverage and credentials are checked at authorized
stage entry; missing inputs block the corresponding evidence claim, not silently
switch to mocks. Builds/Docker image packaging/installation/release are not C01
acceptance requirements. No performance claim or benchmark is made.

## 5. Execution and repair envelope

| Field | Bound |
|---|---|
| Allowed current changes | This L3, owner-requested fiscal requirement/mirrors and relevant contracts/ownership, reciprocal/version/index navigation; prior 21-document transfer |
| Future allowed changes | S01–S05 declared zones only after separate execution authority; narrow integration fixes and tests matching the changed boundary |
| Forbidden | Source checkout/snapshot mutation, MS-001…003 plan/pack/journal/receipt rewrites, resuming held stages, new service/query/chart library, goals/shared implementation, arbitrary metrics, release/publication |
| Delegated detail | Internal factoring, test names, exact next migration ID if occupied, localized copy preserving meaning, fixture counts adequate to the specified cases; no scope/acceptance weakening |
| Reserved owner decisions | Accept/change this exact L3 and its tradeoffs; choose agent organization; later pack/entry authority; final user-result acceptance. Already answered L2/product choices are not reopened |
| Repair | Fix within the selected stage and rerun invalidated checks. Cross-boundary contract changes amend this plan before execution; no silent stage expansion |
| Rollout/recovery | D02/D07, no old-binary rollback after v2 writes; no deployment in this task |
| Documentation effects | At implementation update actual authoring/recovery/API/Web source contracts and capability inventory with actual versioned behavior; preserve target/implemented distinction and source hashes. This fiscal follow-up updates target semantics only; runtime contracts remain unimplemented |
| Sensitive data | Synthetic inputs only; no secrets, cookies, raw provider payloads, auth headers, local credential paths in committed evidence; screenshots exclude protected session information |

## 6. Execution artifact binding

| Field | Binding |
|---|---|
| `plan_doc` | Accepted design 0.2.0, editorial binding 0.2.1; exact final digest pinned in all prompts and the journal |
| `prompt_pack_dir` | [Five stage prompts](../../../../../.codex/agents/generated/MS-004/MS-004-S01.md) in `.codex/agents/generated/MS-004/`; preparation authorized, execution separately selected |
| `stage_ledger` / `execution_ref` | [Canonical draft journal](../../../../../.codex/delivery/ledgers/MS-004.md); no claims, current_stage null, all stages pending and disallowed |
| Validation profile | Repository `prompt-pack/v1`, `validate_prompt_packs`; preparation validation/review recorded in journal-linked evidence; no entry-ready claim without execution authority |
| Claim/update mechanism | Existing repository `tools.custometry_quality.stage_ledger` exclusive transactions, read-only capability inspection bound in preparation evidence; stage preflight required again at authorized entry |
| Execution mode | Proposed `manual_sequential`; no Goal mode or agent dispatch selected |

The journal will own all execution status and closure. This document has only
planned outcomes and design decisions, not a second status board.

## 7. Owner decision packet and history

| Decision ID | Question | Options / recommendation and basis | Decider | Blocks | Resolution |
|---|---|---|---|---|---|
| MS-004/DEC-01 | Accept this exact bounded L3? | Accept 0.2.0 with D01–D08 and S01–S05, or identify concrete amendments; selected design preserves existing ownership and avoids new infrastructure | Owner | Pack preparation and subsequent execution | Accepted 2026-09-20: owner explicitly confirmed that the decisions and expectations are accepted; covers L3 0.2.0, D01–D08, S01–S05 and AC-01…11 |
| MS-004/DEC-02 | Agent organization for later execution | Owner selects when requesting pack/execution; no parallelism assumed | Owner | Agent assignment only | Not selected; does not affect L3 acceptance |

No outstanding product-policy questionnaire or unresolved C01 engineering schema
choice remains. Reader integration and two-period corpus are explicitly allocated
implementation/proof work, not assumed existing features. The accepted tradeoffs include:
per-day leap policy, explicit old-client upgrade boundary, complete all-card Save,
engineering limits, personal Saved View behavior and month-based fiscal profile. Acceptance is the explicit owner confirmation recorded in DEC-01; runtime
proof and final result acceptance remain future work.

| Version | Date | Change / references | Approval basis |
|---|---|---|---|
| 0.2.1 | 2026-09-20 | Bind authorized five-prompt pack and draft journal; no technical decision or criterion change | Explicit owner request for next preparation step and technical-branch synchronization; inherits design acceptance 0.2.0 |
| 0.2.0 | 2026-09-20 | Add company fiscal calendar/settings to C01, pin versions and basis, specify adoption, migration, UI, identity and AC-11 | Owner required fiscal-year support, then explicitly accepted L3 decisions and expectations on 2026-09-20; MS-004/DEC-01 |
| 0.1.0 | 2026-09-20 | Initial concrete C01 L3; accepted 21-document input transfer, bounded code observations, technical contracts and five future stages | Owner requested L3 preparation in separate task; in_review, not accepted |

### Mandatory documentation handoff

Register MS-004 under WS-003/C01 and navigation in DIR-004, MAP-001, roadmap and
architecture index. Editorial parent/navigation patches preserve accepted L2
scope, broader MAP/L1 planning statuses and historical version decisions; unchanged
MS-001…003 bindings remain at their original basis. The authorized triad is now linked; preparation evidence remains separate from runtime proof.
The owner fiscal correction updates METRIC-030 in the normative/human/UI sources
to revision 2026-09-20.2, the authoring contract to v10 and context map to v14.
WS-003 3.0.0 accepts that product correction only; MAP/DIR navigation 2.3.0 remains
in_review. S01 onward records actual implementation contracts separately. Current source checks establish documentation consistency
only. Authoring validation results follow below.

### Authoring validation for 0.1.0 (historical)

- `source scripts/activate-toolchain.sh`: pass; repository toolchain activated.
- `uv run --locked python -m tools.custometry_quality.generate_docs_index`: pass,
  73 documents; `docs/README.md` includes MS-004.
- `uv run --locked python -m tools.custometry_quality.generate_requirement_index`:
  pass, 1282 requirements; no additional change to the transferred requirement index.
- `uv run --locked python -m tools.check --scope local`: pass (documentation/source
  consistency and static doctor), including the final editorial pass.
- Bounded authoring assertions: parent chain and preserved statuses, requirement
  pins, stage/criterion IDs, incoming-versus-authored file separation and unchanged
  product/historical artifacts checked; `git diff --check` passed. The first
  index-label assertion expected a dot instead of the generated em dash; the
  assertion was corrected to check the canonical link and then passed. No source
  defect or failed runtime check was represented as a pass.

The prescribed locked checks initialized this worktree's local `.venv` from the
existing lockfile; no dependency declaration or lockfile changed. No product tests,
browser runtime, migration, application build, container or release check was run.
These results do not prove C01 behavior. No commit/push/PR or execution triad was created.

### Fiscal amendment validation — 0.2.0

`generate_requirement_index` passed (1282 requirements), `generate_docs_index`
passed (73 documents), and `uv run --locked python -m tools.check --scope local`
passed after correcting three new section links rejected by the link checker.
`git diff --check` and bounded source-pin/parent-chain assertions passed.
Machine/human/UI revisions are 2026-09-20.2; exact machine hash is pinned by the
selected L3/L2/L1/map. The five-stage sequence now covers base settings and fiscal
calculation; AC-11 proves configuration rights/versioning and explicit adoption.
No implementation, application tests, database/browser run or publication occurred.

### Owner acceptance — 2026-09-20

The owner explicitly confirmed acceptance of the decisions and expectations after
review guidance covering the month-based fiscal calendar, explicit calendar
adoption, atomic Apply/Save behavior and five-stage local acceptance outcome.
This records acceptance of L3 **0.2.0**, D01–D08 and AC-01…11; no engineering scope
or criterion is changed by this acceptance record. Reviewed candidate SHA-256:
`91354244c2e4e3958044c8935f0d8964c9df59efd86bc6cb691849626503974c` (bytes preserved outside the repository before this editorial update).
Parent/navigation patches only record this acceptance; broader MAP/L1 statuses
remain in_review. Agent organization remains unselected, execution_ref is null,
and no pack, journal, implementation, publication or deferred MS-003 stage is
started. Next available handoff is separately authorized pack/journal preparation.

Acceptance-record checks: `generate_docs_index` passed (73 documents),
`uv run --locked python -m tools.check --scope local` and `git diff --check` passed.
Bounded assertions verified the accepted L3, exact reciprocal parent versions,
unchanged broader in_review status and absent execution triad. Documentation proof only.

### Authorized pack preparation — editorial binding 0.2.1

On 2026-09-20 the owner requested the next step after L3 acceptance, followed by
technical-branch remote synchronization and deletion of that branch. This authorizes
five prompts, one draft journal, required preparation evidence and the normal PR/CI
synchronization route. It does not authorize implementing S01 or changing its
accepted outcome. Version 0.2.1 inherits accepted design 0.2.0 with only execution
artifact links and this authority record; technical decisions/criteria are unchanged.
The journal alone owns stage allowances. All initial rows remain pending/disallowed.
Preparation checks and independent-review availability are recorded in the journal
and its preparation evidence, not claimed from historical plan checks.
