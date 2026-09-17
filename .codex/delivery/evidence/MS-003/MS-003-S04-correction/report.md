# MS-003-S04 — owner-requested pilot fidelity correction

Iteration: 2026-09-15, correction of the rejected S04 visual implementation.
Authority: the owner explicitly rejected the unsolicited adaptation and ordered
all implemented report elements to follow the preserved pilot. No successor
execution or publication is included. This report supersedes only the previous
visual-fidelity claim in [S04](../MS-003-S04/report.md); the terminal journal,
receipt, accepted plan and earlier immutable evidence are preserved.

## Sources and cause

Accepted [plan 0.2.0](../../../../../docs/architecture/planning/milestones/MS-003/plan.md),
SHA-256 `4a6b1bf2a64a04b74e073bb22e46895795e187be57fe93b6711408069d6e7280`.
Preserved [pilot](../../../../../docs/architecture/ui/target-pilot/README.md):
`ru/source.html`, SHA-256
`b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700`.
Checkout base: `cb4f696dc1dca3bc051debd347810f7d74caa319`, with existing S03/S04
uncommitted work. The earlier implementation treated a demonstrated composition
as permission to create another layout. Its browser journey passed without
proving exact composition. That interpretation was wrong.

## Changes and source mapping

The report now uses the source CSS cascade and SVG symbol definitions. Only
root scoping and seven CSS class prefixes isolate legacy global rules; a test
compares the complete transformed cascade against the pinned source bytes.
The rail, workspace, title row, document tabs, parameter clusters, KPI rail,
chart panel, docked/overlay inspector and Focus use the source classes.
Header Trust opens a native dialog; inspector tabs, popovers and Focus support
Escape and focus restoration. RU/EN copy is held in localization.

The required title/source form is in the inspector. Period, Store and Comparison
use toolbar menus. Save is in the inspector footer and view menu. Existing real
Apply/Save/CAS, immutable preview, protected-query invalidation and access behavior
remain connected. Chart and table use server series; no customer demo data or
browser aggregation is introduced.

Contract impact: browser presentation is a compatible change under the owner's
correction. The adapter validates S03 canonical spec/default reference hashes
before applying the pilot palette, axes and legend presentation. Persisted data,
metric bindings, BrandProfile, CompanyPack and identity hashes are unchanged.
There is no new API, persistence, permission or dependency change in this repair.

Owned changes: `apps/web/src/features/reports/{ReportWorkspace.tsx,ReportChart.tsx,
PilotChrome.tsx,pilot.css,pilot-symbols.ts,report.css,pilot-source.test.ts}`;
`packages/localization/src/{index.ts,report-pilot-copy.ts}`;
`tests/e2e/ms-003-report-fidelity/`; this evidence directory; live Web source
contract, analytical authoring contract, architecture index, localized report
help and generated documentation index. No files are deleted. Existing S03
backend/persistence/contracts changes are excluded from this correction.

## Verification boundary

The slice config owns host Vite 41734, production API 58104, fault-control 58105,
and a read-only pilot server 8834. It uses the original real S01 preparation
fixture against the explicitly owned Hybrid database and artifacts. Each run
creates its own ordinary analyst; fault controls are restricted to that analyst's
snapshots and sessions. No positive auth/API response is mocked. User runtime
5173/8000 remains separate and available.

Final verification: all six Playwright scenarios passed in 38.5 seconds; Web
build/type checking and all 79 Web tests passed; both localization tests and
strict public documentation build passed. Positive journeys had no unexpected
console warnings/errors or failed HTTP responses. Expected connection failures
occurred only during the deliberate production API restart. Test servers shut
down and the temporary analyst credential file was removed. Captures under `browser/`
compare normalized 1920x1080 and 768x1024 states with the actual preserved source.
Geometry checks compare workspace/header/tabs/intro/KPI/panel-header/rail and
open inspector; source backgrounds, radius and typography are also compared.
These checks are stronger than the previous visual claim but do not imply
pixel identity for different business content or complete design-system coverage.

## Scope and retained limits

The pilot demonstrates customer metrics and channel groups; this stage supplies
three eligible receipt metrics and a canonical daily net-revenue line. Unsupported
customer segments, authoring/export and publication controls remain disabled.
Login and library have no complete equivalent source screen. Their necessary
controls reuse pilot styling. These content limits do not authorize another
report layout. Source bytes remain unchanged.

No installed HTTPS/candidate bundle, S05 execution, S06 owner visual acceptance,
or release is claimed. The canonical ledger remains the stage-state authority;
this correction does not forge a terminal-stage reopen or a new receipt.

Live navigation: [Web source contract](../../../../../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md),
[architecture index](../../../../../docs/architecture/README.md).

## Commands and observed results

- `corepack pnpm exec playwright test --config tests/e2e/ms-003-report-fidelity/playwright.config.ts --max-failures=1`: 6 passed.
- `corepack pnpm --filter @custometry/web build`: passed, including TypeScript; existing chunk-size advisory remains (ECharts report chunk above 500 kB).
- `corepack pnpm --filter @custometry/web test`: 18 files, 79 tests passed, including full source CSS mapping and source hash verification.
- `corepack pnpm --filter @custometry/localization test`: 2 passed.
- `uv run --locked --package custometry-docs mkdocs build --strict`: passed.
- `uv run --locked python -m tools.custometry_quality.generate_docs_index`: passed.
- `uv run --locked python -m tools.check --scope local`: passed before final evidence binding; final rerun recorded in verification.json.

Initial browser failures exposed missing explicit select labels and asynchronous
test navigation waits; these were corrected before the passing run. Two immediate
restarts hit the fixture's OS socket reuse interval; no foreign process was killed.
One interrupted run was discarded. Earlier screenshots were not used as passing
proof. The final run's captures and source hashes are bound by `verification.json`.

A separate real UI login/Apply/Save smoke on the user runtime 5173 also passed
with zero page errors. Its saved report is
`/w/1af52456-b651-4bd8-9703-f558cd7fd7f1/reports/fceaed2b-b9af-5107-9944-a0ef91b466f9/edit`.
The user can inspect this report using the already supplied analyst account.
