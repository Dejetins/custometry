---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.11.0-draft
ticket_id: W42-COMPOSER-INTEGRATED-CANVAS
proof_boundary: local-platform-with-real-api-and-disposable-test-databases
proof_skills: [better-layout, better-ui, contract-impact-analysis, browser-qa-evidence]
verdict: passed
redaction: Synthetic retail data only; no credentials, tokens or browser storage captured.
executed_checks:
  - Focused Python contract/service tests (61 passed)
  - Focused frontend tests (31 passed)
  - pnpm --filter @custometry/web build
  - uv run --no-sync python -m tools.check --scope local
  - git diff --check
  - Real API browser create, calculate, filter, save and reload
observations:
  - Four block types persisted and restored through the platform API.
  - Local store filter changed only its linked chart; unlinked table retained totals.
  - Width preset and Undo restored the expected canvas geometry.
---

# W42 integration evidence

[Ticket](../../tickets/W42-COMPOSER-INTEGRATED-CANVAS.md) ·
[Contract](../../../../docs/contracts/analytical-authoring-contract.md) ·
[UI inventory](../../../../custometry-ui-blueprint-ru.md)

## Outcome and scope

The existing platform editor now uses the owner-selected 24-column block canvas,
shared inspector, add palette, text and explicitly linked local store controls.
Analytical blocks retain real providers/calculation, server snapshot persistence,
undo/redo, scoped locks and authorization. The standalone prototype is unchanged.
Requirements: ANALYTICAL-DOC-002/004/006/014, DASHBOARD-006.

## Commands and observations

- `uv run --no-sync --package custometry-api pytest tests/contract/presentation/test_composer.py tests/contract/presentation/test_composer_structure.py tests/contract/presentation/test_composer_canvas.py tests/unit/presentation/test_composer_service.py -q`: 61 passed.
- `pnpm --filter @custometry/web exec vitest run src/features/reports/composer-canvas.test.ts src/features/reports/composer-state.test.ts src/features/reports/composer-structure.test.ts src/features/reports/composer-temporal-editor.test.tsx src/features/reports/composer-page-navigation.test.tsx`: 31 passed.
- `pnpm --filter @custometry/web build`: TypeScript and Vite passed; large-chunk warning remains.
- In-app browser against Vite 41748 / real API 58148 with disposable Postgres/source artifacts: created analytical chart, calculated, added text and store control, duplicated analytical block as table, linked only chart, selected Store 1, recalculated, saved and reloaded four blocks. Chart January value 2611.6; unlinked table January value 43908.52.
- Full-width preset: block and canvas 1418 px; Undo restored 706 px. Saved again.
- At 768 px, closing inspector restored a visible 651 px canvas; temporary viewport override reset.
- Saved preview showed read-only content and disabled control, without manipulation handles. Returned to editor. No browser console errors observed.
- Independent contract/security review found store-ceiling preflight, capability advertisement and content-duplicate gaps; all corrected with regression coverage. Existing legacy serialization test caught inherited-field omission, also corrected.

## Verdict

Local real-platform integration with synthetic data; no production deployment or
Git publication. Existing older runtime and reports were preserved. New API/client
must roll out together: old readers cannot accept new block types/24-column geometry.
Physical pointer drag/resize was not automated by the available in-app browser API;
layout transactions, collision/lock validation, presets and undo were tested.
Screenshot records the editor, not proof of pointer gestures. User interaction with
the delivered local editor is the next visual acceptance step.

[Editor screenshot](editor.png)

Final screenshot review corrected checkbox row alignment in the inspector (32 px
rows); final frontend build passed.

Repository gate: `uv run --no-sync python -m tools.check --scope local` passed
after correcting the owned ticket/evidence metadata. `git diff --check` passed.

## Owner feedback: compact editor chrome

Removed the structure/comparison/scopes panels and duplicate add/history toolbar
from the canvas. Single-page tab and single-section heading are omitted; multiple
pages retain navigation. One shell toolbar contains Add, Undo/Redo icons and the
existing manipulation hint. Save has a disk icon. Inspector toggle now opens an
empty-selection prompt and closes correctly, verified in the live browser.
The report data/saved definition are unaffected. Final build passed.
Screenshot: [compact editor](editor-compact.png).

