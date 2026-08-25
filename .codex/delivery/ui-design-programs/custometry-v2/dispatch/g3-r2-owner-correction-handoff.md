---
task_schema: codex.executor-task/v1
task_id: custometry-v2-correct-g3-r2-pilot-inheritance
artifact_kind: non_authoritative_executor_dispatch
language: en
classification: ui_design_program_single_stage_bounded_owner_correction
program_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2
execution_mode: continuation_same_stage_revision
authorized_stage_sequence:
  - G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2
terminal_target: g3_r2_corrected_review_ready_awaiting_owner_acceptance_g4_unclaimed
publication_authorized: false
mobile_scope: unauthorized
owner_acceptance:
  G3: false
state_authority: stage_ledger_only
dispatch_authority: current_user_request_live_triad_and_explicit_task_handoff
source_thread_id: 019ff273-7c9e-7082-85a6-f21985066478
live_working_tree: /Users/daniildegtyarev/.codex/worktrees/e0a0/Custometry
existing_executor_claim: codex-root-g3-r2-019ff2af-20260811T211852Z
claim_handoff_policy: preserve_existing_claim_do_not_mint_competing_claim
user_input_policy: no_routine_or_technical_owner_input_finished_visual_review_required
---

# Objective

Continue and correct only `G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2` in the exact
live working tree. The owner has confirmed the diagnosis and authorized a
bounded correction: the current owner-facing result incorrectly presents
`UI-ADMIN-003` as the representative G3 result even though the accepted pilot
depicts a different screen. This was an executor implementation error, not a
requirement of the G3 stage prompt.

Replace the rejected owner-facing G3 checkpoint with a finished foundations and
application-shell checkpoint whose acceptance meaning is explicit:

> The owner is accepting that the accepted pilot's visual and interaction
> foundations and shell rules have been faithfully codified for downstream G4
> screen design. The owner is not accepting `UI-ADMIN-003`, any other target
> screen, copied pilot fixture semantics, or a rebuilt pilot screen.

Stop at the mandatory G3 owner checkpoint. Do not self-accept G3 and never claim
or execute G4 under this dispatch.

# Exact owner correction to record

Record the latest natural-language owner correction through the canonical typed
`requested_changes` and owner-input-response flow against the current decision
packet before resuming implementation. Preserve the Russian source wording in
the typed evidence while expressing its normalized intent in English:

```yaml
response_kind: requested_changes
canonical_owner_input_string: |-
  какой нахрен UI-ADMIN-003 если пилот делает вообще другой экран? почему так?

  да ты правильно понял ошибку, продолжаем доработку
canonical_owner_input_serialization: join_the_two_verbatim_messages_with_exactly_two_newline_characters
canonical_decision_text: >-
  The owner requests a bounded correction to the same G3 r2 revision:
  UI-ADMIN-003 must not be the owner-facing acceptance target; the corrected
  review must demonstrate pilot-derived foundations and shell rules without
  rebuilding the pilot screen or copying its fixture product semantics.
```

Put the exact single serialized Russian string above in the schema-required
`owner_input` field. Put the normalized English statement in `decision_text`.
Do not add `owner_response_source_language`, message-array, or normalized-intent
properties to canonical request objects because the live schemas forbid extra
properties.

Existing `owner-requested-changes-r1*` and `owner-input-response-r1*` files are
historical evidence for an earlier correction in this same revision. Do not
overwrite them. Use new unique `r2` correction filenames and decision IDs unless
the canonical repository tool selects a stricter next identifier.

# Mandatory skills and routing

Read and follow these skills completely before crossing their boundaries:

- `staged-plan-runner` for ledger-bound continuation, typed owner response,
  lifecycle, evidence, transition, and pause behavior;
- `ui-design-program` for G3 authority, pilot inheritance, fixed-domain gates,
  review-board closure, and adjacent-stage constraints;
- `browser-qa-evidence` and `playwright-cli` for canonical loopback browser
  captures, console/network checks, responsive proof, and accessibility smoke;
- `better-layout`, `better-accessibility`, `better-ui`, `better-colors`, and
  `better-typography` for the specific shell and visual-language surfaces.

Do not route through Figma, Penpot, Product Design cloning, `ui-ux-pro-max`, or
mobile design. The direction is already accepted. Final owner-facing reporting
and review copy must be in Russian. Repository-authored artifacts remain English
unless an existing localized artifact requires otherwise.

# Authoritative execution triad

```yaml
plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md
exact_stage_prompt: .codex/agents/generated/custometry-ui-design-g0-v2/31-g3-foundations-shell-r2.md
```

