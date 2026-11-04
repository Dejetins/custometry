# WS-004 complete clause inventory — C01

Source: [machine blueprint](../../../../../custometry-technical-blueprint-ru.md),
SHA-256 `5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5`.
Allocation: [WS-004 matrix](../../../../../docs/architecture/planning/directions/DIR-004/workstreams/WS-004-requirements.md).
This is an evidence inventory, not a second execution ledger or implementation percentage.
Every semicolon separates an assertion requiring its own eventual acceptance evidence;
conjunctions inside an assertion retain all named checks. Normative MUST/MUST NOT,
SHOULD and MAY come from each exact source clause; optional behavior is not upgraded.
The observed subset never satisfies an entire compound clause automatically.

## Search boundary and source keys

Current checkout is c67c at the entry-audit fingerprints. Read machine clauses and
human explanations, then inspect actual packages/apps/tests. Named-contract search
across packages and apps found no implemented PivotSpec/PivotResult,
AnalyticalTemplateVersion/ResolvedParameterSet, general BlockDefinition or
filter_targets contract. This bounded search is evidence of a missing located
provider, not proof that arbitrary external code does not exist. Runtime capability
for those providers is `unknown` until owner-port implementation and proof exists.
No guessed provider values, latency budget or forecast resumption is introduced.

| Key | Current source / observed boundary |
|---|---|
| C | `packages/contracts/presentation/__init__.py`, `workspace.py`; generated v1/v2 composition, one selection, loose nested Block; `tests/contract/presentation` |
| P | `packages/presentation/application/workspace.py`, `infrastructure/workspace.py`, `application/reports.py`; creator/CAS/replay, immutable draft snapshots and personal views; `tests/unit/presentation` |
| A | `packages/contracts/analytics/workspace.py`, `packages/analytics_core/application/workspace_service.py`, `workspace_calculation.py`, `domain/model.py`; three-metric retail provider and flat typed filters; `tests/unit/analytics`, `tests/contract/analytics` |
| I | `packages/identity_access/application/resource_access.py`, Presentation guard and row-policy intersection; `tests/unit/presentation/test_workspace_access.py` |
| W | `apps/web/src/features/reports/ConfiguredWorkspace.tsx`, `WorkspaceProjection.tsx`, `FilterPrototype.tsx`, `workspace-presentation.ts`; current single-result UI, not arbitrary composition |
| E | `packages/chart_compiler_ts/src/line.ts`, `src/index.ts`, `tests/line.test.ts`; canonical daily-line subset. WorkspaceProjection builds options separately; no full shared Web/SSR compiler proof |
| X | `apps/web/src/features/reports/result-export.ts`, `ResultExportMenu.tsx`; browser result-table export, not immutable multichannel document render |
| B | `packages/presentation/infrastructure/system-brand.v1.json`, contracts SystemBrandProfileV1/SystemCompanyPackV1, `packages/ui-foundation/src/report-theme.ts`; bundled initial branding only |
| L | `apps/web/src/i18n.ts`, `packages/localization/src/index.ts`, catalogs and parity tests; English fallback and RU catalogs, component locale branches still present |
| R | `apps/api/src/custometry_api/reports/prepared.py`, `runtime_policy.py`, `packages/artifacts/infrastructure/document_snapshots.py`, W39 evidence; prepared bounded reads, not new multi-page scale or full refresh lifecycle |
| T | `docs/contracts/analytical-authoring-contract.md`, `report-refresh-serving-recovery-contract.md`, context map; accepted targets, not implementation proof |

Executed at this baseline: Presentation contracts/units 63 passed, Analytics
contracts/units 51 passed, shared line-compiler 28 passed. Other named tests are
located candidates, not rerun evidence. Browser, real DB, SSR, delivery, accessibility
and scale checks are not performed by this inventory. Existing W39/W40 proof remains
historical and build-bound. All generic-provider gaps have a named owner below.

## Initial 26 clauses

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

These initial rows retain their entry-audit observations. Provider ownership: ANALYTICAL-DOC belongs to Presentation/Web with Identity and Artifact ports; BLOCK-BUILDER belongs to Analytics/Semantic Model with Presentation integration; REPORT-018/019 belongs to Presentation/Identity and WS-003 shared-set outputs. Newly implemented C01 schema evidence is recorded separately in the final stage report rather than rewriting baseline observations.

