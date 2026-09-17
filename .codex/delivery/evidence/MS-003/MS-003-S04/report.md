# MS-003-S04 — real-API report workspace

Milestone: MS-003. Stage: MS-003-S04. Iteration: 1 (resumed after owner scope decision).
Plan: [MS-003 0.2.0](../../../../../docs/architecture/planning/milestones/MS-003/plan.md).
Prompt: [S04](../../../../agents/generated/MS-003/MS-003-S04.md).
Journal: [canonical execution state](../../../ledgers/MS-003.md).
Plan SHA-256: `4a6b1bf2a64a04b74e073bb22e46895795e187be57fe93b6711408069d6e7280`.
Source baseline: `cb4f696dc1dca3bc051debd347810f7d74caa319` plus preserved S03 changes
and the exact S04 file hashes in [validation evidence](validation-evidence.json).
No commit, push, deployment or accepted-bundle modification was performed.

## Result and authority

The bounded ordinary-analyst report workspace is implemented and its source,
real API/database/artifact and host-Vite browser checks pass. Final stage status
and successor permission belong exclusively to the journal and immutable receipt.
The [owner's context-extension decision](owner-context-authorization-20260915.md)
authorized the previously missing first-report discovery boundary; the original
[partial report](attempt-1-report.md) and [checks](attempt-1-validation-evidence.json)
remain preserved. The accepted plan, prompt and prior receipts were not rewritten.

UI-AUTH-001 provides real sign-in using supplied workspace/email/password access
details. UI-RPT-001 creates the supplied template and opens saved owned drafts.
UI-RPT-002 edits title, published source version, dates, Store and prior-year
comparison. Apply computes; Save uses CAS to persist the chosen result. UI-RPT-003
reopens the exact snapshot/page, including after API restart, without computing.
The existing workspace-prefixed routes/history remain intact. A 409 retains
unsaved input and offers reload; history retains local unsaved controls. Session
expiry/revocation hides protected results and clears queries and draft memory;
a generation check rejects late protected responses.

The compiler validates the closed canonical line subset and its identity;
the tree-shakable ECharts 6.1.0 SVG adapter verifies reference hashes and pinned
system defaults. No browser aggregation or localStorage result truth is used.
The chart and full accessible current/prior tables consume the same server series.
Result Trust preserves the item-attribution limitation (14,995 / 15,000 eligible
relationships, five quarantined items), selected-period coverage and the current-only
reference-data caveat. Eligible completed EUR receipt totals remain visible as such.

## Compatibility and changed paths

The [exact manifest](validation-evidence.json) separates created and modified paths
and names shared files. New report feature routes/components/styles, UI theme
variables, RU/EN copy, compiler/adapter, generated report-context DTOs, context unit
and integration tests, slice-owned Playwright fixtures/specs and bilingual help
belong to S04. ECharts 6.1.0 plus its transitive packages are the sole new library.
No product source files were deleted.

Owner-authorized additional zones: Analytics application context projection,
Semantic public discovery port and PostgreSQL adapter, typed analytics API/OpenAPI,
and focused backend tests. The context endpoint discovers only published governed
versions in the actor's workspace and integrity-checked Store labels through the
existing Artifact port. It does not expose raw storage paths, connection secrets,
other workspaces or customer/product directories and does not calculate results.
This is `compatible-change`; no migration, new permission grant, schema rewrite
or bypass was introduced. The generated preview client additionally forwards the
server's existing exact page locator. Cache/identity behavior is fail-closed.

One necessary integration hunk outside the initial listed zones updates API health
`SUPPORTED_HEAD` from `0010_sales_report` to the already accepted S03 migration
`0011_presentation_drafts`. The stale value caused a real readiness 503. This
aligns readiness with the existing schema; it adds no migration or release claim.

Documentation updates cover the current bounded route capability inventory,
Web source contract, analytical-authoring consumer boundary, bilingual report/login
help, required navigation and generated shipped help index. The contributor index
was regenerated and was already byte-current. Mutable documentation is snapshotted
under this stage before receipt binding.

Foreign work preserved: S03 report API/main composition, Presentation application,
domain and persistence, Artifact snapshots, migration 0011, S03 contract/schema
and test files, evidence and prior receipt. Separable mixed files are the analytics
router, contracts index, generated reports client/generator, analytical-authoring
contract and architecture index. Their whole-file hashes identify the integrated
source; only the documented S04 hunks are claimed. MS-001/MS-002 artifacts, pilot
bytes and unrelated routes remain unchanged.

## Verification and criterion coverage

Exact commands, results, source hashes and successor input hashes are in
[validation evidence](validation-evidence.json). All commands ran after repository
toolchain activation. The final focused suites passed: 34 backend unit/contract/
health tests, one isolated real PostgreSQL context integration test, 78 Web tests,
28 compiler tests, two UI-foundation tests and 10 Playwright tests. Web/UI/contracts/
compiler TypeScript and focused Python/Ruff checks passed. The required grouped
`uv run --locked python -m tools.check --scope local`, strict MkDocs build,
generated route/client/docs checks and production Web build passed.

| Requirement | Observed proof |
|---|---|
| AC-02/05 ordinary analyst journey | Actual S01 preparation, fresh real invited analyst; browser login, first template Apply/Save, period/Store/comparison, title, library reopen and exact snapshot |
| AC-05/06 UI and language | RU/EN at 768x1024 and 1920x1080; keyboard Focus open/Escape/close/return, exact Focus link, chart/table, history input retention, 200% layout-zoom reflow |
| AC-05/06 failure truth | Real CAS 409, empty period, temporarily unavailable owned snapshot, actual access expiration and real session revoke; protected tables/metrics removed; invalid page locator fails |
| TECH-06 persistence | Fresh production API process restart followed by exact snapshot reload; browser observes zero new compute POSTs on reopen; S03 provides the stronger source/calculation-disabled persistence evidence |
| TECH-07 chart/identity | Closed-spec/unsafe-field rejection, binding/hash validation, decimal table preservation, calendar-date prior-year alignment, real ECharts SVG, complete server-series table |
| Pilot fidelity | [Normalized source comparison](comparison.md), preserved source hash, wide/narrow screenshots, table/Trust and zoom evidence; scoped omissions stated |

Positive journeys observed no browser console errors/warnings, uncaught page errors
or HTTP failures. Negative flows deliberately produce 409, 401, unavailable/invalid
locator responses; API restart produces transient loopback readiness connection
failures while its process is stopped. These are expected fault evidence, not
positive-journey failures. Node's NO_COLOR/FORCE_COLOR warning is test-runner output.

The Playwright config owns Vite 41734, production API 58104, test-only control 58105
and preserved pilot 8834 on loopback, waits for actual API readiness and does not
reuse foreign servers. No auth stub or route fulfillment certifies the journey.
It replays S01 against the explicitly owned Hybrid source/control PostgreSQL and
artifact root; each suite creates its own ordinary analyst. Fault operations check
that snapshot ownership matches that new analyst. The separate context integration
creates and drops only its own unique test database. Final browser cleanup left
all four owned ports free and removed the transient credential file.

During development, malformed initial test selectors and duplicate titles caused
false failures; selectors were scoped and report titles made unique. An interrupted
uv-wrapped API subprocess was left running; process inspection established the
cause, its exact owned PID was terminated, and the fixture now launches the Python
API child directly, rejects occupied API ports, checks child/readiness and uses
graceful shutdown. Uvicorn re-raises SIGTERM after graceful shutdown; a fixture
handler now unwinds the cleanup block so temporary credentials are removed. The
final complete 10-test run passed with fresh owned servers
and observed cleanup. Earlier failed attempts are not counted as proof. Stale help
index/title/anchor checks were corrected and the final local/docs gates rerun.

## Proof limits, residual risks and successor

This proves a host-Vite browser with production API, owned PostgreSQL and immutable
artifacts, not installed HTTPS/Edge, a complete design system or official release.
200% uses actual-browser CSS layout zoom; native browser-toolbar magnification and
full accessibility certification are not claimed. The browser is Chromium; broader
browser/platform qualification is outside this stage. The Web build passes with
Vite's >500kB chunk warning (report chunk about 559kB / 193kB gzip); no performance
SLO claim is made. Source preparation and test-created reports remain only in the
owned Hybrid environment. Existing development processes outside the test's owned
ports were not restarted or used as acceptance targets.

S05's prompt and all currently declared inputs were read and checked: this report,
the exact accepted plan, existing internal bundle producer, installer and runtime
contract. S04's inputs are produced here. New image/config/bundle identities,
protected HTTPS routes and candidate stop/resume proof remain S05 work. Enabling
its pending row is a handoff only; manual sequential execution stops after S04.
S06 retains actual owner visual/product acceptance. No such acceptance is invented.
