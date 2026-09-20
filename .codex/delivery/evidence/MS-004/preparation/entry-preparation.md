# MS-004 entry preparation — 2026-09-20

This is evidence linked by the [canonical journal](../../../ledgers/MS-004.md),
not another execution-state register. The accepted
[plan](../../../../../docs/architecture/planning/milestones/MS-004/plan.md)
remains version 0.2.1, preserving design 0.2.0. No product implementation,
stage claim, transition receipt, publication or deployment occurred in this unit.

## Current owner authority and organization

The owner supplied `goal-objective.md` on 2026-09-20 and explicitly selected:

- One coordinator, one independent read-only preparatory reviewer and five
  sequential executor tasks, one executor per stage. No additional delegation.
- The canonical checkout `/Users/daniildegtyarev/.codex/worktrees/575c/Custometry`.
  The original `/Users/daniildegtyarev/Projects/Custometry` stays read-only.
- Complete MS-004 S01–S05 within the accepted scope, with `manual_sequential`
  execution in each task and real session-owned stage claims.
- Coordinator review and normal technical-branch PR synchronization after each
  accepted stage: required Foundation gate, squash merge, confirmed remote main,
  checkout update and local/remote technical-branch deletion before the next stage.
- Executor receipts keep `next_stage_allowed:false`; after synchronization the
  coordinator uses the supported `advance` operation with current evidence.
  The coordinator never accepts or resumes another task's claim.
- S05 needs explicit owner acceptance of the demonstrated finished result.
  Plan acceptance and this execution request are not result acceptance.
- No production deployment, C02/C03 implementation, Forecasting or MS-003 resumption.

This later request supersedes historical preparation-only authority statements;
accepted product decisions and acceptance criteria remain unchanged. This record
is an authority summary, not a conversation transcript or fabricated approval.

## Independent review

