<codex_delegation>
  <input>
---
task_schema: codex.executor-task/v1
task_id: custometry-v2-g4-01-family-auth-shell-auth-r2
artifact_kind: non_authoritative_executor_dispatch
language: en
classification: ui_design_program_single_stage_family_execution
program_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2
execution_mode: single_stage_owner_gated
authorized_stage_sequence:
  - G4@family.auth.shell-auth.baseline-exception-auth-r2
terminal_target: g4_01_review_ready_awaiting_owner_acceptance
publication_authorized: false
mobile_scope: unauthorized
owner_acceptance:
  G3: true
  G4_01: false
state_authority: stage_ledger_only
dispatch_authority: current_user_request_to_start_g4_in_a_new_project_thread
live_working_tree: /Users/daniildegtyarev/.codex/worktrees/e0a0/Custometry
claim_policy: mint_one_unique_claim_only_after_live_preclaim_validation
user_input_policy: no_routine_or_technical_owner_input_finished_visual_review_required
---

# Objective

Execute only `G4@family.auth.shell-auth.baseline-exception-auth-r2` in the exact
live working tree. Claim the row only after the ledger-bound preclaim context
and accepted G3 incoming transition validate. Produce the finished,
browser-verifiable family review result and stop at the mandatory G4 owner
checkpoint with `review_ready`, `next_stage_allowed: false`, row status
`needs_input`, and ledger status `awaiting_input`.

Do not self-accept G4. Do not claim or execute another G4 family, G5, G6,
production implementation, publication, deployment, or mobile-specific scope.

# Exact live frontier at dispatch creation

```yaml
ledger_status: active
current_stage: G4@family.auth.shell-auth.baseline-exception-auth-r2
next_stage_allowed: true
selected_row_status: pending
selected_row_execution_allowed: true
selected_row_executor_claim: none
g3_status: accepted
g3_transition_status: ready
g3_transition_sha256: 9c91cdb1bab21a57a28a28b337001f4518fe13fea058c14011affea2fb74840e
g3_owner_acceptance_sha256: 9bae65aed9e786a007f6fad1510605b0debf26fefdfc33c667e28e3191fbb6ea
g4_rows: 26
g4_rows_pending: 26
g4_claims: none
live_context_status: bounded
live_context_file_count: 8
live_context_estimated_tokens: 43554
```

Revalidate every value before any write. Stop on a changed frontier, competing
claim, missing live path, stale/mismatched hash, invalid incoming transition,
or an unbounded/misdirected context manifest.

# Authoritative execution triad

```yaml
plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md
exact_stage_prompt: .codex/agents/generated/custometry-ui-design-g0-v2/40-g4-01-family-auth-shell-auth-baseline-exception-auth-r2.md
incoming_transition: .codex/delivery/ui-design-programs/custometry-v2/evidence/g3-r2/stage-transition.json
```

This dispatch is not a fourth execution-state authority. The stage ledger is
the only mutable state authority. The exact stage prompt and the freshly
generated ledger-bound context manifest are the executable contract.

# Accepted source and hash bindings

```yaml
program_sha256: 21810c42b847bfc591db9a7ad76cf3df64c6bb5ad0cb82dd80082bd0c7a124d2
stage_ledger_sha256: d9da235b1e9e90cd70ff3dba8a5c4277f834b88a804482f62beb69262bc2f5ac
exact_stage_prompt_sha256: 3c0652457903311408ceff9195b4f2e5850b03332f6dfe0733b1e33f50b548e3
incoming_g3_transition_sha256: 9c91cdb1bab21a57a28a28b337001f4518fe13fea058c14011affea2fb74840e
accepted_g3_review_board_sha256: c85d7102feb50e40a1165e89f96a734758625a96b9d8d456c695a20e31b3495f
accepted_visual_source_sha256: d5639f0e20a79581972853979cd643ca456b6235c1ce098f5adc98d89636ca15
platform_baseline_sha256: c0e6c547f61211c2ae7b21dde614a3dee1637667c156d03233f3138175f935a3
target_family_slice_sha256: 15187dd655888a5619f0593848e7729a4028fe626ea4b06edee999768e5e7371
representative_screen_slice_sha256: e79f5f9cda9d246765e745cff83c163685ae075e7a5d30620e6325074f118846
```

# Hash-pinned prompt control note

The accepted G3 transition hash-pins the exact G4 stage prompt above as its
handoff artifact. Its static pre-entry header still renders the pre-acceptance
values `Next stage allowed: false`, `execution_allowed: false`, and an empty
incoming receipt. Do not edit that hash-pinned prompt or the accepted G3
transition merely to rewrite those static header values. The live ledger and
the validated incoming G3 receipt independently and canonically establish the
current execution state listed above. The prompt task body already conditions
execution on ledger selection and claim. If canonical validators disagree with
this interpretation at claim time, stop with the exact control-plane error;
never bypass or hand-edit a receipt.

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
aggregate. Do not pretend the three non-representative family members were
individually designed or accepted by this row. Record the reuse decision and
its evidence without expanding the workload budget.

# Visual and product authority

Carry forward the owner-accepted G3 foundations/application-shell contract.
The accepted pilot is binding visual-language and platform-baseline authority,
not exact target-screen composition or fixture/product truth. G4 may now
realize the source-backed product semantics of `UI-AUTH-001`, but must not copy
pilot fixture values, legend thresholds, unrelated analytical composition, or
production implementation.

