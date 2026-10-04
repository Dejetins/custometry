# MS-004-S03 publication typing correction

Date: 2026-09-21. Authority: coordinator's narrowly scoped same-task publication
correction before PR. S03 remains accepted. No claim reset, journal mutation,
new stage/task, production change or Git mutation is performed by this correction.
This append-only record supplements [accepted evidence](report.md),
[validation](validation.md), [source manifest](owned-files.json) and
[consumed receipt](receipts/001-ready.md); those artifacts are unchanged.

## Cause and scope

The required Foundation typing command in `.github/workflows/ci.yml` covers
`apps/api/src tests/integration`. S03's initial focused Pyright covered production
sources only and therefore did not prove this required integration-test boundary.
The coordinator found 158 diagnostics; the same focused command was reproduced
before editing, exit 1 with **158 errors**, all in `test_workspace_s03.py`.
Classification: **introduced by the S03 test implementation**, not an environmental
failure, unrelated baseline failure or flaky runtime test.

The causes were missing helper argument types, `object` DTO version values passed
to `int`, heterogeneous actor/request dictionaries losing per-key types, nullable
SQL `fetchone` results indexed by existing assertions, untyped fault-injection
forwarding helpers, and the concurrent-save lambda's unknown argument. Inferring
real repository types also exposed explicit test access to protected fault seams.

Only `tests/integration/presentation/test_workspace_s03.py` changed:

- Added a precise `ActorArguments` TypedDict and typed connection, request,
  resource-binding and fault-injection helper boundaries.
- Kept dynamic JSON payloads explicit as `dict[str, Any]` and route matrices typed
  as method/path/optional-payload tuples. JSON return values remain dynamic at the
  TestClient boundary; existing status and value assertions are retained.
- Added no-op casts for DTO version values and rows already required by existing
  indexing. No runtime default, missing-row fallback or assertion removal was added.
- Replaced the concurrent lambda with a typed helper containing the identical
  single `client.post` call. Fault injection uses explicit `getattr`/`setattr` on
  the same `_checkpoint` instance field, retaining the same call order and values.
- Added no ignore comment, file-wide/global diagnostic override, test skip,
  production workaround or weakened validation.

Contract impact: **none** for API, persisted data, permissions, runtime behavior,
product requirements and accepted acceptance criteria. This repairs test-source
static verification only. Existing requirement/criterion mappings remain in the
accepted report and are not amended.

## Exact source identity

| Source | Before SHA-256 | After SHA-256 |
|---|---|---|
| `tests/integration/presentation/test_workspace_s03.py` | `67739f003378c2d0fef54525563d51a9b62abd6edd176708371888946489fd21` | `f9ad87b312ca82b4c5a5af9d619a076247fbac36a7eb59c87d90b57896682d26` |

The before hash matches the consumed source manifest. All other 43 source hashes
in that manifest were verified unchanged. The old manifest is intentionally not
rewritten; this addendum records the final publication hash for the one correction.

## Checks and proof boundary

Working directory: `/Users/daniildegtyarev/.codex/worktrees/575c/Custometry`.
Existing toolchain activated with `source scripts/activate-toolchain.sh`.

```sh
uv run --locked pyright tests/integration/presentation/run_s03.py tests/integration/presentation/test_workspace_s03.py tests/integration/presentation/test_drafts.py tests/integration/presentation/conftest.py tests/integration/analytics/test_workspace_s02.py
uv run --locked pyright apps/api/src tests/integration
uv run --locked ruff check tests/integration/presentation/run_s03.py tests/integration/presentation/test_workspace_s03.py tests/integration/presentation/test_drafts.py tests/integration/presentation/conftest.py tests/integration/analytics/test_workspace_s02.py
uv run --locked pytest --collect-only -q tests/integration/presentation/test_workspace_s03.py
uv run --locked python -m tools.check --scope local
uv run --locked python -m tools.custometry_quality.validate_prompt_packs
git diff --check
```

- Focused Pyright: final exit 0, **0 errors, 0 warnings** (before: 158 errors).
- Full CI-equivalent Pyright scope: exit 0, **0 errors, 0 warnings**.
- Ruff: exit 0, all checks passed. Formatting was restricted to the one test file.
- Pytest collection: exit 0, **1 test collected in 0.32s**. This proves imports and
  discovery only, not another runtime scenario execution.
- Local profile: passed. Prompt-pack validator: passed for four journals,
  structure/file binding only. Diff whitespace check: passed.
- The optional Pyright version-update notice is informational; no tool upgrade
  or dependency installation was performed.

An AST comparison of the preserved pre-edit source and final source removed only
annotations/type-only imports/TypedDict, unwrapped `typing.cast`, normalized the
explicit `_checkpoint` getattr/setattr to the previous attribute syntax, and
inlined the named single-expression concurrent helper back to the previous lambda.
The resulting executable ASTs are equal. All **49 assertions** are identical under
the same normalization; no query, literal, branch, call argument, expected status,
fault injection or ordering changed.

Normalized executable AST SHA-256: `fa9df33f919e09d077c88b6a9c4c390d056a8f8bc737525961164bf5806b69b5`.

The existing real-boundary run is reused as explicitly authorized for these
semantics-preserving typing changes: main scenario **1 passed in 260.88s**, legacy
suite **2 passed in 5.01s**, successful disposable-resource cleanup. It was not
rerun and is not presented as a new run. This correction's new proof is static
CI typing, lint, collection and AST equivalence. Browser, remote CI, publication
and production proof are not claimed.

## Preserved consumed hashes and handoff

The following exact hashes were checked equal before/after correction:

| Preserved path | SHA-256 |
|---|---|
| `.codex/delivery/evidence/MS-004/MS-004-S03/report.md` | `7bf20392233e1712e632d6bb984edbcacdd45a4210c8333a9148d61a5fc452d2` |
| `.codex/delivery/evidence/MS-004/MS-004-S03/validation.md` | `2cfb5e86ba4b883e42e20fdc60ed318703d395a8eab3986d44237ad8b1ba4ced` |
| `.codex/delivery/evidence/MS-004/MS-004-S03/corpus.json` | `20948e43207d564df3c09db73b71b2f2f47a33776967c83bee895d58c0b0bad7` |
| `.codex/delivery/evidence/MS-004/MS-004-S03/owned-files.json` | `da99301bc6a5a1e41c67831824bf483e1d05f7f4791ef2e096585445a8130817` |
| `.codex/delivery/evidence/MS-004/MS-004-S03/receipts/001-ready.md` | `cc4d97dd29800999b053c4b7dd437574a335978f05600e0cd6e5f3599521fa6c` |
| `.codex/delivery/ledgers/MS-004.md` | `f92f2a4380446b034eb883c7aee33e92b4323e0c229db33e5966afc9a511c6ff` |

No consumed evidence, receipt or journal bytes changed. No new receipt is needed
or fabricated for this bounded publication correction. The coordinator may now
review this final test hash and proceed with the authorized technical-branch PR,
Foundation gate, squash merge, remote-main verification and branch deletion.
S04 remains disallowed until the coordinator's supported subsequent advance.
