---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-003",
  "title": "First saved analyst report on governed retail data",
  "version": "0.2.0",
  "planning_status": "in_review",
  "language": "en",
  "parent_ref": {
    "id": "WS-002",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-002.md",
    "version": "0.2.0"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "2f04dacc2184ec0ad30636526855309262b6bf5e",
    "evidence_refs": [
      "docs/architecture/planning/milestones/MS-003/plan.md#current-state-evidence"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:183d9d2f2070cb8e651eca46fa44244b0d0af2a914830bcee6e5716ae15fd163",
      "ids": [
        "DATA-RULE-002",
        "DATA-RULE-004",
        "DATA-RULE-005",
        "DATA-RULE-007",
        "DATA-RULE-008",
        "METRIC-001",
        "METRIC-002",
        "METRIC-004",
        "METRIC-005",
        "METRIC-007",
        "METRIC-008",
        "ANALYTICS-SALES-OVERVIEW",
        "ANALYTICAL-DOC-001",
        "ANALYTICAL-DOC-002",
        "ANALYTICAL-DOC-006",
        "ANALYTICAL-DOC-007",
        "ANALYTICAL-DOC-012",
        "ANALYTICAL-DOC-015",
        "CHART-001",
        "CHART-002",
        "CHART-004",
        "REPORT-002",
        "REPORT-003",
        "REPORT-004",
        "REPORT-005",
        "REPORT-008",
        "REPORT-012",
        "REPORT-014",
        "UI-SHELL-001",
        "UI-SHELL-002",
        "UI-SHELL-003",
        "WEB-ARCH-003",
        "WEB-ARCH-004",
        "SEC-001",
        "SEC-007",
        "SEC-016",
        "I18N-001",
        "A11Y-001",
        "DATA-RULE-001",
        "DATA-RULE-009",
        "DATA-RULE-010",
        "DATA-RULE-011",
        "DQ-INPUT-001",
        "DQ-INPUT-003",
        "DQ-INPUT-004",
        "DQ-INPUT-005",
        "DQ-INPUT-006",
        "DQ-INPUT-007"
      ]
    }
  ],
  "decision_refs": [
    "FRAME/DEC-03",
    "FRAME/DEC-04",
    "FRAME/DEC-06",
    "MAP-001/DEC-09",
    "MAP-001/DEC-10",
    "MAP-001/DEC-11",
    "WS-002/DEC-01",
    "MS-003/DEC-01",
    "ADR-0006",
    "ADR-0007",
    "MS-003/DEC-04"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-003.md",
    "schema_version": "prompt-pack-ledger/v1"
  }
}
---

# MS-003. First saved analyst report on governed retail data

L3 review candidate `0.2.0`, 2026-09-12. Parent:
[WS-002 0.2.0](../../directions/DIR-004/workstreams/WS-002.md).
The owner requested the plan, prompts and journal together. Prepare the complete
review package now; do not claim acceptance of the newly written details.

## Result and boundaries

| Item | Definition |
|---|---|
| Before / after | Existing installation and isolated analytical features → an ordinary analyst opens a pilot-derived real-data report, changes period/store/comparison, saves a draft and reopens its exact values after reload/restart |
| First scenario | Synthetic Northwind Retail PostgreSQL `demo`, seed `20260716`, six source tables including 5,000 receipts, 1,000 customers, 120 products and 15,000 items; `net_revenue`, `receipt_count`, `average_receipt`; one ordered report page with metric group, daily revenue chart, complete daily table and Result Trust |
| First controls | Title; explicit date range; all stores or one authorized store; no comparison or previous-year same dates when coverage permits; chart/table and Focus; save and reopen from library/deep link |
| Lifecycle | An owned `workbook_report` draft with immutable saved versions and exact draft preview snapshots. Saving is not publication, sharing or a scheduled refresh. It never grants another account access |
| Excluded | Directory management screens; full installation/bootstrap/admin UI; arbitrary source wizard; complete metric designer; segment builder/selection; arbitrary page/block editor; automatic refresh, publication, separate-reader grants, email, downloads/XLSX, Forecasting, large-workload or full installation qualification |
| Authority | This request authorizes documentation and initial non-runnable pack construction. Product execution, Git publication, transfer, trust-store mutation and deployment are separate actions. Ordinary engineering work is delegated only within an accepted stage |
| Input decisions | The concrete sales scenario and this L2/L3 detail need owner review. All future stage outputs are producer-owned work, not inputs to request from the owner |

### Current-state evidence

