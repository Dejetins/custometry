# W39 owner correction 009 — title focus ring

[Ticket](../../../tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md) · [Source contract v26](../../../../../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md)

The report title inherited a 2px focus outline with a 2px outward offset. `workspace.css` gives this input a 1px inset outline and no shadow, retaining keyboard visibility without expanding its painted bounds. No title/input sizing or persistence behavior changes. Requirements: A11Y-001, UI-SHELL-001. Bounded compatible presentation repair; no backend change, publication or MS-004 acceptance.

The owner's second comment requests explanation only: port-epilogue maps both filters-menu-open and groupby-menu-open to the context inspector. Context contains period, grain, calendar basis and common stores. The raw day label reflects daily grain. No changes to these buttons were authorized or made.

Build and local gate logs are adjacent. Browser proof checks focused input geometry/style and both context entry points in a separate tab; the original user draft is untouched.

Observed: typing “Тестовое название” leaves input height26px; computed outline1px, offset−1px, shadow none. Both context and day buttons select the Context inspector tab. TypeScript/Vite build and local gate passed; diff whitespace check passed.
