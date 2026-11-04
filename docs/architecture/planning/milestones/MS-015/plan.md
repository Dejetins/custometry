---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-015",
  "title": "C04 immutable time-zone calendars",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.11"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-014/MS-014-S01/report.md"
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
    "MS-015/DEC-01",
    "MS-015/DEC-02"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-015.md"
  }
}
---
# MS-015 — immutable time-zone calendars

## 1. Outcome and authority

Parent [WS-004 v0.2.11](../../directions/DIR-004/workstreams/WS-004.md) and the
[owner continuation](../../../../../.codex/delivery/evidence/WS-004/owner-continuation-addendum-2026-10-07.md)
authorize this technical decomposition and acceptance. COMPARE-001–013, the human
mirror, accepted authoring contract and MS-014 evidence govern this bounded C04 unit.
The mounted provider currently requires UTC and month-based v1 calendars. This unit
adds explicitly selected IANA-zone month-based calendars with pinned rules, local
receipt dates, truthful elapsed duration and conservative source completeness.
V1 wire bytes/hashes and all persisted calendar references remain unchanged.

Other calendar families, population providers and C05–C11 remain required work.
No entire compound capability is accepted by completion of this milestone.

## 2. Accepted decisions and contracts

DEC-01: Semantic owns new business-calendar/v2 input and stored profile. Input carries
an IANA name and explicit boundary/coverage policies. A Semantic infrastructure adapter
loads TZif from the already locked tzdata 2026.3 package through a public port. Stored
immutable profile embeds bounded TZif bytes, their hash and package version. Profile
hash therefore pins rules; later host or package changes cannot reinterpret an old
calendar. Calculators parse those bytes in memory. No domain/application filesystem
access and no current-zone lookup during replay. Never accept caller-supplied rule
bytes at the public update endpoint. Existing JSON persistence needs no migration.
The original actor-bound request defines idempotency, and existing CAS remains atomic.

DEC-02: local dates use half-open midnight boundaries. Repeated midnight chooses the
earliest valid instant; nonexistent midnight or skipped dates fail with a bounded
capability reason before calculation, rather than shifting silently. Validate every
selected day, including comparison dates. Elapsed seconds use UTC instants (23/25-hour
DST days), while calendar duration counts local dates. Receipt timestamps remain
aware instants and data-as-of remains UTC. Registered receipt_date filter semantics
remain UTC and are disclosed separately. V2 coverage is conservative: a local day is
covered/complete only when every intersecting UTC source-calendar day is present/
complete. The result discloses that coverage basis. Raw metric totals are not duration
normalized. Previous/year mapping uses the same pinned zone on both sides.

DEC-03: administrator settings create a new default immutable version. The composer
lets an author explicitly select the current company calendar for a block; unchanged
edits preserve pinned references and ancestor locks still reject unauthorized
replacement. New blocks may use current default under existing authoring behavior.
UI displays IANA zone, UTC boundaries and elapsed hours where comparison is shown.
No automatic adoption by old reports, no source data rewrite or deployment.

| Boundary | Impact | Proof |
|---|---|---|
| Calendar input/stored profile | compatible additive v2; old readers reject v2 | strict version dispatch, invalid zone/rule injection, actual v1 reader/golden |
| Semantic persistence/identity | compatible JSON payload, same CAS/idempotency | real API old/new versions, permissions, replay/conflict |
| Analytics context | additive zone support, unchanged UTC behavior | DST 23/25h, edge instants, conservative missing coverage, skipped dates, pinned replay |
| Browser authoring | explicit opt-in | administrator save, block adoption, actual values and Save/reopen |

Reader-before-writer rollout; rollback preserves v2 bytes for compatible readers.
Unsupported midnight/date mappings fail explicitly. Python zoneinfo.from_file is the
standard in-memory parser; reference https://docs.python.org/3/library/zoneinfo.html.

## 3. Ownership and implementation

MS-015-S01 owns Semantic profile/ports/adapter and API composition, Analytics local
calendar projection, generated clients, composer calendar controls, focused tests and
documentation. One executor and one independent read-only reviewer; no parallel
implementation, Goal, publication, production migration or destructive cleanup.
Retained runtime/data and existing completed journals/receipts are preserved.

## 4. Acceptance

- AC-01: immutable v2 rules, bounded validation, real Semantic CAS/permissions/replay.
- AC-02: local grouping and DST durations, conservative coverage and explicit invalid
  boundaries; actual v1 golden outputs unchanged.
- AC-03: real mounted settings/adoption, truthful rendered zone/duration and persistence.
- AC-04: focused backend/frontend/types/static checks, real disposable browser/API,
  local gate, independent review and reciprocal docs/evidence complete.

Proof covers the local published retail provider and month-based v2, not production,
SLOs, other calendar families or the complete workstream.

## 5. Execution and documentation

Use exclusive journal transactions and immutable receipt; no direct active-ledger
mutation. Routine technical fixes and local disposable infrastructure are authorized.
Maintain authoring contract, matrix/parent links/navigation and exact evidence.
Keep raw traces/credentials temporary and only sanitized synthetic evidence durable.

## 6. Bindings

plan_doc: `docs/architecture/planning/milestones/MS-015/plan.md`, v0.1.0.
prompt_pack_dir: `.codex/agents/generated/MS-015`.
stage_ledger: `.codex/delivery/ledgers/MS-015.md`.
Existing prompt-pack/v1 POSIX updater; manual_sequential with whole-WS continuation.

## 7. Decision history

Version 0.1.0 technically accepted under WS-004/DEC-06 and owner continuation on
2026-10-07. Stage acceptance still requires all declared proof; then continue C04
and C05–C11 under existing authority without stopping at this milestone.
