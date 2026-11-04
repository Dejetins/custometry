# W39 owner correction 005

Date: 2026-09-23. Executor: coordinator task `01a0c02d-5267-7601-b735-5b43d11789c0`, directly, following the owner's explicit instruction to stop delegating these repairs to another task.

[Ticket](../../../tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md) · [Source contract v22](../../../../../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md) · [Validation](validation.md).
Requirements: METRIC-025, METRIC-027, METRIC-028, CHART-021, A11Y-001.

## Scope and causes

Four owner corrections: fill the workspace with Focus; keep standard-width KPI cards; move comparison controls into the report; eliminate overlap in the expanded metric catalog.

The card rail used `minmax(220px,1fr)`, stretching three cards across wide screens. Focus used viewport-fixed offsets rather than the actual workspace bounds. Comparison controls were rendered only inside the chart inspector. Catalog search and metric buttons lacked an explicit separated layout.

## Changes

- `ConfiguredWorkspace.tsx`: comparison/pair/display controls now live beside chart/table controls; obsolete chart inspector tab removed. Existing shell comparison entry navigates to the on-page controls. Catalog options have their own layout. Focus is supplied to the shell as a separate portal, with keyboard focus restored on exit.
- `PilotDocument.tsx`: Focus portal is a direct workspace child; background workspace children are inert while open, then restored. This avoids clipped/offset report scroll containers and respects actual shell/navigation geometry.
- `workspace.css`: Focus fills the inner workspace rectangle with uniform 16 px content padding (12 px narrow). Cards are 260 px wide, 220 px at <=600 px, without growing to fill unused rail space. Catalog options are separate full-width controls with 8 px gaps and 12 px below search.
- `WorkspaceProjection.tsx`: Focus plot sizing follows the actual Focus container bounds and observes its resize. Normal chart height is unchanged.

Browser presentation impact: compatible-change. API, schemas, calculation, saved identities and export precision: none. Existing view dirty/Apply semantics remain unchanged. No original user tab/reload/save, no owner report mutation, no other agent, backend restart, publication, canonical import or MS-004 acceptance.

## Real Browser verification

Mechanic: Codex in-app Browser, agent-created tabs only; owner January report loaded from localhost:41746. No intercepted data or mocked responses. Original user tab and unsaved state untouched. Tests used transient view selections only.

| Check | Observed result |
| --- | --- |
| 2688x1575 cards | Three cards each260 px; unused rail remains empty. |
| 2688 Focus | Focus x63/y9/right2679/bottom1566, exactly workspace inner bounds (outer x62/y8/right2680/bottom1567). |
| 1480x969 direct Focus URL | Dialog receives focus. Inner bounds x63/y9/right1471/bottom960; plot x79/y53/right1455/bottom944. Uniform16 px content inset; no viewport offset mismatch. |
| Focus isolation/exit | Header, navigation, report and inspector have inert attributes; dialog does not. Escape removes Focus and returns activeElement to Focus button. Close button also returns focus. |
| 1480 catalog | Search bottom394.586; buttons y406.586/442.586/478.586, each28 px high.12 px search gap and8 px option gaps; no overlap. |
| Comparison placement | Controls are in report toolbar, absent from inspector. Selecting delta_trend renders Delta-percent axis. Selecting two card checkboxes enables Compare two cards. |
| 400x850 | Cards220 px; rail client307/scroll680. Controls wrap inside291 px. Focus x63/y6/right394/bottom844 matches inner workspace; plot x75/y46/right382/bottom832.12 px inset. |
| Console | No error logs observed in tested tab. |

Viewport override restored. Fresh final delivery tab will retain the saved report, without test changes. This is focused local browser proof, not production/release or a new performance qualification.