## FILTER — Semantic Model / Analytics; Presentation/Web integration

All rows are `code_observed` only for the A/W bounded store or flat-filter subset;
full registry/expression capability is `documented_only` in T, runtime `unknown`.
Do not equate the FilterPrototype or basic store picker with the target evaluator.

| Requirement | Independently required assertions | Current evidence / missing proof |
|---|---|---|
| FILTER-001 | Versioned typed tree only; no arbitrary SQL/string input | A has flat typed predicates; general tree and version dispatch missing |
| FILTER-002 | Authorized catalog search by ID/entity/localized labels/description/type; no forbidden-field disclosure | W store picker only; registry search and denial cases missing |
| FILTER-003 | Backend typed operator/value; versioned null/hierarchy/relative-date validation | A validates categorical/numeric operators; registry policies unverified |
| FILTER-004 | Normalize expression and registry/hierarchy/calendar versions; anchor/timezone/defaults in spec/manifest/request/cache | A workspace normalizer includes bounded period/calendar/store policy; full tree dependencies missing |
| FILTER-005 | Apply workspace/object/row/PII before facet aggregation/pagination/search | I validates bounded scope; generalized facets/count non-disclosure unverified |
| FILTER-006 | Adapter-declared safe pushdown; otherwise typed execution and volume preflight | A has analytical implementations; generic expression planner capability missing |
| FILTER-007 | Search-only or bounded lookup for high cardinality; never full distinct browser load | W receives store list; high-cardinality contract/limits unverified |
| FILTER-008 | Show applied/default/locked filters, grain and estimate; hidden business rule must be versioned | W displays current controls; registry-wide effective set and origin proof missing |
| FILTER-009 | Draft local Focus filters isolate parent; explicit apply; reset inherited state; undo | W Focus renders current result; independent filter draft/undo missing |
| FILTER-010 | Reauthorize/revalidate apply; normalize identity; expose and preserve system/locked restrictions | P/I bounded apply checks exist; general locked-expression proof missing |
| FILTER-011 | Searchable entity catalog; AND/OR and nested same-container scopes; readable expression before apply | W prototype is not authoritative; correlated evaluator/UI integration missing |
| FILTER-012 | Separate draft/applied/optional estimate; estimate permission-filtered; reauthorized normalized apply | A/W current apply is bounded; generic estimate schema and stale handling missing |
| FILTER-013 | Versioned relationship exists/not_exists; explicit parent/child predicate scope; same-object correlation; no arbitrary joins/member multiplication | A flat FilterPredicate cannot express this; public provider contract absent in bounded search |
| FILTER-014 | Pin scope/row/window/metric-or-count/grain/unit/null/returns/operator; ratios pin operands/denominator; complete empty count zero; unknown never zero | A retail ratio/count tests pass only for fixed metrics; scoped aggregate provider missing |
| FILTER-015 | Ordered signed steps/event versions/time/windows/gaps/property-session/tie policy; strict equal-time behavior; complete interval for absence | T target only; sequence evaluator/history provider missing |
| FILTER-016 | matched/not_matched/unknown; NOT/AND/OR three-valued logic; certified absence evidence; no unknown confirmed membership | A current result states are not this membership logic; completeness provider and truth-table tests needed |
| FILTER-017 | Validate typed scopes/cardinality/capabilities; one normalized planner; preserve v1; reject lossy downgrade; identity pins versions/dependencies | A supports bounded flat subset; v2 reader/planner/downgrade tests missing |
| FILTER-018 | Versioned depth/steps/fanout/cardinality/work limits; blocker before run; exact versus estimate; cancellation/stale protection; no browser/row-Python bypass | Current workspace limits exist; general policy and planner admission missing |

## COMPARE — Analytics / Semantic Model; Presentation integration

`code_observed` for A's retail temporal/pair comparison. Executed analytics tests
prove their exact fixed-provider cases only. Generic population/time-v2 and
multichannel parity remain `documented_only` / runtime `unknown`.

