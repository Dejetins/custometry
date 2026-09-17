# MS-003-S03 — versioned owned drafts and exact preview snapshots

Milestone: MS-003. Stage: MS-003-S03. Iteration: 1.
Plan: [MS-003 0.2.0](../../../../../docs/architecture/planning/milestones/MS-003/plan.md).
Journal: [MS-003](../../../ledgers/MS-003.md).
Prompt: [MS-003-S03](../../../../agents/generated/MS-003/MS-003-S03.md).
Plan SHA-256: `4a6b1bf2a64a04b74e073bb22e46895795e187be57fe93b6711408069d6e7280` (unchanged).

## Scope and results

Presentation now owns the bounded common `AnalyticalDocumentCompositionV1`, one
`workbook_report` template, stable ordered page/section/metric-group/chart/table/trust
IDs, immutable draft versions and exact root/page snapshots. New documents receive
new node IDs; edits retain them. PeopleService remains byte-identical to entry.
There is no separate sales document store or computation inside Presentation.

The API exposes prepare, create/list, latest draft read, CAS version save and exact
preview. It reuses the real Identity session adapter, current Analytics result owner
port and Artifact Lifecycle adapter. Browser mutations require the existing
Origin/CSRF checks; read responses prohibit caching. Ownership, report permissions
and current result policy intersect; no installation-admin bypass exists. A matching
snapshot/page/block/version locator opens exact data; mismatched locators deny.

`POST /prepare` persists a validated canonical line ChartSpec plus actual versioned
system BrandProfile/CompanyPack records. The packaged system palette is copied from
accepted local token values and carries the original source SHA/version; CompanyPack
pins the S02 metric IDs, hashes, units and formats. Save consumes exact known ID/hash
pairs and rejects unknown, malformed or incompatible bindings. Web compilation and
render behavior remain S04 work.

The actual preserved dataset is `e81d5594-b690-5863-8650-9f21e1a8db84`, QualityReport
`c23cb37a-52b8-5597-8968-81508272b212`, result
`5cd26336-11ad-5156-8d62-7ee4ce9a12a4`. Default totals remain `393858.68` EUR,
`2144` receipts and `183.7027425373134328358208955` EUR/receipt. The root retains all
six entity/hash bindings, Calendar, current-only relationship policy, locked
eligibility, metric/parameter/schema/grain/unit identities and the five quarantined
item limitation. [Runtime proof](runtime-proof.json) records actual report/snapshot,
ChartSpec/default IDs and hashes, root/page manifests and safe aggregate values.
No live directory or new source-version resolution occurs on reopen.

## Acceptance coverage and proof boundary

- **AC-04 / TECH-05/06:** real PostgreSQL transactions prove four same-key saves
  return one identical version, two competing editors yield one successor and one
  `REVISION_CONFLICT`, and changing a used key returns `IDEMPOTENCY_CONFLICT`.
  A fault after the version INSERT and before latest switch rolls back the version
  and leaves the prior complete draft readable. Stable node IDs survive edits;
  the exact first snapshot remains unchanged after a new title/result version.
- **AC-04 / references:** the API creates real canonical records; unknown spec,
  brand and pack IDs fail. Integration also inserts a known but incompatible chart
  and mismatched brand/pack through the test persistence boundary, and verifies
  rejection. Reopen returns the exact original valid ID/hash/projection bindings.
- **AC-04 / TECH-08:** a fresh owned test database starts at actual `0010_sales_report`,
  ingests real source data and writes a real S02 result before upgrading. Upgrade to
  `0011_presentation_drafts`, repeated upgrade, original manifest counts and prior
  result readability pass. Downgrade after document writes is rejected without data
  loss. Earlier migration bytes remain unchanged. [Owned runtime upgrade](runtime-upgrade.json)
  records the protected pre-upgrade backup and additive migration.
- **AC-06 / integrity and access:** foreign principal/workspace, changed effective
  policy, missing manage permission and corrupt/missing root/page/result artifacts
  cannot expose data or hidden counts. Real staging obstruction and metadata
  alteration fail safely; subsequent reads retain the last complete version. The
  setup administrator has workspace-owner functional permissions but still receives
  404 for another creator's report and zero visible report entries.
- **AC-06 / no compute:** an independent production API process opens the same latest
  and historical snapshots with the calculation and Semantic source ports disabled.
  An actual HTTP calculation request verifies that the injected unavailable provider
  rejects compute, while exact reads pass. The isolated integration test also deletes
  its historical source files and reopens both versions. The real Hybrid source is
  never modified. Real session revocation denies both original and fresh-process reads.

