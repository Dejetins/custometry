# W39 owner correction 010 — redundant context shortcuts

[Ticket](../../../tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md) · [Source contract v27](../../../../../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md)

Owner requested removal of the two just-discussed Context/day shortcuts. `workspace.css` removes their entire control cluster from configured-report rendering and keyboard/accessibility navigation, without leaving an empty group. Preserved pilot DOM remains available to its legacy runtime bindings. Existing inspector and other specific controls remain usable. Scope: UI-SHELL-001/A11Y-001, presentation only; no backend or persistence change, publication or MS-004 acceptance.

Validation: TypeScript/Vite build and local gate logs adjacent; whitespace diff check. Real in-app Browser verifies both shortcuts are hidden, their cluster has zero width and remaining report controls remain visible. Original user tab/draft untouched.
