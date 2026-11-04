---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-007",
  "title": "Document hierarchy, profiles and reversible layout authoring",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.2"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-006/MS-006-S01/report.md",
      ".codex/delivery/ledgers/MS-006.md"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5",
      "ids": [
        "ANALYTICAL-DOC-001",
        "ANALYTICAL-DOC-002",
        "ANALYTICAL-DOC-003",
        "ANALYTICAL-DOC-005",
        "ANALYTICAL-DOC-007",
        "ANALYTICAL-DOC-010",
        "ANALYTICAL-DOC-012",
        "ANALYTICAL-DOC-014",
        "ANALYTICAL-DOC-015",
        "DASHBOARD-006",
        "REPORT-001",
        "REPORT-018",
        "A11Y-001",
        "A11Y-005"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-007/DEC-01",
    "ADR-0007"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-007.md"
  }
}
---
# MS-007 — C03 document structure and layouts

## 1. Result and boundaries

Parent: [WS-004 v0.2.2](../../directions/DIR-004/workstreams/WS-004.md).
[Owner delegation](../../../../../.codex/delivery/evidence/WS-004/owner-continuation-2026-10-07.md)
accepts technical decomposition, implementation and sequential acceptance for C01–C11.
This exact v0.1.0 is accepted under that delegation. One executor; independent
read-only review. No Goal, publication, dependency installation or parallel coding.

Before: accepted C02 persists arbitrary graph structure but renders every page and
only exposes one grid page with chart/table authoring. After: users manage optional
chapters, pages, nested sections and blocks, choose presentation profile/layout,
move/resize/copy/hide/lock/group, use Undo/Redo and navigate a searchable page index.
Only the active page mounts. Structure/layout changes retain result identity.

Included: shared presentation for dashboard/workbook_report/narrative_research,
grid/table-first flow/narrative, density, chart/table nodes and existing exact-save
path. Profiles do not grant Dashboard ACL, live refresh, Research findings lifecycle,
publication, filters, pivots or content not implemented until C04–C09. Those accepted
later outcomes remain mandatory; profile structure alone does not close them.

| Evidence / dependency | Current observation | Consumer / proof |
|---|---|---|
| D01 MS-006 v0.1.0 | [C02 report](../../../../../.codex/delivery/evidence/MS-006/MS-006-S01/report.md), accepted [journal](../../../../../.codex/delivery/ledgers/MS-006.md) | existing API/store/result/auth foundation |
| D02 composer DTO/service | nested graph validators, strict closed models; profile currently workbook-only | evolve explicit authoring capability; old payload fixture compatibility |
| D03 PilotDocument + ComposerWorkspace | same renderer/shell; all pages mount; no structural controls/history | active-page UI and input-independent layout operations |
| D04 machine/human/UI blueprints | exact selected IDs above, UI 8.5.3/8.5.4 | observable C03 clauses; no invented business rules |

Current implementation sources: [analytical-authoring contract v19](../../../../contracts/analytical-authoring-contract.md) and
[Web source contract v28](../../../ui/custometry-web-implementation-source-contract-v1.md).
The parent v17 reference is historical; these inspected versions govern this stage.

## 2. Implementation decisions

| Decision | Current -> accepted target | Boundary/compatibility | Recovery/proof |
|---|---|---|---|
| DEC-01 graph metadata | add optional hide/lock/copy lineage on page/section/block; use existing chapters and nesting for groups | authoring contract additive pre-release evolution; old omitted fields still read. Generated clients updated together; no old-client forward compatibility claim | strict invalid refs/lineage, old snapshot fixture read, immutable version save |
| DEC-02 structure operations | pure graph commands maintain globally unique IDs, parent/order and valid grid placement | new UI; IDs/results unchanged on move; duplicate IDs fresh and source copy independent | command invariants + actual API roundtrip |
| DEC-03 history | transient bounded Undo/Redo of authoring inputs, every edit creates local draft state; Save records immutable revision | no published-history mutation, no localStorage persistence | undo delete/resize/move; dirty/baseline preserved; authorization reset clears memory |
| DEC-04 profile/layout | three presentation profiles share same contracts/renderers; grid twelve columns, flow/narrative ordered blocks | no new analytical query or resource ownership semantics; creator restriction retained for all current personal compositions | profile/layout save/reopen, stable query identity and no Apply request |
| DEC-05 navigation | ordered chapter/page index, tabs with overflow/search, active-page-only mount; exact snapshot/page route | existing allowed page/view query keys; unauthorized data never exposed by routing | keyboard/overflow/deep-link and hidden-page reader behavior, RU/EN and 200% zoom |
| DEC-06 locks/hide | authoring safety flags, not ACL; inherited locks require explicit unlock, hidden nodes remain author-manageable but omitted from reader surface | cannot broaden Identity/source permissions; no server security claim for presentation lock | locked edit/drag rejection; read-only snapshot lacks author controls |
| DEC-07 operations UI | pointer drag/drop with validity feedback and equivalent move/resize/group commands | accessible deterministic DOM order independent of coordinates; retain accepted pilot tokens | real keyboard + drag + narrow-width smoke |

