---
doc_id: ARCH-UI-WEB-IMPLEMENTATION-SOURCE-001
title: Custometry Web implementation source contract
doc_version: 28
product_spec_version: 0.11.0-draft
ui_spec_version: 0.9.0-draft
visibility: internal
ship: false
owner: engineering
requirement_ids: [WEB-ARCH-003, WEB-ARCH-004, WEB-ARCH-005, WEB-ARCH-006, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, A11Y-001, I18N-001]
status: active
proof_boundary:
  label: repository-web-implementation-routing-and-reference-contract
  exclusions: [product-runtime-readiness, browser-acceptance, release-readiness]
---

# Custometry Web implementation source contract

## Accepted initial composition — 2026-09-17

The owner accepted the [metric-workspace composition](drafts/metric-workspace-v1/README.md),
version 4 (editorial navigation update), as the starting baseline for worksets, configured cards, comparisons
and goal placement. Preserve the current native-pilot implementation as the
foundation. This addition governs the demonstrated new report surfaces; the
original pilot governs the shell and unaffected surfaces. The prototype does
not establish backend contracts. [WS-003](../planning/directions/DIR-004/workstreams/WS-003.md)
records the accepted order and all twelve product choices. C01 must implement
all six grains and creator-only report editing; C02/C03 own the added goal/shared
behavior. Exact L3 contract decisions remain to be fixed. Both UI affordances
and backend mutations enforce REPORT-018; reader filtering is not authoring.
New owner requirements may amend the baseline; synchronize affected sources and
the selected execution unit without treating the old document as a product veto.
Settle overlapping card/context/chart/persistence changes before final polish.
Develop and verify locally. MS-003 S05/S06 are deferred in the canonical journal;
container packaging and delivery qualification require a separate selected task.

## Decision and execution authority

The owner-selected [2026-09-17 metric interaction atlas](references/mindbox-metrics-2026-09-17/README.md), version 1, adds future workset/card/comparison/goal requirements (blueprint requirements revision `2026-09-17.1`). It supplies ten source screenshots for those added behaviors. The preserved pilot still governs its demonstrated elements; this addition neither replaces its shell nor changes the current route capability inventory or accepted milestone execution authority.

On 2026-09-04 the owner selected the final interactive pilot as the target UI
concept and authorized removal of the G0-G6 program and generated materials.
The [retirement record](ui-program-retirement.md) identifies the exact historical
commit and recovery boundary. Deleted boards, prompts, ledgers, suspension
markers, and stage receipts are no longer active dependencies.

The owner adopted [hierarchical planning](../planning/framework-v1/README.md)
on 2026-09-06 for all development directions, including Web. New milestone work
uses the accepted plan, prompt pack and one canonical iteration journal; separate
bounded tickets retain their declared status authority. A graph is topology only.
The retired G0-G6 program, certification layers and historical ledgers remain
inactive; adopting the new framework does not restore them. Existing product,
visual-source and browser-proof requirements below remain unchanged.

## Source precedence for implementation

Read only the smallest applicable set:

1. `custometry-technical-blueprint-ru.md` and its synchronized human mirror
   for normative business semantics, contracts, and requirement IDs;
2. `custometry-ui-blueprint-ru.md` and executable route/surface contracts for
   surface identity, roles, states, permissions, and responsive intent;
3. the [target pilot](target-pilot/README.md), its byte-pinned entrypoint and
   decision notes for the demonstrated composition, navigation, analytical
   controls, interactions, density, and visual language, plus the accepted
   [metric-workspace composition, version 4](drafts/metric-workspace-v1/README.md)
   for its explicitly added report surfaces;
4. accepted architecture, especially ADR-0007, for production technology and
   dependency boundaries;
5. production code, focused tests, and observed browser evidence for the
   current implementation and its gaps.

The pilot is a target concept, not merely a visual-language anchor. Its
demonstrated structures and interactions should be implemented faithfully.
It is also a fixture-backed prototype: it neither changes backend contracts
nor proves production API, persistence, permissions, accessibility, or responsive
readiness. Screens not shown in the pilot retain their product requirements;
derive coherent patterns from the pilot without forcing every screen into the
same composition. Resolve a material conflict or a non-derivable product/design
decision with the owner before implementation.

The existing frontend remains working implementation evidence. Removing
the design program does not roll it back or certify its conformity. Alignment
to the target concept is subsequent, bounded implementation work.

## Execution unit and proof contract

