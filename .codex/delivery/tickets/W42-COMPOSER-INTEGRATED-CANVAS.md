---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.11.0-draft
ticket_id: W42-COMPOSER-INTEGRATED-CANVAS
status: accepted
workstream_id: W42
summary: Integrate the owner-selected block canvas with platform authoring and immutable report snapshots.
requirement_ids: [ANALYTICAL-DOC-002, ANALYTICAL-DOC-004, ANALYTICAL-DOC-006, ANALYTICAL-DOC-014, DASHBOARD-006]
blockers: []
context_sources: [AGENTS.md, .codex/AGENTS.md, custometry-ui-blueprint-ru.md, docs/adr/0007-responsive-web-frontend-platform.md, docs/contracts/analytical-authoring-contract.md]
change_scope:
  allowed_write_paths: [apps/api/src/custometry_api/reports/prepared.py, apps/web/**, packages/contracts/**, packages/presentation/**, tests/contract/presentation/**, tests/unit/presentation/**, tests/e2e/ms-006-composer/**, pnpm-lock.yaml, docs/contracts/analytical-authoring-contract.md, custometry-ui-blueprint-ru.md, .codex/delivery/tickets/W42-COMPOSER-INTEGRATED-CANVAS.md, .codex/delivery/evidence/W42-COMPOSER-INTEGRATED-CANVAS/**]
  forbidden_write_paths: [deploy/**, .codex/delivery/ledgers/**]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills: [better-layout, better-ui, contract-impact-analysis, browser-qa-evidence]
  commands: [focused frontend tests, focused Python contract and service tests, frontend build, uv run python -m tools.check --scope local]
  proof_boundary: local-platform-with-real-api-and-disposable-test-databases
  evidence_target: .codex/delivery/evidence/W42-COMPOSER-INTEGRATED-CANVAS/report.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W42-COMPOSER-INTEGRATED-CANVAS/report.md]
---

# Outcome

Owner explicitly selected prototype integration on 2026-10-10: 24-column grid,
drag/resize feedback, one add palette, text and local store controls, shared inspector.
This independent unit continues the c67c runtime code; it does not resume a milestone.
Preserve analytical providers, access, history, scoped locks and immutable snapshots.
Prior pilot/menu recipes do not veto the current owner-selected design.

# Non-goals

Production deployment, changes to analytical methodology and cross-section pointer transfer.

# Acceptance evidence

See the [report](../evidence/W42-COMPOSER-INTEGRATED-CANVAS/report.md).
Local runtime delivery only; no Git publication or production deployment.

Owner continuation (2026-10-10): use the prototype composition as the platform editor, retain existing KPI card presentation inside the shared grid, and continue development on the platform. Any existing metric set is acceptable. Include chart reveal/filter/type transitions; replace the default new-report entry with this editor.

Owner-reported reload regression (2026-10-11): include the prepared API adapter fix and existing request-read regression tests; preserve access and snapshot contracts.

Owner continuation (2026-10-11): implement the agreed type-aware right inspector, separate per-block data/filter and visual entry points, live presentation changes, per-series combo settings, persisted descriptions and visual configuration. The full visualization catalog must explain missing data capabilities honestly. Preserve historical snapshots and analytical result identity for presentation-only changes.

The visualization continuation also owns `packages/chart_compiler_ts/**`: typed presentation-to-ECharts mapping is shared rather than embedded in inspector components. Existing MS-003 compiler exports remain unchanged.

Owner repair continuation (2026-10-11): unify authoring form fields/actions,
replace the nested existing-block wizard with a single data form, reveal selected
cards without moving focus or compacting the grid, and repeat the three-table,
two-chart, text-description flow. Report-only audit findings outside this selected
repair remain follow-up work.

Owner repair (2026-10-11): remove temporal diagnostic summaries and calendar mapping columns from canvas blocks; compact chart tooltips and color signed deltas. Preserve server comparisons and missing-value semantics.

Owner repair (2026-10-12): reserve side-legend layout space, keep category axis
titles visible, make value labels readable on bars, and add paired range/numeric
controls for maximum bar thickness and category spacing.


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

Owner continuation (2026-10-13): remove the geometry inspector tab; put duplicate and confirmed delete beside each block’s data and visual actions. Preserve grid geometry, undo and locks.

Owner continuation (2026-10-13): readable 220×140px minimum metrics, separate action row, two-line titles, no nested metric scrolling or ordinary Ready/YoY-off copy; preserve placements and scroll the canvas when needed.
