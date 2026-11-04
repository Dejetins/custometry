# W39 owner correction 007 — result expansion

[Ticket](../../../tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md) · [Source contract v24](../../../../../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md)

Owner requested direct, bounded repair. `ConfiguredWorkspace.tsx`, `workspace-copy.ts` and `workspace.css` replace the Focus text button with an accessible expand icon in the result panel's upper-right action row. Expanded content follows the selected chart/table view; collapse is an upper-right icon. Escape and focus restoration are retained. Workset reorder controls are hidden for a single workset and use horizontal arrows and descriptive labels for multiple worksets.

Requirements: CHART-021, METRIC-025, A11Y-001, I18N-001. Browser presentation impact: compatible-change. Backend, persistence, calculations: none. No delegated agent, user-tab reload/save, publication or MS-004 acceptance.

Actual in-app Browser at1480x969: no Focus text button; zero workset arrows with one set; expand right edge1101 equals result panel right edge1101, top417.5 versus panel415.5. Expanded chart fills workspace inner bounds x63/y9/right1471/bottom960; no duplicate table. Expanded table contains31 rows and no chart. Escape restores focus to expand; collapse works. Console check recorded no errors. Original user tab/draft untouched.

Validation: `corepack pnpm --filter @custometry/web build` PASS (TypeScript and Vite; existing chunk-size advisory). `uv run --locked python -m tools.check --scope local` and `git diff --check` results in local.log. Existing106 tests from correction006 are not presented as rerun for this styling/control-placement repair. Browser proof covers changed behavior. This is local evidence only.
