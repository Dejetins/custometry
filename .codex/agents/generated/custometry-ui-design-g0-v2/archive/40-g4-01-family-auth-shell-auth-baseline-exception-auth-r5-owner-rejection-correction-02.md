---
task_schema: codex.executor-task/v1
task_id: custometry-g4-auth-r5-owner-rejection-structural-correction-02
artifact_kind: non_authoritative_executor_dispatch
language: en
classification: same_row_g4_owner_requested_structural_ui_correction
program_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2
execution_mode: bounded_stage_resume
goal_artifact_required: false
publication_authorized: false
deployment_authorized: false
production_implementation_authorized: false
mobile_scope: unauthorized
state_authority: stage_ledger_only
live_working_tree: /Users/daniildegtyarev/.codex/worktrees/e0a0/Custometry
current_stage_at_dispatch: G4@family.auth.shell-auth.baseline-exception-auth-r5
requested_terminal_target: corrected_g4_auth_family_review_ready_awaiting_owner_acceptance
foreign_changes_excluded: true
---

# Objective

Resume the existing, unaccepted G4 auth-family row after an explicit owner
rejection and structurally redesign the review result. The current result is
not accepted. Correct the source generator, screen contracts, copy model,
semantic controls, layout system, pilot inheritance, browser evidence, family
aggregate, review board, transition receipt, and ledger checkpoint. Return the
same G4 r5 row to a truthful `review_ready` / `needs_input` state and stop for
the owner's natural-language decision.

This is not a cosmetic CSS patch. Do not preserve a defective composition only
by changing colors, widths, or labels. Diagnose and remove the systemic causes
that produced arbitrary buttons, invented or internal-facing copy, broken
alignment, and semantically incorrect form controls.

# Exact authority and live root

Operate only in:

```text
/Users/daniildegtyarev/.codex/worktrees/e0a0/Custometry
```

Do not substitute the ambient checkout, the saved project checkout, another
worktree, or a reconstructed branch.

The stage ledger remains the only mutable execution-state authority:

```yaml
plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md
```

Dispatch-time bindings, which must be revalidated before any mutation:

```yaml
stage_ledger_sha256: 90f21a6107a4342952e07d634db228c03ad86fb5560a962b49c0aa527bf1e4c9
rejected_review_board:
  path: .codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-auth-shell-auth-baseline-exception-auth/review-board.html
  sha256: 679d62abd791b00fba9f3339d6d3c3607565da9dad734640b0ecc2a3456cbe04
rejected_screen_surface:
  path: .codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-auth-shell-auth-baseline-exception-auth/screens/auth-family.html
  sha256: 85cc3a47dc34aaae884f05c733796dd89b7ef2ec8c637eb7a353d2e1baf57c71
rejected_family_acceptance:
  path: .codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r5/family-auth-shell-auth-baseline-exception-auth/family-acceptance.json
  sha256: 03a0c56b4b031918ce58b20ef352f16d22ba22f98c815814bda7972aa2d6e7e2
current_owner_decision_packet:
  path: .codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r5/family-auth-shell-auth-baseline-exception-auth/owner-review-decision-packet-correction-r5-01.json
  sha256: 4a5babe66a9fdf2873f8b9faefc567b215edb3b340af82d2b1466551b1e86486
accepted_visual_authority:
  path: .codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v3-metadata/ru/source.html
  sha256: b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700
```

If a live hash changed, inspect the live ledger and evidence. Continue only if
the same r5 row is still the unique current-authority `needs_input` row and no
competing writer or claim exists. Stop on a material authority conflict; never
edit evidence merely to reproduce this dispatch snapshot.

# Owner rejection authority

The owner explicitly rejected the current result. Treat the following as
binding correction authority, not as acceptance:

```yaml
decision: requested_changes
same_stage_revision: true
scope_change: false
owner_findings:
  - The sign-in and recovery compositions are visually unacceptable.
  - The visible phrase "Помощь с паролем" is unacceptable and must not return.
  - Buttons have incoherent geometry, hierarchy, alignment, and grouping.
  - Text hierarchy, wording, and alignment are visibly poor.
  - The correction must be systemic and reusable, not a one-off patch.
```

Owner-supplied rejection observations:

