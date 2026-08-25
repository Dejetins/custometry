---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: G4@family.auth.shell-auth.baseline-exception-auth-r2
gate_id: G4
target_id: family.auth.shell-auth.baseline-exception-auth-r2
title: Family acceptance: family.auth.shell-auth.baseline-exception-auth
report_path: .codex/delivery/evidence/custometry-ui-design-program-v2/g4-r2/family-auth-shell-auth-baseline-exception-auth-family-report.md
proof_boundary: finished family review board with exact representative screen/state coverage, canonical browser evidence, responsive-Web proof, and accessibility smoke; no production implementation, deployment, performance, or full WCAG conformance proof
expected_touch_zones: .codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**
blocker_policy: needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for owner_required product meaning or finished-result review; hard-block only unsafe or unrecoverable conditions
decision_packet: none
resume_condition: none
resume_evidence_ref: none
Next stage allowed: false
execution_allowed: false
transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r2/family-auth-shell-auth-baseline-exception-auth/stage-transition.json
incoming_transition_receipt: none
incoming_transition_receipt_sha256: none
runtime_profile: codex.ui-stage-runtime-profiles/v1@1.6.0
execution_mode: goal_driven
goal_artifact_required: false
current_stage: G4@family.auth.shell-auth.baseline-exception-auth-r2
rendered_review_target: finished_visuals_only
known_stop_resolution: none
owner_review_target: finished_visuals_only
plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md

visual_authority:
  source_visual_ref: .codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v2/ru/source.html
  source_visual_sha256: d5639f0e20a79581972853979cd643ca456b6235c1ce098f5adc98d89636ca15
  source_evidence_mode: renderable_html
  owner_decision_ref: .codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/visual-authority-decision-v2.json
  screen_acceptance_scope: Visual-language and platform-baseline authority only; never exact target-screen composition, product semantics, fixture truth, legend-threshold truth, production implementation, or novel-screen fidelity.
  visual_language_scope: Linear Graphite shell character, calm professional density, compact contextual navigation, bounded analytical surfaces, concise KPI and command language, visible Result Trust, Focus/Explore character, readable analytical labels and tables, and adaptive external series-panel behavior as a visual-language reference.
  reusable_foundation_scope: Hash-pinned source-backed colors, typography stack, spacing rhythm, compact controls, rounded command language, shell/navigation relationships, overlay behavior, and analytical presentation primitives only; exact composition, information architecture, component implementation, runtime semantics, and target-screen acceptance remain later-gate work.
  inheritance_policy: required
  mobile_scope: unauthorized

prompt_pack_execution:
  plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
  prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
  stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md

context:
  always_read: [AGENTS.md, .codex/AGENTS.md, .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md]
  task_entrypoints: [.codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json, .codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/families/family.auth.shell-auth.baseline-exception-auth.json]
  conditional_bundles: [Read only the live ledger-bound context_manifest and named triggered bundles.]
  consult_if_needed: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md]

skills:
  primary: ui-design-program
  companions: [browser-qa-evidence, playwright-cli]

validation_strategy:
  proof_boundary: finished family review board with exact representative screen/state coverage, canonical browser evidence, responsive-Web proof, and accessibility smoke; no production implementation, deployment, performance, or full WCAG conformance proof
  evidence_target: .codex/delivery/evidence/custometry-ui-design-program-v2/g4-r2/family-auth-shell-auth-baseline-exception-auth-family-report.md
  commands: [ui_program_context, validate_ui_design_program, playwright-cli, validate_stage_ledger, assemble_stage_transition, validate_stage_transition]

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

Execute only `G4@family.auth.shell-auth.baseline-exception-auth-r2` when the ledger independently selects and claims it. Complete one bounded family review unit from the accepted G2 structure and G3 foundations.

## Context / Current State

Use the accepted revision-2 product intent, exact platform baseline, visual-language authority limits, responsive-Web contract, and mobile scope `unauthorized`. Do not infer exact target composition from the candidate.

## Requirements

Run the ledger-bound context workflow before claim, validate the exact incoming transition, claim atomically, regenerate context, and consume only the emitted manifest. Produce finished visuals and canonical browser evidence before owner review.

# Context acquisition protocol

Read only the bounded post-claim manifest, exact pointers, and triggered bundles. Expand only for a named failed binding or validator error.

# Reading manifest

Respect the live profile limits of 16 files and approximately 600k estimated tokens.

# Work plan

1. Revalidate status, triad, ledger, and incoming transition.
2. Claim only this row and regenerate context.
3. Build the exact bounded family artifacts and browser evidence.
4. Assemble the typed review board and strict gate evidence.
5. Enter `needs_input` with `review_ready`; accept only after natural-language owner acceptance is canonically recorded.

# Acceptance criteria

The family aggregate exact-covers every declared representative screen/state and passes `family_acceptance` before finished-result review.

# Implementation constraints

Do not change product semantics, accepted baseline authority, mobile scope, production code, publication state, deployment, secrets, or another family/wave. Do not hand-edit receipts.

# Quality gates

Run the emitted runtime-profile commands, canonical `playwright-cli` evidence, the strict aggregate validator, ledger validation, and adjacent transition validation.

# Adjacent-stage preflight

Current-gate success alone never allows the next row. G4 closes from one exact-cover family aggregate; G5 closes from one exact-cover wave aggregate.

# Final output

Show the finished review board, material exceptions, concise validation boundary, and at most three genuine owner questions. Keep raw JSON and hashes in linked evidence.
