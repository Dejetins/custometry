---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.11.0-draft
ticket_id: W41-COMPOSER-CANVAS-LAYOUT
proof_boundary: local-composer-canvas-with-existing-test-data
proof_skills: [better-layout, better-accessibility, browser-qa-evidence]
verdict: passed
redaction: Synthetic fixture only; no credentials or raw API payloads recorded.
executed_checks: [focused frontend tests, frontend build, browser pointer and keyboard flows, save and reopen, responsive anchors]
observations: [Native pointer drag reordered charts, native pointer resize changed width and height, undo restored placement, saved table width persisted on reload]
---

# W41 canvas layout evidence

[Ticket](../../tickets/W41-COMPOSER-CANVAS-LAYOUT.md) and
[UI requirements](../../../../custometry-ui-blueprint-ru.md).

## Outcome and scope

Owner authorized direct manipulation and removal of useless block whitespace.
Existing grid placements could only be edited through a technical structure form;
empty status paragraphs reserved space and routine UTC paragraphs displaced results.
Changes are in the serving c67c checkout, with previous uncommitted work preserved.
No dependency, backend, API or persistence schema change; browser behavior is a
compatible addition. Layout updates reuse existing history, query identity and save.

New composer-layout.ts reorders/repacks a section, preserving IDs, queries and locked
blocks. ComposerLayoutControls.tsx provides pointer handles, insertion indication,
width/height menu and earlier/later alternatives. ComposerWorkspace.tsx connects
existing undo/save and collapses block actions; composer.css allocates result height.
Routine timezone and empty status rows are gone; errors/loading and meaningful UTC
coverage limitations remain (the latter in a disclosure). UI blueprint links W41.

## Commands and observations

- Vitest: composer-layout.test.ts (6) and composer-structure.test.ts (9), 15 passed.
  Covers no overlap, mixed widths, heights, query identity, locks, invalid input,
  undo/redo and flow ordering. Final test fixture typing correction rerun recorded
  in command output; no change to product semantics.
- TypeScript + Vite build passed. Initial build caught a readonly assignment in
  the new test fixture; corrected by immutable replacement. Chunk-size warning remains.
- In-app browser on existing synthetic demo: native drag moved receipts before
  revenue; native corner drag expanded revenue to 12 columns, undo restored 6;
  vertical drag changed row span to 2 and plot height to 629px, undo restored it.
- Keyboard Enter opened Layout; width selection made the table full width;
  earlier/later commands moved it. Saved via real API. Reload retained both 6-column
  charts and 12-column table with unchanged result values, no empty status paragraph.
- Responsive anchors 768x1024 and 1920x1080: blocks had equal client/scroll widths,
  no horizontal overflow. Temporary viewport overrides were reset.

## Boundaries

Movement is within the current section: cross-section movement changes inheritance
and remains an explicit structure operation. Resize is grid-only; flow/narrative
support ordering. Narrow layout stacks blocks; width remains persisted for desktop.
Locked affected blocks reject mutation rather than move silently. Read-only saved
snapshots expose no layout controls. No new report creation journey or full screen
reader audit was run. This is not completion of WS-004 or production publication.


## Verdict

Passed for the bounded canvas change. New immutable snapshot
1feb0f9d-97cc-46eb-ab97-b3a4cc02a74a retained saved layout and exposed zero drag
handles. Snapshot plots measured 298px within 358px inner block height. Screenshot:
/tmp/custometry-canvas-layout-saved.jpg. The owner is returned to the edit route.
Local gate initially rejected ticket metadata/section omissions; corrected to the
canonical closed schema without weakening validators. No production readiness claim.

Final local gate passed (observed=true); git diff --check passed. Browser console
error query empty. Editor screenshot: /tmp/custometry-canvas-layout-editor.jpg.


## Owner follow-up: calculation action and chart area

On 2026-10-08 the owner requested removal of permanent Apply chrome and more plot
area. BlockCalculationAction now exposes Recalculate in the block menu for ready
results, Calculate/Retry in the header when needed, and no mutation action in saved
preview. Existing calculation/read retry handlers and permission checks remain.
WorkspacePlot has an opt-in compact grid for composer; other consumers retain the
original margins. No series, formatting, units or query semantics changed.

