---
task_schema: codex.executor-task/v1
task_id: custometry-v2-execute-g3-r2
artifact_kind: non_authoritative_executor_dispatch
language: en
classification: ui_design_program_single_stage_execution
program_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2
execution_mode: goal_driven_single_stage
authorized_stage_sequence:
  - G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2
terminal_target: g3_r2_review_ready_awaiting_owner_acceptance_g4_unclaimed
publication_authorized: false
mobile_scope: unauthorized
owner_acceptance:
  G3: false
user_input_policy: no_routine_or_technical_owner_input; finished_visual_review_required
state_authority: stage_ledger_only
dispatch_authority: current_user_request_and_live_triad
live_working_tree: /Users/daniildegtyarev/.codex/worktrees/e0a0/Custometry
---

# Objective

Using the current working-tree snapshot supplied to the new task, execute only
`G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2` for Custometry UI Design Program V2.

The validated uncommitted r2 snapshot lives at
`/Users/daniildegtyarev/.codex/worktrees/e0a0/Custometry`. If the task host opens
in another generated worktree that does not contain the exact hashes and ledger
state below, operate on this exact live working tree instead. Do not reconstruct
r2 from the default branch, copy a partial state, or overwrite its foreign
changes. Stop if the exact live path is unavailable or owned by a competing
executor.

Produce a finished foundations/application-shell result with canonical browser,
responsive-Web, visual-language-conformance, and accessibility-smoke evidence.
Stop at the mandatory owner checkpoint with:

1. the G3 machine gate passing under `program_ready`;
2. one finished, inspectable review board ready for the owner;
3. a validated `review_ready` G3 transition receipt with
   `next_stage_allowed: false`;
4. G3 in `needs_input` and the ledger in `awaiting_input` with the exact owner
   review resume condition;
5. every G4 row unclaimed and unexecuted.

Do not self-accept G3. If the owner later accepts or requests bounded corrections
in the same task, record that natural-language response through the canonical
typed owner-response flow, resume the same G3 revision, and follow the live
state machine. Never claim G4 under this dispatch.

# Mandatory skills and authority

Read completely before their boundary is crossed:

- `ui-design-program` — primary stage contract and visual-program gate model;
- `staged-plan-runner` — context generation, selection, atomic claim, lifecycle,
  review-ready pause, ledger update, and handoff;
- `browser-qa-evidence` and `playwright-cli` — canonical loopback browser
  captures, console/network checks, responsive proof, traces where useful, and
  redacted evidence;
- `better-layout` — shell, rail, contextual navigation, drawer, inspector,
  analytical workspace, and responsive layout behavior;
- `better-accessibility` — keyboard/focus/dismissal semantics for menus,
  drawers, dialogs, tables, and representative shell controls;
- `better-ui` — interaction states, layering, overlay behavior, and visual
  polish inherited from the accepted baseline;
- `better-colors` and `better-typography` — exact foundation-token realization,
  contrast, analytical-label readability, and RU/EN stress.

Do not route through Figma, Penpot, Product Design cloning, `ui-ux-pro-max`, or
mobile design. The direction is already accepted. Final user-facing reporting
and owner review must be in Russian; repository-authored artifacts remain
English unless an existing localized artifact requires otherwise.

# Authoritative execution triad

- `plan_doc`: `.codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json`
- `prompt_pack_dir`: `.codex/agents/generated/custometry-ui-design-g0-v2`
- `stage_ledger`: `.codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md`
- exact stage prompt: `.codex/agents/generated/custometry-ui-design-g0-v2/31-g3-foundations-shell-r2.md`

This dispatch is not a fourth source of execution state. The ledger is the only
mutable state authority, and the exact stage prompt plus live context manifest
remain the executable stage contract.

# Validated entry state

At dispatch preparation:

- ledger status: `active`;
- current stage: `G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2`;
- G2 r2: `accepted`, `execution_allowed: false`;
- G3 r2: `pending`, `execution_allowed: true`, no executor claim or timestamp;
- G3 r2 is the unique pending executable row;
- incoming G2→G3 receipt:
  `.codex/delivery/ui-design-programs/custometry-v2/evidence/g2-r2/stage-transition.json`;