Static inspection on `2f04dacc2184ec0ad30636526855309262b6bf5e`; existing local
MAP/DIR `2.0.0` and supporting-doc deltas preceded this authoring unit. No product
runtime, browser, container or source connection was exercised during planning.

| Claim ID | Capability | Observation | Evidence | Gap / resolution |
|---|---|---|---|---|
| MS-003/EV-01 | Identity | `code_observed` | [Identity router](../../../../../apps/api/src/custometry_api/identity/router.py), [service](../../../../../packages/identity_access/application/service.py) | Bootstrap/invitation/login exist. Cookies are scoped to `/identity`; analytics currently accepts bearer only. S01 connects the browser session safely |
| MS-003/EV-02 | Intake | `code_observed` | [DataPipelineRunner](../../../../../apps/worker_data/vertical_slice.py), [real pipeline tests](../../../../../tests/integration/data_pipeline/test_vertical_slice.py), [demo profile](../../../../../deploy/demo-source/profiles/demo.json) | Existing full retail runner covers Customer/Receipt/ReceiptItem/Product and its tests use a Product-reference waiver. S01 extends a separate six-entity profile with Store/Calendar, qualified relationships and the explicit derived-subset disposition below; no test waiver becomes production setup policy |
| MS-003/EV-03 | Analytics | `code_observed` | [AnalyticsService](../../../../../packages/analytics_core/application/service.py), [router](../../../../../apps/api/src/custometry_api/analytics/router.py), [repository](../../../../../packages/analytics_core/infrastructure/postgres.py) | Existing totals, filter/comparison and immutable-result seams; no daily-series/registered-three-metric report acceptance observed. S02 proves and completes them |
| MS-003/EV-04 | Documents/charts | `documented_only` target; bounded code observed | [Presentation package](../../../../../packages/presentation/application/people.py), [compiler entry](../../../../../packages/chart_compiler_ts/src/index.ts) | PeopleService is not a document store; compiler exposes `planned`. S03 implements the bounded common model and S04 the selected Web compiler/adapter |
| MS-003/EV-05 | Web | `code_observed` | [SalesOverview](../../../../../apps/web/src/features/analytics-sales/SalesOverview.tsx), [old browser fixture](../../../../../tests/e2e/web-analytics-sales/real_analytics_fixture.py), [accepted pilot](../../../ui/target-pilot/README.md) | Existing test fixture injects token identity and writes admitted rows directly; this is not the selected end-to-end proof. S04 uses S01 real preparation and S03 APIs |
| MS-003/EV-06 | Delivery | Historical bounded proof; current config observed | [MS-002 journal](../../../../../.codex/delivery/ledgers/MS-002.md), [runtime contract](../../../development-runtime-contract.md), [installation contract](../../../runtime-network-installation.md) | Installed ingress exposes installation routes only. S05 proves selected protected product routes in a new candidate; preserves MS-002 native/VM/LAN exceptions |

### Dependencies