Preserve the Graphite/cyan language, density, typography, fixed shell rules,
responsive-Web range, keyboard/focus behavior, Result Trust/recovery clarity,
and applicable auth baseline exception. Resolve reversible design and technical
choices autonomously from accepted sources. Ask the owner only for genuinely
non-derivable product meaning or the final finished-result decision.

# Mandatory workflow and skills

Read each selected skill completely before crossing its boundary:

- `staged-plan-runner` for live row selection, atomic claim, ledger lifecycle,
  transition, and pause behavior;
- `ui-design-program` for G4 family exact-cover, authority inheritance,
  aggregate closure, and owner gate;
- `browser-qa-evidence` and `playwright-cli` for canonical loopback captures,
  responsive behavior, console/network checks, keyboard/focus, and
  accessibility smoke.

Load only materially crossed `better-*` craft skills. Do not use Figma,
Penpot, Product Design cloning, `ui-ux-pro-max`, or mobile design. The visual
direction is already accepted.

# Required execution sequence

1. Operate on `/Users/daniildegtyarev/.codex/worktrees/e0a0/Custometry` even if
   the new thread opens in another checkout.
2. Read `AGENTS.md` and `.codex/AGENTS.md` completely; inspect and preserve the
   dirty working tree and all foreign changes.
3. Revalidate the triad, hashes, ledger frontier, accepted G3 owner decision,
   incoming `ready` transition, exact family slice, representative screen
   slice, baseline, and visual source.
4. Run the ledger-bound `ui_program_context.py --ledger ... --project-root ...`
   before claim. Require the selected G4 row and a bounded manifest. Read only
   the emitted entries, exact JSON pointers, and triggered bundles.
5. Re-read the ledger and atomically claim only the selected row with a unique
   executor claim and timestamp. Stop if another claim won the race.
6. Regenerate the ledger-bound context immediately after claim and consume only
   that post-claim manifest.
7. Build deterministic, family-owned G4 artifacts for the exact representative
   screen/state coverage. Use source-backed target semantics and the accepted
   G3 visual/platform inheritance without turning the pilot into a target
   screen specification.
8. Capture all required responsive-Web anchors and material states through the
   canonical loopback Playwright route. Collect render provenance, geometry,
   interaction, console/network, RU/EN stress, 200% zoom, reduced motion,
   keyboard/focus, and accessibility-smoke evidence required by the emitted
   live profile.
9. Assemble—not hand-edit—screen acceptance and the exact-cover
   `family_acceptance` aggregate. Build one compact, interactive owner review
   board with a hash-bound typed manifest and exact rendered entries.
10. Pass `family_review_ready`, ledger validation, source freshness, fixed
    inheritance, deterministic repeatability, and adjacent-stage preflight.
11. Assemble and validate a `review_ready` transition with
    `next_stage_allowed: false`.
12. Set this same G4 row to `needs_input`, ledger status to `awaiting_input`,
    preserve its executor claim, bind the exact decision packet and resume
    condition, and leave every other G4/G5/G6 row unclaimed and unexecuted.
13. Report in Russian. Lead with what finished family result the owner is
    accepting, show no more than five useful visual links, state material
    exceptions and proof limits, and ask exactly one decision: accept the
    family result or request bounded corrections.

# Minimum validation boundary

Run the exact commands emitted by the fresh live runtime profile, including:

- `ui_design_tool.py preflight`;
- `screen_contract_ready` for every active representative contract;
- canonical Playwright capture/provenance/comparison and interaction evidence;
- `visual_acceptance` and `screen_acceptance` receipts;
- `assemble_family_acceptance.py`;
- `family_review_ready` before owner review;
- review-board manifest/HTML nested closure and exact rendered entries;
- source freshness, write scope, foreign-change, and adjacent-stage preflight;
- `validate_stage_ledger.py`;
- `assemble_stage_transition.py` and `validate_stage_transition.py`;
- `source scripts/activate-toolchain.sh`;
- `uv run python -m tools.check --scope local`.

Do not use a global raster score as primary proof. Use source-backed
region/domain comparisons, geometry, behavior, readable content, and fixed
contract checks; raster comparison is supporting evidence only.

# Allowed write scope

Writes are limited to program-owned artifacts and evidence for this exact G4
family row, its deterministic builders if needed, its execution report, and
the required ledger/transition synchronization inside the stage prompt's
declared touch zones.

Do not modify accepted G0/G1/G2/G3 artifacts or receipts, the accepted pilot,
production application code, another G4 family, G5/G6 outputs, unrelated docs,
mobile scope, or foreign user changes. No commit, push, PR, publication,
deployment, stash, destructive recovery, secrets, paid action, or external
mutation is authorized.

# Required terminal state

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

# Final owner-facing report

Report in Russian and lead with the exact finished auth-family result being
reviewed. Explain the representative screen/state coverage, inherited G3 shell
and visual rules, responsive and interaction behavior, the auth baseline
exception, material allowed differences, validation boundary, changed paths,
residual risks, preserved foreign changes, and confirmation that no adjacent
row was claimed or executed. Ask exactly one owner decision: accept this
family result or request bounded corrections.
  </input>
</codex_delegation>