Cold-head review: completed. Mode: independent read-only review in the one
owner-authorized separate task, `MS-004 independent prompt-pack review`.
The reviewer created no further reviewers and changed no repository files.
The reviewed checkout and remote main were
`471314d42d6c49e0f9cec5f1794b44dbaeb03a14` (merged PR #84).

Scope: complete plan, five prompts, journal, preparation/capability evidence,
direct product/architecture sources, framework templates, lifecycle, receipt and
repository validation contracts. Checklist: installed architecture-review
`references/cold-head-plan-prompt-pack-review.md`.

Original verdict: **Block** until H1 is corrected; one High, two Medium findings.
The review found exact triad/stage/capability bindings consistent and preserved
real PostgreSQL/API/browser proof, independent SQL, atomic Save and S05 acceptance.

| Finding | Observed fact and consequence | Coordinator disposition |
|---|---|---|
| H1 / High | Plan DEP-04 requires current access before v2 activation; S02 asked for public Analytics routes while S03 owned the access adapter and named only report activation. This could expose a route early or shift responsibility implicitly; no existing bypass was demonstrated. | S02 now produces unmounted adapters, real calculation/artifacts and proof that new public routes are unavailable. S03 mounts all report/Analytics/context/catalog/result v2 endpoints only after object/data-access proof, including direct callers, denied scope, cross-workspace, revocation and reuse. Matching stage contracts, checks and touch zones are synchronized in the journal. D01/D06 are unchanged. |
| M1 / Medium | METRIC-022 includes published-default personal reset; the plan allocates Saved View semantics but no C01 published-default reset scenario. | Applicability is explicit in S03–S05: C01 has existing draft reports and explicitly excludes publication; the pinned base snapshot is not a published-default contract. Full METRIC-022 published-presentation conformance is not claimed. No new publication/reset semantics or requirement waiver is invented. |
| M2 / Medium | S04 required real browser smoke while S05 instructed creation of the harness; the Web source contract requires an owned lifecycle for each browser-depth unit. | S04 produces the exact MS-004 config and real API fixture with webServer, loopback, readiness and cleanup. S05 declares those as S04-produced entry inputs and consumes/extends them. 1920/768 desktop projects remain; 400px is additional desktop reflow smoke, not a mobile-specific project. |

Local deterministic follow-up, not a second independent review, checks the saved
corrections. The review's original Block verdict is preserved rather than rewritten
as a reviewer approval. Product decisions, immutable plan bytes and historical
MS-001–003 execution evidence are unchanged.

The reviewer observed a first system-Python failure due to absent `yaml`, then
passed the portable gate using the existing `.venv`, with no dependency install.
The draft check passed and S01 entry was correctly refused for its unresolved
preparation packet. These were read-only checks, not runtime evidence.

## Initial dispatch assessment (superseded)

The task-management project inventory currently maps saved Custometry to the
original read-only checkout. `create_thread` selects a saved project and has no
arbitrary checkout parameter. No saved project maps to the selected canonical
checkout. Computer Use refused access to the Codex app for safety reasons; no
UI bypass or private application-state modification was attempted.

The owner was asked to add a saved local project for the canonical checkout.
This is a task-binding input, not a request to repeat execution authorization.
The preparatory review safely read the canonical checkout using explicit paths;
no executor task has been dispatched against the wrong checkout. S01 stays
pending/disallowed in the unclaimed draft until this input is resolved and entry
is rechecked. No runtime `needs_input` or blocked stage is fabricated.

## Documentation and compatibility

Owned changes: five prompts, matching draft contracts/prose and this evidence.
The original preparation report is retained with a link to this later record.
No plan/product-source version changed: fixes clarify accepted security and proof
allocation, and record narrower claim applicability. Parent/child plan links and
their exact versions remain valid. Prompt/journal contracts and future producer
inputs are synchronized. No new canonical architecture document or docs index
entry is required for journal-linked evidence.

Contract impact: product API/persistence/runtime `none` in this preparation;
executor instruction/proof allocation `compatible-change` within accepted intent.
No foreign changes were present in the canonical checkout at entry. The original
checkout and historical ledgers/receipts were not modified.

## Preparation validation before binding resolution

- `source scripts/activate-toolchain.sh`: passed with the existing toolchain.
- `uv run --locked python -m tools.custometry_quality.validate_prompt_packs`:
  passed, four journals; exact artifact structure/file binding only.
- `uv run --locked python -m tools.check --scope local`: passed, including the
  saved prompt/journal/evidence links. No CI/runtime claim.
- `git diff --check`: passed.
- Deterministic assertions: passed for unchanged accepted plan SHA-256, matching
  prompt/journal contracts, S02 unmounted versus S03 guarded activation, S04-produced
  config/fixture consumed by S05, manual_sequential, all rows pending/disallowed,
  no claims/receipts/transitions and owned changed paths only.
- `git ls-remote origin refs/heads/main` and PR #84 metadata: remote main and the
  merged PR both identify `471314d42d6c49e0f9cec5f1794b44dbaeb03a14`.

Cold-head review: completed. Local follow-up: completed. H1 and M2 are resolved
in executor instructions; M1 is addressed by explicit published-default
applicability and a preserved conformance limitation. No unresolved Blocker/High
review finding remains. Overall verdict: **Block entry** on the separate saved
project binding input, not on missing implementation proof masquerading as review.
`draft_valid`: true; `entry_ready`: false; no implementation stage is accepted.

Next action: verify the owner-selected saved-project binding, recheck unchanged
entry inputs/review/capability, enable only S01 through permitted draft authoring,
run actual updater preflight, and dispatch its executor. Preparation changes stay
local for inclusion in the first accepted stage's authorized synchronization.
No technical branch or new PR was created, so branch deletion is not applicable.


## Binding resolution and S01 handoff

The owner's follow-up delegates technical sequencing to the coordinator and asks
only for material unresolved decisions. The earlier saved-project requirement
was an unnecessarily narrow tool choice, not a missing product decision.

The existing project task `Custometry — L3 первого этапа WS-003` already uses the
canonical checkout. The supported `fork_thread` with `environment:same-directory`
created the distinct task `MS-004 S01 — Contracts and fiscal calendar` without a
new worktree. Task metadata readback confirms its actual cwd is
`/Users/daniildegtyarev/.codex/worktrees/575c/Custometry`. It remains idle until
entry checks complete and the coordinator sends the S01-only execution request.
No private app-state edit, UI bypass, user project setup or change of checkout
scope is required. Subsequent stages use this same verified mechanism after
predecessor synchronization. Inherited authoring conversation is historical;
each executor receives the current exact prompt, evidence and stage-only authority.

Review fixes, accepted plan and updater capability bindings are unchanged. Only
S01 is enabled by permitted unclaimed-draft authoring; all rows remain pending,
current_stage is null, and no claim or lifecycle transition is fabricated.
The executor must run fresh preflight and claim under its own real session.
The initial binding blocker and its entry_ready:false assessment above are
historical and resolved. Remaining product decision before final completion is
owner acceptance of the actual S05 demonstration; no additional input is needed
for S01 preparation.

Post-resolution checks: `validate_prompt_packs` passed (four journals), actual
`stage_ledger preflight --ledger .codex/delivery/ledgers/MS-004.md --stage MS-004-S01`
returned exit 0 / `status:pass`, `check --scope local` and `git diff --check`
passed. `draft_valid:true`, `entry_ready:true` for S01 only. These prove entry
inputs/updater availability and source consistency, not S01 implementation.
