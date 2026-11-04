---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-005",
  "title": "Composer clause audit and versioned authoring contract foundation",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.0"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/W40-WORKSET-CATALOGUE-INTERACTIONS/report.md",
      "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md#current-state-evidence"
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
        "FILTER-007",
        "FILTER-008",
        "FILTER-009",
        "FILTER-010",
        "FILTER-011",
        "FILTER-012",
        "FILTER-013",
        "FILTER-014",
        "FILTER-015",
        "FILTER-016",
        "FILTER-017",
        "FILTER-018",
        "COMPARE-001",
        "COMPARE-002",
        "COMPARE-003",
        "COMPARE-004",
        "COMPARE-005",
        "COMPARE-006",
        "COMPARE-007",
        "COMPARE-008",
        "COMPARE-009",
        "COMPARE-010",
        "COMPARE-011",
        "COMPARE-012",
        "COMPARE-013",
        "BLOCK-BUILDER-001",
        "BLOCK-BUILDER-002",
        "BLOCK-BUILDER-003",
        "BLOCK-BUILDER-004",
        "BLOCK-BUILDER-005",
        "BLOCK-BUILDER-006",
        "BLOCK-BUILDER-007",
        "BLOCK-BUILDER-008",
        "BLOCK-BUILDER-009",
        "PIVOT-001",
        "PIVOT-002",
        "PIVOT-003",
        "PIVOT-004",
        "PIVOT-005",
        "PIVOT-006",
        "PARAM-001",
        "PARAM-002",
        "PARAM-003",
        "PARAM-004",
        "PARAM-005",
        "ANALYTICAL-DOC-001",
        "ANALYTICAL-DOC-002",
        "ANALYTICAL-DOC-003",
        "ANALYTICAL-DOC-004",
        "ANALYTICAL-DOC-005",
        "ANALYTICAL-DOC-006",
        "ANALYTICAL-DOC-007",
        "ANALYTICAL-DOC-008",
        "ANALYTICAL-DOC-009",
        "ANALYTICAL-DOC-010",
        "ANALYTICAL-DOC-011",
        "ANALYTICAL-DOC-012",
        "ANALYTICAL-DOC-013",
        "ANALYTICAL-DOC-014",
        "ANALYTICAL-DOC-015",
        "CHART-001",
        "CHART-002",
        "CHART-003",
        "CHART-004",
        "CHART-005",
        "CHART-006",
        "CHART-007",
        "CHART-008",
        "CHART-009",
        "CHART-010",
        "CHART-011",
        "CHART-012",
        "CHART-013",
        "CHART-014",
        "CHART-015",
        "CHART-016",
        "CHART-017",
        "CHART-018",
        "CHART-019",
        "CHART-020",
        "CHART-021",
        "FOCUS-001",
        "FOCUS-002",
        "FOCUS-003",
        "FOCUS-004",
        "FOCUS-005",
        "FOCUS-006",
        "FOCUS-007",
        "FOCUS-008",
        "FOCUS-009",
        "FOCUS-010",
        "FOCUS-011",
        "FOCUS-012",
        "DASHBOARD-001",
        "DASHBOARD-002",
        "DASHBOARD-003",
        "DASHBOARD-004",
        "DASHBOARD-005",
        "DASHBOARD-006",
        "DASHBOARD-007",
        "DASHBOARD-008",
        "DASHBOARD-009",
        "DASHBOARD-010",
        "DASHBOARD-011",
        "DASHBOARD-012",
        "REPORT-001",
        "REPORT-002",
        "REPORT-003",
        "REPORT-004",
        "REPORT-005",
        "REPORT-006",
        "REPORT-007",
        "REPORT-008",
        "REPORT-009",
        "REPORT-010",
        "REPORT-011",
        "REPORT-012",
        "REPORT-013",
        "REPORT-014",
        "REPORT-015",
        "REPORT-016",
        "REPORT-017",
        "REPORT-018",
        "REPORT-019",
        "REPORT-REFRESH-001",
        "REPORT-REFRESH-002",
        "REPORT-REFRESH-003",
        "REPORT-REFRESH-004",
        "REPORT-REFRESH-005",
        "REPORT-REFRESH-006",
        "REPORT-REFRESH-007",
        "BRAND-001",
        "BRAND-002",
        "BRAND-003",
        "BRAND-004",
        "BRAND-005",
        "BRAND-006",
        "BRAND-007",
        "BRAND-008",
        "BRAND-009",
        "I18N-001",
        "I18N-002",
        "I18N-003",
        "I18N-004",
        "I18N-005",
        "I18N-006",
        "I18N-007",
        "I18N-008",
        "I18N-009",
        "I18N-010",
        "I18N-011",
        "A11Y-001",
        "A11Y-002",
        "A11Y-003",
        "A11Y-004",
        "A11Y-005",
        "A11Y-006",
        "A11Y-007",
        "A11Y-008",
        "A11Y-009",
        "A11Y-010",
        "REPORT-PERF-001",
        "REPORT-PERF-002"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-005/DEC-01",
    "ADR-0007"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-005.md"
  }
}
---
# MS-005 — Composer contract foundation (C01)

