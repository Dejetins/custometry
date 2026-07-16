---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B06
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b06-analytics-forecasting-vertical-alpha-module.md
plan_doc: docs/architecture/workstreams/b06-analytics-forecasting-vertical-alpha-plan.md
prompt_pack_dir: .codex/agents/generated/b06-analytics-forecasting-vertical-alpha
stage_ledger: docs/architecture/workstreams/b06-analytics-forecasting-vertical-alpha-stage-reports/b06-analytics-forecasting-vertical-alpha-stage-ledger.md
execution_mode: goal_driven
hard_dependencies:
- B01
- B02
- B03
- B04
- B05
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
- vertical_alpha
- public_mvp
- v1_target
spec_version: 0.8.2-draft
requirement_ids:
- AC-007
- AC-008
- CHART-001
- CHART-002
- CHART-003
- CHART-004
- CHART-005
- CHART-006
- CHART-009
- CHART-010
- CHART-011
- CHART-014
- CHART-015
- CHART-016
- CHART-017
- COMPARE-001
- COMPARE-002
- COMPARE-003
- COMPARE-004
- COMPARE-005
- COMPARE-006
- COMPARE-007
- FOCUS-001
- FOCUS-002
- FOCUS-003
- FOCUS-004
- FOCUS-005
- FOCUS-006
- FOCUS-007
- FOCUS-008
- FOCUS-009
- FOCUS-010
- FOCUS-011
- FOCUS-012
- GAP-013
- GAP-015
- GAP-037
- GAP-047
- JOURNEY-004
- OPEN-008
- RISK-005
- RISK-018
- RISK-020
- SEC-014
- TEST-INV-003
- TEST-INV-004
- TEST-INV-008
- TEST-INV-009
- TEST-INV-030
- TEST-INV-033
- TEST-INV-043
- TEST-INV-049
- UC-004
- UC-005
- UC-012
- UC-017
- UC-018
- UI-AN-001
- UX-JOURNEY-005
- V1-AC-001
- V1-AC-016
---

# Analytics and Forecasting Vertical Alpha — Initial Plan

## Identity and authority

- program/workstream: `custometry-v1 / B06`;
- authority: normative blueprint, accepted architecture, Program Plan, and generated requirement matrix;
- current proof boundary: planning scaffold only;
- activation rule: this plan remains dormant until its ledger becomes `active` and `.codex/PLANS.md` registers the exact trio.

## Objective and non-goals

Deliver the first complete analytics and baseline-forecasting journey with typed filters, vs LY, Result Trust, Focus mode, ChartSpec/ECharts, monthly net revenue, Seasonal Naive, CatBoost, and rolling backtest.

Non-goals: Forecasting expansion, promotion causality, dashboards, email delivery, operational channels, and XLSX are outside this workstream.

## Current-state fact ledger

| Type | Fact, assumption, proposal, or unknown | Source/evidence | Consequence |
|---|---|---|---|
| Fact | The matrix allocates 61 primary requirements to `B06`. | `docs/architecture/program/requirement-matrix.json` | The plan may not absorb another workstream's primary ownership. |
| Fact | Hard dependencies are `B01`, `B02`, `B03`, `B04`, `B05`; soft dependencies are none. | Program routing source | Missing hard evidence keeps the ledger dormant. |
| Fact | No implementation stage is authorized by creating this scaffold. | Ledger `dormant`, prompts `outline/false` | No code, migration, browser, runtime, or external mutation may begin. |
| Unknown | S01 contract details not fixed by accepted sources remain decisions, not defaults. | Module definition open-decision section | Stop the affected contract path until resolved. |

## Dependencies and milestones

Release participation is `vertical_alpha`, `public_mvp`, `v1_target`. Hard dependency evidence is an entry gate; soft dependencies may use versioned generated contracts temporarily but must reconcile before milestone verification.

## Requirement allocation

- exact primary IDs: 61;
- primary families: `AC` (2), `CHART` (13), `COMPARE` (7), `FOCUS` (12), `GAP` (4), `JOURNEY` (1), `OPEN` (1), `RISK` (3), `SEC` (1), `TEST-INV` (8), `UC` (5), `UI-AN` (1), `UX-JOURNEY` (1), `V1-AC` (2);
- source: generated exact matrix; no manually maintained numeric ranges;
- stage prompts may repeat an ID when one requirement needs contract, adapter, browser, and acceptance evidence, but may not reference an ID outside this plan.

## DDD target and contracts

Analytics owns analysis specifications and result manifests; Forecasting owns the minimum baseline forecast specification, rolling backtest, candidates, and predictions; Presentation owns ChartSpec and reportable block contracts.

AnalysisSpec, TimeComparisonSpec, FilterExpression, AnalysisResultManifest, ResultTrust, ChartSpec, FocusState, ForecastSpec, BacktestWindow, ForecastCandidate, ModelMetric, PredictionManifest; analytical values are computed server-side on CPU.

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

OPEN-008 is a hard B06-S01 decision gate for its affected analytics/forecast contract; B09 cannot absorb or postpone the Vertical Alpha baseline slice.

Principal risks: Comparison misalignment, filter semantic drift, misleading chart animation, mutable result identity, temporal leakage, incomparable backtests, and client-side analytical computation.

## Change ownership

- planned primary paths: `packages/analytics_core`, `packages/analytics_sales`, `packages/forecasting`, `packages/presentation`, `packages/chart_compiler_ts`, `apps/web`, `apps/worker_ml`;
- planning paths: `docs/architecture/workstreams/b06-analytics-forecasting-vertical-alpha-*` and `.codex/agents/generated/b06-analytics-forecasting-vertical-alpha/`;
- foreign exclusions: unrelated dirty files, other workstreams, secrets, generated caches, production systems, and Penpot until separately authorized;
- mixed-file policy: stop when safe hunk separation is impossible;
- branch policy: one authorized short-lived workstream branch; per-stage branches are forbidden.

## Completion rule

The workstream completes only when every non-superseded stage is terminal, the ledger is `completed`, all primary requirements have their matrix-declared evidence, release checkpoints are reconciled, and no blocker remains.
