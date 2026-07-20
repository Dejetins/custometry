---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.2-draft
ticket_id: W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION
proof_boundary: canonical-penpot-product-0.9.2-ui-0.6.2-discount-methodology-visual-delta
proof_skills: ["product-design:audit"]
verdict: passed
penpot_file_id: 7cd71457-8d32-8044-8008-549f83bb4645
penpot_start_revision: 164
penpot_end_revision: 181
repository_fingerprint: d085f788eb20b0131f9cb539492eaab3be5a3a8a6f119eee49572b71416967f1
redaction: No credentials, customer data, Penpot document payloads, browser state, or environment dumps were retained.
executed_checks:
  - confirm W06 and W07 accepted with passed terminal evidence
  - exact ordered W08 repository fingerprint before the first Penpot write and immediately before verdict
  - canonical Penpot file ID and revision-164 guard before the first scoped write
  - individually export and visually inspect every W08 target frame and prototype flow 09
  - reconcile contract stable UI-IDs against Penpot root-board IDs
  - validate the five C24 local library components and prototype flow 09 structure
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - git diff --check
observations:
  - Canonical Penpot file 7cd71457-8d32-8044-8008-549f83bb4645 ended at revision 181; serial guards showed no unexplained concurrent drift.
  - Stable-ID reconciliation found exactly 110 routes, 25 overlays, and 5 system surfaces; duplicate, missing, and orphan lists were empty.
  - The repeated ordered repository fingerprint was d085f788eb20b0131f9cb539492eaab3be5a3a8a6f119eee49572b71416967f1.
---

# W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION Evidence

> Compact evidence for one terminal ticket. It is not another execution-state
> source or a replacement for the product specification.

## Outcome and scope

- outcome: the canonical Penpot file now visibly represents the accepted
  discount-component, policy/cap, metric-certification, method-availability,
  exact PVM, Result Trust, Research, and export-disclosure delta as one compact
  governed flow;
- requirement IDs: [UC-027, METRIC-017, METRIC-018, METRIC-019, METRIC-020,
  DISCOUNT-001, DISCOUNT-002, DISCOUNT-003, DISCOUNT-004, DISCOUNT-005,
  DISCOUNT-006, DISCOUNT-007, DISCOUNT-008, DISCOUNT-009, DISCOUNT-010,
  DISCOUNT-011, DISCOUNT-012, DISCOUNT-013, DISCOUNT-014, DISCOUNT-015,
  DISCOUNT-016, DISCOUNT-017, DISCOUNT-018, DISCOUNT-019, DISCOUNT-020,
  METHOD-009, METHOD-010, METHOD-011, METHOD-012, METHOD-013, METHOD-014,
  PVM-001, PVM-002, PVM-003, PVM-004, PVM-005, PVM-006, V1-AC-032,
  V1-AC-033, V1-AC-034, V1-AC-035, V1-AC-036];
- included: C24, the 11 declared route frames, C17, UI-OVR-006,
  UI-OVR-012, five local library components, and prototype flow 09 in the
  canonical Penpot file;
- exclusions: this is Penpot design implementation proof only. It does not
  prove browser or runtime behavior, runtime accessibility, permissions,
  calculations, analytical correctness, export generation, performance,
  deployment, or release readiness.

Frost styling, the W06 compact 64 px KPI density, ordered MetricGroup output,
on-demand Result Trust, and every existing stable UI-ID were preserved.
Commercial discount, customer benefit, and recognized net revenue remain
distinct. Historical cap breaches are diagnostic and never clamp source data;
simulated breaches block publication. CompanyPack 50% values are visibly
labelled as an example rather than a platform default.

## Penpot inventory

### Created component surface and local components

- C24 board: `33a2a659-d0eb-80bd-8008-5af8130c0d8f`;
- Discount Attribution Badges: component
  `33a2a659-d0eb-80bd-8008-5af81685f937`, main board
  `33a2a659-d0eb-80bd-8008-5af81327b596`;
- Compact Discount Component Table: component
  `33a2a659-d0eb-80bd-8008-5af816868dfa`, main board
  `33a2a659-d0eb-80bd-8008-5af81353e9fb`;
- Discount Stacking Matrix: component
  `33a2a659-d0eb-80bd-8008-5af81687b5ec`, main board
  `33a2a659-d0eb-80bd-8008-5af814626f5b`;
- Discount Cap States: component
  `33a2a659-d0eb-80bd-8008-5af816888eaa`, main board
  `33a2a659-d0eb-80bd-8008-5af81507a222`;
- PVM Waterfall and Data Table: component
  `33a2a659-d0eb-80bd-8008-5af816891327`, main board
  `33a2a659-d0eb-80bd-8008-5af8153fecc8`.

### Updated existing board IDs

- data: `e451483d-aae3-807d-8008-54a99ff1f7c5`,
  `e451483d-aae3-807d-8008-54a9a09abd1d`,
  `e451483d-aae3-807d-8008-54a9a1d14227`,
  `e451483d-aae3-807d-8008-54a9a23fca7a`,
  `3e34a4ec-283e-800b-8008-5932e011b257`, and
  `3e34a4ec-283e-800b-8008-5932e09ed7ba`;
- analytics: `e451483d-aae3-807d-8008-54a9b8c6fbdf`,
  `e451483d-aae3-807d-8008-54a9bb462e68`,
  `e451483d-aae3-807d-8008-54a9bbc4981f`,
  `e451483d-aae3-807d-8008-54a9bc3e5639`, and
  `3e34a4ec-283e-800b-8008-593261aa606b`;
