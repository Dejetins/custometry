---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4
gate_id: G0
target_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4
title: Repaired active-contract successor G0: CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4
report_path: .codex/delivery/evidence/custometry-ui-design-program-v2/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4-report.md
proof_boundary: current-contract source authority, exact-cover pilot standard, metadata-only equivalence, owner-reviewed baseline, and adjacent-stage readiness; no production implementation, publication, deployment, mobile-specific design, or full WCAG conformance proof
expected_touch_zones: .codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**
blocker_policy: needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for exact visual-authority and baseline owner acceptance
decision_packet: none
resume_condition: none
resume_evidence_ref: none
Next stage allowed: false
execution_allowed: true
transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4/stage-transition.json
incoming_transition_receipt: none
incoming_transition_receipt_sha256: none
runtime_profile: codex.ui-stage-runtime-profiles/v1@2.0.0
execution_mode: goal_driven
goal_artifact_required: false
current_stage: G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4
rendered_review_target: compact_successor_baseline_and_visual_authority_board
known_stop_resolution: shared_writer_and_canonical_owner_decision_repairs_verified
owner_review_target: exact_successor_pilot_baseline_clause_inventory_and_rendered_standard_board
plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md

prompt_pack_execution:
  plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
  prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
  stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md

context:
  always_read: [AGENTS.md, .codex/AGENTS.md, .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md]
  task_entrypoints: [.codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r4/repair-evidence.json, .codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v3-metadata/derivation-receipt.json]
  conditional_bundles: [Read only the live ledger-bound context_manifest and named triggered bundles.]
  consult_if_needed: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/ui-route-contracts.json]

skills:
  primary: ui-design-program
  companions: []

safety:
  recoverable_input_policy: needs_input_and_resume_same_stage
  hard_blocker_policy: terminal_blocked_only_for_unsafe_or_unrecoverable_state
  mobile_scope: unauthorized_unless_exact_user_authorization_is_cited
  agent_self_acceptance: prohibited

owner_interaction:
  raw_json_review: prohibited_by_default
  magic_acceptance_string_required: false
---

# Task

Execute only `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4` after bounded ledger context and an atomic claim. Complete the exact-cover pilot standard and successor baseline, render the compact comparison/standard board, reach `review_ready`, and request the one mandatory natural-language owner decision. Preserve historical evidence, accepted v2 bytes, the metadata-only v3 candidate lineage, and foreign changes. Do not claim G1 across the owner checkpoint.
