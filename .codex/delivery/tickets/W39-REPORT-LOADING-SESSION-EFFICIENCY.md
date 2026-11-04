---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.11.0-draft
ticket_id: W39-REPORT-LOADING-SESSION-EFFICIENCY
status: active
workstream_id: W39
summary: Open saved reports directly in the native report frame with fast bounded result reads and useful write-efficient session lifecycle management.
requirement_ids: [WEB-ARCH-002, WEB-ARCH-004, WEB-ARCH-006, WEB-PERF-001, WEB-PERF-002, WEB-PERF-003, WEB-PERF-004, WEB-PERF-005, WEB-PERF-006, ROUTE-003, AUTH-004, AUTH-005, AUTH-006, AUTH-009, SEC-010, A11Y-001, I18N-001, METRIC-025, COMPARE-013, CHART-021]
blockers: []
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/README.md
  - docs/adr/0007-responsive-web-frontend-platform.md
  - docs/architecture/bounded-context-map.md
  - docs/architecture/ui/target-pilot/README.md
  - docs/architecture/ui/custometry-web-implementation-source-contract-v1.md
  - docs/contracts/report-refresh-serving-recovery-contract.md
  - .codex/delivery/evidence/MS-004/MS-004-S05/correction-002/report.md
  - .codex/delivery/evidence/MS-004/MS-004-S05/correction-002/validation.md
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md
    - .codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY.md
    - .codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/**
    - apps/web/src/features/reports/**
    - apps/web/src/app/**
    - apps/web/tests/**
    - apps/api/src/custometry_api/**
    - apps/api/pyproject.toml
    - apps/worker_data/**
    - packages/identity_access/**
    - packages/presentation/**
    - packages/contracts/**
    - packages/localization/**
    - migrations/**
    - tests/unit/identity_access/**
    - tests/unit/presentation/**
    - tests/contract/**
    - tests/integration/identity_access/**
    - tests/integration/presentation/**
    - tests/e2e/report-loading/**
    - tests/performance/report-loading/**
    - tests/e2e/ms-004-workspace/**
    - docs/contracts/**
    - docs/architecture/README.md
    - docs/architecture/ui/custometry-web-implementation-source-contract-v1.md
    - docs-site/docs/en/**
    - docs-site/docs/ru/**
    - scripts/**
    - uv.lock
  forbidden_write_paths:
    - .codex/delivery/ledgers/**
    - .codex/agents/generated/**
    - .codex/delivery/evidence/MS-004/**
    - docs/architecture/planning/milestones/**
    - docs/architecture/ui/target-pilot/**
    - deploy/**
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: browser
  proof_skills: [browser-qa-evidence, backend-performance-evidence, backend-quality-gates, contract-impact-analysis]
  commands:
    - source scripts/activate-toolchain.sh && uv run --locked python -m tools.custometry_quality.validate_delivery_tickets
    - uv run --locked python -m tools.check --scope local
    - focused real PostgreSQL identity and presentation integration tests
    - focused Web tests and typecheck
    - real API browser report-loading and existing MS-004 regression journeys
    - reproducible before-after 50-user report-open and idle-resource benchmark
    - git diff --check
  proof_boundary: local-real-postgresql-api-browser-50-user-report-serving-and-session-retention
  evidence_target: .codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence:
  - .codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY.md
  - .codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/handoff.md
---

# Outcome

A user opening an existing report enters the accepted native report frame
immediately. Only the data regions load, with local progress and useful errors.
Saved results are read without recomputation. Fifty logged-in users do not cause
periodic activity writes or unbounded caches simply by leaving reports open.

## Authority and execution entry

The owner started implementation on 2026-09-23 through coordinator task
`01a0c02d-5267-7601-b735-5b43d11789c0`. Execution is owned by this isolated
checkout with one executor, no publication and no MS-004 journal mutation.

The owner accepted this optimization direction and performance acceptance in the
coordinator task on 2026-09-23, then required bounded memory/disk use, fewer disk
writes, activity records with concrete consumers, and a separate launch-ready
task. This is an independent ticket, not MS-004 S06 and not S05 acceptance.
Preparation is authorized now; implementation starts when the owner starts this
separate task. No further product decision or milestone publication is an entry
dependency. Numerical resource defaults below are delegated engineering choices.

Use an isolated local working copy of the current canonical source baseline:
base commit `86055ce732640ebe68fd5415a55f7bbde3499181`, plus the current uncommitted
S05 correction-002 source and this ticket. Preserve a hash manifest of inherited
files and separate inherited changes from W39 changes. The original checkout
`/Users/daniildegtyarev/Projects/Custometry` remains read-only. The canonical
`/Users/daniildegtyarev/.codex/worktrees/575c/Custometry` supplies the baseline but
W39 implementation does not edit it. Copied milestone journals/evidence remain
read-only historical inputs, never a second active journal.

The task can start using synthetic local fixtures and existing PostgreSQL,
API and Chromium tooling. It does not require production credentials, new
infrastructure, a settings screen, another milestone, or S05 owner acceptance.
Select task-owned ports and disposable databases; do not reuse or stop the
owner's running report demonstration. Normal in-scope tooling/dependency setup
is part of execution, not an owner prerequisite. Publication needs its own
scope reconciliation; readiness here means local implementation can start.

# Non-goals

- New report design, analytics formulas, implicit compute/refresh, company
  settings or financial-calendar setup/adoption inside reports.
- Analytics/adoption surveillance, attendance tracking, a new activity dashboard,
  per-request security audit, or retention of data with no named operational use.
- A second persistent result cache, offline report storage, speculative loading
  of every workset, a new service, production mutation, Git publication or deploy.
- Accepting, advancing or rewriting MS-004, its receipts or prior evidence.

# Work and repair boundary

## 1. Direct report entry and bounded critical path

Mount the existing native report frame before protected data resolves. Show
neutral reserved chart/card regions with local spinners and accessible status;
do not leak report titles, counts, prior data or object existence before current
authorization. Eliminate both standalone actor-loading and loading-report pages.
Keep layout, URL/history, keyboard, focus, RU/EN, responsive behavior and the
accepted pilot composition. Delay, failure, offline and retry stay inside the
report frame; controls are usable only when their actual prerequisites hold.

The report-open API supplies authorized metadata and capabilities together,
performing authentication in that request instead of a preceding `/identity/me`
waterfall. Fetch ready results for the active workset in bounded batches with
cancellation, concurrency and payload limits. Other worksets must not delay the
first useful graph. Repeated references share one read. Result/version/hash,
metric/calendar and saved-view identities remain unchanged. Ready open must
not enqueue compute, rescan source history or persist result copies.

## 2. Memory and disk budgets

Prefer existing immutable artifacts and normal filesystem reads. Reuse lookups
within one request and pool existing database connections with bounded size and
queue/timeouts. Do not equate more disk reads with better performance: measure
latency, IO and memory together before adding a cache.

Default cross-request server result-cache budget is **zero**. No new result
cache on disk or browser localStorage/IndexedDB/service-worker storage. Browser
reuse is limited to the active report working set: at most **16 MiB of accounted
cached payload and 32 entries per tab**, with inactive/old entries evicted first,
no duplicate query/data copies and no cache admission for oversized entries.
In-flight requests and decoded/rendered data also need bounded lifecycle and
release on navigation; 16 MiB is not a claim about total JavaScript heap/RSS.
Stream/page large results through the existing result contract where supported.

A nonzero server result cache is unnecessary for the default solution; any
later proposal must show comparative evidence and a total service budget rather
than multiplying an unbounded allowance per user/worker. Do not add it silently
just to pass a warm benchmark. Record browser heap and backend RSS separately,
including the active data/renderer working set and connection/event buffers.

## 3. Authentication, useful activity and events

Remove the report's ten-second actor poll. Real protected requests continue
checking current session, workspace, membership and resource authorization.
Request-scoped reuse must not become a stale cross-request permission cache.
Preserve refresh rotation/replay detection, expiry, CSRF, logout/revoke and the
client generation guard against late successful responses after denial.

Deliver logout, session revoke and relevant access changes as bounded server
notifications using existing application/infrastructure boundaries. Events are
invalidation hints; current server state remains authoritative. Cover multiple
workers/tabs, reconnect and missed events. A dropped authorization channel must
hide protected cached content until reconciliation; retry with bounded backoff,
not empty ten-second checks. Network keepalive is allowed without DB activity
writes or per-heartbeat audit. Reuse existing infrastructure; no new service is
an entry prerequisite. Healthy revoke-to-hidden target is p95 <= 1 second;
protected content is not restored after disconnect before fresh authorization.

Keep sessions for authentication, token-family replay defense and the existing
own/admin session-list-and-revoke process. `last_seen_at` is an approximate
last interactive use for recognizing devices in that process, not an expiry
clock or attendance log. Write at most once per session per **five minutes**
when actual foreground user action causes authenticated work; coalesce parallel
requests atomically. Passive open tabs, event keepalives, token refresh and
background refetch do not count as user activity. No rows/events are created
just to record a heartbeat. Document every retained field/event's consumer;
remove redundant activity collection with no operational consumer.

## 4. Lifecycle and bounded cleanup

Use configurable internal defaults: remove expired session rows and their
refresh history **seven days after absolute expiry**, with replay evidence kept
through the whole usable token-family lifetime. Revocation does not prematurely
remove hashes needed to detect replay. Cleanup runs once daily in bounded
restart-safe batches with a fixed work/time budget using an existing worker or
scheduled maintenance mechanism. No archive of identical expired session rows.

Keep real security transition events for investigations and session/access
incident diagnosis, default **90 days** for this identity event category, then
bounded policy-driven deletion. Do not purge unrelated audit categories or
weaken append-only application writes/tamper evidence. Failed cleanup is
observable without logging credentials/raw tokens. Expiry, deletion and any
necessary backups have explicitly distinct retention behavior. Document that
DB pages/WAL/backups can outlive logical deletion; do not promise immediate
physical shrink or run routine VACUUM FULL.

## 5. Implementation sequence and contract impact

First capture comparable baseline; then make report entry/result serving
bounded, remove redundant checks and pool connections, separate activity from
authentication, add event invalidation/recovery and retention, and run combined
proof. This is one independent execution unit with no artificial inter-ticket
blockers. Within the listed directories edit only these seams and required
contract generation/documentation; the wide globs are not feature authority.

Use public ports across Identity/Presentation; no private cross-context table
reads. Classify API, persistence, event, cache identity, browser and rollback
impact. Prefer additive API/schema changes and bounded backfills; preserve old
clients during rollout, explicit result identity and atomic Apply/Save. Update
affected contracts and documentation within the same unit. If retained S05
source changes invalidate its earlier evidence, record W39 proof and exact
before/after hashes without editing consumed S05 artifacts or claiming them
current. MS-004 acceptance remains separately owned.

# Acceptance evidence

All performance thresholds are targets, not measured facts at preparation.
Reference profile is this local 18-core / 36-GiB host, production Web assets,
real PostgreSQL/API and pinned Chromium, 1440x900 viewport and local network.
Record actual hardware/build/resource limits and client/API/render spans.
Use 50 distinct synthetic user sessions (one open tab each), three worksets of
six cards, all three existing metrics and two years of daily ready results;
only the active workset blocks useful paint. Add a maximum-supported workset
and oversized-result stress case for resource bounds. Hold baseline/candidate
fixtures, process count and configuration constant. Reuse task-owned fixtures
without altering the live demo. No mocks for the measured serving path.

- Warm internal navigation: neutral report frame acknowledgement <= 100 ms;
  interaction-to-dispatch and response-end-to-stable-paint p95 <= 100 ms each;
  representative INP p75 <= 200 ms without recurring blocking tasks.
- First useful saved graph: p95 <= **1 s warm**, <= **2 s cold** at 50 concurrent
  users. Report p50/p75/p95/p99, sample count and raw redacted timings; collect
  at least 200 opens per mode. Cold means fresh browser state and application
  restart/empty application caches; disclose OS filesystem-cache state rather
  than pretending it was flushed. Include repeated restart batches and full
  active-workset completion time so a fast first card cannot hide hanging peers.
- No standalone loading page in normal, deliberately delayed, empty, error,
  expired, unauthorized and reconnect cases. Existing authorized content may
  remain only while its permission state is trusted. Never display a cached
  title/result across workspace, principal or denied-session boundaries.
- A 30-minute, 50-user idle soak including token renewal has **zero activity
  UPDATEs/heartbeat audit inserts**; authentication rotation writes are counted
  separately and justified. An equivalent active scenario proves <= 12
  activity updates/session/hour (<= 600/hour for 50 sessions), with actual
  login, refresh, revoke, audit and cleanup writes separately attributed.
- Report DB row counts, relation/index bytes, WAL bytes, dead tuples, filesystem
  result bytes, cache payload/entries, browser heap and backend RSS before/after.
  Fifty sessions are not fifty new rows every ten seconds. Cache/result disk
  growth from idle report viewing is zero; DB/WAL growth is measured, not
  extrapolated from logical row size. Repeated navigation/reconnect stress must
  plateau after bounded eviction rather than retain every visited report.
- Real PostgreSQL tests cover concurrent activity coalescing, refresh replay,
  expiry/revoke, cleanup thresholds, batch limits and retry after interruption.
  Real API/browser tests cover access changes, event loss/reconnect/multi-worker,
  logout-all, in-flight late responses, rapid route switches, offline/retry,
  active/inactive worksets, RU/EN, keyboard and narrow viewport.
- All relevant existing MS-004 save/reopen/reader/calculation invariants remain
  green. Record exact commands, source hashes, contract impacts and evidence
  limits in the ticket's evidence target. Passing preparation checks does not
  establish performance, behavior, milestone acceptance or production delivery.

## Owner correction 001 — 2026-09-23

The owner authorized this bounded follow-up in the same local unit: remove all
visible/accessible EUR/UTC from report presentation; dock the inspector without
chrome overlap; use an SVG card gear; preserve geometry and authorized chart
content across card selection; fit chart height to viewport/Focus; and match
action controls to the 28 px / 16 px radius / 10 px period-control sample.
This supersedes the earlier single currency/timezone header decision, without
changing API units, timezones, calculations or persisted identity. The Web source
contract is now version 18. Single executor; no publication or canonical import.
The existing API/DB, owner tab and unsaved six-card draft, and owner ports
41744/58144 remain outside correction mutation scope. Production preview: 41746.

[Correction evidence](../evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-001/report.md)
appends current frontend proof and attributed coordinator Browser observations.
Earlier backend/idle measurements remain historical evidence for unchanged
backend scope; they are not rerun or represented as new frontend qualification.
Ticket status remains `active` for owner review.

## Owner correction 002 — 2026-09-23

The owner extended the same bounded local unit to (1) a persistent external report
header/toggle above report and inspector, (2) idempotent unfinished-workset Add
with visible configuration and distinct names for new sets/copies, and (3) a
content-height left navigation dock that displaces the workspace in configured
and legacy reports. Existing user sets/cards and unsaved tabs must be preserved.
No mass rename/deletion, agents, publication, import or MS-004 acceptance.

[Correction 002 evidence](../evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-002/README.md)
binds the three-item scope to Web source contract version 19 and targeted
geometry, keyboard, Add and synthetic persistence checks. Existing backend/idle
proof remains unchanged. Status remains `active` for owner review.

## Owner correction 003 — 2026-09-23

The owner authorized roomier/aligned report navigation, compact separate KPI
cards, signed semantic-color tooltip deltas, bounded normal-chart height with
padded line-axis data ranges, and per-card authoritative aggregate YoY. The normal
height cap supersedes correction 001's full remaining-space interpretation.
No client-generated aggregate changes, bucket-percent sums or shared selected-chart
comparison may substitute for each card's bound server result. Preserve unknown,
incomplete/zero-baseline/disabled/unapplied and denied states. Mindbox atlas images
01/05 support interaction context; crop01 is not evidence of a full YoY component.

[Correction 003 evidence](../evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-003/README.md)
records source contract version 20, read-only owner January data, separate synthetic
complete-context numeric proof, responsive/hover tests and unchanged backend inputs.
Single executor, current preview41746, user draft preserved, no publication/import
or MS-004 acceptance. Ticket remains `active` for owner review.

## Owner correction 004 — 2026-09-23

The owner authorized whole-unit monetary card presentation and at most one
fractional digit for percentages, removal of the metric-catalog frame, whole-card
selection with independent secondary controls and horizontal scrolling, separation
of configuration/results surfaces, and cached selection without automatic Apply
or false pending status. Preserve truthful unsaved and stale-query states; animate
existing charts for 180–240 ms and honor reduced motion. Full grouped numbers are
not scaled; raw/export precision remains authoritative.

[Correction 004 evidence](../evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-004/README.md)
binds source contract version 21 to bounded synthetic coordinate/keyboard/drag,
formatting, animation, explicit Save/reload and context-change checks. Single
executor; preserve owner report/tab/draft, API/DB and ports. No publication,
canonical import, MS-004 acceptance or backend/idle/performance campaign rerun.
Ticket remains `active` for owner review.

## Owner correction 005 — 2026-09-23

The owner explicitly requested direct coordinator implementation, without another
task. Four repairs: Focus fills the workspace; fixed-width KPI cards; comparison
controls on the report; non-overlapping expanded catalog. [Correction005 evidence](../evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-005/README.md)
binds source contract22 and focused Browser proof. Existing c67c checkout and41746
runtime retained. Original checkout, canonical MS-004 journal and user draft stay
untouched. Ticket remains active for owner review; no publication/import authority.

## Owner correction 006 — 2026-09-23

Owner accepted variant 2 and direct coordinator implementation: move editable
title, status and Apply/Save into the global header; use an overflow disclosure
for restore/snapshot; retain compact workset controls above the results.
[Correction 006 evidence](../evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-006/README.md)
records the bounded implementation and browser checks. Source contract v23 selects
this correction; unchanged calculation/persistence authority and MS-004 boundary
remain. No delegation, owner report save, publication or canonical import.

## Owner correction 007 — 2026-09-23

Direct bounded correction: result-local expand/collapse icons, current chart/table
representation in expanded mode, and meaningful horizontal workset ordering.
[Evidence](../evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-007/README.md)
is selected by source contract v24. No publication or MS-004 acceptance.

## Owner correction 008 — 2026-09-23

[Direct caption removal](../evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-008/README.md) follows the owner request; source contract v25. No persistence or acceptance changes.

## Owner correction 009 — 2026-09-23

[Title focus repair](../evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-009/README.md) follows the owner request under source contract v26. Context/day behavior is explained only.

## Owner correction 010 — 2026-09-23

[Context shortcut removal](../evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-010/README.md) follows the owner request under source contract v27. Local presentation only.
