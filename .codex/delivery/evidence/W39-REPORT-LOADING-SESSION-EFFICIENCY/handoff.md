# W39 implementation handoff

Ticket: [W39-REPORT-LOADING-SESSION-EFFICIENCY](../../tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md).
This is a local implementation checkpoint, not owner acceptance, MS-004 stage
completion, publication, import into the canonical checkout, or runtime release
qualification. The ticket remains active. Inherited source and evidence are
separated by [the inherited manifest](inherited-baseline.json); the canonical
MS-004 journal and owner demonstration were not changed.

## Implemented behavior

Saved reports enter the native frame with neutral local loading regions before
protected data resolves. Current authorization gates titles, cards, plots and
controls. Active-workset results are verified and optionally embedded in the
editor response; bounded fallback reads preserve existing immutable result
identity. Opening a report does not enqueue computation. Request-local reuse,
short reads, connection pooling and negotiated gzip reduce redundant work.

Browser payload reuse is bounded to 16 MiB / 32 entries; inactive queries are
released. The budget measures accounted payload, not total JavaScript heap.
Server result cache remains zero. Repository request reuse shares a 64-entry /
16-MiB budget; prepared-model parsing has a separate 32-entry / 16-MiB request
budget. Artifact verification still checks files and hashes. No browser or
server persistent result cache was introduced.

Transactional notifications invalidate access across workers and tabs. Lost
event connections hide protected content until fresh authorization succeeds.
An unsaved definition survives temporary reconciliation only within its same
principal/report identity; denial and logout clear it. Real foreground activity
is atomically coalesced to one write per five minutes. Passive reads, keepalives
and token renewal do not update activity. Daily bounded cleanup retains token
family evidence through absolute expiry plus seven days and security audit
events for 90 days; physical pages, WAL and backups have separate lifetimes.

The renderer avoids hidden legacy chart initialization, redundant first resize,
and idle SVG frames. Card progress marks remain static while the plot indicator
rotates. The workspace header's scoped blur removal changed at most two RGB
levels in [the captured comparison](chrome-surface-comparison.json).

## Selected local performance profile

18-core Apple M5 Max / 36-GiB host; Docker VM 18 CPUs / 8,317,267,968 bytes;
production Web assets; Chromium 136.0.7103.25 headless shell, one browser with
50 isolated contexts at 1440×900. Eight API processes share an 8-CPU / 4-GiB
container; PostgreSQL has 4 CPUs / 2 GiB. The owned proxy dispatches RPCs to the
least-outstanding worker and distributes SSE independently. Optional application
settings select two synchronous threads per process and GC threshold 1,000,000;
unset settings preserve runtime defaults. This profile is explicit, not a claim
about every deployment or browser renderer.

All 50 baseline/candidate saved documents match canonical JSON hashes in
[fixture equality](fixture-equality.json): three worksets of six cards, all three
metrics, daily 2025 results and 2024 temporal comparison. Existing 366-day
single-period limits remain unchanged. Each mode contains four batches of 50.
Warm preparation uses four concurrent opens outside the timed region; all 50
timed opens start together. Cold batches restart the application and browser;
the operating-system filesystem cache was not flushed. Timed opens use real
API, PostgreSQL and artifacts. Resource collection starts after timed openings.

| Candidate measure, ms | p50 | p75 | p95 | p99 |
| --- | ---: | ---: | ---: | ---: |
| Warm neutral frame | 45.1 | 51.7 | 62.0 | 64.6 |
| Warm dispatch | 4.1 | 4.5 | 5.4 | 6.8 |
| Warm first useful graph | 564.8 | 744.9 | 794.6 | 951.1 |
| Warm complete active cards | 555.8 | 733.2 | 778.9 | 908.0 |
| Warm last completed response to stable graph | 32.4 | 44.3 | 88.7 | 102.8 |
| Cold first useful graph | 1166.1 | 1367.6 | 1495.9 | 1620.9 |
| Cold complete active cards | 1162.9 | 1365.0 | 1482.4 | 1571.3 |

Candidate: **200/200 warm and 200/200 cold openings passed**. The selected warm
frame/dispatch/paint and warm/cold graph thresholds pass. Foreground two-toggle
Event Timing upper-bound p75 is 48 ms in both modes; this sampled interaction
measure is not a field INP claim. Simultaneous interaction in 50 tabs is reported
separately and is not substituted for foreground interaction. Warm openings had
zero observed LongTask entries. Measurements and source/build/harness hashes are in
[warm](candidate-warm-8w-controlled.json),
[cold](candidate-cold-8w-controlled.json), and [quantiles](timing-summary.json).

