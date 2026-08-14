---
doc: ui-pilot-candidate-browser-review
program_id: custometry-v2
candidate_id: custometry-v2-pilot-r2
correction_pass: 18
status: awaiting_owner_review
date: 2026-08-11
---

# Pilot candidate V2 browser review

## Correction pass 18 scope and authority

This additive report records local Chromium evidence for the external chart
series panel and contextual navigation rail. It preserves the pass 17 report
below and does not accept the candidate, revise G0, reopen accepted G1, start
G2, change production code, or authorize publication.

The pass 18 matrix used RU and EN at `1920x1080`, `1600x1000`, `1365x768`,
`800x800`, and `390x844`, with Small, Medium, and Large analytical sizes.
Apache ECharts 6.1.0 rendered SVG from the vendored local asset.

## External series panel

- Overview used the right panel with six series; Quarterly Contribution used
  the factorized metric × scenario panel with nine series. Large panel width
  was `276 px`, Medium `240 px`, and Small `220 px` when the plot could retain
  its minimum width.
- At `800x800` and `390x844`, the panel moved below the plot at exactly the
  chart width and used panel-local vertical scrolling. Root horizontal overflow
  stayed at zero.
- An SVG-boundary audit forced the three-series Dynamics view external when end
  labels overlapped or clipped. The safe three-series Segment view kept its
  native legend. External mode rendered no native legend or chart end labels.
- Quarterly groups exposed mixed pressed state and scenario rows named with
  metric, scenario, latest value, and visibility. Actual, Plan, and Historical
  remained visually distinguishable through solid, dashed, and dotted samples.
- Hiding eight of nine series succeeded; hiding the last visible series was
  blocked and announced in the live status. Visibility survived RU/EN,
  period, palette, grouping, rerender, Focus, and right/bottom relocation.
- Chart -> Table -> Chart removed the panel from active layout and restored one
  synchronized panel. Keyboard focus returned to the same series control after
  rerender and relocation.
- Native SVG export composed the plot with the external legend, localized
  visible labels, latest values, and scenario patterns. Hidden series were
  omitted. PNG reused that SVG composition. Existing XLSX and CSV exports
  remained valid.

## Contextual navigation rail

- Closed desktop navigation retained a `62 px` icon rail. Analytics and Data &
  Management both opened at `x=68`, `y=6`, `292 px` wide and `1068 px` high at
  `1920x1080`; switching roots changed content in place and did not resize or
  shift the chart.
- Analytics preserved its complete destination hierarchy. Data & Management
  preserved both nested groups. Same-root activation, outside click, and
  Escape closed the panel; Escape restored focus to the originating root.
- At `390x844` the drawer measured `x=70..382` and `y=8..836`, stayed inside
  the viewport, activated a backdrop, trapped focus, and made the workspace
  inert. Resizing an open desktop panel to `800x800` activated the same modal
  semantics; resizing back cleared them.
- RU/EN locale changes preserved the open shell geometry. With reduced motion,
  transition duration was `0.001 s`. Inspector coexistence preserved stable
  overlay geometry and zero root overflow.
- The final visible-control audit found zero unnamed controls among 74 visible
  buttons, selects, and summaries. Closed navigation had zero interactive
  descendants. Chromium reported zero console errors and zero warnings.

## Correction pass 17 scope and authority (preserved)

This report records browser-visible evidence for correction pass 17 of the
unaccepted revision 2 pilot candidate. It does not accept the candidate, revise
G0 visual authority, reopen the accepted G1 atlas, authorize G2, or update the
normative product blueprints.

The candidate was served from an isolated loopback target and exercised with
`playwright-cli` in Chromium at `2048x1152`, `1920x1080`, `1600x1000`,
`800x800`, and `390x844`. Apache ECharts 6.1.0
loaded from the vendored local asset and rendered SVG. No production data,
external delivery, secrets, browser permission, or deployment was used.

## Shared table geometry

- The visible defect was localized to column geometry rather than row height:
  at `2048x1152`, the Overview semantic stub measured `98.3 px` while the
  Lifecycle stub measured `191.7 px`. Both tables were `1278 px` wide and their
  data rows were already `36 px`, so every period column began at a different
  horizontal coordinate.
- Tables are now grouped by page plus the normalized sequence of every trailing
  header. Each comparable group receives one maximum-content semantic stub,
  one shared table width, and identical value-column tracks through an injected
  `colgroup`. Row content, grouping depth, and one-line versus two-line values
  no longer change the period grid.
