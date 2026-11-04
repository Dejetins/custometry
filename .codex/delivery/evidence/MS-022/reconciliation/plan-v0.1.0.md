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
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.18"
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
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-022.md"
  }
}
---
# MS-019 — correlated filters in saved report authoring

## 1. Outcome and authority

Parent [WS-004 v0.2.15](../../directions/DIR-004/workstreams/WS-004.md), whole-workstream
continuation and accepted MS-018 genuine provider authorize the next C04 unit.
Read FILTER-001–013/016–018 and human §6.5, existing authoring/scopes contracts,
MS-018 provider, UI blueprint/target pilot/ADR-0007. Make the published receipt/item
conditions usable in block and hierarchy editors, Apply, immutable Save and reopen.
Expose confirmed-vs-unknown selection limitations in stored results. Preserve v1
payload meaning and MS-016 once-only company calendar policy.

## 2. Decisions

DEC-01: receipt_filter admits an explicit typed receipt-filter/v2 alongside unchanged
v1; old readers fail closed. The v2 provider shares the same normalized scoped AST
for preview and calculation, never Python predicate evaluation. Persist all semantic
and policy dependencies through request/result identity. Existing v1 bytes remain
unchanged when new optional fields are absent. No automatic stored-payload rewrite.

DEC-02: combine hierarchy/link/base predicates into one typed plan. All-v1 uses its
existing canonical combination unchanged. For mixed v1/v2, an explicit provider-
validated legacy registry compatibility reference permits lifting published root
fields without changing field versions/null semantics. Reject mismatches. Rebase
node/child-scope IDs deterministically per binding when composing; preserve within-
child same-row correlation and independent scopes. Locks, links and ancestor rules
remain; field replacement must match one root field and compatible registry meaning,
never weaken a correlated constraint through leaf-name coincidence.

DEC-03: the existing receipt editor keeps v1 editing intact; an explicit related-item
condition starts/upgrades a draft v2 tree using the current catalog. Group fields by
entity; allow same-item conjunction, independent exists/not_exists and Boolean groups,
show readable expression and draft/applied/mandatory state, undo/reset, preview and
backend-validated apply. Stable IDs persist across unrelated edits. Cancellation and
stale response suppression remain. Existing report/calendar controls stay unchanged.

DEC-04: v2 facets remain bounded/searchable and apply current root/store/child namespace
ceilings before counts/pagination. Define the grain explicitly: root field counts
matching receipts; item field counts observed positions within matching receipts.
They are not a completeness or absence certificate. No independent child-root query.
Use the same compiled membership plan and bounded inputs, with final grant recheck.

DEC-05: results include optional versioned receipt selection evidence (dataset-wide
matched/not-matched/unknown/authorized counts, limitations and filter identity).
Amounts/counts are computed only from confirmed members; unknown membership is
explicitly limited/descriptive, including temporal comparisons. Show scope of counts
so dataset preview counts are not mislabeled as period counts. Save/reopen must retain
this evidence and current authorization preflight. No silent zeros for unknown absence.

## 3. Impact, proof and scope

Additive API/query/result/scopes/client contracts; v1 hashes and absent optional bytes
preserved. No migration, production/deploy, financial-calendar policy or Forecasting
change. One executor, existing read-only independent reviewer, manual sequential.

- AC-01: v1 compatibility and strict v2 persisted input/result evidence with current
  provider validation; complete dependency identities and no node loss.
- AC-02: hierarchy/link/base composition, explicit legacy bridge, deterministic IDs,
  field replacement and locks preserve meaning; malformed/mismatched refs reject.
- AC-03: real provider facets/Apply/Save/reopen prove values, unknown limitation,
  root grain, current permissions and bounded execution. Decimal math stays exact.
- AC-04: mounted browser same-item/independent/negative editing, draft undo/reset,
  stale preview, save/reload and locked scope scenarios, plus focused backend/frontend/
  type/local gates and independent review. Visual/runtime evidence remain distinct.

Aggregate, sequence, population nodes and remaining C04/C05–C11 are not waived.
Continue them after this unit, without requesting repeat technical acceptance.

## 4. Bindings and synchronization

plan_doc: `docs/architecture/planning/milestones/MS-019/plan.md`, v0.1.0.
prompt_pack_dir: `.codex/agents/generated/MS-019`.
stage_ledger: `.codex/delivery/ledgers/MS-019.md`.
Maintain parent/requirements/authoring/UI inventory, generated contracts/index and
redacted proof before immutable receipt acceptance. Retained runtime/data preserved.

## 5. Decision history

Version0.1.0 accepted under existing delegated technical authority on2026-10-07.
This is bounded receipt/item authoring, not the complete filter language or workstream.