Text-height correction: new text defaults to one row, pointer/inspector minimum
is one row in platform and standalone prototype. Existing prototype layout
constraints are upgraded without changing saved heights. Browser reduced the
selected existing text from three to two to one row; decrement then disabled.
Screenshot: [one-row text](text-one-row.png).

## Platform parity continuation (2026-10-10)

Owner selected platform-only continuation and any existing metric set. Added source-bound KPI blocks (revenue, receipt count, average receipt) to the common grid; retained existing KPI value/readiness/YoY presentation. Ported prototype surfaces, compact chart/table rendering, shared controls and inspector. New reports use the composer; existing composer reports open without a query flag. Historical report formats retain their reader.

Persisted line/bar presentation with omission-compatible old serialization. Chart reveal uses 850 ms linear line clipping with synchronized symbols; bars use 400 ms growth with 110 ms stagger (capped for long series). Reduced-motion preference disables animation. Effective filter queries refresh automatically through existing stale-result guards.

Local API 58149 uses the same disposable database/artifacts as the earlier fixture, with web 41748. Browser opened the normal report URL, loaded seven saved blocks with three KPI cards, switched line to bars, saved, and changed Store 1 to all permitted stores. The linked chart automatically changed January from 2611.6 to 43908.52; unlinked table and KPI totals remained unchanged. Source-backed metric switching was exercised for receipt count and average receipt. Motion options are source-verified; no frame-by-frame timing claim.

Focused Python contracts/service tests: 62 passed. Focused frontend state/canvas/structure tests: 24 passed. TypeScript and production frontend build passed (existing large-chunk warning). No production delivery or Git publication.

Final verification: saved revision 5 contains seven blocks and five real result references. Reload restored bar presentation, all-store selection and three KPI values. The local session expired during verification; signed back in using the existing synthetic account. Saved-result hydration was noticeably delayed; sequential API reads for each KPI completed in about 2 seconds, but browser completion took longer. Root cause and latency improvement are not claimed. Final screenshot: [platform editor](platform-final.png). Final TypeScript, `check --scope local` and `git diff --check` passed.

## Hover card reference (2026-10-11)

Owner requested the supplied tooltip format. Shared platform charts now use a rounded slate surface, two aligned columns with muted right-aligned labels and bold values, and a separator before enabled temporal comparison. Missing comparison is omitted instead of showing empty deltas. Existing projection values/localization and safe DOM text insertion remain unchanged. Browser verified the tooltip on the live line chart without saving or replacing the user's current draft. [Screenshot](chart-tooltip.png). TypeScript and local profile passed; comparison layout is source-checked, not browser-exercised in this change.

Tooltip correction (2026-10-11): added an independent adjacent-point section (previous period/value and signed absolute/percentage change). It uses the immediately preceding plotted bucket, never skips nulls, and leaves the percentage unavailable for a zero baseline. Temporal/server comparison is a separate section with its actual mode label, baseline value and server deltas, shown only when comparison values exist. Live browser verified July versus June: 43215.10 versus 39765.08, +3450.02 (+8.7%). Year-over-year data was unavailable in this demo; that section was source-checked. Focused presentation tests, TypeScript and local profile passed.

## Reload regression — confirmed cause and repair (2026-10-11)

Owner reported slow page reload after canvas integration. In the same local report
(7 blocks / 5 saved analytical results), temporary browser request instrumentation
recorded 2.254 s for the first editor response, a redundant editor refetch taking
26.246 s, and successful block reads taking 14.279–30.518 s. Development StrictMode
also starts/cancels the first mount's requests. Response-body parsing was negligible.
No authorization tokens or payloads were logged; instrumentation was removed.

A separate cProfile API process using the same disposable database/artifacts
measured ComposerService.result at 3.374 s with profiler overhead: 3.347 s was in
five preflights called by validate_sources. A local store control makes every saved
report read preflight every analytical block. PreparedAnalyticsService inherited
query_inputs(metadata_only=True), which still fell back to verified_inputs for
unfiltered queries, repeatedly decoding all six raw entities. Saved-result reads
already had an identity-only Store projection; the new preflight path missed it.

