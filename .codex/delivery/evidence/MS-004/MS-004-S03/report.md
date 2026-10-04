# MS-004-S03 — guarded APIs and atomic configured report revisions

Stage: MS-004-S03. Iteration: 001. Accepted plan: MS-004 0.2.1, retaining design
0.2.0, D01–D08 and AC-01…11. Baseline: `750b28f145c3dcd7c833cac71814444f5f4a7fa7`.
This report covers local API/PostgreSQL/artifact implementation, not browser,
packaged delivery, release, production or finished-milestone owner acceptance.
The [canonical journal](../../../ledgers/MS-004.md) alone owns execution status.

## Implemented boundary

- Identity owns a public current-resource decision projection. Request adapters
  reauthenticate actual sessions/tokens and intersect functional, object and data
  policy. Immutable creator identity additionally protects old and new report
  definition writes; an administrative role or edit grant is not creator identity.
- Presentation owns configured report, exact legacy/base reads, personal Saved
  Views, per-card bindings, typed errors and complete report/companion-view CAS.
  All worksets, including inactive cards, are validated before one transaction
  switches the complete report/view latest pointers. Apply does not mutate them.
- Analytics owns current access, exact query/result verification, input/output
  integrity and comparison verification through public ports. Report-authorized
  legacy result verification is internal and checks the real stored result owner;
  direct HTTP requests cannot supply arbitrary owner/access fingerprints.
- Public `/api/reports/v2` and `/api/analytics/metric-workspace/v2` routes are
  mounted with real Identity adapters and mutation CSRF enforcement. The existing
  v1 HTTP path gains current object/data checks and mixed v1/v2 permission-filtered
  listing. v1 snapshots retain their bytes; upgraded v1 latest/update returns 409.
- Generated strict contracts, editor/OpenAPI and TypeScript client expose current
  editor capabilities, report/view revisions, exact result/comparison/chart
  projections and `WorkspaceRequestError` with code/status/retryable. Display-only
  creator Apply may verify `reuse_result_ids` without `analysis.run`; calculations
  require run permission. No GET computes or silently repairs artifacts.
- Calendar defaults remain independent of pinned report versions. Creator-only
  explicit Apply/Save adopts a new version; old snapshots preserve prior bindings.

Implementation entrypoints are
`packages/presentation/application/workspace.py`,
`packages/presentation/infrastructure/workspace.py`,
`packages/identity_access/application/resource_access.py`,
`packages/identity_access/infrastructure/resource_access.py`,
`packages/analytics_core/application/snapshot_verification.py`,
`apps/api/src/custometry_api/reports/workspace_composition.py`,
`apps/api/src/custometry_api/reports/workspace_router.py`, and
`apps/api/src/custometry_api/analytics/workspace_access.py`.

## Criterion and requirement evidence

Affected requirement IDs: METRIC-021/022/025/026/027/028/030, CHART-021,
COMPARE-013, REPORT-018 and ANALYTICAL-DOC-015. WEB-ARCH-003/004,
A11Y-001 and I18N-001 remain S04/S05 presentation-proof obligations.

| Criterion / source | Implemented and observed boundary |
|---|---|
| AC-01/05; METRIC-025/026/027, ANALYTICAL-DOC-015 | Stable worksets/cards, equivalent-context distinct bindings, all active/inactive cards, retired-ID rejection, empty definition, explicit Apply versus complete Save/exact reopen; report and companion view concurrency and independent reader views. |
| AC-06 | Original unbound owner v1 read/exact/replay and v2 editor entry; stranger denied; strict old snapshot equality after upgrade, mixed filtered listing, v1 upgrade-required, real old-schema v1 result migration with preserved payload/artifacts. |
| AC-07; REPORT-018 | Actual author, reader/admin with grants, scoped token without run, cross-workspace session and revoked session. Current dataset scope, store ceiling and unsupported scope denial; privacy of creator overlay and reader views; old/new precommit revocation and access-checked replay. |
| AC-09 | One winning concurrent Save, stale report/companion revision, exact replay and changed-body conflict, missing/corrupt result/comparison artifacts, injected artifact and pre-pointer DB failures. Fresh connections verify prior complete pointers after failure. |
| AC-11; METRIC-030 | Changed April default does not alter existing calendar pin. Explicit creator adoption creates another saved revision, while old exact snapshots remain unchanged. Full six-grain/SQL/leap/fiscal math evidence remains S02 and is not reclassified as S03 browser proof. |
| S03 activation prerequisite | Current public access adapters guard every mounted v2 report/result/context/catalog/comparison route. Negative cases use real Identity sessions, organization resource bindings/policies/grants, real PostgreSQL and artifact bytes. |

