---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
ticket_id: W08-PENPOT-ANALYTICS-BASELINE-RECOVERY
status: accepted
workstream_id: W08
summary: Recover the canonical Penpot analytics baseline after unexpected post-acceptance drift by restoring UI-AN-002 and removing the UI-AN-011 configuration overlap without changing product or route identity.
requirement_ids: [UC-027, METRIC-014, METRIC-015, DISCOUNT-017, DISCOUNT-018, V1-AC-021, V1-AC-034]
blockers: [W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/agents/iteration_report_template.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/contracts/ui-route-contract.md
  - docs/contracts/ui-surface-contract.md
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-route-contracts.schema.json
  - packages/contracts/routes/ui-surface-contracts.json
  - packages/contracts/routes/ui-surface-contracts.schema.json
  - .codex/delivery/tickets/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
  - .codex/delivery/evidence/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
  - .codex/delivery/tickets/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
  - .codex/delivery/evidence/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
  - .codex/delivery/tickets/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
external_write_scope:
  provider: penpot
  file_id: 7cd71457-8d32-8044-8008-549f83bb4645
  expected_start_revision: 185
  allowed_operations: [restore_missing_stable_route_frame, edit_existing_target_frame, edit_design_annotations, repair_prototype_link]
  forbidden_operations: [create_or_replace_file, delete_existing_stable_id_frames, rename_other_stable_ids, change_product_scope, change_route_identity, edit_other_penpot_files, start_w10_delta]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W08-PENPOT-ANALYTICS-BASELINE-RECOVERY.md
    - .codex/delivery/evidence/W08-PENPOT-ANALYTICS-BASELINE-RECOVERY.md
    - custometry-ui-blueprint-ru.md
    - docs/contracts/ui-surface-contract.md
    - .codex/delivery/tickets/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - docs/architecture/**
    - packages/**
    - apps/**
    - plugins/**
    - deploy/**
    - migrations/**
    - .codex/delivery/tickets/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
    - .codex/delivery/evidence/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
    - .codex/delivery/tickets/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: [product-design:audit]
  commands:
    - confirm canonical Penpot file ID and exact revision 185 before the first design write
    - confirm serial revision guards remain stable and compute the ordered context_sources SHA-256 fingerprint before the first design write
    - restore UI-AN-002 from the accepted W08 baseline metadata, design evidence, Frost shell patterns, and active route contracts
    - remove unintended UI-AN-011 overlap by integrating W08 content into the existing Configuration and Metric groups regions
    - individually export and visually review UI-AN-002 and UI-AN-011 after the final design write
    - confirm exactly 110 route frames, 25 overlay frames, and 5 system surfaces with no duplicate missing or orphan UI-ID
    - confirm Penpot currentFile.validate returns no errors
    - repeat the identical ordered context_sources fingerprint immediately before verdict
    - uv run python -m tools.custometry_quality.validate_blueprints
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.check_docs_links
    - uv run python -m tools.custometry_quality.generate_docs_index --check
    - source scripts/activate-toolchain.sh && uv run --locked python -m tools.check --scope local
    - git diff --check
  proof_boundary: canonical-penpot-analytics-baseline-recovery-after-revision-181
  evidence_target: .codex/delivery/evidence/W08-PENPOT-ANALYTICS-BASELINE-RECOVERY.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence:
  - .codex/delivery/evidence/W08-PENPOT-ANALYTICS-BASELINE-RECOVERY.md
---

# Outcome

The canonical Penpot baseline contains the contract-backed UI-AN-002 route
frame again and UI-AN-011 presents discount-methodology content inside its
existing Configuration and Metric groups regions without overlap. Historical
W08 acceptance at revision 181 remains immutable; the recovery terminal
revision becomes the current baseline for W10.

# Non-goals

- Do not rewrite W08 ticket/evidence or reinterpret revision 181.
- Do not change product requirements, route identity, machine/human blueprints,
  architecture, executable contracts, permissions, or localization.
- Do not start or partially implement the W10 Organization/People delta.
- Do not claim browser, runtime, accessibility-runtime, calculation, export,
  authorization, deployment, or release proof.

# Work and repair boundary

Recover only UI-AN-002 on page 24 Analytics, repair only the overlapping W08
delta inside UI-AN-011, and restore the flow-09 link into UI-AN-002 when
needed. Preserve Frost, W06 density, W08 methodology semantics, the exact
stable UI-ID strings, and every other stable frame. Repository follow-up is
limited to the current UI baseline references in the UI blueprint, UI surface
contract, and ready W10 ticket.

# Acceptance evidence

- Start/end revisions, canonical file ID, repeated ordered fingerprint, restored
  and changed board IDs, and any bounded repair are recorded.
- Fresh individual exports of UI-AN-002 and UI-AN-011 pass clipping, overlap,
  alignment, density, and structural visual review.
- Stable-ID reconciliation is exactly 110 routes, 25 overlays, and 5 systems
  with empty duplicate, missing, and orphan lists.
- Penpot validation and every declared repository validator pass.
- W10 stays ready, references the recovery ticket/evidence, and starts from the
  recovery terminal revision; W10 itself is not executed.
