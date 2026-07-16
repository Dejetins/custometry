---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B04
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b04-execution-compute-artifact-spine-module.md
plan_doc: docs/architecture/workstreams/b04-execution-compute-artifact-spine-plan.md
prompt_pack_dir: .codex/agents/generated/b04-execution-compute-artifact-spine
stage_ledger: docs/architecture/workstreams/b04-execution-compute-artifact-spine-stage-reports/b04-execution-compute-artifact-spine-stage-ledger.md
execution_mode: manual_sequential
hard_dependencies:
- B02
- B03
soft_dependencies:
- B01
stage_ids:
- S00
- S01
- S02
- S03
- S04
- S05
- S06
release_milestones:
- product_foundation
- vertical_alpha
- public_mvp
- v1_target
spec_version: 0.8.2-draft
requirement_ids:
- AC-011
- AC-012
- AC-023
- AC-025
- AC-033
- AC-036
- AC-037
- ADMIN-008
- ARTIFACT-001
- ARTIFACT-002
- ARTIFACT-003
- ARTIFACT-004
- COMPUTE-001
- COMPUTE-002
- COMPUTE-003
- COMPUTE-004
- COMPUTE-005
- COMPUTE-006
- COMPUTE-007
- COMPUTE-008
- COMPUTE-009
- COMPUTE-010
- EXEC-CANCEL-001
- EXEC-CANCEL-002
- EXEC-CANCEL-003
- EXEC-CANCEL-004
- EXEC-CANCEL-005
- EXEC-CANCEL-006
- EXEC-DISPATCH-001
- EXEC-DISPATCH-002
- EXEC-DISPATCH-003
- EXEC-DISPATCH-004
- EXEC-DISPATCH-005
- EXEC-STATE-001
- EXEC-STATE-002
- EXEC-STATE-003
- EXEC-STATE-004
- EXEC-STATE-005
- EXEC-STATE-006
- EXEC-STATE-007
- GAP-008
- GAP-010
- GAP-011
- GAP-026
- GAP-028
- GAP-044
- GAP-045
- PROGRESS-001
- PROGRESS-002
- PROGRESS-003
- PROGRESS-004
- PROGRESS-005
- PROGRESS-006
- PROGRESS-007
- PROGRESS-008
- RISK-003
- RISK-009
- RISK-016
- SEC-002
- TEST-INV-005
- TEST-INV-006
- TEST-INV-014
- TEST-INV-015
- TEST-INV-020
- TEST-INV-024
- TEST-INV-027
- TEST-INV-040
- TEST-INV-041
- UX-JOURNEY-003
- UX-JOURNEY-004
- V1-AC-005
- V1-AC-006
---

# Execution, Compute and Artifact Spine — Initial Plan

## Identity and authority

- program/workstream: `custometry-v1 / B04`;
- authority: normative blueprint, accepted architecture, Program Plan, and generated requirement matrix;
- current proof boundary: planning scaffold only;
- activation rule: this plan remains dormant until its ledger becomes `active` and `.codex/PLANS.md` registers the exact trio.

## Objective and non-goals

Provide authoritative run state, CPU-only dispatch, leases and fencing, cancellation, progress and ETA, outbox delivery, reconciliation, and atomic immutable artifact visibility.

Non-goals: Business analytics, forecast model semantics, remote object storage, GPU execution, and Kubernetes are outside this workstream.

## Current-state fact ledger

| Type | Fact, assumption, proposal, or unknown | Source/evidence | Consequence |
|---|---|---|---|
| Fact | The matrix allocates 72 primary requirements to `B04`. | `docs/architecture/program/requirement-matrix.json` | The plan may not absorb another workstream's primary ownership. |
| Fact | Hard dependencies are `B02`, `B03`; soft dependencies are `B01`. | Program routing source | Missing hard evidence keeps the ledger dormant. |
| Fact | No implementation stage is authorized by creating this scaffold. | Ledger `dormant`, prompts `outline/false` | No code, migration, browser, runtime, or external mutation may begin. |
| Unknown | S01 contract details not fixed by accepted sources remain decisions, not defaults. | Module definition open-decision section | Stop the affected contract path until resolved. |

## Dependencies and milestones

Release participation is `product_foundation`, `vertical_alpha`, `public_mvp`, `v1_target`. Hard dependency evidence is an entry gate; soft dependencies may use versioned generated contracts temporarily but must reconcile before milestone verification.

## Requirement allocation

- exact primary IDs: 72;
- primary families: `AC` (7), `ADMIN` (1), `ARTIFACT` (4), `COMPUTE` (10), `EXEC-CANCEL` (6), `EXEC-DISPATCH` (5), `EXEC-STATE` (7), `GAP` (7), `PROGRESS` (8), `RISK` (3), `SEC` (1), `TEST-INV` (9), `UX-JOURNEY` (2), `V1-AC` (2);
- source: generated exact matrix; no manually maintained numeric ranges;
- stage prompts may repeat an ID when one requirement needs contract, adapter, browser, and acceptance evidence, but may not reference an ID outside this plan.

## DDD target and contracts

Execution Control owns runs, node runs, tasks, leases, cancellation, progress, outbox, and reconciliation; Artifact Lifecycle owns manifests, hashes, retention, authorization, and commit visibility.

Run, NodeRun, TaskEnvelope, Lease, FencingToken, CancellationRequest, ProgressSnapshot, OutboxMessage, and ArtifactManifest; stale leases cannot commit and terminal state is monotonic.

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

No queue product or remote worker topology is assumed. Adapter selection remains behind owned ports.

Principal risks: Duplicate execution, stale commit, split-brain run state, cancellation races, false ETA, artifact partial visibility, and CPU oversubscription.

## Change ownership

- planned primary paths: `packages/execution`, `packages/artifacts`, `apps/orchestrator`, `apps/outbox_dispatcher`, `apps/reconciler`, `apps/worker_data`, `apps/worker_ml`, `apps/worker_report`;
- planning paths: `docs/architecture/workstreams/b04-execution-compute-artifact-spine-*` and `.codex/agents/generated/b04-execution-compute-artifact-spine/`;
- foreign exclusions: unrelated dirty files, other workstreams, secrets, generated caches, production systems, and Penpot until separately authorized;
- mixed-file policy: stop when safe hunk separation is impossible;
- branch policy: one authorized short-lived workstream branch; per-stage branches are forbidden.

## Completion rule

The workstream completes only when every non-superseded stage is terminal, the ledger is `completed`, all primary requirements have their matrix-declared evidence, release checkpoints are reconciled, and no blocker remains.
