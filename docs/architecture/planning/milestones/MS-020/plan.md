---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-020",
  "title": "C04 scoped count and ratio execution",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.16"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-019/MS-019-S01/report.md"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5",
      "ids": [
        "FILTER-001",
        "FILTER-004",
        "FILTER-006",
        "FILTER-014",
        "FILTER-016",
        "FILTER-017",
        "FILTER-018"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-020/DEC-01",
    "MS-020/DEC-02",
    "MS-020/DEC-03",
    "MS-020/DEC-04",
    "MS-020/DEC-05"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-020.md"
  }
}
---
# MS-020 — scoped count and ratio execution

## Outcome, authority and current boundary

Parent [WS-004 v0.2.16](../../directions/DIR-004/workstreams/WS-004.md), its existing
owner continuation and accepted MS-019 authorize the next bounded C04 unit. Sources:
FILTER-014/016–018 and human §6.5; the existing correlated DuckDB executor and public
Semantic/Artifact/Identity contracts. Current execution supports predicates/existence,
not scoped aggregates. No complete-history claim follows from retail transport.

## Decisions and consequences

DEC-01: Semantic owns immutable registered typed count/count_distinct definitions:
relationship version, child grain/field versions, unit, null/empty/returns policies,
window time-field version and entity. Trusted grants additionally pin observation
coverage and knowledge-as-of. Analytics compiles aggregate operands and comparisons
using the existing isolated bounded DuckDB engine and current authorization checks.
No browser/Python row evaluator, arbitrary joins/SQL or new service is introduced.

DEC-02: a separate aggregate execution request declares capability explicitly. Keep
current relational/receipt v2 readers and generated browser schema unchanged. New
recursive Boolean/correlation/aggregate nodes have deterministic canonical bytes.
Scalar comparisons, compatible window-to-window counts and count ratios pin both
operands, typed comparator/units and denominator. Ratios use exact bounded decimal
cross-products, never floating division; denominator zero is unknown. Unsupported
registered financial metrics remain a subsequent provider increment, not a silent
fallback to row counts.

DEC-03: windows are explicit absolute half-open UTC timestamp intervals with pinned
observation/knowledge cutoffs. Resolve relative/calendar definitions in a later
provider step; no host timezone or current clock enters evaluation. Complete empty
count is zero. Incomplete relationship/window, unknown predicate/time/grain property
or null under a propagated policy yields unknown. Known null exclusion is explicit.
Every aggregate uses authorized child rows and the same parent key scope; root rows
are never multiplied. Count returns policy is all observed rows, with explicit row
predicate; do not relabel it as a net financial metric or certified business history.

DEC-04: each operand consumes correlation/work/node/value budgets; pin all definitions,
coverage and policies in identity and recheck authorization after actual input reads.
Preserve existing input integrity, fanout/cardinality, timeout/cancellation and no
external DuckDB I/O. New aggregate capability absent/stale/mismatched => typed blocker.

DEC-05: reuse the existing compiler/engine rather than build another execution path.
A separate DTO protects old readers; widening existing saved DTOs would advertise
unsupported editor behavior. No persistence migration, production rollout or UI
change in this foundation. Mount genuine published capabilities and editor/save flows
next, after the foundation is verified. Existing calendar correction remains binding.

## Acceptance and proof

- AC-01: strict versioned definitions/operands/windows/units and old-reader rejection;
  canonical order and complete dependency identity, incompatible references denied.
- AC-02: real synthetic admitted Parquet/DuckDB proves count/count_distinct, complete
  empty zero, unknown/null/incomplete/coverage behavior, both scoped operands and
  exact ratios/zero denominator. Independent small expected sets, no mock SQL result.
- AC-03: authorization before aggregation, current-policy changes, unique root grain,
  malformed scopes, fanout/resource limits and cancellation remain fail closed.
- AC-04: focused old execution regression, Ruff/Pyright/local gates, independent
  read-only review and synchronized authoring/requirements/index evidence.

Tests-only acceptance is justified for an unmounted execution/contract foundation;
no genuine retail provider, HTTP, persisted report or browser acceptance is claimed.
Those require the following unit. Financial metric operands, relative calendar
windows, behavioral sequences/populations and all remaining C04/C05–C11 remain.

## Bindings and decisions

One executor, existing independent read-only reviewer, manual sequential. No new
agent, Goal, publication/deployment/reset. Plan v0.1.0 accepted under delegated
technical authority on2026-10-07. Plan/pack/journal form the sole execution triad:
`docs/architecture/planning/milestones/MS-020/plan.md`,
`.codex/agents/generated/MS-020`, `.codex/delivery/ledgers/MS-020.md`.
Maintain exact parent/dependencies, canonical authoring contract and clause matrix,
generated index and immutable evidence before accepting the journal. Continue WS-004.
