# Criterion amendment — correction 002

Read the [owner amendment](../owner-correction-2026-09-22.md) and retained
[baseline matrix](../criterion-matrix.md). This table supersedes only affected
calendar UI statements. Baseline review001 is historical, not current acceptance.

| Criterion | Current correction proof and reuse boundary |
|---|---|
| AC-01/03/04 | Real fiscal multi-workset scenario uses an already configured April-start company calendar; six independent cards and same/different-store result identities, four financial quarters, exact server chart/table values and fiscal labels. Six-grain RU workflow remains. Existing arithmetic/source-intake SQL corpus remains unchanged. |
| AC-05/06 | Old v1 and new v2 exact snapshots remain equal; reopen does not calculate. Prior persistence/atomicity/compatibility corpus is reused because its backend sources did not change. |
| AC-07/09 | Reader cannot configure/adopt a calendar; existing reader view-only Save and real logout clearing remain. Backend per-resource and session authorization, CSRF and JSON-generation guards are unchanged. Prior late-body/reload race evidence remains within that unchanged logic. |
| AC-08 | Same generated native pilot, RU/EN and keyboard scenarios, current 1920 and 400 screenshots. No visual redesign. Administration no longer opens calendar setup in the report. |
| AC-11 (amended) | No report settings form, fiscal start-month/year-label controls, current/pinned technical labels or adoption action. No current-calendar GET on report reload. Company calendar setup occurs only in synthetic fixture preparation, not in report UX. Server once-only setup enforcement and future administrator page are explicitly deferred; old API version/CAS proof is compatibility evidence, not proof of this target lifecycle. |
| AC-10 | Corrected local demonstration is ready for review only after validation. Owner request to fix is not acceptance of the finished result. |

AC-02 and unaffected baseline requirements retain their exact previous evidence.
No claims about production, release, C02 goals, C03 shared worksets or auth speed.