- incoming receipt SHA-256:
  `562e62f911cba2bc89ccb73b9a0b385b206d5f63a984788ca942536c9b201445`;
- stage prompt SHA-256:
  `6d2a55583a30b49c9e112843777c3761a0a17a1e2b86b8aed2e82e8a56889a0e`;
- platform baseline SHA-256:
  `c0e6c547f61211c2ae7b21dde614a3dee1637667c156d03233f3138175f935a3`;
- accepted visual source SHA-256:
  `d5639f0e20a79581972853979cd643ca456b6235c1ce098f5adc98d89636ca15`;
- pre-claim G3 context resolves 9 bounded files and all required exact labels.

The G3 prompt intentionally keeps its incoming receipt fields as `none` because
the G2 receipt hash-pins the prompt bytes. The exact incoming binding lives in
the ledger. Do not introduce a prompt/receipt cryptographic self-reference and
do not hand-edit or rebuild the accepted G2 receipt.

# Claim and context discipline

Before any G3 side effect:

1. inspect `git status` and preserve every foreign/uncommitted change;
2. read `AGENTS.md` and `.codex/AGENTS.md` completely;
3. validate the triad, live ledger, exact G2→G3 receipt, prompt hash, baseline
   hash, and visual-authority hash;
4. run the live ledger-bound `ui_program_context.py --ledger ... --project-root ...`;
5. read only the emitted manifest entries, exact JSON pointers, and triggered
   bundles;
6. confirm G3 remains the unique pending executable row;
7. atomically claim only G3 with a unique executor claim and UTC timestamp;
8. reread the row, regenerate context immediately, and revalidate selection and
   hashes;
9. execute only the claimed G3 stage.

Stop on a competing claim or changed frontier. Do not claim any G4 row.

# Owner intent: accepted pilot inheritance

The accepted `pilot-candidate-v2` is a binding visual-language and platform-
baseline authority, not loose inspiration. G3 must make inheritance inspectable
and exact for every G3-relevant fixed domain. It must not silently simplify,
replace, or reinterpret accepted pilot behavior.

At minimum, produce a source-backed inheritance matrix that maps accepted pilot
and baseline decisions to the G3 realization, evidence, and disposition:
`inherited_exactly`, `adapted_within_fixed_contract`, `not_applicable_with_source`,
or `owner_exception_required`. No fixed-domain exception is agent-decidable.

Preserve all G3-relevant obligations from the 68 `OWNER-REC` and 13 `RECON-ADD`
bindings; record which remain downstream obligations for G4/G5 rather than
pretending G3 closes target-screen work.

## Shell, sidebar, and popup behavior

Realize and prove the full fixed shell/navigation contract, including:

- compact icon rail plus contextual navigation and fluid rounded workspace;
- contextual navigation overlays the desktop workspace rather than resizing it;
- stable workspace geometry and independent content scrolling;
- exact navigation identity: labels, order, icons, groups, destinations, and
  active matching remain fixed;
- narrow-Web transformation into a viewport-contained modal drawer without
  inventing mobile-specific information architecture;
- deterministic open/close, active, hover, focus-visible, disabled where
  applicable, `Escape`, outside-dismissal, focus transfer/return, keyboard
  traversal, scroll containment/locking, and layer ordering;
- report inspector as a sibling pane on wide Web and viewport-contained overlay
  on narrow Web;
- high-cardinality series as a right sibling panel or lower panel without
  redefining chart semantics;
- source-backed fixed geometry and tokens, including the baseline's zero-
  tolerance values such as the 12 px shell/workspace gap and 32 px profile
  area, plus every other fixed baseline field rather than only these examples.

Create a compact state/behavior matrix and demonstrate the material states in
the finished review board.

## Charts, tables, and analytical behavior

The representative shell result must make the accepted analytical language
concrete enough to validate inheritance. Cover the applicable foundations and
interactions for:

- chart ↔ data-table presentation;
- readable axes, labels, values, legends, and analytical hierarchy;
- Result Trust visibility and recovery meaning;
- Focus / Explore character;
- inspector and external series-panel behavior;
- bounded analytical surfaces and local overflow;
- fixed table geometry, including the 32 px minimum analytical row height;
- logical keyboard order, named sorting/paging controls, visible focus, and
  sticky headings excluded from the tab sequence;
