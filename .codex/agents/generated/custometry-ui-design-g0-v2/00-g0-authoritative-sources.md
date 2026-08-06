---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r1
gate_id: G0
target_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2
title: Authoritative sources and platform baseline
report_path: .codex/delivery/evidence/custometry-ui-design-program-v2/g0-execution-report.md
proof_boundary: documentation authority, hash-pinned source provenance, intake and platform-baseline contracts, and control-plane validation; no browser, runtime, implementation, accessibility-conformance, responsive-behavior, or performance proof
expected_touch_zones: .codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/**, docs/architecture/ui/**, docs/architecture/**, docs/adr/**
blocker_policy: needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for owner_required product meaning; hard-block only unsafe or unrecoverable conditions
decision_packet: none
resume_condition: none
resume_evidence_ref: none
Next stage allowed: true
execution_allowed: true
transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/g0/stage-transition.json
incoming_transition_receipt: none
incoming_transition_receipt_sha256: none
runtime_profile: codex.ui-stage-runtime-profiles/v1@1.6.0
execution_mode: manual_sequential
goal_artifact_required: false
current_stage: G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r1
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
  task_entrypoints: [.codex/delivery/ui-design-programs/custometry-v2/evidence/g0/owner-intent.json, .codex/delivery/ui-design-programs/custometry-v2/evidence/g0/pilot-import-receipt.json, docs/adr/0007-responsive-web-frontend-platform.md]
  conditional_bundles: [Read the machine and human technical blueprints and nearest architecture sources only through the live G0 context manifest.]
  consult_if_needed: [.codex/delivery/ui-design-programs/custometry-v2/ui-program-intake.json, .codex/delivery/ui-design-programs/custometry-v2/platform-ui-baseline.json, packages/contracts/routes/ui-routes.json, packages/contracts/routes/ui-route-contracts.json, packages/contracts/routes/ui-surface-contracts.json, apps/web/**]

skills:
  primary: ui-design-program
  companions: [prompt-manager, architecture-design]

validation_strategy:
  proof_boundary: documentation authority, hash-pinned source provenance, intake and platform-baseline contracts, and control-plane validation; no browser, runtime, implementation, accessibility-conformance, responsive-behavior, or performance proof
  evidence_target: .codex/delivery/evidence/custometry-ui-design-program-v2/g0-execution-report.md
  commands: [ui_program_intake, intake_ready, baseline_ready, draft, validate_stage_ledger, assemble_stage_transition, validate_stage_transition, repository local documentation and contract gates]

file_manifest:
  expected_touch_zones: [.codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/**, docs/architecture/ui/**, docs/architecture/**, docs/adr/**]
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

Execute only `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r1`. Complete the authoritative product intake, bind the hash-verified repository-owned RU/EN HTML pilot evidence, establish the immutable responsive-Web platform baseline and target frontend ownership boundaries, validate the draft triad, and close G0 with an adjacent G1 transition receipt. Do not execute G1.

## Context / Current State

The active program is the new `CUSTOMETRY-UI-DESIGN-PROGRAM-V2`; V1 is terminal historical evidence only. Responsive Web is required and mobile-specific scope is `unauthorized`. The accepted pilot is visual-language and density authority, not exact composition, information architecture, frontend architecture, component implementation, responsive acceptance, or novel-screen fidelity authority.

## Requirements

Generate the ledger-bound G0 contract before stage work:

```text
python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/ui_program_context.py --ledger .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md --project-root /Users/daniildegtyarev/Projects/Custometry
```

Consume its live `context_manifest`; do not substitute advisory `--stage` output. Preserve the accepted owner intent, the current visual authority, the architecture decisions delegated to G0, and the explicit non-goals in the authorized task.

# Context acquisition protocol

Read the declared always-read sources, bounded task entrypoints, emitted `context_manifest`, and only its named companion references. Expand only for a recorded source conflict, missing binding, or failing validator.

# Reading manifest

Keep baseline context to at most eight files and about 45k tokens. Use hash-pinned machine manifests as the complete source index and follow exact pointers where emitted.

# Work plan

1. Claim only this row through `staged-plan-runner`.
2. Verify and import the exact RU/EN HTML sources without changing bytes or authority scope.
3. Complete and validate `ui-program-intake.json`, `platform-ui-baseline.json`, and `ui-design-program.json` from the accepted product path and source contracts.
4. Record the target application-shell, design-system, ports/adapters, route, permission, localization, state, data, responsive, visual-inheritance, rollout, and later-proof ownership boundaries.
5. Run the G0 validators, assemble and validate the adjacent G1 transition receipt, update the ledger to `accepted`, and stop.

# Acceptance criteria

Both RU/EN pilot copies are repository-owned and hash-current; intake passes `intake_ready`; baseline passes `baseline_ready`; program passes `draft`; the triad is exact and synchronized; the G0 transition is `ready` with `next_stage_allowed: true`; G1 has one unambiguous pending entry and is not claimed; no browser, runtime, accessibility-conformance, responsive-behavior, performance, implementation, publication, or mobile claim exceeds observed evidence.

# Implementation constraints

Do not change product semantics, expand current route manifests as a G1 substitute, revive V1, hand-edit assembled receipts, ask the owner for technical bookkeeping, or create a branch, worktree, stash, Goal, commit, PR, deployment, external mutation, or mobile-specific IA.

# Quality gates

Run the live profile-emitted validators and the smallest applicable repository documentation, delivery-contract, link, blueprint, and local quality gates. Evidence must distinguish machine/static proof from later browser, accessibility, responsive, and performance proof.

# Adjacent-stage preflight

Require intake and baseline to be ready and hash-current, the draft triad to remain cross-linked, screen and journey collections to exact-cover the accepted intake inventory, program-owned paths to remain known, and the G1 prompt to be the sole pending adjacent entry. Assemble the transition receipt from its request and validate it with both the transition and ledger validators.

# Final output

Report `completed`, `needs_input`, or `blocked` in Russian. Include changed paths, program/plan/pack/ledger/G0 state, baseline ownership decisions, pilot verification, concise validation results, proof boundary, residual risks, and one next safe action. If completed, say explicitly that G1 is ready but was not executed.

## Execution control

Apply `decision_policy`; keep `decision_packet`, `resume_condition`, and `resume_evidence_ref` exact. Before closure, update the ledger with validation commands/results, evidence and transition hashes, file manifest, residual risk, the adjacent incoming receipt, and the exact `Next stage allowed` value. Never infer acceptance from readiness alone.