Repair: PreparedAnalyticsService now routes metadata-only, non-receipt-filter
requests through existing identity_inputs. Scope normalization, calendar, current
access/recheck, saved-result hashes and artifact verification remain in place.
Compute continues through full inputs, and receipt-filter queries delegate to the
existing bounded provider. No schema/persisted data/cache identity change (`none`);
read validation now consistently uses the previously accepted prepared-reader
boundary rather than rereading unrelated raw history. ComposerWorkspace suppresses
mount refetch only when its normal-route guard has already loaded the editor;
explicit `view=composer` retains mount refetch.

Before-fix regression run: 1 failed / 4 passed, specifically detecting all six
entities read where only Store is needed. After: focused request-read/composer/
contract/scope suite 65 passed; TypeScript, focused Ruff and local profile passed.
Tests compare normalized context/hash with full inputs, reject forbidden stores,
and confirm calculation still reads all six entities. Independent review found
and resolved the explicit-route refetch issue; no remaining narrow findings.

Same-machine real HTTP measurement (Python urllib, existing synthetic author,
5 parallel saved-result GETs, no compute or data mutation): baseline batches
12.716 / 12.550 s; candidate batches 0.182 / 0.114 s. Candidate first editor GET
0.080 s. API process restarted for candidate; OS filesystem caches were warm in
both, no cold-start or production performance claim. Baseline first editor sample
20.433 s overlapped browser load and is not an isolated comparison. Browser reload
after fix: editor 70 ms, all five result reads 207–376 ms, full values visible.
Profiler process was stopped; current local API remains on 58149, web on 41748.
This supersedes the earlier unresolved slow-hydration limitation for this tested
fixture. Larger datasets and deployment environments were not benchmarked.

### Reload layout stabilization (2026-10-11)

Composer loading now uses a neutral status instead of the legacy speculative KPI
layout. The iframe paint guard remains until workspace portals mount; canvas
width is measured in a layout effect. Grid placement transitions are limited to
active drag/resize; the composer inspector no longer animates canvas width.
Chart series entrance/update animations are unchanged. No report data was saved.
Two local browser reloads reached the saved seven-block report. Computed block
and workspace transition durations were 0s outside gestures; no console errors
were reported. See [loaded report](reload-stable.png). This is local browser
inspection, not a frame-by-frame recording or a production performance claim.
TypeScript and `tools.check --scope local` passed.

### Free row placement (2026-10-11)

Disabled React Grid Layout vertical compaction (`compactType={null}`). Blocks
retain chosen grid rows with empty space above; grid snapping and overlap
validation remain. Browser drag moved the selected metric from row 2 to row 4
(y 279.84 to 371.84) without pulling it back up. Captured
[free placement](free-placement.png), then undid only the verification gesture;
the user's existing unsaved layout was preserved. TypeScript, four canvas tests
and the local tooling gate passed.

### Stationary neighbors (2026-10-11)

Enabled `preventCollision` together with disabled compaction. Drag/resize cannot
push neighboring blocks. Inspector geometry changes likewise reject overlapping
placements instead of relocating unlocked neighbors. Added a regression test for
move/resize collision rejection and free placement with unchanged neighbors.
Browser drag toward the occupied heading stopped at the last free row; all six
other block coordinates stayed identical. See
[collision placement](collision-placement.png). Verification movement was undone
and all seven coordinates matched the user's prior unsaved layout. No save or
reload was performed. TypeScript, five canvas tests and local tooling passed.

### Card-surface dragging (2026-10-11)

Exercised local Metabase's editing surface: dragging inside the Sankey plot moved
its card; dragging back restored all captured card transforms, without saving.
Adopted whole-card dragging in Composer instead of a grip-only handle. Native
controls, links, labels, editable fields and control roles are excluded from drag
initiation. Editable cards use grab/grabbing cursors; locked/read-only cards do
not advertise dragging. Corner resizing, no compaction and collision prevention
remain. Updated toolbar and inspector hints.

