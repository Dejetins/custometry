# Source recovery and GitHub synchronization — 2026-11-04

The owner authorized preservation of all current uncommitted development through
a technical branch, green Foundation CI, merge, and branch deletion.
Publication is tracked by [PR #95](https://github.com/Dejetins/custometry/pull/95).
This is source synchronization, not milestone acceptance or runtime release.

## Recovered source

The deleted working checkout was recovered from local Git snapshot `1c2074f`
(parent `86055ce732640ebe68fd5415a55f7bbde3499181`). Its source delta was applied
onto `b84af6bdea917d8c42a265c5bf3207fc6dca3d2d`, preserving the newer repository
UI and agent guidance. Snapshot commit ancestry was not published.
This preserves composer work through the goal-line repair, analytical filtering,
tests, contracts and historical engineering evidence. Relevant composer
requirements include ANALYTICAL-DOC-004 and DASHBOARD-006; their earlier runtime
observations remain in [the original report](report.md).

W39 evidence was sanitized before publication: raw process payloads became counts
and hashes, and five raw resource/patch files were excluded. Originals were
retained in an ignored local archive with verified hashes. Local databases,
runtime directories, credentials and restored demo state are not Git artifacts.
The original deleted database and exact dashboard layout were not recovered.

## Synchronization repairs

- Regenerated committed report, workspace, sales and identity contract artifacts
  from their current providers; updated the explicit report-route contract.
- Added package markers to distinguish same-named contract/integration modules.
- Typed integration fixtures and dynamic provider boundaries without changing
  global strictness or removing behavioral assertions.
- Updated two migration lifecycle tests to expect head `0014_composer_reports`;
  downgrade, repeat and re-upgrade checks remain.
- Reclaimed unused Android, .NET and GHC SDK directories on the disposable
  GitHub-hosted quality runner. The first CI attempt failed with 14.97 GiB free
  against the existing 25 GiB requirement; that requirement remains unchanged.

The repairs have no intended product API or persistence behavior change;
generated contracts now describe the recovered provider. The recovered feature
set itself includes API and migration changes documented by its original units.

## Review and proof boundary

A bounded independent static review covered repository policy, request projection,
migrations 0013/0014, evidence sanitation, and the synchronization repairs.
No material blocker was confirmed within that scope. This was not an exhaustive
security audit or a new runtime acceptance run.

Local `tools.check --scope local` and `--scope ci`, Ruff, strict API/integration
Pyright, frontend lint/typecheck and frontend tests passed (web: 265 tests).
The full Python run reached 898 passed / 59 skipped with five Python 3.12
`Generator` annotation failures introduced during typing repair. After correcting
all three generic parameters, the affected analytics suite passed all 182 tests,
including those five cases. Infrastructure-dependent skips remain explicit.
Final GitHub status is recorded in the PR. Full build, Compose/browser and release qualification are
outside this synchronization profile. Historically captured screenshots do not
prove the newly merged runtime.