This dispatch is not a fourth execution-state authority. The ledger is the only
mutable state authority. The exact stage prompt and a freshly generated live
context manifest remain the executable contract.

# Validated handoff state

At handoff creation on 2026-08-12:

```yaml
ledger_status: awaiting_input
current_stage: G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2
g3_status: needs_input
g3_execution_allowed: false
g3_executor_claim: codex-root-g3-r2-019ff2af-20260811T211852Z
g3_executor_claimed_at: 2026-08-11T21:18:52Z
g3_transition_status: review_ready
g3_next_stage_allowed: false
g4_rows: 26
g4_status: pending
g4_execution_allowed: false
g4_claims: none
incoming_g2_receipt_sha256: 562e62f911cba2bc89ccb73b9a0b385b206d5f63a984788ca942536c9b201445
stage_prompt_sha256: 6d2a55583a30b49c9e112843777c3761a0a17a1e2b86b8aed2e82e8a56889a0e
platform_baseline_sha256: c0e6c547f61211c2ae7b21dde614a3dee1637667c156d03233f3138175f935a3
accepted_visual_source_sha256: d5639f0e20a79581972853979cd643ca456b6235c1ce098f5adc98d89636ca15
current_g3_transition_sha256: ac0412f2b9c2104dd1f122a10726966b1698cc68dba00fbc39bdb61b80b7661b
current_decision_packet_sha256: 77a8f646dc103369e6db3360b380eca35864f1656908fc95089364830ed110b8
rejected_review_board_sha256: f1100db5c695b7428dae6cb23e39a7f43d4cdabdf67701b09f2d62e3a4ec04a1
```

Revalidate all values before any side effect. Stop on a changed frontier, a
competing executor, missing exact live path, or a material hash mismatch. The
user explicitly handed this work to the new task, so continue under the existing
G3 claim and preserve its identity. Do not mint, replace, or duplicate the claim.
If canonical tooling cannot safely represent this handoff, stop and report the
specific control-plane conflict rather than bypassing it.

# Source hierarchy and fixed visual authority

Use the fresh G3 context manifest to preserve these distinct source classes:

```yaml
accepted_visual_authorities:
  accepted_pilot_html: .codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v2/ru/source.html
  accepted_platform_baseline: .codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/platform-ui-baseline.json
control_and_state_bindings:
  incoming_transition: .codex/delivery/ui-design-programs/custometry-v2/evidence/g2-r2/stage-transition.json
  current_decision_packet: .codex/delivery/ui-design-programs/custometry-v2/evidence/g3-r2/owner-review-decision-packet.json
rejected_implementation_inputs_to_inspect_and_replace:
  current_builder: .codex/delivery/ui-design-programs/custometry-v2/build_g3_r2_artifacts.py
  current_transition_builder: .codex/delivery/ui-design-programs/custometry-v2/prepare_g3_r2_transition.py
  current_review_board: .codex/delivery/ui-design-programs/custometry-v2/artifacts/g3-r2/review-board.html
```

Only `accepted_visual_authorities` define the visual result. The control/state
bindings govern lifecycle and provenance. The rejected implementation inputs are
diagnostic material, not design authority, and must not preserve their unrelated
screen semantics merely because their mechanics or prior checks were useful.

The accepted pilot is a binding visual-language and platform-shell authority,
not loose inspiration and not a target-screen specification. Its relevant
character includes the graphite/cyan language, compact rail, rounded fluid
workspace, compact top chrome, tabs and filters, dense KPI rhythm, restrained
analytical lines, external series panel, and stable responsive shell behavior.

The accepted platform baseline deliberately adapts two source-observed values:

- shell/workspace gap: exactly `12px`;
- profile area: exactly `32px`.

These are fixed baseline adaptations, not owner exceptions. Revalidate and
realize every other applicable fixed baseline field as well.

# Confirmed root cause

The current builder hardcodes an unrelated product screen:

```yaml
file: .codex/delivery/ui-design-programs/custometry-v2/build_g3_r2_artifacts.py
problematic_bindings:
  - line_hint: 33
    code: 'SCREEN_ID = "UI-ADMIN-003"'
  - line_hint: 34
    code: 'SCREEN_REVISION_ID = "UI-ADMIN-003.populated.WA.ru.graphite.r2"'
  - line_hint: 407
    code: 'json_pointer: "/screens/94"'
root_cause: executor_selected_a_technical_stress_fixture_as_the_owner_facing_g3_subject
contract_fact: the_exact_G3_prompt_requires_a_representative_shell_but_does_not_require_UI-ADMIN-003
```

