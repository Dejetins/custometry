# MS-004-S01 — contract and fiscal-calendar foundation

Date: 2026-09-20. Iteration: 1. Baseline: merged main
`471314d42d6c49e0f9cec5f1794b44dbaeb03a14` plus coordinator-owned entry preparation.
Accepted design 0.2.0 / editorial plan 0.2.1 is unchanged. Authority is the
coordinator's S01-only dispatch and journal-linked entry preparation. This report
is execution evidence, not a second state register; the canonical
[journal](../../../ledgers/MS-004.md) owns acceptance and successor allowance.

## Delivered boundary

- Added `packages/contracts/presentation/workspace.py`,
  `packages/contracts/analytics/workspace.py` and `packages/contracts/semantic`.
  Strict v1/v2 unions retain existing v1 fields/enums. New personal definition,
  common composition, ChartSpec, complete card-result, comparison, query/display
  Saved View and public port types are available. The configuration parser bounds
  raw bytes; validators bound days, sets/cards/stores, identity and selections.
  Copy helpers preserve registry references and remap instance IDs. Legacy
  projection uses deterministic IDs, calendar basis and the original base snapshot;
  it never computes, persists or pretends a legacy result is metric-workspace/v2.
- Added Semantic-owned `WorkspaceCalendarService` and
  `PostgresCalendarRepository`. The immutable month-based UTC/Monday profile
  supports January/non-January starts and both year labels. CAS/idempotency,
  actor-bound replay, default-version transaction and exact pinned reads work.
  Bootstrap/workspace creation invokes public idempotent provisioning; an
  authorized default read recovers interrupted/old-writer initialization.
- Mounted only `/api/semantic/workspace-calendar/v1`, its POST `/versions` and
  exact GET `/versions/{version_id}?content_hash=...`. Current Identity sessions,
  active workspace/membership/roles and browser Origin/CSRF are checked. Read uses
  workspace.read; write uses workspace.manage. Scope and policy are rechecked on
  replay. Administrator permission does not grant report-definition rights.
- Added `0012_metric_workspace`, following actual head 0011: immutable creator
  backfill/legacy-insert trigger; explicit report/result discriminators; personal
  Saved View tables with workspace/report/version FKs, revision/key uniqueness and
  latest-version binding; immutable Semantic versions and CAS default pointer.
  Existing JSON bytes are preserved. Initial version identity is UUIDv5(workspace,
  `business-calendar/v1/initial-january`); revision 0 has explicit system attribution
  (`created_by:null`). Human-created versions require a creator and predecessor.
- Added the bounded generator `packages.contracts.generate_workspace_client` using
  the existing Pydantic/OpenAPI/TypeScript rendering pipeline. New workspace
  OpenAPI contains components and **no paths**. Calendar OpenAPI/client includes
  the actual guarded routes and error responses. Existing report OpenAPI/client
  and MetricVersion definitions are unchanged.
- Updated authoring contract v12 and recovery contract v3 to separate this
  implementation from later calculation/save/access/UI work. The accepted plan
  and historical milestone artifacts remain unchanged. Navigation indexes use
  the existing generator.

## Acceptance and proof

| S01 criterion | Actual evidence | Boundary / remaining work |
|---|---|---|
| AC-01 foundation | Strict configuration, allowed three metric IDs, immutable reference preservation, copy/remapping, null/empty distinction, limits, selection/owner checks, complete binding check, Saved View separation and generated parity tests | Registry resolution, historical deleted-ID checks, actual Apply/Save and UI are S02–S04 |
| AC-06 foundation | Strict dual readers/legacy fixture, original snapshot/result bytes unchanged; real PostgreSQL 0011→0012 backfill, old-style insert, immutable creator, safe downgrade/re-upgrade; separate downgrade refusals for report v2, Analytics v2, Saved View and custom calendars | No public report v2 reader/writer is activated; v1 latest upgrade error and actual saved v2 artifacts are S03 |
| AC-11 foundation | Real Identity bootstrap/login/workspace creation and settings API; January→April/October, exact initial-version read, concurrent CAS (one success/one conflict), same-key/body replay after later writes, key mismatch, CSRF/invalid-profile denial, administrator success, analyst denial, other-workspace 404, membership revocation, immutable version UPDATE/DELETE refusal and failed-pointer-write rollback | Fiscal bucket math, report adoption and browser settings are S02–S05 |

