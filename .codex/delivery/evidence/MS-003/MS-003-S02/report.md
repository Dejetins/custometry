# MS-003-S02 — registered immutable daily sales results

Milestone: MS-003. Stage: MS-003-S02. Iteration: 1.
Plan: [MS-003 0.2.0](../../../../../docs/architecture/planning/milestones/MS-003/plan.md).
Journal: [MS-003](../../../ledgers/MS-003.md).
Prompt: [MS-003-S02](../../../../agents/generated/MS-003/MS-003-S02.md).
Plan SHA-256: `4a6b1bf2a64a04b74e073bb22e46895795e187be57fe93b6711408069d6e7280` (unchanged).

## Delivered scope and observed values

Implemented TECH-03/04 through the existing AnalyticsService, Semantic owner,
Artifact Lifecycle and PostgreSQL repositories. Exactly three immutable metric
definitions include qualified receipt grain, numerator/denominator version refs,
English/Russian labels, units and formats. Completed/EUR is locked; excluded
returns/cancellations do not become refund-adjusted revenue. No item/customer join
is involved in receipt aggregates. The explicit daily MART-SALES-PERIOD projection,
chart data, table data and totals share one immutable `sales-report/v1` artifact.

The real S01 preparation was replayed without changing its input IDs or source
fingerprint. Dataset `e81d5594-b690-5863-8650-9f21e1a8db84`, QualityReport
`c23cb37a-52b8-5597-8968-81508272b212` and all six canonical bindings remain pinned.
The actual API results reconcile to independently written readonly source SQL:

| Inclusive UTC period | Store | Net EUR | Receipts | Average EUR/receipt |
|---|---|---:|---:|---:|
| 2025-01-01..2025-11-30 | all | 393858.68 | 2144 | 183.7027425373134328358208955 |
| 2025-01-01..2025-11-30 | 1 | 20610.80 | 109 | 189.0899082568807339449541284 |
| 2024-01-01..2024-11-30 | all | 428374.84 | 2235 | 191.6665950782997762863534676 |
| 2025-06-01..2025-06-30 | all | 39765.08 | 200 | 198.8254 |

The first result with previous-year comparison is
`5cd26336-11ad-5156-8d62-7ee4ce9a12a4`; its committed JSON SHA-256 is
`baca5675d3533d9d50bc041e9b1c6a5efef946ffefb1bc3cc90f96c78e8b1d29`.
[Runtime reconciliation](runtime-reconciliation.json) contains all result/artifact
IDs and exact metric versions/definition hashes. [The retained oracle](verify_runtime.py)
compares each observed daily value to source SQL and each complete JSON payload to
its actual artifact bytes; no production aggregation helper supplies expected values.

## Criterion coverage

- **AC-03 / METRIC-001/002/004/005/007/008:** independent header-only SQL matches
  totals, ratios and every observed daily aggregate for all stores, selected store,
  changed period and previous-year same dates. Ratios recompute from totals, not
  daily ratios. Tests cover null/nonfinite amounts, negative values, mixed source
  currencies with locked EUR selection, excluded statuses, duplicate qualified keys,
  empty days, partial/missing Calendar coverage, leap-day boundaries and UTC conversion.
- **AC-03 / source lineage:** all six entities and scoped DQ accounting remain in
  Result Trust. The real corpus has three item lines per receipt, 111 anonymous
  eligible receipts in the default period, and five quarantined product links.
  Header-only SQL retains eligible headers linked to those items exactly once;
  aggregate evidence records them. Multiplying item lines in the focused test cannot
  alter header totals. Product/category/brand controls return validation errors.
  Product/basket coverage stays degraded; dimensions remain current-only.
- **AC-06 / identity and publication:** four concurrent production-service calls
  on a real isolated PostgreSQL and four actual HTTP calls coalesce to one exact
  result. Period, store, dataset and effective-policy changes separate identity.
  Result files use atomic no-replace publication; metadata uniqueness verifies the
  exact authorized winner. All canonical source hashes plus raw/quarantine artifact
  visibility/integrity are checked on compute/reuse; result reads verify manifest
  identity and exact content and never substitute a latest version.
- **AC-06 / retention and failures:** real filesystem corruption and missing source
  and result files fail explicitly. Controlled next-input snapshots change receipt
  amounts through the test intake boundary over real source rows, yielding a new
  dataset/result while preserving the exact prior result. The real source database
  is never modified by this test. Old-result reads work with unavailable source
  files. Workspace/owner separation, policy changes, real session revocation on both
  read and repeated POST, unsupported store values and absent CSRF are denied.
  A real filesystem staging obstruction returns a stable storage failure.

## API and S03 consumer instructions

Use the ordinary analyst session through the owned Hybrid Web/API prefix.
`POST /api/analytics/sales-reports/v1` accepts:

```json
{
  "semantic_dataset_version_id": "e81d5594-b690-5863-8650-9f21e1a8db84",
  "starts_on": "2025-01-01",
  "ends_on": "2025-11-30",
  "store_id": null,
  "comparison": "previous_year_same_dates"
}
```

The period and comparison default to 2025-01-01..2025-11-30 and `none`; a window
contains at most 366 dates. Mutation uses the current session's CSRF header and
same-origin policy. The synchronous operation exposes no fabricated progress/ETA.
`GET /api/analytics/sales-reports/v1/{result_id}` consumes the exact result, with
current Identity permissions and artifact verification, without source access or
calculation. Old `/analytics/results` operations and component schemas are unchanged.

