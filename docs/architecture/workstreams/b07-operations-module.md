---
artifact_kind: module_definition
staged_schema_version: 1
workstream_id: B07
doc_id: ARCH-B07-MODULE-001
title: Operations module definition
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: architecture
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
status: initial
proof_boundary:
  label: b07-operations-target-contract
  exclusions:
  - implementation-proof
  - runtime-readiness
  - release-readiness
---

# Operations — Module Definition

> This definition precedes implementation. It is not an activation, stage ledger, or runtime-readiness claim.

## Identity

- workstream: `B07`;
- bounded contexts: Execution Control owns schedules and run operations; Notifications owns in-app events, preferences, permission-aware projections, acknowledgement, and resolution.
- target packages/apps: `packages/execution`, `packages/notifications`, `apps/scheduler`, `apps/orchestrator`, `apps/reconciler`, `apps/web`;
- release milestones: `public_mvp`, `v1_target`;
- primary requirement IDs: 20 exact allocations from the canonical matrix.

## Purpose and non-goals

Provide governed schedules, Operator Center visibility, run control, and the public-MVP in-app notification subset.

Non-goals: Operational email/webhook channels, plugin lifecycle, and user-sent report email are owned by B11 and B10, not this workstream.

## Ubiquitous language

| Term | Meaning | Not the same as |
|---|---|---|
| `Schedule` | Versioned recurrence and target specification that creates idempotent run intents. | A cron string alone |
| `OperatorView` | Permission-aware projection of runs, attempts, node state, and actions. | Direct access to execution tables |
| `Notification` | Permission-checked in-app operational event with acknowledgement state. | User-sent report email |
| `Reconciliation` | Process that resolves stale or unknown execution/delivery state. | Blind retry |

## Domain model

Schedule, ScheduleVersion, RunIntent, OperatorProjection, NotificationEvent, NotificationPreference, Acknowledgement, Resolution; schedules do not duplicate run identity and notifications are re-authorized before display.

Every write belongs to one context. Cross-context reads use public projections or query ports. Actor, workspace, trace, and contract-version context cross every protected boundary.

## Use cases and contracts

| Command/query/event | Actor/caller | Input/output owner | Errors, idempotency, and version |
|---|---|---|---|
| `Create/Update/DisableSchedule` | Authorized operator | Versioned schedule command | Idempotent recurrence identity |
| `QueryOperatorCenter / RetryRun / CancelRun` | Authorized operator | Execution public projections and commands | No private-table reads; fenced effects |
| `Project/AcknowledgeNotification` | Execution events or user | In-app notification contracts | Dedupe identity and permission recheck |

Public schemas are versioned before external reliance. Unknown state is explicit; it is never mapped to success or empty data.

## Data ownership

Execution-owned schedule/run state and notification-owned projections/preferences; notification content is redacted and links to authorized source objects.

Migration, compatibility, retention, lineage, redaction, and rollback are defined before persistence becomes authoritative. No context reads or mutates another context's private tables.

## Ports and adapters

| Port owner | Adapter | Auth/trust | Timeout/retry/unknown state | Degradation |
|---|---|---|---|---|
| Scheduler | Execution submit port | Service identity and workspace scope | Idempotent run intent; reconcile unknown submit | Schedule degraded |
| Notifications | Execution event/outbox consumer | Versioned event and actor policy | At-least-once dedupe | Projection lag visible |
| Web operations | API projections and commands | Operator permissions | Stable errors and cancellation semantics | Read-only degraded view |

## UI and documentation

Runs, Operator Center, schedules, in-app notifications, acknowledgement/resolution, retry/cancel actions, filters, freshness, full-screen Focus for tables/charts, and route-backed return.

The Web contract includes loading, empty, degraded, forbidden, failed, refresh, unsaved-change, and return-to-origin behavior. Shipped `/docs` and `/help` content follows visibility and localization policy. Penpot mutation requires separately confirmed live authority.

## Operations

Schedule lag, missed/duplicate intents, run failure rate, reconciliation backlog, notification projection lag, acknowledgement latency, and permission-denied audit events.

All logs, traces, notifications, and evidence redact secrets and raw PII. Capacity assumptions remain single-server and CPU-only through `v1_target` unless an ADR changes the topology.

## Fixtures and acceptance

Deterministic schedules and runs across queued/running/succeeded/failed/cancelling states, duplicate triggers, stale attempts, notifications, preferences, acknowledgement, and cross-workspace denial.

Acceptance follows S00–S06 and requires unit/property, contract, real adapter, browser, runtime, recovery, security, or performance evidence only where the changed boundary triggers it.

## Contract impact

This initial definition is a `compatible-change` to repository planning artifacts and an `unknown` future product contract until S01 freezes schemas. It changes no running API, persistence, browser behavior, or external side effect.

## Open decisions and blockers

Channel delivery remains explicitly deferred to B11; this workstream cannot add anonymous alert email or webhook side effects.

Principal risks: Duplicate scheduling, stale operator actions, unsafe retry, notification leakage, alert fatigue, and hiding unknown execution state.
