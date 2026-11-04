# WS-004 C01 entry audit — 2026-10-07

## Scope and verdict

Preparation for [WS-004 v0.1.0](../../../../docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md)
and its [169-requirement allocation](../../../../docs/architecture/planning/directions/DIR-004/workstreams/WS-004-requirements.md).
This is dated evidence, not a milestone, execution ledger, accepted schema design,
or C01 completion. Verdict: **Ready with changes for continued C01 investigation;
Not ready for new composition writes.** Workstream decomposition acceptance is
still unresolved. The owner was asked to select the C01–C11 sequence; no acceptance
is inferred from silence or from the handoff.

## Verified baseline

- Checkout: `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`.
- HEAD: `86055ce732640ebe68fd5415a55f7bbde3499181`; numerous tracked and untracked
  pre-existing working-copy changes are part of the observed baseline.
- `lsof` identified port 41746 listener PID 5502; its cwd was the checkout's
  `apps/web`. This proves the frontend process binding, not backend image identity
  or browser behavior.
- All seven fingerprints in WS-004 matched, including the machine specification
  digest `5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5`.
- Root and `.codex/AGENTS.md` read in both saved-project and serving checkouts.
- MS-004 machine record remains `awaiting_input`; S01–S04 are `accepted`, S05 is
  `needs_input`, `execution_allowed: false`, with an existing claim and owner
  acceptance question. Introductory prose saying no stage was claimed is stale;
  the machine record is authoritative. No journal was changed or resumed.
- Forecasting remains on hold in the project map and analytical authoring
  contract v17. C07 forecast/scenario acceptance cannot silently resume it.

## Plan assessment and concrete findings

| Area | Assessment | Evidence and consequence | Required next action |
|---|---|---|---|
| Goal, scope, ownership, reuse | OK | WS-004 names one Presentation composition model, provider ownership, old readers and concrete user scenarios | Keep these boundaries |
| Implementation baseline | OK, code-only | `ConfiguredWorkspace.tsx` has one `table` mode and one definition selection; `WorkspaceService.save` generates one page and metric-group blocks from cards | Introduce block-keyed authoring through the existing service seam, not a second UI-only store |
| Writable composition contract | Gap / High | `WorkspaceSaveRequest` accepts `ConfiguredReportV2`; there is no arbitrary composition input. `save` discards no submitted layout because the wire contract cannot submit one | Specify a separately dispatched authoring version and explicit conversion; prove all readers before activation |
| Closed schema safety | Risk / High before new writes | `Page.layout_mode` only accepts `flow`; `Block` admits arbitrary nested `source_binding` and `presentation` keys. DTO probe accepted a synthetic `library_options` key | Introduce closed typed bindings/presentation for the new writer; do not expose the existing loose Block DTO as a safe authoring API. No current API exploit is asserted |
| Stable hierarchy | Gap / High | V2 validator checks card bindings and report/metric identity, not a general page/section/block graph; current Save constructs the graph internally | Validate unique IDs, parent/destination existence, cycles, default page, reading order and cross-document references before accepting user graphs |
| Stage boundaries | Partial / Medium | C02 promises side-by-side independent blocks; broad layout/context/lifecycle work is allocated to C03/C04/C08 | C02 needs the minimum typed placement, local semantic input, CAS/idempotency, permission and old-reader proof. Later stages extend these; they cannot supply their first implementation after C02 |
| Scope and query identity | Gap / High | `_cards` uses common grain/calendar/context and selection-derived temporal alignment for all cards; only store overrides are card-local | Separate document save identity from normalized per-block result identity; test layout-only edits, local periods/grains and stale response isolation |
| Provider breadth | Unknown / High for complete target | Workspace Analytics DTO limits metrics to net revenue, receipt count and average receipt; population/action bindings are None. This does not establish the capabilities of all other providers | Inventory provider-specific normalized definitions and readiness before promising universal builder behavior; preserve Forecasting hold |
| Old snapshots and personal views | Partial / High | Dual readers, pinned saved views and exact artifacts exist; saved-view display still has one selection and chart/table representation | Add explicit old/new view and immutable snapshot fixtures; do not mutate old bytes or silently flatten unsupported documents |
| Concurrency and recovery | Partial | Repository locks document, checks creator, replays key/hash, checks document and saved-view revision, inserts version/view, rechecks authorization and advances latest in one transaction | Reuse these invariants; rehearse new-format crashes/replay/CAS on a disposable database |
| Verification and migration | Partial | Roadmap has the right scenarios, but no candidate schema/reader or new-format migration rehearsal exists | Bind concrete schema fixtures, API/DB/browser tests and rollback conditions to the selected milestone |
| Operations and delivery | N/A for current repair; unresolved for future writes | No runtime configuration, migrations, deploy, queues or notifications changed | Resolve alerts/runbook consequences when those surfaces are changed, not through a new platform |