Every Web implementation unit (ticket or milestone stage) names exact screen or surface IDs, requirement
IDs, user-visible outcomes, dependencies, and safely separable path ownership.
It produces working production UI, focused automated tests, and real-browser
evidence for the changed boundary. Design-only boards, broad pre-implementation
state matrices, or copied program receipts do not satisfy a ticket.

Browser proof covers critical changed states, relevant en/ru behavior,
keyboard/focus and accessibility smoke, console/network failures, and responsive
Web endpoints. Use 768 CSS px and 1920 CSS px as required endpoint anchors
when applicable, adding intermediate widths only when layout risk or a declared
breakpoint warrants them. This is boundary-matched smoke, not a claim of full
WCAG conformance or exhaustive every-state-by-every-anchor coverage.
Mobile-specific design remains unauthorized.

Each browser-depth execution unit (ticket or milestone stage) owns a Playwright
configuration below its declared `tests/e2e/<unit-slice>/` path. It uses Playwright's `webServer` lifecycle to
start host Vite on an explicit loopback port, wait for readiness, fail on startup
error, and clean up. It discovers only unit-owned specs and declares desktop
Web projects for `768x1024` and `1920x1080`; it does not depend on a pre-existing
`CUSTOMETRY_BASE_URL`, reuse the historical foundation-only config, or enable
a sub-768 mobile project.

Evidence is written once at the implementation boundary. Source checks do not
prove browser, API, persistence, Compose, release, or production behavior.
Publication and deployment require explicit authority.

## Existing topology and next work

The existing dependency/path topology is
`.codex/delivery/graphs/custometry-web-implementation-frontier-v1.json`.
Read live ticket frontmatter and accepted dependency evidence before choosing
work; the graph's existence is not a declaration that W31 or any successor is
ready. Historical ticket evidence describes its original implementation basis,
not acceptance against the newly selected target concept.

Plan remaining cohesive product slices through the framework with the owner; execute the selected milestone or independent-ticket route.
This cleanup does not activate a new W39 frontier or implement a UI redesign.

## First-run entry increment — MS-002-S03

The root `/` now composes the installation entry directly, outside the legacy
workspace shell. Its shared `pilot-entry/v1` primitives live in
`packages/ui-foundation/src/installation.tsx`; existing theme IDs and feature
routes retain their previous behavior. The preserved FoundationHome remains a
compatibility source, not an accepted target design.

The entry inherits the pilot's graphite palette, 17px heading, 14px base type,
10px panels, 7px controls, cyan primary action and 2px focus treatment. Its
720px single-column status composition is derived for an installation with no
workspace, rather than copying the pilot's report/navigation composition.
The typed operational adapter consumes S02 status including HTTP 503; Query
owns refetch/cancellation and hides retained successful data after errors.
Public help is linked by localized catalog URL. No account or domain truth is
stored in the browser.

[Stage evidence](../../../.codex/delivery/evidence/MS-002/MS-002-S03/report.md)
separates host-Vite/real-API behavior from normalized source comparison. S04
must package these sources with S02 API in a new identified bundle; S05 retains
the owner's final visual decision. This does not expand product-route coverage.

## Bounded report workspace — MS-003-S04

The current capability inventory below narrows the `implemented` marker in the
[route registry](../../../packages/contracts/routes/ui-routes.json) and
[execution contracts](../../../packages/contracts/routes/ui-route-contracts.json).
Those markers identify a working bounded route, not completion of every target
capability on that screen. Route identities and workspace-aware path/query shapes
are unchanged; the prepared access details supply the workspace UUID.

| Route | Implemented capability | Deferred target capability |
|---|---|---|
| UI-AUTH-001 | Real ordinary-analyst email/password session, workspace identifier, RU/EN, failure/re-entry | Password recovery, remember-device settings, administrative setup |
| UI-RPT-001 | Authorized saved-draft library and supplied sales template | Publication, delivery scheduling, arbitrary templates |
| UI-RPT-002 | Title, source version, dates, Store, same-date previous-year comparison; explicit Apply and CAS Save | Block builder, segments, product/customer analysis |
| UI-RPT-003 | Exact saved draft/page preview, canonical SVG line and full accessible tables, Result Trust, Focus | Published reports, email/XLSX/export, full renderer certification |

