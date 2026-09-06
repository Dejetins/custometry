---
doc_id: CONTRACT-REPORT-REFRESH-SERVING-RECOVERY-001
title: Report refresh, prepared serving and recovery contract
doc_version: 1
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [REPORT-REFRESH-001, REPORT-REFRESH-002, REPORT-REFRESH-003, REPORT-REFRESH-004, REPORT-REFRESH-005, REPORT-REFRESH-006, REPORT-REFRESH-007, ARTIFACT-COMMIT-001, ARTIFACT-COMMIT-002, ARTIFACT-COMMIT-003, REPORT-PERF-001, REPORT-PERF-002, OPS-009, OPS-010, TEST-INV-123, TEST-INV-124, TEST-INV-125, TEST-INV-126, V1-AC-068, V1-AC-069, V1-AC-070]
status: accepted
acceptance_basis: owner-approved-report-refresh-load-and-backup-requirements-2026-09-06
proof_boundary:
  label: accepted-target-requirements-and-architecture-allocation
  exclusions: [implemented-api-schema, persistence-migration, runtime-proof, browser-proof, performance-proof, recovery-proof, release-authority]
---

# Report refresh, prepared serving and recovery

## Authority and decision scope

On 2026-09-06 the owner accepted automatic preparation of working reports,
explicit adoption of updates by an active reader, coalescing incoming updates,
and retention of the v1 single-server topology. The owner additionally required
a refresh period setting and visible status for every analytical document,
near-instant prepared-report opening, a workload of 1–50 concurrent authors and
1–100 concurrent viewers, and administrator-configurable daily-evening backups
with an off-primary-server destination capability.

The [machine blueprint](../../custometry-technical-blueprint-ru.md) is normative;
the [human mirror](../../custometry-technical-blueprint-human-ru.md) explains the
same IDs and the [UI blueprint](../../custometry-ui-blueprint-ru.md) defines the
derived interaction. This contract allocates those requirements within the
[system design](../architecture/system-design.md) and existing
[bounded contexts](../architecture/bounded-context-map.md). It is registered in
the [contract index](README.md) and [architecture index](../architecture/README.md).

This amendment extends the current 0.10.0-draft requirements in place, with this
versioned contract as its dated acceptance record. It selects no new database,
storage vendor, third authoritative store or independent scheduling engine.
Parquet remains durable analytical storage, PostgreSQL control truth and
Valkey/process memory bounded ephemeral cache. An off-host backup target is not
a live remote artifact adapter. Forecast-specific development remains on hold.

## Logical model and storage ownership

| Object | Owner and storage | Meaning |
|---|---|---|
| Stable analytical document | Presentation; PostgreSQL | Identity, permissions and current successfully published snapshot reference |
| Definition version | Presentation; PostgreSQL | Shared AnalyticalDocumentVersion hierarchy, formulas, bindings and presentation; ReportDefinitionVersion is its report lifecycle projection |
| Refresh policy revision | Presentation intent, scheduled through Execution Control public contracts; PostgreSQL | Trigger, period/cron/timezone, selected definition, input binding policy and lifecycle |
| Prepared materialization/result | Analytics or other producing context; immutable Artifact Lifecycle storage | Typed computed values, aggregate state and chart data; reusable across compatible consumers |
| Root/page snapshot | Presentation metadata in PostgreSQL plus immutable artifact manifests | Exact definition, input/result versions, resolved block bindings and complete publication identity |
| Bounded API response | Presentation serving adapter | Authorized active-page data read from prepared results, optionally cached by snapshot/projection/policy identity |
| Export | Presentation via artifact ports | Immutable rendering of that exact snapshot, never a second hidden analytical calculation |

The artifact-format vocabulary remains owned by the
[artifact format contract](artifact-format-contract.md). This amendment does not
pick a new scalar-result encoding or place every small result in a separate
Parquet file. Formatting, authorization, serialization and bounded projection
still cost work; prepared viewing does not imply zero CPU or disk IO.

Example: a report backed by millions of purchases can reuse a daily/store
materialization and serve a month chart from a small prepared series. Daily
distinct-customer counts cannot simply be summed for a monthly distinct count;
aggregate selection must preserve exact metric semantics. Exact pins stay
pinned. Refreshing a logical latest-by-fixed-definition binding resolves a new
exact input set for a new snapshot; it never edits the previous snapshot.

## Refresh and serving lifecycle

1. An authorized author configures the common policy surface on any supported
   dashboard, workbook-report or research document. New published working
   reports/dashboards default to after-ingestion; research and pinned
   publications remain manual/pinned unless deliberately configured otherwise.
   Draft or unsupported bindings expose preflight blockers.
