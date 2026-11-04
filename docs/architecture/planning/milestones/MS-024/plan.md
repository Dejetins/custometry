---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-024",
  "title": "C04 receipt selection by customer event history",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.21"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-023/MS-023-S01/report.md"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5",
      "ids": [
        "FILTER-001",
        "FILTER-002",
        "FILTER-003",
        "FILTER-004",
        "FILTER-005",
        "FILTER-006",
        "FILTER-013",
        "FILTER-014",
        "FILTER-015",
        "FILTER-016",
        "FILTER-017",
        "FILTER-018"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-024/DEC-01",
    "MS-024/DEC-02",
    "MS-024/DEC-03",
    "MS-024/DEC-04",
    "MS-024/DEC-05"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-024.md"
  }
}
---
# MS-024 — receipt selection by customer event history

## Outcome and authority

[WS-004 v0.2.21](../../directions/DIR-004/workstreams/WS-004.md), the continuation
addendum and accepted MS-023 authorize this C04 integration. FILTER-001–006/013–018
and human §6.5 govern scoped expressions, event sequences and history uncertainty.
MS-023 already proves genuine native published events and the authorized observed
Customer universe. Receipt remains the report/metric grain. This milestone delivers
customer history membership in receipt filters, without asserting full populations,
certified absence, complete C04 or C05–C11. Retained runtime41746 is preserved.

## Decisions

DEC-01: additive receipt-filter/v4 and cohort-filter-execution/v1 introduce a
CustomerEventMembership leaf nested in receipt Boolean/correlated expressions.
The leaf follows exactly the published Customer→Receipt relationship to its unique
parent and evaluates a typed SequenceExpression rooted at Customer. It selects all
authorized receipts of qualifying customers, including receipts outside the event
window; metric period remains independent. Only valid nullable unlinked keys produce
unknown. Required-key damage and nonnull orphans still fail preflight. NOT preserves
unknown. No Customer IDs or raw membership rows reach catalog/preview/facet HTTP.

DEC-02: one uncorrelated AS MATERIALIZED Customer CTE per membership leaf, with its
own nested Compiler and mandatory authorized observed-customer universe. All CTEs
use the same admitted tables, immutable bindings and authorization snapshot. Merge
node/scope IDs with explicit collision rejection; enforce total depth, correlations,
nodes, parameters and work ceilings. Every leaf is charged separately. SQL parameters
are ordered prelude, main expression/ceiling, facets. Prove materialization from actual
DuckDB plans and behavior, not an assumed optimizer rewrite. No row-wise evaluator,
client ID collection, wider budgets or private cross-context reads.

DEC-03: the trusted cohort grant pins the public old Receipt/ReceiptItem registry
bridge and observed-customer universe. v4 includes receipt_registry_versions and
promoted_registry_sets retaining each exact v2/v3 source map; backend validates
all maps and fields against public published metadata/artifact bindings. Preserve
v1 legacy UUID compatibility. Only local node/scope/step/anchor/binding references
are rebased; event, field, relationship and window versions remain unchanged.
Mixed scopes preserve locks; membership leaves are never field-replaceable even
inside Boolean wrappers. Copy/title changes do not alter query identity.

DEC-04: S01 adds genuine provider-backed v4 catalog, count-only preview and receipt/
item facets plus generated DTOs. Do not widen saved ReceiptSelection before S02.
Current Identity/store ceilings, Artifact admission, CSRF, cancellation and final
authorization recheck remain mandatory. S02 wires report persistence, scope algebra,
provider dispatch and mounted authoring with Apply/Reset/Undo/Save/reopen proof.

DEC-05: mounted RU/EN sequence editor supports positive/negative ordered steps,
fixed/publication-relative UTC windows, gap bounds and published property bindings.
Use observed-receipt labels, explicit current-history/unknown limitations and receipt
count grain. Preserve publication microseconds without JavaScript Date truncation.
Do not invent session fields, purchases, lifecycle transitions, calendar setup or
certified absence. Verify keyboard/focus and390px layout with real browser flow.

## Stages and acceptance

S01: AC-01 genuine published bridge/provider and explicit strict contracts;
AC-02 materialized SQL membership, global limits, parameter order and nullable/access
boundaries with real Parquet/DuckDB; AC-03 genuine publication/source SQL oracle and
authenticated catalog/preview/facets including revocation, no-ID output and old-reader
denial; AC-04 focused/static/local gates, independent review and synchronized evidence.

S02 depends on accepted S01: AC-05 persisted v4/scopes/locks/rebasing and unchanged
query identity; AC-06 mounted RU/EN editor including exact relative as-of windows;
AC-07 genuine Apply/Save/reopen, reset/undo, mixed filters and390px/browser proof;
AC-08 regressions/static/local gates, independent review, documentation and receipts.

Compatible additive contracts/provider/HTTP; S02 adds versioned persistence and
browser behavior. No migrations or production actions. Old readers reject new schemas.
Rollback must retain readers for saved v4 documents, or prevent opening those documents;
never silently downgrade their meaning. Performance is bounded by policy here, not a
latency claim. C10 measured latency work and remaining C04/population/financial metric
requirements continue after this milestone.

## Bindings

Plan0.1.0 accepted under existing technical delegation2026-10-07. One executor and
existing independent read-only reviewer. Triad: this plan, `.codex/agents/generated/MS-024`,
`.codex/delivery/ledgers/MS-024.md`; journal alone owns state. S01 receipt may enable S02
only after all declared proof. Final acceptance requires both stages. Continue the
whole authorized WS-004 afterward; no Goal mode or repeated owner approval.