| Requirement | Independently required assertions | Current evidence / missing proof |
|---|---|---|
| COMPARE-001 | Explicit TimeComparisonSpec or none; no hidden shift | A has TimeComparison and workspace alignment enum; all reportable providers unverified |
| COMPARE-002 | Leap day; ISO week 53; fiscal/timezone/calendar version | A calendar and workspace tests pass; complete mode/calendar matrix missing |
| COMPARE-003 | Explicit incomplete-period policy; no silent full prior period | A old comparison policy and clipped buckets observed; all modes unverified |
| COMPARE-004 | Current/prior values; absolute/relative delta; coverage/status; missing not zero | A typed deltas/states and tests exist; other metric/provider behavior unverified |
| COMPARE-005 | Immutable comparison; both periods/timezone/policy/metric/activity/segment/dataset/filter versions; incompatible definition blocks or audited rebase | A bounded artifact refs exist; segment/activity/rebase combinations missing |
| COMPARE-006 | Independently check both periods' history/DQ/access/definition | A verify/compare rechecks results; universal capability preflight missing |
| COMPARE-007 | Same mode/limitations/artifact in Web/email/XLSX | W/X bounded browser exports; shared static/delivery provider missing |
| COMPARE-008 | Shared defaults; optional explicit per-block override; resolved spec in request/cache/snapshot | P uses global grain/calendar/selection; new local semantic seam required |
| COMPARE-009 | Calendar-aligned month/quarter/year across tabs; exact snapshot pair/coverage/compatibility per block | A six-grain retail subset; segment migration/size provider integration missing |
| COMPARE-010 | Grain changes boundaries/reduction/point count; chart/table/export same buckets; backend production reduction | A buckets, W shared projection; arbitrary datasets and full export proof missing |
| COMPARE-011 | previous_period/custom_period v2; calendar-bucket or local-day resolution; visible DST/overlap/incomplete policy; unchanged v1 | A workspace enum only none/previous_year_same_dates; explicit new provider version required |
| COMPARE-012 | same_population versus pair; pin memberships/time basis; disclose changed axes/overlap/universe; no disjoint/causal fiction | No matching public PopulationComparisonSpec found; Analytics/population provider blocks acceptance |
| COMPARE-013 | Typed deltas; percentage points separate from relative percent; zero/unknown denominator reason; disclose coverage/definition differences | A zero-base reason and fixed metric deltas; rate/percentage-point and population matrix missing |

## PIVOT — Analytics / MetricRegistry; Presentation/Web projections

All six rows: `documented_only` in T; public PivotSpec/PivotResult not located in
packages/apps search. Existing retail tables and ratio tests are reusable inputs,
not proof of generalized pivot behavior.

| Requirement | Independently required assertions | Provider / next proof |
|---|---|---|
| PIVOT-001 | Versioned BlockDefinition PivotSpec; ordered dimensions/measures/totals/sort/top-N/calendar/cell states; stable semantic keys/grain/provenance/coverage; no renderer formulas/SQL | Analytics strict spec/result schema and invalid fixtures |
| PIVOT-002 | Full authorized backend totals at target grain; recomputed distinct/ratio/semi-additive; no sum-visible/average-percent/header duplication; top-N basis | MetricRegistry + Analytics golden totals and privacy cases |
| PIVOT-003 | Seven explicit cell states; age/denominator/completeness/limitations survive export; no suppressed inference or zero substitution | Analytics/DQ/Identity cell-state and totals attacks; channel parity |
| PIVOT-004 | Expand/collapse, multiple measures, shelves/transpose/pinning/typed formatting; display changes preserve identity; new grouping validated/new result | Analytics grouping seam then Web keyboard/identity checks |
| PIVOT-005 | Bounded projection/virtualization/preflight; viewport not canonical cap; loading/partial/error/last-good/cancel/fallback; same snapshot and explicit overflow | Analytics/Execution limits plus real large-result browser/channel evidence |
| PIVOT-006 | Absolute and registered rate/cumulative; exact denominator/origin/age; explicit comparable-age basis; distinct source/total/hidden-level keys | Analytics typed provenance and drill/annotation/selection fixtures |

## PARAM — Presentation templates and interactions; Semantic Model / Analytics

All five rows: `documented_only` in T. Generic template/parameter contracts were
not located. Prototype controls do not establish typed persisted template behavior.

