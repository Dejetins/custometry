---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: G1@atlas-r1
gate_id: G1
target_id: atlas-r1
title: Complete exact-cover screen atlas
report_path: .codex/delivery/evidence/custometry-ui-design-program-v2/g1-atlas-report.md
proof_boundary: machine-rendered exact-cover atlas and source reconciliation; no target screen design, browser runtime, accessibility-conformance, responsive-behavior, or performance proof
expected_touch_zones: .codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**
blocker_policy: needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for owner_required product meaning; hard-block only unsafe or unrecoverable conditions
decision_packet: none
resume_condition: none
resume_evidence_ref: none
Next stage allowed: false
execution_allowed: true
transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/g1/stage-transition.json
incoming_transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/g0/stage-transition.json
incoming_transition_receipt_sha256: pending-g0-closure
runtime_profile: codex.ui-stage-runtime-profiles/v1@1.6.0
execution_mode: manual_sequential
goal_artifact_required: false
current_stage: G1@atlas-r1
rendered_review_target: none
known_stop_resolution: none
owner_review_target: non_visual_summary_for_G0-G2
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
  task_entrypoints: [.codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json, .codex/delivery/ui-design-programs/custometry-v2/ui-program-intake.json, .codex/delivery/ui-design-programs/custometry-v2/evidence/g0/stage-transition.json]
  conditional_bundles: [Read individual source manifests only when source reconciliation fails.]
  consult_if_needed: [custometry-ui-blueprint-ru.md, packages/contracts/routes/ui-routes.json, packages/contracts/routes/ui-route-contracts.json, packages/contracts/routes/ui-surface-contracts.json]

skills:
  primary: ui-design-program
  companions: []

validation_strategy:
  proof_boundary: machine-rendered exact-cover atlas and source reconciliation; no target screen design, browser runtime, accessibility-conformance, responsive-behavior, or performance proof
  evidence_target: .codex/delivery/evidence/custometry-ui-design-program-v2/g1-atlas-report.md
  commands: [ui_program_context, atlas_gate, render_screen_atlas, validate_stage_ledger, assemble_stage_transition, validate_stage_transition]

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

Execute only `G1@atlas-r1` after a hash-current accepted G0 transition makes this row claimable. Build the complete exact-cover screen atlas from the accepted intake without designing target screens or advancing to G2.

## Context / Current State

The G0 artifacts and incoming transition receipt are the sole admission boundary. Responsive Web is required and mobile-specific scope remains `unauthorized`.

## Requirements

Generate and consume the ledger-bound G1 `context_manifest`. Reconcile every current route, flow, persistent shell, route-backed transient, overlay, system-state family, internal/non-visual surface, justified historical exclusion, and new target capability family exactly once.

# Context acquisition protocol

Read the bounded manifest and expand only for a specific failed source binding.

# Reading manifest

Keep baseline context to at most eight files and about 40k tokens.

# Work plan

1. Validate the incoming G0 receipt and claim only this row.
2. Build immutable screen and journey shard indexes with exact-cover reconciliation.
3. Render the atlas and validate `atlas_gate`.
4. Assemble and validate the G2 adjacent-stage transition, update the ledger, and stop.

# Acceptance criteria

Every authoritative intake surface is represented exactly once, counts derive from the live indexes, exclusions remain justified, the rendered atlas is current, and no G2 identifiers or structure work are invented inside G1.

# Implementation constraints

Do not execute this prompt during the authorized G0 unit. Do not design screens, mutate production code, create mobile IA, publish, or infer browser/runtime proof.

# Quality gates

Run the profile-emitted atlas validator, rendered-atlas check, ledger validator, transition assembler, and transition validator.

# Adjacent-stage preflight

Require hash-pinned screen and journey indexes, a current rendered atlas, exact-cover reconciliation, and one unambiguous G2 entry before allowing the next stage.

# Final output

Report the atlas outcome, machine evidence, proof boundary, residual risks, and one next action in Russian without dumping the full inventory.

## Execution control

Apply `decision_policy`; keep `decision_packet`, `resume_condition`, and `resume_evidence_ref` exact. Before closure, update the ledger with validation commands/results, evidence and transition hashes, file manifest, residual risk, the adjacent incoming receipt, and the exact `Next stage allowed` value. Never infer acceptance from readiness alone.
