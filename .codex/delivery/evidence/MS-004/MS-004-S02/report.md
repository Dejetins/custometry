# MS-004-S02 — fiscal-grain calculation and immutable results

Date: 2026-09-20. Iteration: 1. Baseline:
`b4aaa1680cfff5885fe61ff98fe7e69cf4934df0` plus coordinator-owned S02 advance
and S01 synchronization evidence. Accepted plan 0.2.1 remains unchanged.
The coordinator's current S02-only instruction supplies implementation authority.
The [canonical journal](../../../ledgers/MS-004.md) alone owns execution status.

## Delivered boundary

- `packages/analytics_core/application/workspace_calculation.py` implements
  D03 normalization and D04 math. Common/local stores are validated then intersected
  with trusted allowed scope; null inherits and empty stays empty. Identity binds
  workspace/actor/policy/scope, publication, six input bindings, the unchanged three
  registered metric/component definitions, pinned calendar, period/grain/alignment
  and calculation version. Output ordering is canonical too; shuffled provider
  bindings/definitions cannot give equal IDs with different bytes.
- UTC receipt-header aggregation produces all six calendar/fiscal grains. Results
  carry exclusive natural/effective bounds, clipping, fiscal indices, daily
  components and distinct expected/Calendar/declared-complete/observed coverage.
  Average receipt is recomputed from revenue/count with local Decimal precision
  38; no average-of-averages or item fan-out. Empty values stay null, genuine zero
  stays zero. January/April/October and both FY label conventions are exercised.
- Same-dates comparison maps every current date before bucketing. Current Feb 29
  without a prior date blocks its bucket and whole-period delta, not unaffected
  days. Prior unmapped leap day is excluded and disclosed. Both sides' coverage,
  baseline dates and typed raw/server delta values remain explicit.
- `workspace_service.py` resolves current access via mandatory public provider port,
  verifies pinned Semantic calendar/registry/inputs, rechecks access on return,
  groups equivalent batch contexts and keeps card/configuration bindings separate.
  It creates typed pair/temporal comparison artifacts; unit mismatches have no
  subtraction/percentage, incompatible period/grain/calendar/basis has no combined
  buckets, and zero baseline keeps a valid absolute delta but no relative delta.
  Application binding checks retain registered unit/projection/format meaning.
- `packages/artifacts/infrastructure/workspace.py` reuses existing admission,
  manifest and dependency mechanics for immutable v2 result/comparison JSON.
  Existing Analytics PostgreSQL uniqueness returns one exact concurrent winner;
  its stored discriminator is now explicitly taken from the result contract.
  Missing/corrupt input/output fails; no silent repair or recomputation on GET.
- `custometry_api.analytics.workspace_router` provides unmounted result, context,
  catalog and comparison adapters. It requires injected read/run actor dependencies
  and a service with an actual access provider. No production composition imports
  or mounts it. The OpenAPI remains components-only. Existing generators emit the
  completed result/comparison and Analytics request/batch shapes and TypeScript.
- Updated authoring contract v13 and recovery contract v4 with implementation,
  proof limits and reproducible isolated runner. Existing accepted plan, prompts,
  historical evidence, original checkout, v1 calculation and MetricVersions remain
  untouched. No new dependency, migration, service, queue or deployment.

## Criterion evidence and boundary

| Criterion | Evidence | Limits |
|---|---|---|
| AC-02 | Null/empty/disjoint/denied/unknown scope, equivalent inherited/explicit contexts, separate copied card IDs, policy/actor identity partitions and concurrent winner checks | Trusted projection seam is exercised; real Identity/report resource authorization is S03 |
| AC-03 | Independent readonly PostgreSQL receipt SQL for all six grains, both bases, January/April/October starts and both year labels; exclusive boundaries, coverage and ratio counterexample | Local synthetic six-table source, not production or browser proof |
| AC-04 | Independent SQL current/prior date mapping including year-crossing week, mapped baseline totals, positive two-period values, leap/empty/zero/incomplete cases; all three unit pairs and typed incompatibility reasons | S04/S05 consume the same artifact values in actual UI; no UI claim here |
| AC-11 calculation | Financial boundary/year-label matrix; full April–March leap-crossing year; pinned calendar mismatch; changed calendar refs partition identity | Settings writes were used through real Semantic repository; S01 owns settings API proof, S03/S04 report adoption |
| AC-07 prerequisite | Production app returns 404 on new v2 route probes; adapters run only in an explicitly composed test app | No production v2 endpoint activation or real object/data authorization claim |

