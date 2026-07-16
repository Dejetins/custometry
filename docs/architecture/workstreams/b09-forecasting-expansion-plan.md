---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B09
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b09-forecasting-expansion-module.md
plan_doc: docs/architecture/workstreams/b09-forecasting-expansion-plan.md
prompt_pack_dir: .codex/agents/generated/b09-forecasting-expansion
stage_ledger: docs/architecture/workstreams/b09-forecasting-expansion-stage-reports/b09-forecasting-expansion-stage-ledger.md
execution_mode: goal_driven
hard_dependencies: [B04, B05, B06, B08]
soft_dependencies: [B07]
stage_ids: [S00, S01, S02, S03, S04, S05, S06]
release_milestones: [public_mvp, v1_target]
spec_version: 0.8.2-draft
requirement_ids: [AC-009, AC-010, AC-038, GAP-013, GAP-014, GAP-015, GAP-016, JOURNEY-005, RISK-005, SEC-005, TEST-INV-004, TEST-INV-009, TEST-INV-030, UC-005]
---

# B09 Forecasting Expansion — Initial Plan

## Objective and boundary

Expand the accepted B06 baseline into versioned forecast specifications,
rolling backtests, advanced model training/comparison, immutable prediction
products, champion promotion/rollback, and monitoring. Preserve mandatory
Seasonal Naive/statistical baselines and prohibit future leakage.

B09 does not own generic execution, source features/metrics, customer/promotion
semantics, operational center, or report delivery.

## Dependencies and activation

Hard dependencies are B04, B05, B06, and B08; B07 is soft. Activation requires
accepted dependency slices, explicit user authority, and the exact dormant trio
registered in `.codex/PLANS.md`.

## Requirement groups

| Group | IDs | Planned evidence |
|---|---|---|
| Baselines and leakage | `AC-009`, `AC-010`, `TEST-INV-004`, `TEST-INV-009` | rolling-cutoff property tests and real backtests |
| Spec/model identity | `AC-038`, `SEC-005`, `TEST-INV-030` | schema/FK/migration, safe model formats, and immutable registry evidence |
| Product journey | `JOURNEY-005`, `UC-005` | run, compare, promote/rollback, browser and monitoring flow |
| Gaps/risks | `GAP-013`–`GAP-016`, `RISK-005` | model registry, intervals, monitoring, reproducibility, rollback |

The B06-owned Vertical Alpha IDs repeated here are explicit contributor inputs:
B09 must preserve their accepted baseline contracts while expanding the
lifecycle, but does not re-own or postpone them.

## Stage outline

| Stage | Planned outcome | Exit boundary |
|---|---|---|
| `S00` | Inventory B06 baseline, data/features, compute, customer/promotion inputs, and open forecast decisions. | Source-anchored discovery |
| `S01` | Freeze forecast-spec/model/prediction/monitoring schemas, journeys, APIs, errors, and Result Trust. | Versioned contracts |
| `S02` | Implement spec, cutoff, split, comparison, promotion, and monitoring policies. | Domain/property evidence |
| `S03` | Implement model-library, artifact, PostgreSQL, execution, and scheduler adapters. | Real training/backtest/API evidence |
| `S04` | Implement specification, comparison, prediction, promotion/rollback, and monitoring UI. | Browser/accessibility evidence |
| `S05` | Prove reproducibility, leakage negatives, baseline comparison, cancellation, resources, monitoring, and rollback. | Target runtime/benchmark evidence |
| `S06` | Reconcile requirements, docs, migration, cold review, and milestone readiness. | Workstream acceptance |

## Contracts and rollback

Breaking dimensions include target/grain/horizon/calendar/cutoff, feature
availability, split/backtest identity, spec/model FK, champion scope,
prediction/interval schema, and monitoring meaning. Promotion creates an
audited state transition; rollback selects a previous immutable version.
Serialized model formats require integrity, compatibility, supply-chain, and
fallback policies.

## Validation and proof

Required evidence includes property tests at every cutoff, mandatory baselines,
real training/backtest artifacts, deterministic repeated runs within declared
tolerance, cancellation/cleanup, CPU allocation, migration, API/browser flows,
monitoring freshness, and cold review. Unit tests alone cannot prove model
adapter, resource, or prediction behavior.

## Risks and completion rule

Primary risks are leakage, mutable specs, non-reproducible libraries, optimistic
accuracy, hidden baseline removal, unsafe model serialization, and monitoring
without action. Completion requires terminal stages, traceability, real
evidence, rollback, docs, and no unresolved cold-review blocker.
