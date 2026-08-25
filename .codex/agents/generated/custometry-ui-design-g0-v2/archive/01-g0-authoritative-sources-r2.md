---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2
gate_id: G0
target_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2
title: Authoritative sources and platform baseline reconciliation r2
report_path: .codex/delivery/evidence/custometry-ui-design-program-v2/g0-r2-execution-report.md
proof_boundary: documentation authority, complete candidate file/hash provenance, current-source freshness, promoted-requirement reconciliation, accepted platform-baseline contracts, and control-plane validation; no target-screen design, browser runtime, implementation, accessibility-conformance, responsive-behavior, performance, publication, deployment, or mobile-specific proof
expected_touch_zones: .codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**, custometry-ui-blueprint-ru.md, docs/generated/requirement-index.json
blocker_policy: needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for owner_required product meaning; hard-block only unsafe or unrecoverable conditions
decision_packet: none
resume_condition: none
resume_evidence_ref: none
Next stage allowed: true
execution_allowed: true
transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/stage-transition.json
incoming_transition_receipt: none
incoming_transition_receipt_sha256: none
runtime_profile: codex.ui-stage-runtime-profiles/v1@1.6.0
execution_mode: goal_driven
goal_artifact_required: false
current_stage: G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2
rendered_review_target: none
known_stop_resolution: none
owner_review_target: non_visual_summary_for_G0-G2
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
  task_entrypoints: [.codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/visual-authority-decision-v2.json, .codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/requirement-reconciliation.json, .codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/ui-program-intake.json, .codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/platform-ui-baseline.json]
  conditional_bundles: [Read only the live ledger-bound context_manifest and named triggered bundles.]
  consult_if_needed: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/ui-route-contracts.json, packages/contracts/routes/ui-surface-contracts.json]

skills:
  primary: ui-design-program
  companions: []

validation_strategy:
  proof_boundary: documentation authority, complete candidate file/hash provenance, current-source freshness, promoted-requirement reconciliation, accepted platform-baseline contracts, and control-plane validation; no target-screen design, browser runtime, implementation, accessibility-conformance, responsive-behavior, performance, publication, deployment, or mobile-specific proof
  evidence_target: .codex/delivery/evidence/custometry-ui-design-program-v2/g0-r2-execution-report.md
  commands: [ui_program_context, validate_ui_design_program, validate_stage_ledger, assemble_stage_transition, validate_stage_transition]

file_manifest:
  expected_touch_zones: [.codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**, custometry-ui-blueprint-ru.md, docs/generated/requirement-index.json]
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

Execute only `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2` when the ledger independently selects and claims it. Reconcile current canonical sources, all 74 pilot-candidate-v2 files and hashes, 68 OWNER-REC entries, 13 RECON-ADD requirements, conflicts, later-stage obligations, the canonical UI blueprint, and the revision-2 intake/platform baseline. Validate G0 and assemble only the adjacent G1 transition.

## Context / Current State

Revision 1 remains immutable historical evidence. Revision 2 uses the current canonical product/UI sources and the candidate only as visual-language/platform-baseline authority. Responsive Web is required; mobile-specific IA remains unauthorized.

## Requirements

Run `ui_program_context.py --ledger .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md --project-root <root>` before claim, validate the exact incoming transition when present, claim atomically, regenerate context immediately, and consume only the emitted manifest. Preserve foreign changes and all authority limits.

# Context acquisition protocol

Read only the bounded post-claim manifest, exact pointers, and triggered bundles. Expand only for a named failed binding or validator error.

# Reading manifest

Respect the live profile limits of 16 files and approximately 600k estimated tokens.

# Work plan

1. Revalidate git status, triad, ledger, and incoming transition.
2. Claim only this stage and regenerate the ledger-bound context.
3. Build only the stage-owned deterministic artifacts and evidence.
4. Run the emitted gate, ledger, source-freshness, exact-cover, and adjacent-transition checks.
5. Update the ledger before reporting; never claim the adjacent stage without independent authorization.

# Acceptance criteria

intake_ready, baseline_ready, draft, source freshness, prompt/ledger synchronization, G0 gate, and the G0-to-G1 transition all pass; G1 remains unclaimed.

# Implementation constraints

Do not rewrite r1 artifacts or receipts, hand-edit generated receipts, infer target-screen composition from the candidate, grant fixture/legend-threshold/mobile/production authority, mutate production code, publish, deploy, commit, push, create a PR, use secrets, or perform external side effects.

# Quality gates

Run the live profile-emitted commands, stage-specific deterministic builders/validators, `source scripts/activate-toolchain.sh`, and the smallest applicable repository local gate.

# Adjacent-stage preflight

Validate both the current gate and the exact adjacent transition receipt. Current-gate success alone never allows the next stage.

# Final output

Report stage status, changed paths, exact ledger state, validation results, proof boundary, excluded foreign changes, residual risks, and one safe next action in Russian.

## Execution control

Keep decision policy, file manifest, transition receipt, and `Next stage allowed` synchronized with the ledger. G0-G2 have no routine owner acceptance. Never infer acceptance from readiness alone.
