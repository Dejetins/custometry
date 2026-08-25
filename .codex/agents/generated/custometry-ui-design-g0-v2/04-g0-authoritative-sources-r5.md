---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5
gate_id: G0
target_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5
title: Blueprint semantic rebind successor G0: CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5
report_path: .codex/delivery/evidence/custometry-ui-design-program-v2/g0-r5-source-rebind-report.md
proof_boundary: current-contract source authority, exact-cover pilot standard, metadata-only equivalence, owner-reviewed baseline, and adjacent-stage readiness; no production implementation, publication, deployment, mobile-specific design, or full WCAG conformance proof
expected_touch_zones: .codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**
blocker_policy: needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for exact visual-authority and baseline owner acceptance
decision_packet: none
resume_condition: none
resume_evidence_ref: none
Next stage allowed: false
execution_allowed: true
transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r5/stage-transition.json
incoming_transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/blueprint-rebind-r5/active-semantic-migration/prepared/historical-control-plane-migration-receipt.json
incoming_transition_receipt_sha256: 4c1d8bf79c297882ace7366cf9ead14c3b77924131f4b2c771cdc515130b21a6
runtime_profile: codex.ui-stage-runtime-profiles/v1@2.0.0
execution_mode: goal_driven
goal_artifact_required: false
current_stage: G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5
rendered_review_target: none_inherited_visual_baseline
known_stop_resolution: shared_writer_and_canonical_owner_decision_repairs_verified
owner_review_target: none_inherited_visual_baseline
plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md

prompt_pack_execution:
  plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
  prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
  stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md

context:
  always_read: [AGENTS.md, .codex/AGENTS.md, .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md]
  task_entrypoints: [.codex/delivery/ui-design-programs/custometry-v2/evidence/blueprint-rebind-r5/active-semantic-migration/prepared/historical-control-plane-migration-receipt.json]
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

Execute only `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5` after bounded ledger context and an atomic claim. Rebind the accepted blueprint semantics and current surface contract to the inherited hash-pinned visual baseline, verify exact source coverage and adjacent G1 readiness, then durably update the sole stage ledger. Preserve all accepted visual bytes, historical evidence, and foreign changes. This semantic rebind creates no new visual-authority decision and must not claim G1.