The nine real-boundary tests use production routers, Identity authentication,
Semantic service/repository and Alembic against disposable PostgreSQL. No mocked
DB, fake API authentication, skipped required test or route interception is used.
The coordinator's final source check identified PostgreSQL CHECK's UNKNOWN
behavior for a null custom-version request hash. The migration now explicitly
requires `request_hash IS NOT NULL`; a ninth real-DB test verifies rejection and
unchanged default/version count. No second review was dispatched.
The control metadata/legacy fixture is synthetic: it is **not** six-table source
intake/calculation proof. No artifact bytes are rewritten by the migration.
The explicit old/new contract tests do not claim exact v2 report runtime acceptance.

[Validation](validation.md) records exact commands and observed outcomes.
[Owned manifest](owned-files.json) distinguishes implementation from coordinator
preparation and records source bytes before publication. Implementation readiness
has no user-result acceptance requirement for S01; S05's owner checkpoint remains.

## Compatibility and recovery

| Surface / consumer | Classification | Condition |
|---|---|---|
| Existing v1 DTOs/routes/readers and saved payloads | compatible-change | Original strict models and generated bytes retained; additive schema preserves old inserts and original payloads |
| New v2 DTO/port catalogue | compatible-change | Additive opt-in, no public consumers yet; S02/S03 must enforce runtime registry/access/hash checks |
| Workspace calendar settings API/default | compatible-change | Authenticated current-workspace API; initial January behavior, immutable versions, no rewrite of pinned definitions/results |
| Persistence 0012 | compatible-change | Migrate before API use; same-workspace/report constraints and immutable creator; no old-binary/new-v2-data support promise |
| Downgrade after v2/Saved View/custom-calendar writes | breaking-change to old-schema rollback | Explicitly refused; dual reader/forward repair or separately authorized coherent pre-upgrade backup restore |
| Metrics, deployment, browser and source intake | none in S01 | No formulas, deployment, browser implementation or intake semantics changed |

No new service, queue, library, formula, C02/C03 capability or Forecasting work.
No performance, browser, release, backup-restore or production claim.

## Ownership and working state

The coordinator owns the five prompt edits, preparation report/entry-preparation
and draft organization/allowance changes. They are preserved for coordinator
publication. The only executor journal writes use the supported CAS updater:
preflight, actual-session claim and receipt-backed acceptance. No hand-edited
runtime state, foreign claim, plan/hash rewrite or historical receipt mutation.
The original `/Users/daniildegtyarev/Projects/Custometry` was not modified.
No commit, branch, push, PR or merge was performed by this executor.

Repository-prescribed locked Python/API/test dependencies and pnpm dependencies
were materialized locally; no dependency declaration or lockfile changed. The
existing Docker installation was started and an already available PostgreSQL
image was used; no image build or pull. Every proof container/database/anonymous
volume and temporary secret file is task-owned and cleaned by the runner.

## S02 handoff

- Import public types from `packages.contracts.analytics.workspace`,
  `packages.contracts.presentation.workspace` and `packages.contracts.semantic`.
  Semantic calendar port implementation: application/calendar.py and
  infrastructure/calendar.py. Profile hashes cover canonical full profile bytes;
  version identity is separate and workspace-scoped. New report configurations use
  the explicit current pin/fiscal basis; legacy projection uses initial January
  and calendar basis. Preserve these pins in D03 identity and D04 boundaries.
- Migration head is `0012_metric_workspace`; do not renumber earlier revisions.
  S01 fixtures are control/schema proof only. S02 must build its task-owned real
  six-entity source intake/artifact corpus and independent SQL oracle, as specified
  by its prompt. Do not substitute these legacy fixtures for source proof.
- `WorkspaceResultV2` and `CardComparisonV1` are schema foundations, not precomputed
  results. Implement calculation and immutable storage; registry verification,
  access partition identity and exact manifest resolution remain mandatory.
  No failed binding may become saveable; decimal values stay canonical strings.
- Keep new report/Analytics/context/catalog/result v2 routes unmounted until S03
  proves current object/data-access adapters, including direct callers. Only the
  calendar settings routes are mounted in S01. Original v1 routes remain intact.
- The next prompt and its existing source entrypoints have been inspected; this
  report supplies its sole S01-produced entry input. `next_stage_allowed:false`
  remains mandatory: coordinator must inspect evidence, publish via technical
  branch/PR, pass Foundation, squash merge, confirm remote main and branch deletion,
  then perform a fresh supported advance. Never rewrite this report/receipt to add
  publication metadata. S01 does not execute or enable S02.
