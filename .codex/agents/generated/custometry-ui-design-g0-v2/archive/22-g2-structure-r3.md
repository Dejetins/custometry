---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3
gate_id: G2
target_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3
title: Active-contract successor G2: CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3
report_path: .codex/delivery/evidence/custometry-ui-design-program-v2/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3-report.md
proof_boundary: current-contract stage evidence and adjacent-stage readiness; no production implementation, publication, deployment, mobile-specific design, or full WCAG conformance proof
expected_touch_zones: .codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**
blocker_policy: needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for owner_required decisions
decision_packet: none
resume_condition: none
resume_evidence_ref: none
Next stage allowed: false
execution_allowed: false
transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3/stage-transition.json
incoming_transition_receipt: none
incoming_transition_receipt_sha256: none
runtime_profile: codex.ui-stage-runtime-profiles/v1@2.0.0
execution_mode: goal_driven
goal_artifact_required: false
current_stage: G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3
rendered_review_target: non_visual_summary_for_G0-G2
known_stop_resolution: none
owner_review_target: non_visual_summary_for_G0-G2
plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md

prompt_pack_execution:
  plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
  prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
  stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md

context:
  always_read: [AGENTS.md, .codex/AGENTS.md, .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md]
  task_entrypoints: [.codex/delivery/ui-design-programs/custometry-v2/evidence/compatibility-migration-r3/prepared/historical-control-plane-migration-receipt.json]
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

Execute only `G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3` after bounded ledger context and an atomic claim. Use the current active contract, preserve historical evidence and foreign changes, satisfy the exact gate and adjacent-stage preflight, then durably update the sole stage ledger. Do not claim another row across an owner checkpoint.
