---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-013",
  "title": "C04 explicit previous and custom period comparison",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.9"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-012/MS-012-S01/report.md"
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
    "MS-013/DEC-01",
    "MS-013/DEC-02"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-013.md"
  }
}
---
# MS-013 — explicit period comparison

## 1. Result, evidence and authority

Parent: [WS-004 v0.2.9](../../directions/DIR-004/workstreams/WS-004.md).
The [owner addendum](../../../../../.codex/delivery/evidence/WS-004/owner-continuation-addendum-2026-10-07.md)
authorizes this sequential technical design/implementation and acceptance on proof.
Current observations: workspace query/result supports none/previous_year_same_dates;
workspace_calculation normalizes UTC, exact pinned calendar and per-day legacy mapping.
The older Analytics TimeComparison domain/API supports previous-year enum values but
is a distinct legacy path; it is not the mounted composer calculation provider.
BusinessCalendarProfile v1 is deliberately UTC/month-based with Monday weeks, selected
in MS-004 D04. Do not reinterpret that profile, old comparison modes or old stored data.

After this stage, composer blocks and inherited context can select previous_period
or custom_period, calculate actual authorized current/comparison values, disclose
resolved ranges and limitations, and save/reopen immutable result references.
Included: versioned additive input/result, backend date/bucket resolution and coverage,
UI authoring and rendering, inherited override, identity and proof. Other calendar
profiles, other previous-year adapters and population comparison remain future C04
work. This is no waiver and no full C04/WS-004 closure.

## 2. Architecture decisions

DEC-01 (accepted under delegated technical authority): add optional versioned temporal
settings to workspace inputs and context overrides, with a distinct immutable v2
comparison artifact embedded in the existing manifested result. Keep absent input and
legacy alignment unchanged. Do not extend the meaning of the old alignment enum or
label a new mode as last-year. Presentation owns settings/inheritance; Analytics owns
resolution, values and deltas; Semantic owns the pinned calendar; Artifact/result
storage and PostgreSQL keep their current ownership and transaction semantics.

Keeping only the current design cannot satisfy previous/custom periods. Reusing the
legacy alignment enum would reinterpret old readers and is rejected. The selected
additive seam isolates new semantics without another service, database or dual writer.
V2 artifacts pin normalized settings, both resolved periods/buckets, calendar/ref,
timezone, policy/request/filter/metric identity, coverage and limitation reasons.
The parent result manifest protects the embedded artifact; no separate mutable truth.

DEC-02 (accepted): previous_period explicitly chooses calendar_bucket_count or
local_date_duration. Calendar count requires a range aligned to full selected buckets,
then takes the immediately preceding equal number of calendar/fiscal buckets. Custom
range uses the preceding equal number of local dates. custom_period stores an explicit
comparison interval, may disclose overlap/different duration, and never normalizes
per-day silently. Both intervals obey existing bounded range limits. Request timezone
comes from the pinned provider (UTC here); unsupported profiles/modes fail before Run,
not by approximation. Full timezone/DST capabilities cannot be inferred from this
UTC-only provider. Legacy same-date leap behavior remains byte/hash-equivalent.

Incomplete-period policy is explicit: exclude makes incomplete comparisons unavailable;
explicit_partial retains observed values/deltas with partial status and reasons;
comparable_elapsed_days selects an explicitly disclosed leading complete elapsed-date
prefix of both intervals. No unknown becomes zero. A zero/unknown denominator gets
an unavailable relative delta reason. The three current measures are EUR, receipt and
EUR/receipt, not percentage rates; percentage-point output is not fabricated.
Calendar-aligned unequal-length bucket totals remain raw registered measure values,
with duration difference disclosed. Custom unmatched buckets remain unavailable.

| Boundary | Impact | Proof |
|---|---|---|
| Optional input and inherited context | compatible-change for old readers' old inputs; explicit rejection of new fields | preserved actual reader and normalizer/output fixtures |
| New result artifact/cache identity | compatible-change in new readers; no old namespace reinterpretation | exact settings/calendar/policy effects, layout invariance, integrity/save/reopen |
| Provider/permission | no access expansion | both periods use current authorized inputs and same mandatory filters |
| Browser | additive modes and truthful series/table disclosure | real values, empty/partial/zero cases, independent blocks and local overrides |

No DB migration, external side effect or new retry path. Existing per-block abort/stale
and save CAS/idempotency semantics remain. Errors are bounded codes without credentials
or raw provider logs. Reader-before-writer rollout; rollback preserves new bytes for
compatible readers. No irreversible transformation or dual-write/backfill is introduced.

## 3. Work and ownership

MS-013-S01 owns analytics temporal DTO/planner/projection, optional workspace contract,
composer scope context/renderer/builder, generated clients, tests and canonical docs.
One executor and one independent read-only boundary review. Preserve foreign/baseline
work, retained data and completed journals. No Goal, parallel implementation, publication,
deploy, production migration or destructive reset.

## 4. Acceptance and proof

- AC-01: bounded previous/custom resolution, leap/month/fiscal/year and invalid range/
  overlap disclosure; explicit incomplete policy and exact Decimal deltas.
- AC-02: current real provider executes both intervals, pinned v2 identity/artifact
  survives save/reopen, current policy and filter restrictions apply to both periods.
- AC-03: block and hierarchy authoring expose mode/basis/dates/policy; rendering shows
  comparison values, deltas and reasons without reusing last-year labels; stale guards.
- AC-04: actual old reader/normalizer behavior unchanged, focused backend/frontend tests,
  disposable real API/browser scenarios, local gates, independent review/docs pass.

Proof is local published retail integration, not full family coverage, performance
SLO or production delivery. Requirements COMPARE-001–011/013 are contributed to only
at this declared provider boundary; remaining assertions stay in WS-004.

## 5. Repair and documentation

Routine implementation choices/fixes are delegated; new product scope or irreversible
tradeoffs remain owner decisions. Synchronize authoring/columnar contract where changed,
parent/dependency links, requirement coverage, indexes and evidence. Do not rewrite
historical receipts. Record failed/skipped/unavailable separately from observed passes.

## 6. Canonical bindings

plan_doc: `docs/architecture/planning/milestones/MS-013/plan.md`, v0.1.0.
prompt_pack_dir: `.codex/agents/generated/MS-013`.
stage_ledger: `.codex/delivery/ledgers/MS-013.md`.
Repository prompt-pack/v1 validator and exclusive POSIX updater; manual_sequential
with explicit whole-workstream continuation, no Goal. Source snapshots and entry
baseline are preserved in MS-013/preparation.

## 7. Decision history and continuation

Version 0.1.0 accepted on 2026-10-07 under WS-004/DEC-06 and current owner addendum.
No material owner input blocks this bounded provider extension. Independent review
and actual proof remain required before stage acceptance. Continue later C04 and
C05–C11 under the same authority; technical milestone completion does not end the task.