- Day, Week, Month, Quarter, and Year were exercised between Overview and
  Lifecycle. Every grain produced `0 px` maximum left-edge difference and
  `0 px` maximum width difference for every corresponding column. Monthly
  desktop geometry resolved to `192 + 12 × 90.5 px` inside the `1278 px`
  analytical surface.
- The same generic mechanism aligned the Segment chart table and Segment
  Profiles table across all eight columns with `0 px` left-edge and width
  differences. English month headers also produced a shared signature and
  zero differences.
- Small, Medium, and Large preserved identical peer-table row heights and
  column tracks; no rich Lifecycle cell had vertical content clipping in the
  tested state.
- At `390x844`, both monthly tables resolved to `168 + 12 × 96 px`, both
  wrappers had `1320 px` scroll width, and root overflow remained zero. At
  `800x800` both constrained wrappers exposed the same `960 px` table grid.
  Opening the desktop inspector likewise gave both tables the same constrained
  grid and table-owned overflow; closing it restored the shared `1278 px` grid.

## Mode-aware report exports

- Every reportable block now exposes export through the same download icon.
  Overview, Dynamics, Quarterly Contribution, and Segments automatically
  switched their one export menu from `PNG / SVG` in Chart mode to
  `Excel .xlsx / CSV .csv` in Table mode. Switching back restored the image
  formats without a stale or mixed menu.
- Lifecycle, Segment Profiles, Segment Migration, and the shared Focus table
  exposed `XLSX / CSV` directly. The shared Focus chart exposed `PNG / SVG`.
  The tab-by-tab DOM audit covered all eight table scopes and five chart
  surfaces; every visible export summary used `#i-download`.
- The generated XLSX uses a native OOXML workbook package. A real browser
  download was identified as `Microsoft Excel 2007+`; `[Content_Types].xml`,
  workbook relationships, workbook, and worksheet all passed `unzip -t`.
- Real browser downloads were also verified as a `1808x1880` RGBA PNG, native
  SVG, and CSV text. The Lifecycle CSV retained group and row hierarchy plus
  the twelve month columns.
- Export menus close on outside pointer press and Escape. Escape restored
  focus to the triggering summary. Labels and titles track the current view,
  including `Скачать график`, `Скачать таблицу`, and format-specific accessible
  names.

## Top-right report inspector

- The former mid-edge handle was removed. One `34x34 px` rounded slider control
  now sits in the trailing top-right header actions, uses the dedicated
  `#i-inspector-toggle` symbol, and exposes synchronized `aria-expanded`, title,
  and open/close accessible names.
- On desktop the open inspector remains a trailing reflow pane but now has an
  `18 px` radius, inset spacing, and a contained surface shadow. The toggle has
  a `12 px` radius and visible hover, active, open, keyboard-focus states.
- Escape closed the inspector, set `aria-hidden="true"`, and restored focus to
  the top-right toggle. At `390x844`, the inspector became a fixed right overlay
  from `x=22` to `x=382`, remained fully inside the viewport, retained its
  `18 px` radius, and produced zero root horizontal overflow.

## Focus typography, table rhythm, and bounded surfaces

- The report-wide analytical-size state is now inherited from `body`, not only
  from the ordinary workspace. A Lifecycle table opened directly in shared
  Focus under Large resolved to `13 px` table text, `15 px` primary values,
  `42 px` data and group rows, and `38 px` header rows.
- The same Large measurements were observed in both Overview tables and all
  three Segment table panels. Medium resolved to `10 px / 36 px / 34 px` and
  Small to `9 px / 32 px / 30 px` for table text, data rows, and headers.
  Group rows share the data-row height for the selected preset.
- The selected S/M/L choice now renders as a complete pressed pill with a
  `4 px` accent marker. Hovering the selected Large choice changed its whole
  background to `rgb(72, 73, 80)` and exposed both tooltip and accessible name
  `Выбрано: Крупный размер (L)`.
- Every ordinary direct report panel is now a centered, separated analytical
  surface with `1 px` border, `12 px` radius, and a maximum width of `1280 px`.
  At `1920 px`, Overview, Dynamics, and Segment panels all measured exactly
  `1280 px`; both Overview panels shared identical geometry and surface color.
- Dynamics reserves a readable right gutter for line end labels. All nine
  actual, plan, and 2024 labels across the three channel facets remained inside
  the chart rectangle at Large; root horizontal overflow remained zero.

## Analytical appearance and control grouping

