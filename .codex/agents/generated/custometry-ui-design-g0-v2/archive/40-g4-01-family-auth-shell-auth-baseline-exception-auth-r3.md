---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: G4@family.auth.shell-auth.baseline-exception-auth-r3
gate_id: G4
target_id: family.auth.shell-auth.baseline-exception-auth-r3
title: Family acceptance replacement: family.auth.shell-auth.baseline-exception-auth
report_path: .codex/delivery/evidence/custometry-ui-design-program-v2/g4-r3/family-auth-shell-auth-baseline-exception-auth-family-report.md
proof_boundary: finished family review board with exact representative screen/state coverage, canonical capture 1.6.0 browser evidence, responsive-Web proof, and accessibility smoke; no production implementation, deployment, performance, or full WCAG conformance proof
expected_touch_zones: .codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**
blocker_policy: needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for owner_required product meaning or finished-result review; hard-block only unsafe or unrecoverable conditions
decision_packet: none
resume_condition: none
resume_evidence_ref: none
Next stage allowed: true
execution_allowed: true
transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r3/family-auth-shell-auth-baseline-exception-auth/stage-transition.json
incoming_transition_receipt: .codex/delivery/ui-design-programs/custometry-v2/evidence/g3-r2/replacement-auth-r3/stage-transition.json
incoming_transition_receipt_sha256: ledger_bound
runtime_profile: codex.ui-stage-runtime-profiles/v1@1.6.0
capture_tool_version: 1.6.0
execution_mode: manual_sequential
goal_artifact_required: false
current_stage: G4@family.auth.shell-auth.baseline-exception-auth-r3
replaces_stage: G4@family.auth.shell-auth.baseline-exception-auth-r2
repair_evidence_ref: .codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r3/family-auth-shell-auth-baseline-exception-auth/repair-evidence.json
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
  proof_boundary: finished family review board with exact representative screen/state coverage, canonical capture 1.6.0 browser evidence, responsive-Web proof, and accessibility smoke; no production implementation, deployment, performance, or full WCAG conformance proof
  evidence_target: .codex/delivery/evidence/custometry-ui-design-program-v2/g4-r3/family-auth-shell-auth-baseline-exception-auth-family-report.md
  commands: [ui_program_context, ui_design_tool preflight, capture_geometry 1.6.0, validate_ui_design_program, playwright-cli, assemble_visual_qa_receipt 1.5.0, validate_stage_ledger, assemble_stage_transition, validate_stage_transition]

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

Execute only `G4@family.auth.shell-auth.baseline-exception-auth-r3` when the ledger independently selects and atomically claims it as the unique repaired replacement for terminal row `G4@family.auth.shell-auth.baseline-exception-auth-r2`. Complete one bounded family review unit from the accepted G2 structure and G3 foundations.

## Context / Current State

The r2 stage instance stopped because capture `1.5.0` incorrectly applied target-screen actions and fixture metadata to the immutable pilot reference. The released proof contract resolves that control-plane defect without changing the accepted family scope, product semantics, visual authority, G3 result, responsive-Web range, or mobile authorization.

Use the accepted revision-2 product intent, exact platform baseline, visual-language authority limits, responsive-Web contract, and mobile scope `unauthorized`. The accepted pilot is binding visual-language authority, not an exact composition or fixture specification for `UI-AUTH-001`.

## Requirements

Run the ledger-bound context workflow before claim, validate the exact ledger-bound incoming transition and repair evidence, claim atomically, regenerate context, and consume only the emitted manifest. Produce finished visuals and canonical browser evidence before owner review.

For every `visual_language_conformance` comparison:

- capture the unchanged accepted pilot as `visual_authority_reference` with capture `1.6.0`;
- enforce source bytes, render provenance, screenshot, common browser/viewport/motion conditions, fixed clock, network isolation, and redaction on the reference;
- do not apply target locale/theme markers, regions, elements, actions, fixture/font/asset metadata, accessibility acceptance, keyboard behavior, or overflow gates to the reference;
- capture the target as `screen_implementation` and apply the complete target-screen contract there;
- reject `unexpected_visible_regions` and every missing, duplicate, forbidden, unexpected, or unregistered target element on the implementation;
- assemble new visual-QA receipts with assembler `1.5.0`; capture `1.5.0` receipts may be read only as historical evidence and must not enter the new proof chain.

Keep `source_fidelity` strict: when it is actually selected by a source-backed same-screen contract, its reference profile remains `screen_reference`.

# Context acquisition protocol

Read only the bounded post-claim manifest, exact pointers, and triggered bundles. Expand only for a named failed binding or validator error.

# Reading manifest

Respect the live profile limits of 16 files and approximately 600k estimated tokens.

# Work plan

1. Revalidate the blocked frontier, unique pending replacement, triad, accepted G3 owner decision, repair evidence, and incoming transition.
2. Run ledger-bound `ui_program_context.py` before claim; require this exact r3 row and a bounded manifest.
3. Atomically reactivate the ledger and claim only this row; preserve the terminal r2 row and its claim.
4. Regenerate ledger-bound context and consume only its emitted entries, pointers, and triggered bundles.
5. Build the exact bounded family artifacts and canonical capture `1.6.0` browser evidence.
6. Assemble render provenance, visual-QA, screen acceptance, the exact-cover family aggregate, and the typed interactive review board; do not hand-edit passing receipts.
7. Enter `needs_input` with a validated `review_ready` transition and `next_stage_allowed: false`; accept only after natural-language owner acceptance is canonically recorded.

# Acceptance criteria

- The family aggregate exact-covers every declared representative screen/state pair for `UI-AUTH-001` and passes `family_review_ready` before finished-result review.
- The three non-representative family members are recorded as a reuse decision, not falsely claimed as individually designed or accepted.
- Every active capture in the new proof chain uses capture `1.6.0` and the purpose/side-specific profile required by the current contract.
- Reference provenance remains hash-bound to the unchanged accepted pilot; implementation-side actions, fixture metadata, accessibility smoke, keyboard/focus, overflow, and exhaustive inventory checks pass.
- The final row state is `needs_input`, ledger state is `awaiting_input`, transition state is `review_ready`, and no adjacent row is claimed.

# Implementation constraints

Do not change product semantics, accepted baseline authority, accepted G0-G3 artifacts or receipts, mobile scope, production code, publication state, deployment, secrets, or another family/wave. Do not mutate, wrap, or inject behavior into the accepted pilot. Do not hand-edit capture, provenance, raster, visual-QA, screen-acceptance, family-acceptance, owner, or transition receipts.

# Quality gates

Run the exact commands emitted by the live r3 runtime profile, including `ui_design_tool.py preflight`, capture/provenance/comparison and interaction evidence, `screen_contract_ready`, `visual_acceptance`, `screen_acceptance`, `assemble_family_acceptance.py`, `family_review_ready`, review-board nested closure, source freshness, write-scope and foreign-change checks, `validate_stage_ledger.py`, `assemble_stage_transition.py`, `validate_stage_transition.py`, `source scripts/activate-toolchain.sh`, and `uv run python -m tools.check --scope local`.

# Adjacent-stage preflight

Current-gate success alone never allows the next row. G4 closes from one exact-cover family aggregate; until owner acceptance, keep every other G4/G5/G6 row unclaimed and unexecuted.

# Final output

Report in Russian. Lead with the finished auth-family result under review, show at most five useful visual links, state material exceptions and proof limits, and ask exactly one decision: accept the family result or request bounded corrections. Keep raw JSON and hashes in linked evidence.