## 1. Result and boundaries

Parent: [WS-004 v0.2.0](../../directions/DIR-004/workstreams/WS-004.md).
Authority: [owner continuation](../../../../../.codex/delivery/evidence/WS-004/owner-continuation-2026-10-07.md).
The owner accepted C01–C11 and delegated technical decomposition and sequential
execution. This v0.1.0 bounded plan is accepted by that delegated technical decision,
not by a fabricated separate owner review. Existing product holds remain unchanged.

Before: generated single-page v1/v2 reports, no arbitrary authored graph input.
After: all 169 clauses have explicit assertions, evidence strength, provider and
remaining proof; a selected closed versioned chart/table authoring foundation has
positive/negative and legacy fixtures; C02 has an exact compatibility contract.
No new API writer, production migration, browser feature or complete-target claim.

Preserve existing v1/v2 types/readers, metrics, Identity checks, repositories,
ChartSpec/compiler and pilot UI. No dependency, branch, worktree, publication,
Goal or parallel implementation agent is needed.

Current-state evidence: [C01 entry audit](../../../../../.codex/delivery/evidence/WS-004/C01-entry-audit.md)
and the serving checkout at HEAD 86055ce732640ebe68fd5415a55f7bbde3499181 with
recorded foreign changes. All machine-source IDs in metadata are audit inputs;
only ANALYTICAL-DOC-001/002/004/014/015, BLOCK-BUILDER-001/004/006/008 and REPORT-018
have a contract-foundation implementation subset in this milestone.

| Dependency | Provider/output | Needed before | Current evidence |
|---|---|---|---|
| D01 | Presentation current v1/v2 readers and ports | entry | current files and 63 contract/unit checks in entry audit |
| D02 | Analytics workspace query/result contracts | schema design | three-metric bounded provider; universal capabilities must be audited |
| D03 | Identity access policy, artifact admission | future C02 writer | existing seams, not new-writer proof |
| D04 | Forecasting, Research, Pivot, template/refresh providers | affected later acceptance | audit status/holds must be explicit; do not fabricate provider output |

## 2. Implementation decisions

| Decision | Selection / rationale | Compatibility and recovery | Required proof |
|---|---|---|---|
| DEC-01 | Technical completion/continuation delegated in WS-004/DEC-06 | No repeated owner checkpoint for this plan; retain material product escalation | Honest checks and receipt |
| DEC-02 | New closed versioned authoring contract; do not relax legacy DTOs | Old bytes and dispatch stay unchanged; no persisted writes in C01 | old fixtures, unknown-version rejection, strict nested fields |
| DEC-03 | Stable composition IDs and placements separate from analytical query | Presentation owns hierarchy; Analytics owns normalized inputs/results; no formulas or SQL in composition | graph/order/reference validation, layout-independent query identity |
| DEC-04 | Start with typed chart/table provider support and extensible versioned envelope | Unsupported provider block types are explicit audit gaps; no phantom supported union | strict capability tests and complete provider inventory |

