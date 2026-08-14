<codex_delegation>
  <input>
---
task_schema: codex.executor-task/v1
task_id: custometry-v2-g4-01-family-auth-shell-auth-r3
artifact_kind: non_authoritative_executor_dispatch
language: en
classification: ui_design_program_single_stage_family_replacement_execution
program_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2
execution_mode: manual_sequential
goal_artifact_required: false
authorized_stage_sequence:
  - G4@family.auth.shell-auth.baseline-exception-auth-r3
terminal_target: g4_01_r3_review_ready_awaiting_owner_acceptance
publication_authorized: false
mobile_scope: unauthorized
owner_acceptance:
  G3: true
  G4_01_r3: false
state_authority: stage_ledger_only
dispatch_authority: current_user_request_to_start_the_revisioned_g4_replacement_in_a_new_project_thread
live_working_tree: /Users/daniildegtyarev/.codex/worktrees/e0a0/Custometry
claim_policy: atomically_reactivate_and_mint_one_unique_claim_only_after_live_preclaim_validation
user_input_policy: no_routine_or_technical_owner_input_finished_visual_review_required
foreign_changes_excluded: true
---

# Objective

Execute only `G4@family.auth.shell-auth.baseline-exception-auth-r3` in the exact
live working tree. This is the unique pending revisioned replacement for
terminally blocked row
`G4@family.auth.shell-auth.baseline-exception-auth-r2`. Revalidate and atomically
reactivate the blocked ledger by claiming only r3, produce the finished,
browser-verifiable auth-family result, and stop at the mandatory G4 owner
checkpoint with:

```yaml
g4_family_gate: passing_family_review_ready
g4_result: finished_and_visually_reviewable
g4_transition_status: review_ready
next_stage_allowed: false
g4_ledger_status: needs_input
ledger_status: awaiting_input
executor_claim: preserved
owner_acceptance: pending
other_g4_rows: pending_unclaimed_unexecuted
g5_g6: pending_unclaimed_unexecuted
```

Do not self-accept G4. Do not resume, mutate, or replace r2. Do not claim or
execute another G4 family, G5, G6, production implementation, publication,
deployment, or mobile-specific scope.

# Exact live frontier at dispatch creation

```yaml
ledger_status: blocked
current_stage: G4@family.auth.shell-auth.baseline-exception-auth-r2
next_stage_allowed: false
canonical_selected_executable_stage: G4@family.auth.shell-auth.baseline-exception-auth-r3
selection_errors: []
r2_status: blocked
r2_current_authority: false
r2_executor_claim: codex-root-g4-01-019ff348-20260812T000614Z
r2_claimed_at: 2026-08-12T00:06:14Z
r3_status: pending
r3_current_authority: true
r3_execution_allowed: true
r3_executor_claim: none
r3_replaces_stage: G4@family.auth.shell-auth.baseline-exception-auth-r2
g3_status: accepted
incoming_transition_status: ready
incoming_transition_next_stage_allowed: true
current_authority_g4_rows: 26
current_authority_g4_rows_pending: 26
current_authority_g4_claims: none
g5_claims: none
g6_claims: none
live_context_status: bounded
live_context_file_count: 8
live_context_estimated_tokens: 45190
runtime_profile: codex.ui-stage-runtime-profiles/v1@1.6.0
```

Revalidate every value before any write. Stop on a changed frontier, competing
claim, missing exact live path, stale or mismatched hash, invalid incoming
transition, unreadable repair evidence, or an unbounded or misdirected context
manifest. The preclaim ledger front matter intentionally remains blocked on the
historical r2 row; only the canonical replacement rule may atomically move the
ledger to active and r3 to in_progress.

# Authoritative execution triad

```yaml
plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md
exact_stage_prompt: .codex/agents/generated/custometry-ui-design-g0-v2/40-g4-01-family-auth-shell-auth-baseline-exception-auth-r3.md
incoming_transition: .codex/delivery/ui-design-programs/custometry-v2/evidence/g3-r2/replacement-auth-r3/stage-transition.json
repair_evidence: .codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r3/family-auth-shell-auth-baseline-exception-auth/repair-evidence.json
```

