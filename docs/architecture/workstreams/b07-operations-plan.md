---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B07
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b07-operations-module.md
plan_doc: docs/architecture/workstreams/b07-operations-plan.md
prompt_pack_dir: .codex/agents/generated/b07-operations
stage_ledger: docs/architecture/workstreams/b07-operations-stage-reports/b07-operations-stage-ledger.md
execution_mode: goal_driven
hard_dependencies:
- B01
- B03
- B04
- B06
soft_dependencies:
- B05
stage_ids:
- S00
- S01
- S02
- S03
- S04
- S05
- S06
release_milestones:
- public_mvp
- v1_target
spec_version: 0.8.2-draft
requirement_ids:
- AC-027
- AC-030
- AC-040
- ADMIN-001
- ADMIN-003
- ADMIN-005
- GAP-036
- JOURNEY-006
- NOTIFY-001
- NOTIFY-002
- NOTIFY-003
- NOTIFY-004
- NOTIFY-005
- NOTIFY-007
- SCHEDULE-001
- SCHEDULE-002
- SCHEDULE-003
- SCHEDULE-004
- SCHEDULE-005
- UC-010
---

# Operations — Initial Plan

## Identity and authority

- program/workstream: `custometry-v1 / B07`;
- authority: normative blueprint, accepted architecture, Program Plan, and generated requirement matrix;
- current proof boundary: planning scaffold only;
- activation rule: this plan remains dormant until its ledger becomes `active` and `.codex/PLANS.md` registers the exact trio.

## Objective and non-goals

Provide governed schedules, Operator Center visibility, run control, and the public-MVP in-app notification subset.

Non-goals: Operational email/webhook channels, plugin lifecycle, and user-sent report email are owned by B11 and B10, not this workstream.

## Current-state fact ledger

| Type | Fact, assumption, proposal, or unknown | Source/evidence | Consequence |
|---|---|---|---|
| Fact | The matrix allocates 20 primary requirements to `B07`. | `docs/architecture/program/requirement-matrix.json` | The plan may not absorb another workstream's primary ownership. |
| Fact | Hard dependencies are `B01`, `B03`, `B04`, `B06`; soft dependencies are `B05`. | Program routing source | Missing hard evidence keeps the ledger dormant. |
| Fact | No implementation stage is authorized by creating this scaffold. | Ledger `dormant`, prompts `outline/false` | No code, migration, browser, runtime, or external mutation may begin. |
| Unknown | S01 contract details not fixed by accepted sources remain decisions, not defaults. | Module definition open-decision section | Stop the affected contract path until resolved. |

## Dependencies and milestones

Release participation is `public_mvp`, `v1_target`. Hard dependency evidence is an entry gate; soft dependencies may use versioned generated contracts temporarily but must reconcile before milestone verification.

## Requirement allocation

- exact primary IDs: 20;
- primary families: `AC` (3), `ADMIN` (3), `GAP` (1), `JOURNEY` (1), `NOTIFY` (6), `SCHEDULE` (5), `UC` (1);
- source: generated exact matrix; no manually maintained numeric ranges;
- stage prompts may repeat an ID when one requirement needs contract, adapter, browser, and acceptance evidence, but may not reference an ID outside this plan.

## DDD target and contracts

Execution Control owns schedules and run operations; Notifications owns in-app events, preferences, permission-aware projections, acknowledgement, and resolution.

Schedule, ScheduleVersion, RunIntent, OperatorProjection, NotificationEvent, NotificationPreference, Acknowledgement, Resolution; schedules do not duplicate run identity and notifications are re-authorized before display.

The implementation preserves dependency direction: domain → application ports → adapters → composition roots. Public APIs, DTOs, events, persisted schemas, config/defaults, idempotency identity, and browser-visible defaults require compatibility classification and migration when changed.

## Stage plan

| Stage | Outcome | Entry gate | Exit evidence | Rollback/stop gate |
|---|---|---|---|---|
| `S00` | Discovery | Previous stage accepted; hard dependencies remain observed | Confirm source-anchored scope, ownership, vocabulary, dependencies, risks, and stop gates. | Missing authority, contract, or boundary evidence blocks progression |
| `S01` | UX and contract | Previous stage accepted; hard dependencies remain observed | Freeze routes, states, commands, queries, events, schemas, permissions, errors, and compatibility. | Missing authority, contract, or boundary evidence blocks progression |
| `S02` | Domain and application | Previous stage accepted; hard dependencies remain observed | Implement or specify framework-free aggregates, invariants, policies, use cases, and owned ports. | Missing authority, contract, or boundary evidence blocks progression |
| `S03` | Adapters | Previous stage accepted; hard dependencies remain observed | Implement or specify persistence and outbound adapters, migrations, retry classes, and unknown-state reconciliation. | Missing authority, contract, or boundary evidence blocks progression |
| `S04` | Web integration | Previous stage accepted; hard dependencies remain observed | Connect the accepted contract to the Frost Web experience with complete system states and accessibility. | Missing authority, contract, or boundary evidence blocks progression |
| `S05` | Real-boundary proof | Previous stage accepted; hard dependencies remain observed | Observe the nearest database, API, browser, worker, Compose, or artifact boundary required by the slice. | Missing authority, contract, or boundary evidence blocks progression |
| `S06` | Acceptance | Previous stage accepted; hard dependencies remain observed | Reconcile requirement evidence, contracts, docs, rollback, residual risk, and independent review. | Missing authority, contract, or boundary evidence blocks progression |

## Migration, rollback, and recovery

S01 records compatibility and migration obligations before implementation. Stateful S03 work requires empty-install and supported upgrade evidence. Rollback never deletes authoritative state blindly; unknown external or durable effects are reconciled through owned identities.

## Validation and proof boundaries

Focused validation starts with the smallest affected unit/contract and expands to database, API, browser, worker, Compose, recovery, security, performance, or delivery only when that boundary is changed. Green planning validators do not prove implementation or release readiness.

## Documentation continuity

Keep the Program Plan, routing, generated matrix, module definition, plan, ledger, stage prompts, architecture index, affected contracts, and runbooks synchronized. Product obligations first change the normative blueprint and human mirror.

## Risks and open decisions

Channel delivery remains explicitly deferred to B11; this workstream cannot add anonymous alert email or webhook side effects.

Principal risks: Duplicate scheduling, stale operator actions, unsafe retry, notification leakage, alert fatigue, and hiding unknown execution state.

## Change ownership

- planned primary paths: `packages/execution`, `packages/notifications`, `apps/scheduler`, `apps/orchestrator`, `apps/reconciler`, `apps/web`;
- planning paths: `docs/architecture/workstreams/b07-operations-*` and `.codex/agents/generated/b07-operations/`;
- foreign exclusions: unrelated dirty files, other workstreams, secrets, generated caches, production systems, and Penpot until separately authorized;
- mixed-file policy: stop when safe hunk separation is impossible;
- branch policy: one authorized short-lived workstream branch; per-stage branches are forbidden.

## Completion rule

The workstream completes only when every non-superseded stage is terminal, the ledger is `completed`, all primary requirements have their matrix-declared evidence, release checkpoints are reconciled, and no blocker remains.