| Requirement | Independently required assertions | Provider / next proof |
|---|---|---|
| PARAM-001 | Stable typed parameter IDs/labels/required/default/range/capability/targets; period/filter/metric/population refs; published refs and per-resolution authorization | Presentation schema; Semantic Model allowed-value discovery and Identity denial tests |
| PARAM-002 | Type-compatible destination mapping/inheritance/override; no lock relaxation; deterministic resolution; reject missing/invalid/unused/cyclic targets | Presentation resolver plus whole-graph negative fixtures |
| PARAM-003 | Pin template/definition/default-origin/values/windows/targets/policy in identities; display preferences separate; compatible reuse across pages | Presentation/Analytics identity and reuse tests |
| PARAM-004 | Draft/validated immutable template/linked pinned instance; explicit upgrade diff/new draft; independent copy lineage/fresh IDs; isolated personal defaults | Presentation version/CAS/upgrade tests and real reopen |
| PARAM-005 | Allowlisted highlight/filter_targets/drill/navigate; semantic keys/typed mappings; show target set/effective filters; highlight no compute; return history; no loops/lock/access bypass | Presentation/Web dispatcher and Analytics drill/Identity targets; network/history/denial proof |

## CHART — Presentation compiler and renderer; Web / Report Delivery consumers

`code_observed` for E/C/W bounded subsets unless explicitly noted. Full static
render/delivery and richer chart providers were not located; no SSR/PNG/email
proof is inferred from the 28 passing canonical-line tests.

| Requirement | Independently required assertions | Current evidence / remaining proof |
|---|---|---|
| CHART-001 | Product ChartSpec sole canonical source; options/images/workbook charts derived | C/E v1 exists; W v2 directly constructs options and needs convergence |
| CHART-002 | Immutable content addressing; schema/data/compiler/build/renderer/font/theme/locale/timezone/profile manifest identity | P/B store versioned refs; complete render identity invalidation unverified |
| CHART-003 | Source/schema/grain/counts/dimensions/measures/units/reduction/comparison/access; no client metric logic | C/E line subset validates metadata; v2 and all chart types need shared contract proof |
| CHART-004 | ECharts only; allowlisted compiler adapter | W uses ECharts; v2 options bypass E package; shared compiler amendment required |
| CHART-005 | No production Dash dependency/runtime/routes/state/callback | No Dash package match in inspected manifests/locks; full packaged-runtime exclusion unverified |
| CHART-006 | No core Plotly through v1; optional later trusted plugin only | No Plotly package match in inspected manifests/locks; future plugin not active |
| CHART-007 | Separate versioned range_timeline type; no timeline-frame substitution | C range_timeline is None; type/provider missing |
| CHART-008 | Planned/actual windows, lanes/audience, overlap/density, window fetch/detail; descriptive overlay only | Promotion projection and range renderer unavailable in inspected path |
| CHART-009 | One immutable compiler build for Web/SSR; no metrics in compiler; identical normalized input gives same hash | E daily-line package present; W v2 divergence and SSR consumer missing |
| CHART-010 | Reject options/callback/HTML/CSS/arbitrary URL/regex; trusted IDs for special renderers | E validates exact nested line subset; broader C Block is loose; strict new fields required |
| CHART-011 | SVG/Canvas via versioned measured policy; identical semantics and query identity | W registers SVG; measured selection-policy/Canvas parity missing |
| CHART-012 | Bounded embedded SSR inside report worker; no separate service/default Chrome | No report-worker implementation located in apps inventory; renderer provider required |
| CHART-013 | Email PNG from deterministic SVG; lossless native XLSX or same PNG plus typed sheet | X browser XLSX is not this pipeline; shared export provider missing |
| CHART-014 | Semantic style roles; no raw theme in business spec; render manifest pins theme/profile | E semantic roles exist; W hardcoded options and full render manifest unresolved |
| CHART-015 | Localized meaningful summary, units/limitations, accessible table; non-pointer meaning | E/W table and aria subset; all charts and full summary/a11y proof missing |
| CHART-016 | Bounded chart artifact; backend aggregation/sampling/LOD; authorized window fetch | A server buckets; E 366-day subset; general LOD/window admission missing |
| CHART-017 | No GL/WebGL/GPU analytics through v1; no browser reduction bypass | No corresponding dependency in inspected manifests; runtime/full bundle proof pending |
| CHART-018 | Static no-network/assets; bounded batch/dimensions/output/temp/CPU/memory/time; cancel/error/crash cleanup | Static provider absent in inspected apps; no fabricated operational proof |
| CHART-019 | Release validation/security, compiler hash parity, SVG/Canvas, raster fidelity, font invalidation, timeline/XLSX/theme/golden parity | E unit tests only; complete release gate not run or ready |
| CHART-020 | Versioned semantic style/palette/contrast/type/density; report default and optional block override; snapshot/render identity; Settings builder | B fixed system branding; user template lifecycle/override/Settings absent from located path |
| CHART-021 | Per-bucket connectors/delta series; presentation-only visibility; artifact values/units/reasons; no infinity/null bridge; table/tooltip deltas; bounded labels; trusted spec | W implements bounded connectors and backend deltas; shared typed compiler and complete semantic parity required |

