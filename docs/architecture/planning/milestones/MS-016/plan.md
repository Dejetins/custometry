---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-016",
  "title": "C04 once-only calendar policy correction",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.12"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-015/MS-015-S01/report.md"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5",
      "ids": [
        "METRIC-030",
        "COMPARE-002",
        "COMPARE-005",
        "COMPARE-011"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-016/DEC-01",
    "MS-016/DEC-02"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-016.md"
  }
}
---
# MS-016 — restore once-only company calendar policy

## 1. Outcome, authority and correction

Parent [WS-004 v0.2.12](../../directions/DIR-004/workstreams/WS-004.md), continuing
owner authority and normative METRIC-030 authorize this corrective unit. Read the
[2026-09-22 owner amendment](../../../../../.codex/delivery/evidence/MS-004/MS-004-S05/owner-correction-2026-09-22.md),
machine METRIC-030, human Calendar explanation and current authoring contract's
Company calendar correction. MS-015's comparison-focused review missed this affected
requirement: its report-mounted settings/adoption conflict with the prior owner
instruction. Passing functional tests did not prove product conformance. Preserve
MS-015 plan/receipt/evidence as historical observations; this stage supersedes only
its report controls/adoption and repeated-update lifecycle, not its valid DST math.

Remove all company calendar setup/version/adoption controls from reports. Provide
once-only administrator setup in existing UI-ADMIN-004 workspace settings/policies.
Enforce once-only configuration server-side for v1 and v2. Existing versions/results
remain readable and unchanged; reports retain their internal pinned references.

## 2. Accepted technical decisions

DEC-01: revision0 system default means not yet administrator-configured. Any positive
revision means configured, including existing historical multi-version workspaces.
Within the existing pointer row lock, check actor-bound idempotent replay first,
then expected revision, then reject any new configuration if revision>0 with
CALENDAR_ALREADY_CONFIGURED (409). A successful first configuration, even identical
to the system default, fixes policy. Concurrent first writes yield one success.
Replay and all exact-version reads remain unchanged. No migration or data rewrite.
This intentionally breaks repeated-update writes to meet the already normative
owner policy; do not retain an alternate UI/API bypass or silently unlock on rollback.

DEC-02: reuse Identity session invalidation and /identity/me for the settings page;
require current matching workspace and workspace.manage before reading/displaying
administrator controls. Semantic still independently authorizes every write.
Configured settings are readable and disabled, with explicit once-only notice.
No report setup/adoption/version controls. Editing an existing block needs no current
calendar GET: retain its source pin. A new block still resolves its internal default
through the existing authoring dependency; that is not a user adoption command.
No new shared context persistence schema or automatic rebasing is introduced.

DEC-03: mount a bounded calendar section in UI-ADMIN-004; other policy capabilities
remain unimplemented. Reuse existing shell/forms, locale, errors and session recovery.
Expose workspace-settings navigation outside the report analytical controls. Keep
financial/calendar basis and ordinary date/grain controls available in reports.

| Boundary | Impact | Proof |
|---|---|---|
| Calendar writes | breaking repeated-update behavior by required policy | API first write/race/409/replay/roles and retained versions |
| Existing profiles/results | none | DST and frozen v1 outputs remain current |
| Report UI | corrective removal | absence of setup/adoption/version selector and edit-only calendar GET |
| Settings UI | additive bounded route | administrator setup, disabled configured state, reload and nonadmin denial |

## 3. Ownership

MS-016-S01 owns repository once-only check/error, mounted settings and removal of
report controls, focused tests and docs. One executor, one independent read-only
reviewer. No Goal/publication/deployment/production migration/destructive cleanup.
Retained runtime/data and accepted journals remain untouched.

## 4. Acceptance

- AC-01: actual first configuration is atomic and once-only; replay, authorization,
  conflicts and exact immutable reads stay correct.
- AC-02: report setup/adoption is absent; edits preserve pins and remove unnecessary
  calendar fetch; one-time company settings work on the administrator route.
- AC-03: real API/browser save/reopen proves non-UTC25h results with a configured
  calendar as precondition; nonadmins cannot configure and stale responses clear.
- AC-04: focused/type/static/local gates, independent product-policy review, current
  docs and explicit supersession record are complete.

## 5. Execution and documentation

Use the existing exclusive updater, immutable receipt and baseline manifest.
Maintain parent/index/requirement links and correct current contract prose. Never
rewrite consumed MS-015 evidence; append a current supersession reference. Keep raw
traces and credentials temporary. Whole C04/C05–C11 remain required work.

## 6. Canonical bindings

plan_doc: `docs/architecture/planning/milestones/MS-016/plan.md`, v0.1.0.
prompt_pack_dir: `.codex/agents/generated/MS-016`.
stage_ledger: `.codex/delivery/ledgers/MS-016.md`.
Manual sequential continuation under existing owner authority; no Goal.

## 7. Decision history

Version0.1.0 technically accepted on2026-10-07 as necessary correction of the newly
detected METRIC-030 violation. This is not new owner approval of the rejected UI.
Continue remaining C04 relational/filter providers after correction.
