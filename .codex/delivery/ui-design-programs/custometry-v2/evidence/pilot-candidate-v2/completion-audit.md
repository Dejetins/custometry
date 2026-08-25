---
doc: ui-pilot-candidate-completion-audit
program_id: custometry-v2
candidate_id: custometry-v2-pilot-r2
correction_pass: 18
status: awaiting_owner_review
date: 2026-08-11
---

# Pilot candidate V2 completion audit

## Correction pass 18 authority boundary

This additive audit records the external chart-series panel and contextual
navigation rail requested for correction pass 18. It preserves the pass 17
evidence below, does not accept the candidate, does not revise G0 or accepted
G1 receipts, and does not start or claim G2.

## Correction pass 18 completion evidence

- Source hash: `d5639f0e20a79581972853979cd643ca456b6235c1ce098f5adc98d89636ca15`.
- Charts with six or nine visible series use one external sibling panel. At
  `1600x1000`, Large used a `276 px` right panel while preserving a readable
  plot. At `800x800` and `390x844`, the same panel moved below the chart and
  owned its vertical scrolling; root horizontal overflow remained zero.
- Three-series Dynamics became external only when measured SVG end labels
  would collide or clip. A safe three-series Segment chart retained its native
  legend. Native legends are disabled whenever the external panel is active.
- The quarterly nine-series view is factorized into metric groups and
  Actual/Plan/Historical scenario rows. Latest values and line-pattern swatches
  remain visible in RU and EN. Individual and group pressed states update the
  ECharts instance and never permit a zero-visible-series state.
- Series visibility survived period, palette, grouping, locale, rerender, and
  right-to-bottom relocation. Source and Focus shared the same visibility
  state, and Chart -> Table -> Chart restored one panel without stale copies.
- SVG and PNG exports use the same composed export SVG and visible-series
  selection; a hidden series was absent from the downloaded SVG. XLSX and CSV
  table exports remained valid and unchanged.
- The permanent shell is a compact `62 px` icon rail. Context panels overlay
  the workspace at a stable `292 px` desktop width, switch section content in
  place, and leave chart geometry unchanged. The narrow drawer remains inside
  the viewport and activates backdrop plus `workspace.inert`.
- Same-root toggling, outside click, destination selection on narrow Web, and
  Escape close the navigation. Escape restores trigger focus. Resizing an open
  flyout across the `820 px` breakpoint adds and removes modal semantics
  correctly. Reduced-motion transitions resolve to `0.001 s`.
- The visible-control audit found zero unnamed controls among 74 controls and
  no interactive descendants inside the closed navigation panel. Chromium
  reported zero console errors and zero warnings at the tested states.

## Correction pass 17 authority boundary (preserved)

This audit closes correction pass 17 for the unaccepted revision 2 candidate.
It does not accept the candidate, revise the G0 visual-authority decision,
recalculate accepted G1 bindings or receipts, start G2, or alter normative
product documentation. The accepted G1 atlas remains unchanged.

## Current owner-correction coverage

