# Stable chart axis-name alignment

Owner requested fixed metric-label text origin on 2026-09-24. In `WorkspaceProjection.tsx`, the left Y-axis name now has explicit left alignment at the axis endpoint; the optional right axis aligns inward from its endpoint. The former implicit centered alignment shifted the text origin by half the label width.

Validation: frontend build including TypeScript passed. Real local browser at 1480x969 switched Net revenue, Receipts and Average receipt and measured the first matching SVG axis-label bounding box for each. The horizontal-origin spread was <=0.5 CSS px. [Final screenshot](axis-label-alignment.png) was visually inspected. Local grouped gate and diff whitespace check passed. No data, API, persisted configuration or calculation changed. This is a bounded visual correction under [W40](../../tickets/W40-WORKSET-CATALOGUE-INTERACTIONS.md).