## FOCUS — Presentation/Web; Analytics and Identity filter/read ports

All rows `code_observed` for the W modal single-result subset. No new browser
acceptance claimed; generic Focus/filter/large-table behavior remains unverified.

| Requirement | Independently required assertions | Current evidence / next proof |
|---|---|---|
| FOCUS-001 | Every authorized chart/table/timeline opens viewport Focus; retain binding/comparison/access/context | W focus modal exists; multiple block anchors/timeline missing |
| FOCUS-002 | Title/period/correct comparison axes; all filters/Trust/export/close | W export/close subset; complete contextual header and policy filters unverified |
| FOCUS-003 | Search every allowed registry field; no forbidden field/facet/count/existence | General FilterFieldRegistry provider missing |
| FOCUS-004 | Isolated local draft; explicit apply/reset/undo; parent unchanged before apply | W uses same definition; separate Focus draft lifecycle needed |
| FOCUS-005 | Backend validation/access/identity on apply; backend compute with common progress/ETA | P/A bounded apply exists; generalized Focus/progress integration missing |
| FOCUS-006 | Only allowlisted legend/zoom/pan/brush/drill; reset view; no client analytics/reduction | E interactions largely disabled; richer typed capability path missing |
| FOCUS-007 | Columns/sort/density/pinning/pagination; server access/bounds/PII | W simple complete table; generic bounded server projection missing |
| FOCUS-008 | Chart/table retain same binding/comparison/filter/grain/units/access/freshness/trust; disclose differences | W shared projection observed; exact per-block runtime and export parity pending |
| FOCUS-009 | Close/Escape/Back restore route/block/scroll/focus/parent edits; explicit local-draft discard | W close/Escape callback observed; browser history and dirty local draft cases pending |
| FOCUS-010 | Keyboard/focus/names/non-hover/summary/table/200%; trap only modal | W modal trap and table observed; real keyboard/screen-reader/zoom checks missing |
| FOCUS-011 | All loading/empty/filter-empty/warning/degraded/blocked/failed/forbidden/stale/partial states remain usable | W limited flags; full state matrix missing |
| FOCUS-012 | Ephemeral presentation default; no query/cache impact; persistence only versioned view; semantic filters obey identity | W local flags/P saved views observed; all controls need query-count/identity proof |

## DASHBOARD — Presentation dashboard profile; Identity / Research / Collaboration

`documented_only` in T for target dashboard authoring: C currently restricts profile
to workbook_report. Reusable report/Identity seams are not evidence of dashboard
publication, policy-safe omission or collaboration provider readiness.

| Requirement | Independently required assertions | Provider / next proof |
|---|---|---|
| DASHBOARD-001 | Immutable published version; layout/widget edits new version | Presentation dashboard lifecycle/readers and immutable DB proof |
| DASHBOARD-002 | pinned_result or latest_successful_by_spec; visible policy/resolved artifact | Presentation/Analytics capability and resolved snapshot tests |
| DASHBOARD-003 | Validate global/local filters against source; persist reproducible spec | Analytics/Semantic resolver plus dashboard integration |
| DASHBOARD-004 | Intersect dashboard/artifact/PII access | Identity denial and revoked-artifact dashboard tests |
| DASHBOARD-005 | Widget and document stale/degraded/failed/missing; no false new data | Per-block projections and last-good policy scenarios |
| DASHBOARD-006 | Keyboard equivalent for every DnD operation | Web complete authoring keyboard browser proof |
| DASHBOARD-007 | Sections/heterogeneous blocks; deterministic overview-to-detail order | Shared composition and profile adapter; graph/read-order proof |
| DASHBOARD-008 | Published metric-group version or versioned override; same group/metric order across channels | Semantic Model group provider + shared snapshot renderer |
| DASHBOARD-009 | Evidence-linked versioned findings/conclusions; separate viewer discussion | Research/Collaboration ports missing from inspected path; no fake findings |
| DASHBOARD-010 | Explicit access-management permission; author/publish does not grant ACL rights | I reusable policy; dashboard grant/revoke API and role matrix |
| DASHBOARD-011 | Authorized omission/replacement; no existence/values/labels via gaps/comments/counts/export | Policy-safe page projection and adversarial multi-channel tests |
| DASHBOARD-012 | Authorized snapshot/block comments; exact immutable deep link | Collaboration/Presentation provider and revoked-link tests |

