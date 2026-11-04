---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.11.0-draft
ticket_id: W40-WORKSET-CATALOGUE-INTERACTIONS
proof_boundary: local-preview-real-api-workset-and-catalogue-interactions
proof_skills:
- browser-qa-evidence
- contract-impact-analysis
verdict: passed
redaction: Screenshots contain synthetic local report fixtures only. No credentials,
  cookies, session payloads or vendor business data are included.
executed_checks:
- corepack pnpm --filter @custometry/web build
- corepack pnpm --filter @custometry/web test
- uv run python -m tools.check --scope local
- git diff --check
- playwright-cli local preview with real API
observations:
- 110 frontend tests passed across 22 files.
- Empty set persisted and remained empty after full reload.
- Named creation, catalogue membership, rename, hide/show, copy and deletion observed
  in browser.
---

# Outcome and scope

[W40 ticket](../../tickets/W40-WORKSET-CATALOGUE-INTERACTIONS.md) implements the owner-selected interactions from the [follow-up reference](../../../../docs/architecture/ui/references/mindbox-metrics-2026-09-17/follow-up-2026-09-24/README.md), with ordinary creation explicitly empty.

Requirements: METRIC-025, METRIC-026, METRIC-027, REPORT-018, REPORT-019, A11Y-001, I18N-001.

Changed frontend: `ConfiguredWorkspace.tsx`, `WorksetControls.tsx`, `MetricCatalogue.tsx`, `workspace.css`, `workset-controls.test.tsx`. Preserved existing common/card scope, bulk store settings, explicit Apply/Save, report revision checks and creator/reader capabilities. Added named creation, duplicate-name checks, All disclosure search/show/hide/rename/delete, explicit save-as-new, selected/available metric checkboxes, staging of metric filters, drag ordering and keyboard ordering buttons. Empty sets never show the previous plot.

Browser-visible impact: compatible-change to existing report contracts, with changed creation flow. API/DTO/schema/persistence/migrations: none. Visibility is a session presentation setting; saved names and card composition use the existing report version. Save-as-new explicitly copies current cards and saves the report. No shared-brand propagation is invented.

# Commands and observations

| Command / action | Result | Observation |
|---|---|---|
| `corepack pnpm --filter @custometry/web build` | pass | TypeScript and Vite; existing large-chunk warning remains |
| `corepack pnpm --filter @custometry/web test` | pass | 22 files, 110 tests; name validation, cancellation/focus return, reader controls and staged picker cancellation covered |
| `uv run python -m tools.check --scope local` | pass | Initial generated-index drift repaired with `generate_docs_index` |
| `git diff --check` | pass | No whitespace errors |
| playwright-cli: create, add metric, Apply, Save, reload | pass | Real local API persisted membership |
| playwright-cli: rename, hide/show, save-as-new, reload | pass | Named copy persisted; source remained present |
| playwright-cli: empty creation, Save, reload | pass | Empty cards and empty state preserved, no stale plot |
| playwright-cli: delete own test sets, Apply/Save | pass | Test sets removed and cleanup persisted |
| screenshots at 1440x1000 and 768x900 | pass | [Catalogue](catalogue-desktop.png), [narrow picker](metric-picker-narrow.png), [persisted empty set](empty-persisted.png), visually inspected |
| playwright-cli console after final reload | pass | 0 errors, 0 warnings |

The first scripted copy check timed out because it waited for `/save`; the actual route is `/versions`. Subsequent full reload confirmed the saved copy, and final save/cleanup checks awaited successful `/versions` responses. An earlier immediate reload triggered the existing beforeunload guard while save completion was pending; subsequent checks awaited completion. Neither harness issue is counted as a successful original check.

# Verdict

Passed at the local preview / real API boundary on localhost:41746 in checkout c67c. Test fixtures were cleaned up. No publication, production deployment, vendor equivalence beyond the observed interactions, screen-reader certification or fresh server-side reader security audit is claimed. Creator actions are hidden for readers in the focused component test; server guards are unchanged. RU/EN copy is implemented; browser screenshots use English. Existing foreign checkout changes and milestone ledgers were preserved.

## Subsequent owner correction

[Browser feedback correction](feedback-2026-09-24.md) supersedes duplicate-save behavior and adds the explicit temporal difference overlay.

[Compact catalogue correction](compact-catalogue-correction.md) records the latest owner-selected modal catalogue, compact workset popovers and store-count summary.

[Grouped catalogue correction](grouped-catalogue-correction.md) records compact category rows and visible, explicit report-filter inheritance.

[Axis-label alignment](axis-label-alignment.md) records the fixed metric-name origin.

[Zero-baseline correction](zero-baseline.md) replaces the tightly cropped Y-axis domain under the latest owner instruction.

[Restored result downloads](restored-result-exports.md) records PNG/SVG and XLSX/CSV menu restoration.

## Owner follow-up: active navigation tile

The owner-provided screenshot supersedes the pilot's cyan active rail indicator. `apps/web/src/features/reports/navigation-dock.css` now renders the active destination as a neutral gray tile with an 8px radius and a light icon, without inset strokes, including when the contextual navigation is expanded. Existing keyboard focus indication remains unchanged. Preserved pilot sources remain unmodified.