Primary code evidence: [composition DTOs](../../../../packages/contracts/presentation/__init__.py),
[workspace DTOs](../../../../packages/contracts/presentation/workspace.py),
[public result port](../../../../packages/contracts/presentation/workspace_ports.py),
[workspace service](../../../../packages/presentation/application/workspace.py),
[repository](../../../../packages/presentation/infrastructure/workspace.py),
[API routes](../../../../apps/api/src/custometry_api/reports/workspace_router.py),
[editor](../../../../apps/web/src/features/reports/ConfiguredWorkspace.tsx).

## Initial requirement-to-code-to-proof audit

The full machine clauses, human explanation and UI sections 8.5.3–8.5.4 govern
these assertions. Each semicolon separates an independently required check;
evidence labels describe the observed subset, not completion of a compound MUST.
None of the following rows is a full-target acceptance claim.

| Requirement | Assertions and observed subset | Evidence strength / remaining proof |
|---|---|---|
| ANALYTICAL-DOC-001 | One versioned contract; all three profiles share semantics. V1/V2 composition exists, only workbook profile admitted | `code_observed`; cross-profile writer/reader parity missing |
| ANALYTICAL-DOC-002 | Stable node IDs; hierarchy; deterministic/reading order; fresh duplicate IDs. Pages/sections/blocks and card-copy remapping exist | `boundary_verified` only for contract copy tests; general graph and UI order unverified |
| ANALYTICAL-DOC-003 | dashboard, workbook_report, narrative_research; no active story enum. Current DTO admits only workbook_report | `code_observed`; other profile adapters missing from inspected DTO |
| ANALYTICAL-DOC-004 | Every specified block variant; reject SQL/executable HTML/library options. Existing Block union has four variants and loose nested dictionaries | `boundary_verified` for DTO probe only; typed new union and full write admission missing |
| ANALYTICAL-DOC-005 | Page reorder/duplicate/hide/lock/group; new revision; lineage; permissions preserved | `documented_only` at inspected authoring boundary; Save constructs one visible page |
| ANALYTICAL-DOC-006 | All five scopes; precedence; inheritance/locks; acyclic linked targets; normalized/effective identity; authorization | `code_observed` for document/workset/card DTO and store intersection only; hierarchy-wide resolver and DAG proof missing |
| ANALYTICAL-DOC-007 | Exact authorized version/page/block; access on open/return; origin/scroll/focus; no PII URL | `code_observed` for existing snapshot routes; full multi-page return/access flow unverified |
| ANALYTICAL-DOC-008 | Explore does not alter publication; version-pinned view; normalized filters; explicit personal/shared visibility | `code_observed` for SavedViewV1 owner/version/hash; no full personal/shared composer proof |
| ANALYTICAL-DOC-009 | No small universal cap; 100 x 30 benchmark; measured versioned resource policy | `code_observed` current v2 limits 20 worksets/50 cards per set/200 cards/1 MiB; these are not a general-document policy or scale proof |
| ANALYTICAL-DOC-010 | Authorized page index; active-page-only mount; bounded safe prefetch | `documented_only` for multi-page path; generated single page cannot prove this |
| ANALYTICAL-DOC-011 | Resolve all included blocks/scopes/segments; atomic immutable root; channel manifest reuse without duplicate compute | `code_observed` for draft artifact creation and atomic DB latest switch; publication/channel parity unverified |
| ANALYTICAL-DOC-012 | Hierarchy/order/meaning under RU/EN; tab overflow; keyboard; 200% zoom | `unknown` for new composer; no browser checks in this audit |
| ANALYTICAL-DOC-013 | Safe author and updated/version metadata; author pinned in manifest; Web/export equality | `code_observed` response author and saved_at; manifest/export parity unverified |
| ANALYTICAL-DOC-014 | Three layouts; independent modes/density; DnD and keyboard/menu; Undo/drop feedback; standalone table | `boundary_verified` current DTO rejects grid/narrative; remaining target requires new authoring model |
| ANALYTICAL-DOC-015 | Reader/Explorer/Author separation; mode switches preserve semantics; distinct save/apply/publish; zoom table access; creator restriction | `code_observed` creator checks and personal-view path; mode/zoom/publication scenarios unverified |
| BLOCK-BUILDER-001 | Common normalized creation across data blocks/profiles | `code_observed` card-based WorkspaceResults integration; general BlockDefinition and all profiles not established |
| BLOCK-BUILDER-002 | Three required stages in order; invalid state cannot preview/run | `unknown` at universal builder boundary; current new-report preparation is not this proof |
| BLOCK-BUILDER-003 | Conditional population requirement; reason/version/snapshot/policy | `code_observed` Card.population_binding is None; provider capability audit required |
| BLOCK-BUILDER-004 | Optional filters/comparison/presentation; meaningful defaults normalized | `code_observed` store/selection contracts; per-block defaults and all capabilities unverified |
| BLOCK-BUILDER-005 | Capability/permission/trust/cost/reuse preflight before Add/Run; explain outcome | `code_observed` authorization/materialization calls; full surfaced preflight unverified |
| BLOCK-BUILDER-006 | Guided/Advanced compile one versioned definition/runtime/result identity | `documented_only` for universal contract; schema selection is C01 output |
| BLOCK-BUILDER-007 | Resumable builder draft; excluded from result identity until commit; autosave no publication/compute | `unknown` for new builder; existing browser draft state is insufficient proof |
| BLOCK-BUILDER-008 | Explicit destination; stable block ID; compatible artifact reuse | `code_observed` result verification/reuse seam; arbitrary destination not writable |
| BLOCK-BUILDER-009 | Filtered/ratio trial; typed operands/unit/grain/null/denominator; backend validation; registry review/certification | `unknown`; three-metric workspace port does not establish generalized MetricRegistry authoring |
| REPORT-018 | Immutable creator plus functional/object/data permissions; grants/admin cannot replace creator; readers do not write definition | `boundary_verified` only for native-workspace/deny-wins unit tests; repository creator lock is code evidence; full real-role browser/API matrix not rerun |
| REPORT-019 | Shared set visible with report/data access; creator edits; personal values survive update; explicit adoption/reset; recheck old views | `code_observed` personal-only workset contract; shared-set completion must remain with WS-003 provider, not be assumed here |