On the platform, dragging directly on the metric value moved it down three rows
(y 647.84 to 785.84); the verification movement was undone. See
[surface drag](surface-drag.png). The store dropdown opened normally and the
chart settings button opened its inspector. No console errors were reported.
The current crowded chart drag did not relocate the chart; a successful chart
surface move on the platform was not independently established in this pass.
TypeScript, five canvas tests and local tooling passed. No report was saved by
the agent during these checks.

### Remove redundant drag grip (2026-10-11)

Removed the grip button and its unused import/styles; all buttons are excluded
from drag initiation. Settings remain right-aligned on each card. Browser check:
zero grip elements, seven settings buttons, selected table shows only settings.
See [updated canvas](no-drag-grip.png). TypeScript and local tooling passed.
No report layout or saved data was changed by the verification.

### Immediate text editing (2026-10-11)

Confirmed cause: the inspector textarea committed only on blur and used text as
its React key. Changed to a controlled value/onChange binding with stable element
identity. Local draft updates are immediate, without waiting for blur or save.
Regression test failed before the fix (preview retained old text), then passed:
updates before blur, same focused textarea, middle-insertion caret and empty text.
TypeScript and local tooling passed. Browser verification found matching textarea
and canvas text while the textarea still had focus; see [live text](live-text.png).
The verification input was undone; no report was saved. Browser observation
confirms live propagation, not a quantitative end-to-end latency benchmark.

### Type-aware visual inspector (2026-10-11)

Implemented Data / Visualization / Block inspector routes and adjacent per-block
settings/paintbrush entry points. Type-aware sections include title/description,
combo series, labels/number formatting, axes/grid, legend, goal, tooltip and motion;
tables expose column visibility/order/width/alignment/wrap/precision, conditional
text colors, freezing, row numbers and pagination. Text has size/alignment/style.
Changes render immediately; continuous field edits share one undo entry.

Persisted typed presentation settings and shared chart compiler mapping preserve
legacy omission serialization. Contract impact: new-reader/old-data compatible;
old-reader/new-visual-fields is breaking, requiring coordinated API/Web rollout.
Analytical query identity and authorization are unchanged. Unsupported shape types
remain disabled with required-data explanations (not fake rendered options).
Full catalog inclusion does not claim new graph/geography/distribution/pivot
providers, full Metabase feature parity, or export-renderer parity.

Validation: 19 focused Python contract tests; TypeScript and Web production build;
local tooling profile PASS. Browser: correct icon-to-tab route, live combo bar/line
with independent colors, server calculation on additional metric, immediate title
while focused, one-step undo of continuous typing, description popover, table
precision/pagination/row numbers. API save/read roundtrip passed on a disposable
report `3c0ae51f-2165-4997-8174-bd5ee4bd1a57` in the local synthetic fixture; the
owner's report was not saved or replaced. Initial verification attempts used a
wrong direct API prefix and then lacked Origin; both failed before any save, and
were corrected using the configured proxy/header contract.

Independent source review identified and resolved automatic-axis clipping,
implicit multi-metric rendering, lost combo temporal pairs, and lost partial-table
indicators. Focused regression tests cover these cases including temporal_v2.
Review is local source evidence; no production release/deployment claim.

Final focused frontend suite: 16 tests passed. Post-undo saved-state detection
compares both the canvas-normalized definition and saved result references, so
undoing all edits removes the unload guard without saving. Verified in browser.
During development HMR retained a stale chart after the effect dependency shape
changed; a clean reload rendered the chart correctly. This was observed during
hot replacement, not on the verified clean-load path.

[Current platform visual inspector](visual-inspector.png).

## Authoring inspector repair — 2026-10-11

Owner-selected follow-up to the local audit: shared visible field/button styles,
flat existing-block data form, and selection reveal. Browser interaction impact:
compatible-change for local authoring; API, persisted schemas and calculation
semantics unchanged. The no-stroke global rule is overridden only inside composer
forms; other surfaces are unaffected. New blocks retain the three-step creation
flow. Existing blocks apply validated data from one form, preserving concurrently
edited title/type. Text creation selects the content tab. Canvas reveal scrolls
the report container without focus transfer, layout compaction or animation.

