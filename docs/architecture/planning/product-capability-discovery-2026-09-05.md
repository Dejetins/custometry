---
doc_id: ARCH-PRODUCT-DISCOVERY-001
title: Product capability discovery for segmentation and analytical authoring
doc_version: 2
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: product
requirement_ids: [FILTER-001, SEGMENT-001, SEGMENT-019, BLOCK-BUILDER-001, ANALYTICAL-DOC-001, COMPARE-001, METRIC-001]
status: accepted
source_commit: d5ecbd33c1fd582058ec3514e2084820c8a3f1c2
proof_boundary:
  label: comparative-product-research-and-requirement-gap-analysis
  exclusions: [ implementation-readiness, production-code-audit, forecast-resumption, release-authority]
---

# Product capability discovery for segmentation and analytical authoring

## Purpose and evidence boundary

The owner corrected the earlier narrow three-condition segment example and card-oriented report example. The requested work is to investigate Mindbox and adjacent products, inspect an existing compact HTML report, and identify valuable missing or incomplete requirements. No new prototype is requested. Forecasting remains on hold. The first external release scenario remains undecided; showing interest in reports and segments does not accept a permanently restricted product scope.

The findings and coverage labels below preserve the pre-adoption research baseline. Candidate labels remain research references, not execution IDs. The owner subsequently approved the core ideas; the adoption note links each accepted capability to normative requirements and retains the explicitly optional expansions separately.

Evidence collected on 2026-09-05:

- Official public documentation for Mindbox, RetailCRM, Amplitude, Sigma, Metabase and Microsoft Power BI. These are documented product patterns, not authenticated hands-on verification of each vendor's current application or pricing tier.
- The machine blueprint, required human mirror and UI blueprint from verified remote main `d5ecbd33c1fd582058ec3514e2084820c8a3f1c2`. The shared local checkout remains at historical commit `80cd0976c434b6db62d3e415bc638cbe4a9468c2` with foreign changes; it was not reset or rebased. The previous audit at `94672bf...` remains a frozen historical observation.
- The user-supplied `cohort_html/index.html`, inspected in source and rendered locally at 1600 × 1050. Browser requests were restricted to the loopback reference server. No business values, row identities or source data files are copied into this report. The file is a layout/interaction reference, not evidence that its forecasting methodology is correct or authority to resume forecasting.

Source fingerprints: machine blueprint `9d791c1a348e2cdb167f9f07eff1f1c3a4e4f7072245e12d3b935df716880f0a`; human mirror `8490111d143cb8b02d6bfecdc4ba3dadd2c5c9a5fc8ea92647b4999dd77ca621`; UI blueprint `bd2bee4bc3a07c898dc8a6526359c4bf7ba2b1de278e564c1916758876904b69`; local reference HTML `7aeaac493b1f4cd6fe3933504505d5739a6a5db31c72bc1998161db85c53bfad`.

## Adoption receipt — 2026-09-05

After reviewing the ideas, the owner explicitly requested adding these
requirements throughout the project documentation. The
[analytical authoring contract](../../contracts/analytical-authoring-contract.md)
contains the S/R-to-requirement and acceptance mapping. Core S01-S03, S05-S10 and
R01-R10 are adopted; S04 adopts the explicit customer entity envelope while
additional membership types remain future scope. R11 and additional-format
parts of R12 retain their stated optional status. Existing R12 snapshot/channel
obligations remain required. Forecasting remains held.

Machine/human/UI requirements, architecture ownership, the continuation roadmap,
UI capability bindings and generated indexes are synchronized by this adoption.
The earlier coverage labels, source hashes and verification observations below
are historical findings, not assertions that the new requirements are still
missing. Accepted requirements do not establish implementation or release
readiness. The completed documentation checks are recorded in the authoring
contract's verification record.

## Findings that change the earlier recommendation

1. Segment authoring is a governed query over related entities and events, not just filtering a flat customer-feature table. AND/OR is one part of that language. Relationship scope, absence, aggregates and temporal order determine its expressive power.
2. Drag-and-drop is an authoring interaction; density and report layout are independent choices. A report can be a compact analytical worksheet dominated by a matrix, with no permanently visible block palette or inspector.
3. Current requirements already contain considerably more than the earlier example showed. `FILTER-011/012` explicitly require nested refinements and distinct draft/applied/preview states. UI density and table-first compositions are already required. These are not newly discovered missing features.
4. Important gaps occur between an intent statement and its executable semantics. For example, `FILTER-011` requires same-container refinements, while the shown `filter_expression` shape only has Boolean nodes and a field/value predicate; section 12.10 still requires only `MART-CUSTOMER-FEATURES` and a Polars expression. Relationship traversal, quantifiers and their compilation need a precise contract. This is a specification gap, not a claim that code was freshly audited and found absent.
5. The product is explicitly B2C retail and self-hosted. Mindbox provides valuable segmentation references, but campaign automation, audience activation, B2B sales objects and SaaS operation are not silently added to Custometry. See blueprint section 1 and `NON-GOAL-013–015`.