```yaml
sign_in_observation:
  path: /var/folders/bz/j3xmpgc95cz8ty7p79b272gh0000gn/T/codex-clipboard-b32cc2f5-57c0-425e-871c-06a23e4ced4b.png
  sha256: 2d0b5c049ab44a933902010a3ca9556f84da9ea8613eb39cd4dfab04a7307957
recovery_observation:
  path: /var/folders/bz/j3xmpgc95cz8ty7p79b272gh0000gn/T/codex-clipboard-4f6ecf06-46eb-489b-9440-1cb257e00b18.png
  sha256: f6f11bd5049f5b14c598f8c1d8a669058cdb67d211c5bd88f980040eb2b1007e
```

If these temporary files are still readable, copy them into the existing G4
evidence directory with their hashes before editing the rejected surface. If
they are gone, the hash-bound rejected HTML is sufficient authority; reproduce
the exact two rejected states in the browser and capture equivalent durable
before-evidence.

# Required skill routing

Use the skills in this order:

1. `staged-plan-runner` for the exact `needs_input -> in_progress ->
   needs_input` lifecycle and every compare-and-swap ledger mutation.
2. `ui-design-program` for the active G4 family contract, exact pilot
   inheritance, family aggregate, review board, and transition rules.
3. `root-cause-debugging` before edits to identify why the generator produced
   the rejected control semantics, copy, and layout.
4. `better-writing`, `better-layout`, `better-ui`, and
   `better-accessibility` only for the material defects named here.
5. `browser-qa-evidence` with exactly `playwright-cli` as the canonical browser
   mechanic for all gate evidence.
6. `prompt-manager` only if a deterministic current prompt/control field must
   be synchronized; do not create another plan, pack, ledger, or state file.

Do not use Product Design, Figma, Penpot, `ui-ux-pro-max`, a new design
direction, mobile design, Browser, Chrome, or the legacy `playwright` alias.

# Lifecycle requirements

1. Read `AGENTS.md`, `.codex/AGENTS.md`, the selected skills, the current r5
   prompt, the current ledger row/detail, the accepted visual-authority digest,
   the two auth route contracts, and only the bounded evidence needed for this
   correction.
2. Revalidate the dirty worktree, triad, current claim, ledger hash, rejected
   artifact hashes, owner packet, and absence of a competing writer.
3. Assemble, never hand-edit, a canonical `requested_changes` owner decision
   and `codex.ui-owner-input-response/v1` bound to the exact current decision
   packet and rejected board.
4. Resume the same r5 row with the released compare-and-swap writer. Preserve
   executor claim `codex-root-g4-auth-r5-20260813T222203Z` unless the live
   ledger proves a canonical successor claim already exists.
5. Regenerate ledger-bound context after resume and consume only that bounded
   post-resume manifest.
6. Correct the generator and reusable auth-family construction. Generated HTML
   alone is not an acceptable edit target.
7. Rebuild every affected screen contract, applicability manifest, capture,
   visual-QA receipt, screen acceptance, family aggregate, review manifest,
   decision packet, transition receipt, and report through canonical
   assemblers.
8. Return the same row to `needs_input`, ledger to `awaiting_input`, and
   `Next stage allowed: false`. Preserve the existing claim and create one new
   hash-bound finished-result decision packet.
9. Do not accept G4, claim another G4 row, claim G5/G6, or modify production
   frontend code.

# Product and route semantics

Preserve these authoritative identities:

```yaml
sign_in:
  screen_id: UI-AUTH-001
  route: /auth/sign-in
  surface_kind: editor
  required_meaning: credentials, remember preference, language, route to password recovery, self-hosted trust
recovery:
  screen_id: UI-AUTH-004
  route: /auth/recovery
  surface_kind: wizard
  required_meaning: host/admin reset-token flow, password rules, generic security messages, no implied email reset channel
```

The route identifiers must remain machine-checkable but must not appear as
decorative visible copy. The pilot governs reusable visual rules; it does not
own target product meaning, exact target copy, or exact novel-screen
composition.

# Structural repair requirements

## Sign-in

- Replace the fake button with `role="checkbox"` by a native checkbox and one
  associated visible label for the remember preference.
- Represent recovery navigation as a real link with a valid `/auth/recovery`
  destination and a source-backed, natural RU/EN label. The rejected string
  `Помощь с паролем` is forbidden.
- Use one coherent form column with shared alignment edges. Labels, inputs,
  checkbox row, recovery link, primary action, and state feedback must not form
  unrelated widths or drifting baselines.
- Give the primary action an intentional width derived from the form grammar;
  do not use arbitrary fixed widths or a narrow cyan strip disconnected from
  the input width.
- Remove visible route-path decoration and all placeholder/internal language
  such as `Проверочное значение`.
- Do not render an empty or generic status panel in the initial state. Status,
  validation, retry, and session-expired messages appear only in the states
  where they carry useful information.

