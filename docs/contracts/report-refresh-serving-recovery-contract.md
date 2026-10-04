---
doc_id: CONTRACT-REPORT-REFRESH-SERVING-RECOVERY-001
title: Report refresh, prepared serving and recovery contract
doc_version: 5
product_spec_version: 0.11.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [REPORT-REFRESH-001, REPORT-REFRESH-002, REPORT-REFRESH-003, REPORT-REFRESH-004, REPORT-REFRESH-005, REPORT-REFRESH-006, REPORT-REFRESH-007, ARTIFACT-COMMIT-001, ARTIFACT-COMMIT-002, ARTIFACT-COMMIT-003, REPORT-PERF-001, REPORT-PERF-002, OPS-009, OPS-010, TEST-INV-123, TEST-INV-124, TEST-INV-125, TEST-INV-126, V1-AC-068, V1-AC-069, V1-AC-070, REPORT-018, METRIC-032, METRIC-034]
status: accepted
acceptance_basis: owner-approved-refresh-2026-09-06-and-creator-only-amendment-2026-09-20
proof_boundary:
  label: accepted-target-with-bounded-ms004-api-transaction-evidence
  exclusions: [complete-refresh-runtime, browser-proof, performance-proof, production-recovery, release-authority]
---

# Report refresh, prepared serving and recovery

The 2026-09-20 owner amendment, REPORT-018, narrows report-definition and
report-refresh-policy editing to the report creator with the required permissions.
Administrative access management and execution of an already authorized refresh
policy remain separate operations. Goal occurrence creation and manual goal
actual recomputation follow METRIC-032/034; recurring goals do not implicitly
select scheduled report refresh. See the
[authoring amendment](analytical-authoring-contract.md#owner-selected-behavior-2026-09-20).

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


## MS-004 S01 additive schema and recovery boundary

Migration `0012_metric_workspace` follows `0011_presentation_drafts`. It backfills
immutable `presentation_documents.creator_principal_id` from the existing owner,
adds explicit report/result discriminators, same-workspace/report Saved View
foreign keys and Semantic-owned calendar versions/default pointers. Old v1
inserts retain their compatibility path through the creator initialization
trigger. Owner changes cannot rewrite creator attribution. No historical JSON
payload or artifact is rewritten. See the
[implemented authoring foundation](analytical-authoring-contract.md#ms-004-s01-implemented-foundation)
and [S01 proof](../../.codex/delivery/evidence/MS-004/MS-004-S01/report.md).

The supported local downgrade to 0011 succeeds only before any configured-report
v2, metric-workspace v2, Saved View or custom-calendar record exists. After any
such write, it fails with
`METRIC_WORKSPACE_FORWARD_REPAIR_OR_PREUPGRADE_BACKUP_REQUIRED`; retain a dual
reader and forward-repair. A separately authorized coherent PostgreSQL/artifact
restore would lose changes after the backup and is not normal edit undo.
System-only January initialization is reversible. Calendar versions reject
UPDATE/DELETE; the default and previous-version FKs enforce workspace identity.

Local reproducible proof uses `tests/integration/semantic/run_s01.py --image
<available-postgresql-image-id>` through the locked API Python environment.
It owns one loopback-only disposable container, generates a private temporary
password file, creates fresh databases, migrates from 0011, runs actual
PostgreSQL/Identity/API tests and removes its container/volumes and secrets.
It never connects to a shared development database. Run after the repository's
locked dependency/toolchain setup. A plain test-suite run without this fixture
skips the real boundary; it cannot substitute for the owned non-skipped run.

These checks prove bounded local migration/API behavior, not backup restoration,
installation, production deployment or the broader scheduled-refresh contract.


## MS-004 S02 immutable calculation recovery boundary

The [S02 calculation contract](analytical-authoring-contract.md#ms-004-s02-calculation-and-immutable-result-boundary)
uses existing `analytics_sales_reports` uniqueness with the explicit
`metric-workspace/v2` discriminator. The admitted JSON artifact is durable before
the result row. Concurrent equal requests may duplicate CPU work but converge on
one result ID, exact bytes and manifest; disagreement fails instead of overwriting.
The existing S01 downgrade refusal therefore also applies to these actual v2 rows.

Exact reads and reuse verify immutable output bytes and admitted source bindings;
missing, corrupt or mismatched content produces an explicit failure. There is no
compute-on-GET, fallback to a stale result, implicit new calendar adoption or
in-place repair. Comparison artifacts retain dependencies on their result artifacts.
Temporary staging files are cleaned by their producer; orphan final files after a
failed database transaction do not become admitted results. Existing lifecycle
policy owns retention; this stage introduces no cleanup worker.

`tests/integration/analytics/run_s02.py --image <available-postgresql-image-id>`
provisions a loopback-only disposable PostgreSQL container with separate fresh
control/source databases and a private temporary secret. It seeds real PostgreSQL
retail tables, runs production readonly intake and independent readonly source SQL,
then deletes only its own container, volumes and secret. The optional
`MS004_S02_EVIDENCE_PATH` records redacted synthetic corpus IDs/hashes/counts, never
rows or credentials. A plain test run that skips prerequisites is not proof.

These checks cover local input/output corruption, missing output, registry and
context identities, concurrent result admission and policy recheck seams. S03
still owns real Identity object/data authorization, full report-save transactions
and their fault-injection proof. No production restore, deployment or release is
claimed by calculation tests.


## MS-004 S03 atomic report and view recovery

Configured report Save verifies every result, comparison and chart dependency,
then admits immutable page/root artifacts before one control-PostgreSQL transaction
writes the report revision and deterministic companion Saved View revision. Both
CAS values must match. Final access rechecks precede the latest-pointer switch;
failed artifact admission, current-access denial, stale companion revision or
injected database failure preserves the previous complete report/view pointers.
Historical replay returns its original version, not the current latest version.
Unreferenced admitted artifacts can remain after a failed Save; existing retention
owns their lifecycle, with no new cleanup worker or automatic recomputation.

Exact reads verify result/comparison and page/root bytes plus current data access.
The safe v2 envelope distinguishes `ARTIFACT_MISSING` / `ARTIFACT_CORRUPT` (409),
`ACCESS_CONTEXT_CHANGED` and CAS/idempotency conflicts (409), denied access (403),
private/unknown locators (404), bounds (413), malformed DTOs (422), and retryable
storage failures (503). A former allowed policy version cannot silently reuse old
Apply bindings. No partial success, implicit calendar adoption or stale fallback
is returned as a successful Save. Existing v1 HTTP writes also recheck current
authorization and verified data before commit and on replay.

`tests/integration/presentation/run_s03.py --image <available-postgresql-image-id>`
creates only task-owned loopback PostgreSQL source/control databases and temporary
secrets, performs real intake and API tests, then removes its own container/volumes.
A second fresh control database starts at 0011 for the existing migration/legacy
suite; its historical v1 row uses the actual old column shape before the current
adapter is restored after migration. `MS004_S03_EVIDENCE_PATH` optionally records
synthetic IDs, admitted lineage/manifest hashes and HTTP outcome counts, never
credentials or provider rows. See [S03 evidence](../../.codex/delivery/evidence/MS-004/MS-004-S03/report.md).
These checks use actual Identity sessions, ASGI HTTP handlers, transactions and
artifact bytes; they do not establish browser, production restore or deployment.