The other **143 of 169** requirement rows retain their original `unknown pending
C01` audit status. They have not received clause-level code/proof assessment in
this entry investigation. In particular, CHART, FILTER, COMPARE, PIVOT, PARAM,
FOCUS, BRAND, REPORT-REFRESH, REPORT-PERF, A11Y, I18N, DASHBOARD and the other REPORT
clauses cannot be called implemented from these tests. Full clause splitting,
provider inventory and evidence binding remain required C01 work.

## Compatibility matrix

| Interaction | Classification | Evidence / required transition |
|---|---|---|
| Current v1/v2 models and generated readers | `none` for this test-only repair | No production model/client/persistence changes; 63 local tests pass after expectation repair |
| Put grid/narrative or arbitrary blocks into current v2 | `breaking-change` if represented as supported same-version payload | Current strict definition rejects blocks/unknown version; Page rejects non-flow. Preserve existing validators rather than silently relaxing them |
| New version-aware reader with old v1/v2 bytes | `unknown` for future composer | Existing dual-reader tests prove only current v1-to-v2 deterministic adaptation and preserved source payload; new reader does not exist |
| Old client with new server continuing old endpoints | `unknown` for future composer | Preserve original outputs and prove negotiation/errors; adding enum values is not automatically safe |
| Old reader with new-format persisted versions | `unknown` | No negotiated writer/schema or rollback exists. New documents must be preserved and explicitly unavailable to old clients, never downconverted by loss |
| Saved-view v1 with multiple independent selections | `breaking-change` if new meaning is sent in unchanged shape | ViewDisplay has one selection/representation. Need version dispatch and explicit adaptation |
| Result identity / reused jobs | `unknown` | `_cards` combines common context/grain and global temporal selection; distinguish document hash from analytical reuse key before adding layout |
| DB transaction / snapshot transition | `unknown` for extension | Current creator/CAS/idempotency/atomic pointer structure is reusable; new-format restoration/crash rehearsal not run |
| Browser block selection/settings | `unknown` until implementation | Intentional move from single-result to block-keyed behavior needs persistence and isolation scenarios U01–U03/U08–U12 |