Alternatives: adding UI-only blocks cannot persist independently; relaxing v2
changes already-supported validation and old-reader semantics. A separate service
or persistence store adds no needed boundary. Keep the modular monolith and one
future repository path. Full wire/API/save/view version and migration design is
recorded in the stage design output before C02 implementation. No production
state changes occur here, so runtime rollout/alerts are future-writer obligations.

## 3. Work breakdown

| Stage | Result | Dependencies | Owned zones | Later consumer |
|---|---|---|---|---|
| MS-005-S01 | 169-clause audit, closed foundation DTO/fixtures, compatibility/recovery design and C02 entry evidence | none | contracts/presentation, focused tests, existing planning/authoring documentation, own evidence | C02 |

One executor; old MS-004 claim/history are foreign. Use the exclusive updater for
this new journal. Review has no implementation ownership or parallel topology.

## 4. Acceptance and proof

| Criterion | Observable proof | Boundary / authority |
|---|---|---|
| AC-01 | 169 unique exact source IDs; each has assertions, owner, current evidence/gap and next proof | complete audit, not 169 implemented clauses; technical |
| AC-02 | Valid chart/table graph round-trips; duplicate/orphan/cyclic or unsafe content rejected; stable IDs and deterministic reading order | pure DTO/contract tests; technical |
| AC-03 | V1/v2 fixtures remain readable byte-preservingly; new schema dispatched separately; result identity excludes placement | old and new contract tests; no DB/API migration claim |
| AC-04 | Design specifies save/view/version negotiation, CAS/replay, access, migration/rollback and provider holds; required review findings resolved | architecture/contract evidence; actual writer and disposable DB/browser proof required in C02 |
| AC-05 | Focused tests/lint, docs links/index and local profile pass; canonical receipt names exact outputs | source/local checks; no release proof |

Tests-only execution is appropriate for the unmounted pure contract foundation:
there is no API route or persistent writer. C02 cannot claim runtime compatibility
from this acceptance. New security-boundary implementation requires independent
review before writer activation; unresolved review gaps cannot be called ready.

## 5. Execution and repair envelope

Delegate reversible schema/code/test decisions and same-scope repairs. Preserve
foreign changes and existing calculations. Escalate only new material product
semantics or prohibited actions. Full 100 x 30 scale and concurrency budgets remain
C10 evidence, not an invented new limit. Keep legacy hard limits in legacy readers.
No blanket library install or schema backfill. No secrets/raw provider payloads in
evidence. Update the existing analytical authoring contract only with this bounded
contract's actual state and proof; maintain indexes and reciprocal parent links.

## 6. Execution artifact binding

- Plan: this accepted v0.1.0; exact digest in prompt and journal.
- Prompt directory: `.codex/agents/generated/MS-005`.
- Journal: [MS-005](../../../../../.codex/delivery/ledgers/MS-005.md).
- Profile: `prompt-pack/v1`, repository `validate_prompt_packs` and `stage_ledger`;
  immutable `prompt-pack-receipt/v1`.
- Claim: current POSIX flock/session-owned CAS/fsync/atomic-replace updater;
  bound capability evidence in the journal, rechecked at claim.
- Mode: `manual_sequential` per stage; explicit whole-plan delegation authorizes
  continuation into the next independently prepared/validated unit, without Goal.

## 7. Decisions and history

| Version | Date | Decision/source |
|---|---|---|
| 0.1.0 | 2026-10-07 | Delegated C01 technical decomposition under WS-004/DEC-06; accepts this exact bounded plan |

No material owner question is outstanding for C01. Provider holds limit later
outcomes, not this audit. Execution state and final technical closure live only
in the journal, not this plan.