Requirements covered within this subset: ANALYTICAL-DOC-001/002/006/007/015,
CHART-001/002 (spec/data identity only), REPORT-002/003/004/005/008/012/014 and the
S03-owned portion of AC-04/06. This is real local PostgreSQL, files, authenticated
HTTP and fresh API-process evidence. It is not browser/visual fidelity, compiler,
packaged/HTTPS, published/shared/refresh, production, performance or release proof.

## Contracts, consumers and recovery

| Surface | Baseline → implementation | Classification and required order |
|---|---|---|
| Existing Analytics/People APIs | Original endpoints/schemas and PeopleService retained; composition factory made public for app wiring | `compatible-change`; existing Analytics unit/contract suites pass and old OpenAPI remains equal |
| Presentation API/DTOs | No document endpoint → independently versioned draft API, explicit input contract version and generated client/schema projections | `compatible-change` for existing clients; S04 must consume new API/schema, older servers cannot serve it |
| Result owner integration | Presentation reads exact authorized `AnalyticsService.get_sales_report` | `compatible-change`; preserves S02 policy identity and no-source-read behavior, never queries private Analytics/Semantic tables |
| Artifact integration | New public snapshot port, Artifact-owned immutable JSON adapter | `compatible-change`; existing manifests/readers remain valid, root/page dependencies are committed before document visibility |
| Persistence | `0010_sales_report` → additive Presentation references/documents/versions plus constrained latest pointer | `compatible-change` for new reader with old data; apply migration before new endpoints |
| Post-write rollback | Old application cannot read the new documents; downgrade deliberately refuses to drop saved versions | `breaking-change` for lossless downgrade expectations; retain pre-upgrade owned backup/immutable files or forward repair |
| Configuration/dependencies | Existing Hybrid environment, artifact root and locked packages | `none`; no dependency or deployment topology change |

The [authoring contract](../../../../../docs/contracts/analytical-authoring-contract.md)
advances 3 → 4 and includes the credential-free client example. The
[artifact contract](../../../../../docs/contracts/artifact-format-contract.md) advances
2 → 3, with reciprocal implementation/evidence links. Architecture navigation
advances 35 → 36; generated documentation is checked. Accepted plan/pack bindings
and completed MS-001/MS-002 artifacts are unchanged. Mutable document snapshots are
retained under this stage before receipt binding.

Residual limits: failed/concurrent saves may leave unreferenced immutable artifacts;
no orphan-cleanup service is implemented. Source/result permissions must still be
available at read time. The protected backup is not an externally published backup
and no restore/installation qualification is claimed. Current-only dimensions,
degraded product/basket coverage, and bounded template/line-chart scope remain explicit.

## Files, checks and execution history

[Validation evidence](validation-evidence.json) records exact final commands, actual
outcomes and a SHA-bound owned file manifest. Source changes are limited to new
Presentation contracts/domain/application/PostgreSQL and token adapter, report API
composition, additive migration, generated schemas/OpenAPI/client, focused tests,
canonical documentation and this evidence directory. Nothing is deleted.
The necessary extra provider path is
`packages/artifacts/infrastructure/document_snapshots.py`: only Artifact Lifecycle
can own the new root/page commit/read adapter. The existing Analytics router has a
separable factory-name/public-composition hunk; its route behavior is unchanged.

There were no foreign changes at entry. No agents, new branch/worktree/stash,
commit/push/merge, production deployment, external transfer, dependency installation,
foreign data reset or completed-evidence rewrite was performed. Formatting-only
changes accidentally introduced to PeopleService were removed before handoff.
The journal is mutated only by its exclusive updater.

Initial failed checks are not passes: the staging-obstruction test first reached
S02's broad artifact-unavailable error; the new Presentation adapter now normalizes
its chained missing-file/storage failure without changing S02. Fixture teardown was
made unconditional for its own rows. Focused Ruff/type diagnostics were corrected.
The fresh-process proof initially injected an unhandled 500 that closed keepalive;
it now injects a typed unavailable-provider failure and verifies that response.
The admin-negative test originally assumed 403, but the existing workspace-owner
role explicitly includes analytical permissions; its correct no-ownership result is
404 and a zero-count list. No product permission was changed to satisfy that test.

## S04 handoff

The full [S04 prompt](../../../../agents/generated/MS-003/MS-003-S04.md) was read.
[Next-entry checks](next-entry-check.json) bind its declared inputs and actual
S03 outputs; all are readable. S04 consumes the new API, real canonical ChartSpec
and system-default projections, with `daily` and `comparison.daily` as immutable
sources. It implements compiler/render, UI, browser proof and pilot fidelity.
It must not replace backend reference creation with fixtures or compute on open.

Current journal authority permits enabling S04 after S03 acceptance. Manual
sequential execution stops here; enabling S04 is not claiming or executing it.