The actual commands, outcomes and proof limits are in [validation](validation.md).
The redacted [corpus](corpus.json) records synthetic dataset/snapshot identities,
six admitted source dependencies, result/comparison manifest hashes and observed
HTTP status counts. It contains no credentials, tokens or source rows.

## Compatibility, documentation and ownership

| Boundary | Classification and consequence |
|---|---|
| API/DTO/generated client | compatible-change: additive explicitly versioned routes and strict unions; v1 snapshot bytes unchanged; upgraded latest v1 consumers receive the accepted explicit upgrade-required response. |
| Identity/data access | compatible-change within accepted REPORT-018: current fail-closed object/data projection and immutable creator guard; supported store scopes only. Arbitrary row expressions/column restrictions remain unsupported and denied. |
| Persistence | compatible-change using existing S01 tables/discriminators, additive revisions and atomic dual-CAS; no S03 migration or old snapshot rewrite. |
| Cache/identity | compatible-change: current policy version participates in access/result verification; no cross-actor result reuse. A changed allowed policy requires explicit re-Apply. |
| Side effects/recovery | compatible-change: explicit Save transaction and owned artifact admission; failed Save can leave unreferenced immutable artifacts for existing retention, never a partial latest report. |
| Browser/operations | Web integration deferred to S04; no browser/runtime topology/deployment change or performance claim. |

Canonical authoring/recovery contracts, Web handoff source contract and architecture
navigation are updated with current API boundaries and historical S01/S02 context.
Generated schema/OpenAPI/client and documentation indexes are synchronized. The
accepted plan, prompts, source blueprints and earlier consumed receipts are unchanged.
[Owned files](owned-files.json) records exact final source hashes. The existing
S02 synchronization evidence is coordinator-owned and excluded. Journal entry/
advance changes supplied by the coordinator are preserved; this executor uses
only its own claim/receipt transition, never direct journal edits.

The legacy migration regression needed an old-column-shape writer only in its
pre-0012 fixture: the current Analytics adapter correctly requires the migrated
`contract_version` column. The fixture still persists a real v1 result before
migration and verifies its exact retrieval with the current adapter afterwards.
The migration backfill also required disposable-fixture cleanup of its own calendar
records before workspace teardown. Its immutability trigger remains active for all
assertions and is disabled only inside the isolated teardown transaction. No
production compatibility fallback or weakened schema was introduced.

## S04 handoff and limitations

S04 consumes the generated workspace editor/client (`configuredReports` export)
and Semantic calendar client,
actual v2 HTTP routes and current capabilities. Preserve the native pilot and
server-owned projections; handle both report and view CAS, explicit Apply/Save,
stale/error draft preservation, reader-only overrides and creator calendar adoption.
Report source paths and S04 entry files have been inspected; its own browser config
and real API fixture are S04 outputs, not missing S03 deliverables.

No complete METRIC-022 published-default reset is claimed: the pinned v1 draft base
is lineage for authorized reader access, not a published default. Shared worksets,
publication, additional metrics, Forecasting and MS-003 deferred stages remain out
of scope. These tests use real ASGI API handlers, isolated PostgreSQL and artifacts;
HTTP proxy/network delivery, browser behavior and owner demonstration remain S04/S05.

S04 remains disallowed until coordinator review and technical-branch PR/Foundation
synchronization, confirmed remote main and branch deletion, followed by supported
`advance` with current input evidence. This executor creates no commit, branch, PR,
merge, deployment or successor task.
