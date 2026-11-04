# MS-013 verification

All work used `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`.
No retained user data/runtime was changed. Disposable browser fixtures use separate
PostgreSQL control/source, published Semantic/Artifact data and real Analytics.

## Focused proof

- `uv run --locked pytest tests/unit/analytics/test_temporal_resolution.py tests/unit/analytics/test_temporal_projection.py tests/unit/analytics/test_workspace_calculation.py tests/unit/analytics/test_receipt_filter_identity.py tests/contract/presentation/test_temporal_scopes.py tests/contract/presentation/test_composer_scopes.py tests/contract/presentation/test_receipt_scopes.py tests/unit/presentation/test_composer_service.py -q`: **82 passed**.
- `pnpm --filter @custometry/web exec vitest run src/features/reports/composer-temporal-editor.test.tsx src/features/reports/temporal-comparison.test.tsx src/features/reports/composer-state.test.ts src/features/reports/workspace-presentation.test.tsx`: **35 passed**.
- Frontend `typecheck`: pass. Focused Python Ruff and Pyright: pass, 0 type errors/warnings.
- `check --scope local`: pass; docs index generated and `git diff --check` pass.

Backend proof includes leap/month/year/fiscal/ISO-week previous buckets, custom overlap,
range/unaligned rejection, incomplete exclude/partial/shared-prefix policies, exact
zero-denominator deltas, typed artifact/hash, current Store ceiling and mandatory
metric rules on both periods, unchanged actual pre-stage reader/calculation output,
old-reader rejection, reciprocal inherited legacy/new override and lock denial.

UI proof includes server paired dates/values/null handling and mode labels, explicit
inherit/none and removal of only comparison fields. Three mounted Builder regressions
failed before the reviewed repair and passed after it: modern base/local legacy none,
legacy base/ancestor none, and the same with a locked ancestor. Tests prove existing
query/context precedence survives an unrelated title edit.

## Real browser and persistence

Target `http://127.0.0.1:41747`, API58147, Chromium. Requests are real; upstream apply/
save bodies are observed then forwarded unchanged. No synthetic API response is used.
A standalone October reference equals the comparison-side total of both November
previous-period and custom-period runs. Both date spans, 30/31 date counts, raw deltas,
duration limitation and no-normalization text are rendered. Root previous-period
resolves September for October; explicit local none/custom override the root. The
custom artifact content hash survives scope change and actual Save/reopen, with the
same rendered baseline amount. Screenshot `temporal-comparison.png` was inspected.

Broad regression command: Playwright config `tests/e2e/ms-006-composer/playwright.config.ts`
with `temporal.spec.ts receipt-scopes.spec.ts filters.spec.ts composer.spec.ts scopes.spec.ts`
and `--trace retain-on-failure`: **8 passed (2.8m)**. This includes prior Store/Receipt
scopes, filters, pair, RU empty/Undo, independent blocks, duplication and reconnect.
After the final compatibility repair, reran affected `temporal.spec.ts composer.spec.ts`:
**4 passed (1.4m)**. These are the final source's relevant browser results; unchanged
Store/Receipt regressions reuse the immediately preceding evidence.

Early harness failures: missing wait for completed scope validation caused a correctly
aborted stale Apply; expected undefined instead of explicit v2-none null; attempted
reopen of a result invalidated by a changed scope without first applying it. These
assertions were corrected. A new permission test initially reused receipt primary
keys and correctly failed grain validation; unique fixture keys fixed it. No production
logic was weakened. Early TS fixtures lacked required fields; corrected fixtures now
pass typecheck. Raw browser traces remain temporary and are not durable evidence.

## Boundary

This proves the declared local UTC/month-based provider path, not other business
calendar profiles/DST, population comparison, all report tabs/exports/delivery channels,
scale/SLO or production delivery. The retained 41746 preview was not rebuilt/restarted
by this stage. Full C04 and C05–C11 remain work under the existing continuation authority.