This dispatch is not a fourth execution-state authority. The stage ledger is
the only mutable state authority. The exact stage prompt and the freshly
generated ledger-bound context manifest are the executable contract. If any
dispatch snapshot differs from the live validated ledger, prompt, or manifest,
follow the higher live authority and stop on a material conflict.

# Hash-pinned entry bindings

```yaml
program_sha256: 21810c42b847bfc591db9a7ad76cf3df64c6bb5ad0cb82dd80082bd0c7a124d2
stage_ledger_sha256: c6916d432ee58da92e923fe0b5d0fd84890a192d278a1463c85ea282dd999c6e
exact_stage_prompt_sha256: 1d5d599ad35a574d29244e5adcfe45e4a9103b5fa676db56cb27b15d0ef6dff7
incoming_g3_transition_sha256: 36a10295cb916cc432d7fd49c39b6933c6be45ebb2ccb87c06eabd06daad776c
repair_evidence_sha256: cf4390492737127b8f76ce296e3b3ba3786f05c6488a480b9223d9aa1f027798
accepted_g3_owner_decision_sha256: 9bae65aed9e786a007f6fad1510605b0debf26fefdfc33c667e28e3191fbb6ea
accepted_g3_review_board_sha256: c85d7102feb50e40a1165e89f96a734758625a96b9d8d456c695a20e31b3495f
accepted_visual_source_sha256: d5639f0e20a79581972853979cd643ca456b6235c1ce098f5adc98d89636ca15
platform_baseline_sha256: c0e6c547f61211c2ae7b21dde614a3dee1637667c156d03233f3138175f935a3
target_family_slice_sha256: 15187dd655888a5619f0593848e7729a4028fe626ea4b06edee999768e5e7371
representative_screen_slice_sha256: e79f5f9cda9d246765e745cff83c163685ae075e7a5d30620e6325074f118846
```

The stage ledger hash is a preclaim snapshot and is expected to change only
through the authorized atomic claim and later lifecycle updates. All other
accepted input bindings must remain stable unless the live contract explicitly
classifies a new repair or owner decision. Never hand-edit a hash-pinned
incoming receipt or accepted artifact to make validation pass.

# Mandatory workflow and skill instructions

Read each selected skill completely before crossing its boundary:

- `staged-plan-runner` — primary execution workflow for blocked-ledger
  replacement selection, ledger-bound context, atomic reactivation and claim,
  lifecycle, review-ready pause, transition, and handoff;
- `ui-design-program` — G4 family exact-cover, accepted authority inheritance,
  capture 1.6.0 proof semantics, aggregate closure, review board, and owner gate;
- `browser-qa-evidence` — browser QA scope, evidence sufficiency, console and
  network review, responsive behavior, keyboard/focus, accessibility smoke, and
  readiness report;
- `playwright-cli` — the single canonical terminal browser mechanic for
  loopback captures, screenshots, traces when useful, and reproducible
  interaction evidence.

For `browser-qa-evidence`, also read its
`references/browser-mechanics-contract.md` before browser work and select
exactly `playwright-cli`; do not open a competing Browser or Chrome mechanic.
Read focused Playwright references only when the exact mechanic requires them.

Load a `better-*` craft skill only if a material design decision, observed
defect, or required proof actually crosses its domain. Do not preload the full
craft set merely because the screen contains layout, text, color, and controls.

Do not use Figma, Penpot, Product Design cloning, `ui-ux-pro-max`, or mobile
design. The visual direction is already accepted. Final owner-facing reporting
must be in Russian; repository-authored artifacts remain English unless an
existing localized artifact requires otherwise.

# Bounded family contract

```yaml
family_id: family.auth.shell-auth.baseline-exception-auth
family_title: auth / shell-auth / baseline-exception-auth
family_slice: .codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/families/family.auth.shell-auth.baseline-exception-auth.json
representative_screen_ids:
  - UI-AUTH-001
family_screen_ids:
  - UI-AUTH-001
  - UI-AUTH-002
  - UI-AUTH-003
  - UI-AUTH-004
workload_budget:
  max_screens: 4
  max_screen_state_pairs: 24
representative_screen_slice: .codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/screens/UI-AUTH-001.json
representative_route: /auth/sign-in
representative_shell_variant: shell.auth
representative_baseline_exception: baseline-exception-auth
representative_states:
  - UI-AUTH-001.initial
  - UI-AUTH-001.loading
  - UI-AUTH-001.populated
  - UI-AUTH-001.error
  - UI-AUTH-001.permission_denied
  - UI-AUTH-001.recovery
representative_action_ids:
  - UI-AUTH-001.inspect
```

