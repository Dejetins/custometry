---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-022",
  "title": "C04 behavioral sequence execution",
  "version": "0.1.1",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.19"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-021/MS-021-S01/report.md"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5",
      "ids": [
        "FILTER-001",
        "FILTER-004",
        "FILTER-005",
        "FILTER-006",
        "FILTER-013",
        "FILTER-015",
        "FILTER-016",
        "FILTER-017",
        "FILTER-018"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-022/DEC-01",
    "MS-022/DEC-02",
    "MS-022/DEC-03",
    "MS-022/DEC-04",
    "MS-022/DEC-05"
  ],
  "supersedes_ref": {
    "path": ".codex/delivery/evidence/MS-022/reconciliation/plan-v0.1.0.md",
    "version": "0.1.0",
    "reason": "Wrong copied plan body before product implementation"
  },
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-022.md"
  }
}
---
# MS-022 — bounded behavioral sequence execution

## Outcome, authority and current evidence

Parent [WS-004 v0.2.19](../../directions/DIR-004/workstreams/WS-004.md) and its
whole-workstream delegation authorize the next sequential C04 unit. MS-021 proves
published count editing and persistence. FILTER-015/016/017/018 and human §6.5 require
ordered events, time windows, gaps, bindings and honest absence. The current flat
registry admits dates but no timestamp; the relational engine admits exact immutable
Parquet and typed correlations. It has no sequence node. The foundation remains
unmounted here; genuine publication and report UI follow in the next bounded unit.

## Decisions and alternatives

DEC-01: keep Semantic ownership of event meaning. Add an explicit event-definition
version, event-time field version and trusted observation interval/evidence. Admit
native Arrow timestamp(us, UTC) columns through a separate provider-owned time binding;
old flat registry/value DTOs stay byte-compatible and cannot request timestamps.
Do not stringify timestamps or weaken artifact/schema validation. Preserve exact UTC
microseconds and explicit known-column observation; timezone conversion belongs to
upstream published meaning, not browser or row-wise Python evaluation.

DEC-02: add sequence-filter-execution/v1 with ordered positive/negative steps,
registered event definitions and row predicates. Reuse the one relational DuckDB
executor and aggregate predicate subset. One sequence traverses one declared
parent→event relationship; different registered event definitions may share that edge.
The first step is positive. Later positive steps pin inclusive min/max elapsed gaps
from the preceding positive anchor and require strictly increasing event time.
Equal timestamps never manufacture order through IDs. Negative steps name the preceding
positive anchor and a half-open offset interval, strictly after its timestamp; any
following positive step occurs after that negative interval. No negative-first rule.

DEC-03: fixed aware UTC windows are half-open. Relative windows persist a versioned
publication-observation-as-of anchor, elapsed microsecond offsets and exact resolved
bounds; validate resolution against current trusted cutoffs. No wall-clock guessing.
Pin observation/knowledge-as-of, event/relationship/property versions, null/time policy,
coverage/evidence and effective authorization in identity. Same-property/session
bindings compare typed versioned fields across named positive steps; missing properties
remain unknown. Explicit UTC elapsed time is not a claim of local-calendar semantics.

DEC-04: compile parameterized bounded SQL with generated aliases only. Apply root and
child ceilings before candidate paths/absence. Confirm observed positive witnesses;
certify absence only when the entire relevant interval is covered and authorized
relationship history complete. Unknown time/property/predicate or incomplete history
cannot establish absence or false certainty. Candidate paths use three-valued logic;
when missing observations could hide a path, return conservative unknown. NOT preserves
unknown. Do not return event payloads to the caller.

DEC-05: cap steps, depth, correlations, fanout and conservative candidate-path work
before running sequence joins, in addition to existing byte/row/memory/cancellation
limits. Old request schemas reject new nodes; old identity remains unchanged without
new grants. No API/receipt schema, persistence or UI migration in this foundation.
No new service, arbitrary join/SQL, provider completeness claim or production action.

## Boundary and proof

Semantic contracts → Analytics contracts → infrastructure compiler/admission; public
trusted grants are the integration port. Existing application/API behavior is unchanged.
Rollback is removal of an unmounted additive capability; no durable data migration.
The existing shared executor is retained over a parallel engine because it owns artifact,
authorization, work limits, policy recheck and SQL three-valued semantics already.

- AC-01: strict versioned contracts, native UTC time admission and relative resolution;
  old flat/correlated/aggregate DTOs reject sequences and retain old behavior/identity.
- AC-02: actual immutable Parquet/DuckDB proves positive ordering/ties/gaps, negative
  intervals/coverage, fixed/relative windows, property/session bindings and three-valued
  truth. Independent expected fixtures include hidden rows and late/unknown observations.
- AC-03: forged event/time/field/relationship/as-of, wrong timestamp schema, authorization
  changes and bounded-work/cancellation checks reject safely before result delivery.
- AC-04: focused regressions/static/local gates, independent read-only review, synchronized
  authoring contract/matrix/index and immutable evidence through the exclusive updater.

This tests-only foundation proves native columnar execution, not genuine Semantic
publication, mounted editing, complete FILTER-015 or C04. Financial metrics, remaining
calendar/relative policies, populations and C05–C11 remain required. MS-016 once-only
company calendar policy and C10 performance follow-up remain unchanged.

## Impact and bindings

Compatible additive internal event/time/grant/request capability. No old DTO widening,
HTTP/persistence/default/credential/deployment changes. One executor and existing
read-only reviewer. Plan0.1.1 accepted under delegated technical authority2026-10-07.
Triad: this plan, `.codex/agents/generated/MS-022`, `.codex/delivery/ledgers/MS-022.md`.
Journal owns execution state; maintain reciprocal links, versions and evidence.

Revision0.1.1 replaces the erroneous copied body; original S01 remains blocked history.
S01-R1 is the unique replacement, with [reconciliation evidence](../../../../../.codex/delivery/evidence/MS-022/reconciliation/authoring-error.md).