Recommended engineering direction is an explicitly versioned extension using the
same repositories/ports and strict new authoring DTOs, with old readers retained.
No version number, schema or migration is accepted by this recommendation.
Actual rollout order: reader/schema preparation, old fixture parity, new/explicit
conversion writes, recovery/rollback rehearsal, then any authorized cutover.
No production migration or destructive backfill is part of this work.

## Next bounded result for owner review

Keep C01–C11 as proposed. C01 must deliver the remaining clause audit, actual
provider capability/hold inventory, selected versioned schema, positive/negative
fixtures, exact save/view/snapshot reader matrix and disposable migration/recovery
rehearsal design. This is an engineering result, not a UI release.

C02 then closes only on: four independently configured charts; two standalone
tables; side-by-side chart/table with a compatible shared result; add/copy/delete
with stable/fresh IDs; independent error/loading state; real API save/reopen;
creator/CAS/replay failures; unchanged old reports/views/snapshots. Minimum layout,
local query inputs, authorization and conflict checks are C02 prerequisites, while
full page tooling, hierarchy filters and publication remain their later increments.

After workstream selection, prepare the concrete milestone plan under the adopted
framework; milestone acceptance precedes executable pack/journal preparation.
Use one executor unless the owner selects another organization. Do not create
another mutable status source, claim old MS-004 or bypass a provider hold.

## Repair and observed checks

Only product-adjacent repair: [test_reports.py](../../../../tests/contract/presentation/test_reports.py)
now expects `/v2/new/prepare`, `/v2/new/apply` and `/v2/new/versions`. These routes
already exist in the router, generated OpenAPI and client. The failure occurred
before this turn's edits; diagnosis is a stale expected route inventory, not a
schema-generation failure. Exact route-set equality and all schema/client drift
assertions remain intact.

Working directory for checks is the serving checkout. Toolchain activated with
`source scripts/activate-toolchain.sh`; observed Node 24.18.0, pnpm 11.13.0,
uv 0.9.26. `--no-sync` prevents dependency installation during focused checks.

| Check | Outcome / proof boundary |
|---|---|
| `uv run --locked --no-sync pytest -q tests/contract/presentation tests/unit/presentation` before repair | 1 failed, 62 passed; only route inventory assertion failed |
| Same command after repair | 63 passed in 0.50s; contract/unit boundary, not DB/API/browser execution |
| `uv run --locked --no-sync ruff check tests/contract/presentation/test_reports.py` | passed |
| In-memory synthetic DTO probe using existing `definition()` fixture | v2 JSON round-trip passed; arbitrary blocks and v3 label rejected; flow accepted; grid/narrative rejected; loose Block nested library-options key accepted |
| `uv run --locked --no-sync python -m tools.check --scope local` | passed; static/source profile, not runtime or release proof |
| Documentation synchronization | architecture index v58 links this report; contributor index regenerated; WS-004/parent versions and its 169 allocations unchanged; 26 initial audit rows plus 143 remaining verified |
| `git diff --check` | passed across the observed working copy |
| Real DB/API/browser and migration/rollback | not run; this entry audit adds no writer; future checks require an isolated disposable target and synthetic reports |

The integration fixture performs teardown writes and must only run through its
owned disposable-database harness, never against the retained local report.
No user data, sessions, credentials, runtime payloads or screenshots were saved.
No publication/deployment, independent security review or full C01 closure claimed.