Exact-cover the declared representative screen/state pairs in the G4 family
aggregate. Do not claim that `UI-AUTH-002`, `UI-AUTH-003`, or `UI-AUTH-004`
were individually designed or accepted by this row. Record the exact reuse
decision and supporting evidence without expanding the workload budget.

# Visual, product, and repaired proof authority

Carry forward the owner-accepted G3 foundations/application-shell contract.
The accepted pilot is binding visual-language and platform-baseline authority,
not exact target-screen composition, fixture truth, product semantics, or
production implementation. G4 may realize the source-backed semantics of
`UI-AUTH-001`, but must not copy pilot fixture values, legend thresholds,
unrelated analytical composition, or runtime/product meaning.

Preserve the Graphite/cyan language, calm professional density, typography,
fixed shell rules, responsive-Web range, keyboard/focus behavior, Result
Trust/recovery clarity, and the applicable auth baseline exception. Resolve
reversible design and technical choices autonomously from accepted sources.
Ask the owner only for genuinely non-derivable product meaning or the final
finished-result decision.

The r2 blocker was a proof-contract defect, not a product or visual change.
Every new proof chain must use runtime/capture `1.6.0` and visual-QA assembler
`1.5.0`:

- for `visual_language_conformance`, capture the unchanged accepted pilot as
  `visual_authority_reference` and bind exact bytes, source provenance,
  screenshot, common browser/viewport/motion conditions, fixed clock, network
  isolation, and redaction;
- do not apply novel target locale/theme markers, regions, elements, actions,
  fixture/font/asset metadata, accessibility acceptance, keyboard behavior, or
  overflow gates to `visual_authority_reference`;
- capture the target as `screen_implementation` and apply the full target
  screen contract there, including exhaustive inventory,
  `unexpected_visible_regions`, actions, fixture metadata, accessibility smoke,
  keyboard/focus, and overflow;
- retain `screen_reference` for strict same-screen `source_fidelity` only;
- treat capture `1.5.0` and old receipts as historical-read-only; they cannot
  participate in the new r3 proof chain;
- never mutate, wrap, inject target behavior into, or otherwise alter the
  accepted pilot.

# Required execution sequence

1. Operate on `/Users/daniildegtyarev/.codex/worktrees/e0a0/Custometry` even if
   the new task opens in another checkout.
2. Read `AGENTS.md` and `.codex/AGENTS.md` completely. Inspect the dirty working
   tree and preserve every foreign change; do not clean, stash, reset, or
   reconstruct it from another branch.
3. Read the ledger, exact r3 prompt, repair evidence, and incoming transition.
   Revalidate the triad, hashes, accepted G3 owner decision, exact family and
   representative slices, platform baseline, accepted visual source, unique
   pending replacement, and absence of live competing claims.
4. Run the ledger-bound
   `ui_program_context.py --ledger ... --project-root ...` before claim. Require
   canonical selection of this exact r3 row and a bounded manifest. Read only
   the emitted entries, exact JSON pointers, and triggered bundles.
5. Re-read the ledger immediately before mutation. Atomically perform the
   authorized blocked-ledger replacement transition: set the ledger active,
   select r3 as current, change only r3 `pending -> in_progress`, and mint one
   unique executor claim plus UTC timestamp in the same mutation. Preserve r2
   as blocked/current-authority-false with its historical claim and evidence.
   Re-read the result and stop if another writer won the race.
6. Regenerate the ledger-bound context immediately after claim and consume only
   that post-claim manifest for stage work.
7. Build deterministic, family-owned G4 artifacts for the exact representative
   screen/state coverage, using source-backed target semantics and accepted G3
   inheritance without turning the pilot into a target-screen specification.
