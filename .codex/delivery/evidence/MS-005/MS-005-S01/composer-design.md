# Composer authoring contract and C02 transition design

## Decision and implementation boundary

Selected under WS-004/DEC-06 technical delegation. C01 implements only the pure
[analytical-authoring/v1 DTO](../../../../../packages/contracts/presentation/composer.py)
and its tests. All API/repository/browser transitions below are C02 implementation
obligations, not deployed facts. This is a Presentation modular-monolith extension;
no new service, independent document store, second formula engine or ChartSpec fork.

The existing v1/v2 contracts remain unchanged. Authoring-v1 is a separate envelope,
not a relabelled configured-report/v2. It defines chapters/pages/sections/blocks,
closed placement/presentation and explicit Analytics input references. The first
supported data-block subset is chart/table using metric-workspace/v2. Structural
profile validation recognizes the three normative profiles; C02 capability
negotiation exposes only the implemented workbook workflow until other profile
adapters exist. Structural acceptance does not authorize a provider or actor.

Alternatives rejected: placing untyped blocks in v2 breaks strict readers and
allows arbitrary nested options; localStorage loses durable truth; a separate
composer repository would duplicate source of truth and transactional invariants.
A separate new schema evolves safely while sharing repositories, public ports,
component shell and future root/page manifest lifecycle.

## Identity, ownership and validation

Presentation owns graph/placement/presentation/document draft/version. Analytics
owns WorkspaceRunRequest normalization, provider capability, policy-bound results
and totals. Semantic Model owns metric/calendar validity; Identity owns actual
actor/object/data authorization. DTO creator attribution is untrusted input until
matched to authenticated actor and immutable repository creator.

- Node IDs are unique across document/chapter/page/section/block/analysis definitions.
  Sibling order is explicit, unique and nonnegative. Default page exists; section
  parents must exist in the same page; cycles fail. Rendering traverses chapter,
  page, section and block orders, not source-array order or visual coordinates.
- Grid sections use 12 logical columns, positive spans and non-overlapping integer
  rectangles. This is a presentation coordinate system, not a page/block count cap.
  Flow/narrative reject grid placement. Responsive stacking preserves reading order.
- Definitions carry typed existing provider queries; blocks reference exact metric
  versions included in the query. No SQL, callbacks, library options, raw HTML/CSS
  or arbitrary asset/URL fields exist. Titles are plain text, never interpreted HTML.
- Copy creates fresh block and editable definition IDs. A shared-result chart/table
  may reference one definition. Editing just one block's semantic input must detach
  to a new definition when shared (copy-on-write), unless the user explicitly edits
  the shared source. Presentation edits never detach or trigger a calculation.
- `input_fingerprint` excludes IDs/layout/title/density and canonicalizes metric
  order; it is only a grouping hint. It cannot authorize reuse or serve as a final
  cache key: Analytics `normalize` adds actor/workspace, policy/allowed stores,
  source publication/bindings, metric components and calendar context. Different
  fingerprints can still normalize to one effective query after inheritance.
- No 20-workset/200-card cap is copied into the new document. Request size, active
  page and compute admission use explicit existing runtime/resource policy; richer
  document policy is later versioned/benchmarked. The 100 x 30 DTO test proves only
  shape admission, not speed, concurrency, memory or runtime scale.
- Cross-page authorization and permission-safe block omission are resolved before
  returning metadata. A failed block result stays local; document identity/access
  failure invalidates the whole document. No denied labels/counts/layout holes.

## C02 public API and persistence seam

Target route namespace: `/api/reports/composer/v1`, mounted before legacy dynamic
report-ID routes. Required operations: prepare a new definition; validate/resolve
and apply a selected block; save a document revision; read editor/latest version;
read an exact saved version/snapshot. Use generated OpenAPI/TypeScript contracts.
C02 must finalize response DTOs before mounting, with explicit capability values
for profile, provider, block kind and output channel. Unsupported old clients
receive a stable authorized version/capability error, never lossy flattening.

The save command uses ComposerSaveRequest (`contract_version`, complete definition,
`expected_revision`, `idempotency_key`). A draft save is definition persistence,
not a hidden compute or Publish. If exact ready results are included in a saved
preview, verified result references and per-block input fingerprints are admitted
separately; changed/unresolved inputs must remain explicitly pending and cannot
reuse stale trusted values. Do not turn draft autosave into calculation.

A saved report response is version-dispatched as `composed-report/v1`, with exact
document/revision/version/snapshot/author/saved-at and closed composition/verified
result bindings. Add readers before new writes. Preserve all old response bytes,
creator-only definition edits, saved-view-v1 parsing and native v2 behavior.
New saved views require `composer-view/v1`, pinning document version/hash and typed
block-keyed display/context overrides. Do not overload the one-selection ViewDisplay.
C02 needs exact save/reopen; full shared Explore/publication remains C08.

Reuse `presentation_documents` and `presentation_versions`; add the new discriminator
through an additive migration. **The existing 0012 CHECK admits only draft-report/v1
and configured-report/v2.** Therefore new persisted writes cannot be activated by
code alone. Inspect the live migration head and the unrelated 0013 identity changes
before selecting the actual new revision; do not renumber or edit accepted migrations.