Local browser repeated creation of revenue/receipts/average-receipt tables, revenue
line chart, receipts bar chart, an info description, and a text block. Saved report:
`0280898a-0ac8-4fff-8047-6a8f6e344faf`. Saved preview contains all six blocks. Existing
table grain changed month -> quarter -> month using the flat form and recalculated
successfully. The lower selected chart was fully inside the scroll viewport
(card y=337..699, viewport y=148..711 at the inspected desktop width). Receipt filter
search has a visible 1px border and 2px focus outline. Full network, mobile and
assistive-technology audits are not part of this proof.

Validation: 12 focused frontend tests passed, including flat-form validation and
preservation of externally edited title/type; TypeScript and production frontend
build passed (existing large-chunk warning). Local tooling profile passed.
No production deployment or source publication. Remaining audit items, including
long one-row text overflow, table scroll discoverability, localization/technical
labels and preview navigation, were not included in these three selected repairs.

Evidence: [flat data form](inspector-flat-data.png),
[selected lower chart](inspector-selected-chart.png).

## Compact comparison repair — 2026-10-11

Owner requested compact hover comparisons, signed green/red deltas, removal of
technical temporal summaries and calendar mapping columns from canvas blocks.
Changed ComposerWorkspace, WorkspaceProjection and ComposerVisualTable; retained
server values/deltas, unavailable percentage semantics and row coverage warnings.
Canvas tables now name current/baseline value columns. Temporal charts reuse the
current bucket label rather than a full date range. API/persistence: none;
browser presentation: compatible-change. Existing legacy details component remains
available to other consumers. No calculation or permission changes.

Validation: 13 focused projection/temporal tests pass, TypeScript and frontend
production build pass (existing large-chunk warning), check:local passes.
Browser on local :41748 showcase: both comparison charts retain full plot height;
comparison tables no longer include calendar columns/duplicate totals. Hover May
shows +3,587.46 (+10.1%) in green and YoY -645.96 (-1.6%) in red; September negative
adjacent and YoY changes are red. Screenshot: [compact tooltip](compact-comparison-tooltip.png).
Network and full responsive coverage were not re-audited. Local evidence only.

## Legend/axis/label controls — 2026-10-12

Shared composer compiler reserves a width-aware left/right legend lane with
truncated long labels and scroll navigation; the plot updates on container resize.
Category titles use centered placement and reserved space in both orientations.
Inside labels use light text on a dark backing; outside labels use a dark outline.
Maximum thickness is labeled as a cap; paired sliders/numeric inputs also control
category gap, including stacked bars. No analytical/API/persistence schema change;
compatible presentation change: existing bar_gap also controls category spacing.

Browser: observed left/right legend separation, visible X title in vertical and
horizontal orientations, thickness change 25 to 4 px and category gap change
71 to 20, readable labels on narrow bars. User draft was lost during dev reload;
restored observed chart settings but not the entire unsaved layout. Saved report
was not overwritten. Final screenshot: legend-label-controls.png.
10 compiler tests and TypeScript pass; frontend build passed before final label
background adjustment, which was covered by the subsequent typecheck/tests.
check:local passes. Local browser/runtime only; no production deployment.


## Owner continuation — text surfaces and metric clipping (2026-10-12)

Removed the text Size selector; existing serialized text_size values remain
compatible. Plain text blocks now have a transparent outer surface and the
English option reads “No background”; Callout retains its accent surface.
Metric content no longer flex-shrinks below its line box; a 1.2 line height
and tighter inter-row spacing preserve the existing three-row card size.

Browser evidence on the local metrics catalog: all six KPI line boxes changed
from 23.7–24.9 px (31.05 px line height) to 32.4 px (32.4 px line height).
Both plain text surfaces are transparent; Callout toggles to rgb(24,39,44).
The owner draft was saved before HMR; the background smoke change was undone.
Scope: presentation only; no schema/API or analytical calculation changes.

Validation for text/metric continuation: web typecheck, local tooling profile
and git diff --check passed. Real-browser checks covered the six metric cards,
removed control, and both background states. Screenshot:
[text/metrics result](text-metrics-fixed.png). No production delivery claimed.