The [OpenAPI](../../../../../packages/contracts/openapi/analytics.openapi.json),
[request schema](../../../../../packages/contracts/schemas/sales-report-request.schema.json)
and [generated client](../../../../../packages/contracts/src/analytics-client.ts)
are provider/drift checked. `@custometry/contracts` exports `salesReports` including
`SalesReportClient`; its base URL is `/api/analytics`. No browser storage credentials
or client-side business calculation is introduced.

S03 consumes the AnalyticsService owner methods, never private Analytics tables.
Intersect document permissions with result permissions; pin the result manifest,
metric versions, Calendar artifact, dataset/source hashes, current-only relationship
policy and QualityReport. `daily` is the shared chart/table source; `totals` is
server-calculated. Empty-day values are null, with an explicit state; Calendar
coverage is imported metadata, not inferred from observed sales. An incomplete
comparison returns unavailable values. Preserve these states and limitations in
snapshots. Presentation document APIs, ChartSpec and system BrandProfile/CompanyPack
are S03's outputs and remain deferred.

The full S03 prompt was read. Its five declared inputs are checked in
[next-entry evidence](next-entry-check.json). Current S03 authority is recorded in
the journal. Acceptance can enable S03; this execution does not claim or run it.

## Validation and execution boundary

The authoritative command outcomes, source manifest and proof limits are in
[validation evidence](validation-evidence.json). Commands run after
`source scripts/activate-toolchain.sh`:

- `uv run --locked pytest -q tests/unit/analytics tests/contract/analytics`:
  24 passed, including existing v1 regressions and generated request/client drift.
- `uv run --locked python .codex/delivery/evidence/MS-003/MS-003-S02/run_tests.py`:
  2 integration tests passed against `custometry_ms003_s02_tests`; upgrade/repeat
  uses the owned control server and never truncates the prepared database.
- `prepare_runtime.py`: real owned Hybrid upgrade to `0010_sales_report`, followed
  by successful unchanged S01 preparation replay.
- `verify_runtime.py`: real HTTP/SQL/artifact reconciliation and session-revocation
  checks passed; four same-key HTTP responses were identical.
- Focused Ruff and Pyright, contracts TypeScript and the source `local` profile:
  final outcomes are recorded in validation evidence alongside documentation gates.

Initial failed checks are not counted as passes: eager artifact-directory creation
at API import was moved to actual use; the Foundation no-input HTTP generator was
inapplicable, so the client reuses its DTO renderer with bounded request methods;
new Decimal optional-type errors were fixed and existing service dictionary type
annotations were narrowed without changing their calculations. No dependency was
added or upgraded and no assertion was relaxed.

Observed boundary: owned real source/control PostgreSQL, real ingestion artifacts,
registered metrics, immutable daily result and authenticated HTTP. No document/UI,
packaged candidate, VM/LAN, workload/SLO, release, external publication or production
claim. Calendar completeness remains the imported declaration. A policy change
intentionally denies older-policy result reads; S03 must not bypass that check.

## Compatibility, documentation and recovery

| Surface | Classification and conditions |
|---|---|
| Existing analytics API/data | `compatible-change`: old paths and schemas compare equal to HEAD; existing unit/contract/real integration tests pass; new endpoints use separate projection/table |
| Semantic | `compatible-change`: exactly three new immutable definition IDs in a separate table; old publications/artifacts are unchanged |
| Persistence/artifacts | `compatible-change` for current/new readers: nullable producer batch only for new analytical outputs, preserving ingestion replay; all source lineage uses dependencies; old batch queries retain original behavior |
| Rollback after new writes | `breaking-change` for restoring the old NOT NULL batch invariant with new result artifacts present: downgrade fails rather than deleting them; use forward repair; no lossless data downgrade claim |
| Policy/cache identity | New version only: current workspace/actor/permission identity separates results and denies old-policy reads; no old-result namespace rewrite |
| Config/dependencies | `none`: existing runtime/environment and locked dependencies; new API requires migration before use |

Authoring contract advances 2 → 3; artifact format contract 1 → 2. Their new bounded
sections link this evidence and each other; architecture navigation and generated
documentation index are maintained. The accepted plan's baseline document versions
remain unchanged and the compatible implementation deltas are documented here.
Normative blueprint meaning, planning scope and completed MS-001/MS-002 bytes are
unchanged. Immutable documentation snapshots are bound by the receipt.

There were no foreign checkout changes at entry. The validation manifest lists
created/modified paths and exact source hashes; nothing was deleted from the
repository. Changes are limited to Analytics/Semantic/Artifact contracts/adapters,
API composition, the additive migration, focused tests, affected documentation and
this stage's evidence. Small typing-only hunks in the existing service enable its
focused type gate. The stage journal is changed only through its exclusive updater.
No agent dispatch, branch/worktree/stash, commit, push, merge, cleanup of accepted
state, dependency installation or deployment was performed.

Residual operational limit: failed metadata publication can leave an unreferenced
artifact; no result success is returned and no generic orphan-cleanup implementation
is claimed. Runtime protected files and artifact volume must remain available.
Current-only dimensions, degraded product/basket coverage and draft/document work
remain their explicit boundaries. The next safe execution unit is S03 after the
receipt-backed transition, under manual sequential execution.