- Palette and analytical text size share one report-level Appearance popover.
  One compact S/M/L choice now updates primary values, data labels,
  axes/legend, KPI values, and every analytical table together without scaling
  the interface.
- Under Large, Segment labels resolved to `15-16 px`, both Segment tables
  resolved to the same `13 px`, and KPI values resolved to `22 px`.
- Period/comparison/stores, filters/grouping, and appearance/view are rendered
  as three borderless rounded clusters. The cluster computed with `0 px`
  border and `none` box-shadow; hovering Period changed only that command from
  the group background `rgb(29, 30, 33)` to `rgb(48, 49, 54)`. Keyboard focus
  visibility remains intact.
- Palette is no longer duplicated in each analytical block. Block menus retain
  local period, comparison, and inherit-or-disable grouping controls.

## Ordered, extensible grouping

- Report grouping is an ordered list rather than a single enum. The tested
  catalog includes Channel, Store, Segment, Product category, City, and Loyalty
  tier. Items can be added, removed, moved up, and moved down with named buttons.
- The first dimension defines sections and following dimensions refine the row
  hierarchy. `Store -> Segment` rendered Central, North, and Online once as
  section rows, with the five segment rows inside every section.
- Personal analysis state and snapshot-link state include the complete ordered
  dimension list. Legacy single-value fixture state is migrated to the ordered
  representation.

## Aligned period comparison

- Dynamics Year no longer produces isolated annual points. It renders January
  through December for `2025 actual`, `Plan 2025`, and `2024`, aligned by month.
  Retail, E-commerce, and Marketplaces facets all show complete lines and named
  end values.
- The quarterly contribution view now uses Q1-Q4 within the selected year
  instead of treating comparison years as unrelated categories.
- Lifecycle Selected Base now selects a comparison period (`Plan 2025` or
  `2024`), not one month cell. With 2024 selected, every 2025 month compares to
  its matching 2024 month. The visible subtitle states
  `2025 · факт ↔ 2024 · месяц к соответствующему месяцу`.
- Previous Period remains a separate mode and still compares adjacent closed
  buckets. Values/Percent, denominator, comparison mode, and delta display
  remain independent axes.

## Shared facet normalization and stack isolation

- Grouped charts now calculate one explicit value-axis range from every
  visible channel and comparison series. Quarterly contribution resolved to
  `0..30K` for Retail, E-commerce, and Marketplaces; Segment size resolved to
  `0..60K` across all three facets.
- Every grouped stacked series receives a facet-specific stack identity. The
  nine quarterly stacks are unique across three periods and three channels, so
  every channel starts at zero instead of continuing the preceding channel's
  accumulated stack.
- Actual, Plan 2025, and 2024 quarterly stacks all render retained, new, and
  reactivated labels. Small top-segment labels sit above their stack while
  larger labels remain inside.

## Chart visibility and analytical text

- Segment charts render compact labels for actual, plan, and 2024 on every
  segment in every channel facet. Examples observed include `20,2K`, `20,7K`,
  and `18,6K`; exact integers remain in tooltips and tables.
- Overview and Dynamics end labels use a reserved right gutter and overlap
  shifting. Monthly axes use reduced label density on narrow screens.
- Large horizontal Segment charts increase facet height and bar-group spacing
  together with the label size. A bounding-box audit of 60 large data labels
  found zero intersections with a `3 px` safety margin.
- The 100% composition and heatmap modes show data labels outside Focus; bar,
  line, stacked contribution, and segment labels respond to the report-level
  value-size preset.
- KPI customer frequency is shown as `5,8` with `2025` metadata. The redundant
  `за период` copy was removed.

## Table geometry and contrast

- At `1600x1000`, the twelve Overview numeric columns each measured `102 px`.
  Lifecycle numeric columns measured `93.9-94.0 px`; both spreads were at most
  `0.1 px`.
- Lifecycle used its available width with `scrollWidth == clientWidth == 1326`.
  It no longer has a separate horizontal or vertical scroll surface on a wide
  screen. Narrow screens retain table-owned horizontal scrolling.
- Overview, Lifecycle, and Segment table values all resolved to
  `rgb(201, 203, 208)`. Group headers and semantic positive/negative deltas keep
  their distinct roles.
- Channels and stores occur once as section headers rather than repeating in
  every leaf row. Periods remain columns for Day, Week, Month, Quarter, and Year.

## Dismissal, accessibility, and responsive smoke

- Report popovers, block `details`, and export menus close on outside pointer
  press, another command, or Escape. Native popover state and `aria-expanded`
  stay synchronized.
