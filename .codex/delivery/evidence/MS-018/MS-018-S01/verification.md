# MS-018 verification

Servicing checkout `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry` only.
Retained runtime41746 unchanged. Disposable task-owned PostgreSQL containers were
removed by their fixture. No publication/deployment/production migration.

- Focused command with `tests/unit/semantic/test_retail_relational.py`,
  `test_retail_filters.py`, `tests/integration/analytics/test_relational_filters.py`,
  `test_relational_decimal_storage.py`, `test_columnar_filters.py`,
  `test_retail_filter_mount.py`:107 passed in0.87s. Real synthetic Parquet/DuckDB
  plus isolated provider-port negative tests; includes only-same-scale lossless
  widening and unchanged v1 strict precision, malformed relationships/admission,
  no inferred complete history and existing truth/resource/security cases.
- `run_retail_filters.py --image sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4 --test-file test_retail_relational_provider.py`:
  1 genuine multi-boundary scenario passed in2.68s. Fresh source/control PostgreSQL,
  actual source intake/publication/Artifact manifests, current Identity policies and
  real Parquet/DuckDB. Membership independently matches source SQL joining eligible
  products; negative existence has no confirmed absence and preserves unknown count.
  Store1 narrowing, absent-store empty universe, foreign workspace denial, policy
  mutation after actual input read and current-session revocation are verified.
  Real Reports ASGI HTTP checks cover bearer and cookie+CSRF, missing auth/CSRF,
  localized catalog search, count-only response keys/no-store, v1 rejection ofv2,
  unknown workspace/root/SQL input fields and registry mismatch. Catalog session
  revoked after projection is denied before delivery despite GET request auth memo.
- Same runner default v1 scenario after shared reader change:1 passed in2.25s.
- Focused Ruff/Pyright:pass, zero type errors. Generated OpenAPI/TypeScript client,
  frontend `tsc --noEmit`, docs index, `check --scope local`, `git diff --check`:pass.
  Observed profile is local, not CI/release or browser proof.

Earlier attempts: combining two bootstrap scenarios in one database failed the
expected once-only bootstrap guard; runner now selects one scenario per fresh DB.
Actual v2 input failed FILTER_INPUT_SCHEMA because Arrow inferred narrower decimal
precision. Fixed only through explicit same-scale lossless widening with four real
Parquet regressions. One negative unit test initially used a Pydantic copy method on
a dataclass test binding; corrected fixture construction. None waived product guards.

The browser surface and persisted report format are unchanged. This proves genuine
provider/HTTP behavior, not report editing/save/reload or full FILTER/C04 capability.
