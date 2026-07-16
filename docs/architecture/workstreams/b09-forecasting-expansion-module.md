---
artifact_kind: module_definition
staged_schema_version: 1
doc_id: MODULE-B09-FORECASTING-EXPANSION
title: B09 Forecasting Expansion module definition
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
workstream_id: B09
owner: forecasting
status: initial
requirement_ids: [AC-009, AC-010, AC-038, GAP-014, GAP-016, JOURNEY-005, SEC-005]
proof_boundary:
  label: planned-b09-module-boundary
  exclusions: [trained-model-proof, production-monitoring-proof, autonomous-promotion, causal-forecasting, release-readiness]
---

# B09 Forecasting Expansion — module definition

## Purpose and boundaries

B09 expands the B06 baseline forecast into a governed forecasting product:
versioned forecast specifications, model registry, training/backtest
orchestration, model comparison, prediction artifacts, monitoring, and safe
promotion/rollback of a champion. It consumes B08 customer/promotion features
when available but does not own their definitions.

It does not own generic execution (B04), ingestion/metrics (B05), baseline
analytics presentation (B06), operational center (B07), reporting delivery
(B10), or plugin/runtime channels (B11).

## Ubiquitous language

| Term | Meaning |
|---|---|
| Forecast specification version | Immutable target, grain, horizon, calendar, feature, split, metric, and policy contract |
| Training dataset version | Immutable artifact resolved from accepted source/feature versions |
| Backtest | Rolling-origin evaluation with no future leakage |
| Model version | Immutable algorithm, hyperparameters, code, environment, training data, and metrics |
| Baseline | Required Seasonal Naive or statistical comparator |
| Candidate | Evaluated but not promoted model version |
| Champion | Audited model selected for a governed scope |
| Prediction artifact | Immutable point/interval forecast with lineage |
| Monitoring window | Versioned observed period used for drift/error evaluation |

## Domain model and invariants

- Every backtest/model version references an existing immutable
  `forecast_spec_version_id` in the same workspace.
- Target, grain, hierarchy, horizon, calendar/timezone, incomplete-period
  policy, feature availability, cutoffs, loss/metrics, and intervals are frozen
  in the spec.
- Backtests use rolling origins and prohibit feature values unavailable at each
  cutoff.
- Seasonal Naive and one statistical baseline remain visible in comparison;
  CatBoost or another advanced model cannot be accepted without them.
- Current incomplete periods are excluded unless an explicit versioned policy
  says otherwise.
- Promotion is an audited state transition, not a mutable status flag on the
  same model payload.
- Prediction, interval, backtest, and monitoring artifacts are immutable and
  carry source lineage, code version, execution profile, and Result Trust.
- Retraining is scheduled through B04/B07 and does not occur invisibly on read.

## Commands, queries, and events

Commands create/publish forecast specs, launch training/backtests, compare
models, promote/rollback champions, and register monitoring evaluations.
Queries resolve specs, models, comparisons, prediction products, drift/error,
and lineage. Events are versioned and outbox-delivered for model trained,
comparison ready, champion changed, monitoring degraded, and rollback.

All long commands return run/status identity, support cancellation where safe,
and remain idempotent under retry.

## Ports and dependencies

- B04 supplies run/lease/fencing/cancellation/artifact/progress infrastructure.
- B05 supplies governed time series, metrics, calendars, features, DQ, and
  source lineage.
- B06 supplies baseline forecast/reportable ChartSpec contracts.
- B08 supplies optional customer/segment/promotion features through versioned
  artifacts.
- B07 is a soft operational/scheduling integration.
- B03 supplies workspace, permissions, tokens, audit, and actor context.

The forecasting domain remains free of FastAPI, Celery, concrete databases,
filesystem, CatBoost runtime wiring, or chart-engine imports. Adapters implement
training libraries, PostgreSQL metadata, artifact storage, and UI/API.

## Persistence and model artifacts

PostgreSQL owns specs, versions, state transitions, model registry metadata,
comparisons, monitoring definitions, and audited champion scopes. Training
tables, serialized models, predictions, intervals, explanation payloads, and
backtest results are immutable artifacts with checksums and schemas.

Model serialization is never trusted as executable input without approved
format, integrity, compatibility, and supply-chain policy.

## UI and operations

Owned surfaces include forecast overview/detail, specification lifecycle,
backtest launch/history, model comparison, champion promotion/rollback,
prediction charts/tables, and monitoring status. They preserve `vs LY`,
interval labeling, Result Trust, local filters, Focus/Explore, progress/ETA,
and safe non-animated dense/domain-changing data.

Operations expose queue/run identity, resource allocation, training versions,
error codes, monitoring freshness, and rollback history without secrets or raw
sensitive features.

## Contract impact and acceptance

Changing target/grain/calendar/cutoff/feature-availability/backtest identity,
model/spec foreign-key semantics, champion scope, prediction schema, or
monitoring meaning is breaking after publication. Optional metadata is
compatible only when result identity and reproducibility remain stable.

B09 hard-depends on B04, B05, B06, and B08; B07 is soft. Completion requires
baseline comparisons, leakage-negative tests, real training/backtest adapter
evidence, browser proof, monitoring/rollback evidence, reproducible resource
receipts, cold review, and all routed requirements reconciled.