Frontend build passed. Browser verification on the local configured report confirmed no box shadow, zero border width, gray background and light icon in the current state; expanded current state also has no selection stroke. [Rail screenshot](active-rail.png) visually inspected. `uv run python -m tools.check --scope local` and `git diff --check` passed. This is a cosmetic owner-authorized follow-up, with no navigation or data behavior changes and no production claim.

## Owner follow-up: structured workset bar

Implemented the owner-accepted one-row arrangement: Sets disclosure, borderless underlined active workset tabs and create control on the left; metric inspector and current-set overflow actions on the right. Rename/copy/delete now live in the current-set action disclosure; the Sets list retains search and session visibility controls. The tab region scrolls independently while actions remain visible. Changed `WorksetControls.tsx`, its existing tests, `ConfiguredWorkspace.tsx` and `workspace.css`. No persistence/API changes.

Build and frontend tests passed (24 files, 116 tests). Two existing tests initially expected the previous controls; updated them to exercise the new copy flow and reader restrictions. Local browser checks covered empty creation, rename, copy, delete, switching, list search and Escape, at 1480×969 and 390×844. The first narrow screenshot exposed intrinsic grid width overflow; `min-width:0` on the row fixed it and the flow was rerun. [Wide](setbar-wide.png) and [narrow](setbar-narrow.png) screenshots visually inspected. Changes remained in the isolated browser draft; no report was saved. Local grouped gate and whitespace check passed. Local UI evidence only, no production claim.

## Owner correction: checkbox catalogue; filter scope unresolved

Catalogue membership is now a staged checkbox selection across grouped metrics, applied together. Cancel leaves existing cards intact. Existing selected cards retain their IDs and local filters; new cards inherit report context. Per-card configuration remains a separate edit flow. Changed `MetricCatalogue.tsx`, `workspace.css` and existing component tests. Browser verified cancelling multi-selection, batch removal and batch addition against the local editor; no report was saved. [Catalogue screenshot](batch-metrics.png) inspected. Build, 24 test files / 117 tests, local grouped gate and whitespace check passed.

The broader owner request to restore Mindbox-style filtering remains OPEN. Investigation found the preserved runtime's advancedFilterCatalog (customer, order, product, communication and coverage conditions), while the live Card contract in `packages/contracts/presentation/workspace.py` accepts only local_store_ids with population/target bindings fixed to None. The reference calls for metric-capability-specific typed filters. A user question is pending on whether the next delivery is an explicitly identified design prototype or backend-connected filtering. No unsupported conditions were made to appear applied, and no extended filter implementation/completion is claimed. This follow-up completes only checkbox selection.

## Owner-selected filter design prototype

The owner resolved the preceding question by selecting a design prototype first, with calculation/persistence integration deferred. `FilterPrototype.tsx` adds a session-only builder to report Context and metric catalogue/configuration. Categories cover communications, customers, orders, products and coverage; fields use enum, boolean, text, number and date inputs with applicable operators. Groups and their conditions expose AND/OR logic, add/remove, reset and cancel. Metric conditions can inherit the prototype report conditions or be applied to all checked cards. Sample field/value status, absence of calculation/report-save effects and reset-on-reload behavior are explicit in the UI. The existing functioning store restriction stays separate in card configuration. No API, schema or database changes; no capability claim for the sample fields.

State is held in an in-memory session map keyed by workspace/report/card, separate from report DTOs, persistence, browser storage and query identity. Applying prototype conditions does not imply applying real report results. Nested same-order/subquery evaluation and metric-specific backend capability validation remain future integration work.

Build and 24 frontend test files / 117 tests passed. Browser flow verified report inheritance, a channel condition, numeric minimum order amount, OR between groups, applying conditions to all selected cards, switching metric and cancelling a reset. The interaction flow generated no API writes. It was repeated after final explanatory copy. [Wide](filter-prototype-wide.png) and [narrow](filter-prototype-narrow.png) screenshots record the design. An initial ambiguous Metrics selector was scoped to inspector navigation before the successful runs. Local grouped gate and whitespace check passed. Evidence is limited to local prototype interactions, with backend integration explicitly deferred.

## Owner follow-up: direct report period menu

The top calendar button now opens a shared anchored picker for new/legacy and configured reports, without routing through the inspector. It offers current/previous calendar week (Monday–Sunday), month, quarter and year, plus a validated custom inclusive date range. Presets use the browser's current local date. Selecting a period changes draft context only; existing Apply/Save semantics remain. The legacy adapter carries custom ranges through to its existing calculation request; configured reports update common_context dates without changing grain. Read-only/busy models cannot open the editor.

Changed `ReportPeriodPicker.tsx`, `PilotDocument.tsx`, `ConfiguredWorkspace.tsx`, `pilot-period.ts`, the production `pilot/runtime.ts` adapter, navigation styles and focused date tests. Preserved pilot document remains unchanged. Browser verified quick month and custom selection on `/reports/new/edit`, quarter/custom selection and Escape on an existing report. The initial test exposed stale legacy period-summary rendering; it was fixed and the scenario passed. [Menu screenshot](report-period-menu.png) inspected. Date tests cover Monday/year boundaries, leap February, previous year/quarter and exact custom dates. Build, 25 test files / 120 tests, local grouped gate and whitespace check passed. No report was saved; calculation execution and production delivery are not claimed for this UI correction.