## Owner continuation — compact metric numbers (2026-10-13)

Owner accepted automatic k/m/b suffixes, whole base-unit values, at most one
compact decimal, and at most one decimal for percentages. Added the shared
metric-number formatter, applied it to composer/configured metric cards,
chart totals and card absolute changes, and removed conflicting metric precision
controls. Full rounded KPI values remain available through title tooltips.
Percentage precision is capped for visual table comparisons, percent-valued
columns, chart labels and axes; existing tooltip/YoY formatters already cap at one.
Stored numeric values, results and schemas are unchanged. Presentation impact:
compatible change; historical decimals/compact cannot override KPI formatting.

Validation: 26 formatter cases and 10 chart option tests passed; web typecheck,
local tooling profile and whitespace check passed. Browser inspection confirmed
all six KPI cards display 393.9k / 2.1k / 184, full rounded title values,
and compact YoY absolute changes. English locale was observed live; Russian
decimal formatting and boundaries through 100b were unit-tested.
[Browser result](metric-numbers.png). No production deployment.


## Large-monitor grid correction (2026-10-13)

Owner reported excessive scaling at 2622×1565. Composer content now caps at
1200 CSS px and centers within the canvas area; narrower screens remain fluid.
Rows stay at 40 CSS px independently of viewport width. Grid coordinates/spans,
free placement and source data remain unchanged. Browser checks at 2622×1565
and 1414×959 confirmed canvas widths 1200/940 and identical 132 px heights for
all six three-row KPI cards. Temporary viewport override was reset; draft was
not saved or reloaded. Typecheck, canvas tests and local gate passed.


## Empty block title repair (2026-10-13)

Confirmed cause: the Data title field committed only on blur and restored its
previous value when empty. It now updates the shared draft on every change,
including empty input. BlockPresentation.title accepts an empty string (200
character maximum retained); report/page title constraints are unchanged.
Generated schemas/client were regenerated. Text blocks omit empty heading markup.
Contract impact: input validation relaxation, with newly emitted empty titles
requiring the updated reader/server; no persistence migration. Existing snapshots
remain valid. Local API was restarted with the existing configuration.

Verification: nine presentation contract tests passed including an empty-title
serialization roundtrip; web typecheck and local gate passed. Browser observed
clear -> blur retaining empty -> retype restoring title. Test editing was restored
without saving the user's draft. No pre-fix red test was captured; direct handler
inspection established the rejection. No production delivery.


## Wider canvas follow-up (2026-10-13)

Owner found the previous 1200 px cap too narrow. Raised it to 1800 px while
retaining the fixed 40 px row height and fluid width on smaller screens.
This supersedes the earlier width cap, not grid coordinates or stored layouts.
Browser: 2622×1565 yields 1800 px canvas; 1414×959 yields the unchanged 940 px.
Three-row metric cards remain 132 px tall in both. Viewport override reset.
Only CSS and documentation changed; no draft mutation or page reload.


## Page navigation feedback (2026-10-13)

Page tabs now have a full button-width 2 px active underline, hover surface/line,
and keyboard focus outline. Overview retains the full-width separator without
the unrelated fixed 48 px active mark. Page titles remain literal, with no
automatic numbering or regex stripping of owner-authored numbers.
The six numbered showcase page titles were renamed through the versioned API,
after saving the current browser draft; expected_revision protected the write.
Browser verified page switching and active underline rgb(120,200,218), 2 px.
Local gate and diff check passed. Screenshot: [page tabs](page-tabs.png).


## Inspector header stability (2026-10-13)

Header flex-shrink caused 71 px height on short panels and 58.07 px on Data.
Fixed the direct inspector header at a non-shrinking 58 px with fitting padding.
Browser measured Data, Visualization and Block at exactly 58 px and identical
bottom coordinates after switching. No report content or draft persistence changed.
Local gate and diff check passed. Evidence: [header](panel-header.png).

## Block actions continuation — 2026-10-13

Removed the Block inspector tab and geometry controls. Every canvas block now
has duplicate/delete after data/visual actions. Delete uses a native HTML modal
with named target, initially focused Cancel, Escape cancellation and explicit
confirmation. Locks/read-only guards are retained; removal uses existing undo.
Browser-visible contract: compatible-change in action placement; no API/schema change.

