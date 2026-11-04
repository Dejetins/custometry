# MS-004 S05 correction 002 — report calendar boundary

The owner's 2026-09-22 correction removes financial-calendar setup/adoption from
reports and places stable once-only configuration in future administrator-only
company settings. This addendum is the current correction result; the original
[review001 report](../report.md) remains an immutable historical baseline, not
current owner acceptance. [Owner authority and exact supersession mapping](../owner-correction-2026-09-22.md)
cover D04/D08/AC-11 without rewriting the accepted plan/prompt contracts.

## Implemented scope

ConfiguredWorkspace no longer mounts CalendarSettings, fetches the current company
calendar, or exposes current/pinned version IDs and adoption. The native bridge
no longer sends Administration into report settings. Dates, six grains and the
calendar/fiscal analytical choice remain. Stored pins, result values, APIs and
security logic are unchanged. METRIC-030 machine/human and UI revision2026-09-22.1,
authoring/Web source contracts and architecture navigation record the correction.
The old unmounted component remains source history, not an active settings page.

[Validation](validation.md) records 5 real browser scenarios, 85 Web tests,
typecheck, generator, local and prompt-pack checks. The [criterion amendment](criterion-amendment.md)
reconciles changed proof with reused evidence; [source manifest](source-manifest.json)
records before/current hashes; [browser manifest](browser-manifest.json) binds the
new captures/observations. [Demonstration](demonstration.md) retains the live owner
report. [Access analysis](auth-analysis.md) identifies polling and database writes
without changing authentication or inventing measured performance improvements.

## Contract impact and remaining boundary

Browser behavior: compatible-change under explicit owner correction (removes
misplaced administrative controls). Target settings lifecycle: breaking-change
relative to repeatable setup, documented/deferred rather than falsely implemented.
API/DTO/persistence/cache identity/security implementation: none in this correction.
The existing calendar API still permits version updates; once-only backend setup
and its administrator page require the later settings unit. No automatic rebase,
release, production or remote synchronization claim. No foreign edits published.
Coordinator-owned S04 synchronization evidence remains untouched.

Technical correction is review ready; S05 remains subject to explicit acceptance
of the demonstrated finished result. No next stage is allowed. Original receipt001
and every bound original proof file remain unchanged; new receipt002 binds this
addendum as current validation while retaining the required baseline report path.