Baseline: 195/200 warm openings completed, with successful graph p95 321.4 ms;
five timed out before the full workset criterion. That fast baseline path can
display retained inactive cached data before a current API response completes.
It is not equivalent to the candidate's fresh authorized read, so no warm
speedup ratio is claimed. All 200 cold baseline openings timed out at 30 seconds;
there are no successful cold-baseline quantiles. Every failure remains in
[warm baseline](baseline-warm-8w-controlled.json) and
[cold baseline](baseline-cold-8w-controlled.json). Diagnostics and rejected
profiles remain in [execution notes](execution-notes.md).

## Compatibility and rollout

Requirement IDs are those declared by the ticket, notably WEB-PERF-001..006,
WEB-ARCH-002/004/006, AUTH-004/005/006/009, SEC-010, ROUTE-003, A11Y-001 and
I18N-001. [Serving contract version 7](../../../../docs/contracts/report-refresh-serving-recovery-contract.md)
and [Web source contract version 17](../../../../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md)
describe the resulting boundaries.

| Boundary | Classification | Practical effect |
| --- | --- | --- |
| Editor API | compatible-change | Optional bounded ready results; old fallback reads remain available |
| Content encoding | compatible-change | Gzip only when negotiated and smaller; no-store and Vary preserved |
| Identity API/events | compatible-change | Additive activity/event paths; current authorization and CSRF still apply |
| Persistence | compatible-change | Migration 0013 adds lifecycle/invalidation support without rewriting results |
| Activity semantics | compatible-change | Approximate interactive last-use; no longer passive polling timestamps |
| Config | compatible-change | Optional process policy; defaults unchanged |
| Result/view identity | none | No new result identity, formula, calendar or save semantics |
| Browser/cache lifecycle | compatible-change | Bounded eviction and fail-closed reconciliation; navigation state preserved |
| Rollback/operations | compatible-change | Coordinate API, Web and migration; old code cannot provide new invalidation/retention guarantees |

Migration and rollback checks are local evidence. This task neither selects a
production deployment target nor authorizes destructive downgrade or cleanup.
No claim is made that a source-only rollback preserves the new browser security
behavior while incompatible API versions are mixed.

## Verification and remaining observation

Final source gates passed: `uv run --locked python -m tools.check --scope local`,
`node apps/web/scripts/generate-pilot.mjs --check`, and `git diff --check`.
Focused Ruff and Pyright passed. Final production build and 87 Web tests passed.
Focused unit tests passed 27/27; isolated real PostgreSQL lifecycle passed 9/9
and presentation save/reopen passed 1/1. Final browser regressions passed 16/16.

The explicitly targeted lifecycle suite passed 4/4, including cross-process
revocation p95 32 ms across 20 tab observations / 10 session cycles. The initial
wrong-target invocation failed fixture login with 422 and skipped two cases;
it remains disclosed in [exact commands and outcomes](final-checks.json).
The 50-card stress case admitted 1,426,034 bytes in one cache entry and issued
zero result GETs or compute POSTs on open; the oversized real transport was
rejected and recovered on retry.

Extended navigation passed 1,000 mount/unmount cycles and 201 reconnects. With
explicit browser collection for retained-heap measurement, the final 400 cycles
ranged from 11.60 to 11.89 MiB; final heap was 11.80 MiB, documents 2, listeners
563 (unchanged), and DOM nodes 3,073 to 3,074. Cache stayed at 51,270 bytes / two
entries. [Sanitized sample record](navigation-memory.json) and [summary](navigation-memory-summary.json)
cover one fixture repeatedly mounted, not distinct reports or total browser RSS.
The earlier 30- and 150-cycle samples are retained separately; their smaller
positive slope was the reason to extend the test, not claim an early plateau.

The separate 2,000-real-read API diagnostic had zero failures, no forced GC and
a final ten-batch RSS range of 1,747.1–1,784.0 MiB, ending at 1,763.5 MiB.
It selected the same GC/thread values through the diagnostic wrapper before
normal application settings were added; it is supporting evidence with that
binding limitation, not a substitute for the final normal-runtime idle test.

Source ownership is recorded in [the W39 delta manifest](owned-source-manifest.json).
It includes the separately preserved owner EUR/UTC context repair in shared
files; the captured patch is identified by hash in the [publication sanitization record](publication-sanitization.json).
All 169 [frozen inherited inputs](frozen-input-check.json) remain unchanged.

The final normal-runtime idle observation completed **1,800,268 ms**, with 50
graphs at every sampled point, zero page errors, zero activity changes and 100
token rotations. No heartbeat security events were inserted. Artifact bytes
remained 100,299,903. Cohort events were 50 initial session creations and 100
rotations. The disclosed early diagnostic login/logout outside the cohort
accounts for one extra session, one extra session update and two audit events.
Global WAL grew 3,103,275 bytes; table relation sizes did not grow, indexes grew
65,536 bytes in total, and sampled session dead tuples rose by 100. These are
observed local deltas, not physical deletion or backup-retention guarantees.

