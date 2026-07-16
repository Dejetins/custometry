---
artifact_kind: stage_ledger
staged_schema_version: 1
ledger_name: b02-local-data-lab-stage-ledger
workstream_id: B02
plan_doc: docs/architecture/workstreams/b02-local-data-lab-plan.md
prompt_pack_dir: .codex/agents/generated/b02-local-data-lab
stage_ledger: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
execution_mode: manual_sequential
ledger_status: dormant
current_stage: S00
allowed_stage_statuses: [pending, in_progress, accepted, blocked, skipped, superseded]
spec_version: 0.8.2-draft
updated_at: 2026-07-16
stages:
  - stage_id: S00
    status: pending
    prompt_path: .codex/agents/generated/b02-local-data-lab/S00-discovery.md
    prompt_readiness: executable
    previous_gate: null
    next_allowed: false
    requirement_ids: [AC-014, AC-016]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S01
    status: pending
    prompt_path: .codex/agents/generated/b02-local-data-lab/S01-ux-contract.md
    prompt_readiness: executable
    previous_gate: S00
    next_allowed: false
    requirement_ids: [JOURNEY-001, GAP-019, TEST-INV-040]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S02
    status: pending
    prompt_path: .codex/agents/generated/b02-local-data-lab/S02-domain-application.md
    prompt_readiness: executable
    previous_gate: S01
    next_allowed: false
    requirement_ids: [TEST-INV-009, TEST-INV-010, TEST-INV-011, TEST-INV-012, TEST-INV-013, TEST-INV-016, TEST-INV-026, TEST-INV-028, TEST-INV-031, TEST-INV-033, AC-021, AC-022]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S03
    status: pending
    prompt_path: .codex/agents/generated/b02-local-data-lab/S03-adapters.md
    prompt_readiness: executable
    previous_gate: S02
    next_allowed: false
    requirement_ids: [TEST-INV-010, TEST-INV-011, TEST-INV-012, TEST-INV-013, TEST-INV-016, TEST-INV-026, TEST-INV-028, TEST-INV-031, TEST-INV-033, AC-016, AC-021, AC-022]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S04
    status: pending
    prompt_path: .codex/agents/generated/b02-local-data-lab/S04-web-integration.md
    prompt_readiness: executable
    previous_gate: S03
    next_allowed: false
    requirement_ids: [JOURNEY-001, AC-014, AC-016]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S05
    status: pending
    prompt_path: .codex/agents/generated/b02-local-data-lab/S05-real-boundary-proof.md
    prompt_readiness: executable
    previous_gate: S04
    next_allowed: false
    requirement_ids: [GAP-019, TEST-INV-009, TEST-INV-010, TEST-INV-011, TEST-INV-033, TEST-INV-040, AC-014, AC-016, AC-021]
    evidence: []
    blocker: null
    supersedes: []
  - stage_id: S06
    status: pending
    prompt_path: .codex/agents/generated/b02-local-data-lab/S06-acceptance.md
    prompt_readiness: executable
    previous_gate: S05
    next_allowed: false
    requirement_ids: [JOURNEY-001, GAP-019, AC-014, AC-016, AC-021, AC-022]
    evidence: []
    blocker: null
    supersedes: []
---

# B02 Local Data Lab — Stage Ledger

This is the sole execution-state authority for B02. The prompts are fully
specified, but the ledger is intentionally dormant: no stage is allowed until
W00 is accepted, the user authorizes B02, and `.codex/PLANS.md` activates this
exact trio.

## Execution rules

- The durable execution trio is exactly the linked `plan_doc`,
  `prompt_pack_dir`, and `stage_ledger`.
- `manual_sequential` executes one ledger-allowed stage and stops.
- Dormant means prepared but not authorized; executable prompt content does not
  override `next_allowed: false`.
- A successor starts only after its predecessor is `accepted` or explicitly
  `superseded` and the ledger authorizes that successor.
- Validation precedes every ledger update; the ledger update precedes the
  completion report.
- A blocker records source evidence, affected contract, owner/authority needed,
  safe remaining work, and the next permitted action.
- No stage may infer authorization to commit, push, deploy, delete foreign
  state, use real customer data, or run the benchmark profile.
- Do not create an alternative goal file, ledger, per-stage branch, worktree,
  stash, or coordination directory.

## Linked artifacts

| Artifact | Path | Prepared state | Notes |
|---|---|---|---|
| Program plan | `docs/architecture/program/custometry-program-plan.md` | external canonical link | Defines W00, B01–B13, W14, dependencies, and milestones |
| Module | `docs/architecture/workstreams/b02-local-data-lab-module.md` | initial | Defines B02 ownership, vocabulary, ports, and proof boundary |
| Plan | `docs/architecture/workstreams/b02-local-data-lab-plan.md` | initial | Defines stages, requirements, rollback, and acceptance |
| Prompt pack | `.codex/agents/generated/b02-local-data-lab` | executable, dormant | Exactly one prompt for each S00–S06 stage |
| Ledger | `docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md` | dormant | Current execution truth |

## Stage status

