---
doc_id: ARCH-BOUNDED-CONTEXT-MAP-001
title: Custometry bounded context map
doc_version: 2
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [ARCH-PRINCIPLE-001]
status: accepted
proof_boundary:
  label: target-ownership-and-dependency-policy
  exclusions: [implemented-import-boundaries, runtime-integration-proof]
---

# Custometry Bounded Context Map

## Purpose

This map establishes DDD ownership and permitted integration directions for the modular monolith. It elaborates on blueprint sections 17.2 and 25 but does not create separate product requirements.

## Contexts and ownership

| Context | Package(s) | Owns | Primary inputs/outputs |
|---|---|---|---|
| Identity & Workspace | `identity_access` | users, roles, memberships, workspaces, sessions, API tokens, policy checks | actor/workspace context, permission decisions, audit subjects |
| Connection Catalog | `connection_catalog` | connections, secret metadata, source catalog snapshots | connection specs, catalog projections, connection health |
| Semantic Model | `semantic_model` | datasets, entity/field mappings, joins, metrics, filter-field registry, capabilities | immutable semantic versions, typed semantic contracts |
| Data Documentation | `data_documentation` | Data Guides, versions, template validation, publication lifecycle | sanitized Markdown, permission-aware guide projection |
| Ingestion | `ingestion` | extract specs, watermarks, landing manifests | source reads, immutable landing artifacts, schema observations |
| Artifact Lifecycle | `artifacts` | manifests, hashes, retention, authorization, commit visibility | immutable artifact references and access decisions |
| Execution Control | `execution` | pipelines, schedules, runs/node runs, outbox, leases, cancellation, reconciliation | commands/tasks, authoritative run state, progress events |
| Data Quality | `data_quality` | rules, reports, drift, remediation/waiver decisions | DQ evidence, gate decisions, issue lifecycle |
| Analytics | `analytics_core`, `analytics_customer`, `analytics_sales` | analysis specs, result manifests, segments and domain analytics | bounded results, reportable block data, `TimeComparisonSpec` |
| Promotion Journal | `promotion_journal` | immutable promotion versions, planned/actual windows, channel scope, audience bindings | promotion overlays, `range_timeline` items |
| Forecasting | `forecasting` | forecast specs, backtests, model registry, predictions | forecast artifacts, metrics, readiness/degradation |
| Presentation & Reports | `presentation`, `chart_compiler_ts` | `ChartSpec`, compiler contract, dashboards, report definitions/snapshots, rendered/export metadata | validated presentation specs and reproducible snapshots |
| Report Delivery | `report_delivery` | sender/domain policies, deliveries, attempts, reconciliation | user-initiated email commands and delivery status |
| Notifications | `notifications` | events, preferences, in-app/operational deliveries | permission-aware operational notifications |
| Audit | `audit` | append-only audit events and redacted projections | audit records and authorized queries |

## Areas that are not bounded contexts

| Area | Role |
|---|---|
| `apps/*` | Delivery/process composition roots; they do not own business rules |
| `contracts` | Narrow shared kernel: locale-neutral identifiers, envelopes, trace metadata, and version primitives |
| `localization` | Catalogs and locale formatting; domain IDs and calculations do not depend on language |
| `plugin_sdk` | Trusted extension boundary and compatibility contract |
| `chart_compiler_ts` | Shared deterministic compiler for Web and the static renderer; not a source of analytical values |
| `plugins/*` | Trusted outbound/source adapters, not owners of product state |

## Dependency rules

### Compile-time

1. `domain` does not import application code, adapters, or frameworks.
2. `application` imports its own domain and ports owned by its context.
3. An adapter imports the port and the technical library it encapsulates.
4. `apps/*` imports application contracts and adapters only for wiring.
5. A domain package does not import another context's private domain or application implementation.
6. Cross-context DTOs and events live with the contract owner or in the narrow `packages/contracts` shared kernel; the shared kernel must not become a generic `utils` package.
7. TypeScript Web uses the generated client and versioned schemas; it does not import backend persistence or domain types.

### Runtime

- Callers pass `workspace_id`, actor and permission context, trace identity, and contract version.
- A write path belongs to exactly one context.
- A cross-context read uses a public projection or query port; application code must not read private tables directly.
- A synchronous call is used for a request-driven decision with immediate failure; an event/outbox is used for durable asynchronous handoff.
- Every delivery path assumes duplicates are possible and therefore requires an idempotency identity.
- Integration failure is not concealed by empty data; the caller receives a stable degraded or failed state.

## Primary relationships

| Caller | Owner/callee contract | Form | Consistency/failure rule |
|---|---|---|---|
| Any workspace use case | Identity & Workspace | synchronous authorization port | deny before fetch; lack of permission does not reveal the resource |
| Connection Catalog | Audit | append command/outbox | connection or secret metadata changes are recorded without secret values |
| Ingestion | Connection Catalog | versioned connection snapshot | the task pins the connection version; rotation does not change a running task |
| Ingestion | Artifact Lifecycle | artifact commit port | staging is invisible; only an atomic manifest makes an artifact available |
| Execution Control | all executable contexts | versioned task envelope | at-least-once, lease/fencing, retry classes, and reconciliation |
| Data Quality | Semantic Model + Artifacts | pinned semantic/artifact references | the report is reproducible; a missing input means blocked/failed, not a silent skip |
| Analytics | Semantic Model + DQ + Artifacts | versioned queries/references | result identity includes inputs, specification, and code; the DQ decision remains visible |
| Promotion Journal | Presentation/Analytics | immutable overlay projection | descriptive only; audience binding and window version are pinned |
| Forecasting | Semantic Model + DQ + Artifacts | pinned feature/series references | temporal ordering and model/specification identity are required |
| Presentation | Analytics/Forecasting/Promotions | `ReportSnapshot`/`ChartSpec` ports | presentation state does not change result identity; invalid specifications are rejected before rendering |
| Report Delivery | Presentation + Identity | immutable snapshot + sender policy | user-initiated, idempotent, allowlisted domains, and reconciliation of unknown state |
| Notifications | domain events + Identity | outbox/event projection | permissions are rechecked before display or delivery |
| All mutating use cases | Audit | append-only redacted event | audit failure policy is decided before the side effect; raw PII and secrets are forbidden |

## PostgreSQL ownership model

A single PostgreSQL deployment does not imply a shared-table model. Every migration and table has an owning context. Repositories live in the owning package's adapter layer. A cross-context foreign key is permitted only as a documented integrity contract; it does not give another context's application layer the right to mutate the row. Read models may denormalize public projections with lineage, version, and explicit freshness semantics.

## Rules for changing the map

- A new bounded context requires a volatility, failure, or ownership rationale, not merely a new directory.
- Extracting a separate service before `v1_target` is prohibited without an ADR that establishes an independent scale, trust, failure, or release boundary.
- Moving ownership is a contract change and requires a consumer inventory, migration, compatibility window, and rollback.
- `check_ddd_boundaries` detects violations of dependency rules. An exception is permitted only through an explicit allowlist with an owner, rationale, and expiry or review trigger.

## Acceptance of a new module

Before implementation, the responsible specification or vertical ticket names
the module purpose and non-goals, vocabulary, aggregates and invariants,
commands, queries, events, data ownership, public ports, permissions,
idempotency/retry behavior, UI routes and states, observability, fixtures, and
proof boundary. The artifact choice and execution rules are defined in
[development-operating-model.md](./development-operating-model.md).
