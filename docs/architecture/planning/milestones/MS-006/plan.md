---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-006",
  "title": "Persistent multi-block chart and table composer",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.1"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-005/MS-005-S01/report.md",
      ".codex/delivery/evidence/MS-005/MS-005-S01/composer-design.md"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5",
      "ids": [
        "ANALYTICAL-DOC-001",
        "ANALYTICAL-DOC-002",
        "ANALYTICAL-DOC-004",
        "ANALYTICAL-DOC-014",
        "ANALYTICAL-DOC-015",
        "BLOCK-BUILDER-001",
        "BLOCK-BUILDER-004",
        "BLOCK-BUILDER-006",
        "BLOCK-BUILDER-008",
        "REPORT-001",
        "REPORT-018",
        "CHART-001",
        "CHART-002",
        "CHART-010",
        "CHART-013",
        "A11Y-001",
        "A11Y-005"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-006/DEC-01",
    "ADR-0007"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-006.md"
  }
}
---
# MS-006 — Persistent multi-block vertical slice (C02)

## 1. Result and authority

Parent: [WS-004 v0.2.1](../../directions/DIR-004/workstreams/WS-004.md).
[Owner continuation](../../../../../.codex/delivery/evidence/WS-004/owner-continuation-2026-10-07.md)
delegates this exact technical decomposition and sequential execution. Accepted
v0.1.0 under that authority; no invented separate owner checkpoint. One executor,
read-only independent review; no Goal or parallel implementation.

Before: C01 has an unmounted strict graph and compatibility design. After: a user
can create four independent charts and two tables, share compatible results, edit
one block without changing others, save/reopen exact definitions/layout through
the real API, and recover local failures. A table needs no chart. Legacy originals,
metric rail/worksets and exact snapshots remain intact; deterministic read-only
single-result projection does not imply lossless conversion of an entire rail.

New runtime capability is workbook_report, retail metric-workspace/v2 charts and
tables only. Full profiles, filters, pivot, interactions, publication and scale
remain later outcomes; Forecasting hold persists. No dependencies, production
migration, retained data reset, external publication or deployment is authorized.

## 2. Current evidence and dependencies

| ID | Provider / source | Evidence | Needed before / consumer |
|---|---|---|---|
| D01 | MS-005 v0.1.0; [C01 report](../../../../../.codex/delivery/evidence/MS-005/MS-005-S01/report.md) | accepted journal, 99 Presentation tests; unmounted schema | entry / composer |
| D02 | Analytics WorkspaceResults public port, normalize/apply/verify | existing source and 51 tests; new integration still unproved | real API acceptance / Presentation |
| D03 | Identity guards, artifacts, Presentation PostgreSQL repository | existing seams; current 0013 migration head is unrelated identity work | persistence / writer |
| D04 | ADR-0007, PilotDocument, shared chart compiler | existing shell/compiler; direct v2 renderer divergence located | frontend / no new compiler fork |
| D05 | synthetic owned PostgreSQL harness | existing fixture, availability checked at execution; never target retained DB | DB and browser proof |

All source is from serving c67c checkout at recorded baseline plus preserved foreign
changes. The old MS-004 journal is not part of this execution and is never edited.

## 3. Decisions and contract impact

| ID | Decision / delegated basis | Impact and recovery | Proof |
|---|---|---|---|
| DEC-01 | Follow C01 versioned design; route `/api/reports/composer/v1`, `analytical-authoring/v1`, `composed-report/v1` | additive API; old clients receive authorized unsupported-version errors for new documents | generated contracts and old/new matrix |
| DEC-02 | Reuse Presentation document/version tables and ports; additive migration after inspected head | new writer incompatible with old CHECK; reader/schema before writer; downgrade refuses new rows | disposable migration/rollback, CAS/replay/crash/revoke |
| DEC-03 | Save definitions without hidden compute; apply uses Analytics policy-aware identity | local block pending/error states; no stale result reuse after semantic edits | independent loading, races, shared chart/table reuse |
| DEC-04 | One normalized builder and block renderer in accepted pilot shell | preserve legacy UX and unchanged originals; explicit projection fallback | real browser scenarios, keyboard and narrow regression |

[C01 design](../../../../../.codex/delivery/evidence/MS-005/MS-005-S01/composer-design.md)
is the detailed integration/migration contract. If a companion view is introduced,
it must use composer-view/v1; do not reinterpret SavedViewV1. C02 draft snapshots
may carry pending results; they are not published analytical snapshots. Current
authorization always precedes response/replay; creator-only editing is additional.
No whole-product acceptance or production rollout is inferred from local proof.

## 4. Work breakdown and ownership

| Stage | Result | Dependencies | Owned areas | Consumer |
|---|---|---|---|---|
| MS-006-S01 | Complete C02 API/persistence/client/UI vertical slice and scenario repair | C01 accepted | Presentation contracts/application/adapters; reports API; web composer/localization/shared chart compiler; additive migration; focused tests/docs/evidence | C03–C11 |

One stage keeps integration acceptance indivisible. Reversible implementation
choices, focused repairs and technical acceptance are delegated. Preserve all
foreign hunks; inspect shared files immediately before editing. No cross-context
private table access, client business calculations, unsafe HTML/options or secrets.

## 5. Acceptance and verification

| Criterion | Required observed result |
|---|---|
| AC-01 | Closed API DTO/OpenAPI/generated client; authorized prepare/apply/save/latest/exact routes; unsupported old-reader handling |
| AC-02 | Real PostgreSQL saves/reopens exact graph/IDs; immutable snapshots; creator/CAS/replay/deny/revoke/crash checks; additive migration and non-destructive rollback refusal |
| AC-03 | Builder subject/product → metrics/grain → supported dimensions/period; add/copy/delete at explicit destinations; selection/settings/loading/error/retry are block-local |
| AC-04 | Browser creates four distinct charts and two tables, side-by-side and standalone table; compatible chart/table avoids duplicate compute; save/reopen exact layout and definitions |
| AC-05 | Legacy reports deterministically project selected result without loss of old rail/worksets/original snapshots; existing editor and legacy tests preserved; layout changes do not compute |
| AC-06 | Independent implementation review resolved; focused backend/frontend/real-API/browser checks and local gate pass; exact evidence/limits and reciprocal docs links maintained |

Use tests first for important behavior failures. Reuse current evidence only when
unchanged. Run owned synthetic fixture for database and browser proofs, never
reset or migrate retained workspace. Match evidence to exact backend/frontend
build. Record failed/skipped/unavailable checks honestly. No fixed numeric SLO is
invented; runtime budgets/large-scale mixed load belong to C10.

## 6. Execution binding and history

Plan: this accepted v0.1.0. Pack: `.codex/agents/generated/MS-006`.
Journal: [MS-006](../../../../../.codex/delivery/ledgers/MS-006.md), sole state owner.
Profile: prompt-pack/v1. Exclusive updater: repository stage_ledger CLI;
manual_sequential, one allowed stage, immutable receipt. Owner delegation permits
continuation to C03 after technical completion, without Goal or repeated approval.

| Version | Date | Decision |
|---|---|---|
| 0.1.0 | 2026-10-07 | C02 bounded technical decomposition accepted under WS-004/DEC-06; no changed eleven-outcome scope |
