# MS-006-S01 — C02 persistent multi-block composition

Status: technically complete within the accepted C02 stage boundary. Canonical
acceptance and execution state belong exclusively to the stage journal.

## Result and owned changes

The accepted pilot shell now offers a three-step chart/table builder and a personal
workbook with independent block inputs, placement, Apply, error/retry, duplicate,
edit and delete. Four distinct time-grain charts and two tables save and reopen
through the real API. Compatible chart/table inputs reuse Analytics results.
Exact snapshot preview is read-only. The existing renderer/compiler handles each
block through deterministic projection; Presentation introduces no business math.

Owned additions are the composer contracts/client generator, application service,
API router, additive migration 0014, ComposerWorkspace/ComposerBuilder/state/copy/
styles, focused tests, disposable API/browser harnesses and this milestone's
planning/evidence artifacts. Owned hunks integrate the router, legacy-reader format
guards, version-aware repository save, permission-aware library dispatch and UI
entry, generated schemas/clients, contract exports and route inventory tests.
Foreign changes in these shared files remain preserved; this report does not claim
the entire dirty checkout as owned. No staging, publication or retained data writes.

Versioned composed-report/v1 storage admits the immutable graph and verified result
references. Creator, current functional/object/data access, optimistic revision,
request-key replay and artifact identity are enforced. Save never runs analytical
calculation. API responses expose current edit/run capabilities with false defaults.
A pre-pointer fault cannot advance the document. Existing v1/v2 rows and snapshots
are untouched, old readers explicitly reject new formats, and downgrade refuses
while composed rows exist rather than deleting or flattening data.

Draft survives session reconciliation while fresh access is required before display.
Definitive access reset purges memory. Save waits for active calculations. Unknown
Save outcomes keep the exact request across remount, freeze edits until retry is
acknowledged and reuse its idempotency key. Stale calculation responses cannot
replace changed inputs; returning to saved inputs reloads the corresponding result.

## Acceptance evidence

| Criterion | Evidence and boundary |
|---|---|
| AC-01 | Strict DTO/generated API/client; six mounted composer routes; current capabilities; old/new discriminator guards; contract tests |
| AC-02 | Owned PostgreSQL/API rehearsal: migration, pre-write rollback/re-upgrade, graph/layout/IDs, creator, CAS, replay/key conflict, concurrent retries, injected transaction failure, exact older snapshots, revocation, downgrade refusal |
| AC-03 | Three-step builder, explicit section target, standalone table, independent duplication/edit/delete, block-local failure/retry, keyboard focus, draft/retry lifecycle scenarios |
| AC-04 | Real browser four charts/two tables and four distinct result IDs; literal chart/table adjacency; exact save/reload without new Apply; 768px/390px observations |
| AC-05 | Existing reader dispatch and deterministic selected-result projection remain intact, preserving rail/worksets/original snapshots. Existing projection tests and legacy API byte assertions pass. Per-block composition uses the same renderer. No lossy conversion or in-place rewrite is claimed; C01 explicitly retains legacy editing until full conversion is representable. Layout identity test and selection observation show no calculation |
| AC-06 | Focused checks below, [independent review](review.md) and synchronized contract/UI/planning evidence |

Implemented subset: ANALYTICAL-DOC-001/002/004/014/015,
BLOCK-BUILDER-001/004/006/008, REPORT-001/018, CHART-001/002/010/013,
and bounded keyboard behavior relevant to A11Y-001/005. This is not full requirement,
accessibility or provider acceptance.

[Verification and repairs](verification.md) records the actual runs and inspected
screenshots. Presentation: **108 passed** (36 composer DTO, 9 service tests included).
Focused Web: **29 passed** across five files. Web TypeScript and new runtime Python
Ruff/strict Pyright passed. Owned PostgreSQL/API rehearsal: **1 passed, 9.86s**.
Browser: **3 passed, 30.0s**; expanded stale/lost-response/reconnect scenario then
**1 passed, 18.1s**. Chart compiler's unchanged **28 passed** C01 evidence is reused.
The local profile passed after documentation synchronization; receipt bindings are
validated again immediately before journal acceptance.

## Contract impact and continuation

API/schema and browser additions: **compatible-change** under explicit format
negotiation; existing endpoints retain their old payloads. Persistence expansion:
**compatible-change** after migration; using the new writer on the old CHECK is
incompatible and not supported. Downgrade with composed data is deliberately refused;
use forward repair or a pre-upgrade backup after an authorized operational decision.
Cache/identity: **none** to Analytics policy-aware identity; composer fingerprints
are grouping hints only. Authorization: **compatible-change**, new routes reuse
current ports and enforce creator/object/source checks. No production rollout proof.

Documentation synchronizes analytical-authoring contract v19, Web implementation
source contract v28, localized UI inventory, parent WS-004 v0.2.1/MS-006 links,
architecture/contributor indexes and redacted evidence. Prior bound snapshots remain
immutable. Forecasting, additional providers/profiles and later capabilities remain
held or scheduled by the accepted WS-004 plan.

After receipt-backed acceptance, continue to C03 (document structure and layouts)
through its own bounded milestone triad under the existing owner delegation.
