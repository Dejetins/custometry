---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: G6@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r1
gate_id: G6
target_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2
title: Cross-program QA and implementation handoff
report_path: .codex/delivery/evidence/custometry-ui-design-program-v2/g6-handoff-report.md
proof_boundary: cross-program review board, critical-journey proof, and reproducible implementation handoff; no publication, deployment, production, or full WCAG conformance proof
expected_touch_zones: .codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**
blocker_policy: needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for owner_required product meaning; hard-block only unsafe or unrecoverable conditions
decision_packet: none
resume_condition: none
resume_evidence_ref: none
Next stage allowed: false
execution_allowed: false
transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/g6/stage-transition.json
incoming_transition_receipt: none
incoming_transition_receipt_sha256: none
runtime_profile: codex.ui-stage-runtime-profiles/v1@1.6.0
execution_mode: manual_sequential
goal_artifact_required: false
current_stage: G6@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r1
rendered_review_target: .codex/delivery/ui-design-programs/custometry-v2/evidence/g6/review-board.html
known_stop_resolution: none
owner_review_target: finished_visuals_only_for_G3-G6
plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md
visual_authority:
  source_visual_ref: .codex/delivery/ui-design-programs/custometry-v2/evidence/pilot/ru/source.html
  source_visual_sha256: 9d82b59fdf766ccc2b72616fa2c0945d99e1110794be4698c049f232425be780
  source_evidence_mode: renderable_html
  owner_decision_ref: .codex/delivery/ui-design-programs/custometry-v2/evidence/g0/visual-authority-decision-v1.json
  screen_acceptance_scope: Visual-language anchor only; no exact-screen fidelity authority for novel or target surfaces.
  visual_language_scope: Calm professional character, compact analytical density, concise KPI and context chrome, visible Result Trust, Focus/Explore interaction character, and independent RU/EN content-stress evidence.
  reusable_foundation_scope: Only source-backed primitives measured into the G0 platform baseline; exact composition, information architecture, responsive acceptance, and implementation remain excluded.
  inheritance_policy: required
  mobile_scope: unauthorized
prompt_pack_execution:
  plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
  prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
  stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md
context:
  always_read: [AGENTS.md, .codex/AGENTS.md, .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md]
  task_entrypoints: [.codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json]
  conditional_bundles: []
  consult_if_needed: []
skills:
  primary: ui-design-program
  companions: [browser-qa-evidence, playwright-cli]
validation_strategy:
  proof_boundary: cross-program review board, critical-journey proof, and reproducible implementation handoff; no publication, deployment, production, or full WCAG conformance proof
  evidence_target: .codex/delivery/evidence/custometry-ui-design-program-v2/g6-handoff-report.md
  commands: [ui_program_context, handoff_ready, browser capture, validate_stage_ledger, assemble_stage_transition, validate_stage_transition]
file_manifest:
  expected_touch_zones: [.codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**]
  foreign_changes_excluded: true
safety:
  recoverable_input_policy: needs_input_and_resume_same_stage
  hard_blocker_policy: terminal_blocked_only_for_unsafe_or_unrecoverable_state
  mobile_scope: unauthorized_unless_exact_user_authorization_is_cited
  agent_self_acceptance: prohibited
  repeated_write_authorization: prohibited_when_current_task_already_authorizes_owned_paths
owner_interaction:
  raw_json_review: prohibited_by_default
  full_screen_inventory_review: prohibited_by_default
  max_questions_per_checkpoint: 3
  magic_acceptance_string_required: false
---

# Task

This row is a non-executable topology placeholder. G2 must first create exact G4/G5 rows, and G6 dependencies and prompt bindings must then be synchronized to all accepted waves. Only after later explicit stage authority may G6 produce the final review board and implementation handoff. Do not run during G0.

## Execution control

Apply `decision_policy`; keep `decision_packet`, `resume_condition`, and `resume_evidence_ref` exact. Before closure, update the ledger with validation commands/results, evidence and transition hashes, file manifest, residual risk, the adjacent incoming receipt, and the exact `Next stage allowed` value. Never infer acceptance from readiness alone.