| Owner correction | Candidate evidence | Result |
| --- | --- | --- |
| Make values and charts readable and make Large visibly larger | Segment labels change from 11 px to 16 px; default axes, legends, table headings, Lifecycle deltas, and chart labels were increased | Addressed |
| Use equal table column widths | Overview spread is 0 px; Lifecycle spread is 0.1 px across twelve numeric columns | Addressed |
| Show every value on Segments | Actual, Plan, and 2024 compact labels render for every segment in all channel facets | Addressed |
| Put palette and font sizes in one settings plane | One report Appearance popover contains data palette plus one compact S/M/L analytical-size choice | Addressed |
| Use one size setting for every chart and table | S/M/L synchronizes values, labels, axes/legend, KPI values, and every analytical table | Addressed |
| Group controls visually like a native toolbar | Three borderless rounded clusters expose hover/active feedback on the individual command | Addressed |
| Use consistent, more rounded corners | Tabs, context chips, segmented controls, and block commands all resolve to 16 px | Addressed |
| Avoid separate scrolling between the two Overview tables | Lifecycle uses full available width and has zero wide-screen overflow; vertical max-height was removed | Addressed |
| Remove `за период` from frequency KPI | KPI value is `5,8`; metadata is `2025` | Addressed |
| Compare period to aligned period | Year mode renders Jan-Dec 2025 against Jan-Dec 2024; Lifecycle base mode aligns matching months | Addressed |
| Support flexible combinations and order of groupings | Ordered dimension list supports add/remove/reorder; Store -> Segment was exercised | Addressed |
| Unify table value contrast | Overview, Lifecycle, and Segment values all resolve to rgb(201, 203, 208) | Addressed |
| Normalize grouped charts | Quarterly and Segment facets use explicit shared bounds; each facet stack starts at zero | Addressed |
| Show quarterly values for every compared year | Actual, Plan 2025, and 2024 render labels for every retained/new/reactivated stack | Addressed |
| Prevent Large Segment labels from colliding | Facet height and bar spacing grow with the selected size; 60 labels had zero intersections at a 3 px margin | Addressed |
| Preserve Day, Week, Month, Quarter, and Year | All five grains remain available in report and local block controls | Preserved |
| Preserve independent Values/Percent, denominator, comparison, and delta axes | Lifecycle controls and personal-view state retain all independent axes | Preserved |
| Apply analytical font size inside Focus tables | Shared Focus inherits the report-level S/M/L state; Large resolves to 13 px table text and 15 px primary values | Addressed |
| Make the selected size unmistakable, including hover | The whole selected S/M/L pill is pressed, carries a 4 px accent marker, changes background on hover, and exposes selected-state tooltip and accessible name | Addressed |
| Synchronize vertical table geometry | Overview, Lifecycle, and all Segment tables use the same preset-specific data, group, and header row heights | Addressed |
| Separate and bound ordinary chart/table areas | Direct analytical panels have a common 12 px bounded surface and center at a maximum width of 1280 px; chart end labels have reserved gutters | Addressed |
| Use the download icon for chart and table exports | Every chart/table export summary uses the shared download symbol | Addressed |
| Switch export formats with the selected representation | Chart mode exposes PNG/SVG; Table mode exposes XLSX/CSV on Overview, Dynamics, Quarterly Contribution, and Segments | Addressed |
| Provide XLSX and CSV for every table | Overview, Dynamics, Quarterly Contribution, Segments, Lifecycle, Segment Profiles, Migration, and Focus all expose XLSX/CSV | Addressed |
| Move the inspector opener to the top right like Codex | The mid-edge handle is removed; one rounded slider control opens the rounded trailing inspector from the header | Addressed |
| Align period columns across tables with different row content | Comparable tables are grouped by their trailing header sequence and receive one shared semantic-stub width plus identical value-column tracks | Addressed |
| Keep alignment for every supported period | Day, Week, Month, Quarter, and Year all produced zero corresponding-column coordinate and width differences | Addressed |
| Preserve alignment across content, locale, and S/M/L | Overview/Lifecycle and both Segment tables align with different grouping depth, one-line/two-line values, RU/EN labels, and every analytical size | Addressed |

## Completion evidence

- Source hash: `584792b3da548b3d9cba9eee681188cf432ad1e656a5e97b32ae0981f4405a88`.
- The original reproduction measured a `98.3 px` Overview stub and a
  `191.7 px` Lifecycle stub inside equally wide `1278 px` tables. After the
  repair, both monthly stubs measured `192 px` and all twelve value columns
  measured `90.5 px` with `0 px` left-edge and width differences.
- Day, Week, Month, Quarter, and Year all produced `0 px` maximum corresponding
  column differences. The Segment table pair and English month labels produced
  the same result.
- Small, Medium, and Large kept peer data-row heights equal and reported zero
  vertically clipped rich Lifecycle cells in the tested state.
- At `390x844`, both tables measured `1320 px` as `168 + 12 × 96 px` inside
  `305 px` table-owned scroll areas; root overflow was zero. At `800x800` both
  wrappers exposed the same `960 px` grid. Inspector reflow preserved identical
  tracks and symmetric table-owned overflow.
- The adaptive export audit covered Overview, Dynamics, Quarterly Contribution,
  and Segments. Each switched from `PNG / SVG` to `XLSX / CSV` with the
  Chart/Table control and switched back without stale options.
- Standalone Lifecycle, Segment Profiles, Migration, and Focus tables exposed
  `XLSX / CSV`; the Focus chart exposed `PNG / SVG`. All export summaries used
  the download icon and all format buttons had format-specific accessible names.
