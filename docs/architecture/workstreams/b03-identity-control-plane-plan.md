---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B03
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b03-identity-control-plane-module.md
plan_doc: docs/architecture/workstreams/b03-identity-control-plane-plan.md
prompt_pack_dir: .codex/agents/generated/b03-identity-control-plane
stage_ledger: docs/architecture/workstreams/b03-identity-control-plane-stage-reports/b03-identity-control-plane-stage-ledger.md
execution_mode: goal_driven
hard_dependencies:
- B01
- B02
soft_dependencies: []
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
- AC-013
- AC-017
- AC-018
- AC-019
- AC-020
- AC-031
- API-001
- API-002
- API-003
- API-004
- API-005
- API-006
- API-007
- API-008
- API-009
- API-010
- AUTH-001
- AUTH-002
- AUTH-003
- AUTH-004
- AUTH-005
- AUTH-006
- AUTH-007
- AUTH-008
- AUTH-009
- AUTH-010
- AUTH-011
- GAP-012
- GAP-022
- GAP-032
- GAP-033
- JOURNEY-001
- OBJ-STATE-001
- OBJ-STATE-002
- OBJ-STATE-003
- OBJ-STATE-004
- OBJ-STATE-005
- RBAC-001
- RBAC-002
- RBAC-003
- RBAC-004
- RBAC-005
- RBAC-006
- RBAC-007
- RBAC-008
- RISK-008
- SEC-007
- SEC-008
- SEC-010
- SEC-012
- SEC-013
- TEST-INV-007
- TEST-INV-018
- TEST-INV-019
- UC-008
---

# Identity and Control Plane — Initial Plan

## Identity and authority

- program/workstream: `custometry-v1 / B03`;
- authority: normative blueprint, accepted architecture, Program Plan, and generated requirement matrix;
- current proof boundary: planning scaffold only;
- activation rule: this plan remains dormant until its ledger becomes `active` and `.codex/PLANS.md` registers the exact trio.

## Objective and non-goals

Provide workspace-scoped identity, session, authorization, object-lifecycle, API-policy, and audit decisions before protected state is fetched or mutated.

Non-goals: External identity-provider federation, billing, and production deployment policy are outside this workstream.

## Current-state fact ledger

| Type | Fact, assumption, proposal, or unknown | Source/evidence | Consequence |
|---|---|---|---|
| Fact | The matrix allocates 55 primary requirements to `B03`. | `docs/architecture/program/requirement-matrix.json` | The plan may not absorb another workstream's primary ownership. |
| Fact | Hard dependencies are `B01`, `B02`; soft dependencies are none. | Program routing source | Missing hard evidence keeps the ledger dormant. |
| Fact | No implementation stage is authorized by creating this scaffold. | Ledger `dormant`, prompts `outline/false` | No code, migration, browser, runtime, or external mutation may begin. |
| Unknown | S01 contract details not fixed by accepted sources remain decisions, not defaults. | Module definition open-decision section | Stop the affected contract path until resolved. |

## Dependencies and milestones

Release participation is `product_foundation`, `vertical_alpha`, `public_mvp`, `v1_target`. Hard dependency evidence is an entry gate; soft dependencies may use versioned generated contracts temporarily but must reconcile before milestone verification.

## Requirement allocation

- exact primary IDs: 55;
- primary families: `AC` (6), `API` (10), `AUTH` (11), `GAP` (4), `JOURNEY` (1), `OBJ-STATE` (5), `RBAC` (8), `RISK` (1), `SEC` (5), `TEST-INV` (3), `UC` (1);
- source: generated exact matrix; no manually maintained numeric ranges;
- stage prompts may repeat an ID when one requirement needs contract, adapter, browser, and acceptance evidence, but may not reference an ID outside this plan.

## DDD target and contracts

Identity & Workspace owns users, workspaces, memberships, sessions, API tokens, and policy decisions; Audit owns append-only redacted audit events.

Workspace, User, Membership, Session, ScopedApiToken, PolicyDecision, ObjectLifecycle, and AuditEvent; deny-before-fetch and cross-workspace non-disclosure are invariants.

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

No blueprint policy is invented. Credential, session-duration, or token defaults not fixed by accepted sources remain S01 decisions.

Principal risks: Resource-existence leaks, confused-deputy workspace context, stale sessions, token disclosure, and audit failure semantics.

## Change ownership

- planned primary paths: `packages/identity_access`, `packages/audit`, `apps/api`, `apps/web`;
- planning paths: `docs/architecture/workstreams/b03-identity-control-plane-*` and `.codex/agents/generated/b03-identity-control-plane/`;
- foreign exclusions: unrelated dirty files, other workstreams, secrets, generated caches, production systems, and Penpot until separately authorized;
- mixed-file policy: stop when safe hunk separation is impossible;
- branch policy: one authorized short-lived workstream branch; per-stage branches are forbidden.

## Completion rule

The workstream completes only when every non-superseded stage is terminal, the ledger is `completed`, all primary requirements have their matrix-declared evidence, release checkpoints are reconciled, and no blocker remains.