Observed on the local platform: duplicated the receipts metric, cancelled deletion
(two copies remained), then confirmed deletion of the disposable copy (only the
original remained). Data and Visualization are the only inspector tabs. The report
returned to Saved without persisting test changes. Screenshot: [block actions](block-actions.png).
Focused inspector/canvas tests: 7 passed. Typecheck and local tooling gate recorded
below. This is local UI proof, not a release or production deployment.

Final checks: frontend typecheck passed; `tools.check --scope local` passed; `git diff --check` passed. Escape closed the confirmation without removing the original metric.

## Inspector width repair — 2026-10-13

The desktop workspace reserved 350px while the composer inspector occupied only
280px. The composer-specific grid column now reserves 280px and its inspector
fills that column, returning 70px to the canvas. The existing <=1100px overlay
rules remain unchanged. No data or API contract change.

Browser DOM measurements at 1414px: before slot/panel 350/280px, after 280/280px;
canvas column increased from 992px to 1062px. Rendered Data form shows no unused
right strip. [Screenshot](inspector-width.png). No report mutation or reload was
performed for this repair. Local tooling and whitespace checks passed.

## Click versus movement — 2026-10-13

RGL start callbacks fire on mouse-down, so they previously flashed the canvas grid
on plain clicks. Grid feedback now starts on drag/resize movement; no-movement
stop skips layout commit. The placeholder is hidden while no movement is active.
Browser click selected the metric without grid feedback. A real RGL DOM regression
test covers held mouse-down, click selection without commit, drag movement and
resize movement, including feedback removal on release. The jsdom fixture supplies
layout measurements/offsetParent; it does not mock RGL callbacks.
Screenshot: [selected block without grid](click-without-grid.png).
No API or persistence schema change; local UI verification only.

Final checks: 7 focused tests passed; frontend typecheck, local tooling gate and whitespace check passed.

## Readable minimum metrics — 2026-10-13

Owner-approved minimum metric dimensions are 220×140 CSS pixels. Canvas geometry
translates the width limit to columns and expands the canvas for existing narrow
placements without changing persisted cells or moving neighbors. Section row
height may increase to meet the pixel minimum; the 40px base remains for other
sections. Only the canvas scrolls horizontally. Selected cards are revealed.

Metric actions reserve a separate 28px row. Titles clamp to two lines with native
full-title hover text; values stay unwrapped. Ordinary Ready and YoY off labels
are removed; enabled comparisons, missing-data reasons, loading/errors remain.
No API or schema change. Compatible presentation change, local runtime only.

Browser evidence: at viewport 1414px the existing four-column metric measured
220×141px, content height/scrollHeight both 111px, and tools ended 6px above the
title. At 2622px the same card measured 295×141px; all six metric bodies had no
vertical overflow. Viewport override restored. User draft was not saved/reloaded.
[Minimum metric screenshot](readable-metric.png).

Eight focused canvas/gesture tests passed, including minimum geometry at laptop
and large widths and unchanged cell positions. Frontend typecheck passed.

Final local tooling and whitespace checks passed.

## Floating block actions — 2026-10-13

Owner replaced the internal action row with an external toolbar above every
canvas block. Hover/focus reveal it; a pointer bridge covers the small gap.
Hovered/focused blocks rise above neighbors. Canvas top padding keeps first-row
actions inside the scrolling viewport. Metric content no longer reserves an
internal action row. Existing deletion confirmation and read-only hiding remain.

Browser: toolbar bottom measured 426.74px against card top 429.74px; clicking
Visualization from the toolbar opened the inspector. No document save/reload.
[Screenshot](floating-actions.png). CSS-only presentation change; no API impact.

Local tooling and whitespace checks passed.

## Narrower metrics after floating actions — 2026-10-13

Owner clarified width only. Reduced pixel width floor from 220 to 140px, allowing
four columns instead of six on the notebook canvas. Height floor remains 140px.
Existing placement values are preserved. Browser at 1414px: four-column card
163×141px, body clientHeight/scrollHeight both 139px; title and number visible.
Viewport restored. Eight canvas tests, local gate and whitespace checks passed.
[Screenshot](narrow-metric.png). Local presentation-only change, no API impact.