| Stage | Observable outcome | Status | Prompt | Expected report | Predecessor | Proof depth | Next allowed |
|---|---|---|---|---|---|---|---|
| `S00` | Source, ownership, consumer, scenario, and gap inventory frozen | `pending` | `S00-discovery.md` | `S00-discovery.md` in the B02 report directory | none | architecture/contract review | no |
| `S01` | Profile, fixture, reset, migration, benchmark, docs, and consumer contracts frozen | `pending` | `S01-ux-contract.md` | `S01-ux-contract.md` | `S00 accepted` | contract and UX review | no |
| `S02` | Deterministic policy core and fixture semantics implemented | `pending` | `S02-domain-application.md` | `S02-domain-application.md` | `S01 accepted` | focused tests | no |
| `S03` | PostgreSQL, Compose, migration, generation, reset, and verifier adapters complete | `pending` | `S03-adapters.md` | `S03-adapters.md` | `S02 accepted` | integration/database | no |
| `S04` | Local docs and optional-demo consumer integration verified | `pending` | `S04-web-integration.md` | `S04-web-integration.md` | `S03 accepted` | browser/contract | no |
| `S05` | Clean-host real-boundary proof recorded | `pending` | `S05-real-boundary-proof.md` | `S05-real-boundary-proof.md` | `S04 accepted` | runtime/performance evidence | no |
| `S06` | Traceability, rollback, docs, and cold review accepted | `pending` | `S06-acceptance.md` | `S06-acceptance.md` | `S05 accepted` | full workstream acceptance | no |

## Current-stage context

- current stage candidate: `S00`;
- ledger status: `dormant`;
- verified completed B02 work: none;
- hard dependency: accepted `W00`;
- soft coordination dependency: `B01`;
- activation inputs: explicit user authority, clean ownership review, exact trio
  registration, and updated source/hash preconditions;
- existing source declarations are facts, not accepted runtime evidence;
- all unrelated worktree changes are foreign and must be preserved;
- exact next prompt after activation:
  `.codex/agents/generated/b02-local-data-lab/S00-discovery.md`;
- next stage allowed now: `no`.

## Contract impact forecast

| Stage | Profile/manifest | Persistence/migrations | CLI/config | Security/data | Browser/docs | Ops/recovery |
|---|---|---|---|---|---|---|
| `S00` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` | `unknown` |
| `S01` | `compatible-change` proposed | ownership frozen | reset/profile contract frozen | synthetic-only and secret-redaction contract | docs/consumer contract frozen | proof and rollback contract frozen |
| `S02` | versioned implementation | none beyond pure fixtures | none | deterministic/PII tests | none | no runtime claim |
| `S03` | adapter-compatible | migration and schema changes classified per hunk | lifecycle changes classified | grants/network/reset negative paths | no product UI | restart/reset/reseed integration |
| `S04` | safe metadata projection | none expected | profile selection wording | no secret or authorization leakage | compatible docs and consumer integration | local help troubleshooting |
| `S05` | no silent contract edits | real migration evidence only | exact command receipts | real-boundary redaction/isolation evidence | browser proof retained | clean install, restart, reset, resource receipt |
| `S06` | accepted version recorded | rollback/runbook recorded | docs frozen | residual risk recorded | indexes and public visibility checked | independent verdict and milestone decision |

## Required evidence by stage

| Stage | Local gates | Real-boundary evidence | Explicit exclusions |
|---|---|---|---|
| `S00` | staged schema, docs links, requirement allocation | none | no implementation or runtime proof |
| `S01` | schema/examples, contract tests or validators, design review | local docs information architecture if available | no accepted adapter or browser behavior |
| `S02` | deterministic unit/property/golden tests | disposable in-process boundaries only | no Docker/PostgreSQL claim |
| `S03` | focused adapter and migration tests | disposable PostgreSQL integration | no clean-host or benchmark support claim |
| `S04` | docs build, contract parity, accessibility smoke | local `/docs` browser flow and console/network check | no first-admin/workspace authorization claim |
| `S05` | focused gates rerun before runtime | clean Compose, migration, golden hash, restart, reset/reseed, negative isolation, resource receipt | no production firewall, distributed topology, or whole-product release claim |
| `S06` | requirement matrix, docs index, staged validator, grouped applicable gates | independent cold review of complete evidence | no acceptance for another workstream |

## File ownership forecast

| Scope | Paths | Rule |
|---|---|---|
| Primary | `deploy/demo-source/**`, `tests/golden/**`, B02-specific tests/tools/docs/reports/prompts | B02 may change with focused evidence |
| Shared | `compose.yaml`, `deploy/compose/bootstrap.sh`, `migrations/**`, program/docs indexes | modify only scoped hunks after ownership review |
| Foreign | B01 shell internals, B03–B13 domain code, production backup, Penpot | preserve and stop if overlap cannot be separated |

## Activation checklist

- [ ] W00 ledger/evidence is accepted.
- [ ] The user explicitly authorizes B02.
- [ ] Program paths and dependency graph still match this trio.
- [ ] Requirement routing identifies every B02 primary and supporting row.
- [ ] `spec_version` still matches the normative blueprint.
- [ ] S00 source hashes or explicit source-state checks are refreshed.
- [ ] `.codex/PLANS.md` lists only genuinely active/blocked workstreams and adds
      B02 with the exact trio.
- [ ] `ledger_status` changes to `active`, S00 remains `pending`, and only S00
      changes to `next_allowed: true`.

## Handoff

The preparation task may validate this dormant ledger but may not activate it.
After the entire program-preparation package passes independent cold review,
only B01 is activated by the parent task. B02 remains prepared for later
explicit activation.

## Change log

| Date | Stage | Change | Evidence |
|---|---|---|---|
| 2026-07-16 | preparation | Created detailed dormant ledger with executable S00–S06 prompts and all gates closed. | B02 plan, module, and prompt pack |
