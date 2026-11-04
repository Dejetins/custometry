---
doc_id: CONTRACT-REPORT-REFRESH-SERVING-RECOVERY-001
title: Report refresh, prepared serving and recovery contract
doc_version: 7
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


## MS-004 S05 Saved View comparison integrity

Personal-view comparison projections are immutable dependencies of new view
versions. Current reads verify both their selected result bindings and their
manifest bytes. Missing or corrupt comparison artifacts fail closed; GET does
not recalculate, repair or silently drop them. Existing view payloads without
the optional projection retain their original serialization. A later explicit
Save can admit a comparison from already verified results, under current access,
without running the source query or editing the report definition.

Old strict view readers cannot consume new projection-bearing payloads; keep
updated readers and use forward repair after these writes. No migration rewrites
historical views or snapshots. [S05 evidence](../../.codex/delivery/evidence/MS-004/MS-004-S05/report.md)
records the real API/database integrity, fresh-application reopening and browser
checks. Production recovery, installation and deployment remain outside this proof.

S05 browser completion checks capture the selected-context generation at Apply
dispatch and reject obsolete success/error publication after reload, edits or own
view selection. Reload responses also check generation. Auth-generation checks
remain independent and are exercised while an exact production result body is
held by the task-owned transport fixture; releasing it after logout must not
restore protected state.

## W39 local serving and identity lifecycle

The owner-selected [W39 ticket](../../.codex/delivery/tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md)
adds bounded prepared serving and session lifecycle work. Its
[evidence](../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/execution-notes.md)
separates inherited S05 inputs, source checks and still-pending runtime acceptance.

The report editor response adds optional actor metadata (workspace, principal,
permissions) alongside the existing authorized report/capabilities. New browser
code uses it to avoid an earlier `/identity/me` waterfall. Install the new API
and migration before the new browser: old clients can ignore the additive field;
the new client requires the authorization event channel. Rolling back browser/API
leaves existing result identities intact; retaining schema 0013 is safe for old
writers. Downgrade removes the event trigger and maintenance metadata, never
restores already expired/deleted sessions or security events.

Prepared reads verify current authorization, publication identity, saved query,
calendar/metric pins and immutable output hashes. They read the bounded Store
identity projection used for scope normalization; they do not reread Receipt,
ReceiptItem or quarantine/raw history merely to show an already admitted result.
Compute/Apply retain full input validation. There is no cross-request server result cache. Each GET also bounds immutable
repository memoization to one shared 64-entry / 16-MiB budget across the
Presentation, Analytics, Semantic, Calendar and artifact-metadata adapters; parsed prepared results have a
separate 32-entry / 16 MiB request lifetime budget. These are not per-user caches.
Identity projection rows may be reused inside that GET at one effective time,
with at most 128 statement keys, 2,048 rows per admitted statement and 1 MiB
of accounted row payload. Evaluators receive independent row copies. A new
request constructs a new projection and reads current committed access state.
Request-scoped authentication/access reuse ends with the HTTP read; mutations
retain their transaction-boundary checks and do not use this projection. API connections share a bounded pool
(default maximum 8 per worker, 64 waiters, 5-second queue timeout); this is not
permission/result reuse. Total deployment connection budgets multiply by the
explicit worker count and must be recorded in performance evidence.
`CUSTOMETRY_API_SYNC_THREAD_LIMIT` (1–40) and
`CUSTOMETRY_API_GC_ALLOCATION_THRESHOLD` (700–1,000,000) are optional internal
process settings; unset values preserve the Python/AnyIO defaults. They neither
disable GC nor create a result cache, and their prior values are restored at
application shutdown. Use a single application lifespan per serving process.
Any selected worker/thread/GC profile requires matched latency and RSS evidence;
it is not automatically qualified for unrelated API workloads.
Report GET adapters use statement autocommit on a checked-out connection to avoid
an implicit transaction around every short read. This keeps read-committed
statement visibility; explicit transactions remain atomic, including initial
calendar provisioning. The connection returns to its prior mode before pool
reuse. Mutation adapters retain their ordinary transaction mode. Resolving a
saved-view head may reuse the same request's validated immutable version, while
the current head pointer is still read from PostgreSQL.

The editor composer reuses its already validated report model and encodes the
validated response directly. Pooled JSONB decoding uses the existing Pydantic
parser without a cross-request string cache. These representation optimizations
do not remove saved binding, artifact hash or current authorization checks.
The editor response negotiates gzip for payloads of at least 4 KiB when it
reduces transfer size. Responses remain `Cache-Control: no-store` and vary by
`Accept-Encoding`; all payload limits apply to decoded bytes.

The editor response may carry `ready_results` already verified while reading the
saved document. It contains only the default active workset, deduplicated, with
at most 32 results and 2 MiB combined result payload. If the whole active set
does not fit, the list is empty and the existing bounded result-read path applies.
The browser verifies every embedded result against its saved binding and uses
those same objects in the editor query; it does not store a second query copy.
Changing to an unrepresented workset releases the embedded data before retaining
the newly fetched working set. Older responses without this additive field use
the existing result endpoint. Old strict external decoders are not proven by
the local Web compatibility tests.

