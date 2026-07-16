---
artifact_kind: stage_ledger
staged_schema_version: 1
ledger_name: <plan-slug>-stage-ledger
workstream_id: B01
plan_doc: docs/architecture/<area>/<plan-slug>.md
prompt_pack_dir: .codex/agents/generated/<plan-slug>/
stage_ledger: docs/architecture/<area>/<plan-slug>-stage-reports/<plan-slug>-stage-ledger.md
execution_mode: goal_driven
ledger_status: dormant
current_stage: S00
allowed_stage_statuses: [pending, in_progress, accepted, blocked, skipped, superseded]
spec_version: 0.8.2-draft
updated_at: YYYY-MM-DD
stages:
  - stage_id: S00
    status: pending
    prompt_path: .codex/agents/generated/<plan-slug>/S00-discovery.md
    prompt_readiness: outline
    previous_gate: null
    next_allowed: false
    requirement_ids: [<normative-requirement-id>]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S01
    status: pending
    prompt_path: .codex/agents/generated/<plan-slug>/S01-ux-contract.md
    prompt_readiness: outline
    previous_gate: S00
    next_allowed: false
    requirement_ids: [<normative-requirement-id>]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S02
    status: pending
    prompt_path: .codex/agents/generated/<plan-slug>/S02-domain-application.md
    prompt_readiness: outline
    previous_gate: S01
    next_allowed: false
    requirement_ids: [<normative-requirement-id>]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S03
    status: pending
    prompt_path: .codex/agents/generated/<plan-slug>/S03-adapters.md
    prompt_readiness: outline
    previous_gate: S02
    next_allowed: false
    requirement_ids: [<normative-requirement-id>]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S04
    status: pending
    prompt_path: .codex/agents/generated/<plan-slug>/S04-web-integration.md
    prompt_readiness: outline
    previous_gate: S03
    next_allowed: false
    requirement_ids: [<normative-requirement-id>]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S05
    status: pending
    prompt_path: .codex/agents/generated/<plan-slug>/S05-real-boundary-proof.md
    prompt_readiness: outline
    previous_gate: S04
    next_allowed: false
    requirement_ids: [<normative-requirement-id>]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S06
    status: pending
    prompt_path: .codex/agents/generated/<plan-slug>/S06-acceptance.md
    prompt_readiness: outline
    previous_gate: S05
    next_allowed: false
    requirement_ids: [<normative-requirement-id>]
    evidence: []
    blocker: null
    supersedes: []
---

# <Plan Name> — Stage Ledger

This ledger is the source of truth for current stage, evidence, blocker, and handoff. It does not replace the linked plan or stage prompts.

## Execution rules

- The durable execution trio is exactly `plan_doc + prompt_pack_dir + stage_ledger`.
- One Codex Goal owns this workstream's currently authorized S00–S06
  iteration; do not create a separate Goal per stage.
- After each accepted stage, the Goal re-reads this ledger and may continue
  only when the successor is current and `next_allowed: true`.
- The Goal stops on a blocked/completed/dormant/superseded ledger, failed
  validation, missing or stale evidence, required approval, or no explicitly
  unlocked successor.
- A dependent stage starts only after its predecessor is `accepted` or explicitly `superseded` by a named replacement.
- The union of S00–S06 `requirement_ids` equals the linked plan requirement set.
- The active executable current stage pins at least one reviewed repository source hash.
- Validation happens before the ledger update; the ledger update happens before the stage/final report.
- `blocked` records the blocker, evidence, owner/authority needed, and whether safe work remains.
- Goal runtime state is not durable project truth. Never create `GOAL.md`.
  A second ledger, branch, worktree, stash, or coordination folder still
  requires explicit user authority.

## Linked artifacts

| Artifact | Path | Verified state/hash | Notes |
|---|---|---|---|
| Plan | `docs/architecture/<area>/<plan-slug>.md` | TBD | What and why |
| Prompt pack | `.codex/agents/generated/<plan-slug>/` | TBD | One self-contained prompt per stage |
| Ledger | `docs/architecture/<area>/<plan-slug>-stage-reports/<plan-slug>-stage-ledger.md` | this file | Current execution truth |

## Stage status

| Stage | Requirement IDs/outcome | Status | Prompt | Report/evidence | Predecessor gate | Validation depth | Proof boundary | Blocker | Next allowed |
|---|---|---|---|---|---|---|---|---|---|
| `S00` | TBD | `pending` | `.codex/agents/generated/<plan-slug>/S00-discovery.md` | `docs/architecture/<area>/<plan-slug>-stage-reports/S00-discovery.md` | none | TBD | TBD | none | no |

## Current-stage context

- current stage: `S00`;
- verified completed work: none;
- required inputs/state/hash: TBD;
- owned paths: TBD;
- foreign changes to preserve: TBD;
- stop gates: TBD;
- next-stage rule: TBD.

## Contract impact

| Stage | API | Ports/DTO/events | Persistence/artifacts | Config/defaults/identity | Service calls/retry/idempotency | Logs/audit/redaction | Browser | Ops/runbooks | Migration/rollback |
|---|---|---|---|---|---|---|---|---|---|
| `S00` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | TBD |

## Verification and evidence

| Stage | Local gates | Real-boundary evidence | Result | Evidence path | What this does not prove | Residual risk |
|---|---|---|---|---|---|---|
| `S00` | TBD | TBD | TBD | TBD | TBD | TBD |

## File manifest

| Stage | Created | Modified | Deleted | Outside expected paths | Justification | Foreign excluded | Mixed-file status |
|---|---|---|---|---|---|---|---|
| `S00` | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## Blockers and approvals

| Stage | Blocker/approval | Severity | Evidence | Required owner/action | Resolved by | Next allowed |
|---|---|---|---|---|---|---|
| `S00` | TBD | TBD | TBD | TBD | TBD | no |

## Handoff for the next stage

- accepted facts: TBD;
- decisions that must not be reopened: TBD;
- unresolved risks: TBD;
- exact next prompt: TBD;
- next stage allowed: `no`.

## Change log

| Date | Stage | Change | Evidence |
|---|---|---|---|
| YYYY-MM-DD | `S00` | Ledger created from template. | `.codex/agents/stage_execution_ledger_template.md` |