## Owner follow-up: single inspector toggle

Removed the duplicate close icon from the configured inspector header in `ConfiguredWorkspace.tsx`. The existing global inspector button remains the open/close control; Escape remains supported. Frontend build passed. Local browser verified opening, absence of the inner close control, closing and reopening through the global button, and Escape dismissal. Local grouped gate and whitespace check passed. No report data changes or publication.

## Owner follow-up: automatic refresh without loading flashes

The owner accepted automatic result refresh instead of a global Apply action, with explicit report saving and delayed loading feedback. Configured and new/legacy reports now coalesce query changes for 150 ms and refresh automatically. Pending requests are serialized; configured results reject superseded generations, and legacy results reject mismatched query context. The loading indicator appears only after 400 ms, disappears on completion, and does not change the workspace layout. Configured charts and KPI values retain their previous result during replacement. Export and saving are blocked while the replacement is pending. Calculation errors retain a retry action.

Real store checkbox edits are staged locally with Show results/Cancel, so a multi-selection is submitted once. The expanded filter design prototype remains session-only and is not connected to calculation or persistence. Explicit Save remains responsible for report persistence. This supersedes the manual-Apply behavior recorded under the earlier period-menu follow-up.

Focused timer tests cover suppression for fast requests, delayed feedback, coalescing, serial execution and avoiding repeated retries for a failed key. The frontend suite passed (26 files / 122 tests); production build passed with the existing chunk-size warning. Local browser checks verified automatic prior-year comparison (+33.4% revenue), automatic new-report January 2025 calculation (43908.52), and a deliberately delayed real response: loading appeared, switching back to the saved context discarded the stale response and reused the saved result without another request. Initial delay harness attempts used an unavailable sandbox timer and then an incorrect two-request expectation; both were corrected before the successful run. No report was saved, no test data was replaced, and no publication was performed. Evidence concerns the local browser/runtime only.

Final verification: `uv run python -m tools.check --scope local` returned `PASS check:local (observed=true)`; `git diff --check` passed.

## Owner follow-up: report library

Implemented the owner-accepted UI-RPT-001 frontend reorganization under the [W40 ticket](../../tickets/W40-WORKSET-CATALOGUE-INTERACTIONS.md). ReportLibrary.tsx and report-library.css replace the mixed template/list surface with a table and a separate creation section. Actual saved_at values drive date filtering and sorting. Search and browser-local favorites combine with filters. Favorite IDs are scoped to workspace/principal; report payloads and authentication data are not stored. The list reads subsequent API pages rather than silently filtering only the first 50 reports.

Contract impact: compatible browser presentation change, unchanged API/persistence. Current list metadata lacks author/type and the configured client has no blank-create method. Author/type/Mine filters, report rename/copy/delete and blank creation remain unimplemented. Blank creation is explicitly disabled; the sales-template destination works. This is the first frontend implementation, not completion of every proposed capability.

Build and 27 frontend test files / 124 tests passed. Focused tests cover combined filters, immutable sorting and local-day boundaries. Browser checks at 1476x959 and 390x844 covered search, empty results, reset, date filtering, favorite persistence, section switching, reload/Back, Russian presentation, template and existing-report links. The initial harness needed a wait for asynchronous list loading. A subsequent run exposed route rejection of the new query parameter; router history state now preserves section navigation without changing the URL contract. Screenshot review found inherited numeric alignment, fixed with scoped styles before rerunning checks. Console check reported zero warnings/errors. Local grouped gate and whitespace check passed. No reports were saved/deleted/reseeded or published.

Visually reviewed: [library](library-ru.png), [creation](library-create.png), [narrow library](library-mobile.png). Narrow tables scroll within their container without page overflow. Favorites are browser-local, not synchronized between devices.

### Library creation entry correction

Removed the duplicate top-right creation button at the owner's request. The section-row entry now has a Plus icon and normal text contrast next to Library. Existing creation navigation remains unchanged. Removed unused primary-button styling.

Correction validation: frontend build passed; local browser verified absence of header creation, presence of the Plus icon, navigation to creation and back, and narrow-screen visibility. Local grouped gate and whitespace check passed. No report data changed.

### Library dropdown consistency correction

Both library selects now share the upper control's module background, border, 34px height and text spacing. A decorative Lucide ChevronDown replaces the native arrow, centered vertically with a 10px trailing inset; pointer events remain on the native select. Removed the sort-only transparent override. Frontend build passed. Local browser confirmed identical computed styles, zero vertical icon offset, both selections working and no page overflow at 390px. Screenshot visually reviewed. No data or filter semantics changed.

### Owner correction: control focus without outlines

The owner requested removing persistent focus outlines across controls and using a filled active navigation item. Added a shared control-focus.css, imported by the application entry and injected into the report iframe. Focus uses a surface fill (and link underline) instead of outline/shadow; forced-colors uses Highlight/HighlightText. The library's active rail now matches the existing neutral report-editor tile. Ordinary control borders and selected metric semantics remain intact. Main entry import is a necessary scope extension for the explicit application-wide request.

Build passed. Browser verified no outline/shadow on the library select after selection/focus and on the report iframe comparison select; active rail has neutral fill and no shadow; Tab navigation retains background feedback. This is focused runtime proof, not an exhaustive accessibility audit of all application screens. No report data changed.

