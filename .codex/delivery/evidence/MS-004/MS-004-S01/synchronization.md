# S01 synchronization and S02 entry — 2026-09-20

The coordinator completed the owner-authorized publication sequence after the
[S01 review](coordinator-review.md) and append-only publication corrections
([generated newline](publication-newline-correction.md),
[migration assertions](publication-ci-correction.md)). Accepted report, receipt
and their bound evidence remain unchanged.

- [PR #85](https://github.com/Dejetins/custometry/pull/85), head
  `aa466ceba7bbdd6d3ca10c2f44d462cddb8d1b08`, passed the required
  [Foundation gate](https://github.com/Dejetins/custometry/actions/runs/35532624333).
  Locked static/unit/contract gates passed; disposable Compose/browser proof was
  skipped by the selected fast synchronization profile. No release or deployment.
- Squash merge confirmed at `2026-09-20T19:35:48Z`, merge commit
  `b4aaa1680cfff5885fe61ff98fe7e69cf4934df0`.
- `git fetch origin main` and `git ls-remote --heads origin main` confirmed that
  exact remote main. The canonical checkout is detached at that commit.
- Remote `codex/ms004-s01` is absent; the local technical branch was deleted
  after merge confirmation. The original project checkout was not changed.

S02 entry is authorized by the existing whole-pack request and accepted S01
receipt. Its declared source inputs and predecessor report exist in the merged
tree. The accepted plan remains version 0.2.1 with hash
`9d0d590f7c3fccc581a6257365f0bcba961539f1fa9e0f93eec651e36255360e`.
Only S02 may now be advanced and dispatched as one separate same-directory
executor task; later stages remain disallowed. The coordinator will use the
exclusive updater with a freshly read journal hash, then run S02 preflight.

Carry the review's D04 envelope completion requirement into S02: exclusive
bucket/effective ends, fiscal indices and distinct expected, Calendar,
declared-complete and observed coverage must be produced and proved by S02.
Keep new public v2 routes unmounted until S03 current-access evidence. This
document proves synchronization and entry readiness, not calculation or browser
acceptance. It is coordinator-owned carryover for the next publication.