[The implementation](../../../apps/web/src/features/reports/ReportWorkspace.tsx)
now hosts the actual preserved pilot document. The owner explicitly rejected
both the first adaptation and the subsequent CSS-based recreation, and required
using the pilot itself with real APIs. [Current integration evidence](../../../.codex/delivery/evidence/MS-003/MS-003-pilot-native/report.md)
records this correction; earlier S04 receipts and correction captures remain
historical and do not establish current fidelity or owner acceptance.

A deterministic generator takes the byte-pinned HTML, CSS and SVG unchanged,
removing executable script tags only. It compiles the original presentation
runtime with explicit data/persistence seams. No replacement JSX report layout
is used. A same-origin document island isolates original selectors, CSS globals,
focus and native popovers. React remains the route/session owner; a typed port
carries model snapshots and actions into that document. TanStack Query and the
existing generated clients own all backend access. Server payloads never become
HTML, scripts, callbacks or arbitrary ECharts options. The bridge escapes text,
validates canonical references, compiles the server series and applies the
pilot's original chart presentation functions.

Original report elements, including eight KPI positions, the second table panel,
full contextual navigation, menus, inspector and Focus, remain in the document.
Three supplied receipt metrics replace their corresponding value slots; other
customer metrics are unavailable. Unsupported comparisons, segmentation,
publication and export cannot claim backend success. Fixture values are cleared
from the generated data declarations. Pilot browser-storage access is replaced
with ephemeral presentation preferences; it cannot store result truth.

The source title element edits the report title; source context controls drive
Apply; the original view-menu action drives Save, and the inspector's saved-view
row opens the exact draft preview. New report labels/data semantics still come
from the accepted receipt-total scope. Login and library have no complete source
pilot screen and retain their separately bounded implementations.

TanStack Query owns server results, drafts and versioned projections. Component
state holds only unsaved controls/presentation; a session-scoped memory map retains
unsaved inputs across history navigation. Only locale preference enters
localStorage. Authorization failure clears protected queries and draft memory,
hides protected content, and rejects late responses from the previous generation.
A 409 retains input and offers explicit reload. Apply never silently replaces a
saved snapshot; Save pins the calculated result. Exact reopen validates the page
locator and reads immutable artifacts without calculation.

[Stage evidence](../../../.codex/delivery/evidence/MS-003/MS-003-S04/report.md)
records real host Vite/production API/owned PostgreSQL/artifact browser proof,
RU/EN at 768x1024 and 1920x1080, keyboard/Focus and 200% layout zoom smoke.
This source increment does not certify packaged HTTPS, full accessibility or
complete design-system fidelity; S05 packages it and S06 retains owner review.
User-facing [report help](../../../docs-site/docs/user-guide/reports.md) explains
entry details, Apply/Save and recovery without backend implementation jargon.


## MS-004 S03 API handoff to Web integration