## REPORT — Presentation / Artifact Lifecycle / Rendering / Identity

`code_observed` for P/C/B/I/R bounded draft workflows; publication, render-worker,
delivery and general content are not established. REPORT-018/019 appear above.

| Requirement | Independently required assertions | Current evidence / missing proof |
|---|---|---|
| REPORT-001 | Published definition immutable; any block/binding/layout/theme edit new version | P immutable draft versions; publication lifecycle not implemented by this seam |
| REPORT-002 | Every block resolves all source/projection/filter/metric/comparison/chart/schema/count/unit/lineage/PII; pin locale/timezone/currency/theme/render contract | C/P bounded saved payload; arbitrary block and render envelope missing |
| REPORT-003 | Same snapshot/spec/data for Web/email/XLSX; no DOM/options/recompute/channel formulas | P snapshots + E line contract; X uses browser table export, not full document pipeline |
| REPORT-004 | Declare schema/grain/count/unit/format/lineage/PII per data block | A result metadata observed; new per-block projection contract required |
| REPORT-005 | Intersect report/source/row/object/PII/export; recheck before render/download/send | P/I read/save guards; all export/send paths and revoke not verified |
| REPORT-006 | Render manifest/hash/renderer/version/size/retention/snapshot reference | R document artifact manifests only; rendered artifact lifecycle absent in inspected worker inventory |
| REPORT-007 | Analytics/forecast/dashboard/DQ reportability; exclude Operator/Admin telemetry | A retail result available; forecast hold and other provider gaps block full union |
| REPORT-008 | Trust includes as-of/freshness/DQ/filters/comparison/limitations/lineage | A trust and P bindings exist; per-block/channel UI fidelity pending |
| REPORT-009 | Async render preflight/cancel/progress/ETA/resources/idempotency/errors | Execution infrastructure exists; report renderer application port/consumer not located |
| REPORT-010 | Policy cleanup only rendered artifacts; retain definitions/snapshot metadata/redacted audit | Artifact infrastructure alone not proof; retention teardown and immutable history tests needed |
| REPORT-011 | Ordered sections/metric groups/findings/conclusions/methodology/narrative and chart/table | C four block variants; Research content provider and full union missing |
| REPORT-012 | Pin BrandProfile/CompanyPack; all channels/docs same local corporate identity | B/P pinned initial refs; multichannel rendering unverified |
| REPORT-013 | Mutable comments excluded by default; approved summary separate versioned block | No Collaboration integration located; snapshot-content exclusion must be explicit |
| REPORT-014 | Access administration/author/send/PII permissions independent | I/P creator/access checks; complete grant/send/PII matrix missing |
| REPORT-015 | Exact cell/result/version; retain metric/filter/period/population; separate row grant before query/count/export; ratio/distinct reconciliation; safe aggregate fallback and return | No general drill-through provider located; A aggregate explanation is insufficient |
| REPORT-016 | Exact authorized revision diff; separate data/definitions/population/policy/presentation; mixed/unknown without causal invention; denied versions leak nothing | P versions exist; semantic diff service/UI unavailable in inspected path |
| REPORT-017 | Pre-publish block/semantic/value/dependency diff; same inputs no fake delta; compute preflight/access; immutable publications/no auto re-anchor | General publication/diff provider missing; C08 acceptance blocked on real implementation |

## REPORT-REFRESH — Presentation / Scheduler / Execution / Artifacts / Identity

All rows `documented_only` in T for full lifecycle. W automatic local calculation
and R prepared reads are different capabilities. Neither implements document
refresh policies, durable demand or published current-pointer fencing.