Without forced collection, summed browser heap decreased from 601,486,316 to
583,153,788 bytes. Maximum final accounted cache was 1,353,193 bytes / two
entries. Aggregate API RSS rose from 1,335.0 to 2,019.9 MiB (about 1.97 GiB),
below the 4-GiB container limit; it remained near 1,998–2,020 MiB after the second
renewal. No indefinite-duration memory guarantee is inferred. See [raw idle
sample record](final-profile-idle.json) and [attributed summary](final-profile-idle-summary.json).
The active controlled-clock real-SQL test observed exactly 600 activity updates
for 50 sessions over 60 simulated minutes; this is not an elapsed-hour soak.

Expanded strict Pyright initially exposed missing test annotations and a
decorator registration diagnostic. Typed fixtures/helpers and an explicit
non-null session assertion were added; the nine real PostgreSQL tests passed
again in 8.86s. The sole post-measurement API edit is an exact comment-only
suppression for the FastAPI-registered endpoint. [Python 3.12 compiled-code
equality](python-bytecode-equivalence.json) proves no bytecode, constant or line
metadata change. All other 247 performance-bound source files are unchanged.
Final full-API / affected-integration Pyright and scoped Ruff pass. Test-helper
formatting and configurable long-navigation cycles do not change product code.

The [ordinary local stand](http://localhost:41746/w/70568e58-2a23-4de1-9cf7-17bb44e8ae8d/reports/9285c38c-574d-5ce3-a8d1-028e809cc1ff/edit)
uses the selected eight-process policy without instrumentation. Its localhost
origin is separately allowed to avoid cookies shared with the owner's
127.0.0.1 demonstration. [UI login and ready graph proof](final-stand.json) and
[screenshot](final-demo.png) passed without compute requests. The old task-owned
41740/58140 stand was stopped; owner ports 41744/58144 were untouched.

Synthetic local login: workspace `70568e58-2a23-4de1-9cf7-17bb44e8ae8d`, email
`author@example.test`, password `synthetic-author-password`. These are disposable
fixture credentials, not production credentials. The demonstrated three-card
original report is a UI smoke fixture; the measured 50-user workload remains the
separately documented three-workset/six-card fixture.

Local implementation and declared local proof are complete. The ticket remains
`active` for owner review; MS-004 acceptance, canonical import, publication and
production rollout are outside this handoff. The next safe action is review of
this checkpoint and its separately identified W39 changes.

## Subsequent owner correction 001

[The correction report](owner-correction-001/report.md) records the owner's six
presentation corrections, updated build and targeted checks. It supersedes the
currency/timezone presentation decision above, preserving all earlier raw proof.
Frontend performance values above belong to the earlier measured build; no new
50-user performance or idle qualification is inferred for the corrected bundle.

## Subsequent owner correction 002

[Correction 002](owner-correction-002/README.md) appends the external header, independent left/right
docks and guarded workset creation evidence. Earlier correction and measurement
files remain unchanged. The current bundle has targeted local frontend proof,
not a new backend/idle/load qualification.

## Subsequent owner correction 003

[Correction 003](owner-correction-003/README.md) records compact cards, authoritative per-card YoY,
signed semantic-color tooltips and bounded normal-chart height with padded axes.
It supersedes the earlier remaining-viewport normal-height decision; earlier
measurements remain attached to their original build and are not rewritten.

## Subsequent owner correction 004

[Correction 004](owner-correction-004/README.md) records whole-unit cards, percentage precision, native
whole-card selection and independent controls, separated surfaces, cached
selection without automatic Apply, and reduced-motion-aware chart updates.
This is additive local proof; prior backend/idle evidence remains unchanged.
Source contract version 21; no publication/import or milestone acceptance.

## Subsequent owner correction 005

[Correction005](owner-correction-005/README.md) records direct coordinator repairs to workspace-bound Focus, fixed card widths, on-page comparison controls and expanded catalog layout. Source contract22; focused local Browser proof, no publication or milestone acceptance.

## Owner correction 006 — direct coordinator follow-up

[Evidence](owner-correction-006/README.md) records the owner's selected variant 2:
editable title, state and primary report actions in the global header, secondary
actions in an accessible disclosure, compact worksets above results. Source
contract v23 supersedes the previous configuration-panel presentation. No other
task or agent was used; no owner report was saved. Existing acceptance and
publication boundaries remain unchanged.

## Owner correction 007

[Result expansion correction](owner-correction-007/README.md) records direct implementation and browser proof under source contract v24. Local UI only; existing acceptance/publication boundaries unchanged.

## Owner correction 008

[Table caption removal](owner-correction-008/README.md) implements the owner correction under source contract v25. Local presentation proof only.

## Owner correction 009

[Title focus repair](owner-correction-009/README.md) records the bounded UI correction under source contract v26; no acceptance/publication changes.

## Owner correction 010

[Context shortcut removal](owner-correction-010/README.md) implements source contract v27; acceptance/publication boundaries unchanged.
