# MS-010-S01 verification

All commands ran in `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`.
Tests use owned disposable containers/source/control databases and temporary files.
Retained runtime 41746 and saved user reports were not changed.

- `uv run --locked --no-sync python tests/integration/analytics/run_retail_filters.py --image cf78e76683b9`:
  final run 1 passed. The runner creates a uniquely named owner-labeled PostgreSQL
  container, two fresh DBs, seeds only that source, applies current migrations only
  there, runs the test and removes only its own container/volumes in finally.
- Actual fixture path: PostgreSQL source -> normal DataPipelineRunner -> published
  semantic version and committed canonical Parquet -> current Identity resource
  policy -> Artifact-owner admission -> DuckDB. Membership for all completed
  receipts and Store=1 matches independent read-only source SQL exactly. No provider
  or policy stubs replace these boundaries.
- Real negative cases: unsupported Store gives zero authorized rows; wrong workspace
  denied; cross-workspace, entity/hash mismatch and uncommitted manifest invisible;
  changing published department/object policy after input read discards the result;
  revoking the actual session after input admission blocks delivery and later use.
- First provider run failed with `FORBIDDEN` after the test gave an object required
  scope `store:1` while the department had no such scope. Causal source inspection
  established `required_row_scope_refs <= department.row_scope_refs`. This was a
  fixture defect, not a reason to weaken Identity. Test now publishes matching
  department policy through OrganizationService before binding. Subsequent real
  runs passed; retained policy was never touched.
- `uv run --locked --no-sync pytest -q tests/unit/semantic/test_retail_filters.py tests/integration/analytics/test_columnar_filters.py tests/unit/analytics/test_workspace_scopes.py tests/contract/presentation/test_composer_scopes.py`:
  77 passed. Unit negatives cover unavailable profile/namespace/capability, wrong
  grain, version sensitivity, empty current universe and permission deny before
  Semantic access. Real provider proof remains separate from these unit fixtures.
- Focused `ruff check` for new/touched modules and tests: passed.
- `uv run --locked --no-sync pyright packages/contracts/analytics/columnar_filters.py packages/semantic_model/application/retail_filters.py packages/semantic_model/infrastructure/postgres.py packages/artifacts/infrastructure/sales.py apps/api/src/custometry_api/analytics/filter_access.py`:
  0 errors/warnings.
- Contributor index generation passed. After toolchain activation,
  `uv run --locked --no-sync python -m tools.check --scope local`: passed.

No browser/API save/reopen claim: this milestone adds provider ports without a
mounted route or UI. It does not prove generic registry/facets, relational/history/
population evaluation, full C04 or production. Resource settings are test-harness
inputs, not installed production workspace defaults. Independent reviewer scope
and limitations are recorded in review.md.
