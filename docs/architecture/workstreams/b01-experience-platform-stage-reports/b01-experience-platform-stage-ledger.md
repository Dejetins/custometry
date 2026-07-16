---
artifact_kind: stage_ledger
staged_schema_version: 1
ledger_name: b01-experience-platform-stage-ledger
workstream_id: B01
plan_doc: docs/architecture/workstreams/b01-experience-platform-plan.md
prompt_pack_dir: .codex/agents/generated/b01-experience-platform
stage_ledger: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
execution_mode: goal_driven
ledger_status: active
current_stage: S00
allowed_stage_statuses: [pending, in_progress, accepted, blocked, skipped, superseded]
spec_version: 0.8.2-draft
updated_at: 2026-07-16
stages:
  - stage_id: S00
    status: pending
    prompt_path: .codex/agents/generated/b01-experience-platform/S00-discovery.md
    prompt_readiness: executable
    previous_gate: null
    next_allowed: true
    requirement_ids: [AC-028, AC-029, GAP-021, GAP-034, GAP-035, GAP-046, RISK-010, TEST-INV-022, TEST-INV-023, TEST-INV-042, TEST-INV-050, TEST-INV-051]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S01
    status: pending
    prompt_path: .codex/agents/generated/b01-experience-platform/S01-ux-contract.md
    prompt_readiness: executable
    previous_gate: S00
    next_allowed: false
    requirement_ids: [A11Y-001, A11Y-002, A11Y-003, A11Y-004, A11Y-005, A11Y-006, A11Y-007, A11Y-008, A11Y-009, A11Y-010, HELP-001, HELP-002, HELP-003, HELP-004, I18N-001, I18N-002, I18N-003, I18N-004, I18N-005, I18N-006, I18N-007, I18N-008, I18N-009, I18N-010, I18N-011, MOTION-001, MOTION-002, MOTION-003, MOTION-004, MOTION-005, MOTION-006, MOTION-007, MOTION-008, MOTION-009, MOTION-010, MOTION-011, MOTION-012, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, THEME-001, THEME-002, THEME-003, THEME-004, THEME-005, THEME-006, THEME-007, THEME-008, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, UX-JOURNEY-001, UX-JOURNEY-002, UX-JOURNEY-006]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S02
    status: pending
    prompt_path: .codex/agents/generated/b01-experience-platform/S02-domain-application.md
    prompt_readiness: executable
    previous_gate: S01
    next_allowed: false
    requirement_ids: [I18N-001, I18N-002, I18N-003, I18N-008, I18N-009, I18N-010, I18N-011, MOTION-001, MOTION-002, MOTION-003, MOTION-004, MOTION-005, MOTION-006, MOTION-007, MOTION-008, MOTION-009, MOTION-010, MOTION-011, MOTION-012, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, TEST-INV-022, TEST-INV-023, TEST-INV-042, TEST-INV-050, TEST-INV-051, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S03
    status: pending
    prompt_path: .codex/agents/generated/b01-experience-platform/S03-adapters.md
    prompt_readiness: executable
    previous_gate: S02
    next_allowed: false
    requirement_ids: [AC-028, AC-029, HELP-001, HELP-002, HELP-003, HELP-004, I18N-001, I18N-002, I18N-003, I18N-004, I18N-005, I18N-006, I18N-007, I18N-008, I18N-009, I18N-010, I18N-011, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, THEME-001, THEME-002, THEME-003, THEME-004, THEME-005, THEME-006, THEME-007, THEME-008]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S04
    status: pending
    prompt_path: .codex/agents/generated/b01-experience-platform/S04-web-integration.md
    prompt_readiness: executable
    previous_gate: S03
    next_allowed: false
    requirement_ids: [A11Y-001, A11Y-002, A11Y-003, A11Y-004, A11Y-005, A11Y-006, A11Y-007, A11Y-008, A11Y-009, A11Y-010, AC-028, AC-029, HELP-001, HELP-002, HELP-003, HELP-004, I18N-001, I18N-002, I18N-003, I18N-004, I18N-005, I18N-006, I18N-007, I18N-008, I18N-009, I18N-010, I18N-011, MOTION-001, MOTION-002, MOTION-003, MOTION-004, MOTION-005, MOTION-006, MOTION-007, MOTION-008, MOTION-009, MOTION-010, MOTION-011, MOTION-012, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, THEME-001, THEME-002, THEME-003, THEME-004, THEME-005, THEME-006, THEME-007, THEME-008, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, UX-JOURNEY-001, UX-JOURNEY-002, UX-JOURNEY-006]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S05
    status: pending
    prompt_path: .codex/agents/generated/b01-experience-platform/S05-real-boundary-proof.md
    prompt_readiness: executable
    previous_gate: S04
    next_allowed: false
    requirement_ids: [A11Y-001, A11Y-002, A11Y-003, A11Y-004, A11Y-005, A11Y-006, A11Y-007, A11Y-008, A11Y-009, A11Y-010, AC-028, AC-029, HELP-001, HELP-002, HELP-003, HELP-004, I18N-001, I18N-002, I18N-003, I18N-004, I18N-005, I18N-006, I18N-007, I18N-008, I18N-009, I18N-010, I18N-011, MOTION-001, MOTION-002, MOTION-003, MOTION-004, MOTION-005, MOTION-006, MOTION-007, MOTION-008, MOTION-009, MOTION-010, MOTION-011, MOTION-012, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, UX-JOURNEY-001, UX-JOURNEY-002, UX-JOURNEY-006, V1-AC-007, V1-AC-017, V1-AC-018]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S06
    status: pending
    prompt_path: .codex/agents/generated/b01-experience-platform/S06-acceptance.md
    prompt_readiness: executable
    previous_gate: S05
    next_allowed: false
    requirement_ids: [AC-028, AC-029, GAP-021, GAP-034, GAP-035, GAP-046, RISK-010, TEST-INV-022, TEST-INV-023, TEST-INV-042, TEST-INV-050, TEST-INV-051, UX-JOURNEY-001, UX-JOURNEY-002, UX-JOURNEY-006, V1-AC-007, V1-AC-017, V1-AC-018]
    evidence: []
    blocker: null
    supersedes: []
---

# B01 Experience Platform — Stage Ledger

This ledger is the sole execution-state authority for B01. The preparation
gate is accepted and the workstream is active. Only S00 Discovery is currently
allowed; no successor is authorized by prompt content or registry text.

## Execution rules

- The durable execution trio is exactly the linked `plan_doc`,
  `prompt_pack_dir`, and `stage_ledger`.
- One Codex Goal owns the active B01 S00–S06 iteration. After an accepted stage,
  it re-reads this ledger and continues only when the successor is current and
  `next_allowed: true`.
- The ledger may become active only after accepted W00 evidence, successful
  preparation review, explicit user authorization, and synchronized
  `.codex/PLANS.md` registration.
- A successor is eligible only after its predecessor is `accepted` or
  explicitly `superseded`, and only when the ledger sets that successor
  `next_allowed: true`.
- A prompt marked executable is prepared content, not authorization.
- Any blocker is written to the current stage before the user-facing report.
- Evidence paths must be repository-relative, durable, redacted, and tied to
  the exact source/runtime state being accepted.
- Penpot access and canonical-file authority are outside this ledger. A stage
  that discovers a Penpot-dependent decision stops and records it rather than
  selecting or mutating a design file.

## Activation transition

The authorized activation edit is narrow:

1. verify W00 and preparation evidence are current;
2. change `ledger_status` from `dormant` to `active`;
3. keep `current_stage: S00`;
4. set only S00 `next_allowed: true`;
5. register the same trio as the sole active workstream in `.codex/PLANS.md`;
6. rerun the staged-work validator before executing S00.

No prompt, plan, branch name, or chat statement may substitute for this state
transition.

## Stage state table

| Stage | Current state | Required predecessor | Prepared outcome |
|---|---|---|---|
| `S00` | pending, allowed | W00 plus explicit activation | current-state and scope discovery |
| `S01` | pending, locked | S00 accepted/superseded | UX and contract freeze |
| `S02` | pending, locked | S01 accepted/superseded | framework-independent policy/application core |
| `S03` | pending, locked | S02 accepted/superseded | generated and local adapters |
| `S04` | pending, locked | S03 accepted/superseded | composed Frost Web experience |
| `S05` | pending, locked | S04 accepted/superseded | fresh real-browser proof |
| `S06` | pending, locked | S05 accepted/superseded | independent acceptance and completion |

## Evidence convention

Accepted stage reports use:

- `S00-discovery.md`;
- `S01-ux-contract.md`;
- `S02-domain-application.md`;
- `S03-adapters.md`;
- `S04-web-integration.md`;
- `S05-real-boundary-proof.md`;
- `S06-acceptance.md`.

Each report records outcome, exact source state, requirement disposition,
contract impact, file manifest, validation commands, nearest real-boundary
evidence, exclusions, fixed blockers, residual risks, and the ledger transition.

## Completion rule

B01 completes only when S00–S06 are accepted or validly superseded, S05 evidence
matches the final browser-affecting state, S06 has an independent cold-review
verdict without unresolved blockers, all applicable gates pass, and the ledger
is changed to `completed` with `current_stage: null` and no next-allowed stage.
This does not complete `product_foundation`, another workstream, deployment, or
the full product release.