### Owner correction: borderless controls across pages

The owner clarified that ordinary control/menu borders are prohibited too, across all pages and future iterations. The normative UI blueprint now records this rule. Shared shell/iframe CSS suppresses control strokes in default and interaction states, with background keyboard feedback. Supported browsers use customizable base-select popups to remove native picker frames; older browsers retain OS-controlled popup rendering, which CSS cannot fully override. Library selectors use a borderless shared dropdown with outside dismissal, Escape, arrows/Home/End and focus restoration. This replaces the earlier native-select styling, rather than claiming that focus-only removal met the request.

Validation: build, local grouped gate and whitespace check passed. Chromium supports base-select. Open library menu reports 0px border and no outline; selection, keyboard arrows/End/Enter, Escape and outside dismissal passed. Open-menu screenshot visually reviewed. Other routes inherit shared CSS; exhaustive all-page verification was not performed.

### Owner correction: sorting action menu

Replaced the persistent sort-value selector and adjacent decorative icon with one icon-only sorting button. The borderless contextual menu displays radio choices with the active order checked; title/accessibility label identify the action and current order. Shared LibraryDropdown retains its listbox mode for the period filter and exposes menu/menuitemradio semantics for the sorting action.

Build, local gate and whitespace check passed. Browser verified icon-only trigger, initially hidden menu, choice changes, checked current order, Escape and keyboard Home/Enter activation. Report data unchanged.

### Owner correction: consistent navigation dock

The library PilotFrame still used the preserved overlay layout, while report iframes used a grid dock. Extracted navigation-shell.css shared by both shells, with matching grid columns, panel/workspace top inset, height and corner radius. Opening navigation allocates a column rather than covering content; narrow layouts allocate a row above the workspace. Existing report-specific inspector styles remain in navigation-dock.css. No navigation destinations or report data changed.

Build passed. Browser checked library, new report and configured report at 1476x959: workspace moves right, panel never overlaps it, both start at y=8 and have height 943. At 390x844 the panel occupies a row above content without overlap. Library wide/narrow screenshots visually reviewed. Existing reduced-motion rule remains shared.

### Owner correction: compact export and no duplicate chart title

On 2026-10-03 reduced legacy chart/table export menus to content width with compact left-aligned rows. Removed the redundant revenue y-axis name in overviewOption, shared by normal/focus rendering; the enclosing chart heading remains. Preserved source HTML unchanged. Build passed. Browser on the real new-report route verified the opened export menu measures about 85x64px in English. The isolated page displayed a data-unavailable empty chart; waiting for a populated series timed out, so removal of the duplicate axis name is source/build-verified only, not verified against a populated chart in this run. Screenshot visually inspected. No report was saved or dataset changed.

## Unified creation and editing (2026-10-03)

Owner approved one editor for creation and editing. Expanded bounded ticket scope
covers native first Save; no publication or baseline test-data changes.

Implementation: `NewConfiguredWorkspace` resolves available dataset/default period
and prepares a native definition, then mounts the same `ConfiguredWorkspace` as
saved reports. Blank and sales-template entry points are enabled. First Save
creates a native personal draft and companion Saved View atomically; normal Save
and first Save share materialization/verification. Initial report identity and
save key survive normal retries; unsaved calculations create no report.

Requirements: REPORT-018 (creator-only editing), METRIC-025/026/027 (personal sets
and cards), I18N-001. Existing legacy base-reader and private-workset boundaries
remain; this does not implement publication or REPORT-019 shared-workset target.

### Contract impact

| Surface / consumer | Change | Classification / boundary |
| --- | --- | --- |
| Existing report operations and old stored documents on new server | Existing endpoints and exact legacy base preserved | compatible-change; both Original reports reopen at revisions 7/1 |
| New API / frontend | Prepare, calculate, first-save endpoints; shared editor; blank creation | compatible-change for current paired local frontend/backend |
| Native persisted definitions / old reader | Nullable legacy base for native personal drafts | breaking-change for rollback to readers requiring non-null base; retain upgraded reader after native writes |
| SQL schema / source dataset | Existing tables, no migration or source mutation | none |
| Access | Current actor, CSRF, functional/object/data scope + immutable creator | existing guarantees preserved for tested personal-draft flow; no shared native publication claimed |

### Observed verification

Target: local preview `localhost:41746`, real API workers 58160–58167 and existing
`custometry-w39-candidate-c67c` database. Isolated Playwright CLI session `w40`.

- Frontend typecheck/build passed; existing >500 kB bundle warning remains.
- Full frontend unit suite before final draft-retention refinement: 124 passed;
  new preparation/source-choice suite: 4 passed. Final totals recorded below.
- Presentation unit suite including native author/access/preparation/concurrent
  service interleaving: 34 passed; focused Ruff and Pyright passed.
- Real browser sales template: three cards 393,859 / 2,144 / 184 for
  2025-01-01–2025-11-30; first Save and reopen use the configured editor.
- Lost-response experiment: actual first Save succeeded, its response was replaced
  with a test-only 502. Retry returned the same report/version/revision 1; no
  duplicate document was created.
- Blank creation from library: empty metric set, first Save revision 1, reload
  retains empty state and title.