## Recovery

- Keep recovery structurally distinct from sign-in, but redesign it as a
  coherent user-facing reset flow rather than a developer/admin diagnostic
  panel.
- Preserve the source-backed host/admin token semantics without exposing
  internal implementation vocabulary as unexplained UI copy. Do not imply an
  email reset channel.
- Use one stable action hierarchy per step. Do not place unrelated secondary,
  navigation, and primary actions in a mismatched two-column grid.
- The step indicator, form, actions, errors, and safe return path must share a
  legible reading order and alignment system at every accepted Web anchor.
- Do not show technical explanatory prose such as “separate route” or policy
  assertions as prominent product copy. Security guidance must be concise,
  calm, source-backed, and user-facing.
- Do not render a generic empty status panel in the initial state.

## Copy

- Build an exhaustive visible-copy inventory for all 12 required screen/state
  pairs in RU and EN.
- Bind every product-semantic phrase to the current blueprint/route sources or
  classify it as minimal target-authored connective copy with a specific
  justification.
- No marketing copy, implementation notes, test-fixture terminology, raw route
  paths, invented channel behavior, unexplained tokens, or vague help labels.
- Buttons use concise action labels; links describe destinations; validation
  text says how to recover next to the failing field.
- RU/EN must retain equivalent meaning and stable layout under realistic string
  growth.

## Controls and pilot inheritance

- Re-derive the auth action taxonomy from actual semantics: submit action,
  secondary action, navigation link, checkbox, language control, and wizard
  progression are not all the same component.
- Map each taxonomy member to the exact applicable pilot component, variant,
  size, slot, and state. Do not apply one generic button identity to every
  clickable element.
- Inherit complete applicable pilot clauses for typography, palette, control
  height, padding, radii, border/surface treatment, density, focus, hover,
  active `scale(.96)`, disabled behavior, and reduced motion.
- Default, hover, focus-visible, active, selected/checked, loading, disabled,
  validation, and error states must be visually and semantically coherent.
- Audit the unaccepted r5 button `standard_exception` decisions. Remove or
  supersede any exception that merely legalized the rejected generic mapping.
  Do not create a broader exception. A genuinely necessary new material
  exception requires a narrow clause-bound owner checkpoint and therefore
  cannot be self-accepted in this task.
- Do not mutate the accepted G0 baseline, accepted pilot bytes, G3 acceptance,
  historical r2/r3 artifacts, or their receipts.

## Layout and visual quality

- Establish an explicit auth layout grammar in the generator: container,
  brand/header, form width, field stack, inline utility row, primary action,
  wizard progression, feedback region, and responsive transformations.
- Use shared edges, consistent gaps, and component-derived sizing. Remove
  accidental whitespace, arbitrary width literals, mismatched button blocks,
  and visually detached copy.
- The result must feel like one designed system at 768, 1024, 1440, and 1920
  widths and at 200% zoom, while mobile-specific composition remains excluded.
- Preserve compact professional density from the pilot without shrinking
  targets below the active accessibility and hit-area policy.

# Required browser proof

Use loopback or `file://` only as permitted by the active G4 profile and use
isolated fixtures. Re-run every affected target-side capture and receipt.

At minimum, prove in a real browser:

- all 12 representative state pairs for `UI-AUTH-001` and `UI-AUTH-004`;
- every accepted responsive-Web anchor;
- RU and EN structural stress;
- pointer and keyboard completion of sign-in and recovery navigation;
- native checkbox name/role/state and label hit target;
- real link semantics and destination for recovery and return-to-sign-in;
- computed default, hover, focus-visible, active, checked/selected, loading,
  disabled, validation, failed, and session-expired styles where applicable;
- physical mouse-down evidence for active-state geometry, not a synthetic event;
- shared alignment edges and coherent action widths from computed geometry;
- no visible forbidden strings, raw route decoration, fixture placeholders,
  empty initial status panel, or internal implementation notes;
- 200% zoom/reflow, reduced motion, overflow, focus order, accessible names,
  console, network isolation, deterministic repeatability, and freshness;
- exact review-board nested evidence closure and actual interactive state
  selection.

Global raster similarity is supporting evidence only. Blocking proof comes
from source-derived clause applicability, computed target values, semantic
elements, geometry, behavior, and readable content.

# Required quality gates

Run every command emitted by the live G4 runtime profile and at least:

```text
python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/ui_program_context.py --ledger .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md --project-root /Users/daniildegtyarev/.codex/worktrees/e0a0/Custometry
python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_ui_design_program.py --profile screen_contract_ready --project-root <root> <each-contract>
python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_ui_design_program.py --profile visual_acceptance --project-root <root> <each-visual-qa>
python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_ui_design_program.py --profile screen_acceptance --project-root <root> <each-screen-acceptance>
python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_ui_design_program.py --profile family_review_ready --project-root <root> <family-acceptance>
python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_stage_ledger.py --project-root <root> <ledger>
python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_stage_transition.py --project-root <root> --ledger <ledger> <transition>
source scripts/activate-toolchain.sh
uv run python -m tools.check --scope local
```

Also run the exact focused regression that proves the generator cannot regress
to a fake checkbox, generic help label, raw route decoration, generic initial
status box, or one-button-identity-for-all-actions model.

# Allowed writes

Ordinary writes are limited to the current G4 r5 program zones required for
this correction:

```text
.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/**
.codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r5/**
.codex/delivery/ui-design-programs/custometry-v2/build_g4_auth_r4_artifacts.py
.codex/delivery/ui-design-programs/custometry-v2/run_g4_auth_r5_board_qa.py
.codex/delivery/ui-design-programs/custometry-v2/prepare_g4_auth_r5_transition.py
.codex/delivery/ui-design-programs/custometry-v2/mutate_g3_g4_r4_lifecycle.py
.codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md
.codex/agents/generated/custometry-ui-design-g0-v2/40-g4-01-family-auth-shell-auth-baseline-exception-auth-r5.md
.codex/delivery/evidence/custometry-ui-design-program-v2/family.auth.shell-auth.baseline-exception-auth-r5-report.md
```

Add another current-program path only when a canonical assembler directly
requires it and record it as `outside_expected_paths`. Do not touch production
application code, accepted G0/G3 artifacts, historical r2/r3 evidence, other
G4 rows, G5/G6, publication, deployment, secrets, or mobile-specific design.

# Stop conditions

Stop before mutation and report a precise blocker if:

- the exact live root or triad is absent;
- the live current-authority row is no longer the same unaccepted r5 G4 row;
- a competing writer or claim exists;
- the rejected board or decision packet no longer matches live authority and
  the change cannot be explained by canonical lifecycle evidence;
- authoritative product sources no longer support the two-screen topology;
- a correct result requires changing the accepted baseline, G3 acceptance,
  production frontend code, mobile scope, or another G4 family;
- exact pilot applicability cannot be derived without a new material owner
  exception;
- the final family gate cannot pass truthfully.

Do not use hard `blocked` for reversible UI decisions inside this accepted
correction envelope. Do not ask the owner intermediate micro-decisions. Make
the bounded design and technical choices, then present one finished result.

# Acceptance criteria

The task is complete only when all are true:

1. The owner rejection is assembled as canonical `requested_changes` evidence
   and the same r5 row is resumed through compare-and-swap.
2. The generator, not only generated HTML, contains the systemic repair.
3. `Помощь с паролем`, raw route decoration, fixture placeholders, technical
   reset prose, and empty initial status panels are absent from owner-visible
   surfaces.
4. Remember preference uses a native checkbox; route changes use real links;
   submit and wizard actions use real buttons.
5. Sign-in and recovery have coherent, distinct, source-backed compositions
   with shared alignment edges and intentional action hierarchy.
6. Each action type maps to the correct pilot component taxonomy and inherits
   all applicable reusable clauses without a generic-button shortcut.
7. Every relevant interaction state is proven with computed browser evidence,
   including physical active-state proof.
8. All 12 contracts, 48 target visual acceptances, 12 screen acceptances, the
   family aggregate, review board, ledger, transition, and local repository
   gate pass under the active contract.
9. The new review board is interactive, compact, readable, and contains one
   finished-result decision packet bound to its exact bytes.
10. The same G4 r5 row ends at `needs_input`, ledger at `awaiting_input`, and
    `Next stage allowed: false`; its claim is preserved and owner acceptance is
    pending.
11. Historical r2/r3 evidence is byte-preserved; no adjacent row is claimed.
12. Production implementation, publication, deployment, and mobile scope are
    untouched.

# Final owner-facing report

Write the final report in Russian. Lead with the corrected auth-family result
and link no more than five useful visuals. Briefly explain the corrected
control semantics, copy boundary, layout grammar, pilot inheritance, browser
proof, changed paths, preserved history, and residual risk. Do not expose raw
hash inventories by default.

Ask exactly one question: accept the corrected auth-family result or request
bounded corrections.