| Requirement | Independently required assertions | Provider / next proof |
|---|---|---|
| REPORT-REFRESH-001 | Versioned mode/cron/IANA/status/due/evaluations; specified defaults per profile; preserve definition/snapshot; blocker on invalid inputs | Presentation policy DTO/repository and Scheduler schedule integration |
| REPORT-REFRESH-002 | Verified-ingestion trigger; durable due occurrence; wait/re-evaluate inputs; no early run/fake refresh; periodic identity; existing scheduler/outbox semantics | Execution/Scheduler event and durable occurrence tests |
| REPORT-REFRESH-003 | Fixed published definition; resolve exact inputs; authored changes require version; pinned stays pinned; new root/page snapshot; old references retained | Presentation/Artifacts immutable refresh fixtures |
| REPORT-REFRESH-004 | Coalesce durable demand per document/policy; latest consistent generation; existing single-flight; bounded fairness/progress/lag | Execution concurrency/race tests under sustained updates |
| REPORT-REFRESH-005 | Required block readiness/manifests/DQ/access/partial policy; atomic PostgreSQL current; revisions/fencing/monotonic generation; old late run cannot roll back current; failure preserves good | Presentation transaction/fencing tests on disposable DB |
| REPORT-REFRESH-006 | Viewer pinned until explicit update; freshness/progress/available version; preserve compatible context; latest normal open/exact deep link; last-good policy/current access/revoke | Presentation serving + Web two-session/revoke/update tests |
| REPORT-REFRESH-007 | Separate availability/integrity/freshness/execution; full states; updated not proof of freshness; no false corruption; safe reason/action | R/P stable errors reusable; full lifecycle and UI error-state matrix missing |

## BRAND — Presentation / Semantic Model / Admin Web

`code_observed` for B/P initial system profiles; configurable branding lifecycle
and channel-wide proof remain missing. No additional asset or external network
access is authorized by this audit.

| Requirement | Independently required assertions | Current evidence / next proof |
|---|---|---|
| BRAND-001 | Immutable profile; token/contrast/asset/MIME/dimensions/safe-channel validation | B fixed profile, not general validator; negative asset/contrast fixtures |
| BRAND-002 | Content-addressed bundled PNG or sanitized SVG; no script/external/font/filter/executable abuse | Bundled assets exist; general admission/sanitizer evidence missing |
| BRAND-003 | All named product surfaces resolve one pinned profile | B current report subset; login/email/docs/XLSX parity missing |
| BRAND-004 | Semantic tokens only; no CSS/HTML/JS/customer fork | B/E bounded typed data; configurable override validator not located |
| BRAND-005 | Admin previews/validation/diff/impact/publish/rollback/reset | No general brand admin implementation located; lifecycle and channel preview proof |
| BRAND-006 | Snapshot pins brand version/asset hash; later brand does not rewrite history | P refs observed; actual historical multichannel artifact test missing |
| BRAND-007 | Pack schema/version/hash/preflight/diff; exclude secrets/data/PII/keys | C system CompanyPack only; import/export allowlist and leak tests needed |
| BRAND-008 | Stable icon IDs/labels; bundled fallback; unknown IDs do not break navigation/render | Existing pilot symbols; general pack fallback/label policy unverified |
| BRAND-009 | Branding cannot change auth/domain/values/run identity/legal notices | No new theme behavior here; full identity and license preservation test required |

## I18N — Localization / Web / Rendering providers

`code_observed` for L/W/E/X. English fallback and RU catalogs exist, but locale
conditionals in components violate the target generic-locale architecture; parity
of today's keys does not establish completeness of all shipped text or new locale.

| Requirement | Independently required assertions | Current evidence / next proof |
|---|---|---|
| I18N-001 | English default/fallback; complete RU for UI/backend texts | L config correct; whole-product coverage not established |
| I18N-002 | Pinned namespaced adapter/interpolation/plurals/fallback/pseudolocale; no product locale branches | L i18next present; W/E branch on locale; refactor/canary needed |
| I18N-003 | Backend presentation uses gettext/Babel | General rendering provider absent in inspected path; catalog/format integration needed |
| I18N-004 | Stable codes/params in API/logs/audit/manifests/events; translation at presentation | P/A stable errors observed; full event/log boundary unverified |
| I18N-005 | Live language switch without login; preserve values/calendar/run/artifact/cache identity | L/W switch and E locale test; browser/network/identity proof for new composer pending |
| I18N-006 | Independent language/format_locale/timezone/currency | W mostly coupled locale formatting and A UTC/EUR subset; generalized settings/identity missing |
| I18N-007 | Canonical CSV headers default; optional localized plus metadata; canonical Parquet/JSON | X serializer accepts arbitrary rows; full canonical-header/default metadata contract unverified |
| I18N-008 | Registry/catalog/gettext/builtins/parity/pseudolocale/E2E permit new locale without domain edits | L two-language constants/branches; extensible registry pipeline missing |
| I18N-009 | CI placeholder/plural/en-ru coverage; release missing-key error | Localization parity/source gate exists; complete release missing-key behavior unverified |
| I18N-010 | CSS logical properties; registry direction even before RTL shipping | W scoped CSS and no established direction registry; reflow/RTL fixture required |
| I18N-011 | Isolated plugin namespace; required English and official/bundled Russian | No runtime plugin translation integration located; provider-specific admission required |

