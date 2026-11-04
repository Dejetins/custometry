# MS-011-S01 verification

Servicing checkout: `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`.
All DB/browser fixture runs use a new owner-labeled container with separate source
and control databases and temporary artifacts. Retained user data was untouched.

## Deterministic checks

- `uv run --locked python -m pytest -q tests/unit/analytics/test_bounded_filter_inputs.py tests/unit/analytics/test_filter_cancellation.py tests/unit/analytics/test_receipt_filter_identity.py tests/integration/analytics/test_retail_filter_mount.py tests/integration/analytics/test_columnar_filters.py tests/unit/semantic/test_retail_filters.py tests/unit/analytics/test_workspace_scopes.py tests/unit/analytics/test_workspace_calculation.py tests/unit/presentation/test_composer_service.py tests/contract/presentation/test_composer.py tests/contract/presentation/test_composer_scopes.py`: 158 passed.
- After `source scripts/activate-toolchain.sh`, `pnpm --filter @custometry/web test src/features/reports/receipt-filter-editor.test.tsx src/features/reports/composer-state.test.ts src/features/reports/composer-structure.test.ts`: 18 passed.
- Focused Ruff and Pyright on changed contracts, analytics, Artifact and API modules:
  passed; Pyright 0 errors/warnings. `pnpm --filter @custometry/web typecheck`: passed.
- `generate_docs_index`, `check --scope local` and `git diff --check`: passed before
  final evidence write; final source gate is repeated after evidence/index sync.

Real DuckDB tests cover authorization before facet grouping/pagination, empty/denied
values and injection-shaped search, exact counts and unknown, field/version/policy
rejection, canonical Boolean identity and Arrow membership projection. HTTP disconnect
and handler cancellation signal the actual evaluator and wait for worker exit.
Budgets reject before eager legacy loading or Python materialization, including full
IdentityWorkspaceAccess preflight and compressed string expansion. These synthetic
engine tests do not replace actual published-provider browser proof below.

Actual pre-MS-011 Python query reader and normalizer bytes were reconstructed and
SHA-checked against the entry baseline before preservation. Tests run both readers:
old input roundtrips identically and normalizes to the same hash; old reader rejects
new filter fields; compatible reader retains new serialized bytes; absent provider
cannot silently ignore the filter. New policy/registry identity changes the result.
This proves reader rollback preservation/rejection, not a production deployment drill.

## Real browser and HTTP

Target `http://127.0.0.1:41747` with real API `58147`, disposable published retail
input, Identity, PostgreSQL, Artifact store and DuckDB. No fabricated provider
response. Browser viewport 1440x1000, plus 768 and 390 width in selected scenarios.
New filter scenario: searchable allowed catalog, visible mandatory constraints,
zero-match exact preview without member IDs, draft Reset/Undo, keyboard Apply,
pending Apply prevents early Add, actual changed totals/request hash, save/reopen,
retained expression and mobile access. Parent definition changes only after builder
commit. Unit race test rejects a late aborted preview without showing stale counts.

Early test repairs: ambiguous hidden/visible Value locator and wrong Edit button
name were test defects. After those, the initial combined four scenarios passed.
After adding the delayed-Apply check, Chromium `Network.getResponseBody` returned
“No data found” on actual POST 200; the OPTIONS hypothesis was refuted by method
instrumentation. Upstream response capture now forwards exact real API responses
unchanged and asserts their bytes, avoiding that CDP retrieval boundary. No product
behavior was changed for this test-tool failure; underlying CDP cause is undetermined.
A focused final filter run passed using that actual-upstream capture.

Expanded run initially had two readiness timeouts. A diagnostic rerun reproduced
one: the captured iframe showed the builder's invalid-fields state, no validate
request was sent, and the selected metric context response arrived after Add.
The builder now gates Continue/Add and submit on required dataset/metric/calendar
readiness. The new browser regression withholds a real context response and checks
Continue remains disabled until release. This establishes the reproduced race;
the earlier untraced timeout is not independently attributed.

Final command after repair: `pnpm --filter @custometry/web exec playwright test
--config ../../tests/e2e/ms-006-composer/playwright.config.ts filters.spec.ts
composer.spec.ts scopes.spec.ts --trace retain-on-failure`: **6 passed (2.1m)**.
Covers independent blocks/shared results, standalone table/duplication/recovery,
reconnect/save ordering, filters, inherited/pair/saved scopes, RU linked empty
scope/keyboard/Undo. Final frontend typecheck passed. Traces stay ephemeral because
they contain fixture authentication traffic; no raw trace copied into evidence.

## Limits

This is mounted flat Receipt filtering. It does not prove general relational,
sequence/population semantics, Focus filtering, production delivery or full C04.
The retained `http://localhost:41746` preview still serves its prior built bundle;
this stage has not claimed to refresh that retained runtime. No publication, deploy,
production migration, destructive reset or external message occurred.