[Validation](validation.md) records commands and outcomes;
[corpus evidence](corpus.json) records actual admitted IDs/hashes, dates/counts and
independent oracle coverage. Evidence contains no raw source rows or credentials.
The test `Access` object is an explicit trusted projection double, not a claim that
Identity's real current-access integration already exists. Production SQL, intake,
Semantic versions, result persistence and artifact files are real. Test-only HTTP
composition uses an explicit actor dependency; it does not prove CSRF/authentication.

## Contract impact

| Surface | Classification / supported interaction |
|---|---|
| v1 computation, routes and result bytes | `none` for formats/math; preserved original algorithms and generated v1 files, real v1 integration regression retained |
| Existing result repository | `compatible-change` after migration 0012: writes explicit v1/v2 discriminator; original v1 payload and uniqueness are preserved |
| S01 v2 DTO foundation | `breaking-change` for a hypothetical consumer constructing the previous incomplete DTO: mandatory D04 coverage/boundary and comparison fields are added before public activation; regenerate all in-repository consumers together; no mounted v2 client was supported |
| Public v2 HTTP | `none` for exposure: remains unavailable; opt-in adapter factory is new and cannot be mounted safely without S03 |
| New result/cache and artifact identity | `compatible-change` for coexisting v1: separate v2 calculation/version namespace and actor partition, immutable exact winner verification; no reuse across actors |
| Old-schema rollback after v2 records | Existing S01 `breaking-change` constraint remains: migration refuses downgrade; forward repair or separately authorized coherent backup restore |
| Dependency/deployment/browser | No changes or readiness claim |

## Ownership and handoff

Coordinator-owned incoming changes are the S02 journal advance and
`MS-004-S01/synchronization.md`. They are preserved. S02's own journal changes use
only the exclusive updater and this task's actual session. The coordinator does
not borrow that claim. [Owned source manifest](owned-files.json) identifies stage
files; no broad staging, Git publication or source-checkout mutation occurred.

S03 should compose `WorkspaceAnalyticsService` with `PostgresSalesSemanticRepository`,
`PostgresAnalyticsRepository`, `WorkspaceArtifactStore`, the public calendar port
and a real `WorkspaceAccessPort`. Deny unsupported row/column restrictions; the
current implementation accepts only an explicit permitted-store projection.
Resolve access before context/catalog as well as run/get/compare and after work.
The provider must include current policy versions and scope in its fingerprint.
The report creator/object guard and direct Analytics caller checks remain S03.

Use `apply` for at most 200 distinct card IDs. Presentation supplies the actual
configuration hash from its validated definition; Analytics preserves that binding
and verifies the requested immutable metric. A successful full batch returns all
bindings or raises; no failed card is saveable. S03 must re-verify every binding,
current scope and definition hash before complete atomic Save. For reader exact
snapshots S03 must add the planned authorized shared verification projection;
the S02 `get` intentionally remains actor-owned and never silently narrows data.

`WorkspaceResultV2.comparison` remains null in the reusable context result because
card identities must not enter its bytes. Its `temporal` stores card-independent
mapped component/delta values. `compare` creates the separate immutable
`CardComparisonV1`, with specific card IDs and result-artifact dependencies.
Temporal right-side context is the aligned current axis; its `baseline_dates`
contains original dates. Both sides' coverage is carried with each typed value.

The next prompt and its declared existing entrypoints were inspected. This report
supplies S03's S02-produced input only. `next_stage_allowed:false` is mandatory:
coordinator review, technical-branch PR/Foundation/squash synchronization, remote
confirmation/branch deletion and a fresh `advance` must precede S03. No successor
was enabled and no stage outside S02 executed. Final milestone owner acceptance,
report transaction proof, browser demonstration and release remain unclaimed.