## A11Y — Web / UI foundation / QA

`code_observed` for W individual labels, table headers, Focus trap and reduced
motion. No browser or screen-reader conformance claim; remaining assertions need
real interaction, including new multi-block modes and layouts.

| Requirement | Independently required assertions | Current evidence / next proof |
|---|---|---|
| A11Y-001 | Every function keyboard-operable; visible logical focus | W selected controls only; full scenario keyboard traversal |
| A11Y-002 | Add/connect/move/reorder/delete equivalent to dragging | Future multi-block editor commands; browser equivalence assertions |
| A11Y-003 | Text/icon/pattern beyond color; WCAG 2.2 AA contrast | W labels and semantic classes; all themes/state contrast not measured |
| A11Y-004 | Programmatic labels/instructions/field errors; submit focus error summary | W labels subset; new builder error-summary and invalid-input flow |
| A11Y-005 | Appropriate non-noisy live announcements for progress/completion/notifications | W role=status subset; real screen-reader async-state sequence |
| A11Y-006 | Localized summary/units/limitations/table; no hover/pointer/color-only meaning | W/E table subset; meaningful multi-series summaries and exact values |
| A11Y-007 | Header associations; keyboard grid; sort/filter announcements; virtualization accessibility | W semantic th scope; no general virtual grid evidence |
| A11Y-008 | Usable 200% reflow; reduced motion | W matchMedia reduced motion observed; multi-layout zoom test pending |
| A11Y-009 | RU/EN accessible-name parity | W localized names; whole control catalog and missing-key assertions |
| A11Y-010 | CI automated a11y; release keyboard/screen-reader smoke | Source QA infrastructure only; actual release/manual checks not performed |

## REPORT-PERF — Presentation serving / Execution admission / runtime QA

`code_observed` for R prepared reads and historical W39 measured subset. Full
performance acceptance remains `unknown`; no measurements are extrapolated.

| Requirement | Independently required assertions | Current evidence / next proof |
|---|---|---|
| REPORT-PERF-001 | Instant-feeling prepared open; active workload 1–50 analysts/1–100 readers including 50+100 with refresh; shared CPU/memory/IO admission and fairness; no arbitrary-hardware promise | W39 p95 evidence is its own build/workload only; agreed mixed-load hardware/corpus/resource profile required |
| REPORT-PERF-002 | Authorized snapshot and bounded page reads; reuse/no equivalent source scan; explicit compute for new filters/drill; cold/warm/hot active-page/filter/lag/percentiles/throughput/resources/bytes/duplicate work; agree numeric budgets/hardware/distribution/profile first | R request-read optimization exists; multi-page instrumented benchmark and owner-selected performance budgets required before C10 acceptance |

## Dependency conclusions and continuation

C02 may use the proven bounded retail provider to deliver independent chart/table
blocks, with truthful capabilities. It must not advertise Pivot, general filters,
parameters, full publication/delivery or Forecasting merely because a slot exists.
Shared worksets remain WS-003's provider obligation. Missing provider code is an
implementation dependency to resolve through existing owner boundaries, not a
reason to stop independent composition work or claim completion with mocks.

Forecasting hold remains a hard limit on forecast/scenario functionality. Numeric
performance budgets and reference hardware/workload remain a material owner choice
before performance acceptance; no such choice is needed for the C01 schema or C02
vertical slice. Release, external delivery and production migration are outside
current authority. Every unmet assertion above stays open for its assigned later
outcome; finishing this inventory does not mark its product requirements complete.