The [configured report contract](../../contracts/analytical-authoring-contract.md#ms-004-s03-guarded-api-and-configured-report-persistence)
and [S03 evidence](../../../.codex/delivery/evidence/MS-004/MS-004-S03/report.md)
provide real guarded API and persistence inputs for S04. Use generated
`packages/contracts/src/workspace-client.ts` and `workspace-contracts.ts`; external
paths are `/api/reports/v2` and `/api/analytics/metric-workspace/v2`. The editor
returns an exact version plus current capabilities and companion-view revision.
Preserve the current native pilot and typed bridge; no S03 change implements Web UI.

Apply is explicit and Save consumes its exact verified bindings and chart payloads.
Display-only creator changes can pass `reuse_result_ids` to verify existing results
without compute permission. Handle the typed error envelope, both CAS revisions,
private reader base/own-view boundaries, pinned calendar versus current default,
and explicit creator adoption. Server-projected numbers/comparisons remain the
sole chart/table/tooltip values. A rejected Save must retain the user's draft.
S04 supplies its own real-API browser harness; S05 consumes it. API tests are not
browser/fidelity/accessibility proof or acceptance of the finished milestone.


## MS-004 S04 native workspace integration

`ConfiguredWorkspace` composes the existing `PilotDocument` through its typed
bridge and a React portal in the preserved overview. The original document,
SVG assets, shell and navigation remain the source; maintained `port-epilogue.js`
and `workspace.css` implement new seams and the generator owns `runtime.ts`.
Worksets and the card rail share the docked Set/Card/Chart/Context inspector.
The narrow inspector has keyboard containment and Escape returns to its opener;
Focus provides the same chart and accessible table with focus return.

Generated v2 clients own transport contracts. TanStack Query holds editor,
view and verified result projections; local state holds unsaved inputs.
The result reader verifies manifest and metric bindings before rendering.
Server buckets, temporal projections and comparisons supply values and deltas;
localization formats them without recomputing business metrics. Card order and
labels preserve result identity; changes to query or calendar require Apply.
Display-only creator Save uses verification-only preparation; reader Save uses
existing verified bindings without requiring a calculation or creator capability.
Selecting a Saved View restores its query, display, pinned calendar and results.

The 2026-09-22 owner correction removes report-mounted financial-calendar settings,
current/pinned version controls, adoption and the associated calendar GET.
Administration navigation reports unavailable; no settings page is added. Once-only
company calendar setup belongs to administrator-only company settings and remains
a deferred lifecycle requirement. Existing backend pins and exact results remain.
See the [owner amendment](../../../.codex/delivery/evidence/MS-004/MS-004-S05/owner-correction-2026-09-22.md)
for the explicit mapping that supersedes the original D04/D08/AC-11 UI clauses.
A failed Save retains the draft; authorization-generation checks also reject a
late response body decoded after logout or session replacement.

[S04 evidence](../../../.codex/delivery/evidence/MS-004/MS-004-S04/report.md)
records the real local API/browser boundary and reproducible task-owned harness
at `tests/e2e/ms-004-workspace/`. S05 consumes it for complete AC-01…11 coverage
and owner acceptance. This increment does not establish packaged runtime,
release readiness, shared-workset behavior or goal implementation.


## MS-004 S05 integrated projection and keyboard proof

The same native document and typed bridge remain authoritative. Saved personal
views consume their persisted comparison rather than dropping it on reopen.
Temporal series keep their prior-year identity; chart/table/tooltip/Focus expose
the same server values, deltas, mapped dates and unavailable reasons. Older pair
views with no verified comparison keep independent card values and require an
explicit Apply/Save for the comparison, without browser arithmetic.

Initial inspector focus follows actual iframe-portal mount. The bounded browser
checks exercise initial Tab/Shift+Tab containment, Focus, Escape and return, plus
RU/EN and 1920/768/400 viewport classes. The maintained real fixture and added
`parity.spec.ts` bind fiscal multi-workset/store comparisons and exact snapshots
to actual API/artifact values. See [S05 evidence](../../../.codex/delivery/evidence/MS-004/MS-004-S05/report.md).
The journal alone records final owner acceptance; this is not application-wide
accessibility certification, a new visual concept or release qualification.

S05 also invalidates obsolete Apply completions on context edits, saved-context
reload and own-view selection. Actual production-response transport-delay tests
cover revocation during JSON decoding and reload during Apply. Save retains its
own commit lifecycle; reload/view switches are unavailable until Save finishes.
Unit labels and metric headings use the same RU/EN dictionaries across legend,
axis, tooltip and table; canonical artifact units remain locale-neutral.

The configured Focus surface respects the native rail width through `--sidebar`;
its close control remains inside the visible workspace. Result tables retain
intrinsic column widths with horizontal scrolling so exact dates and metric labels
are readable instead of inheriting the pilot's compact fixed-column ellipsis.


## W39 report entry and session lifecycle

The independent [W39 ticket](../../../.codex/delivery/tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md)
selects native pending/error report entry and bounded active-workset serving.
The shell mounts before protected metadata; the prototype markup cannot paint
before the application bridge substitutes neutral values. Authorization failure
keeps that shell with an empty title and no visible result data. The editor DTO
provides actor/capability metadata in its authorized response. A healthy event
channel precedes protected display; reconnect repeats current authorization.
On the initial mount, the authorized editor request and channel connection start
concurrently. Editor data cannot render until the channel is trusted. Reconnect
waits for renewal before dispatching fresh editor reads. Optional embedded ready
results cover only the active workset and are checked against saved bindings;
older responses use the bounded result endpoint path. Projection buckets and
formatters are reused within the active renderer to avoid repeated full-array
searches and chart reconstruction on unrelated inspector changes. Definition
hydration and chart initialization run before the next paint. Decoded response
byte counts are reused for immutable query payload accounting. Static SVG plots
sleep after one still frame and wake on normal updates/interaction. Card loading
marks stay local and static; the plot-region progress indicator rotates unless
reduced motion is requested. The workspace header does not blur its own empty
backdrop; its grid geometry, color, border and controls remain the same.

The browser removes the periodic actor poll, cancels abandoned result reads,
evicts inactive query data and enforces the 16 MiB / 32-entry active cache budget.
Results are deduplicated by immutable identity and fetched only for the current
workset. This is not an offline cache. Trusted input may mark ensuing protected
work as interactive; token renewal and passive viewing do not record activity.
Channel reconciliation can retain one hidden, principal-bound unsaved definition;
fresh authorization is required before restoration. Login, logout and denied
access clear it, and snapshot views never restore an editing draft.
Owner correction 001 (2026-09-23) supersedes the earlier report-header currency
and timezone decision: report presentation omits visible and accessible EUR/UTC
in configured and legacy views, tables, Focus and tooltips. API units, timezone,
calculation and immutable identity remain unchanged. The inspector occupies its
own grid column alongside both chrome and content; at narrow widths it occupies
the content row below the chrome and opens explicitly. The rail remains stable.
Action controls use the period-control dimensions (28 px height, 16 px radius,
10 px font); card configuration uses a named SVG gear. Fixed card/status geometry,
prevent-scroll focus restoration and an updated-in-place chart preserve the
plot origin while selecting cards. One last authorized projection may remain
under a loading indicator while new results load, and is cleared on loss of
trust/authorization. The chart fits available content or Focus height and resizes.
See the [bounded correction evidence](../../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-001/report.md).
The earlier performance measurements remain attributed to their measured build;
they are not a new performance qualification of this presentation correction.

The [serving/lifecycle contract](../../contracts/report-refresh-serving-recovery-contract.md)
(version 7) owns API rollout, event, pool, retention and resource bounds.
[W39 execution evidence](../../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/execution-notes.md)
records the actual source/runtime checks and unmet performance targets. W39 does
not update the consumed MS-004 ledger or confer its acceptance.

## W39 owner correction 002 — independent docks and workset creation

[Correction 002](../../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-002/README.md)
refines the local W39 presentation without importing or accepting MS-004.
The existing report header is now a direct workspace child spanning the report
and inspector columns. Its inspector toggle stays at the outer right edge while
the right dock opens/closes; the dock starts below that header. Configured and
legacy report shells use this structure. At narrow widths the navigation row
sizes to its stacked tabs and controls instead of retaining a fixed 40 px height.

The shared left navigation context occupies a column after the fixed rail and
moves/shrinks the workspace. It aligns with the workspace top and fits its content
with bounded scrolling. Changing groups reuses that column. At <=640 px it is a
content-sized row above the workspace, with a 45dvh cap. Navigation is non-modal;
Tab may leave it, Escape restores its rail opener, and clicking the workspace
does not dismiss the dock. Left and right docks can coexist without overlap.
The preserved pilot source remains unchanged; runtime changes use declared seams.

Add workset resumes an existing empty personal workset whose bilingual name is
still an automatic new-workset name, then opens its Set inspector. Rename or
adding a metric finishes that pending state and allows another new workset.
Successive/rapid Add events consult the latest draft synchronously. Newly created
worksets and explicit copies receive collision-free bilingual labels; existing
worksets/cards are neither removed nor renamed. Explicit copies retain their
independent workset/card IDs and immutable metric references. The serialized
contract is unchanged; the new creation behavior and labels are presentation
policy. Targeted real Save/reload proof uses a separate synthetic report.

## W39 owner correction 003 — compact metrics and bounded chart presentation

[Correction 003](../../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-003/README.md)
adds five explicit owner refinements. Header, report navigation and main content
share 20 px inline insets (12 px narrow), with roomier auto-height navigation.
KPI cards are independent 124 px surfaces, 10 px gaps and the existing panel
radius; selection, gear, loading and comparison states preserve their geometry.
This uses the Mindbox atlas for separate-card interaction context, not its exact
skin or business values. The cropped atlas image does not demonstrate a complete
YoY card component; that requirement comes from the current owner decision.

Each KPI YoY reads its own bound result's authoritative
`temporal.changes[binding.bucket_projection]` aggregate. It never sums bucket
percentages or copies the selected chart's comparison across cards. Temporal off,
unapplied context, loading, incomplete/missing data and zero baseline remain
explicit; unavailable deltas are not reconstructed from current/prior totals.
Server calculations, units and serialized identities are unchanged.

The normal chart now uses a bounded adaptive 320–520 px height (44 percent of
viewport height before clamping), superseding correction 001's remaining-space
height policy. Focus remains separately expanded. Each line axis uses padded
finite data bounds and readable intervals independently per unit; zero is not
forced for nonzero line ranges. Empty, constant, zero and negative ranges remain
valid without modifying any plotted observations. Tooltips render signed server
deltas through product-owned DOM text nodes; positive/negative/neutral colors use
existing semantic tokens, with signed text so color is not the only cue. Existing
EUR/UTC removal, dock layout, Add guards and trust/authorization boundaries remain.

## W39 owner correction 004 — cached selection and report presentation

[Correction 004](../../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-004/README.md)
records the owner-selected follow-up: full grouped whole-unit card totals and
absolute deltas; percentage presentation with at most one fractional digit;
an unboxed, keyboard-focusable metric catalog; a horizontally scrollable KPI rail
whose whole card selects through one native button, with independent gear and
multi-select controls; and separate configuration/results surfaces including the
chart toolbar. This is presentation rounding only; raw values and export precision
remain unchanged. No implicit millions, EUR or UTC are introduced.

A cached single-metric selection changes the persisted view draft without automatic
Apply, calculation/save network calls or pending status. Explicit Save may prepare
the selected view using existing result IDs. Actual query-context changes retain
stale-result notice and Apply requirement. Existing ECharts instances update for
200 ms, with animation disabled under reduced motion; drag does not select a card.
This local correction does not accept MS-004 or requalify prior load measurements.

## W39 owner correction 005 — workspace-bound Focus and report controls

[Correction 005](../../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-005/README.md)
was implemented directly by the coordinator at the owner's request. Focus fills
the workspace inner bounds through a dedicated shell portal; it no longer derives
asymmetric offsets from the browser viewport. KPI cards keep260 px width (220 px
narrow) with unused rail space and horizontal overflow preserved. Comparison,
pair selection and series/delta display controls live in the report toolbar,
not an inspector tab. Expanded metric catalog search and options use separated
rows. This supersedes prior growing-card/inspector-placement presentation only;
calculation, Apply/Save and existing rounding/motion contracts remain unchanged.

## W39 owner correction 006 — global report actions

[Correction 006](../../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-006/README.md)
implements the owner's selected second layout variant: editable report title and
status in the spanning global header; primary Apply and disk-icon Save actions;
secondary restore/snapshot actions in an accessible overflow disclosure. Above
results, only compact workset tabs, active-workset reorder controls, Add and
Configure remain. The large configuration panel, repeated heading and repeated
period are removed. Meaningful stale/error notices and capability guards remain.
Narrow screens retain title/status and icon-only Save. Existing calculation,
save semantics, card widths, comparison placement and Focus bounds are preserved.

## W39 owner correction 007 — result expansion

[Correction 007](../../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-007/README.md)
replaces the Focus label with an accessible upper-right expand icon attached to
the chart/table result. The selected representation fills the existing workspace
surface; collapse and Escape restore the invoking control. Workset ordering uses
left/right controls, shown only with multiple worksets. Data and save semantics
are unchanged.

## W39 owner correction 008 — table caption

[Correction 008](../../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-008/README.md) removes the visible server-values caption in normal and expanded tables. Accessible naming remains via aria-label, without a replacement visible label.

## W39 owner correction 009 — title focus

[Correction 009](../../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-009/README.md) keeps the title keyboard-focus indicator inside the input bounds with a 1px inset outline; title sizing and persistence remain unchanged.

## W39 owner correction 010 — redundant context shortcuts

[Correction 010](../../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-010/README.md) removes the Context/day cluster from configured-report rendering and navigation; settings remain available in the inspector.


## MS-006 composer implementation seam

[MS-006](../planning/milestones/MS-006/plan.md) adds a workbook chart/table composer
inside the accepted PilotDocument shell on existing UI-RPT-002/003 routes, selected
by the existing `view` query key (`composer`). The route registry stays unchanged.
ComposerWorkspace, ComposerBuilder and composer-state own new authored block state;
WorkspacePlot/WorkspaceTable remain the result projection/rendering seam. Legacy
ConfiguredWorkspace remains available and hands new-version responses to the
composer, preserving old worksets and snapshots. No live design tool or alternate
prototype replaces the accepted source. Narrow composer CSS handles grid stacking
and wrapping of header controls without modifying the preserved pilot source.

[Verification](../../../.codex/delivery/evidence/MS-006/MS-006-S01/verification.md)
separates local scenario observations from the stage's pending independent acceptance
and later C03–C11 outcomes. The journal is the only execution-state authority.