Before source hot update, saved the owner's unsaved test draft via its existing
Save action and observed Saved. That draft intentionally had revenue width 2/12;
kept that placement. Native Recalculate menu action was exercised in the other
test tab, observed Calculating and then result with no footer action. The current
owner tab has no horizontal block overflow at 768x1024 (649/649); viewport reset.
22 focused tests passed (4 action-state interactions + 18 presentation tests).
Hot refresh logged the React dependency-array-size warning while adding compact
as an effect dependency; clean reload was performed afterwards. This is recorded
rather than claiming a clean historical console. Screenshot:
/tmp/custometry-chart-space-fixed.jpg. No save of the test recalculation was issued.


## Owner follow-up: visual size presets

Replaced the 12-value width select with four labelled visual buttons (3/6/9/12
columns), using aria-pressed for the active preset. Pointer resizing snaps to the
same four sizes. Height uses decrement/increment controls. Existing custom widths
remain unchanged until an explicit choice. The menu uses viewport-bounded fixed
positioning rather than overflowing past the left workspace edge. Escape returns
focus to its summary. Two focused tests cover four choices, custom-width preservation,
selection handler and pointer snapping. Real browser opened the 224px menu at x116,
fully within the viewport; screenshot /tmp/custometry-size-presets.jpg.

Preset follow-up verification: real browser selected 1/2 (span 6) and Undo restored
custom span 2. At 768px viewport the menu stayed at x536..760. Escape closed it
and focused SUMMARY. Initial test build rejected Testing Library's unsupported
exact option; removed it, reran tests/build successfully. Local gate passed.

## Owner regression: overlapping contextual menus

The owner's running editor had two independently open Layout disclosures. Prior
preset checks did not cover switching between blocks; that evidence did not prove
menu exclusivity. Saved the owner's current draft through Save before hot update,
observed Saved, and retained widths 6/6/12.

ComposerBlockMenu now owns shared Layout/action disclosure behavior: opening one
closes other block menus; repeat trigger, outside pointer/focus, Escape, report
scroll and viewport resize dismiss it. Escape returns focus. Width/reorder/action
selection closes; height steppers remain open. Both menus are viewport bounded.
Inspector return focus targets the visible actions summary, not a hidden button.
No report schema, query, calculation or permission behavior changed (compatible
browser interaction correction; no API/persistence impact).

Eight focused tests passed: six menu lifecycle/interaction checks plus two existing
size preset tests. TypeScript/Vite build passed with the existing large-chunk
warning. Real browser verified Layout A -> Layout B -> Actions A exclusivity,
repeat close, Enter/Escape with summary focus, outside click, native scroll,
Edit block -> inspector -> close with actions-summary focus, 3/4 selection followed
by Undo restoring 6/6/12, and repeated height increase/decrease. At 768x1024,
viewport resize closed the menu; reopening stayed within x536..760 and y624..890.
Reset viewport. Reload retained the local dirty draft; verified the restored
6/6/12 widths, one-row heights and row positions, then saved that baseline again.
These checks establish this menu fix, not overall completion of the composer.
Screenshot: /tmp/custometry-single-block-menu.jpg.

Menu regression handoff: `tools.check --scope local` and `git diff --check`
passed. Final browser state was Saved with exactly one open Layout menu.


## Owner correction: keep menus open during scroll; plain-language sizing

The owner explicitly rejected scroll dismissal and fractional width labels.
This supersedes the preceding scroll/resize dismissal behavior and its acceptance
observation; previous tests proved the wrong intended interaction.
Menus now re-anchor on report scroll/viewport resize without closing. Outside
pointer/focus, Escape and switching menus still dismiss. Width choices use
Narrow/Medium/Wide/Full width (RU: Узкий/Средний/Широкий/Во всю строку), with
visual previews; height uses Shorter/Taller without a technical row multiplier.
Placement storage and the four supported spans are unchanged.

Eight focused tests passed, including anchor movement while staying open and
ignoring internal panel scrolling. TypeScript/Vite build passed (large-chunk
warning retained). Browser report scroll moved the same open menu from y553 to
y265; no reopening was needed. No report data changes were made in this follow-up.

Browser also verified exclusivity, Escape and outside dismissal after the change.
Resize to 768x1024 kept the menu open within x536..760, y749..1016. Restored
viewport. Local gate and whitespace check passed. Screenshot:
/tmp/custometry-plain-sizing-menu.jpg. The owner's active locale remains English;
both RU and EN labels were updated without changing that preference.
