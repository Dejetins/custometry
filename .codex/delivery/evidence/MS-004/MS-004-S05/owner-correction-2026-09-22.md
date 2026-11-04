# MS-004 S05 — owner correction, 2026-09-22

Source: direct owner message in the original S05 executor task on 2026-09-22.
This rejects the affected review-001 UX and authorizes same-claim corrective work;
it is not result acceptance, a new stage, or publication authority.

> по поводу "календаря компании" имелось в виду что календарь настраивается один раз и потом не меняется, в каждой компании финансовый год может начинаться в разное время, но календарный год для всех одинаковый (естественно).
>
> не должно быть в отчетах настройки периодов финансового календаря, исправляй это. я не говорю что сейчас надо начать дорабатывать страницу с настройками, но в конце концов это требование должно быть реализовано именно в настройках, и эти настройки доступны только администратору.
>
> ещё меня смущает процесс проверки сессии и прав доступа, нахрена это делать каждый раз при открытии отчёта? есть же более оптимальные методы, которые не будут нагружать систему но при этом будут обеспечивать безопасность

## Accepted correction and mapping

Company financial calendar setup is once-only, stable afterwards, and belongs in
administrator-only company settings. Reports expose no fiscal-calendar setup,
current/pinned technical version controls or adoption. Building the settings page
is explicitly deferred. Report dates, grain and calendar/fiscal analytical basis
remain independent analytical choices; they do not configure company boundaries.

This later owner decision supersedes the report-facing controls/adoption in D04,
the report-mounted settings form in D08, and the corresponding AC-11 browser
clauses and S05 bounded-work item 3. Original plan 0.2.1, prompt and contract hashes
remain unchanged. Revised proof uses an already configured calendar as a fixture
precondition and checks absence of report setup/adoption and of its calendar GET.
No automatic rebasing, backend pin changes or saved-result reinterpretation.
The existing versioned calendar update API does not yet enforce once-only setup;
that lifecycle and its administrator settings page remain deferred requirements.

## Access diagnosis scope

Inspect and explain actual redundant requests and activity writes. Remove the
calendar GET needed only by the rejected report controls. Keep authentication,
per-resource authorization, revocation and late-response clearing. Do not claim
measured performance gains or implement an unreviewed security cache policy.

## Evidence continuity

All files bound by consumed review001 remain byte-for-byte at original paths.
New correction report, validation, current manifest and demonstration live under
correction-002/. A new receipt retains the contract-required baseline report path
and explicitly binds the correction evidence in validation and handoff_reason.
Review001 is historical and superseded for current UX by this owner rejection.
Finished S05 acceptance still requires a new explicit owner decision.
