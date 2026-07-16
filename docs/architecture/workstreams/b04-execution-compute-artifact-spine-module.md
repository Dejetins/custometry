---
artifact_kind: module_definition
staged_schema_version: 1
workstream_id: B04
doc_id: ARCH-B04-MODULE-001
title: Execution, Compute and Artifact Spine module definition
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: architecture
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
status: initial
proof_boundary:
  label: b04-execution-compute-artifact-spine-target-contract
  exclusions:
  - implementation-proof
  - runtime-readiness
  - release-readiness
---

# Execution, Compute and Artifact Spine — Module Definition

> This definition precedes implementation. It is not an activation, stage ledger, or runtime-readiness claim.

## Identity

- workstream: `B04`;
- bounded contexts: Execution Control owns runs, node runs, tasks, leases, cancellation, progress, outbox, and reconciliation; Artifact Lifecycle owns manifests, hashes, retention, authorization, and commit visibility.
- target packages/apps: `packages/execution`, `packages/artifacts`, `apps/orchestrator`, `apps/outbox_dispatcher`, `apps/reconciler`, `apps/worker_data`, `apps/worker_ml`, `apps/worker_report`;
- release milestones: `product_foundation`, `vertical_alpha`, `public_mvp`, `v1_target`;
- primary requirement IDs: 72 exact allocations from the canonical matrix.

## Purpose and non-goals

Provide authoritative run state, CPU-only dispatch, leases and fencing, cancellation, progress and ETA, outbox delivery, reconciliation, and atomic immutable artifact visibility.

Non-goals: Business analytics, forecast model semantics, remote object storage, GPU execution, and Kubernetes are outside this workstream.

## Ubiquitous language

| Term | Meaning | Not the same as |
|---|---|---|
| `Run` | Authoritative execution aggregate for one versioned specification. | A worker process |
| `Lease` | Time-bounded authority to execute a task. | Permanent ownership |
| `FencingToken` | Monotonic identity that rejects stale worker commits. | A retry counter |
| `ArtifactCommit` | Atomic transition from invisible staging to immutable manifest visibility. | A completed file write |

## Domain model

Run, NodeRun, TaskEnvelope, Lease, FencingToken, CancellationRequest, ProgressSnapshot, OutboxMessage, and ArtifactManifest; stale leases cannot commit and terminal state is monotonic.

Every write belongs to one context. Cross-context reads use public projections or query ports. Actor, workspace, trace, and contract-version context cross every protected boundary.

## Use cases and contracts

| Command/query/event | Actor/caller | Input/output owner | Errors, idempotency, and version |
|---|---|---|---|
| `SubmitRun / CancelRun` | Authorized product use case | Versioned execution command | Idempotency identity; cancellation is monotonic |
| `ClaimTask / HeartbeatLease / CompleteTask` | Worker | Fenced task protocol | Lease expiry and stale-token rejection |
| `CommitArtifact` | Executable context | Immutable artifact manifest | Hash-verified atomic visibility |

Public schemas are versioned before external reliance. Unknown state is explicit; it is never mapped to success or empty data.

## Data ownership

Execution and artifact owners have separate PostgreSQL tables and repositories; artifact bytes remain on the local filesystem through v1_target with manifest, hash, lineage, retention, and authorization metadata.

Migration, compatibility, retention, lineage, redaction, and rollback are defined before persistence becomes authoritative. No context reads or mutates another context's private tables.

## Ports and adapters

| Port owner | Adapter | Auth/trust | Timeout/retry/unknown state | Degradation |
|---|---|---|---|---|
| Execution application | PostgreSQL run/outbox repositories | Actor and workspace authorized | Transactional outbox and bounded retry | Authoritative failed/degraded state |
| Execution application | CPU worker adapters | Versioned task envelope | Lease, heartbeat, fencing, cancellation | Reconcile unknown completion |
| Artifact application | Local filesystem adapter | Authorized workspace reference | Stage, fsync/hash, atomic manifest commit | Staging remains invisible |

## UI and documentation

Run status, progress bar, ETA, cancellation, retry, operator detail, freshness/loading near the changing block, and no misleading continuous animation.

The Web contract includes loading, empty, degraded, forbidden, failed, refresh, unsaved-change, and return-to-origin behavior. Shipped `/docs` and `/help` content follows visibility and localization policy. Penpot mutation requires separately confirmed live authority.

## Operations

Queue depth, lease age, stale fencing attempts, reconciliation lag, cancellation latency, CPU-core allocation, artifact commit failures, and redacted trace correlation.

All logs, traces, notifications, and evidence redact secrets and raw PII. Capacity assumptions remain single-server and CPU-only through `v1_target` unless an ADR changes the topology.

## Fixtures and acceptance

Deterministic runs for queued/running/succeeded/failed/cancelling/cancelled states, expired leases, duplicate dispatch, stale fencing, partial artifacts, and recovery.

Acceptance follows S00–S06 and requires unit/property, contract, real adapter, browser, runtime, recovery, security, or performance evidence only where the changed boundary triggers it.

## Contract impact

This initial definition is a `compatible-change` to repository planning artifacts and an `unknown` future product contract until S01 freezes schemas. It changes no running API, persistence, browser behavior, or external side effect.

## Open decisions and blockers

No queue product or remote worker topology is assumed. Adapter selection remains behind owned ports.

Principal risks: Duplicate execution, stale commit, split-brain run state, cancellation races, false ETA, artifact partial visibility, and CPU oversubscription.
