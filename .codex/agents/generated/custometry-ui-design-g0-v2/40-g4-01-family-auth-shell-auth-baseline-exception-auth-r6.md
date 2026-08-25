---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: G4@family.auth.shell-auth.baseline-exception-auth-r6
gate_id: G4
target_id: family.auth.shell-auth.baseline-exception-auth-r6
title: Blueprint semantic rebind successor G4: family.auth.shell-auth.baseline-exception-auth-r6
report_path: .codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r6/family-auth-shell-auth-baseline-exception-auth/review-board.html
proof_boundary: current-contract stage evidence and adjacent-stage readiness; no production implementation, publication, deployment, mobile-specific design, or full WCAG conformance proof
expected_touch_zones: .codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**
blocker_policy: needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for owner_required decisions
decision_packet: .codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth/owner-review-decision-packet.json
resume_condition: owner_accepts_or_requests_bounded_corrections_for_exact_finished_g4_auth_r6_board
resume_evidence_ref: .codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth/owner-input-response-acceptance-r6.json
Next stage allowed: false
execution_allowed: false
transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth/stage-transition.json
incoming_transition_receipt: none
incoming_transition_receipt_sha256: none
runtime_profile: codex.ui-stage-runtime-profiles/v1@2.0.0
execution_mode: bounded_stage_resume
goal_artifact_required: false
current_stage: G4@family.auth.shell-auth.baseline-exception-auth-r6
rendered_review_target: finished_rendered_result
known_stop_resolution: none
owner_review_target: finished_visuals_only
source_visual_ref: .codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v3-metadata/ru/source.html
source_visual_sha256: b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700
source_evidence_mode: renderable_html
owner_decision_ref: .codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r4/visual-authority-decision-r4.json
screen_acceptance_scope: Visual-language and platform-baseline authority only; never exact target-screen composition, product semantics, fixture truth, legend-threshold truth, production implementation, or novel-screen fidelity.
visual_language_scope: Linear Graphite shell character, calm professional density, compact contextual navigation, bounded analytical surfaces, concise KPI and command language, visible Result Trust, Focus/Explore character, readable analytical labels and tables, and adaptive external series-panel behavior as a visual-language reference.
reusable_foundation_scope: Hash-pinned source-backed colors, typography stack, spacing rhythm, compact controls, rounded command language, shell/navigation relationships, overlay behavior, and analytical presentation primitives only; exact composition, information architecture, component implementation, runtime semantics, and target-screen acceptance remain later-gate work.
inheritance_policy: required
mobile_scope: unauthorized
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
  primary: staged-plan-runner
  companions: [ui-design-program, root-cause-debugging, better-writing, better-layout, better-ui, better-accessibility, browser-qa-evidence, playwright-cli]

validation_strategy:
  focused_first: true
  active_profile: family_review_ready
  browser_mechanic: playwright-cli
  repository_gate: uv run python -m tools.check --scope local
  proof_limit: local_file_and_loopback_responsive_web_only

file_manifest:
  required: true
  categories: [owned_changed, generated_evidence, foreign_preserved, outside_expected_paths]
  durable_report: .codex/delivery/evidence/custometry-ui-design-program-v2/family.auth.shell-auth.baseline-exception-auth-r6-report.md

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

Execute only `G4@family.auth.shell-auth.baseline-exception-auth-r6` after bounded ledger context and an atomic claim. Rebuild the auth family under the current r5 program semantics using accepted r5 artifacts as read-only historical inputs, produce only unique r6 contracts, renders, receipts, decision packet, report, and transition, then stop at the finished-visual owner checkpoint. Preserve foreign changes and never overwrite or revive accepted r5 evidence.