- loading, populated, empty, partial, error, permission-denied, and recovery
  states where applicable.

Candidate visual language and interaction behavior are authoritative only
within the accepted scopes. Never copy pilot fixture values, legend thresholds,
exact target-screen composition, product semantics, production implementation,
or mobile-specific IA. Product meaning comes from the accepted intake and
normative sources.

# Required G3 outcome

Build deterministic, program-owned G3 artifacts and evidence that replace the
`pending_g3_execution` rendered-proof seed with real canonical evidence:

- realized foundation tokens and accepted shell variants;
- an active representative shell screen contract validated before capture;
- a candidate artifact separate from the accepted source visual;
- mode-correct source and implementation render provenance;
- canonical comparison purpose `visual_language_conformance` where the pilot is
  a platform-language anchor rather than an exact target screen;
- responsive-Web anchor bindings and captures at `768×1024`, `1024×768`,
  `1440×900`, and `1920×1080` unless the emitted live profile provides a stricter
  exact set;
- RU and EN content stress, 200% zoom preservation, reduced-motion behavior,
  keyboard/focus smoke, and zero hidden primary task/trust/recovery controls;
- source-backed inheritance and exception report;
- one compact HTML review board with a hash-bound typed manifest and rendered
  `data-review-entry` exact cover;
- G3 execution report, source-freshness evidence, file manifest, and transition
  request/receipt assembled by repository tools.

Use loopback origins, isolated or mocked fixtures, redaction, and no real user
data or external side effects. Reuse repository builders/templates/assets where
available; create deterministic program-owned builders only where required.

# Validation and review-ready lifecycle

Run the commands emitted by the live G3 runtime profile and repository tools.
At minimum include:

- stage prompt/ledger/incoming-transition synchronization;
- `ui_design_tool.py preflight`;
- representative contract validation with `screen_contract_ready`;
- `validate_ui_design_program.py --profile program_ready`;
- canonical Playwright captures plus geometry, render-provenance, comparison,
  console/network, responsive-Web, and accessibility-smoke evidence;
- deterministic artifact/render repeatability where applicable;
- review-board manifest/HTML nested closure and exact rendered entries;
- source freshness and fixed-domain inheritance checks;
- `validate_stage_ledger.py`;
- G3 gate validation;
- assembly and validation of a `review_ready` G3→G4 transition with
  `next_stage_allowed: false`;
- `source scripts/activate-toolchain.sh`;
- `uv run python -m tools.check --scope local`.

Machine proof is not owner acceptance. When green, move the same G3 row to
`needs_input`, set ledger status to `awaiting_input`, bind the exact decision
packet/resume condition, and show the finished review board in Russian. Do not
mark G3 accepted, do not allow G4, and do not ask the owner to inspect hashes or
raw JSON.

# Write and safety scope

Writes are limited to G3 r2 program-owned foundations/shell artifacts,
candidate/review assets, typed evidence, deterministic builders, execution
report, live plan bindings, and required ledger/transition synchronization.

Do not modify accepted G0/G1/G2 evidence or receipts, `pilot-candidate-v2`,
production application code, unrelated documentation, mobile-specific scope,
or foreign user changes. No publication, deployment, commit, push, PR, stash,
destructive recovery, secrets, paid actions, or external mutation.

# Terminal state before first report

Require all of the following:

- G3 result is machine-valid and visually reviewable;
- G3 transition receipt is `review_ready` and validates;
- `next_stage_allowed: false`;
- G3 ledger row is `needs_input` with its existing executor claim preserved;
- ledger status is `awaiting_input`;
- the exact owner review artifact and resume condition are recorded;
- all G4 rows remain pending, `execution_allowed: false`, unclaimed, and
  unexecuted.

# Owner-facing report

Report in Russian and lead with the finished G3 result. Show the compact review
board and at most five useful visual links. Explain:

1. sidebar/flyout/drawer behavior;
2. chart/table/inspector/series-panel inheritance;
3. responsive endpoint behavior;
4. any material exception;
5. the single owner choice: accept the finished result or request bounded
   corrections.

Also state changed paths, validations, proof boundary, residual risks, preserved
foreign changes, and explicitly confirm that no G4 row was claimed or executed.