- Real API prepare leaves GET of the proposed report at 404. Four concurrent
  identical saves returned HTTP 200 and the same version/revision 1. Changed
  payload with the same key returned HTTP 409 `IDEMPOTENCY_CONFLICT`. Missing
  CSRF returned 403; forged creator returned 400 without saving.
- Original reports remain title `Original`, revisions 7 and 1, HTTP 200; their
  source dataset remains the same `224ffe86-71ab-510e-9ae7-1f2ab10d39ff`.
- Independent read-only review found a first-save replay race and stale generated
  reports-client nullability. Both corrected; locked concurrent replay was then
  exercised above. Review also identified the documented native personal-draft
  reader/rollback boundary. No access bypass found by that static review.

During verification, an initial unsaved calculation hit NOT_FOUND because a scope
recheck still queried persisted report metadata; fixed to use the already-bound
creator while retaining access resolution. One later browser attempt expired its
session (401); the protected UI cleared data. Reauthenticated and resumed focused
verification. These failed attempts are not counted as passing proof.

Final verification on the delivered source:

- `corepack pnpm --filter @custometry/web test`: **128 passed / 28 files**.
- `corepack pnpm --filter @custometry/web build`: **passed**, TypeScript + Vite.
- `uv run pytest -q tests/unit/presentation`: **34 passed**.
- Focused Ruff and Pyright for changed Presentation/API code and new tests: passed.
- `uv run python -m tools.check --scope local`: **PASS (observed=true)**.
- `git diff --check`: passed.
- Editing the newly saved blank report: added all three metrics, enabled prior-year
  comparison, saved revision 2, reloaded; cards and comparison retained. Observed
  at 1480×969 and 400×900: [desktop](unified-editor/desktop.png),
  [narrow](unified-editor/narrow.png). Narrow view retains horizontal card scrolling
  and reachable Save; no new focus border styling introduced.
- Repeated lost-response browser experiment after final identity/key changes:
  two HTTP 200 server saves with identical report ID/key, both revision 1.
- Independent follow-up confirmed both actionable review findings resolved; no
  remaining blocker in the bounded native personal-draft creation flow.
- Deleted exactly four task-created QA documents (including their versions/views)
  using explicit IDs and expected title guards. Existing document rows and source
  artifacts were not altered. Original revisions remain 7/1. Immutable QA result/
  snapshot artifacts are retained under the existing artifact lifecycle; no broad
  artifact deletion or database reseeding occurred.

Local preview and API remain running. This evidence establishes local paired
frontend/backend behavior, not production release or shared native publication.

## Direct inspector catalogue (2026-10-03)

Owner-approved follow-up under W40 and UI-RPT-002: expose available metrics
immediately instead of presenting only an empty selected list. The inspector now
shows the dataset label, grouped checkboxes, search across available metrics,
select matches/all and deselect all. Individual changes use the existing draft
and automatic calculation. Order and per-card settings remain in a collapsible
section, without a decorative border. The central empty-state action opens this
same catalogue. Source-name lookup uses the existing report context API.

Loading reserves space and only shows text after the existing delay. Retryable
catalogue failure, no available metrics, no search matches and no selected metrics
have distinct states. Extended filter editing remains the existing marked
prototype; this change does not expand backend filter capabilities.

Contract impact: compatible browser behavior change; no API/schema/data change.
The [UI blueprint](../../../../custometry-ui-blueprint-ru.md) records the updated
inspector contract, superseding the earlier add-metric modal behavior.

Validation:
- Frontend tests: **132 passed / 29 files**. Updated old modal expectations to
  direct selection and retained settings-cancel protection. Added reference/
  inheritance, search, capacity, delayed loading, retry and empty-state coverage.
- TypeScript/Vite production build: passed; existing bundle-size warning remains.
- Local browser against the running API: library -> blank report -> Add metrics
  exposes all three checkboxes and Northwind Retail immediately. Revenue and
  receipts selected directly; average receipt selected through catalogue search.
  Automatic calculation produced 393,859 / 2,144 / 184 for Jan–Nov 2025.
- Inspected layout at 1480x969 and 400x900:
  [desktop](inline-catalogue/desktop.png), [narrow](inline-catalogue/narrow.png).
  Final collapsible settings computed border=0px, box-shadow=none.
- Existing Original report opened without edits: same catalogue, selected states
  and source label. No reports were saved/created during this check; the local
  unsaved QA draft was discarded. Dataset and existing report versions unchanged.
- `uv run python -m tools.check --scope local`: PASS (observed=true).
- `git diff --check`: passed.

Proof boundary: local frontend and real API success flow; failure/empty/loading
states covered by component tests, not real provider outage experiments. No
production publication performed. Local preview remains available.

## Select value alignment repair (2026-10-03)

Owner-reported UI-RPT-002 comparison/display values sat at the top of their
controls. Browser evidence showed `appearance: base-select`, flex layout,
28px height, zero vertical padding and `align-items: normal`. The shared
base-select rule now centers its selected value and picker icon vertically.
This applies to the application and report iframe without changing selection
behavior or adding strokes. Browser inspection confirmed both controls use
`align-items: center`; a focused control retains `outline-style: none` and
`box-shadow: none`. The toolbar screenshot was visually inspected. Production
build, local gate (`PASS`, observed=true) and `git diff --check` passed. No new
behavioral tests were needed for this CSS-only repair; data was not modified.

