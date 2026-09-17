# MS-003-S04 — partial compiler delivery and report-entry context gap

Milestone: MS-003. Stage: MS-003-S04. Iteration: 1.
Plan: [MS-003 0.2.0](../../../../../docs/architecture/planning/milestones/MS-003/plan.md).
Prompt: [S04](../../../../agents/generated/MS-003/MS-003-S04.md).
Journal: [canonical execution state](../../../ledgers/MS-003.md).
Plan SHA-256: `4a6b1bf2a64a04b74e073bb22e46895795e187be57fe93b6711408069d6e7280` (unchanged).
Source baseline: `cb4f696dc1dca3bc051debd347810f7d74caa319` plus existing accepted S03 changes.

## Result and outstanding decision

S04 is not complete and has no acceptance receipt. Entry preflight and exclusive
claim passed under the actual executor session. The pilot was served locally at
`http://127.0.0.1:8834/ru/source.html`, rendered and visually inspected at 1920x1080
before implementation. Its HTML bytes remain unchanged. This is source inspection,
not an implementation comparison or UI acceptance.

The independent [canonical line compiler](../../../../../packages/chart_compiler_ts/README.md)
is implemented and tested. It accepts the exact S03 specification subset,
validates nested fields and artifact/metric/workspace/owner/policy bindings,
rejects raw options/callbacks/HTML/URLs, preserves null gaps and exact decimal
strings for tables, and emits derived ECharts options. Previous-year values align
by calendar date rather than array position across leap days. Locale affects
labels only. The synthetic fixture comes from the actual Python S03 specification
producer and registered metric definitions; it is not a runtime/provider fixture.

First report creation and authorized store selection need an API projection that
is absent from the inspected providers. The [bounded amendment](entry-context-amendment.md)
records evidence, the smallest proposed endpoint/owner-port repair, additional
write zones, compatibility and required proof. This crosses the current S04 write
zones, so it has not been implemented. The user must decide that extension before
the dependent integration and acceptance can proceed.

## Scope, files and compatibility

Created: compiler `src/line.ts`, `tests/line.test.ts`, provider-produced synthetic
`tests/canonical-line.fixture.json`, package README, and this evidence directory.
Modified: compiler `src/index.ts`, lifecycle test, TypeScript JSON-import setting,
and one separable architecture index version/navigation hunk. The ledger uses
only the exclusive updater. No files are deleted and no unexpected source zones
are changed. [Validation evidence](validation-evidence.json) lists exact paths and hashes.

Existing S03 changes are foreign to this stage: report API and main/analytics
composition, Presentation and Artifact source, migration 0011, generated contract
files and index export, Presentation tests, S03 evidence and canonical contract
docs. They are preserved. Architecture index S03 changes are preserved beneath the
separable S04 hunk. Completed MS-001/MS-002 artifacts and pilot bytes are untouched.

The new compiler export is additive (`compatible-change`); the foundation-only
`chartCompilerLifecycle` changes from `planned` to the narrower `line-v1`. Static
consumer search found only its package test, updated here; the old envelope type
is retained. No runtime application consumes the new compiler yet. Backend APIs,
persistence, permissions and dependencies are unchanged by this partial delivery.

## Validation and proof limits

Exact commands/results are recorded in [validation evidence](validation-evidence.json).
Compiler typecheck and meaningful contract tests cover reference mismatch,
unknown fields, unsafe content, unsupported units/type/version, invalid/duplicate
dates, unavailable values, decimal precision, locale, no comparison, empty data and
leap-year alignment. The required grouped `local` profile is run at source handoff.

AC-05/06 remain unproven. Web/login/library/editor, TanStack cache invalidation,
the ECharts 6.1.0 SVG adapter, system-default/hash verification at the Web boundary,
complete render identity, RU/EN viewport/keyboard/zoom flows, production-API browser
fixture, critical failure flows, screenshots of the implementation and normalized
pilot comparison remain unfinished. ECharts has not been installed. No mocked
response or unit test is claimed as database, browser, packaged or release proof.

## Next input and state

Request the owner decision in the amendment and record its actual answer as
resolution evidence. Resume only with the same valid session claim and an
authorized scope reconciliation; do not impersonate this executor in another task.
Then complete S04 and its actual proof before producing a ready receipt. S05 stays
disallowed; no successor readiness or acceptance is claimed. The accepted plan
and all predecessor receipts retain their exact bytes.