## Relevant existing product patterns

| Reference | Observed documented pattern | Useful transfer to Custometry |
|---|---|---|
| [Mindbox: nested filters](https://help.mindbox.ru/docs/%D0%BA%D0%B0%D0%BA-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82-%D0%B2%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C-%D0%B2-%D1%84%D0%B8%D0%BB%D1%8C%D1%82%D1%80%D0%B0%D1%85) and [filter builder](https://help.mindbox.ru/docs/filters-begin) | A criterion can refine a related action/order; nesting decides whether conditions must hold on the same object. The catalog exposes properties and nested criteria through search. | Entity-aware refinement and a readable statement of which object each condition constrains. Do not copy incidental menu depth or naming. |
| [Mindbox: segmentation creation](https://help.mindbox.ru/docs/segmentations-create) and [membership filters](https://help.mindbox.ru/docs/segmentations-filters) | Different entities and update modes; saved membership can be referenced by other filters, with historical options and visible freshness where supported. | Separate a reusable definition, a mutable user-managed collection, an immutable evaluation result and its consumption policy. |
| [RetailCRM: segmentation mechanism](https://docs.retailcrm.ru/Users/Marketing/Segments/UpdatedSegmentationMechanism) | Distinguishes related collections, absence and aggregate filters. Its absence operation is explicit rather than an arbitrary numeric filter. | Treat existence/absence as first-class semantics and test empty collections. Vendor-specific shortcuts are not universal mathematical rules. |
| [Amplitude: cohort definitions](https://www.amplitude.com/docs/analytics/define-cohort) | Behavioral aggregation, event ordering, relative windows and interval activity can define reusable populations. | Go beyond lifetime totals to behavioral questions. Predictive cohorts are not adopted during the forecasting hold. |
| [Sigma: pivot tables](https://help.sigmacomputing.com/docs/working-with-pivot-tables) and [table formatting](https://help.sigmacomputing.com/docs/format-and-customize-a-table) | Row/column/value assignment, hierarchical expansion, conditional formatting, totals and frozen columns support table-centered workbooks. | A substantial matrix/table capability, with controls for data structure as well as visual density. Do not copy automatic Sum defaults onto non-additive metrics. |
| [Metabase: query builder](https://www.metabase.com/docs/latest/questions/query-builder/editor) and [dashboard interactivity](https://www.metabase.com/docs/latest/dashboards/interactive) | Stepwise query composition, previews, reusable questions and explicit click/filter behavior. | An analytical definition can be reused by several report presentations; clicking a value has a declared destination and filter scope. Arbitrary joins or SQL round-tripping are not automatically safe for Custometry. |
| [Power BI: tables, matrices and lists](https://learn.microsoft.com/en-us/power-bi/paginated-reports/report-builder-tables-matrices-lists) | One tabular region supports alternative data-driven layouts with grouping. | A compact worksheet and a printed document need layout policies over shared semantics. This reference does not add a new PDF or paginated-report product commitment. |

## What the local report demonstrates

The inspected default view has seven adjacent filter controls, four summary measures, and a primary matrix with twelve cohort rows and fourteen columns including the row label and total. At the observed desktop viewport, the entire matrix fits horizontally. The document also has alternate views, a sticky table header/first column, local scrolling when needed, metric-aware formatting, comparison controls and short explanatory text.

The useful pattern is **controls → compact summary → large analytical table → explanation**, with the report using most of the viewport. The authoring controls are not part of everyday consumption. Exact KPI count, font size, employer-specific labels, calculations and the forecast-specific views are not transferred as universal requirements.

Recommended authoring choices are page composition (`dashboard_grid`, table-first/flow, narrative) and display density, kept separate from document profile and calculation meaning. A table-first page remains a `workbook_report` or another compatible existing profile; it is not a fourth document engine. Configure matrix rows, columns and measures through shelves, lists and optional dragging. Arrange surrounding blocks using the common composer. Hide edit handles, palettes and properties in viewer mode.

Current authority already supports this: machine `ANALYTICAL-DOC-001–012`, `UI-DENSITY-001–003`, Focus presentation state, and UI blueprint sections 8.5, 10 and 12. The necessary continuation is a concrete compact authoring specification and acceptance examples, not an assertion that compact reports are wholly missing.

## Candidate requirements and clarification register

Coverage labels refer to reviewed normative documents, not implementation completion: **Partial** means an existing obligation lacks important semantics; **Not found** means no explicit end-to-end requirement was found in the relevant sections and targeted searches; **Covered** means reuse and make acceptance concrete; **Optional** means a product expansion to evaluate separately.

Priority **P0** means decide the representation or semantics before affected implementation, not implement the whole feature immediately. **P1** is a valuable early vertical slice. **P2** is a later candidate or explicit scope decision. Effort is relative engineering uncertainty, not a time estimate.

### Segmentation and exploratory populations

| Candidate | Coverage and evidence | Proposed behavior and business example | Priority / effort / acceptance witness |
|---|---|---|---|
| S01 — Correlated entities and explicit existence | Partial: `FILTER-011`, sections 6.2/6.5 versus flat predicate shape and customer-feature input in 12.10. [Mindbox nesting](https://help.mindbox.ru/docs/%D0%BA%D0%B0%D0%BA-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82-%D0%B2%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C-%D0%B2-%D1%84%D0%B8%D0%BB%D1%8C%D1%82%D1%80%D0%B0%D1%85). | Conditions on one receipt/line/event stay together. Support explicit exists/not-exists over allowed relationships, scoped aggregates and declared cardinality; require an intentional distinction between one qualifying order and two independent orders. | P0 / high. A customer with product A online and product B offline must fail “A bought offline” and pass “bought A and also bought offline.” No join multiplication of members or revenue. |
| S02 — Behavioral temporal sequences | Not found in segmentation sections; digital funnel/event contracts are adjacent but not a reusable segment-sequence specification. [Amplitude definitions](https://www.amplitude.com/docs/analytics/define-cohort). | “Viewed category, then purchased within seven days,” “first purchase followed by no repeat in a complete 60-day window”; define ordering, gaps, same item/session binding, ties, cancellation and late events. | P0 language decision, P2 full execution / high. Reversed order fails; identical timestamps follow a declared tie rule; incomplete observation yields unavailable/partial, not a confident absence. |
| S03 — Aggregates inside a population definition | Partial: feature refs and registered metrics exist; per-condition aggregate/window composition is not specified. | Count distinct purchase days/categories, sum only completed orders in a category, ratio of category purchases to all purchases, compare two windows. A saved flat lifetime field cannot stand in for every such query. | P0 / high. Window-local predicates, units, nulls, unique grain and numerator/denominator are pinned; unrelated joins cannot multiply counts. |
| S04 — Explicit population entity | Partial: filter registry identifies entities, but membership identity in 12.14 remains `canonical_customer_id`. | Begin with customer segments; decide an additive path for reusable Product/Store collections within B2C retail. Reports must know whether the selected object filters customers, transactions or products. | P0 compatibility decision, P2 additional entities / high. A product set never masquerades as customer IDs; unsupported block/entity bindings fail visibly. B2B Account/Lead remains outside current scope. |
| S05 — Imported and manually curated populations | Not found as an explicit segment lifecycle. Immutable calculated snapshots do not describe editable ID collections. [Mindbox creation](https://help.mindbox.ru/docs/segmentations-create), [Amplitude imports](https://amplitude.com/docs/analytics/create-cohorts). | Import a known customer list or curate an exclusion list; resolve IDs with matched/unmatched/duplicate outcomes. Changes create collection revisions and new snapshots while reports keep their original versions. | P1 / medium. Rename, append, replace and remove semantics are explicit; unknown identifiers never silently create customers. No PII is exposed by matching diagnostics. |
| S06 — Segment composition and dependency freshness | Partial: `SEGMENT-021/024` define consumers and dependency visibility, not a complete segment-to-segment expression/dependency contract. [Mindbox membership filters](https://help.mindbox.ru/docs/segmentations-filters). | Union/intersection/difference of reusable populations; pinned versus following-version behavior; reject cycles; evaluate dependencies in order and report the oldest relevant input freshness. | P0 / high. A changed upstream segment produces an impact preview and new result; a failed upstream refresh cannot be advertised as a fully current downstream segment. |
| S07 — Explain inclusion and inspect rule impact | Partial: trust, aggregate profiles, preview and permission rules exist; a membership explanation/condition-impact workflow was not found. | For an authorized member: “which rule matched, which event/window was used, why excluded.” Before saving, show size changes and contradictions; support before/after definition comparison. | P1 / medium-high. Explanations reproduce the evaluator and respect member/field grants. Counts for different branches do not expose restricted small groups. Reordering AND conditions preserves final membership. |
| S08 — Membership at selection time versus event time | Partial: immutable snapshots and migration are well covered by `SEGMENT-019–028`; event attribution while membership changes needs a separate rule. [Mindbox segment reporting](https://help.mindbox.ru/docs/segments-dashboard). | Distinguish “past revenue of today's VIPs,” “revenue earned while customers were VIPs,” and “fixed January cohort's later revenue.” These answer different questions. | P0 / high. The same customer entering a segment midmonth gives intentionally different, explainable totals under each mode; late data and property-history policy are explicit. |
| S09 — Create a population from exploration | Partial: `SEGMENT-010` covers a bucket/stratum cell; general chart, retention and funnel selections need a contract. [Amplitude chart-to-cohort](https://amplitude.com/docs/analytics/create-cohorts). | From a selected cohort cell or drill-through result, save either the exact observed set or a reusable rule, with clear limits where the rule cannot faithfully reproduce the selection. | P1 / medium. Saved population resolves to the same authorized identities as the source result; unsupported conversion is explicit rather than approximated. |
| S10 — Segment health and multidimensional comparison | Covered foundation: profile, overlap, entrants/exits, migration, quality and drift in `SEGMENT-023–028`. | Compare populations on size, share, revenue, repeat behavior and overlap; surface why a population changed. Separate membership changes due to data refresh from changed definitions. | P1 / medium. Reuse existing requirements; do not add a second segmentation analytics module. Overlapping segments do not imply additive totals or causal impact. |

### Report authoring and analytical reuse

| Candidate | Coverage and evidence | Proposed behavior and business example | Priority / effort / acceptance witness |
|---|---|---|---|
| R01 — Compact table-first authoring | Covered intent, Partial authoring detail: `UI-DENSITY-001–003`, `ANALYTICAL-DOC-003`, UI 8.5/10/12 and the supplied report. | Pick a worksheet-like page, keep the table dominant, use compact summaries and adjacent controls, hide authoring chrome for viewers, retain accessible density/column preferences. Dragging is optional arrangement, not a mandatory card aesthetic. | P1 / medium. Recreate the structural pattern on synthetic fixtures in the working ticket; table and comparison begin in the first desktop viewport. Do not require a preceding chart or four KPI cards. |
| R02 — First-class matrix/pivot semantics | Partial: `pivot` is in the block union, but no explicit PivotSpec row/column/value/subtotal model was found. [Sigma pivots](https://help.sigmacomputing.com/docs/working-with-pivot-tables). | Hierarchical row/column dimensions, several measures, subtotals, grand totals, expand/collapse, conditional formatting and transposition. Cohort matrices are a specialized instance with observed-age metadata. | P0 / high. Correct distinct/ratio/semi-additive totals over the full authorized result; no averaging percentages or summing visible paginated rows. Aggregate changes trigger a backend result rather than a hidden browser calculation. |
| R03 — Parameterized reusable analytical products | Partial: templates, normalized builder and filter scopes exist; a named typed parameter/binding contract was not found. | One reusable “category performance” or “retention” analysis exposes period, category, metric and population controls, with declared defaults and restrictions. It can feed several pages without copying formulas. | P0 / medium-high. A parameter resolves consistently at its declared targets; an unsupported mapping is shown, not ignored. Display-only settings remain separate from result-affecting inputs. |
| R04 — Flexible comparison periods and populations | Not found beyond existing LY-oriented modes: `TimeComparisonSpec` enumerates prior-year variants and `none`; segment snapshot-pair comparisons exist separately. | Previous period, custom comparison period and side-by-side population comparison. For example, last four complete weeks versus the preceding four, using the same customer set or explicitly different sets. | P0 contract decision, P1 selected modes / medium-high. Different window length, overlap, period maturity, population basis and % versus percentage-point change are explicit. No forecast is required. |
| R05 — Guided derived-metric authoring | Covered metric lifecycle, Partial creation workflow: sections 6.3/12.15, candidate/verified/canonical statuses. [Metabase metrics](https://www.metabase.com/docs/latest/data-modeling/metrics). | Build a draft ratio, filtered measure or period comparison through a typed formula editor; show units, denominator, allowed dimensions and a test result; promote a reusable definition through existing review. | P1 / medium-high. Reuse MetricRegistry; a report-local trial does not silently redefine a canonical metric or calculate business values only in the browser. |
| R06 — Cell-to-evidence drill-through | Covered chart capability and access boundaries, Partial exact end-to-end workflow. [Metabase drill-through](https://www.metabase.com/docs/latest/questions/visualizations/drill-through). | A number opens its definition, source window, contributing authorized records and reconciliation, with a breadcrumb back. Optionally continue to a saved population or analysis. | P1 / medium-high. Drill-through preserves the parent snapshot/filter basis and explains non-additive totals; reading a report does not automatically grant raw-data access. |
| R07 — Click/filter and cross-page interaction contract | Covered scopes and linked-target DAG, Partial author-facing wiring and feedback. [Metabase dashboard interactivity](https://www.metabase.com/docs/latest/dashboards/interactive). | The author selects whether a click highlights, filters specific blocks, opens details or navigates to another page with parameters. Show affected and unaffected targets. | P1 / medium. No invisible page-wide filter, feedback loop or change to locked scope; Back restores the previous view. |
| R08 — Explicit cohort maturity and missingness in cells | Covered analytics/format intent: section 12.5 right censoring, `METRIC-013`, `COMPARE-003/004`; table-cell acceptance needs binding. | Distinguish observed zero, not yet observable, missing source, suppressed small cell and not applicable. Let users inspect absolute count, percentage, cumulative and comparable-age views. | P0 correctness / medium. An immature cohort never looks like failed retention; denominator and completeness travel with every cell and export. |
| R09 — Compare report/result revisions | Partial: immutable versions, lineage and compatibility exist; a user-facing semantic diff workflow was not found. | “Why did this number change?” separates data refresh, filter/metric/segment definition changes, late corrections and policy changes. A draft can be compared with the published version before replacement. | P1 / medium-high. Equal versions show no invented difference; inaccessible old/new details remain protected; previous publications are not rewritten. |
| R10 — Exploration, templates and evidence-linked conclusions | Covered foundation: Methodology Registry, AnalysisCase, Findings, personal Saved View and shared composition. | A user can explore, save personal views, turn a validated analysis into a reusable template, and publish an evidence-linked conclusion with applicability and limitations. | P1 / medium. Prioritize existing product outcomes instead of inventing another notebook, dashboard or template engine. |
| R11 — Manual targets and plan-versus-actual | Optional; not established as a general reusable target-input contract. The local reference only motivates selectable analytical inputs. | A governed imported budget/target can be compared with actuals without an ML prediction. Targets have entity/metric/period/unit/version and cannot overwrite facts. | P2 / high. Requires a separate scope choice, reconciliation and permissions; do not resume Forecasting or make this a prerequisite for reports. |
| R12 — Portable reading and formal output layout | Covered shared Web/email/XLSX snapshot and export scope; arbitrary executable HTML and a new PDF product are not authorized. [Power BI layout](https://learn.microsoft.com/en-us/power-bi/paginated-reports/report-design/page-layout-rendering-report-builder-service). | A clean reading view uses the same saved result; later allowed exports preserve column meaning, headings, full values and overflow behavior. Evaluate additional standalone formats separately if there is a real use case. | P2 / medium-high. A dense Web matrix is not proof that a printed page or email fits. No DOM scraping or embedding a large raw dataset as the production delivery model. |

## Important capabilities already specified — do not rediscover them as gaps

The existing blueprint already covers a versioned metric registry with correct non-additive aggregation; customer identity and semantic relationship cardinality; time/calendar/currency and incomplete-period policy; cohorts and right censoring; RFM/buckets/KMeans; outlier treatment; segment histories, overlap and migration; data-quality/capability blockers; role/row/PII boundaries; common document snapshots and filter scopes; personal views; methodology/findings/collaboration; schedules, execution control and metric watches; Data Guides; report delivery; backup/restore and self-host operations.

These obligations still need implementation and user-observable proof. Their presence is not proof of readiness. In particular, `UI-DENSITY` and nested filter refinements should have constrained the earlier example more strongly.

## Five decisions with the highest rework risk

1. **Population query language:** resolve S01–S03 and the typed filter/segment mismatch. Choose explicit supported operators and how relational/temporal expressions compile through allowed semantic relationships. A plain expression on a flat feature row is insufficient as the general target.
2. **Population identity and time:** resolve S04–S08. Keep definition, curated collection, evaluated snapshot, member entity, observation window and report membership policy distinct. Implement customer-first without hard-coding every future member key as a customer key.
3. **Analytical result and pivot shape:** resolve R02/R08 and metric aggregation compatibility. Row/column grouping, denominator and observed-cell state must be result semantics; UI size and formatting remain presentation.
4. **Reusable parameters and comparison policy:** resolve R03/R04 plus click/filter mappings. Changing a parameter's scope changes a result; changing density does not.
5. **Analyst workflow and publication:** resolve R01/R06/R09/R10 through a compact worksheet scenario and a segment-to-report scenario. Reader, explorer and author modes share results while keeping different actions and persistence rules.

A decision can define a compatible extension point while deferring its implementation. Temporal sequences, Product/Store populations and manually curated collections need not all be in the first ticket. What must be avoided is declaring a narrow first implementation to be the full intended contract.

## Research-time proposed sequence (adoption tracked above)

Continue shared identity/policy/data-correctness integration where its scope is already settled. Before treating N5/N5S in the roadmap as ready, resolve the five decisions above in bounded product/contract specifications, synchronize adopted requirements machine-first with the human and UI mirrors, and attach concrete acceptance examples. Do not create a new UI certification program, prompt pack, prototype sequence or release promise.

Suggested first implementation outcomes after those decisions:

1. A customer segment over related completed orders/lines, with a reusable definition, a real authorized preview, an immutable snapshot and an inclusion explanation.
2. A compact table-first report with typed controls, one supported matrix/aggregation pattern and that segment binding; save/reopen and inspect the exact result without authoring chrome.
3. Extend to reusable components, selected comparison modes, chart-to-population exploration and semantic revision comparison as their provider contracts become available.

This is a recommended order, not owner acceptance of a first release. Forecasting remains held; clustering and event-sequence computation are not smuggled into shared infrastructure tickets. B2B, marketing activation and new distribution formats remain separately governed scope.

## Acceptance scenarios that expose missing requirements

Use synthetic fixtures rather than employer data to pin these behaviors:

- One customer has product A in an online order and B offline; another has A offline. Same-order and independent-order filters intentionally return different sets.
- A customer has no purchases because the imported period is incomplete. Absence is not certified merely because no matching row was loaded.
- A customer enters a segment halfway through a month. Fixed-cohort, end-of-period population and event-time membership reporting have distinct documented results.
- A customer appears in two overlapping segments. Overall customer total is the union, not the sum of segment counts, unless the analysis explicitly reports membership occurrences.
- Ratio totals and distinct counts are recomputed at their target grain, regardless of visible rows, pagination, collapse or column order.
- A matrix includes a not-yet-observable age bucket. It is distinguishable from observed zero and denied/suppressed cells.
- A draft change to a threshold shows a new preview and affected references; the published report and its old population remain unchanged.
- A dependent segment fails to refresh. A downstream report either uses clearly labeled last-good data under its policy or blocks; it does not claim current data.
- A table cell opens a detailed result only with independent permission and returns with the same context; no raw member access is inferred from aggregate visibility.
- The same report can be read compactly and edited with block controls without altering the calculation merely because the mode or density changes.

## Impact and verification

The original research change had **none** impact on runtime/API/persistence. The subsequent adoption remains documentation and coverage changes only; its specified future transitions are assessed in the authoring contract. Actual provider/consumer and persistence compatibility remains unknown until implementing-ticket inspection and proof; additive versioning is a requirement, not observed runtime evidence.

Read-only verification used official documentation, an immutable remote blueprint snapshot, targeted term/section searches, HTML/CSS/JavaScript inspection and an actual local browser render of the supplied file. The local file was not edited and business calculations were not validated. Keyword absence was used only together with the relevant normative shapes/sections; it is not a proof of repository-wide absence.

Documentation checks passed after contributor-index generation: `validate_blueprints` (1,141 indexed IDs), `generate_docs_index --check` (36 contributor documents), `check_docs_links` (52 documents, 119 local links) and `git diff --check`. The Python checks used `uv run --locked python -m tools.custometry_quality.<command>` after `source scripts/activate-toolchain.sh`. No backend, browser-runtime release, performance or recovery readiness is claimed.
