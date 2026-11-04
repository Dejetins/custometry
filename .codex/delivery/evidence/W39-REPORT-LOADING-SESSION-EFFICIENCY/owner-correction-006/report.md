# W39 owner correction 006

Date: 2026-09-23. Direct executor: coordinator task `01a0c02d-5267-7601-b735-5b43d11789c0`.

[Ticket](../../../tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md) · [Source contract v23](../../../../../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md) · [Validation](validation.md).
Requirements: UI-SHELL-001, UI-SHELL-002, METRIC-025, METRIC-027, A11Y-001, I18N-001.

## Authority and implementation

The owner explicitly accepted the previously discussed second variant and requested direct implementation. No delegation or task dispatch was used.

- `ConfiguredWorkspace.tsx`: report title is directly editable in the global header. Apply and Save retain their existing capability/query/conflict guards. The disk icon accompanies Save; its text collapses on narrow screens. Secondary restore/snapshot actions are in the overflow disclosure, with unsaved-change confirmation. The large configuration surface, duplicate period and duplicate heading are removed. Worksets retain their tabs, with reorder arrows only on the active workset, plus accessible Add and Configure icons. Routine status duplication is removed; query-stale and error notices remain.
- `PilotDocument.tsx`: dedicated React title/action portals in the spanning global header. The runtime-owned title remains hidden so legacy updates cannot overwrite the React input. Pending/legacy reports retain their existing title behavior.
- `ReportActionsMenu.tsx`: native-button disclosure with outside-pointer dismissal, focus-leave dismissal, Escape restoration, accessible label/expanded/controls relationships, and ordinary Tab navigation.
- `workspace-copy.ts`, `workspace.css`: bilingual action labels, compact header/workset layout, standard pill controls, adjacent status, and bounded narrow menu. Narrow title/status stack preserves state visibility.

Browser presentation: compatible-change. API, schemas, backend, calculation and persisted representation: none. Existing save/apply handlers and full-precision data remain. Original user tab and draft were not reloaded, saved or discarded. No owner report was saved, no backend restart, publication, canonical import or MS-004 acceptance.

## Observed browser evidence

Mechanic: actual Codex in-app Browser, separate agent-created tab, existing January report at localhost:41746; no mocks or request interception.

- 1480x969: title and save/apply/menu are in the spanning header; former gray configuration panel absent. Menu exposes restore and snapshot. Tab moves from disclosure trigger to restore; Escape closes it and returns focus to trigger.
- 400x900: Save renders an accessible disk icon. Header buttons remain within x193.7–344 of workspace x63–394. Overflow menu x141.8–344, width202.2, with no clipped text/scroll overflow. Editable title and unsaved badge remain visible.
- Changed only the agent tab title to “Проверка шапки”; header reflected the draft and enabled Save. Restore returned it to “Original” and Saved. The interaction tool reported a mouse-command timeout, but the subsequent live DOM confirmed completed restoration; it was not retried blindly.
- 2688x1575: card widths remain260 px; selecting Receipts yields selected state and busy=false, empty transient status, no configuration panel. Title/status are adjacent (input right151, badge left158).
- Configure workset opens the inspector. Two Add clicks create only one empty “Новый набор 1”; only the active workset has the two reorder controls.
- Browser console error logs: none observed in the tested tab.

This is bounded UI/runtime evidence. The existing persistence handlers were preserved; no new real Save against the owner's report was executed. No performance campaign or production verification is claimed.
