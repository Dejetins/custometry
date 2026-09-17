# MS-003-S04 — proposed bounded entry-context repair

Date: 2026-09-13. Proposal only; no owner acceptance or backend change is implied.
Plan: [MS-003 0.2.0](../../../../../docs/architecture/planning/milestones/MS-003/plan.md).
Stage: [S04](../../../../agents/generated/MS-003/MS-003-S04.md).
Report: [partial execution](report.md). State: [canonical journal](../../../ledgers/MS-003.md).

## Failed requirement and observed gap

AC-05 / TECH-07 requires an ordinary analyst to create the supplied report from
the library and choose an authorized store using real APIs. At current source
`cb4f696dc1dca3bc051debd347810f7d74caa319` plus the accepted, uncommitted S03 changes:

- `analytics/router.py` exposes POST `/sales-reports/v1` requiring a caller-supplied
  `semantic_dataset_version_id`, and GET by a known result ID. It has no profile
  context/dataset/store discovery operation.
- `reports/router.py` exposes prepare by a known result ID, create/save, list
  existing owned drafts and get/preview by known IDs. An empty library cannot
  supply the input for its first calculation. An earlier test-created report
  cannot be a prerequisite for product operation.
- The older GET `/analytics/results` reads `analytics_results` via
  `PostgresAnalyticsRepository.list_visible`; S02 results are in
  `analytics_sales_reports`. That endpoint is not a discovery path for this profile.
- The Semantic provider has `sales_projection(workspace_id, version_id)`, requiring
  an already known version. It provides artifact bindings. Store membership is
  checked against the governed Store artifact in `build_report`; the report
  response does not return the store option catalog.
- The application's complete mounted API families were inspected in `main.py`;
  imports provides intake mutations and connections provides source-management
  discovery, not an ordinary analyst report-context projection.

The exact production `retail-report/v1` setup exists, with safe version IDs in
S01 output. Hardcoding those local IDs or stores into Web, serving private setup
state through Vite, prompting the analyst for internal UUIDs, or precreating a
report in the E2E fixture would bypass the intended library/template journey.

## Smallest proposed repair

Authorize a separable S04 integration extension for a typed, authenticated
GET `/analytics/sales-report-context/v1` operation. Return only the permitted
published `retail-report/v1` version references, safe display labels, pinned Store
ID/label options, and the supplied template's default period plus visible locked
eligibility/currency. Resolve the exact version explicitly; do not silently take
an arbitrary latest result. An empty/denied/unavailable context stays explicit.

Analytics composes existing Semantic and Artifact owner ports. Semantic owns
published-version discovery; Artifact Lifecycle owns reading its Store artifact.
Web must not read private files/tables or expose connection credentials/management.
Reuse existing `analysis.read` / `analysis.run` checks and workspace isolation;
do not add a permission bypass, new framework, service or database schema.
The existing calculation and save operations remain unchanged.

Requested additional zones: selected files under `apps/api/src/custometry_api/analytics`,
`packages/analytics_core`, `packages/semantic_model`, and only necessary public
Artifact/contract ports plus focused unit/contract/real-database tests.
The current S04 zones already cover generated TypeScript/contracts and Web.
Update affected canonical contracts and indexes without changing the accepted
plan bytes or accepted S01-S03 receipts. Any triad scope reconciliation must use
the runner's explicit authorized mechanism, never a hand-edited active journal.

## Compatibility and proof

| Surface | Proposed effect | Assessment |
|---|---|---|
| Existing calculation, draft persistence, schemas | Retain current operations and identities | `none` intended; regression proof still required |
| New context API and owner ports | Add a discoverable safe report input projection | `compatible-change` proposed; existing callers retained |
| Permissions and artifact access | Repeat existing actor/workspace admission before returning choices | Must be demonstrated with ordinary/outsider/denied tests |
| New Web on older API | First-create controls lack their required context provider | Unsupported until matching server is deployed; explicit unavailable state |

Required proof: real S01 preparation, context discovery with no prior draft or
result, no inaccessible counts/labels, actual store-artifact failure, and a
browser create/apply/save/reopen journey. Unit mocks alone cannot close AC-05.

Owner decision requested: allow this bounded provider/API extension within S04,
with the specified scope/proof reconciliation, or select a different authorized
source-context contract. This decision blocks first-create/store integration and
therefore S04 acceptance. Compiler-only work can proceed independently.