## Two-row minimum metric — 2026-10-13

Owner requested one less height cell. Metric minH is now two rows / 92px;
section row geometry remains stable. Two-row cards use smaller padding/type and
a single-line comparison with the existing full comparison title on hover.
Browser resize at 1414px reached 92px for both ordinary and YoY receipt metrics;
YoY body clientHeight/scrollHeight were both 90px and comparison remained visible.
The two successful resize checks were undone and viewport override restored.
[Screenshot](short-metric.png). Ten focused tests and frontend typecheck passed.
No API/schema changes; local proof only.

Local tooling and whitespace checks passed.

## Suppress text selection during gestures — 2026-10-13

The canvas now suppresses selectstart and native/WebKit user selection in its
own document from gesture start. Release, cancel, window blur and unmount remove
the guard; grid feedback still waits for movement. Existing text selection is
cleared when starting the gesture. No persistent selection restriction is applied.
Browser: receipts card resized down/right from 163×141 to 248×239, then up/left
back to 163×141. No text highlighting observed; guard absent after both releases.
Viewport restored. [Screenshot](resize-selection.png). No report save or reload.
Focused real-RGL test verifies selection cancellation during resize and restoration
after release/blur. Local runtime boundary only; no API/schema change.

Focused gesture regression, frontend typecheck, local tooling and whitespace checks passed.

## Unified resize layers — 2026-10-13

Confirmed source cause: RGL uses z-index 1 for resizing and 2 for its placeholder,
while canvas hover/focus raised any neighbor to 8. Collision handling also makes
the placeholder geometry differ from the live card size. This explains split
occlusion and the extra translucent rectangle in the owner screenshot.

Gesture composition now has one opaque active card at z-index 20, neighbors at 0,
no visible placeholder, and no block toolbars while moving/resizing. Grid guides
remain below cards. Section isolation contains these layers within the canvas.
Existing collision prevention, selection suppression and saved placements remain.
No API or persistence changes; compatible presentation repair.

Browser collision exercise at 1414px crossed the right and lower cards. Compared
DOM styles showed no neighbor movement. On release the active geometry was limited
to available cells. The current user tab changed during inspection; an attempted
Undo was disabled, so no further history actions were performed. Viewport restored.
The [final screenshot](clean-resize.png) records the released state, not a held gesture.

Automated real-RGL mouse sequences load the actual composer stylesheet and verify
active drag/resize stacking, opaque active card, hidden placeholder/toolbars,
neighbor layer and unchanged neighbor placement after collision, cleanup after
release, selection suppression/restoration and window blur. A pre-fix visual red
run was not captured; initial test harness failures were resolved before the final
run. Ten focused tests passed, frontend typecheck passed, local tooling and
whitespace checks passed. This is local UI evidence, not production release proof.

## Goal line visibility — 2026-10-13

Owner repair, ANALYTICAL-DOC-004 / DASHBOARD-006. Confirmed source cause: markLine was excluded from automatic value-axis extents; its default end label fell outside the plot. Compiler now expands automatic bounds around the goal, keeps explicit bounds, maps horizontal goals to xAxis and places labels inside the plot. Inspector names the goal-line label and explains its purpose with an example and localized fallback. Browser contract: compatible-change; persisted/API shapes and analytical data unchanged.

Verification: chart compiler and web typecheck passed; `pnpm --filter @custometry/chart-compiler exec vitest run tests/composer-goal.test.ts` passed 5 tests using real ECharts SSR coordinates/SVG (above maximum, negative, zero, explicit limits/removal, horizontal bars). No pre-fix red test captured. `uv run python -m tools.check --scope local` and `git diff --check` passed. In existing in-app tab, changed 35000 to 60000 and label to Sales target; observed visible line and label with scale extended to 63000. Screenshot: goal-visible.png. Restored original 35000 / ваи draft fields; did not save or reload user's draft. Browser error log empty; network not inspected. Local runtime only.
