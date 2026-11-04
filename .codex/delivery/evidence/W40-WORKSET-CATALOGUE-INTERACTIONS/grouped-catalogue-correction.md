# Grouped catalogue and explicit inheritance

Owner correction of 2026-09-24, within [W40](../../tickets/W40-WORKSET-CATALOGUE-INTERACTIONS.md), supersedes the filter presentation in [the preceding correction](compact-catalogue-correction.md).

MetricCatalogue now renders compact 28 px rows grouped as Sales (revenue and receipts) and Averages (average receipt). These are presentation groups for the three registered metrics, not new provider categories. Filters render before a metric is selected. A separate staged scope survives metric switching and is discarded when the dialog closes without Apply.

StoreScopePicker displays the inherited report subset, its count, search and checkbox list. Editing a checkbox changes null inheritance into an explicit subset. Use report filters resets to null. Stores outside the common report scope remain disabled for local metric filtering. Common scope behavior and API schema are unchanged; explicit scopes continue to intersect on the server. ConfiguredWorkspace passes the common scope to the catalogue.

Validation: frontend build/TypeScript passed; 23 files / 113 tests passed, including inherited subset preservation, excluded-store disabling and null reset. Local grouped gate and whitespace check passed. Real preview browser verified both group headings, rows <=30 px, filters visible before metric selection, scope preserved after selecting a metric, automatic custom-mode switch and inherited reset. Desktop 1480x969 and narrow 390x844 screenshots were inspected; final narrow footer bounds are inside the viewport. [Desktop](grouped-catalogue.png), [narrow](grouped-catalogue-narrow.png). Synthetic local fixtures only; no saved report mutation or publication.

The first harness used an exact concatenated heading name without accessibility whitespace and timed out. The corrected accessible-name matcher passed; the failed attempt is not counted as successful proof.
