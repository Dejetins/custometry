---
ledger_name: <plan-slug>-stage-ledger
plan_doc: docs/architecture/<area>/<plan-slug>.md
prompt_pack_dir: .codex/agents/generated/<plan-slug>/
stage_ledger: docs/architecture/<area>/<plan-slug>-stage-reports/<plan-slug>-stage-ledger.md
execution_mode: manual_sequential
overall_status: active
current_stage: "00"
allowed_stage_statuses: [pending, in_progress, accepted, blocked, skipped, superseded]
spec_version: 0.8.2-draft
updated_at: YYYY-MM-DD
---

# <Plan Name> — Stage Ledger

This ledger is the source of truth for current stage, evidence, blocker, and handoff. It does not replace the linked plan or stage prompts.

## Execution rules

- The durable execution trio is exactly `plan_doc + prompt_pack_dir + stage_ledger`.
- `manual_sequential` runs one requested or next allowed stage and stops.
- `goal_driven` may continue only while this ledger explicitly allows the next stage.
- A dependent stage starts only after its predecessor is `accepted` or explicitly `superseded` by a named replacement.
- Validation happens before the ledger update; the ledger update happens before the stage/final report.
- `blocked` records the blocker, evidence, owner/authority needed, and whether safe work remains.
- Do not create `GOAL.md`, a second ledger, branch, worktree, stash, or coordination folder without explicit user authority.

## Linked artifacts

| Artifact | Path | Verified state/hash | Notes |
|---|---|---|---|
| Plan | `docs/architecture/<area>/<plan-slug>.md` | TBD | What and why |
| Prompt pack | `.codex/agents/generated/<plan-slug>/` | TBD | One self-contained prompt per stage |
| Ledger | `docs/architecture/<area>/<plan-slug>-stage-reports/<plan-slug>-stage-ledger.md` | this file | Current execution truth |

## Stage status

| Stage | Requirement IDs/outcome | Status | Prompt | Report/evidence | Predecessor gate | Validation depth | Proof boundary | Blocker | Next allowed |
|---|---|---|---|---|---|---|---|---|---|
| `00` | TBD | `pending` | `.codex/agents/generated/<plan-slug>/00-<slug>.md` | `docs/architecture/<area>/<plan-slug>-stage-reports/00-<slug>.md` | none | TBD | TBD | none | no |

## Current-stage context

- current stage: `00`;
- verified completed work: none;
- required inputs/state/hash: TBD;
- owned paths: TBD;
- foreign changes to preserve: TBD;
- stop gates: TBD;
- next-stage rule: TBD.

## Contract impact

| Stage | API | Ports/DTO/events | Persistence/artifacts | Config/defaults/identity | Service calls/retry/idempotency | Logs/audit/redaction | Browser | Ops/runbooks | Migration/rollback |
|---|---|---|---|---|---|---|---|---|---|
| `00` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | TBD |

## Verification and evidence

| Stage | Local gates | Real-boundary evidence | Result | Evidence path | What this does not prove | Residual risk |
|---|---|---|---|---|---|---|
| `00` | TBD | TBD | TBD | TBD | TBD | TBD |

## File manifest

| Stage | Created | Modified | Deleted | Outside expected paths | Justification | Foreign excluded | Mixed-file status |
|---|---|---|---|---|---|---|---|
| `00` | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## Blockers and approvals

| Stage | Blocker/approval | Severity | Evidence | Required owner/action | Resolved by | Next allowed |
|---|---|---|---|---|---|---|
| `00` | TBD | TBD | TBD | TBD | TBD | no |

## Handoff for the next stage

- accepted facts: TBD;
- decisions that must not be reopened: TBD;
- unresolved risks: TBD;
- exact next prompt: TBD;
- next stage allowed: `no`.

## Change log

| Date | Stage | Change | Evidence |
|---|---|---|---|
| YYYY-MM-DD | `00` | Ledger created from template. | `.codex/agents/stage_execution_ledger_template.md` |
