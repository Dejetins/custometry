---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-012",
  "title": "C04 Receipt filter hierarchy and locked inheritance",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.8"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-011/MS-011-S01/report.md"
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
        "FILTER-008",
        "FILTER-010",
        "FILTER-011",
        "FILTER-012",
        "FILTER-017",
        "FILTER-018",
        "COMPARE-008"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-012/DEC-01"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-012.md"
  }
}
---
# MS-012 — Receipt filter hierarchy

## Outcome and authority

Parent: [WS-004 v0.2.8](../../directions/DIR-004/workstreams/WS-004.md).
Existing [owner delegation](../../../../../.codex/delivery/evidence/WS-004/owner-continuation-addendum-2026-10-07.md)
accepts sequential technical decomposition and implementation. MS-011 supplies the
real mounted provider. One executor; independent review of lock/security compatibility.
No Goal, publication, production migration, retained-data reset or parallel implementation.

## Decisions and boundaries

DEC-01: introduce `composer-scopes/v2` retaining existing Store/context fields and
adding typed Receipt bindings with explicit dataset identity. Preserve v1 readers,
bytes and meaning; old readers must reject v2. Resolve document/chapter/page/outer-to-inner
section/block ancestry, then explicit linked constraints using the existing DAG.
Receipt bindings intersect; explicit replacement requires an ancestor marked
replaceable, the same dataset and one identical field, never locked. Multi-field
expressions cannot claim field replacement. Apply inherited constraints together with
block-local Receipt input through the existing authenticated engine. No silent skip
for incompatible dataset or registry. Locked constraints cannot be removed, retargeted,
weakened or escaped by moving surviving blocks. Provider authorization stays mandatory.
Canonical identity includes meaningful expression/version/dependency inputs; presentation
changes do not recalculate. Preserve duplicate/delete/Undo behavior and direct links.

Presentation owns scope structure; Analytics executes expressions. Move reusable
pure expression canonicalization to the contracts boundary rather than importing
an infrastructure adapter across contexts. No private-table reads or row-wise engine.

| Boundary | Impact | Proof |
|---|---|---|
| Scope/query/schema | compatible-change for new reader; v2 rejects on old reader | actual preserved v1 reader/resolver, byte/hash equivalence and rejection |
| Locks and policy | no relaxation | parent override, links, cycles, move/delete/tamper failures |
| Identity/results | compatible-change | affected blocks change, unrelated/layout retain identity; actual totals |
| UI/persistence | additive hierarchy authoring | real validated apply, save/reopen, effective readable expression and keyboard |

## Stage and acceptance

MS-012-S01 owns contracts, Presentation resolver/service, shared canonical expression
helper, generated API/client, composer scopes/state/builder integration, tests/docs.
- AC-01: versioned v2 scope bindings preserve old inputs and resolve deterministic ancestry,
  direct links and allowed single-field replacement without weakening locks.
- AC-02: affected real calculations and save/reopen pin effective Receipt expressions;
  query invalidation, duplication/deletion and provider authorization remain correct.
- AC-03: existing editor reused at every scope, readable effective/locked context,
  draft/apply separation, explicit backend validation and stale-response protection.
- AC-04: focused backend/frontend/compatibility tests, actual provider browser scenarios,
  local gate, independent boundary review and synchronized docs/evidence pass.

Use disposable real provider/browser fixtures. No full C04, scale or production claim.
Remaining relational, sequence, population, temporal comparison and C05–C11 work
continues under existing authority. Technical acceptance is not workstream completion.

## Canonical bindings

plan_doc: `docs/architecture/planning/milestones/MS-012/plan.md`, v0.1.0.
prompt_pack_dir: `.codex/agents/generated/MS-012`.
stage_ledger: `.codex/delivery/ledgers/MS-012.md`.
Repository prompt-pack/v1 validator and exclusive POSIX updater; manual_sequential
with explicit whole-workstream continuation. Accepted under delegated technical
authority on 2026-10-07. Preserve baseline changes and completed historical journals.