The current implementation may have useful table, permission, inspector,
drawer, focus, and responsive stress coverage. Preserve useful mechanics only
where they remain valid, but do not let that fixture define what the owner is
asked to accept.

# Required correction design

Create one finished, compact owner review board whose visible argument is:

1. accepted pilot reference;
2. source-backed extracted foundation or shell invariant;
3. neutral, program-owned shell/foundation specimen realizing that invariant;
4. responsive and interaction evidence for the same invariant;
5. explicit allowed and forbidden differences.

The owner-facing artifact must be a neutral foundation and application-shell
specimen, not a newly designed target product screen. It must not present
`UI-ADMIN-003`, another unrelated screen ID, a `/screens/94` contract, or copied
pilot fixture semantics as the acceptance subject.

The machine gate still requires an active representative shell screen contract.
Resolve this without smuggling target-screen semantics into the owner checkpoint:

- first use the exact live context, schemas, repository builders, and accepted
  sources to determine whether a program-owned neutral shell specimen identity
  is supported;
- if a repository-authoritative shell representative already exists, use it
  exactly and cite its source;
- do not invent a screen ID or silently reinterpret a target screen;
- if an internal technical stress fixture remains necessary for a validator,
  isolate it from the owner review, label it non-acceptance/internal evidence,
  and prove that it does not determine the visual or product acceptance claim;
- if the gate truly cannot accept a neutral/source-backed representative without
  a product-semantic choice, stop with precise evidence. Do not ask the owner a
  routine implementation question and do not bypass the gate.

The review board must state in Russian, prominently and unambiguously:

```text
Вы принимаете не экран и не его продуктовые данные. Вы принимаете правила
визуального языка и оболочки, извлечённые из пилота и зафиксированные для
последующего проектирования экранов G4.
```

It must also show a compact `pilot source -> invariant -> realization -> proof ->
disposition` matrix with only these dispositions:

- `inherited_exactly`;
- `adapted_within_fixed_contract`;
- `not_applicable_with_source`;
- `owner_exception_required`.

No fixed-domain exception is agent-decidable. Preserve all G3-relevant
obligations from the `68 OWNER-REC` and `13 RECON-ADD` bindings, and mark
screen-specific obligations as downstream G4/G5 work instead of claiming they
are closed by G3.

# Required shell and analytical proof

Demonstrate the accepted shell rules and material states without turning the
specimen into a target-screen design:

- compact icon rail, contextual navigation, fluid rounded workspace;
- desktop contextual navigation overlays rather than resizes the workspace;
- stable workspace geometry and independent content scrolling;
- fixed navigation identity, order, icons, groups, destinations, active match;
- narrow-Web viewport-contained modal drawer with deterministic open/close,
  `Escape`, outside dismissal, focus transfer/return, keyboard traversal, scroll
  locking, and correct layers;
- inspector as wide-Web sibling pane and narrow-Web viewport overlay;
- high-cardinality series as right sibling or lower panel without redefining
  chart semantics;
- chart and table language, readable axes/labels/values/legends, Result Trust,
  Focus/Explore character, bounded analytical surfaces, local overflow, and
  `32px` minimum analytical row height;
- named sorting/paging controls, logical keyboard order, visible focus, sticky
  headings outside the tab sequence;
- loading, populated, empty, partial, error, permission-denied, and recovery
  states where applicable to the neutral specimen.

Do not copy pilot fixture values, legend thresholds, exact target-screen
composition, product semantics, production implementation, or mobile IA.

# Canonical evidence requirements

Build deterministic, program-owned G3 artifacts and replace the rejected
checkpoint and its affected evidence. At minimum provide:

- realized foundation tokens and accepted shell variants;
- a gate-valid, source-backed representative shell contract;
- candidate artifact separate from the accepted source visual;
- render provenance for source and implementation;
- comparison purpose `visual_language_conformance`, not exact target-screen
  identity;
- responsive-Web captures at `768x1024`, `1024x768`, `1440x900`, and
  `1920x1080`, unless the emitted live profile is stricter;
- RU and EN content stress, 200% zoom preservation, reduced-motion behavior,
  keyboard/focus smoke, and zero hidden primary task/trust/recovery controls;
- console/network evidence, responsive geometry, source freshness, fixed-domain
  inheritance report, file manifest, and deterministic repeatability evidence;
- one compact HTML review board with hash-bound typed manifest and exact
  rendered `data-review-entry` cover;
- updated G3 execution report and repository-assembled transition artifacts.