No event, analytical computation, dependency or database schema change is needed:
composition is already versioned JSON with closed DTO validation. Existing artifact,
CAS/replay and current authorization checks remain; any newly discovered dependency
must be resolved before claiming its criterion. Resource-scale qualification remains
C10; no small hard cap is imposed on pages/blocks. History memory may be bounded
independently of document cardinality and must be documented/tested.

## 3. Work and ownership

One stage, MS-007-S01, implements contracts/state/UI then verifies their integrated
behavior, repairs failures and synchronizes documentation. Owned zones:
packages/contracts, packages/presentation/application/composer.py, reports API,
apps/web/src/features/reports, tests, affected docs/blueprint inventory and this
milestone triad/evidence. Preserve foreign changes and completed C01/C02 artifacts.
No other implementation writer. C04 consumes this stable hierarchy.

## 4. Acceptance and proof allocation

All criteria are proved by MS-007-S01 and technically accepted under the owner
whole-plan delegation, with independent implementation review before acceptance.

| ID | Observable criterion / exact proof surface |
|---|---|
| AC-01 | Strict graph metadata/profiles, old omitted-field compatibility, valid hierarchy/copy lineage/order/placements; focused Presentation tests and generated contracts |
| AC-02 | Chapter/page/nested-section creation, rename/reorder/group, duplicate fresh IDs, hide/lock/unlock, move/delete with Undo/Redo; pure operation invariant tests and real browser |
| AC-03 | Grid arbitrary valid spans and position/resize, table-first flow/narrative and density; pointer drag/drop valid/rejected states plus keyboard/menu equivalents, preserving DOM reading order |
| AC-04 | Searchable grouped page index, tab overflow/keyboard, active-page-only blocks, exact saved page link; hidden nodes omitted for preview, author controls absent, access rechecked |
| AC-05 | Real API/browser save/reopen identical graph including profile/lineage/flags; layout/history operations trigger no Apply and keep saved result IDs; standalone table and C02 regressions |
| AC-06 | Focused Python/Web tests, TypeScript/generated checks, real disposable API/browser proof, local gate, independent review and synchronized links/versions/evidence |

Commands use the activated local toolchain and `uv run --locked --no-sync`.
Reuse owned disposable C02 harness; extend tests for C03 and rerun affected C02
scenarios. Never write retained user data. Bounded active-page proof is not TEST-INV-101 / V1-AC-049 scale acceptance.
Unit tests alone do not prove runtime;
local browser/API proof does not prove production, full profiles or 100x30 scale.

## 5. Repair, rollout and documentation

Routine reversible implementation choices and in-scope repairs are delegated.
New business thresholds, owner scope changes, unsupported provider policy, install,
production migration and publication need separate authority. No dependencies or
new runtime may be installed to finish this unit. Preserve source artifacts and
redact all credentials/provider payloads. New fields use defaults for older saved
compositions; old exact artifact bytes remain immutable. No destructive rollback.

Synchronize analytical-authoring contract, Web implementation source contract,
localized UI inventory, reciprocal parent/child/dependency links, architecture and
contributor indexes, report/review and immutable receipt. Snapshot bound source
versions before updates. Canonical journal alone records execution state.

## 6. Execution binding

- plan_doc: `docs/architecture/planning/milestones/MS-007/plan.md`, v0.1.0.
- prompt_pack_dir: `.codex/agents/generated/MS-007`.
- stage_ledger: `.codex/delivery/ledgers/MS-007.md`.
- profile: prompt-pack/v1; validate_prompt_packs and repository stage_ledger CLI.
- mechanism: existing POSIX exclusive updater, source-digest capability evidence,
  live preflight/claim before implementation; no direct active journal mutation.
- execution_mode: manual_sequential with owner-authorized whole-plan continuation.

## 7. Decision history

| Version | Date | Decision / authority |
|---|---|---|
| 0.1.0 | 2026-10-07 | C03 bounded technical decomposition accepted under WS-004/DEC-06; no additional owner checkpoint invented |

Final stage has no fabricated successor. After receipt-backed C03 acceptance,
prepare C04 under existing delegation; never treat C03 as whole WS-004 completion.
