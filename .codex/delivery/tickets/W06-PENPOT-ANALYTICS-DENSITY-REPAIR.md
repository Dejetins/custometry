---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.1-draft
ticket_id: W06-PENPOT-ANALYTICS-DENSITY-REPAIR
status: accepted
workstream_id: W06
summary: Repair the canonical Penpot analytics result presentation so ordered MetricGroup tables and compact on-demand Result Trust are visually demonstrable without changing any route or product contract.
requirement_ids: [UC-017, UC-020, METRIC-009, METRIC-010, METRIC-011, METRIC-012, METRIC-013, METRIC-014, METRIC-015, METRIC-016, CHART-015, A11Y-006, A11Y-007, REPORT-008, UX-JOURNEY-005, V1-AC-020, V1-AC-021, V1-AC-023]
blockers: [W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/agents/iteration_report_template.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/contracts/ui-route-contract.md
  - docs/contracts/ui-surface-contract.md
  - docs/generated/requirement-index.json
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-surface-contracts.json
  - .codex/delivery/tickets/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
  - .codex/delivery/evidence/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
external_write_scope:
  provider: penpot
  file_id: 7cd71457-8d32-8044-8008-549f83bb4645
  expected_start_revision: 159
  allowed_operations: [edit_existing_target_frames, edit_existing_component_examples, edit_design_annotations]
  forbidden_operations: [create_or_replace_file, create_or_delete_stable_id_frames, rename_stable_ids, change_product_scope, change_route_identity, edit_other_penpot_files]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
    - .codex/delivery/evidence/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
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
    - .codex/delivery/tickets/W00-RESET-DELIVERY-MODEL.md
    - .codex/delivery/tickets/W01-EXPAND-TARGET-SYSTEM-DESIGN.md
    - .codex/delivery/tickets/W02-RECONCILE-UI-SURFACE-CONTRACT.md
    - .codex/delivery/tickets/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
    - .codex/delivery/tickets/W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT.md
    - .codex/delivery/tickets/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W00-RESET-DELIVERY-MODEL.md
    - .codex/delivery/evidence/W01-EXPAND-TARGET-SYSTEM-DESIGN.md
    - .codex/delivery/evidence/W02-RECONCILE-UI-SURFACE-CONTRACT.md
    - .codex/delivery/evidence/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
    - .codex/delivery/evidence/W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT.md
    - .codex/delivery/evidence/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: ["product-design:audit"]
  commands:
    - confirm W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION is accepted with passed evidence
    - record one SHA-256 fingerprint over the complete ordered context_sources set before the first Penpot write and compare it again before verdict
    - confirm Penpot currentFile.fileId equals 7cd71457-8d32-8044-8008-549f83bb4645 and current revision equals 159 before the first write
    - individually export and visually review C11, C17, C23 Metric Group and Number Format Preview, UI-OVR-006, UI-AN-003 through UI-AN-012, and UI-AN-014 after the final write
    - confirm all 110 route frames, 25 overlay/state frames, and 5 system surfaces retain their stable IDs with no duplicate or missing IDs
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - git diff --check
  proof_boundary: canonical-penpot-analytics-metric-group-and-result-trust-visual-repair
  evidence_target: .codex/delivery/evidence/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md]
---

# Outcome

The existing canonical Penpot file visibly demonstrates the current reportable
result contract: ordered MetricGroup tables with typed current/comparison values
and a compact Result Trust trigger that opens a dense on-demand drawer. The
repair applies this representation to report-like analytics and Research
Workspace surfaces without adding a route, a new stable UI-ID, a product
requirement, or a new theme.

# Non-goals

- Do not modify blueprints, executable UI contracts, route identities,
  permissions, architecture, W05, or any other accepted ticket/evidence.
- Do not create, replace, delete, or rename a stable Penpot frame or create a
  new Penpot file.
- Do not claim browser, runtime, keyboard, authorization, analytical, export,
  or accessibility-runtime proof.
- Do not replace the Frost design system, introduce an additional theme, or
  add business metrics not already representable by the governing metric,
  chart, and report contracts.

# Work and repair boundary

Edit only the existing C11 Components / Overlays board
(e451483d-aae3-807d-8008-54a67a41bb17), C17 Components / Result Trust board
(e451483d-aae3-807d-8008-54a6e546060f), the C23 Metric Group & Number Format
Preview component example, UI-OVR-006, UI-AN-003 through UI-AN-012, and
UI-AN-014.

Each report-like analytics frame must retain the 64 px KPI strip and use its
existing chart/table state to show an ordered table alternative with at least
two named metric groups, group headers, ordered metric rows, current value,
previous-year value, delta, and full-value/accessibility annotation. Use
screen-appropriate presentation examples only; never make a formatted value
the computational or route identity.

Result Trust remains a compact trigger in analytical layout. C11 must show a
compact, bounded drawer specimen rather than a permanent empty column. C17 and
UI-OVR-006 must show the dense on-demand drawer with as-of/freshness, quality,
dataset and metric versions, grain, filters, comparison/time policy, currency,
lineage, limitations, and a return/close control. The C23 example must visibly
demonstrate MetricGroupVersion ordering and NumberFormatSpec presentation in a
table, not a loose text list.

Stop active work if the canonical file ID or revision differs, the ordered
repository fingerprint changes, Penpot MCP is unavailable, a new product,
permission, or route ambiguity appears, or the file changes during execution.

# Acceptance evidence

- Start/end Penpot revision, canonical file ID, and repeated context fingerprint
  are recorded.
- All target board/frame stable IDs remain unchanged; the final global scan is
  exactly 110 routes, 25 overlays, and 5 system surfaces with no duplicate or
  missing UI-ID.
- The listed 15 target boards/frames receive individual final visual verdicts.
- Each UI-AN-003 through UI-AN-012 and UI-AN-014 visibly contains an ordered
  MetricGroup table or metric-group research block; C11/C17/UI-OVR-006 visibly
  keep Result Trust on demand and dense.
- The route registry, both JSON Schemas, delivery-ticket validator, and
  git diff --check pass.
- Evidence is terminal only when the complete repair is present; otherwise
  leave the ticket active or record a truthful blocker.
