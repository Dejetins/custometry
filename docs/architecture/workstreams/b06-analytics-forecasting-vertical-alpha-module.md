---
artifact_kind: module_definition
staged_schema_version: 1
workstream_id: B06
doc_id: ARCH-B06-MODULE-001
title: Analytics and Forecasting Vertical Alpha module definition
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: architecture
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
status: initial
proof_boundary:
  label: b06-analytics-forecasting-vertical-alpha-target-contract
  exclusions:
  - implementation-proof
  - runtime-readiness
  - release-readiness
---

# Analytics and Forecasting Vertical Alpha — Module Definition

> This definition precedes implementation. It is not an activation, stage ledger, or runtime-readiness claim.

## Identity

- workstream: `B06`;
- bounded contexts: Analytics owns analysis specifications and result manifests; Forecasting owns the minimum baseline forecast specification, rolling backtest, candidates, and predictions; Presentation owns ChartSpec and reportable block contracts.
- target packages/apps: `packages/analytics_core`, `packages/analytics_sales`, `packages/forecasting`, `packages/presentation`, `packages/chart_compiler_ts`, `apps/web`, `apps/worker_ml`;
- release milestones: `vertical_alpha`, `public_mvp`, `v1_target`;
- primary requirement IDs: 61 exact allocations from the canonical matrix.

## Purpose and non-goals

Deliver the first complete analytics and baseline-forecasting journey with typed filters, vs LY, Result Trust, Focus mode, ChartSpec/ECharts, monthly net revenue, Seasonal Naive, CatBoost, and rolling backtest.

Non-goals: Forecasting expansion, promotion causality, dashboards, email delivery, operational channels, and XLSX are outside this workstream.

## Ubiquitous language

| Term | Meaning | Not the same as |
|---|---|---|
| `AnalysisSpec` | Versioned metrics, dimensions, filters, period, comparison, grain, and input references. | Transient Web state |
| `TimeComparisonSpec` | Explicit current period and analogous last-year period with alignment rules. | A label saying vs LY |
| `ResultTrust` | Freshness, quality, grain, lineage, and reproducibility evidence for a result. | A decorative badge |
| `ForecastCandidate` | Pinned model/specification evaluated by temporal rolling backtest. | A chart series name |

## Domain model

AnalysisSpec, TimeComparisonSpec, FilterExpression, AnalysisResultManifest, ResultTrust, ChartSpec, FocusState, ForecastSpec, BacktestWindow, ForecastCandidate, ModelMetric, PredictionManifest; analytical values are computed server-side on CPU.

Every write belongs to one context. Cross-context reads use public projections or query ports. Actor, workspace, trace, and contract-version context cross every protected boundary.

## Use cases and contracts

| Command/query/event | Actor/caller | Input/output owner | Errors, idempotency, and version |
|---|---|---|---|
| `RunAnalysis` | Authorized analyst | AnalysisSpec to immutable result manifest | Stable result identity and cancellation |
| `CompileChartSpec` | Web/static renderers | Product-owned ChartSpec | Deterministic ECharts compilation; no Plotly core |
| `RunBaselineForecast` | Authorized analyst | monthly_net_revenue, Seasonal Naive, CatBoost, rolling backtest | Temporal ordering, pinned inputs, comparable metrics |

Public schemas are versioned before external reliance. Unknown state is explicit; it is never mapped to success or empty data.

## Data ownership

Read-only pinned semantic/mart/artifact references; output manifests contain specification identity, input hashes, code/model versions, quality decision, lineage, and locale-neutral values.

Migration, compatibility, retention, lineage, redaction, and rollback are defined before persistence becomes authoritative. No context reads or mutates another context's private tables.

## Ports and adapters

| Port owner | Adapter | Auth/trust | Timeout/retry/unknown state | Degradation |
|---|---|---|---|---|
| Analytics/Forecasting | Execution and artifact ports | Authorized workspace specification | Idempotent result identity, cancellation, progress/ETA | Explicit failed/degraded result |
| Analytics | Semantic model and quality query ports | Pinned versions | No private-table reads | Blocked when mandatory capability is absent |
| Presentation | TypeScript ECharts compiler and SSR renderer | Validated ChartSpec | Deterministic rendering | Data table fallback |

## UI and documentation

Analytics and forecast routes, compact KPI strip with vs LY, searchable typed filters, Chart/Data table switch, Result Trust, route-backed Focus, legend/zoom/brush/drill-down, and complete responsive/accessibility states.

The Web contract includes loading, empty, degraded, forbidden, failed, refresh, unsaved-change, and return-to-origin behavior. Shipped `/docs` and `/help` content follows visibility and localization policy. Penpot mutation requires separately confirmed live authority.

## Operations

Analysis/forecast latency, CPU cores, queue and cancellation, progress/ETA accuracy, result freshness, backtest coverage, model error metrics, compiler/render failures, and no WebGL in v1.

All logs, traces, notifications, and evidence redact secrets and raw PII. Capacity assumptions remain single-server and CPU-only through `v1_target` unless an ADR changes the topology.

## Fixtures and acceptance

Deterministic monthly net revenue with known seasonality, last-year alignment, missing periods, filter cases, quality states, baseline forecasts, rolling windows, and expected metrics.

Acceptance follows S00–S06 and requires unit/property, contract, real adapter, browser, runtime, recovery, security, or performance evidence only where the changed boundary triggers it.

## Contract impact

This initial definition is a `compatible-change` to repository planning artifacts and an `unknown` future product contract until S01 freezes schemas. It changes no running API, persistence, browser behavior, or external side effect.

## Open decisions and blockers

OPEN-008 is a hard B06-S01 decision gate for its affected analytics/forecast contract; B09 cannot absorb or postpone the Vertical Alpha baseline slice.

Principal risks: Comparison misalignment, filter semantic drift, misleading chart animation, mutable result identity, temporal leakage, incomparable backtests, and client-side analytical computation.