8. Capture all required responsive-Web anchors and material states through the
   canonical loopback Playwright route. Collect render provenance, geometry,
   interaction, console/network, RU/EN stress, 200% zoom, reduced motion,
   keyboard/focus, and accessibility-smoke evidence required by the fresh live
   runtime profile.
9. Assemble, never hand-edit, render provenance, visual-QA receipts, screen
   acceptance, and the exact-cover `family_acceptance` aggregate. Build one
   compact interactive owner review board with a hash-bound typed manifest and
   exact rendered `data-review-entry` coverage.
10. Pass `family_review_ready`, review-board nested closure, source freshness,
    fixed inheritance, write scope, foreign-change exclusion, deterministic
    repeatability, ledger validation, and adjacent-stage preflight.
11. Assemble and validate a `review_ready` transition with
    `next_stage_allowed: false`.
12. Set this same r3 row to `needs_input`, ledger status to `awaiting_input`,
    preserve its executor claim, bind the exact decision packet and resume
    condition, and leave every other G4/G5/G6 row unclaimed and unexecuted.
13. Report in Russian. Lead with the exact finished auth-family result the owner
    is reviewing, show no more than five useful visual links, state material
    exceptions and proof limits, and ask exactly one decision: accept the
    family result or request bounded corrections.

# Minimum validation boundary

Run every exact command emitted by the fresh post-claim runtime profile. At
minimum this includes:

- `ui_design_tool.py preflight`;
- `screen_contract_ready` for every active representative contract;
- canonical Playwright capture, render-provenance, comparison, interaction,
  console, network, responsive-Web, keyboard/focus, and accessibility-smoke
  evidence;
- `visual_acceptance` and `screen_acceptance` receipts;
- `assemble_family_acceptance.py`;
- `family_review_ready` before owner review;
- review-board manifest/HTML nested closure and exact rendered entries;
- source freshness, fixed inheritance, write scope, foreign-change, and
  adjacent-stage preflight;
- `validate_stage_ledger.py`;
- `assemble_stage_transition.py` and `validate_stage_transition.py`;
- `source scripts/activate-toolchain.sh`;
- `uv run python -m tools.check --scope local`.

Do not use a global raster score as primary proof. Use source-backed
region/domain comparisons, geometry, behavior, readable content, and fixed
contract checks; raster comparison is supporting evidence only. A green local
repository gate does not substitute for browser evidence.

# Allowed write and safety scope

Writes are limited to program-owned artifacts and evidence for this exact r3
G4 family row, its deterministic builders if required, its execution report,
and the necessary ledger/transition synchronization inside the exact stage
prompt's declared touch zones.

Do not modify accepted G0/G1/G2/G3 artifacts or receipts, the accepted pilot,
the r2 historical row or evidence, production application code, another G4
family, G5/G6 outputs, unrelated documentation, mobile scope, or foreign user
changes. No commit, push, PR, publication, deployment, stash, destructive
recovery, secrets, paid action, or external mutation is authorized.

# Stop and decision policy

- Resolve reversible `agent_decidable` design and technical choices inside the
  accepted envelope without asking the owner.
- Use `needs_input` only for genuinely non-derivable product meaning or the
  finished-result review; resume the same r3 revision when scope and acceptance
  criteria remain unchanged.
- Use hard `blocked` only for authority, safety, unavailable required evidence,
  permission, inseparable foreign change, or another unrecoverable condition.
- Do not require a magic acceptance string, hashes, paths, revision syntax, or
  ledger operation from the owner.
- Do not mark r3 accepted or allow an adjacent row until an unambiguous
  natural-language owner acceptance is recorded through the canonical typed
  owner-response flow and the strict family gate is rerun.

# Final owner-facing report

Report in Russian and lead with the finished `/auth/sign-in` family result being
reviewed. Explain the six representative states, accepted G3 inheritance,
responsive and interaction behavior, auth baseline exception, material allowed
differences, validation boundary, changed paths, residual risks, and preserved
foreign changes. Confirm that r2 remained historical and no adjacent row was
claimed or executed. Show no more than five useful visual links and ask exactly
one decision: accept the family result or request bounded corrections.
  </input>
</codex_delegation>