Reuse the repository transaction invariant: lock document in workspace; check
immutable creator/current permissions; check idempotency key and full request hash;
CAS expected document revision; insert immutable version; commit any companion view
in the same transaction; recheck authorization; advance latest atomically. A replay
with same key/payload returns the original version after current authorization;
same key/different payload is conflict. Read after unknown response before resubmit;
only an identical key/payload may be retried automatically after reconciliation.

Artifact admission occurs before the database pointer switch. Crash can leave an
unreferenced committed artifact but never a pointer to an incomplete snapshot. Use
existing retention/reconciliation ownership, not broad cleanup. Keep immutable old
snapshots and result-parent edges. A new draft revision never rewrites a publication.

## Calls, failures and recovery

| Caller -> owner | Contract / authorization | Failure and retry |
|---|---|---|
| Web -> reports API | authenticated workspace session and CSRF for mutations; strict versioned DTO; creator plus functional/object/data checks | validation 422; forbidden 403 or existing privacy-safe not-found convention; revision/idempotency 409; unsupported-version stable code after access check |
| Presentation -> Analytics public port | WorkspaceRunRequest and exact refs; current actor/workspace; provider resolve/verify/run | preserve FORBIDDEN, METRIC_BASIS_MISMATCH, CALENDAR_BINDING_MISMATCH, unavailable/integrity codes; no retry of semantic/authorization errors |
| Presentation -> Identity | current resource action/scope; creator is additional requirement | revoke invalidates read/save/export regardless of cached result; no stale allow fallback |
| Presentation -> Artifacts | immutable result/manifests and declared parent hashes | distinguish missing, corrupt and transient storage unavailable; never fabricate empty result; bounded idempotent read retry under existing runtime policy |
| Presentation -> repository | same document lock/CAS/key/hash transaction, current auth recheck | conflict reload/rebase preserves foreign edits; unknown outcome reconciles key/version; no blind new-key retry |

Existing provider calls are synchronous in-process; do not introduce network timeouts
or a queue engine. C02 reuses current request cancellation/runtime policy and gives
each block a generation token so late results cannot overwrite a different input.
No guessed automatic retry count, deadline, latency budget or resource threshold.
Correlate document/version/block/run IDs and sanitized stable error codes; exclude
credentials, session data, rows and raw provider payloads. Existing runtime owners
handle storage/integrity/admission signals; C02 must bind actual operational
metrics/runbook behavior before claiming production rollout readiness.

## Legacy compatibility and explicit conversion

| Direction | Required behavior / classification |
|---|---|
| Existing clients + new server, old documents | preserve v1/v2 payloads/endpoints; `compatible-change` only after generated/real-API regression proof |
| New reader + old documents | dispatch unchanged old reader and deterministic editor projection; preserve original snapshot and saved-view bytes |
| Old reader + new composed-report/v1 | known unsupported payload; `breaking-change` if sent unnegotiated. Retain compatible reader or return explicit unsupported state |
| New views + old saved-view reader | never send composer-view/v1 as saved-view/v1; keep old objects immutable |
| New writer + old DB CHECK | `breaking-change`: INSERT fails until expansion migration; writer must be disabled before schema readiness |
| Old writer after conversion | CAS/version-aware conflict, never regenerate and overwrite a richer composition |
| Rollback with newly written documents | preserve new data; retain new reader or disable access to unsupported documents. Downgrade refuses when new discriminator rows exist |

C02's first useful path creates new composed documents. Old reports continue to
open/edit through their existing supported model and shell. A deterministic
read-only projection may show the old selected result in the block surface, but
must preserve card/workset/context semantics and cannot claim a lossless conversion
by dropping the metric rail. Explicit conversion creates a new draft with origin
lineage and fresh instance IDs only after all existing visible/persisted components
are representable. If not, keep the legacy editor and explain conversion unavailable;
never silently flatten, overwrite, or mutate the old report to finish C02.

## Disposable rehearsal required before C02 writes are accepted

1. Start a new test-owned database/artifact root through the existing synthetic
   harness, not the retained workspace report. Record old v1/v2/view/snapshot fixture
   hashes and restore baseline in that disposable environment.
2. Apply reader/schema expansion, check old reads and old-client API responses;
   exercise denial and immutable creator. No production migration is implied.
3. Create four independently configured charts and two tables; place chart/table
   side by side; save/reopen through real API and compare definitions/IDs/layout,
   results, query counts and artifact identity. Chart/table compatible queries reuse.
4. Race identical save retries and stale revisions; inject failure between artifact
   admission and pointer commit; test revoked access, stale block responses and
   partial result failures. Assert no lost update, duplicate version or bad pointer.
5. Read all old exact snapshots/views and compare original hashes. Verify new
   version cannot be sent through old reader unnoticed. Reconcile lost response.
6. Disable writer; test old-only downgrade on pre-write disposable baseline and
   refusal with new rows. Restore/reopen new documents with compatible reader;
   never delete new rows to force a green rollback.

C01 tests the schema and legacy readers only. None of these real DB/API/browser
steps has been performed for composed-report/v1. They are C02 acceptance inputs.

## Holds and later providers

Full clause inventory lives in [requirement audit](requirement-audit.md). Pivot,
filters/parameters/interactions, Research/Collaboration, general branding and static
rendering require existing-context implementations before their outcomes close.
Forecasting remains held. Numeric performance budgets/hardware/corpus require a
real decision before C10 acceptance. These limits do not block independent C02
chart/table work, and they cannot be erased by adding unsupported UI choices.