- Opening and dismissing a top popover left `workspace.scrollLeft == 0`; the
  workspace is no longer accidentally horizontally scrolled by focused top-layer
  controls.
- The visible-control audit covered 74 buttons, selects, and summaries and found
  zero unnamed controls. Ordered-group actions expose specific accessible names.
- At `390x844`, root and report horizontal overflow were both zero. The Appearance
  popover remained inside the viewport, and the small-multiple x-axis reduced
  month-label density.
- Final Chromium output contained zero console errors and zero warnings.

## Captures

- `screenshots/pass18/six-series-right-panel-large-1600x1000.png` — six
  synchronized series with latest values in the Large right panel.
- `screenshots/pass18/factorized-metric-scenario-panel-large-1600x1000.png` —
  nine quarterly series factorized by metric and scenario.
- `screenshots/pass18/narrow-lower-series-panel-390x844.png` — lower panel with
  panel-owned scrolling and zero root overflow.
- `screenshots/pass18/focus-right-series-panel-large-1920x1080.png` — shared
  Focus using the same source visibility state.
- `screenshots/pass18/compact-rail-closed-1920x1080.png` — persistent closed
  icon rail and stable report workspace.
- `screenshots/pass18/analytics-context-panel-expanded-1920x1080.png` —
  Analytics contextual destination list over the workspace.
- `screenshots/pass18/data-management-stable-shell-1920x1080.png` — section
  swap inside the unchanged contextual shell.
- `screenshots/pass18/narrow-context-drawer-390x844.png` — viewport-contained
  narrow navigation drawer.
- `screenshots/pass18/navigation-inspector-coexistence-1600x1000.png` —
  navigation and report inspector coexistence.
- `screenshots/pass18/data-management-expanded-hierarchy-1920x1080.png` — both
  nested Data & Management groups expanded in the stable shell.

- `screenshots/pass17/aligned-shared-period-grid-2048x1152.png` — the shared
  monthly grid continuing unchanged from single-line Overview values into
  two-line Lifecycle values with different grouping depth.

- `screenshots/pass16/export-table-xlsx-csv-1600x1000.png` — the Overview
  table selected with the download menu offering Excel `.xlsx` and CSV `.csv`.
- `screenshots/pass16/inspector-top-right-rounded-1600x1000.png` — the rounded
  top-right inspector toggle and inset trailing desktop inspector surface.
- `screenshots/pass16/inspector-mobile-rounded-390x844.png` — the rounded,
  viewport-contained narrow inspector overlay.

- `screenshots/pass15/focus-table-large-1920x1080.png` — Focus table inheriting
  Large typography and standardized row heights.
- `screenshots/pass15/overview-tables-large-1920x1080.png` — both bounded
  Overview table surfaces with identical Large geometry.
- `screenshots/pass15/dynamics-bounded-large-1920x1080.png` — centered Dynamics
  surface with complete end labels inside the chart gutter.
- `screenshots/pass15/appearance-selected-hover-large-1920x1080.png` — selected
  Large state with full-pill hover and accent marker.
- `screenshots/pass15/segments-tables-large-1920x1080.png` — synchronized Large
  Segment tables.
- `screenshots/pass15/segments-table-large-390x844.png` — bounded narrow table
  panels with table-owned scrolling and no root overflow.

- `screenshots/pass14/toolbar-hover-borderless-1600.png` — borderless rounded
  command groups with the Period hover state.
- `screenshots/pass14/appearance-palette-sml-1600.png` — palette and the single
  compact S/M/L control in one plane.
- `screenshots/pass14/quarter-shared-scale-all-labels-1600.png` — common 30K
  axes, zero-based isolated stacks, and labels for all three periods.
- `screenshots/pass14/segments-large-adaptive-spacing-1600.png` — Large labels,
  adaptive bar spacing, and a common 60K axis.
- `screenshots/pass14/mobile-appearance-sml-390.png` — narrow Appearance plane
  without root overflow.

## Proof boundary and residual risk

This evidence proves the listed local fixture behavior in Chromium. Values,
bucketing, denominators, comparison deltas, arbitrary-dimension query planning,
and saved-view persistence are interaction fixtures, not production analytical
execution. It does not prove production routes, unique-customer computation,
backend grouping support, authorization filtering, persisted saved views,
concurrent edits, deployment, assistive-technology compatibility, full WCAG
conformance, or owner acceptance. The candidate remains
`awaiting_owner_review`.
