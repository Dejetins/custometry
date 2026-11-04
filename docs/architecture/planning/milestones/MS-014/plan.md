---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-014",
  "title": "C04 explicit previous-year policies",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.10"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-013/MS-013-S01/report.md"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5",
      "ids": [
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
        "COMPARE-013"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-014/DEC-01",
    "MS-014/DEC-02"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-014.md"
  }
}
---
# MS-014 — previous-year comparison policies

## 1. Result, sources and authority

Parent [WS-004 v0.2.10](../../directions/DIR-004/workstreams/WS-004.md) and
[owner authority](../../../../../.codex/delivery/evidence/WS-004/owner-continuation-addendum-2026-10-07.md)
authorize sequential technical decisions, implementation, proof and acceptance.
Normative inputs: COMPARE-001–011/013 and human mirror comparison section, accepted
UTC/month-based BusinessCalendarProfile v1, authoring contract and MS-013 evidence.
Current mounted provider has legacy same-date alignment plus new previous/custom
settings/artifact. The older TimeComparison domain is a separate path and is not
proof of mounted date mapping. Previous-year policy fields/mappings are absent from
this mounted settings contract; generic ISO/fiscal/elapsed modes are not authored.

After this stage the mounted composer exposes previous-year same-date, complete
calendar-aligned, ISO-week-aligned, fiscal-period and comparable-elapsed-date modes
with explicit leap/ISO53/incomplete policies. Exact evaluated date sets, mapping,
exclusions, raw values/deltas and reasons survive persistence and render truthfully.
The old alignment remains available and byte/hash-compatible. MS-013 previous/custom
settings/results retain their existing bytes/hashes. No implicit upgrade changes
old stored report meaning.

Scope excludes changing the UTC-only calendar profile or other provider domains;
timezone/DST profiles, population axes and full C04/C05–C11 remain obligations.
This is a bounded implementation sequence, not a waiver of any normative clause.

## 2. Accepted architecture decisions

DEC-01 (delegated technical acceptance): extend versioned v2 settings with explicit
previous-year modes and policies; add an optional resolved date-mapping payload.
Omit new fields for pre-existing modes, preserving their wire/hash behavior. Old
readers reject new mode/field payloads explicitly. Analytics owns mapping/projection,
Semantic owns calendar identity, Presentation owns authoring/inheritance; the current
result manifest remains the immutable owner. No service/database/dual writer added.
Keeping the current subset cannot meet prior-year requirements. Reinterpreting legacy
alignment is rejected because its leap behavior is already persisted.

DEC-02 (accepted): date mapping uses the pinned calendar, never a clock. Same-date
maps matching month/day to prior year; `exclude` removes unmappable leap dates from
both compared sets, while `merge_with_feb_28` explicitly groups current Feb28/29 and
counts comparison Feb28 once. Mapping and unequal counts are disclosed. A requested
`calendar_map` without an applicable provider mapping fails before Run; do not invent
one. Calendar/fiscal-aligned modes require complete selected month/quarter/half/year
buckets and shift the full envelope twelve months, preserving actual leap-month size.
Fiscal mode requires fiscal basis; calendar mode requires calendar basis.

ISO mapping uses previous ISO year, same ISO week/weekday. Missing week53 supports
explicit exclude or explicit-partial: exclude omits unmatched current dates; partial
keeps them with unavailable baseline/coverage. Missing provider calendar_map fails
preflight. No arbitrary fallback to week52. Matched comparison dates are deduplicated
before aggregation; bucket comparison uses current groups plus their exact mapped
dates, preventing drift across Gregorian boundaries. Empty mapping is unavailable,
never zero. Comparable-elapsed-year requires the explicit elapsed policy and uses
the shared leading complete mapped prefix, without substituting a full prior year.
Other incomplete policies retain MS-013 meaning. Definition policy is same pinned
metric/dataset/filter/calendar versions on both sides; no hidden rebase.

The v2 immutable result records mapping/exclusions/policies, precise ranges, evaluated
sets and limitations. Current permissions/metric rules remain outside authorable
comparison settings. CPU aggregation stays backend; browser only formats server data.
No retry/transaction/concurrency change; existing apply abort/stale, save CAS and
persisted scope locks remain. Boundary errors are bounded codes without provider logs.

| Boundary | Impact | Required proof |
|---|---|---|
| New settings/mapping fields | compatible-change for current readers; explicit rejection by older readers | preserved actual reader plus golden previous/custom/legacy outputs |
| Calendar math and totals | additive modes, unchanged prior modes | leap/ISO53/year/fiscal matrix, merge dedupe, empty/partial/elapsed cases |
| Identity/persistence | additive settings/mapping identity | real API save/reopen, pinned artifact, unchanged layout/old inputs |
| UI and inheritance | additive choices with explicit policies | real block/context selection, truthful label/date/coverage values and negative validation |

Rollout is reader-before-writer; rollback preserves new bytes for compatible readers.
No migration/backfill or irreversible transformation is needed. Unsupported calendar
mapping/profile is a capability error, not a reason to approximate or rewrite settings.

## 3. Work and ownership

MS-014-S01 owns temporal contracts/resolver/projection, workspace composition/preflight,
frontend comparison controls/rendering, generated clients, scoped tests and docs.
One executor, one independent read-only boundary reviewer. Preserve foreign changes,
retained data and completed journals/receipts. No Goal, publication/deployment,
production migration, destructive reset or parallel implementation agents.

## 4. Acceptance and proof

- AC-01: all five explicit previous-year modes resolve permitted inputs; leap merge
  is deduplicated, ISO53 policies/invalid alignment fail or disclose exactly; Decimal
  totals and partial/elapsed exclusions remain truthful.
- AC-02: old readers and frozen actual previous/custom/legacy outputs preserve bytes,
  hashes and meaning; all new settings/mapping participate in identity and current
  permission/filter rules protect both sides.
- AC-03: block and inherited editor exposes mode and explicit supported policies;
  actual result values, mapped dates, reasons and persistence survive Save/reopen.
- AC-04: focused backend/frontend/type/static gates, real disposable API/browser,
  local profile, independent review and required docs/navigation pass.

Proof remains the local published retail provider, not other profiles/datasets,
production delivery, SLOs or entire compound requirement acceptance.

## 5. Execution and documentation envelope

Routine code/fixture repairs and reversible technical choices are delegated. Material
new product scope and irreversible changes remain owner decisions. Update authoring
contract, requirement coverage and parent/child/navigation bindings with precise proof.
Keep raw traces/auth/provider payloads temporary; only synthetic sanitized evidence
is durable. Preserve old receipts; do not manually mutate an active canonical ledger.

## 6. Canonical bindings

plan_doc: `docs/architecture/planning/milestones/MS-014/plan.md`, v0.1.0.
prompt_pack_dir: `.codex/agents/generated/MS-014`.
stage_ledger: `.codex/delivery/ledgers/MS-014.md`.
Existing prompt-pack/v1 POSIX exclusive updater; manual_sequential with explicit
whole-WS-004 continuation. No Goal. Baseline and exact reader/golden sources are
retained in MS-014 preparation. No material owner decision blocks this bounded step.

## 7. Decision history

Version 0.1.0 accepted under WS-004/DEC-06 and current owner addendum on 2026-10-07.
Acceptance requires the declared proof. After this unit continue the remaining C04
providers and C05–C11 without treating milestone completion as workstream completion.
