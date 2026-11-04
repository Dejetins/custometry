# W39 owner correction 001

Date: 2026-09-23. Ticket: [W39](../../../tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md).
Source contract: [version 18](../../../../../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md).
Requirements: WEB-ARCH-004/006, WEB-PERF-003/004, A11Y-001, I18N-001.

## Authority and boundary

The owner selected six bounded presentation corrections in the existing local
implementation. The EUR/UTC removal supersedes the former single-header decision.
No API, DB, calculation, units, timezone, session identity or persistence change
is included in this correction. Browser presentation impact: compatible-change;
API/persistence/identity impact: none. One executor, no subagents, publication,
canonical import or MS-004 acceptance. The ticket remains active for owner review.

The existing production preview is http://localhost:41746. Executor tests used
separate synthetic browser contexts at 127.0.0.1:41746 and disposable regression
fixtures at 41741/58141. The owner tab and unsaved six-card draft were not operated
or reloaded. Owner ports 41744/58144 and the existing production-preview API/DB
were not restarted or modified by this correction's application changes.

## Changes and causal evidence

- Report-local visible and accessible EUR/UTC labels were removed from configured
  projections, legacy copy/runtime, headings, tables and tooltip series names.
  Metric names and periods still identify values; backend units remain intact.
- The inspector is portaled into a separate grid column spanning chrome/content.
  Below 1101 px it occupies the content row beneath chrome, opens explicitly and
  makes the covered report content inert. The rail stays fixed; grid animation
  respects reduced motion. Escape restores the opener after inert is removed.
- The gear uses the pilot SVG symbol, a 28×28 px button and accessible name.
  Action buttons match the existing period control: height 28, radius 16, font 10.
- The extra conditional status paragraph caused a 72.375 px vertical jump. A
  fixed status slot and 160 px cards keep layout stable. Focus restoration uses
  preventScroll. ECharts is initialized once per plot mount and updated in place;
  the previous authorized projection stays visible beneath pending feedback.
  That one-entry projection is cleared when trust/authorization is lost.
- Plot height fits the remaining report or Focus viewport and observes resizing.

[Before](before-geometry.json) versus [after](after-geometry.json), 2688×1575:
card selection previously moved cards and plot down 72.375 px at scrollTop 0 and
replaced SVG. It now preserves cards y=302, plot y=522 and scrollTop=0, with the
same SVG node. Large-screen plot height is 1020 px instead of the fixed 360 px.
Inspector x=2330 follows chrome right=2329; neither overlaps the rail/header.
See [large report](after-2688-open.png), [laptop](responsive-1480-inspector.png),
[narrow dock](responsive-768-inspector.png), [400 px](responsive-400-report.png).

## Verification

Commands run after `source scripts/activate-toolchain.sh`:

- `corepack pnpm --filter @custometry/web test`: 87/87 passed.
- `corepack pnpm --filter @custometry/web build`: TypeScript and production build
  passed; existing >500 kB chunk advisory remains.
- `W39_CORRECTION_PHASE=after corepack pnpm exec playwright test --config tests/e2e/report-loading/correction.config.ts`:
  6/6 passed, production preview, widths 2688/1480/768/400. Checks geometry, SVG
  continuity, controls, rail, no EUR/UTC text/accessible labels, Table, Focus,
  Escape/restored focus and Focus height after +100 px viewport resize.
- `corepack pnpm exec playwright test --config tests/e2e/report-loading/regression.config.ts --project 1920`:
  seven passed initially; temporal saved-view comparison required awaiting exact
  loaded values because retained content now stays mounted during loading.
  The unchanged expected decimals/deltas passed with `--grep "reader temporal"`.
  Coverage includes immutable Save/reopen/snapshots, reader permissions, temporal
  and fiscal chart/table parity, late revoked responses and Reload saved races.

The new legacy fixture returns HTTP 200 with `Data unavailable for this source`;
[its observed state](legacy.json) has no EUR/UTC. No graph-ready claim is made
for that no-data fixture. Configured saved report/Focus/Table proof is separate.
Initial responsive failures were a nonserializable test matcher; it was replaced
by measured bounding-box height. A real narrow Escape focus-order defect was
fixed before the passing run. Failed attempts and their causes are summarized in [validation](validation.md).

## Attributed independent Browser observations

Coordinator task `01a0c02d-5267-7601-b735-5b43d11789c0` reported separate in-app
Browser observations against this production preview (not executor screenshots):

- 2688×1575: no EUR/UTC in rendered text or accessibility tree; chrome ends at
  2329 and inspector begins at 2330; cards y=302/h=160 and plot y=522/h=1020 stay
  unchanged after Receipts selection; SVG gear 28×28 and action dimensions match.
- 1480×969: inspector x=1122..1472, chrome right=1121, plot 414 px; Focus 868 px.
- 768×1024: inspector below chrome, header/navigation remain visible.
- 400×850: toolbar wraps, cards scroll within their region, no page overflow seen.
- New-report route has no EUR/UTC in text or aria/title; gear opens Card;
  Escape closes/restores gear; Browser console empty. The owner's original
  six-card unsaved draft/tab was left untouched.

## Evidence reuse and remaining limits

Earlier [W39 handoff](../handoff.md), raw measurements and frozen MS-004 inputs
are preserved. Prior backend and 30-minute idle results remain evidence for the
unchanged backend only. The old frontend p95 timings belong to the earlier
bundle; this correction does not claim a new 50-user latency or heap qualification.
No full backend/idle or diagnostic campaign was repeated. Screenshots and local
checks establish only the observed local presentation and functional boundaries.
Next safe action: owner review of this correction on the existing preview.

## Final source and repository checks

[Source/build identity](identity.json) binds the corrected production bundle to
its source hashes. [All 169 frozen inputs](frozen-input-check.json) and
[23 backend files](backend-source-check.json) match the earlier manifests.
`uv run --locked python -m tools.check --scope local`,
`node apps/web/scripts/generate-pilot.mjs --check`, and `git diff --check` pass.
The local profile is static repository proof, not release/runtime qualification.
Coordinator additionally confirmed that a clean saved-report deliverable Browser
tab is open and the original draft remains preserved.

Narrow regression (768 px): six scenarios passed in the full run and the two
remaining scenarios passed after targeted harness fixes using
`--project 768 --grep "reader pair|workset catalog"`. All eight distinct
functional scenarios therefore passed at each of 1920 and 768 px. The narrow
flow explicitly opens/closes the dock, instead of assuming the former initial
modal overlay. The pair test observes the browser fetch clone because Chromium
occasionally discards the protocol response-body buffer. Assertions on saved
values, reasons, calculations and permissions were retained.
