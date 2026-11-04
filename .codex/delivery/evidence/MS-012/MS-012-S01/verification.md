# MS-012-S01 verification

All work/tests ran in `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`.
The real browser fixture creates separate task-owned source/control PostgreSQL
and temporary published artifacts. No retained user report/data was written.

## Focused checks

- `uv run --locked python -m pytest -q tests/contract/presentation/test_receipt_scopes.py tests/contract/presentation/test_composer_scopes.py tests/contract/presentation/test_composer.py tests/unit/presentation/test_composer_service.py tests/integration/analytics/test_columnar_filters.py`: **120 passed**.
- `pnpm --filter @custometry/web test src/features/reports/receipt-scope-editor.test.tsx src/features/reports/receipt-filter-editor.test.tsx src/features/reports/composer-state.test.ts src/features/reports/composer-structure.test.ts`: **22 passed**.
- `pnpm --filter @custometry/web typecheck`: pass.
- Focused Ruff and Pyright on changed scope/analytics/composer boundaries: pass,
  Pyright 0 errors/warnings. `check --scope local`, generated docs index and
  `git diff --check`: pass before final evidence synchronization.

The six new contract tests cover all ancestors plus local AND input; explicit
same-field replacement and wrong field/dataset/registry rejection; saved lock
removal/retarget/move denial; direct links/cycles and duplicate constraints;
mixed duplicate order; actual preserved v1 reader/resolver bytes and identity,
old-reader v2 rejection and unchanged effective identity for unaffected blocks.
Pure tests do not independently prove access/provider behavior.

The added UI switching regression first failed (expected B, actual A), then passed
after the keyed-form repair. All 22 selected frontend tests passed after repair.
Initial backend failures were fixture setup errors (grid copy lacked placement,
then assumed two blocks when the reused fixture already contained two); corrected
fixture setup did not weaken the implementation assertions.

## Real browser

Actual target `http://127.0.0.1:41747`, API 58147, Chromium desktop1440x1000 plus
768px and390px in suite. Identity, published Semantic/Artifact inputs, PostgreSQL,
DuckDB and real Analytics values/persistence run in the fixture. Apply/save bodies
are captured upstream and forwarded unchanged; no mocked provider result.
New scenario verifies document condition, allowed block replacement, actual positive
versus empty totals, retained neighboring result reference, effective overridden/
locked origins, v2 Save/reopen and backend rejection of removing a persisted lock.

Early browser fixes: give select controls stable accessible names; correct test's
saved-result assertion to the actual result-reference schema (result_id, not a nested
result). Focused real scenario passed before the reviewer switching repair. Final command after the keyed-form repair: `pnpm --filter @custometry/web exec
playwright test --config ../../tests/e2e/ms-006-composer/playwright.config.ts
receipt-scopes.spec.ts filters.spec.ts composer.spec.ts scopes.spec.ts
--trace retain-on-failure`: **7 passed (2.3m)**. Includes old multi-block/reconnect,
flat filters, Receipt hierarchy, Store/pair scopes and RU linked-empty/Undo scenarios.
Final 768px Receipt scope screenshot inspected: complete locked expression, settings
and denial explanation visible, with native labels and disabled controls. Screenshot
is appearance evidence only; HTTP/result assertions establish functional behavior.

## Proof limit

Only published flat Receipt hierarchy is claimed. No relational/sequence/population,
full Focus, scale/SLO, static/export parity or full C04/C05–C11 completion. Retained
41746 preview has not yet been rebuilt/restarted by this stage. Raw browser traces
remain temporary because they contain fixture authentication traffic; only sanitized
screenshots are eligible for durable evidence. No publication or deployment occurred.