Do not use a global dark-pixel raster score as the primary proof of fidelity.
Use source-backed fixed-region/domain comparisons and geometry/behavior checks;
raster comparison is supporting evidence only and its threshold must be justified.

Use loopback origins, isolated or mocked fixtures, redaction, and no real user
data or external side effects.

# Execution sequence

1. Operate on `/Users/daniildegtyarev/.codex/worktrees/e0a0/Custometry` even if
   the new task opens in another generated worktree.
2. Read `AGENTS.md` and `.codex/AGENTS.md` completely and inspect `git status`.
   Preserve all foreign and uncommitted changes.
3. Validate the triad, ledger frontier, incoming receipt, current G3 receipt,
   decision packet, prompt hash, baseline hash, and visual-source hash.
4. Generate the live ledger-bound G3 context with
   `ui_program_context.py --ledger ... --project-root ...`; read only emitted
   manifest entries, exact JSON pointers, and triggered bundles.
5. Record the owner correction through the canonical typed flow using new r2
   evidence files. Resume the same G3 revision under the preserved claim.
6. Regenerate context immediately and revalidate selection and hashes.
7. Correct the G3 builder, artifacts, evidence, report, and transition tooling
   only within program-owned G3 paths.
8. Run the canonical loopback Playwright capture and behavior suite.
9. Regenerate deterministic artifacts and verify repeatability and nested review
   board closure.
10. Pass the G3 machine gate under `program_ready` and validate the ledger.
11. Assemble and validate a replacement `review_ready` G3 transition with
    `next_stage_allowed: false`.
12. Move the same G3 row to `needs_input`, set ledger status to
    `awaiting_input`, preserve the executor claim, bind the new exact decision
    packet and resume condition, and keep every G4 row closed and unclaimed.
13. Show the corrected review board to the owner in Russian and ask for exactly
    one decision: accept the foundations/shell result or request bounded
    corrections.

# Minimum validation boundary

Run the exact commands emitted by the live runtime profile and repository tools.
The minimum boundary includes:

- stage prompt/ledger/incoming-transition synchronization;
- `ui_design_tool.py preflight`;
- representative contract validation with `screen_contract_ready`;
- `validate_ui_design_program.py --profile program_ready`;
- canonical Playwright captures and geometry, render-provenance, comparison,
  console/network, responsive-Web, and accessibility-smoke evidence;
- deterministic artifact/render repeatability where applicable;
- review-board manifest/HTML nested closure and exact rendered entries;
- source freshness and fixed-domain inheritance checks;
- `validate_stage_ledger.py`;
- G3 gate validation;
- assembly and validation of `review_ready` with
  `next_stage_allowed: false`;
- `source scripts/activate-toolchain.sh`;
- `uv run python -m tools.check --scope local`.

The previous green checks are historical evidence for the rejected owner-facing
surface. Rerun every affected gate and do not use them as sufficient proof of
the corrected checkpoint.

# Allowed write scope

Writes are limited to:

- G3 r2 program-owned foundation/shell artifacts and neutral specimen assets;
- G3 r2 typed owner-response and browser evidence;
- G3 r2 deterministic builders and transition preparation;
- G3 r2 execution report;
- required live plan bindings and ledger/transition synchronization.

Do not modify accepted G0/G1/G2 evidence or receipts,
`pilot-candidate-v2`, production application code, unrelated documentation,
mobile-specific scope, or foreign user changes. No publication, deployment,
commit, push, PR, stash, destructive recovery, secrets, paid actions, or
external mutation.

# Required terminal state

Before the next owner-facing report, require all of the following:

```yaml
g3_machine_gate: passing_program_ready
g3_result: corrected_and_visually_reviewable
owner_acceptance_subject: pilot_derived_foundations_and_shell_rules_only
owner_facing_ui_admin_003: absent
g3_transition_status: review_ready
next_stage_allowed: false
g3_ledger_status: needs_input
ledger_status: awaiting_input
executor_claim: preserved
owner_review_packet: exact_and_hash_bound
g4_rows: pending_unclaimed_unexecuted
```

# Owner-facing report

Report in Russian and lead with what the owner is actually being asked to
accept. Show the compact review board and no more than five useful visual links.
Explain:

1. which pilot foundation and shell invariants were codified;
2. how the neutral specimen proves them without becoming a target screen;
3. sidebar/flyout/drawer, inspector, chart/table, and responsive behavior;
4. every material allowed difference or owner exception;
5. the single owner choice: accept this foundations/shell contract for G4 or
   request bounded corrections.

Also state changed paths, validation results, proof boundary, residual risks,
preserved foreign changes, and explicitly confirm that no G4 row was claimed or
executed.