## Active context navigation stroke removal (2026-10-04)

Owner requested background-only active context navigation. The shared control
stylesheet now removes the legacy inset accent shadow on current context links
in both host and report iframe. Browser checked Customer base in the Analytics
dock: box-shadow=none, border-width=0px, outline-style=none, background remains
rgb(36,37,41). Dock screenshot visually inspected. Build, local gate and
`git diff --check` passed. CSS-only repair; data and navigation behavior unchanged.

## Metric card title background repair (2026-10-04)

The title action inherited generic control hover/focus fills and a 28px minimum
height inside a 20px card row. Shared control styling now keeps this stretched
action transparent in every state and sizes it to its row. Keyboard focus uses
the whole card surface instead of a separate title pill. Browser verified hover
and focus on all three metric titles: transparent background, height 20px,
outline-style none. Card strip screenshot visually inspected. Build, local gate
and diff whitespace check passed. CSS-only repair; no report/data mutation.

## Report creation entry simplification (2026-10-06)

Owner requested “New report” instead of “Blank report” and temporary removal of
the receipt-sales template card. Library RU/EN headings and action labels now
reflect new-report creation; template-specific introductory/empty-library copy
was removed. The existing blank editor route is retained. UI blueprint updated.
Browser verified exactly one creation card, New report / Create report, and
successful navigation to the unified editor without selected metrics. Build,
local gate and diff whitespace check passed. No saved reports/data changed.

## Structural editor regrouping (2026-10-06)

