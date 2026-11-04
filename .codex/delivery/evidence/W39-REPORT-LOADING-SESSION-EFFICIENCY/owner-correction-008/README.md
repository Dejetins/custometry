# W39 owner correction 008 — remove table caption

[Ticket](../../../tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md) · [Source contract v25](../../../../../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md)

Owner requested direct removal of the visible server-values caption. `WorkspaceProjection.tsx` removes it from the shared result table, including expanded mode. An invisible aria-label preserves the accessible table name. No substitute visible caption is introduced. Data and exceptional missing-comparison notices are unchanged.

Scope: bounded presentation repair, A11Y-001/I18N-001; no API/persistence change, publication or MS-004 acceptance. TypeScript/Vite build and local gate logs are adjacent. Browser proof: normal and expanded result table have zero caption elements and retain an accessible name.