2. Presentation submits scheduling intent through Execution Control.
   Existing PostgreSQL schedules, timezone/misfire handling, outbox and workers
   execute it; there is no report-specific independent cron daemon.
3. Ingestion announces a successfully published compatible generation through
   its public contract. Transport arrival alone is not readiness.
4. After-ingestion mode requests preparation immediately after readiness.
   Scheduled mode waits until due; if no eligible fresh input exists at due,
   one durable overdue demand waits for readiness. Later arrivals re-evaluate
   it. Unchanged inputs produce an evaluated/no-change outcome, not a fake
   update timestamp. Resolved rolling/as-of periods may themselves change
   computation identity even when input bytes do not.
5. Execution coalesces pending demand to the latest compatible input set and
   uses the existing reuse-key single-flight for equivalent work. Independent
   sources use a declared consistent version set, not an invented shared
   timestamp. Revisions, pauses and access changes are rechecked at admission
   and publication. Continuous arrivals must allow useful runs to finish;
   bounded freshness and fairness settings govern catch-up rather than
   repeatedly cancelling the only active run.
6. Data workers prepare only affected, semantically necessary results.
   Report workers invoke the shared composition kernel. Required blocks and
   any declared partial policy are validated before root publication.
7. Presentation atomically commits the complete snapshot/current reference
   within its own PostgreSQL transaction after committed artifact evidence.
   Current-reference compare-and-set includes policy/definition revision and
   a monotonically ordered publication generation derived from the resolved
   input set. Completion order and wall clock are not sufficient.
8. The active viewer stays pinned, sees progress/freshness and an available
   update, and explicitly applies it. Compatible page/filter/scroll context is
   retained; incompatible context is explained. Ordinary new opens resolve
   current, while exact snapshot links preserve history.
9. Failure keeps the previous valid snapshot only under current authorization
   and the declared last-good policy. Permission revocation blocks access.
   Exports/comments/annotations remain tied to their original snapshots.

The after-ingestion event and due occurrence initiate report preparation only.
They do not authorize automatic email delivery, definition changes, moving
fixed input pins, rewriting analyst findings or unbounded speculative compute.

## Artifact commit and recovery

Artifact Lifecycle owns validation and publication; PostgreSQL is the sole
publication authority. The worker writes into staging, validates schema/hash
and required quality checks, then ensures durable immutable placement before
the manifest becomes published. Filesystem-specific flush/sync and directory
durability must be demonstrated on supported targets; rename alone is not
power-loss evidence.

A crash before PostgreSQL publication may leave unreferenced staged or placed
files. Through owner ports, the Reconciler checks commit outcome, idempotency,
current lease/fencing, references and retention before resuming a valid
transition or reclaiming files. Unknown commit outcomes are read back before
retry. Cleanup must protect in-flight writes, published dependencies and files
pinned by an in-progress backup.

Execution owns run transitions; Artifact Lifecycle owns file visibility;
Presentation owns the current report reference. Cross-context recovery uses
public contracts and idempotent handoffs, not one application transaction
writing private tables across all three contexts. A committed artifact whose
report publication failed may be reused on retry; it is not automatically the
current report.

Loss or proven corruption after publication blocks affected reads and invokes
authorized restore/recompute with identity verification. Hash mismatch,
temporary storage unavailability and a failed refresh are distinct facts.
An older snapshot may be offered only when policy and authorization permit.

## UI state and recovery actions

State is derived from server-authoritative evidence, with separate dimensions:

| Dimension | Examples | Constraint |
|---|---|---|
| Result availability/integrity | ready, unavailable, confirmed corruption, unknown | Corruption requires evidence; outage or refresh failure alone is insufficient |
| Freshness | as-of, current/stale, available newer snapshot | Ready does not mean fresh; access checks still apply |
| Refresh activity | scheduled, waiting for data, queued, running, failed, blocked | A failed attempt can coexist with a valid last-good result |
| Publication event | updated at, new version available | Successful publication time is distinct from source coverage and last evaluation |

The document header/list and refresh settings share the same state projection.
Readers receive safe reasons and allowed actions; authors can configure or
retry within their permissions; operator recovery stays in existing operations
surfaces. Localized copy must not expose physical paths or denied metadata.
The UI blueprint owns concrete RU labels and the EN/RU implementation contract.

## Performance and operational envelope

