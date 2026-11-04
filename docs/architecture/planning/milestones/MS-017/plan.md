---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-017",
  "title": "C04 correlated filter execution foundation",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.13"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-016/MS-016-S01/report.md"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5",
      "ids": [
        "FILTER-001",
        "FILTER-003",
        "FILTER-004",
        "FILTER-005",
        "FILTER-006",
        "FILTER-013",
        "FILTER-016",
        "FILTER-017",
        "FILTER-018"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-017/DEC-01",
    "MS-017/DEC-02"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-017.md"
  }
}
---
# MS-017 — correlated filter execution foundation

## 1. Outcome and authority

Parent [WS-004 v0.2.13](../../directions/DIR-004/workstreams/WS-004.md) and existing
whole-workstream owner continuation authorize this next C04 provider unit. Read
FILTER-001/003–006/013/016–018 and human §6.5 in full, the bounded-context map,
existing columnar filter contracts/adapter and current published retail semantics.
Current flat filters cannot express conditions on the same related item. This unit
adds versioned scoped Boolean/predicate/exists/not_exists contracts and a real DuckDB
executor over trusted owner-admitted immutable Parquet inputs. It does not yet mount
an API or UI nor claim published retail completeness. That integration follows next.

MS-016's calendar correction remains in force. No report calendar settings/adoption
is reintroduced; forecasting and other existing holds remain untouched.

## 2. Accepted architecture decisions

DEC-01: Semantic public RelationshipVersion owns stable/versioned parent-child keys,
entities, cardinality and policy. Analytics v2 AST has root entity/scope and stable
node/scope IDs; exists/not_exists explicitly bind parent scope, child scope/entity,
relationship ID/version and nested predicate. Only provider-published fields and
relationships are usable. Flat v1 contracts/meaning remain unchanged; old readers
reject v2 instead of stripping nodes. No arbitrary SQL, joins or client grants.

DEC-02: trusted grants carry per-entity current authorized input/field registry and
mandatory ceiling, relationship policies and explicit authorized-scope completeness.
Absence can be false only if complete and all observed predicates are known; a true
observed match makes exists true even if the rest is incomplete. Otherwise missing
history or unknown child predicate yields unknown. NOT preserves unknown; AND/OR
use SQL three-valued logic. Unknown roots are excluded from confirmed membership
and disclosed through counts/reasons. Receipt transport completeness is not business
history completeness: the current retail publication says business history unknown
and has quarantined items. The later adapter must not invent complete absence.

DEC-03: backend compiles predicates and correlated subqueries through fixed generated
identifiers/parameters. Conditions inside one child scope share one row; independent
exists nodes may select different rows. Output retains root grain and rejects duplicate
root IDs or malformed cardinality/keys. Mandatory root and child ceilings are outside
author Boolean logic. Current grant is re-resolved before delivery; changes reject.
Registry/relationship/artifact/content/policy/resource versions, scopes and normalized
expression enter identity. Reordering AND/OR children preserves identity; changing
scope does not. No persistence or cache writer is added in this foundation.

DEC-04: reuse the hardened bounded Parquet reader and isolated DuckDB settings.
Partition the global row/byte allowance equally across admitted entities before
reading, conservatively bounding combined allocations; this may reject a skewed
input that would fit an aggregate budget and must be explicit. Validate AST depth,
nodes/correlations before decode; validate cardinality, fan-out and a versioned
estimated-work formula in bounded preflight before membership evaluation. Runtime
memory/thread/deadline/cancellation controls remain mandatory. Trusted input metadata
and exact bytes are revalidated. No browser or row-wise Python expression execution.

| Boundary | Impact | Proof |
|---|---|---|
| V2 AST/Relationship/grants | additive unmounted contracts | invalid scopes/types/versions, old-reader rejection |
| Execution/identity | new provider foundation, flat unchanged | real DuckDB correlation, root cardinality, three-valued truth, normalized identity |
| Trust/resource boundary | new multi-input read | forbidden/changed grants, external IO restrictions, caps, cancellation and corrupt input |
| API/UI/persistence | none in this stage | no mounted capability/complete retail claims |

## 3. Ownership and continuation

MS-017-S01 owns the public contracts, DuckDB infrastructure execution, focused
synthetic Parquet tests and documentation. One executor and one read-only independent
reviewer; no parallel implementation, Goal, publication/deploy or production data
change. Preserve retained runtime and accepted receipts. The mounted retail adapter,
preview/facet/UI/persistence integration follows in the next C04 unit; aggregate,
sequence, population and remaining C05–C11 are not waived.

## 4. Acceptance

- AC-01: strict versioned scopes/relationships validate and normalize; v1 is unchanged.
- AC-02: real columnar execution distinguishes same-row conjunction from independent
  exists, preserves root grain and implements complete/incomplete/null truth tables.
- AC-03: authorization ceilings/revalidation, typed binding, cardinality/fan-out/work,
  byte/row/depth limits, timeout/cancellation and restricted IO are tested.
- AC-04: focused backend/type/static/local checks, independent review and synchronized
  docs/evidence pass. No browser test is required for this unmounted foundation.

## 5. Execution and documents

Use exclusive stage claim/receipt. Report observed synthetic provider seam separately
from future genuine Semantic/Artifact/Identity integration. Keep data/trace secrets
out of durable artifacts. Maintain parent/index/requirement/authoring references.

## 6. Bindings

plan_doc: `docs/architecture/planning/milestones/MS-017/plan.md`, v0.1.0.
prompt_pack_dir: `.codex/agents/generated/MS-017`.
stage_ledger: `.codex/delivery/ledgers/MS-017.md`.
Manual sequential whole-WS continuation, existing POSIX updater; no Goal.

## 7. Decision history

Version0.1.0 accepted under existing delegated technical authority on2026-10-07.
This is an implementation prerequisite, not complete FILTER-013/016–018 or C04 proof.
Continue immediately to genuine provider integration after acceptance.
