# W39 active execution observations

Owner launch received through coordinator `01a0c02d-5267-7601-b735-5b43d11789c0`
on 2026-09-23 (Europe/Moscow). One executor, no agents/Goal/publication.
Current cwd: `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`.
The inherited manifest matched all 193 files and HEAD before changing the ticket
from ready to active. The original and canonical checkouts remain read-only.

## Baseline stand

Own production Web preview: `http://127.0.0.1:41739`; API: `127.0.0.1:58139`.
Own PostgreSQL: `custometry-w39-3100d0f03545`, image
`sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4`,
2 GiB memory / 4 CPUs, dynamically allocated loopback database port.
Old demonstration ports 41744/58144 are untouched.
The baseline real Chromium login, Apply/Save and reload test passed (1 test,
25.9 seconds, zero page errors); screenshot: [baseline demo](baseline-demo.png).
Access details were sent to the coordinator. All users are synthetic.
The inherited health probe reports schema incompatibility (expects 0011 while
inherited schema is 0012); this is separate from the observed successful journey.

Local dependencies installed with `uv sync --locked --all-packages --all-groups`
and `corepack pnpm install --frozen-lockfile`. Added pinned `psycopg-pool==3.2.6`
for scoped, bounded connection reuse. Pool semantics were checked against the
[official Psycopg documentation](https://www.psycopg.org/psycopg3/docs/advanced/pool.html).

## Measurements in progress

[Baseline serving profile](baseline-profile.txt) observed 6.577 seconds for one
real `WorkspaceReportService.get`, 144 connection establishments and eight full
`read_sales_inputs` calls (5.356 cumulative seconds). Profiling overhead and
concurrent fixture provisioning make this diagnostic attribution, not an
acceptance latency measurement.

Fifty distinct synthetic principals each own a report with three worksets of
six cards, all three registered metrics, and 2025 daily results with the 2024
previous-year comparison. Existing contracts bound each current period to 366
days; two-year coverage uses the existing temporal-comparison contract without
relaxing that limit. Prepared fixtures retain identities between comparisons.
The production browser harness performs 200 warm internal opens at concurrency
50, then a 30-minute idle run. Baseline does not implement renewal; the harness
does not silently inject it or conceal the baseline expiry behavior.
Resource sampling observes only the task-owned database/artifact root and the
explicit task process tree; no unrelated user process activity is collected.

The reproducible baseline source/build was reconstructed under ignored
`.runtime/w39/baseline` from the base commit and inherited patch before candidate
builds. Runtime connection paths and ephemeral synthetic sessions never enter
durable evidence. No performance target is claimed achieved at this point.

## Additional owner correction

The coordinator supplied the explicitly requested EUR/UTC deduplication patch
from canonical `.codex/delivery/evidence/report-context-dedup-2026-09-23/repair.patch`.
`git apply --check` and scoped application passed, preserving W39 edits. It changes
only PilotDocument, WorkspaceProjection, pilot port/seams and generated runtime.
The general context is shown once beside the report title; metric-specific units
remain. This is additional W39 input, not part of the frozen inherited manifest.
No MS-004 evidence or journal has been edited by W39.

## Current source verification

- Web typecheck passed after regenerating workspace contracts.
- Web suite: 85 tests / 20 files passed.
- Focused Python typecheck: passed (pool, identity HTTP/events, prepared serving,
  workspace composition, maintenance).
- Ruff across API, Identity and the new migration: passed.
- `python -m tools.check --scope local --json`: passed, 17 selected source/static
  checks, 13 migration revisions, W39 active, no findings.

These are intermediate source checks. Real candidate behavior, cold/warm
performance, resource bounds, retention, multi-worker reconnect/revoke and final
browser acceptance remain pending. The ticket remains active.

## Candidate runtime checkpoint

The task-owned baseline completed 200 warm attempts with 64 failed attempts.
Failures remain in raw timings; expiry during the long run is a confounder, so
these attempts cannot establish a controlled latency comparison. The baseline
30-minute idle interval began at `2026-09-22T22:39:07.411Z`.
The candidate uses a separate PostgreSQL clone, API 58140 and production Web
41740. Real Chromium smoke found an undefined pending `workspaceChrome`; the
pending model now supplies neutral values. Initial prototype markup is hidden
until the application bridge has replaced it. A repeated real login/report open
returned the graph and six cards with zero JavaScript errors.

Current additional checks:
- `uv run --locked python scripts/w39-integration.py tests/integration/identity_access`:
  10 passed, including interruption rollback/retry.
- `uv run --locked python scripts/w39-integration.py tests/integration/presentation/test_workspace_s03.py`:
  1 passed using its own source/control PostgreSQL fixture (21.74 seconds).
- `corepack pnpm --filter @custometry/web test`: 85 passed in 20 files.
- `corepack pnpm --filter @custometry/web build`: passed; existing bundle size warning.
- Focused Pyright: zero errors/warnings; grouped local gate passed, captured in
  `implementation-local-gates.json`.

An earlier integration invocation named a nonexistent test file; another omitted
source-fixture environment. Both were harness failures, corrected before the
successful runs above. Candidate 50-user timings and idle proof are in progress;
no performance or completion verdict follows from this checkpoint.

The first candidate warm run completed 200/200 without failed opens. Driver-observed
first-graph p50/p75/p95/p99 were 18201.75/19755.61/21897.72/22530.29 ms:
**the warm latency target is not met**. Individual request traces show substantial
API wait, not only browser drawing. The candidate is now in its 30-minute idle
interval. Two explicitly labelled `W39 profile` sessions were created for
read-only diagnostic profiles after this interval began; their login writes must
be separated from the 50 load sessions in aggregate database accounting.

A follow-up request-local repository memo reduces duplicate immutable reads;
it is bounded to 64 entries / 16 MiB and exists only for GET service instances.
It does not replace authentication or resource authorization and is not deployed
to the running idle-soak process yet. PostgreSQL presentation invariants passed
again after this change (1 test, 18.50 seconds). The controlled-clock active-use
integration passed with exactly 600 activity updates across 50 sessions and 60
simulated minutes; this is not represented as a real elapsed-hour observation.

## Browser and lifecycle checkpoint

Dedicated real API/PostgreSQL browser tests passed delayed neutral entry, offline
recovery and two-tab logout. A second independent API process using the same QA
PostgreSQL received transactional invalidation: 20 tab observations over 10
logout-all cycles had p95 54 ms in the initial run (raw repeated measurements
are retained in `cross-worker-revoke.json`). No mock event bus was used.

The maximum supported 50-card workset opened with one deduplicated result read,
zero compute requests and 1,429,699 accounted cache bytes / 3 entries in the
initial stress run. The oversized transport test adds valid JSON whitespace to
an actual real-API result: it is explicit fault injection, not a measured serving
path or a fabricated stored artifact. It verifies rejection and successful retry.

The existing 16 browser regression cases were run against an isolated QA stand.
After updating denial assertions for the retained neutral frame and allowing
request cancellation, 15 passed; one Chromium `Network.getResponseBody` retrieval
failed intermittently. The temporal test now observes a clone of the actual
streamed browser response instead of relying on the discarded CDP body buffer;
both viewport cases then passed. Chart inspection now uses the existing iframe
ECharts instance, so it does not require a development-server module URL.
A production-build regression rerun is in progress.

The baseline idle interval ended at `2026-09-22T23:09:07.448Z` with zero visible
report frames: it does not maintain the 50 open reports through expiry. Candidate
sessions have completed two 50-session rotation cycles without advancing any
load-session `last_seen_at`. Candidate idle completion is still pending.

The pool limit was tightened to 8 connections per worker, bounding an eight-worker
benchmark to 64 pooled connections plus at most eight event listeners. Follow-up
controlled warm/cold scripts use real synthetic sessions prepared outside timing,
refresh before each batch, browser-side frame/graph timing, and explicit worker
counts. The initial single-worker diagnostic timings remain unmodified.

## Completed soak and controlled load checkpoint

Both 30-minute runs completed. `idle-summary.json` contains sampled deltas,
explicit sample boundaries and limitations. Candidate load sessions have zero
activity updates, 100 real refresh rotations/history/audit entries, and zero
artifact growth. Two diagnostic login inserts are separated from that cohort.
The candidate retained 50 report iframes; the baseline retained zero after expiry.
This final count alone does not assert rendered graph correctness. Candidate
API RSS rose from roughly 505 MiB to 635 MiB during the sampled interval; the
navigation/eviction plateau check is a separate required observation.

The 16-case production browser regression passed. Three lifecycle/resource cases
also passed, including real cross-worker invalidation, 50-card deduplication and
rejection/retry for an injected 3.2 MB response. The latest neutral-frame layout
was visually inspected. A subsequent frame-mount layout effect and omission of
unused legacy chart initialization require follow-up browser verification.

The first controlled eight-worker candidate runs each completed 200 openings
without failures. Warm first-graph p95 was 5.228 seconds; cold p95 6.653 seconds.
These do NOT meet the ticket's 1/2 second thresholds. Their raw records are retained
as `candidate-{warm,cold}-8w-before-frame-adjustment.json`. Simultaneous interaction
stress also exceeded the representative INP target and is reported separately
from any single-foreground-user sample. The same eight-worker baseline run has
observed PostgreSQL `too many clients already` errors under concurrent opening;
these are load failures, not silently excluded from acceptance.

## Warm preconditioning repair and next diagnostic seam

The first eight-worker baseline warm run was interrupted after its persisted
50 measurements (49 passed, one timeout). Its raw file is retained as
`baseline-warm-8w-concurrent-prime-partial.json`. Priming all 50 browser contexts
simultaneously also produced connection exhaustion before timing and spent four
minutes waiting for a failed warm-up. The matched harness now primes four users
at a time for BOTH versions, then refreshes real sessions and dispatches all 50
measured navigations concurrently. This changes preconditioning, not the measured
concurrency or thresholds. Fresh comparison files will name that setting.

`scripts/w39_instrumented.py` is an opt-in diagnostic-only ASGI wrapper. It adds
aggregate Server-Timing for application response start, AnyIO thread-queue wait
and synchronous SQL duration/count, without query text or values. The optional
thread limit is a diagnostic factor, not a silently applied production setting.
`api-spans.mjs` will compare equal 50-user direct HTTP batches to isolate metadata
serving from browser transfer/parse/paint. It is not first-graph acceptance proof.
The controlled browser harness now also captures response-start and Server-Timing
when the diagnostic wrapper is explicitly enabled.

The interrupted concurrent-prime process persisted its second batch during
termination before exiting. The preserved partial file therefore contains
100 attempts / 3 failures, superseding the earlier 50-attempt checkpoint count.
The matched four-user preconditioned run remains distinct. Diagnostic helper
Ruff checks passed; no product acceptance follows from helper lint.

## Request projection investigation (not acceptance timing)

While the baseline was in its untimed preconditioning interval, three direct
50-request candidate batches were observed per setting. The raw diagnostics have
UTC start/end timestamps. At 40 AnyIO threads, metadata response-start p95 was
1.552s; queue p95 11ms; each request made 93 SQL statements. At two threads the
response p95 was 1.579s and queue p95 1.368s: that setting merely moved waiting
into the executor queue and was NOT adopted as an optimization.

An opt-in Identity request projection now reuses identical read rows at a fixed
request effective time. Its lifetime is one GET composition, bounded to 128
statements / 2,048 rows per admitted statement / 1 MiB accounted row payload.
It deep-copies rows supplied to evaluators and never participates in POST/write
checkpoints. Every new GET creates a fresh projection. This reduces the observed
metadata statement count from 93 to 59. A first diagnostic still had p95 1.794s
on the shared host; no latency improvement is claimed. Isolated confirmation and
real PostgreSQL access-freshness/organization regression are required before
retaining this implementation. Direct HTTP samples do not measure result follow-up
or browser paint. Original diagnostic files retain the `before-projection` suffix.

## Embedded active result and bounded-memory checkpoint

Three focused checks passed: real PostgreSQL request-to-request membership
freshness plus two projection alias/budget/statement unit checks (0.33s test time).
The editor now returns optional/additive `ready_results` from the same verified
request objects: default active workset only, deduplicated, at most 32 and 2 MiB
combined. If the whole set does not fit, existing result endpoints remain the
fallback. The browser verifies saved bindings and retains these objects only in
the editor query, dropping them when a different working set needs other data.
This removes a second authenticated read/verification/transfer of the same result.

The first lifecycle rerun exposed a composition bug: the response's RootModel was
not unwrapped, so the optional list stayed empty (3 cases passed, maximum-workset
expected-zero-read assertion failed). The router now reads `editor.report.root`.
After that repair all four cases passed in 26.5s. The 50-card case made zero
separate result GETs and zero compute requests; fallback oversize/retry is tested
by explicitly removing the optional field from the real editor response before
injecting whitespace into the real result response. This is fault injection,
not a performance sample.

Thirty internal navigations plus seven real offline/reconnect cycles retained
2 documents and 700 event listeners, with 4,114-4,116 DOM nodes after forced GC.
Heap rose from 8.57 MB initially to 11.60 MB at cycle 25 and 11.48 MB at cycle 30.
That is a one-tab fixture-report plateau observation, not total process RSS or
50 concurrent maximum worksets. `navigation-memory.json` records the actual card
count; an earlier draft description incorrectly named the separate 50-card case.
Production build/typecheck passed after the additive response generation.

For forthcoming matched cold runs, both versions use a 30-second measured-open
timeout (the warm run already underway retains its 240-second timeout). A timeout
is a failure, never a discarded sample or a relaxed 2-second target. Untimed
pre-batch token refresh is also bounded to four concurrent calls so setup does
not become an unintended authentication stress test. New runs record their exact
Web bundle hashes. Existing completed evidence is not relabelled with new hashes.

Frontend projection now reuses stable display inputs, indexes buckets once rather
than repeatedly searching each full date array, and constructs number formatters
per renderer instead of per cell. This addresses the measured interaction-stress
failure; latency improvement remains unproven until the repeated browser sample.
An intermediate typecheck caught a mistaken temporal-index property; corrected
production build and all 86 Web tests passed. No calculation/formula or number
format semantics were changed.

## Model reuse, JSON encoding and dispatch checkpoint

GET verification now returns its validated report model to the editor composer,
which serializes the validated response directly. The pooled JSONB decoder uses
the existing Pydantic JSON parser without string caching. Identity projection
copies retain independent mutable containers while reusing immutable scalars.
Initial editor fetching runs concurrently with the event handshake; protected
rendering remains gated by the trusted channel, and reconnect waits for renewal.

Two intermediate type errors (JSON loader input signature and a deliberately
partial test fixture assertion) were corrected. Production Web build and all
87 Web tests passed. Focused Pyright reported zero errors and Ruff passed;
real PostgreSQL projection/JSON tests passed (6), and separate Presentation
integration passed (1, 16.25s). These checks do not establish the performance goal.

The repeated 200-open runs have zero failures, but still miss graph targets:
warm p95 2,890.1 ms; cold p95 2,994.4 ms. Warm frame p95 is 70.8 ms,
dispatch p95 4.9 ms, and last-response-end to graph p95 84.4 ms. Concurrent
50-tab interaction stress p75 is 592 ms and remains separately reported.
All earlier phase results and baseline failures are retained. Baseline warm has
6 failures among 200 attempts; baseline cold has 200 timeout failures among 200.
No numeric successful cold baseline quantile exists.

Opt-in API instrumentation observes process-wide GC overlapping requests:
three 50-request rounds have overlapping-GC p95 354/347/318 ms. These are
process intervals shared by concurrent requests, not exclusive per-request CPU.
The next diagnostic varies only the GC allocation threshold; this does not
change production settings or establish a memory-safe policy.

## Read transaction and runtime diagnostics

GET pool checkout can use statement autocommit without adding another pool.
Explicit transaction rollback and restoration of ordinary checkout mode passed
against real PostgreSQL (1 test, 0.13s); Presentation integration passed separately
(1 test, 15.88s). Default mutation mode is unchanged. The current saved-view head
is resolved to an immutable version before reusing an already validated version.
The request artifact adapter also reuses only its filesystem configuration object;
every artifact path resolution and hash check still executes.

Runtime experiments remain opt-in harness settings, not product defaults:
GC thresholds 7,000 / 100,000 / 1,000,000 and a 1 ms thread-switch interval.
The 1 ms interval did not materially improve the 100,000-threshold browser run.
With statement autocommit and default GC, a 50-open diagnostic observed 913.6 ms
of overlapping process GC at p95 and graph p95 3,100.9 ms. At threshold 1,000,000,
no collections overlapped that batch: graph p95 1,570.2 ms, sampled API RSS sum
1,871.1 MiB. This is not a memory-plateau proof or a 200-open acceptance sample.
An additional 16-process / 4-pool-connections experiment kept the total pool cap
at 64, but graph p95 was 1,745.2 ms and sampled RSS sum 2,976.5 MiB. It is not
selected and does not replace the matched eight-process comparison evidence.

Concurrent cProfile output under `.runtime/w39/concurrent-profile-*.txt` included
multiple endpoint invocations and cumulative times exceeding the elapsed profile
window. It is not treated as an exclusive single-request attribution. Independent
Server-Timing request spans and thread CPU remain the timing evidence.

A new real-browser reconnect assertion reproduced loss of an unsaved workset
name (expected the draft name, observed persisted `Metrics`). The draft store now
retains one principal-bound definition during channel reconciliation and restores
it only after fresh authorized editor metadata. Logout, login and denied access
clear it; result/query caches still clear on every reconciliation. Snapshot views
do not restore editing drafts. Build and all 87 Web tests passed; browser rerun
is pending at this checkpoint.

## Shared budgets, reconnect and transport checkpoint

The corrected root Playwright invocation passed all 16 regression journeys and
4 lifecycle cases (23.2s), including draft preservation, cross-worker revoke,
maximum workset/oversize rejection and repeated navigation. An earlier invocation
from `apps/web` failed to locate the root virtualenv; its evidence is retained
under `cwd-mismatch-diagnostic`. Shared-budget/encoding unit tests passed (9),
real PostgreSQL Presentation integration passed (1, 15.70s), and focused Pyright
reported zero errors. Production Web build and all 87 tests passed.

The request repository budget is now shared across all adapters. Request artifact
manifest metadata and filesystem configuration can be reused; file/hash checks
remain. Response gzip reduced the measured editor transfer from roughly 1.35 MB
to 110 KB. Container-balanced eight-worker diagnostics (50 opens, no failures)
observed warm graph p95 1,190.7 ms before compression, 1,003.6 ms with compression
and two sync threads, and 1,148.1 ms with four. These are diagnostics, not the
required 200-open acceptance sample. The two-thread run still had response-end
to stable graph p95 129.4 ms.

The task-owned API image is
`sha256:81b4f1eb405c43f53c88c0d79bfd00bd6d366973f6abcb09358ac9eb7f02625e`,
with 8-CPU / 4-GiB limits; the existing task DB remains 4-CPU / 2-GiB. The Docker
VM has 18 CPUs / 8,317,267,968 bytes. Source is mounted read-only, and only the
synthetic fixture artifacts and secret are mounted. Nothing was published.
The opt-in balanced proxy, GC threshold and thread limits remain experiments;
no production runtime policy has been selected. Native worker imbalance reached
21 of 50 requests on one process; least-outstanding routing produced 6–7 per
process. Neither observation proves a production topology or memory plateau.

The next browser change reuses measured decoded payload size instead of encoding
it again and initializes the definition/chart in layout effects before paint.
Its build and 87 Web tests passed; performance and browser checks are pending.

## Browser rendering attribution checkpoint

Decoded-size reuse and synchronous definition/plot initialization produced a
50-open warm diagnostic p95 of 906.4 ms, but response-end to stable graph was
151.4 ms. Explicit SVG flush observed graph p95 924.4 ms and paint-span p95
136.4 ms. Instrumented plot construction p95 was 8.9 ms; response-end to plot
start was 5.8 ms. Chrome updates measured later at 0.4 ms p95. All samples are
retained; neither isolated below-one-second series establishes acceptance.

The static iframe/SVG control (`browser-frame-floor.json`, 200 observations,
50 pages) had two-frame p95 27.7 ms. The trace-enabled application diagnostic
retained only redacted aggregate categories in `browser-render-trace-summary.json`.
V8 major collections reached 89.8 ms and included parallel marking/sweep waits.
Nested/parallel trace totals are not exclusive CPU or request latency. This
rules out treating static browser scheduling alone as the demonstrated blocker.

The access adapter is now a module-level class rather than a new closure-bearing
class per request. Real PostgreSQL integration passed (1, 15.66s), and focused
Pyright passed. An initial test invocation used nonexistent `test_w39_serving.py`;
no tests ran, then the actual `test_workspace_s03.py` passed. Default-GC container
serving still missed the graph target (50 opens, p95 1,123.7 ms). Threshold 7,000
was also insufficient (1,087.1 ms), with overlapping GC p95 223.3 ms. The
one-thread / threshold-1,000,000 diagnostic measured 1,011.5 ms and paint-span
154.7 ms. No runtime tuning is selected from these observations.

The workspace adapter now skips generation of hidden legacy analytical tables,
pickers and configuration controls which are replaced by workspace components.
The seams retain their original behavior for legacy reports and regenerate the
runtime from the unchanged accepted source. Build, tests and browser regressions
are being verified before the next performance comparison.

## Complete warm diagnostic and measurement isolation

All 87 Web tests, 16 regression journeys (1.1m) and 4 lifecycle cases (22.9s)
passed after skipping hidden pilot initialization. A 200-open warm series had
zero failures: graph p95 858 ms, frame 68.5 ms, dispatch 5.3 ms, representative
foreground interaction p75 48 ms. Its response-to-stable-graph p95 still missed
the target at 133.4 ms. This remains a diagnostic runtime configuration.

A browser-only surface comparison found removal of workspace-header backdrop
blur changed 2,671 / 1,296,000 pixels by at most 2 RGB levels; layout and controls
were unchanged. The header has its own grid row without scrolling content
behind it. The scoped CSS override is retained. The next 50-open run observed
paint-span p95 101.1 ms and graph 862.6 ms. Stepped spinner animation did not
provide a consistent further benefit (paint 115.6 ms), so it was reverted.

The 2,000-read real-API run (`api-sustained-memory.json`) had no failed responses.
Without forced collections, the final ten 50-request batches ranged from
1,747.1 to 1,784.0 MiB aggregate API RSS and ended at 1,763.5 MiB. The test used
the diagnostic GC/thread configuration; the same policy is now available via
explicit optional application settings. Default settings remain unchanged.
A policy restoration/failure unit test passed; focused Pyright had zero errors.

Both browser builds report Chromium 136.0.7103.25 and hardware GPU compositing,
but default headless shell uses OpenGL while full Chromium uses Metal/Graphite.
The full-browser diagnostic measured graph p95 3,263.3 ms and frame 2,960.4 ms
for fifty windows; it is not selected. Hardware/renderer identities are saved in
`browser-renderer-profile.json`, and all timings are retained separately.

The harness previously attached CDP and gathered heap data as each page completed
while peer openings were still timed. These resource observations now run only
after all fifty timed openings finish. This removes a measurement interferer;
it does not relax the two-frame graph criterion or discard failures. The first
50-open run with deferred observation had graph p95 862.7 ms and response-to-graph
p95 95.7 ms. Full repeated batches and matched baseline remain pending.

## Final-profile candidate work in progress

The corrected-observation 200-open warm run passed graph latency (p95 840.4 ms)
but not paint latency (120.0 ms); no completion was inferred. Fifty independent
browser processes were also tested and rejected as a reference profile: client
RSS was 13,566.7 MiB, graph p95 4,782.8 ms and frame p95 1,199.7 ms. The selected
client mechanic remains one pinned headless-shell browser with fifty isolated
contexts; the alternate results remain explicit diagnostics.

The SVG renderer now sleeps after one still frame instead of ten empty frames,
using its existing public setting. Its normal refresh/interaction wakeup remains
unchanged. Build, 87 Web tests and all 16 regression cases passed (1.1m), including
server-value tooltips. A reserved pending inspector experiment also passed
functional tests but did not improve paint timing and was reverted. Its prior
failed replacement assertion made no source change; subsequent applied-source
checks were separate and passed.

Card loading marks now remain local and static while the plot-region indicator
rotates. This reduces concurrent moving layers without removing loading status
or the reduced-motion fallback. The 50-open diagnostic observed graph p95
798.5 ms and response-end to stable graph p95 83.9 ms, with no failures. Complete
200-open warm and cold series are running on this exact build. Foreground Event
Timing collection now filters by an interaction start cutoff, preventing queued
entries from the earlier concurrent stress phase entering the representative
foreground observations. No timing thresholds or graph criterion were relaxed.

## Completed final timing series and local gates

The final selected candidate completed 200 warm and 200 cold openings with zero
failures. Warm graph p95 is 794.6 ms, complete active cards 778.9 ms, neutral
frame 62.0 ms, dispatch 5.4 ms, and response-end to stable graph 88.7 ms. Cold
graph p95 is 1,495.9 ms and complete cards 1,482.4 ms. Foreground sampled
two-toggle Event Timing upper-bound p75 is 48 ms. The full selected thresholds
now pass; earlier failed and diagnostic runs remain unchanged.

The matched baseline completed 195/200 warm openings; five incomplete-workset
timeouts remain failures. Its successful graph p95 of 321.4 ms includes retained
inactive cache rendering without a completed fresh API response before paint,
so it is not evidence that the new authorized read is a warm speedup. All 200
cold baseline opens timed out at 30 seconds. No cold baseline percentile or
failure-free comparison is inferred. Read-only public repository checks confirm
identical canonical JSON hashes for all 50 saved baseline/candidate reports.

Final checks passed: local grouped profile, generator freshness, diff whitespace,
Ruff, focused Pyright, 27 unit tests, 9 lifecycle PostgreSQL checks, 1 presentation
PostgreSQL check, and 16 browser regressions. The lifecycle invocation initially
omitted its explicit W39 URL/scenario flags: it used the old default stand,
passed one test, skipped two and failed fixture login with 422. The corrected
owned-stand invocation passed all four tests in 23.1s; no product change was
needed. During the beginning of the final idle observation that mistaken
invocation caused a real login/logout on the shared candidate fixture, producing
one global invalidation/reconciliation of the fifty idle pages. It produced no
idle activity updates. Subsequent lifecycle checks used a separate database.

The selected normal application runtime is now running without diagnostic
instrumentation, using the explicit thread/GC settings. The final-build idle
observer checks source and served-asset hashes, fifty real graphs, SQL writes,
artifact bytes, RSS and heap for at least thirty minutes with no injected refresh,
foreground activity, or forced collections. Its outcome remains pending until
the completed result exists. See [implementation handoff](handoff.md) and
[exact final commands](final-checks.json).


## Completed normal-runtime idle proof and final handoff

The final selected idle run completed 1,800,268 ms with fifty graphs visible at
all 62 sampled points, zero activity changes, 100 token rotations, zero page
errors and zero artifact growth. WAL grew 3,103,275 bytes, indexes 65,536 bytes,
and table relation sizes did not change. Global row deltas include the disclosed
one diagnostic login/logout outside the idle cohort. Summed browser heap fell
from 601,486,316 to 583,153,788 bytes without forced collection. API RSS ended
at 2,019.9 MiB under its 4-GiB limit. Raw data and attributed summary are linked
from the completed implementation handoff.

A longer 1,000-cycle / 201-reconnect navigation test passed; retained heap in
the last 400 cycles stayed between 11.60 and 11.89 MiB, with two documents and
563 listeners. This is a one-report retained-heap experiment with explicit
collections, not total browser RSS or a claim about arbitrary distinct reports.

Expanded Ruff found helper import/layout issues, which were fixed. Expanded
strict Pyright found 114 initial diagnostics in the newly added test annotations
and the registered SSE callback. Typed fixtures/helpers resolved test diagnostics;
the nine PostgreSQL checks passed again. The API correction is a comment-only
precise suppression for the decorated function, with identical Python 3.12.12
compiled code. Final Pyright and Ruff pass. Intermediate failed checks are
preserved in final-checks.json rather than presented as initial passes.

The selected ordinary eight-process API and candidate Web remain at localhost
port 41746, without instrumentation. UI login and saved report rendering passed,
with no computation on open. Its additional localhost origin is the only final
stand harness configuration amendment; measured product behavior is unchanged.
Old task-owned 41740/58140 services and unused benchmark previews/baseline launcher
were stopped after proof capture. Owner 41744/58144 was not touched. The local
source gate, generator freshness and diff check pass after documentation updates.
All 169 frozen inherited files remain unchanged. No MS-004 acceptance, canonical
import, Git publication or deployment was performed.