Owner request `CUSTOMETRY-REPORT-EDITOR-STRUCTURAL-REGROUPING` v1.0, executed as
an authorized follow-up to the [existing W40 unit](../../tickets/W40-WORKSET-CATALOGUE-INTERACTIONS.md).
Requirements: UI-RPT-002, METRIC-025…028, METRIC-030, REPORT-018/019, A11Y-001,
I18N-001. Canonical structure: [UI blueprint](../../../../custometry-ui-blueprint-ru.md#editor-structural-regrouping-2026-10-06).

Baseline is the existing dirty working tree, not HEAD. Listener PID 59159 at
localhost:41746 was verified with lsof/ps to serve Vite preview from
`/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry/apps/web`.
Builds update that checkout's preview output. Other edits and MS-004 journal
remain untouched. Existing browser session w40, viewport 1280x720, was reused;
its original new-report tab was preserved. Evidence uses additional tabs.

### Control relocation map

| Baseline | Target | Preserved owner/behavior |
| --- | --- | --- |
| Title, status, Save, actions, inspector | Header | Same title, save/reload, inspector handlers and dimensions |
| Report-view menu beside dates | Header | Existing report-view/locale commands |
| Page tabs and all context chips in one row | Tabs only, then compact data-context row | Page identity and unavailable-page guards |
| Period chip | Data context | Same ReportPeriodPicker and automatic refresh |
| Upper comparison shortcut plus chart select | One card-scoped temporal select in data context | Same selection.temporal; shortcut was focus-only alias |
| Store shortcut | Filters entrypoint | Same context inspector and common store restriction; no invented channels |
| Workset bar, catalogue count, add, overflow | Immediately above cards | Unchanged WorksetControls and catalogue handlers |
| Card rail | Between worksets and visualization | Byte-unchanged CardRail JSX; no card CSS changes |
| Series/delta and period differences | Contextual View | Same display and differences state; differences chart-only |
| Grain and calendar basis in inspector | View, or inspector for empty sets | Same server query controls, no new grouping dimensions |
| Pair-comparison button always disabled until selection | Visualization toolbar when cards selected | Same two-card selection and handler; temporal and pair scopes remain distinct |
| Chart/table and separate export/fullscreen row | One toolbar immediately above result | Same renderers, ResultExportMenu and Focus handlers/export scope |
| Disabled goals/shared placeholders | Set-inspector availability note | No invented capabilities |
| Empty appearance popover | Omitted | Existing renderReportReadabilityControls returns early for workspace; no operative control removed |

Report common store IDs, card local store IDs and bulk-store restrictions are
not duplicates: they retain their own inspector scopes and inheritance rules.
No separate implemented report-wide temporal spec or chart-local inheritance
control exists in this configured editor. Palette/text size, legend/grid and
channel filtering remain capability gaps; no renderer/API expansion was made.

### Compatibility and focused correction

Browser control location: compatible-change for shared create/edit consumers;
handlers, cards, results and persistence are preserved. API/DTO, persistence,
request/cache identity and backend calculation: none (no changes). The View
popover uses native top-layer positioning and Tab navigation, Escape dismissal
and trigger focus restoration, with the existing background focus treatment.

The browser exercised temporal delta followed by comparison None and observed
POST apply 422. The pre-existing handler retained delta_trend while setting
none; SingleSelection.delta_requires_temporal rejects exactly this combination
with DELTA_REQUIRES_COMPARISON. The moved ReportComparisonControl now restores
series when comparison is removed; delta is unavailable without comparison.
This is a narrow compatible client-side correction to produce valid existing
contracts. Unit coverage checks both directions; browser regression is recorded
below. No backend change or saved fixture mutation.

### Verification

- Final focused frontend run: 45 tests across 10 files passed, including new
  comparison validation and View focus/mode tests, automatic refresh, creation,
  catalogue/worksets, period, store scope, projections and exports. An earlier
  broader run passed 134 tests; the final focused run includes the later repair.
- `pnpm --filter @custometry/web build`: passed (TypeScript and Vite). Existing
  large-chunk warning remains; no bundle-size/performance claim.
- `source scripts/activate-toolchain.sh` then `uv run python -m tools.check --scope local`:
  PASS, observed=true. `git diff --check`: passed.
- Browser: revenue/receipts/average switching; card checkbox selection and pair
  comparison; settings inspector; temporal comparison, differences and delta;
  delta-to-none regression; day/week aggregation; January 15/31 custom ranges
  with successful automatic apply; chart/table switch; CSV and SVG downloads;
  fullscreen/Escape; View initial focus, Escape restoration and mode-specific
  differences availability. No fixture report was saved or reseeded.
- Direct new-report editor: saved a separate QA report
  `2ff44f72-36e6-4d33-af75-ee9aa9b0b268` titled
  `QA structural regrouping 2026-10-06`; full reload retained its name and shared
  shell. The QA report is retained. Library Create report opened an empty set;
  selecting Net revenue in the catalogue displayed one unchanged card and View.
- RU/EN switching and the Russian View entry were observed. Baseline/final
  captures use the same English desktop session at 1280x720.
- Card JSX is byte-identical to the pre-edit working copy. Browser CSS comparison
  was also identical for all three cards: 260x124, 8px padding, 10px radius,
  font, selected/unselected backgrounds and borders, values 43,909 / 210 / 209.
- Widths 1920, 1280 and 768 were exercised with both navigation and inspector
  open. Document scrollWidth equaled viewport width. Navigation reserved width:
  workspace starts after the nav right edge (8px gap). Existing narrow inspector
  mode remained in place. View bounds stayed within the viewport. Final screens
  were visually inspected; no new overlap or unintended toolbar wrapping found.
- One apply 422 was observed before the comparison correction. The corrected
  sequence completed; the final reloaded editor's console had 0 errors/warnings.
  No new backend capability or production state was inferred from this browser run.

Final evidence: [chart](structural-regrouping/after-chart.png),
[table](structural-regrouping/after-table.png),
[View menu](structural-regrouping/after-view.png). Baseline chart/table/inspector,
card computed-style comparison and narrow-panel captures remain in local scratch
under `/Users/daniildegtyarev/.codex/visualizations/2026/10/06/01a111ea-1459-7eb1-9209-94c7004145f5/regrouping`.

Not tested: every export format (PNG/XLSX), every calendar/grain combination,
full assistive-technology conformance, mobile widths below the accepted 768px
boundary, or production delivery. Unit coverage includes both export serializers;
that does not substitute for unperformed browser downloads.

Documentation synchronization: existing ticket/evidence links remain reciprocal;
the UI blueprint links this follow-up and the ticket links back to its hierarchy.
No new plan, pack, stage state, dependency or public contract version was created.
Machine/human product requirements, accepted pilot bytes and ADR-0007 are unchanged:
this is authorized composition plus a valid-selection guard, not new semantics.
No publication or deployment. Local runtime verification passed for this scope;
owner acceptance is not inferred.


### Filters toggle follow-up (2026-10-06)

Owner browser comment requested symmetric opening/closing through Filters. The
shared configured editor now closes an already active Context inspector on a
second Filters activation, and switches other inspector sections to Context.
The trigger exposes matching aria-expanded and aria-controls. Existing report
filters and values are unchanged. Browser proof at 1414x959 verified open, close,
Metrics-to-Context switching, and Enter-to-close; console: 0 errors/warnings.
TypeScript/Vite build, local gate and diff whitespace check passed. Canonical UI
blueprint synchronized. No report save or data mutation was performed.


### Inspector tab naming (2026-10-06)

Owner requested renaming the inspector tab from Context / Контекст to
Filters / Фильтры to match its entrypoint. Only the visible tab label changed;
internal context identity, panel contents and toggle behavior are preserved.


### Local comparison recovery (2026-10-07)

Owner reported access-denied UI after enabling comparison on the retained QA
report `2ff44f72-36e6-4d33-af75-ee9aa9b0b268`. After local restart, GET report
returned 200 while POST apply returned 403 at `http://localhost:41746`. The
task-only `scripts/w39-serve.py` origin allowlist contained 127.0.0.1:41746 but
not localhost:41746. Source tracing showed mutation origin validation and the
frontend fail-closed handling of 403; the response error body was unavailable
through the browser tooling. Added only the exact localhost origin and restarted
the owned API; application authorization and CSRF validation are unchanged.
Contract impact: compatible-change to task-only local runtime configuration.

Browser verification using playwright-cli session compare-fix: comparison none
to previous_year_same_dates returned apply 200 and results 200; cards displayed
year-over-year values and the chart displayed both series. Disabling comparison
and switching to the table remained available. No report save or dataset reset.
[Comparison screenshot](structural-regrouping/comparison-origin-fixed.png).
Local gate passed: `uv run python -m tools.check --scope local`. Independent
source review of the exact origin addition passed; no wildcard, bypass or
non-loopback API listener was introduced. Frontend build/tests were not rerun
because no frontend source changed in this recovery. Production is untested.


### Compact metric cards (2026-10-07)

Owner explicitly superseded the earlier card-dimension preservation constraint
with a request to make the highlighted metric cards more compact. Only local
card layout in workspace.css changed: columns 260 to 220px, height 124 to 106px,
vertical padding 8 to 4px, row gaps 4 to 2px, title row 20 to 18px. Font sizes,
colors, icons, controls, JSX, state ownership and handlers are unchanged.
UI-RPT-002 canonical inventory synchronized; shared create/edit CSS remains one
implementation. Contract impact: none to API/persistence/calculation semantics.

Browser proof on the served c67c checkout at localhost:41746: measured all three
cards before at 260x124 and after at 220x106. At 1414x959, temporal comparison
rendered values and both chart series; metric switching, checkbox selection and
card settings opening passed. At 1024x959 with inspector open, the 562px rail
scrolls 680px of cards; no vertical card overflow or document horizontal overflow.
Console: zero errors/warnings. No report was saved.
[Final desktop capture](structural-regrouping/compact-cards.png).

Validation: 24 existing tests passed across workspace-presentation,
new-configured-workspace and report-comparison-control; frontend typecheck/build
passed (existing chunk-size warning); local gate and diff whitespace check passed.
No CSS-mirroring test added. Browser exercised the saved report in English;
Russian copy, 200% zoom and the create route were not separately browser-tested
in this follow-up. No publication or production verification.


### Compact authoring blocks (2026-10-07)

Owner requested clearer grouping across navigation, context, sets, cards and
result controls. ConfiguredWorkspace now groups the existing workset toolbar,
number note and unchanged CardRail inside the workset section. Result controls
remain with their renderer. Local workspace.css uses the existing surface token
for the context row, metric block and result toolbar, with a result-header divider
and 12px inter-block spacing. Empty alert slots no longer consume a grid row;
redundant page padding and the context top rule were removed. No new control,
renderer, state owner or handler. UI-RPT-002 inventory synchronized. Contract
impact: none to APIs, persistence or calculations.

Browser: playwright-cli blocks, served c67c checkout at localhost:41746, Russian
locale, desktop 1414x959. Sets disclosure, chart/table switching, View opening and
Escape closing, card settings inspector opening passed. Cards remain 220x106.
At 1024 and 768 widths no document horizontal overflow was observed; card rail
retains horizontal scrolling. New-report route also rendered the shared shell.
No report save or dataset mutation. Final editor console: zero errors/warnings;
two earlier asset errors occurred during preview rebuild and disappeared after
full navigation. Downloads, save/reopen and full keyboard/zoom coverage were not
retested for this layout-only change.

Captures: [chart](structural-regrouping/blocks-chart.png),
[table](structural-regrouping/blocks-table.png),
[View](structural-regrouping/blocks-view.png).
Validation: 30 existing frontend tests passed across four focused suites;
TypeScript/Vite build passed with existing chunk-size warning; local gate and
diff whitespace check passed. No publication or production delivery.


### Owner correction: one horizontal control axis (2026-10-07)

The owner clarified that the previous vertical blocks did not meet the request.
That composition is superseded: Data, Set & metrics, and Result view now occupy
three adjacent blocks above the metric cards. PilotDocument provides portal
slots for the existing WorksetControls and visualization toolbar, preserving
state and event handlers in ConfiguredWorkspace. The separate toolbar below
cards and previous metric-block background were removed. Card interiors and
result renderers are unchanged. No API/persistence/calculation contract change.

Browser proof: Russian locale, same retained report, 1414x959: all three blocks
start at y=124 with distinct x coordinates. Sets disclosure, chart/table, View
and Escape, temporal comparison, fullscreen and Escape worked. At 1024px the
three groups still fit; at 768px they wrap whole groups into two rows without
horizontal overflow. At 1024px with the modal inspector open, the relocated
command row is inert; closing restores access. Final console: zero errors or
warnings. No save or reset. [Final capture](structural-regrouping/horizontal-controls.png).

30 existing focused tests passed; typecheck/build passed with existing chunk
warning; local gate and whitespace check passed. Build was repeated after the
small inspector-inert adjustment and that behavior was browser-tested. Export
downloads, save/reopen and the new-report route were not rerun in this correction.
Canonical UI-RPT-002 inventory synchronized; no publication or deployment.


### Content-sized toolbar refinement (2026-10-07)

Owner rejected the stretched three-container appearance and authorized a compact
professional toolbar. Replaced fractional grid columns with content-sized flex
groups, removed group backgrounds and visible captions, kept subtle vertical
separators and centered controls on a common horizontal axis. Group names remain
accessible through aria-labelledby and visually hidden labels. Data context no
longer forces comparison onto its own row. Cards, handlers and result renderers
are unchanged; no API or persistence contract impact.

Browser: Russian, retained QA report at localhost:41746. At 1414x959 all groups
fit one row including prior-year comparison. At 768x959 groups wrap without
command-row or document overflow. Sets menu, comparison, chart/table, View and
Escape passed; final console zero errors/warnings. Build and typecheck passed
(existing bundle-size warning); eight focused menu/workset tests, local gate and
whitespace check passed. Prior broader tests were not rerun for these CSS/label
changes. No save, reset, publication or production checks. Canonical UI inventory
synchronized. [Final screenshot](structural-regrouping/compact-toolbar.png).
