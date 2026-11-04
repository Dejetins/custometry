---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-018",
  "title": "C04 published correlated provider and preview",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.14"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-017/MS-017-S01/report.md"
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
    "MS-018/DEC-01",
    "MS-018/DEC-02"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-018.md"
  }
}
---
# MS-018 — published correlated filter provider and preview

## 1. Outcome and authority

Parent [WS-004 v0.2.14](../../directions/DIR-004/workstreams/WS-004.md), the unchanged
whole-workstream continuation and accepted MS-017 foundation authorize this next
C04 integration. Read FILTER-001/003–006/013/016–018 and human §6.5, the bounded-context
map, published retail projection and existing authenticated flat filter composition.
Mount Receipt→ReceiptItem correlation over actual published Semantic/Artifact inputs
with current Identity policy, a versioned field/relationship catalog and count-only
preview. Report authoring/persistence/facets follow immediately in the next unit;
this backend seam does not claim those user flows or complete C04.

## 2. Decisions and boundaries

DEC-01: Semantic owns an additive public correlated retail projection, validating the
exact published Receipt and ReceiptItem keys and relationship policy. It publishes
an explicit allowlist of receipt/item fields and decimal scales, immutable versions,
artifact identities and completeness evidence. No generic client joins or inferred
product/customer historical dimensions. Preserve flat v1 fields/contracts unchanged.

DEC-02: compose current Identity access, Semantic projection and Artifact admission
in apps/api. The root Receipt namespace/store ceiling is independent of user logic.
Only Receipt→ReceiptItem is available: children inherit their correlated parent's
store visibility and have a mandatory namespace ceiling. No child-root output or
unscoped child facet is exposed. Revocation/policy changes before delivery reject.
Actual publisher history is unknown and items are quarantined; observed matches may
be true, absent matches remain unknown. Do not convert transport completeness into
certified absence. Pin publication/quality/relationship evidence in completeness hash.

DEC-03: additive `/composer/v1/filters/v2/{dataset_id}/catalog` and
`/composer/v1/filters/v2/preview` use server-bound workspace/actor and strict typed
AST. Root is always Receipt. Return exact matched/nonmatched/unknown/authorized
counts and limitation codes, never row IDs or artifact paths. Catalog search uses
localized labels/IDs/types; it carries versions and mandatory policy explanation.
Existing v1 endpoints and saved report schemas keep their meaning. V2 preview cannot
be persisted as a v1 filter; later authoring adds an explicit typed v2 branch.

DEC-04: reuse MS-017 bounded isolated DuckDB, global/per-input caps and cancellation.
Use actual disposable intake/control/source PostgreSQL, immutable artifacts and
HTTP auth in proof, including independent source-SQL expected membership/counts,
store-scope narrowing, foreign targets, old-reader rejection and mid-flight policy/
session changes. Do not infer browser/UI or production delivery from backend proof.

| Boundary | Impact | Proof |
|---|---|---|
| Semantic/public DTO/API | compatible-change, additive v2 | exact publication binding, strict schemas, v1 unchanged |
| Trust/identity | new genuine multi-input composition | current Identity/Artifact and store-parent ceilings |
| Execution/absence | actual published provider | real Parquet/DuckDB vs independent source SQL, unknown absence |
| Persistence/UI/calendar | none | no claim; MS-016 policy remains |

## 3. Execution and acceptance

One sequential executor and the existing independent read-only reviewer. No Goal,
publication/deploy, production migrations or retained runtime/data changes.
MS-018-S01 owns provider/contracts/composition/routes, focused tests and documentation.

- AC-01: strict published field/relationship versions and exact artifact admission.
- AC-02: actual provider produces source-verified root membership, unknown absence
  and current store ceilings; runtime/resource/authorization remain bounded.
- AC-03: authenticated catalog/preview expose count-only results and reject invalid
  payloads, foreign targets and revoked/current-policy changes; v1 stays unchanged.
- AC-04: focused backend/static/local gates, independent review, synchronized docs
  and immutable receipt. No browser requirement for unchanged browser surface.

## 4. Continuation and bindings

Continue immediately to v2 report authoring, facets, persistence/result limitations
and real browser scenarios, then remaining aggregate/sequence/population/C05–C11.
The canonical journal owns execution; no secondary status register.
plan_doc: `docs/architecture/planning/milestones/MS-018/plan.md`, v0.1.0.
prompt_pack_dir: `.codex/agents/generated/MS-018`.
stage_ledger: `.codex/delivery/ledgers/MS-018.md`.

## 5. Decision history

Version0.1.0 accepted under existing delegated technical authority on2026-10-07.
This bounded genuine provider milestone does not waive the remaining WS-004 scope.
