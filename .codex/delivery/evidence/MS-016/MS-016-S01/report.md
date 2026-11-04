# MS-016-S01 corrective result

METRIC-030 and the2026-09-22 owner amendment supersede MS-015's report settings/
adoption UI. The earlier stage's functional pass did not prove compliance with this
affected requirement. This correction preserves its immutable receipts as history.
The gap arose from comparison-focused source selection that omitted METRIC-030.

Company calendar setup now lives only in the existing UI-ADMIN-004 workspace policy
route. Matching workspace/workspace.manage and session invalidation protect that
surface. After first save the form is read-only. Under the existing repository row
lock, original actor-bound replay precedes CAS and the once-only revision>0 guard.
New later writes return409 CALENDAR_ALREADY_CONFIGURED. Concurrent first writes
serialize; no reset/bypass is provided. Existing versions and DST math are unchanged.
Reports contain no setup/adoption/version control. Editing an existing block retains
its pin and does not fetch the current calendar. New-block default resolution remains
an internal authoring dependency, without a user adoption command.

Impact: intentional breaking-change for repeated setup writes, required by existing
owner policy. No payload migration, retained-data rewrite or production deployment.
Existing positive revisions remain configured, including historical multi-update
workspaces. Do not downgrade the writer to restore an unintended update bypass.

[Verification](verification.md), [review](review.md), [owned manifest](manifest.json).
[Canonical journal](../../../ledgers/MS-016.md) alone records acceptance. This resolves
only the calendar section of UI-ADMIN-004; other policies and C04/C05–C11 stay open.
Next: continue relational filter provider work under unchanged owner continuation.