The declared target is near-instant usable opening of a prepared report.
Acceptance must separately measure cold-after-restart, warm and hot serving,
active-page usability, page/filter latency and ingestion-to-publication lag.
Use p50/p95/p99, throughput, CPU/memory/IO, bytes scanned/transferred, duplicate
compute, saturation and refresh backlog. The full profile combines up to
50 active authors with 100 viewers and background refresh; it does not allocate
one unrestricted all-core worker per author.

Existing interactive/precompute/maintenance lanes and common thread budgets
apply to Arrow, Polars, DuckDB and other engines. Ready serving reads bounded
prepared data; an uncached filter or drill-through can require new computation
with preflight. Do not assume every possible filter can be precomputed.
The owner's reported PyArrow speedup is motivation, not platform benchmark
evidence.

The administrator configures a daily-evening backup policy with explicit time,
IANA timezone, destination and retention. Setup must disclose an unconfigured
destination or schedule rather than report protection. A backup pins the
artifact reference closure corresponding to the PostgreSQL recovery point,
and safely includes required key recovery and deployment metadata. Off-primary
copy success and a verified restore are distinct evidence. The same primary
disk, a cache copy or an enabled schedule is not off-primary backup proof.

## Compatibility and rollout

| Surface | Before to after | Classification and consequence |
|---|---|---|
| Exact historical snapshots, pinned links and exports | Remain immutable and use exact IDs | compatible-change at the target contract: new refresh creates new snapshots |
| New working-document default | Optional/policy-selected precompute to default automatic preparation | breaking-change to previous default expectations; initialize explicitly for new objects and migrate existing objects through visible policy selection, never silently enable all old reports |
| Scheduling and backup settings | Existing general facilities to per-document refresh and configured off-primary backup policy | unknown for concrete API/schema/mixed-version consumers until implementation contracts are selected; version DTOs, validate old data and define rollback before rollout |
| Current snapshot publication and cache | Explicit revision/generation checks and pinned response identity | unknown for existing serialized identities and migrations; preserve historical IDs and invalidate only incompatible serving entries |
| UI status and open viewer | Distinct result/attempt states and explicit snapshot adoption | compatible-change with existing immutable history; consumers of future status enums need exhaustive handling and contract tests |
| Active storage/runtime topology | Same local persistent volume and single server | none; external backup is operational capability, not distributed live storage |

This is a documentation unit, not a migration. Before implementation, bind
the existing schedule representation to typed document targets without
silently repurposing pipeline_version_id; specify reader/writer compatibility,
persistent policy backfill, queued work across upgrades and reversible disable.
Use existing approved implementation routes; this contract creates no ticket,
plan, prompt pack, ledger state or runtime readiness claim.

## Proof allocation and unresolved parameters

| Requirement group | Required observation |
|---|---|
| REPORT-REFRESH-001 through REPORT-REFRESH-007 | TEST-INV-123/124; V1-AC-068: due/data order, unchanged input, DST/misfire, revisions, burst/coalescing, out-of-order completion, continuous progress, exact history and real viewer behavior |
| ARTIFACT-COMMIT-001 through ARTIFACT-COMMIT-003 | TEST-INV-125; V1-AC-070: fault injection at every file/metadata/current boundary, fencing, unknown commit, concurrent cleanup and state distinctions |
| REPORT-PERF-001/002 | TEST-INV-126; V1-AC-069: controlled mixed-load baseline and agreed budgets, not a microbenchmark or static validator |
| OPS-009/010 | TEST-INV-126; V1-AC-070: scheduled off-primary coherent backup and restore with key recovery and exact report reproduction |

Before performance acceptance, the owner and measured workload must establish
reference hardware, data volume/distribution, representative document size,
numeric latency/freshness budgets and supported sustained arrival rate. The
user counts are agreed; these remaining values are not. Backup clock time,
destination and retention are installation settings. No numeric RPO/RTO was
accepted; disclose actual last recoverable point and observed restore duration.
These gaps do not block recording the requirements, but block stronger
performance/recovery claims where the corresponding evidence is required.

## Documentation verification — 2026-09-06

The documentation-only amendment adds 14 functional/operational requirements,
four test invariants and three v1 acceptance criteria. Machine/human ID parity,
derived UI behavior, architecture references and generated indexes were
synchronized in this unit. The existing planning and execution state is not
changed; future implementation consumes these requirement IDs through its
selected authorized unit.

After activating scripts/activate-toolchain.sh, the locked requirement-index
and documentation-index generators passed. The command
uv run --locked python -m tools.check --scope local passed, and git diff --check
reported no whitespace errors. This is local documentation/static evidence;
no runtime, browser, load, power-loss or backup/restore drill was executed.