- A downloaded Overview XLSX was identified as `Microsoft Excel 2007+`; all
  five required OOXML package entries passed `unzip -t`. Downloaded PNG, SVG,
  and Lifecycle CSV files were identified as their declared formats.
- The inspector toggle measured `34x34 px` with a `12 px` radius. The open
  desktop drawer used an `18 px` radius; Escape closed it and restored toggle
  focus. At `390x844`, the fixed drawer occupied `x=22..382`, remained within
  the viewport, and produced zero root horizontal overflow.
- In shared Focus, Large produced `13 px` table text, `15 px` primary
  values, `42 px` data/group rows, and `38 px` headers. The corresponding
  ordinary Overview and Segment tables produced the same measurements.
- Small, Medium, and Large table presets were exercised as
  `9 px / 32 px / 30 px`, `10 px / 36 px / 34 px`, and
  `13 px / 42 px / 38 px` for table text, data rows, and headers.
- At `1920x1080`, both Overview panels and every Dynamics and Segment panel
  measured `1280 px`, with a `1 px` boundary and `12 px` radius. Both Overview
  panels had the same surface color and geometry.
- All nine Dynamics line end labels remained inside the chart rectangle under
  Large. The widest observed right edge was below the chart's protected edge.
- Dynamics Year rendered twelve aligned categories, with complete current,
  plan, and 2024 arrays rather than isolated annual points.
- Lifecycle Selected Base exposed `Plan · 2025` and `2024`. With 2024 active,
  the first row produced distinct aligned monthly deltas (`+12.0%`, `+11.7%`,
  `+11.5%`, `+11.2%`) instead of reusing one month as the base for every cell.
- `Store -> Segment` rendered three store section rows and five segment leaf
  rows per store; store names did not repeat in leaf rows.
- Overview numeric widths were twelve times `102 px`. Lifecycle widths were
  eleven times `93.9 px` and once `94.0 px`; the Lifecycle wrapper had zero
  overflow at `1600x1000`.
- Table value color matched across Overview, Lifecycle, and Segment surfaces.
- The single Large choice set all four analytical readability datasets to
  `large`; Segment labels resolved to `15-16 px`, both Segment tables to
  `13 px`, and KPI values to `22 px`.
- Quarterly facets shared `max == 30000`, Segment facets shared
  `max == 60000`, and the nine quarterly period/channel stacks had unique
  stack identities.
- A 60-label Large Segment bounding-box audit found zero intersections with a
  `3 px` minimum safety margin.
- Primary analytical controls resolved to the same `16 px` radius. Command
  clusters had `0 px` border and no box shadow; Period hover changed only its
  command background to `rgb(48, 49, 54)`.
- Opening and dismissing report and block menus left zero open contextual
  details and `workspace.scrollLeft == 0`.
- The final visible-control audit found zero unnamed controls among 74 visible
  buttons, selects, and summaries.
- `1920x1080` and `390x844` had zero root horizontal overflow. Chromium
  reported zero console errors and zero warnings.

## Preserved behavior

- Linear Graphite shell, complete Analytics navigation, Apache ECharts SVG,
  chart/table alternatives, KPI customization, filters, store scope, snapshot
  preview, shared Focus, inspector, report style templates, author metadata,
  and fixture-only email preflight remain intact.
- Accepted G1 coverage and receipts remain untouched. G2 remains unclaimed.
- No production email, external data access, publication, deployment, commit,
  push, or PR was performed.

## Contract and residual risk

The candidate remains a browser-visible, compatible additive revision while it
is unaccepted. No production API, DTO, port, persisted schema, external side
effect, or deployed runtime changed.

Future runtime adoption must include ordered grouping dimensions, period grain
and value, aligned comparison-period identity, block-local period and grouping,
value format, percent denominator, comparison mode and base, delta display,
report palette/readability settings, and saved-view identity in the appropriate
request, query, render/cache, export, snapshot, and persistence contracts. This
audit does not authorize or implement those contracts.

## Readiness verdict

Correction pass 18 is ready for owner visual review. Candidate status is
`awaiting_owner_review`. G1 is unchanged and G2 has not been started or claimed.