- C17: `e451483d-aae3-807d-8008-54a6e546060f`;
- overlays: `e451483d-aae3-807d-8008-54aa9a61e1e1` and
  `e451483d-aae3-807d-8008-54aa9f6f8bf6`.

### Prototype flow 09

The prototype flow is named `09 Dataset mapping → policy/certification →
Margin & Discounts → PVM/Result Trust → Research/Export return`, starts at
UI-DATA-008 (`e451483d-aae3-807d-8008-54a99ff1f7c5`), and has 11 active
next/return interactions plus the Result Trust overlay interaction. Its visual
audit map is `33a2a659-d0eb-80bd-8008-5afbb29fecd7`. The return control is
`33a2a659-d0eb-80bd-8008-5afa9175938c` and returns to Research.

## Final visual QA verdicts

| Board/frame | Final visual verdict |
| --- | --- |
| C24 Discount Components, Cap & PVM | pass — all five component families are compact, labelled, non-color-only, and unclipped; PVM waterfall and exact table reconcile visibly. |
| UI-DATA-008 | pass — mapping roles, redemption/accrual distinction, source total, attribution, coverage, unavailable state, and next action are readable. |
| UI-DATA-010 | pass — effective dates, stacking, accounting, cap parameters, historical diagnostic, simulated block, and labelled CompanyPack example are readable. |
| UI-DATA-013 | pass — lifecycle and independent certification, origin, review, replacement, and impact remain dense and legible. |
| UI-DATA-014 | pass — evidence, quality, robustness, sensitivity, exclusions, usage limit, replacement, and downstream impact are explicit. |
| UI-DATA-021 | pass — native/template/future/unsupported availability and evidence ceilings are visible; future methods are explicitly not runnable. |
| UI-DATA-022 | pass — default pack, PVM order, representativeness, robustness, residual tolerance, pinned policies, and non-causal ceiling are readable. |
| UI-AN-002 | pass — dataset, grain, policy, method, comparison, treatment, coverage, residual, cap, and future-method preflight are visible. |
| UI-AN-010 | pass — four compact KPIs, component table, stacking/depth/cap, exact PVM, margin/revenue, table alternative, and compact Result Trust are visible without clipping. |
| UI-AN-011 | pass — builder pins preserve MetricGroup order, policy, comparison, treatment, coverage classes, table alternative, and preview state. |
| UI-AN-012 | pass — immutable result identity, pinned semantics, exact residual, limitations, export disclosure, and compact Result Trust are visible. |
| UI-AN-014 | pass — evidence, findings, comments, policy/method/certification, limitations, prohibited causal claim, and export disclosure remain distinct. |
| C17 Result Trust | pass — compact triggers and dense on-demand disclosure are unclipped after a bounded height repair; no permanent trust column was added. |
| UI-OVR-006 | pass — compact on-demand policy, attribution, coverage, PVM, residual, certification, method, cap, and limitations fit without clipping. |
| UI-OVR-012 | pass — immutable snapshot, policy, attribution, coverage/residual, cap, PVM formula, method ceiling, README disclosure, acknowledgement, and return action fit without clipping. |
| Flow 09 visual map | pass — the nine-step mapping-to-export-return path and design-only proof boundary are readable end to end. |

## Compatible repairs

- An initial page-context mismatch created an empty C24 board on C17; the exact
  empty board was removed after a guarded structural scan. The canonical C24
  page and populated board remain unchanged.
- Penpot rejected unsupported font weight `500` during the first nested-panel
  attempt; the partial scoped panel was removed and recreated using supported
  `400/600` weights.
- A first flow-map connector used an invalid zero width; its partial map was
  removed and rebuilt with non-zero geometry.
- C24 PVM bars/table spacing, wide total/unavailable/future badges, and the C17
  lower disclosure note received bounded visual repairs and fresh export QA.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
| --- | --- | --- |
| W06 and W07 predecessor records | pass | Both tickets were `accepted`; both evidence verdicts were `passed`. |
| Initial Penpot guard | pass | Canonical file ID matched and current revision was exactly 164 before the first write. |
| Ordered fingerprint, before and after | pass | `d085f788eb20b0131f9cb539492eaab3be5a3a8a6f119eee49572b71416967f1` both times. |
| Penpot export visual QA | pass | Individual current exports of all 16 declared targets were reviewed under `product-design:audit`; see verdict table. |
| Stable-ID reconciliation | pass | Contract and Penpot both contain 110 route, 25 overlay, and 5 system IDs; duplicate, missing, and orphan lists are empty. |
| Penpot file validation | pass | `currentFile.validate()` returned no errors at revision 181. |
| C24 local-library scan | pass | Exactly the five named W08 components were present. |
| Flow 09 structural scan | pass | Named flow starts at UI-DATA-008; 11 next/return interactions and one Result Trust interaction were present. |
| `uv run python -m tools.custometry_quality.validate_route_registry` | pass | Observed 110 routes, 25 overlays, 5 system surfaces, and 110 route contracts. |
| `uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json` | pass | Schema validation completed successfully. |
| `uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json` | pass | Schema validation completed successfully. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | Validator passed before evidence creation and again after the terminal ticket/evidence records were written. |
| `git diff --check` | pass | No whitespace errors before evidence creation or in the terminal rerun. |

## Verdict

`passed`. The canonical Penpot design implements the accepted W08 delta while
preserving Frost, W06 density, ordered MetricGroup output, compact on-demand
Result Trust, route geometry, and every stable UI identity. Residual risk is
limited to the declared proof boundary: no browser, runtime, accessibility-
runtime, permission, calculation, analytical, export-generation, performance,
deployment, or release proof is claimed.
