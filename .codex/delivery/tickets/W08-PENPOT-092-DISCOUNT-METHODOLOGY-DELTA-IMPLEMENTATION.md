---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.2-draft
ticket_id: W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION
status: accepted
workstream_id: W08
summary: Implement the accepted product 0.9.2 and UI 0.6.2 discount-component, cap, PVM, metric-trust, and methodology-availability delta in the canonical Penpot file without changing stable UI identities.
requirement_ids: [UC-027, METRIC-017, METRIC-018, METRIC-019, METRIC-020, DISCOUNT-001, DISCOUNT-002, DISCOUNT-003, DISCOUNT-004, DISCOUNT-005, DISCOUNT-006, DISCOUNT-007, DISCOUNT-008, DISCOUNT-009, DISCOUNT-010, DISCOUNT-011, DISCOUNT-012, DISCOUNT-013, DISCOUNT-014, DISCOUNT-015, DISCOUNT-016, DISCOUNT-017, DISCOUNT-018, DISCOUNT-019, DISCOUNT-020, METHOD-009, METHOD-010, METHOD-011, METHOD-012, METHOD-013, METHOD-014, PVM-001, PVM-002, PVM-003, PVM-004, PVM-005, PVM-006, V1-AC-032, V1-AC-033, V1-AC-034, V1-AC-035, V1-AC-036]
blockers: [W06-PENPOT-ANALYTICS-DENSITY-REPAIR, W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/agents/iteration_report_template.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/system-design.md
  - docs/architecture/bounded-context-map.md
  - docs/contracts/ui-route-contract.md
  - docs/contracts/ui-surface-contract.md
  - docs/generated/requirement-index.json
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-route-contracts.schema.json
  - packages/contracts/routes/ui-surface-contracts.json
  - packages/contracts/routes/ui-surface-contracts.schema.json
  - .codex/delivery/tickets/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
  - .codex/delivery/evidence/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
  - .codex/delivery/tickets/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
  - .codex/delivery/evidence/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
  - .codex/delivery/tickets/W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT.md
  - .codex/delivery/evidence/W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT.md
external_write_scope:
  provider: penpot
  file_id: 7cd71457-8d32-8044-8008-549f83bb4645
  expected_start_revision: 164
  allowed_operations: [create_components, create_component_board, edit_existing_target_frames, edit_existing_component_examples, edit_design_annotations, edit_prototype_flows]
  forbidden_operations: [create_or_replace_file, create_or_delete_stable_id_frames, rename_stable_ids, change_product_scope, change_route_identity, edit_other_penpot_files]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - docs/**
    - packages/**
    - apps/**
    - plugins/**
    - deploy/**
    - migrations/**
    - .codex/delivery/tickets/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/tickets/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
    - .codex/delivery/evidence/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
    - .codex/delivery/tickets/W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT.md
    - .codex/delivery/evidence/W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: [product-design:audit]
  commands:
    - confirm W06 and W07 are accepted with passed evidence
    - compute one ordered SHA-256 fingerprint over every context_sources file before the first Penpot write and compare it again before verdict
    - confirm Penpot currentFile.fileId equals 7cd71457-8d32-8044-8008-549f83bb4645 and current revision equals 164 before the first write
    - individually export and visually review C24, UI-DATA-008, UI-DATA-010, UI-DATA-013, UI-DATA-014, UI-DATA-021, UI-DATA-022, UI-AN-002, UI-AN-010, UI-AN-011, UI-AN-012, UI-AN-014, C17, UI-OVR-006, UI-OVR-012, and the ninth prototype flow after the final write
    - confirm all 110 route frames, 25 overlay/state frames, and 5 system surfaces retain stable unique UI-IDs with no duplicate missing or orphan IDs
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - git diff --check
  proof_boundary: canonical-penpot-product-0.9.2-ui-0.6.2-discount-methodology-visual-delta
  evidence_target: .codex/delivery/evidence/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence:
  - .codex/delivery/evidence/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
---

# Outcome

The canonical Penpot file visibly represents the accepted `0.9.2/0.6.2`
discount and methodology delta. Mapping, policy, metric certification, method
availability, Margin & Discounts, immutable result, Research, Result Trust, and
export preflight tell one compact, traceable story without a new route/overlay,
another design theme, or a second analytics engine.

# Non-goals

- Do not repeat W05/W06 as a full architecture audit or rewrite their evidence.
- Do not change blueprints, architecture, executable contracts, stable UI IDs,
  permissions, localization, or product scope.
- Do not implement browser/API/persistence/calculation/email/XLSX behavior or
  claim runtime, accessibility-runtime, analytical, performance, or release proof.
- Do not design causal inference, uplift, advanced anomaly, automated decision,
  marketing activation, or customer-specific code/UI forks.

# External write authority and guards

The only authorized external target is the existing Penpot file
`7cd71457-8d32-8044-8008-549f83bb4645`. Before writing, verify W06/W07 terminal
evidence, exact file ID, exact revision `164`, and one ordered fingerprint of
all context sources. Stop without writes on any mismatch, MCP unavailability,
concurrent revision drift, missing context file, or unresolved product meaning.
Repeat the identical fingerprint immediately before verdict.

# Work and repair boundary

Use `ui-ux-pro-max` as the primary execution skill, the Penpot MCP for design
writes, and `product-design:audit` for final visual proof. Preserve the Frost
tokens, Lucide mapping, compact 64 px KPI strip, W06 ordered MetricGroup tables,
on-demand Result Trust, aligned context/KPI boundaries, centered controls,
icon-only collapsed sidebar, and current route geometry.

Execute in this order:

1. Add component board `C24 Discount Components, Cap & PVM` without a stable
   UI route/overlay ID. Include direct/derived/proxy/total-only/unavailable
   badges, compact component table, stacking matrix, cap state, PVM waterfall
   plus data-table alternative, and accessible non-color status treatment.
2. Update `UI-DATA-008` with base price and promo/loyalty/bonus/other mapping,
   bonus redemption versus accrual, source total, attribution mode, and coverage.
3. Update `UI-DATA-010` with effective policy dates, stacking/precedence,
   accounting treatment, cap base/rate/components/tolerance/rounding/returns,
   historical no-clamp action, simulated publish block, and CompanyPack binding.
4. Update `UI-DATA-013/014` with lifecycle-independent candidate/verified/
   canonical/deprecated certification, direct/proxy quality, evidence, review,
   replacement, and impact without making cards airy.
5. Update `UI-DATA-021/022` with native/template/future/unsupported availability,
   default MethodologyPack, representativeness, robustness/sensitivity, evidence
   ceiling, and visible non-runnable future state.
6. Make `UI-AN-010` the golden slice: at most four compact KPIs; component
   amount/rate/share/penetration and `vs LY`; stacking/depth; cap diagnostics;
   exact price/volume/mix/assortment/residual reconciliation; margin and
   recognized revenue; linked table/drill-down; compact Result Trust trigger.
7. Update `UI-AN-002/011/012/014`, C17, `UI-OVR-006`, and `UI-OVR-012` so the
   same policy, attribution, certification, PVM method/order, coverage,
   residual, cap, limitations, and export disclosure remain visible.
8. Add prototype flow 09 from dataset mapping through policy/certification,
   Margin & Discounts, PVM/Result Trust, and Research/export return.

Promotion Journal overlap may appear as contextual evidence but must never
visually imply sale-level promo attribution. Historical cap breaches remain
source diagnostics; simulated breaches show a blocking state. First-client
50%/stacking values may appear only as a labelled CompanyPack configuration
example, not a platform default. Commercial discount, customer benefit, and
recognized net revenue must never share an ambiguous “total discount” label.

# Acceptance evidence

- Evidence records exact file ID, start/end revisions, repeated repository
  fingerprint, changed/created board IDs, and any compatible repair.
- C24 and every listed target receive an individual final visual verdict from
  fresh exports; flow 09 is structurally and visually traceable end to end.
- The final stable-ID scan is exactly 110 routes, 25 overlays, and 5 systems,
  with no duplicate, missing, orphaned, renamed, or deleted stable UI-ID.
- UI-AN-010 preserves W06 density/MetricGroup/Result Trust quality and clearly
  distinguishes components, totals, attribution quality, cap, PVM, and `vs LY`.
- Mapping/policy/metric/method states show lifecycle, effective dates, review,
  proxy/future limitations, errors, empty/partial/degraded/blocked states, and
  accessible labels without excessive whitespace, clipping, or overlap.
- Repository contracts and validators remain unchanged and pass. Evidence is
  design proof only; runtime/browser/accessibility/calculation/export proof is
  explicitly excluded.
