---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.1-draft
ticket_id: W06-PENPOT-ANALYTICS-DENSITY-REPAIR
proof_boundary: canonical-penpot-analytics-metric-group-and-result-trust-visual-repair
proof_skills: ["product-design:audit"]
verdict: passed
penpot_file_id: 7cd71457-8d32-8044-8008-549f83bb4645
penpot_start_revision: 159
penpot_end_revision: 164
repository_fingerprint: 966a146df56fc8f0552f1bc2c888656095d0f478faa38f8201847f9225691953
redaction: No credentials, customer data, Penpot document payloads, browser state, or environment dumps were retained.
executed_checks:
  - confirm W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION accepted with passed evidence
  - exact ordered W06 repository fingerprint before the first Penpot write and again before verdict
  - canonical Penpot file and revision-159 guard before the first scoped write
  - individually export and visually inspect each of the 15 W06 target boards after the final write
  - reconcile contract stable UI-IDs against Penpot root-board IDs
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - git diff --check
observations:
  - Canonical Penpot file 7cd71457-8d32-8044-8008-549f83bb4645 ended at revision 164; no concurrent-editor drift was observed by the serial file/revision guards.
  - Stable-ID reconciliation found exactly 110 routes, 25 overlays, and 5 system surfaces; duplicate, missing, and orphan lists were empty.
  - The repeated ordered repository fingerprint was 966a146df56fc8f0552f1bc2c888656095d0f478faa38f8201847f9225691953.
---

# W06-PENPOT-ANALYTICS-DENSITY-REPAIR Evidence

> Compact evidence for one terminal ticket. It is not another execution-state
> source or a replacement for the product specification.

## Outcome and scope

- outcome: existing analytics result surfaces visibly use ordered MetricGroup
  tables, and Result Trust is a compact trigger with a dense on-demand drawer;
- requirement IDs: [UC-017, UC-020, METRIC-009, METRIC-010, METRIC-011,
  METRIC-012, METRIC-013, METRIC-014, METRIC-015, METRIC-016, CHART-015,
  A11Y-006, A11Y-007, REPORT-008, UX-JOURNEY-005, V1-AC-020, V1-AC-021,
  V1-AC-023];
- included: only the existing C11, C17, C23 Metric Group & Number Format
  Preview, UI-OVR-006, UI-AN-003 through UI-AN-012, and UI-AN-014 boards in
  canonical Penpot;
- exclusions: this proves visual Penpot representation only. It does not prove
  browser interaction, keyboard behavior, runtime accessibility, permission,
  calculation, export, or analytics correctness.

No stable UI-ID board was created, deleted, renamed, or moved to another file.
The scoped work changed existing board content and added only nested visual
primitives. A first C11 write stopped after Penpot rejected unsupported font
weight `650`; the same scoped content was immediately repaired using supported
weight `600` before final visual QA. This is reflected in the 159 to 164
revision range and did not change the stable-ID reconciliation.

## Visual QA verdicts

| Existing board/frame | Final visual verdict |
| --- | --- |
| C11 Components / Overlays | pass — bounded Result Trust drawer uses compact two-column rows; no permanent sparse trust column remains. |
| C17 Components / Result Trust | pass — compact trigger placements and a dense, dismissible on-demand drawer are visible without an oversized empty interior. |
| C23 Metric Group & Number Format Preview | pass — compact table shows two ordered groups, current/comparison values, MetricGroupVersion and NumberFormatSpec. |
| UI-OVR-006 Result Trust drawer | pass — dense two-column trust record shows freshness, quality, versions, grain, filters, comparison, time/currency, lineage, limits, return and close. |
| UI-AN-003 Sales Overview | pass — Revenue & demand and Customer behavior table groups with current, vs LY, previous-year and format/detail columns. |
| UI-AN-004 Customer Base | pass — Customer base and Retention groups are a readable table alternative. |
| UI-AN-005 RFM | pass — RFM distribution and Value profile groups are a readable table alternative. |
| UI-AN-006 Cohorts | pass — Cohort retention and Revenue quality groups are a readable table alternative. |
| UI-AN-007 Lifecycle and churn | pass — Lifecycle movement and Churn risk groups are a readable table alternative. |
| UI-AN-008 Basket Analytics | pass — Basket profile and Category affinity groups are a readable table alternative. |
| UI-AN-009 Stores and Channels | pass — Channel performance and Store comparability groups are a readable table alternative. |
| UI-AN-010 Margin and Discounts | pass — Margin quality and Discount performance groups are a readable table alternative. |
| UI-AN-011 Custom Builder | pass — compact MetricGroupVersion output preview is ordered and uses typed number-format labels. |
| UI-AN-012 Result detail and trust | pass — Result metrics and Data quality & limitations groups are a readable table alternative with compact Result Trust trigger. |
| UI-AN-014 Research Workspace | pass — Research signals and Evidence quality appear as an ordered research metric-group table with compact Result Trust trigger. |

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
| --- | --- | --- |
| W05 predecessor record | pass | W05 ticket was `accepted`; W05 evidence verdict was `passed`. |
| Initial Penpot guard | pass | Canonical file ID matched and current revision was 159 before the first write. |
| Ordered fingerprint, before and after | pass | `966a146df56fc8f0552f1bc2c888656095d0f478faa38f8201847f9225691953` both times. |
| Penpot export visual QA | pass | Individual current exports of all 15 listed boards were reviewed under `product-design:audit`; see verdict table. |
| Stable-ID reconciliation | pass | Contract expected 140; Penpot actual 140: 110 routes, 25 overlays, 5 systems; no duplicate, missing, or orphan ID. |
| `uv run python -m tools.custometry_quality.validate_route_registry` | pass | Observed 110 routes, 25 overlays and 5 system surfaces. |
| `uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json` | pass | Schema validation completed successfully. |
| `uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json` | pass | Schema validation completed successfully. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | Validator completed successfully before terminal evidence creation; rerun after evidence is recorded below. |
| `git diff --check` | pass | No whitespace errors. |

## Verdict

`passed`. The canonical Penpot representation now makes the specified
MetricGroup table and compact Result Trust contract directly inspectable.
Residual risk is limited to the declared proof boundary: this design evidence
does not prove a running product or assistive-technology behavior. The next
safe action is implementation/browser validation only if a separate authorized
ticket requests it.