The browser admits at most 16 MiB of accounted query payload and 32 query entries
per tab, with inactive entries removed immediately. Immutable response objects
reuse their measured decoded wire size for accounting; locally composed objects
are encoded for accounting. Active result reads have
four concurrent requests, at most 32 distinct results, 2 MiB per response and
16 MiB combined. Oversized payloads produce a local error without cache admission.
No result data goes into localStorage, IndexedDB, service workers or another disk
cache. Payload accounting is not a JavaScript heap/RSS limit; decoded/rendered
working sets and in-flight buffers are measured separately. Navigation cancels
owned reads; session/channel generation changes reject late decoded responses.

`GET /identity/events` provides same-origin credentialed SSE hints, delivered by
transactional PostgreSQL NOTIFY. Each API worker has one listener and at most 256
subscribers with one pending hint each. Events contain no resource or principal
payload. Access/organization/session-revoke changes invalidate protected state;
notifications are not authorization. Listener loss, network loss, expiry and
reconnect hide protected content until fresh report authorization completes.
Keepalives perform no database activity write. At most ten minutes (or sooner at
access expiry), the channel requests token renewal; browser Web Locks serialize
rotation across tabs sharing cookies. Reconnect uses bounded exponential backoff.
Missed events need no replay log because reconnect always reconciles current state.
One unsaved definition can survive channel reconciliation in memory, bound to
its principal and report. It remains hidden until fresh authorized metadata
arrives for that principal. Login, logout and denied access discard it; snapshot
views do not restore editing drafts. This does not retain result payloads.

Session fields serve authentication (hashed access/refresh/CSRF tokens and expiry),
refresh-family replay defense, and existing own/admin list-and-revoke device
recognition (device label, creation time and approximate `last_seen_at`). The latter
is not an expiry clock or an attendance record. Only foreground interaction-marked
protected work may advance it, with an atomic five-minute coalescing predicate.
Passive queries, keepalives and refresh never advance it. No heartbeat audit rows
are created. Existing API-token `last_used_at` belongs to the separate API-token
inventory/revoke process and is not browser session activity.

Migration 0013 adds cleanup indexes, a single operational maintenance-state row,
and transactional notification triggers. Existing API process lifecycle schedules
Identity-owned maintenance once daily, using a database advisory lock and durable
last-completed time across workers. Default session retention is seven days after
absolute expiry (configuration `identity_session_retention_days`, minimum seven).
Refresh history remains through the whole usable family lifetime and retention
window, including early revocation. Cleanup deletes eligible history, then empty
expired sessions in bounded batches. Default security-event retention is 90 days
(`identity_security_event_retention_days`), restricted to `session.*` and
`password.*` in the Identity event category; unrelated audit categories are retained.
Those transitions support session/access incident investigation and device-revoke
processes. Privileged maintenance is the only deletion path; normal application
audit writes remain append-only. Existing audit metadata is not rewritten.

Maintenance bounds each category to 500 rows per batch, 32 batches per invocation,
with a two-second work budget and bounded statements/locks; interrupted transactions
roll back and are restart-safe. Errors are observable using a fixed redacted log
message. The single state row records completion and deletion counters for operating
the retention job, not user activity. Logical expiry, logical deletion and backup
retention are distinct: database pages, WAL and independently retained backups can
outlive logical deletion. This policy promises neither immediate physical shrink
nor routine `VACUUM FULL`.

Contract impact: additive editor DTO and SSE API are compatible for old clients on
the new server; new-client/old-server rollout is unsupported and requires API-first
ordering. Activity semantics and retention are compatible owner-selected lifecycle
changes for the named session/investigation consumers; immutable result identity,
Apply/Save atomicity and analytical arithmetic are unchanged. No runtime or
performance acceptance follows from this description alone.

### W39 local qualification profile

The local saved-open profile uses production Web assets and Chromium
136.0.7103.25 headless shell on the reference 18-core / 36-GiB host. Fifty
isolated contexts represent fifty distinct authenticated users. The task-owned
API container has eight processes, two synchronous threads per process, a
1,000,000-allocation GC threshold, an aggregate 8-CPU / 4-GiB container limit
and default eight-connection pools (64 maximum across processes). The real
PostgreSQL container has 4 CPUs / 2 GiB. The existing local reverse-proxy test
seam distributes ordinary requests by least outstanding work; event channels
are distributed independently. These exact settings are part of the evidence,
not an unqualified performance claim for a single shared-listener API process.

The API image used for this profile is
`sha256:81b4f1eb405c43f53c88c0d79bfd00bd6d366973f6abcb09358ac9eb7f02625e`.
Application source is mounted read-only; its hashes and Web bundle hashes are
recorded in every benchmark result. Baseline and candidate use the same fixture
identities, resource limits, process/thread/GC settings and browser mechanic.
Cold batches restart the API and browser; OS filesystem caches are not flushed.
Heap/CDP observations occur only after all timed opens finish.

On the candidate's completed 200-open series per mode, graph p95 is 794.6 ms
warm and 1,495.9 ms cold, with zero failed opens. Warm frame acknowledgement
is 62.0 ms p95, dispatch 5.4 ms, and last completed response to stable graph
88.7 ms. Representative foreground two-toggle Event Timing has p75 48 ms;
simultaneous fifty-tab interaction stress is reported separately. These are
local observations, not production deployment or MS-004 acceptance. See the
[W39 observations](../../.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/execution-notes.md)
for the final comparison, resource checks, prior failures and source bindings.
