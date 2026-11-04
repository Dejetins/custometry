# W39 correction 004 — local report presentation

Status: implemented and locally verified; W39 remains `active` for owner review.
Parent: [ticket](../../../tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md),
[handoff](../handoff.md), [evidence index](README.md).
Source contract: `ARCH-UI-WEB-IMPLEMENTATION-SOURCE-001` version 21.
Requirements: WEB-ARCH-003..006, UI-SHELL-001..003, A11Y-001, I18N-001;
owner correction 004 controls the bounded presentation refinements.

## Changes and causes

1. Configured and legacy card totals show grouped whole units. Configured card
   absolute deltas also show whole units; percentages in card labels/accessibility
   text, tooltip, delta-series axis/value and table show at most one fractional
   digit. Raw results, `data-value`, computation, export and persisted precision
   are unchanged. A visible note explains full values and whole-unit rounding.
   Owner January example: `43908.52` becomes `43,909`, never millions.
2. The metric-catalog disclosure has no border/background frame. Its native
   summary retains keyboard activation and visible focus.
3. `CardRail.tsx` coordinates horizontal pointer dragging without selection.
   One native stretched primary button per card covers value, metadata and blank
   space; checkbox and gear remain sibling controls with independent hit areas.
   Gear uses an independent inspected-card ID. Pointer focus prevents page scroll.
4. Configuration has a restrained pilot surface. Results, including the chart
   toolbar, are visually separate. Cards retain 124 px height, 10 px gaps/radius
   and partial next-card visibility on narrow screens.
5. Removed the effect that called `apply(d)` whenever selection differed from
   applied/stored selection. Cached single-card view changes now update draft and
   chart locally, retain truthful unsaved state and keep controls enabled.
   Explicit Save prepares a changed view with existing result IDs as necessary.
   Actual context changes retain old verified plot data, require Apply, disable
   Save and show the stale-result explanation. ECharts merges stable series in
   the existing instance over 200 ms; reduced motion disables animation.

The first coordinate test found a real defect: the pilot's generic
`button:active { transform: scale(.96) }` changed the stretched pseudo-element's
containing block during pointerdown. Event tracing showed button pointerdown,
value pointerup, then article click. An initial scroll-based hypothesis was
insufficient; disabling only the primary card button's active transform fixed
this observed cause. The final actual-coordinate tests and independent Browser
retest both pass. A later drag test needed a genuinely overflowing viewport;
1480 px supplied only 2 px overflow for six cards. This was corrected to 900 px.

## Proof

- 106 Web tests pass, including numeric presentation precision.
- Three bounded browser scenarios pass against the real local API and production
  preview, with final focused reruns for coordinate/drag and real hover precision.
- Coordinate hits on value/lower metadata/blank space, Enter/Space, independent
  gear/checkbox and nonselecting drag pass. Selection emits zero nonidentity API
  requests. 40 sampled frames remain nonempty, same SVG and not busy; ten distinct
  rendered states demonstrate the update transition. Chart option is 200 ms.
- Real synthetic report fixture 7 is the only saved report in this correction.
  Apply of January context, selection of average receipt without Apply, explicit
  Save and reload preserve selected metric and exact raw server series. Save
  preparation reuses the existing result IDs. A subsequent date change disables
  Save and retains the previous verified series with explicit Apply notice.
- Tooltip and table percentages match one-decimal server values. Whole card
  amounts and deltas match rounding of authoritative full values. Raw table
  attributes preserve fractional average-receipt observations.
- At 400 px the rail overflows; reduced-motion updates retain chart instance with
  animation false/duration zero. Catalog summary border zero and focus visible.
- Screenshots were inspected: separated desktop surfaces, readable values and
  next-card peek on narrow viewport. Independent coordinator Browser on a fresh
  separate owner-report tab confirmed final actual coordinate hits, stable
  unsaved status, independent checkbox and no console errors. Earlier separate
  Browser checks confirmed RU formatting, gear, Enter/Space, catalog and narrow
  horizontal scroll. These observations are attributed, not executor API proof.
- Production build, local grouped gate, generated pilot check and diff whitespace
  check pass. 169 frozen inputs and 23 backend source files are unchanged.

## Changed paths and boundary

Product changes: `ConfiguredWorkspace.tsx`, new `CardRail.tsx`, `CardYearChange.tsx`,
`WorkspaceProjection.tsx`, `workspace-presentation.ts`, `workspace.css`, legacy
`pilot/port-epilogue.js` and generated `pilot/runtime.ts` / `pilot/source-map.json`
under `apps/web/src/features/reports/`. Tests: presentation unit test and
`tests/e2e/report-loading/{correction004.config.ts,owner-correction004.spec.ts}`.
Ticket, parent evidence/handoff, architecture index and source contract are linked
in the same unit. [Identity](identity.json) enumerates exact hashes and build files.

Contract impact: browser presentation `compatible-change`; persisted schema,
API/DTO, result/cache identity, backend and deployment `none`. Display selection
remains persisted and unsaved until explicitly saved. Pair comparison may still
require Apply/Save for authoritative comparison; no client-derived pair values
are invented.

Preview remains `http://localhost:41746`; API/DB and owner ports 41744/58144 were
not restarted or changed. Original owner tab and unsaved draft were not operated
or saved. Earlier corrections and raw evidence remain intact. No new backend,
idle/load/regression campaign, publication, canonical import or MS-004 acceptance.
The current build has targeted local proof, not a new 50-user qualification.
Next safe action: owner review of the current preview.
