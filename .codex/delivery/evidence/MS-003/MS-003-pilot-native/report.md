# Native pilot document connected to real report APIs

Owner instruction, 2026-09-16: use the pilot itself, connect real APIs, preserve
its interface elements; internal UI architecture may change. This explicitly
supersedes both earlier reconstructed report implementations. It does not extend
the receipt-total API into customer analytics or authorize S05/S06 execution.

## Authority and implementation boundary

The accepted [MS-003 plan](../../../../../docs/architecture/planning/milestones/MS-003/plan.md)
and terminal S04 journal/receipt remain historical and unchanged by this repair.
The stage updater supports no terminal-stage reopen. This work is the owner's
explicit source correction, not a rerun, replacement receipt or fabricated owner
acceptance. [Earlier correction](../MS-003-S04-correction/report.md) is not current
fidelity proof. The live [Web source contract](../../../../../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md)
and [architecture index](../../../../../docs/architecture/README.md) point here.

The source is `docs/architecture/ui/target-pilot/ru/source.html`, SHA-256
`b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700`.
`apps/web/scripts/generate-pilot.mjs` takes that complete document, removing
executable script tags only. CSS, SVG symbols, HTML elements and their hierarchy
are retained. A test compares the entire generated document to this exact
transformation, not a separately authored screenshot or replacement layout.

The report route no longer renders the reconstructed JSX report. `PilotDocument`
hosts the source document in an isolated same-origin document with its own
selectors, CSS roots, native popovers and focus scope. React owns routes, actor,
TanStack Query results and drafts; typed model/action ports connect the original
source runtime. Business data, persistence and unsupported fixture renderers are
explicit seams recorded in `pilot/source-map.json` and `seams.json`. Fixture
numbers are cleared from generated data declarations. Original browser storage
is replaced with ephemeral presentation preferences and cannot store API truth.
No scripts, HTML or ECharts callback/options are accepted from server data.

The canonical compiler receives validated S03 references and immutable daily
series. The pilot's original chart-base, palette, readability and adaptive-legend
functions apply their presentation to that series. All real table values are
escaped; no business totals or aggregation are calculated in the browser.
Calendar selections are translated to dates, including ISO weeks/leap years.

## Visible result and limitations

The original rail/context-navigation hierarchy, report tabs, eight KPI positions,
chart panel, second table panel, toolbar menus, inspector, palettes, analytical
size controls and full Focus surface are present. Three supported receipt values
are populated; unavailable customer metrics show a dash. Data labels truthfully
identify receipt sales, EUR, UTC and the applied result period. Unsupported
segmentation, KPI persistence, publication/export and arbitrary authoring do not
claim backend success. Original grouping controls remain visible; unsupported
breakdowns are unavailable. The supplied canonical result has no channel/segment
groups; its chart contains the real daily receipt series.

The original heading edits the title. Original period/store/comparison widgets
control Apply; changing their draft does not calculate or replace a saved result.
The original Save view action persists through CAS. The existing saved-view row
opens exact immutable preview. Trust keeps the actual 14,995/15,000 relationship
accounting, five quarantined rows and selected coverage. Authorization denial
unmounts the whole protected document and clears protected queries. Preview can
open a saved store result even when current discovery labels are unavailable.

Login/library are not demonstrated as full screens by this pilot and retain the
previous bounded implementations. This is not a claim that every pilot capability
has a production backend, or that different data produces identical chart pixels.
No copied customer demo data is presented as a real analytical result.

## Owned paths and exclusions

Changed: `apps/web/src/features/reports/ReportWorkspace.tsx`; new `PilotDocument.tsx`,
`pilot-period.ts`, `pilot-native.test.ts`, `pilot/{document.html,runtime.ts,
port-prelude.js,port-epilogue.js,seams.json,source-map.json}`; generator under
`apps/web/scripts/`; `tests/e2e/ms-003-pilot-native/`; affected Web/analytical
contracts, architecture index and bilingual report help; this evidence directory.
No backend/schema/dependency changes, pilot-byte edits, historical evidence
rewrites, commits, publication or deployment were performed. Existing S03/S04
backend, contract and ledger modifications in this shared checkout are excluded.

Contract impact: compatible browser presentation replacement for the supplied
receipt report. API/session, persisted composition/spec/default references,
metric/result identity, artifact hashes and permissions remain unchanged. The
UI now truthfully exposes the pilot's unsupported elements as unavailable rather
than supplying demo results or a substitute layout.

## Proof

The slice-owned Playwright config starts host Vite 41734, the actual production
API 58104 with S01 preparation, owned PostgreSQL/artifacts, bounded fault-control
58105 and preserved source server 8834. Fresh ordinary analyst accounts are used.
No positive route/auth fulfillment is mocked. Browser runs compare the live source
CSS/SVG and shared geometry at 1920x1080 and 768x1024, in RU/EN. They exercise real
create/title/Apply/Save, original period/store/comparison menus, full table,
Trust, keyboard Focus/Escape/restore, exact reopen and 200% zoom smoke. Negative
journeys cover retained CAS input, reload, API restart, storage failure, empty
period and revoked session. Final command outcomes are bound in verification.json.

Source generation checking, Web types/build/unit tests, calendar boundary tests,
strict public documentation build and repository local gates accompany browser
proof. Earlier failed runs exposed a selected-store preview label lookup and
narrow inspector closure and squeezed daily table columns; these were fixed before final validation. The source shared-table geometry now applies to a single real table as well, using its existing horizontal scrolling and 96px value columns. This is an explicit data-volume seam; source CSS remains unchanged. This report
claims no installed HTTPS bundle, full accessibility certification, S05 result,
or owner visual acceptance. Build chunk size is a recorded advisory while the
unmodified source and its presentation runtime are carried together.

## Validation results

- `node scripts/generate-pilot.mjs --check` (from `apps/web`): pass; pinned source and generated document/runtime agree.
- `pnpm build` and `pnpm test` (from `apps/web`): pass; TypeScript/Vite and 81 tests in 19 files. Vite reports a chunk-size advisory.
- `corepack pnpm exec playwright test --config tests/e2e/ms-003-pilot-native/playwright.config.ts --max-failures=1`: final result recorded in `verification.json`; six real API browser journeys. Expected temporary connection refusal during the deliberate API restart is scoped to the fixture health probe.
- `uv run --locked mkdocs build --strict`: pass.
- `uv run --locked python -m tools.check --scope local`: final result recorded in `verification.json`.
- Existing owner Hybrid site: ordinary analyst login, saved report **Продажи по чекам**, actual table/chart and zero observed page errors. Screenshot: `browser/live-1920-ru.png`.

The existing source snapshot is HEAD `cb4f696dc1dca3bc051debd347810f7d74caa319` plus the working files hashed in `verification.json`. Screenshot and documentation snapshots are hashed there. Browser proof uses its own prepared database/artifacts; the owner screenshot uses the existing owner Hybrid database/artifacts and is a separate smoke boundary. S05/S06 remain outside this repair.