| ID | Provider + exact source/version | Required output | Consumer / needed before | Satisfaction proof | Shared writer |
|---|---|---|---|---|---|
| MS-003/DEP-01 | [WS-002](../../directions/DIR-004/workstreams/WS-002.md) `0.2.0`; parent DIR-004 `2.0.2` | Accepted first product scope | S01 entry | Owner decision and synchronized plan/pack bindings | Plan author; runner after activation |
| MS-003/DEP-02 | [Bounded-context map](../../../bounded-context-map.md) doc_version `13`; [authoring contract](../../../../contracts/analytical-authoring-contract.md) doc_version `2` | Provider-owned result/semantic/policy ports; common composition | S01–S04 design/implementation | Contract and real integration tests | Each context owns its writes; apps compose |
| MS-003/DEP-03 | [Runtime](../../../development-runtime-contract.md) doc_version `3`; [MAP cadence](../../project-map.md#development-and-delivery-cadence) `2.0.2` | Existing Fast Loop/Hybrid and package producer | S01 local integration; S05 candidate proof | Reuse exact current tooling, isolated owned state | S05 owns runtime integration |
| MS-003/DEP-04 | [Pilot](../../../ui/target-pilot/README.md), [manifest](../../../ui/target-pilot/manifest.json); [ADR-0007](../../../../adr/0007-responsive-web-frontend-platform.md) doc_version `2` | Demonstrated structure/interaction and production stack | S04 acceptance | Normalized rendered source/implementation comparison | Web/shared UI owner within S04 |

## Implementation decisions

These are concrete proposed choices for this milestone, not permission for an
executor to redesign the stack. Acceptance of this plan fixes them. New endpoints,
files and schemas below are target contracts, not claims that they exist today.

| Decision | Current design → selected change and rationale | Owner/source and compatibility | Migration/recovery | Required proof |
|---|---|---|---|---|
| MS-003/TECH-01: prepared source | Reuse `demo` PostgreSQL seed through the existing readonly connector and DataPipelineRunner. Add named `retail-report/v1` extraction/publication profile for Customer, Product, Receipt, ReceiptItem, Store and Calendar. Land all source rows immutably, then publish the governed canonical subset with explicit quality accounting under the source contract below; no fabricated control-table inserts, embedded UI data or whole-retail DQ waiver | Ingestion/Artifacts/DQ/Semantic; additive profile; DATA-RULE-001/002/005/008..011 and DQ-INPUT-001/003..007 | Keep existing default retail profile unchanged. Idempotent setup references exact batch/dataset IDs and source fingerprint; mismatch fails explicitly. No source mutation or accepted-data reset | S01 proves six-table counts, qualified keys and relationships, anonymous customers, current-only dimension binding, five orphan-item quarantines, unchanged receipt totals, immutable source/derived artifacts and replay; critical key/artifact/security failures remain blocking |
| MS-003/TECH-02: internal actor/session | Prepare a workspace admin for setup, create/invite/accept a separate ordinary analyst through existing Identity services. A loopback-only preparation command uses protected runtime files and records only safe IDs. Minimal login/logout/re-login UI; no user-management programme | Identity; server remains authority. Reuse existing auth/CSRF primitives through a shared API dependency; preserve bearer API clients. Internal analyst has existing analyst permissions, not installation-admin privileges | Browser requests use same-origin `/api`. Access cookie Path `/`, refresh Path `/api/identity`, CSRF Path `/`; Secure in packaged HTTPS, existing explicit loopback-only dev exception. Clear legacy `/identity` cookies and new paths on login/logout; old sessions may require re-login. No token in browser storage/URL | S01 API cookie/origin/CSRF/logout/revoke/outsider tests; S04 real browser login through Vite proxy; S05 actual HTTPS proxy |
| MS-003/TECH-03: metric/time meaning | Register exactly three immutable Semantic metric definitions and their formatting: receipt-grain `net_revenue = sum(net_amount)`, `receipt_count = count distinct(source_system_id, receipt_id)`, `average_receipt = net_revenue / receipt_count`. Proposed initial eligibility: completed receipts, EUR only, visibly locked; refunds/cancellations and SEK are excluded explicitly. Do not describe this as refund-adjusted revenue | Semantic owns meaning, Analytics computes. METRIC-001/002/004/005/007/008. New versions distinguish this profile from prior experimental results | Preserve historical metric/result identities. Initial period 2025-01-01..2025-11-30, UTC; daily grain and same-dates previous year optional. Import/pin Calendar coverage; do not infer completeness from observed sales alone. Reject unsupported/mixed-currency or incompatible grain binding | S02 independent SQL reconciliation, negative/sparse/empty cases, weighted ratio, date boundaries, complete/partial comparison coverage; no sum of daily averages or receipt-total fan-out from ReceiptItem; Customer/Product presence does not enable unsupported metric dimensions |
| MS-003/TECH-04: bounded computation/result | Reuse the current synchronous AnalyticsService for the internal 5,000-receipt fixture and bounded daily outputs, with accessible busy/error state (§15.4 permits synchronous compute). Produce a receipt-grain sales-period mart and daily aggregate through existing data/analytics seams; typed totals and chart/table data share an immutable result. No new worker/service/scheduler for this bounded call | Analytics owns calculations; Semantic public projection and Artifact owner ports supply data. `ANALYTICS-SALES-OVERVIEW`, REPORT-003/004. Version the report projection; retain existing analytics API contracts or add a version-dispatched operation | Identity pins workspace/actor-effective-policy, dataset/artifact hashes, metric/calendar/code versions, normalized filters, periods and grain. Same-key request/result publication is deduplicated in PostgreSQL; concurrent insert losers return only their authorized winner. No partial result reference. Read failures never substitute latest | S02 deterministic replay/concurrent same-key, policy-separated reuse, artifact corruption and no stale authorization; no large-scale/SLO claim. If the fixed fixture cannot fit existing bounds, return for a scoped amendment, not a new engine |
| MS-003/TECH-05: document aggregate | Presentation owns logical document, immutable saved draft versions, ordered page/section/blocks, filter context and exact root/page preview snapshots. One supplied report template instantiates the supported composition subset; save preserves node IDs, new documents receive new IDs. Reuse the canonical `AnalyticalDocumentCompositionV1`, not a sales-only document format | ANALYTICAL-DOC-001/002/006/015 and REPORT-002/012; additive Presentation tables/API. Planned `/reports` collection, `/reports/{id}` draft read, `/reports/{id}/versions` save, `/reports/{id}/snapshots/{sid}` exact preview under the existing API prefix | Atomic expected-revision/CAS + idempotency-key write after required result artifacts are committed and checked. S03 produces and validates the bounded canonical line ChartSpec plus real Presentation-owned versioned system BrandProfile/CompanyPack defaults, using the accepted local assets/tokens and S02 public metric references; it pins their exact IDs/hashes before snapshot commit. No full brand editor is required. Snapshot result IDs/metric/filter/calendar/schema/grain/unit/lineage and author are pinned. Failed save keeps prior draft; conflict preserves unsaved UI changes and offers reload, never silent overwrite | S03 real PostgreSQL concurrent edit/idempotency, unknown ChartSpec/default-reference rejection and fail-between-artifact/metadata tests; reopened snapshots retain exact valid references; another principal/workspace cannot list/read/write even by guessed IDs |
| MS-003/TECH-06: read/open semantics | Library open resolves latest saved draft version once; exact link pins version/snapshot/page/block and rechecks access. Open, page selection, Focus, locale and chart/table toggles do not compute. Explicit Apply period/filter produces a new result; Save writes the draft version. UI labels preview as draft, never published | REPORT-002/005/008/014; ANALYTICAL-DOC-007/015. `report.read`/`report.manage` plus ownership and source/result policy intersect; installation-admin status alone grants no access | Result metadata in PostgreSQL; immutable bulk results in Artifact Lifecycle. Return safe projections without raw local paths, credentials or inaccessible counts. Missing/corrupt/storage-unavailable states are distinct; no old data shown after permission failure | S03/S04 reopen with source/API calculation disabled, refresh browser and restart API, revoked/forbidden/expired session, immutable prior snapshot after edits |
| MS-003/TECH-07: UI/chart | Use existing UI-RPT-001/002/003 and UI-AUTH-001 identities, preserving workspace prefixes. Carry pilot navigation rail/context, document tab, metric rail, inspector, chart/table geometry, Focus/return, density and RU/EN. Implement only this supplied report; hide unsupported actions or explain capability limits truthfully | ADR-0007; Web source contract. TanStack Query owns server state; local state owns unsaved edits. `packages/chart_compiler_ts` owns the selected canonical line ChartSpec compiler; Apache ECharts `6.1.0` matches the inspected bundled pilot version and is the sole approved package addition, pinned in pnpm. Use tree-shakable LineChart/Grid/Tooltip/Legend/SVGRenderer modules | Preserve pilot bytes and unrelated existing routes. Shared semantic UI primitives, no copied demo calculations/localStorage truth. Unsupported ChartSpec fields/types fail before rendering. Raw options/HTML/callback/network URLs are rejected. No SSR/rasterizer or export dependency needed | S04 compiler schema/identity, chart/table same values, no browser aggregation, real API browser, 768/1920 endpoints, RU/EN, keyboard/Focus, 200% zoom and console/network; source screenshot comparison before acceptance |
| MS-003/TECH-08: schema/runtime | Add migrations after the actual current head, never edit sealed migrations. Reuse the existing artifact root and source/dev setup. S05 changes the installed proxy allowlist only for this route set and Identity session endpoints; `/` retains installation readiness and offers the product entry when available | Persistence is additive; new-schema application is the supported reader. Existing experimental data is preserved; no obligation to import it into the new report library | Test upgrade from current head, repeated upgrade and previous-feature readability on the test DB. After new document writes, code rollback requires the pre-upgrade owned backup or forward repair; no destructive downgrade promise. New candidate uses separate owned installation, not an unproven in-place update | S03 migration/data preservation; S05 new image/config/schema identity, protected same-origin HTTPS routes, save/reopen after stop/resume and missing-artifact case |

No new numerical production limits/SLOs, source tolerances, auth policy or broad
resource scheduler are invented. The selected source fixture and date range bound
this internal demonstration; applicable existing limits remain enforced. Unbounded
user sources, complex composition and async render remain subsequent outcomes.
Bigger work is a plan amendment, not silently delivered under this six-stage pack.

### Six-table source and relationship contract

This corpus is synthetic and deterministic; "real source" means an actual
read-only PostgreSQL connection and governed intake, not customer business data.
Use the existing [demo profile](../../../../../deploy/demo-source/profiles/demo.json),
[DDL/seed](../../../../../deploy/demo-source/init/020_schema.sql) and
[golden manifest](../../../../../tests/golden/retail-demo-manifest.json).
Counts below are raw source counts before report date/status/currency filters.

| Source table | Canonical entity | Raw rows | Grain / purpose |
|---|---|---|---|
| `retail.customers` | Customer | 1,000 | One observed customer record; qualified natural key and a separate version key; names, city and source attributes |
| `retail.products` | Product | 120 | One observed product record; qualified natural key and a separate version key; SKU, name, category, brand and unit-price attributes |
| `retail.receipts` | Receipt | 5,000 | One receipt; receipt-grain metric input, including anonymous receipts |
| `retail.receipt_items` | ReceiptItem | 15,000 | One line; links each item to its receipt and product |
| `retail.stores` | Store | 20 | One observed store record; qualified natural key and a separate version key; report store selection |
| `retail.calendar` | Calendar | 1,830 | One date; imported, validated and pinned calendar/completeness metadata |

All source IDs map losslessly to string IDs under the stable source namespace
`northwind-retail`; connection display names are not keys. Receipt has primary key
`[source_system_id, receipt_id]`. Map the stable source `receipt_item_id` to canonical
`line_id`, retaining its source role; the item primary key is
`[source_system_id, receipt_id, line_id]`, never source row position. Customer,
Product and Store retain natural keys plus separate deterministic version keys.
All six entities, schema/mapping/policy versions, hashes and row accounting belong
to the same published dataset version through existing Semantic/Artifact ports.

Publish explicit relationships and cardinality: Customer 1→many Receipt through
nullable `customer_id`; Receipt 1→many ReceiptItem through `receipt_id`; Product
1→many ReceiptItem through `product_id`; Store 1→many Receipt through `store_id`;
Calendar 1→many Receipt through the UTC receipt date. Source entity joins include
`source_system_id`. A null receipt customer means anonymous: retain the receipt
and its amounts, without a fabricated Customer. Non-null unresolved customer,
receipt or store references fail admission of the affected canonical binding.
Duplicate/conflicting mandatory keys block this bounded profile; no arbitrary
winner or automatic identity merge is introduced.

Bind Customer/Product/Store attributes to an explicit **current-only snapshot**
relationship policy. Preserve supplied validity as source evidence and create
synthetic observed validity only where source validity is absent. Do not interpret
this six-table corpus as complete historical dimension state: `customer_history`
and cross-source identity tables are outside it. Pin dimension versions and this
limitation; no event-time classification, invented backdating or historical joins
against a current record. The other eight source tables stay available in the
existing demo database but are not claimed as loaded by this profile.

Apply the existing [imperfect-input requirements](../../../../contracts/source-data-adaptation-contract.md)
through one versioned, profile-specific derived-subset policy. The existing seed
has five items with `product_id=999999`, absent from Product. Preserve all 15,000
raw items; quarantine those five complete item rows into protected diagnostics,
with raw-row provenance and reason `receipt_item.product.reference`. Publish
14,995 eligible item rows with valid product links, all 120 products and all 5,000
receipt headers. Do not add a fake product, alter the fixture, silently discard
rows or create an approval/expiry waiver for ordinary setup. This is an explicit
remediation policy, not a relaxation of the original full-retail profile.

Recheck mandatory keys/references/artifact integrity on the derived subset.
QualityReport and semantic capabilities disclose raw, eligible and quarantined
counts, denominator 15,000, relationship coverage, measured item-net amount by
currency/period where available, and unknown business impact where not established.
Receipt totals remain eligible under their own rules; product/basket coverage is
`degraded`, never complete. Raw intake completeness is distinct from business and
relationship completeness. S02 carries this evidence into Result Trust; S03 pins
it and S04 displays a bounded quality limitation. No new DQ screen or general
remediation framework is required. Unexpected critical failures cannot be hidden
by this one policy, and replay must reproduce the same derived subset and identity.

The first three metrics still aggregate Receipt directly. Customer/Product data
is actually loaded, versioned and related for reuse; this does not authorize
product/category/brand slicing of receipt-grain revenue, item metrics, customer
analytics or directory CRUD screens. Item totals must not be substituted for
receipt totals; this seed is not asserted to reconcile line and header amounts.
S02 independently proves that multiple lines and quarantined lines cannot change
receipt counts/revenue, and that anonymous receipts remain included. Later item
analytics must register item-grain metrics and its own reconciliation policy
under METRIC-008.

### Deferred lifecycle coverage

- DIR-002 next own-data work includes real source configuration, readiness,
  full-snapshot correction/admission and refresh. MS-003's known deterministic
  source is not acceptance of the owner's future daily rebuilt database.
- DIR-003/C02 owns creation, version/save, calculation, immutable membership,
  manual/scheduled recalculation, historical comparison, Used by and report use
  of segments. Do not expose a functional segment picker until that provider exists.
- DIR-004/C01/C02 later adds rich composition and published/shared use;
  DIR-004/C03 retains REPORT-REFRESH-001..007. The first *published working report*
  must have the accepted after-ingestion default and actual lifecycle. This
  draft-only milestone does not redefine that default or mark refresh complete.
- Full BrandProfile/CompanyPack editing, narrative/research, rendering/export and
  universal XLSX remain their allocated requirements; system references used here
  must be real, versioned defaults, not invented successful projections.

## Work breakdown and ownership

| Stage ID | Bounded result | Dependencies | Expected zones | Shared writer constraint | Output consumed later |
|---|---|---|---|---|---|
| MS-003-S01 | Prepared real actor and governed six-table retail dataset | None after owner accepts plan | Identity/API auth glue; developer preparation; existing DataPipelineRunner/connector/DQ/semantic/artifact zones; focused tests | Own only selected profile and session changes; preserve other profiles and migrations | Safe runtime setup instructions and version IDs; report |
| MS-003-S02 | Reproducible registered sales totals and daily result | S01 | Semantic metric versions, AnalyticsService/result projection, typed contracts/mart/artifact seams; tests | Shared contract/migration work sequential | Exact result and independent reconciliation; report |
| MS-003-S03 | Save and reopen exact draft documents through API | S02 | Presentation domain/application/adapter, API composition, contracts and migrations; tests | One document writer; no producer-private reads | Versioned API/client schema, canonical line ChartSpec and system defaults, immutable preview/persistence proof; report |
| MS-003-S04 | Working pilot-derived analyst UI | S03 | Report/login feature routes, UI foundation, chart compiler, ECharts pin, localization, route/client declarations and slice-owned E2E | One shell/route/client integrator | Real browser journey and normalized pilot comparison; report |
| MS-003-S05 | The same feature works in the packaged candidate | S04 | Narrow proxy/runtime/bundle inclusion, product smoke/config and integration evidence | No installer rewrite; separate owned candidate | Candidate identity and actual HTTPS/restart proof; report |
| MS-003-S06 | Reviewable result and owner milestone acceptance | S05 | Criterion/evidence consolidation, canonical behavior docs and journal | No speculative product expansion | Final criterion map and actual owner decision |

No stage is allowed merely by appearing in this table. The journal is the sole
execution authority and defaults to manual sequential. Agent assignment remains
with the owner. Ordinary in-scope repair is included in the responsible stage.

## Acceptance and proof allocation

| Criterion | Requirement / intent | Observable result | Stage | Exact check / real environment | Evidence / authority |
|---|---|---|---|---|---|
| MS-003/AC-01 | Real prepared data | All six declared PostgreSQL tables → actual connector → raw and canonical Parquet/manifests → DQ accounting → published entities/relationships; five orphan items are explicit, all 5,000 receipt headers remain; repeat setup is safe; no fake admission | S01 | New focused tests in existing data-pipeline/identity suites plus actual owned development DBs | S01 report/receipt; technical |
| MS-003/AC-02 | Normal secure analyst | Ordinary analyst logs in; browser cookies work across `/api`; invalid Origin/CSRF, logout/revoke and another workspace deny protected operations; no leaked tokens | S01/S04/S05 | Real HTTP API tests, host browser and packaged HTTPS browser | Reports linked from journal; technical |
| MS-003/AC-03 | Reproducible calculations | Three metrics and daily series reconcile to independent SQL for selected eligibility/currency/time; LY explicitly available/blocked; Customer/Product lineage and quality limitations retained; anonymous receipts included and item joins cannot multiply header totals; replay and concurrent same-key preserve identity | S02 | Focused unit/contract tests and real PostgreSQL-to-artifact analytical integration with oracle queries | S02 report and safe numeric evidence; technical |
| MS-003/AC-04 | Durable draft/snapshot | Save title/context/results atomically; reopen exact values with no computation/source dependency; previous version remains exact; conflict/failure does not overwrite; unauthorized IDs deny | S03 | New Presentation real DB/API/contract suites, fault injection and migration upgrade/repeat/preservation | S03 report/receipt; technical |
| MS-003/AC-05 | Pilot-derived product | Library → draft editor → period/store/LY → chart/table/Focus/trust → save → reload/reopen works via real APIs; source-defined visual structure and keyboard/locale/responsive behavior retained | S04 | Planned `tests/e2e/ms-003-report/playwright.config.ts`, 768x1024 and 1920x1080, real S01 preparation, RU/EN/zoom/console/network, normalized source screenshots | S04 redacted screenshots and report; technical proof, final visual decision S06 |
| MS-003/AC-06 | Failures and identity | No stale result after deny; source refresh cannot silently change saved snapshot; missing/corrupt artifact and temporary storage failure truthful; save conflict retains edits | S02–S05 | Direct API/DB/artifact fault cases and critical real-browser negative journeys | Stage evidence plus S06 complete criterion map |
| MS-003/AC-07 | Packaged compatibility | Identified new candidate runs through real Edge/Web/API and migrated stores; secure login/product routes and save/reopen survive stop/resume; source hashes/images/config match tested code | S05 | Existing producer/installer in separate owned local native M5 test installation; changed boundary only, reuse current matching CI evidence when available | S05 candidate report; no Linux guest, second-Mac trust, upgrade or production claim |
| MS-003/AC-08 | Completion | All criteria mapped to real evidence; owner can try and accepts bounded product behavior and pilot conformity; docs truthful | S06 | Inspect previous reports/receipts, reconcile versions and current docs; present usable tested entry and get actual owner result decision | S06 report, owner evidence and final immutable receipt; owner |

Source checks prove authoring consistency, not these implementation outcomes.
Run focused Python and frontend gates from [tooling](../../../tooling-gates.md).
Existing commands: `uv run --locked pytest -q <selected-suite>`, `corepack pnpm
--filter @custometry/web typecheck`, `corepack pnpm --filter @custometry/web test`,
`corepack pnpm --filter @custometry/chart-compiler test`. New suites and browser
config are declared outputs, created by their stages, not assumed existing commands.
The S04 browser invocation after creation is `corepack pnpm exec playwright test
--config tests/e2e/ms-003-report/playwright.config.ts`. Reuse owned databases;
Playwright owns the host Vite lifecycle and fails rather than adopting a foreign port.

## Execution and repair envelope

| Field | Value |
|---|---|
| Allowed changes | Only each stage's declared feature/provider integration zones, focused proof and justified canonical documentation; shared paths sequential |
| Delegated choices | Function/file layout, straightforward DTO plumbing, indexes justified by queries, reusable components and focused test mechanics within the fixed contracts |
| Reserved changes | Different first report/data/metric policy, new library except specified ECharts, engine/service/framework, admin-first scope, new UI concept, production limits, destructive migration, published refresh semantics or external target |
| Repairs | Fix reproducible in-scope defects and rerun invalidated checks. A material contradiction becomes one concise amendment with evidence and recommended minimal fix |
| Protected state | Preserve foreign changes, pilot files and completed MS-001/MS-002 plan/pack/journal/evidence. No broad staging, stash/worktree/branch cleanup, global Docker prune, accepted-volume reset or browser fake identity |
| Publication/deployment | Current request does not authorize Git publication or product execution. Later stage authority covers its named local test/candidate actions; external push/merge/transfer or trust-store changes need their own scope |
| Dependencies | Use locked upstream packages. Exact ECharts 6.1.0 addition is proposed here; no custom PyArrow/chart/auth substitute. Internal license/scanner findings retain report-only policy and do not create new delivery gates |
| Documentation | Update affected existing contracts/runtime/Web-source/help pages and generated docs index when behavior changes; preserve this plan's bound bytes after acceptance and keep attempts in the journal |
| Sensitive data | Runtime secrets in owned protected files only. Reports contain safe identities, aggregate expected/observed values, redacted errors/screens; no credential/DSN/token/cookie/browser-storage/raw row dumps |

## Execution artifact binding

| Field | Binding |
|---|---|
| `plan_doc` | This file; version `0.2.0`; exact SHA-256 in each prompt and journal |
| `prompt_pack_dir` | `.codex/agents/generated/MS-003/` — six stage prompts, no second control document |
| `stage_ledger` | [MS-003 journal](../../../../../.codex/delivery/ledgers/MS-003.md) |
| Validation | Repository `prompt-pack/v1`; `stage-prompt/v1`, `prompt-pack-ledger/v1`, `prompt-pack-receipt/v1`; `tools.custometry_quality.prompt_pack_validation` and `validate_prompt_packs` |
| Claim/update | Existing `custometry-stage-ledger/v1`, POSIX lock + private session + CAS + atomic replacement; exact current implementation/test evidence bound in preparation capability evidence |
| Mode | `manual_sequential`; initial `draft`, no current stage, all rows pending/disallowed, no fabricated execution receipt |
| Authoring boundary | A nonaccepted plan may structurally validate only while the whole pack is an unclaimed disallowed draft. Entry still requires accepted plan, owner execution request, actual inputs and exclusive updater |

After preparation, `uv run --locked python -m tools.custometry_quality.validate_prompt_packs`
and `uv run --locked python -m tools.custometry_quality.prompt_pack_validation
--root . --ledger .codex/delivery/ledgers/MS-003.md --check draft` must exit 0 with
`status: pass`. Entry uses `stage_ledger preflight --ledger ... --stage MS-003-S01`
after actual acceptance and authoring activation preparation; it must fail while
the decision is pending. Invalid/nonzero/unavailable results are never a pass.
Execution evidence uses immutable receipts; the runner alone claims, pauses,
resumes, accepts and advances. No Goal mode or fourth progress register.

## Owner decisions and history

| Decision ID | Question | Alternatives/consequence | Recommendation/basis | Decider | Blocks | Decision/source/date/version |
|---|---|---|---|---|---|---|
| MS-003/DEC-01 | Accept WS-002/MS-003 `0.2.0` and the proposed first sales scenario, subset and proof boundary? | Accept this complete prepared-data draft cycle; or amend concrete source/controls/policy before starting | Reuse verified project components; gives a useful report before full admin while preserving future semantics | Owner | S01 entry | Pending; question/recommendation raised 2026-09-12. Exact answer belongs in the journal before any allowed entry |
| MS-003/DEC-02 | Implementation and agents | Run one requested stage after acceptance; separate Goal/parallel authority if wanted | Manual sequential pack follows existing owner preference | Owner | Actual execution, not document preparation | No stage execution requested by this authoring task |
| MS-003/DEC-04 | Include Customer and Product reference data? | Load both directories and ReceiptItem relationships in this milestone | Six-table governed source; keep the report at receipt grain | Owner | Source scope for S01 | Accepted source inclusion: owner correction on 2026-09-12; the 0.2.0 mapping/remediation detail remains part of DEC-01 review |
| MS-003/DEC-03 | Accept finished behavior and visual conformity? | Accept demonstrated scope or identify concrete missing criterion | Review actual S05 candidate, with evidence ready in S06 | Owner | Milestone closure | Future final-result decision; not an authoring entry gap |

One combined owner review can settle L2/L3 and first-scenario decisions; no
separate approval round is required for routine technical bookkeeping. If the
owner requests changes, revise the unclaimed drafts and rebind hashes. Before
first runnable entry, record exact accepted versions and synchronize all hashes. While the journal is
still an unclaimed `draft`, Prompt Manager sets only S01 `execution_allowed=true`
after resolving its decision packet and checking declared inputs/capability. Then
run the read-only `stage_ledger preflight`; on success the runner may claim only
under the owner's actual execution request. Failed preflight leaves the draft
unclaimed for correction. This order avoids requiring preflight to pass before
the unique initial allowance exists. Do not manufacture acceptance to satisfy a
validator.

| Version | Date | Change | Affected references | Authority |
|---|---|---|---|---|
| 0.2.0 | 2026-09-12 | Expand to six source tables with Customer/Product/ReceiptItem; fix keys, relationships, explicit orphan handling and receipt-grain proof | WS-002 0.2.0; six prompts/journal; parent navigation 2.0.2 | Owner requires customer/product inclusion; concrete amended plan remains in review |
| 0.1.0 | 2026-09-12 | Concrete first-report design, six stages and single journal | WS-002, six prompts, capability/preparation evidence | Current owner preparation request; new content under review |

## Mandatory documentation handoff

Maintain reciprocal WS/map/direction/index references and all triad bindings.
No completed milestone evidence is edited. Pack preparation and later execution
checks are recorded separately in the canonical journal and its immutable evidence.
