# MS-024-S02 verification

All commands ran in c67c. Scope is local/disposable, not ci/release or deployment.
Counts below are final non-additive runs; overlapping checks are not summed.

| Check | Final observation | Boundary |
|---|---|---|
| Focused backend contract/real Parquet suites | 221 passed, 1.69s | Includes new replacement repair; excludes separate genuine provider/browser fixture |
| Complete @custometry/web Vitest suite | 189 passed, 42 files, 2.15s | DOM tests; provider calls mocked where declared |
| Web typecheck | pass | Generated DTO/editor compatibility |
| Focused Ruff / strict Pyright | pass; 0 errors/warnings | Changed scope/dispatch/contracts and new backend tests; no dependency update from advisory |
| Genuine saved cohort API | 1 passed, 5.11s | Fresh owned PostgreSQL source/control, publication, Artifact, Identity, real Apply/Save and read-only token |
| Real browser combined | 4 passed, 1.2m | cohort-filters, filters, relational-filters, aggregate-filters; no retries; one worker |
| tools.check --scope local | PASS observed=true | Local grouped proof only |
| git diff --check | pass before sealing | Working-tree whitespace only |

The genuine saved test verifies analysis.read without analysis.run can GET saved
metadata and block result, while Apply/preview/facets return403; revoked token
returns401. No tokens/provider payloads are copied to durable evidence.

Browser checks use disposable41747/API58147 and owned temporary PostgreSQL. They
prove v1→v4 promotion, relative window microseconds, two positive events, gap and
same-store binding, item condition in v4, Reset/Undo, Tab focus,390px, Save/reopen,
and one positive plus one negative event yielding0 confirmed/5000 unknown receipts
with unavailable metric values. RU/EN saved coverage is inspected. Four final PNGs
are retained in screenshots/. Prior browser cohort-only pass (20.7s) is superseded
by this combined run. Browser completed before the final backend replacement-only
repair; that repair is covered by the final221 backend tests and independent probes.
No UI source changed after the final browser run.

Narrow controls wrap without horizontal overflow; screenshots show technical UTC
cutoffs/seconds and long expressions. RU state column uses existing ellipsis. This
is functional/layout evidence, not owner usability or visual acceptance, full
screen-reader coverage, app-wide accessibility or measured latency. Save response
60s functional deadlines do not establish a performance SLO.

## Failed attempts and repairs

- Initial cohort browser1/2 failed because History window lacked a usable explicit
  accessible label. Added explicit aria-labels to window/time/event/property/seconds
  controls. A keyboard assertion expected Field but actual next control is the AND
  group selector; corrected the assertion to the observed logical order. Final4 pass.
- Independent P2: report provider required analysis.run for saved reading. Changed
  report composition to require_run=False, retaining run guards at execution. The
  genuine read-only-token test above verifies both allowed and denied actions.
- Independent P2: valid v2/v3 with optional legacy UUID absent failed v4 promotion.
  Exact registry-map bridges now admit absence and preserve origins; conflicting
  supplied pins still fail. Two backend red cases became green; two UI cases cover
  both promotion variants and explicit conflicts.
- Independent follow-up P2: broad compatibility allowed replacement to erase an
  ancestor legacy registry pin. Red regression: DID NOT RAISE,1 failed/6 passed.
  Separate compatible_replacement preserves every present ancestor legacy pin;
  intersection still gathers optional pins. Final221 pass and independent closure.
- Intermediate full UI suite:2 failed/187 passed. Reset remounts inputs to clear
  invalid duration text; old tests read detached DOM nodes. Tests now query current
  visible controls after Reset/Undo. Final189 pass. No stale-value behavior is hidden.
- Initial source lookup used a nonexistent features/composer path and a docs glob;
  corrected through rg --files. These lookup failures are not evidence of absence.

## Reproduction

Activate scripts/activate-toolchain.sh before pnpm/grouped local tools.

```sh
uv run --locked pytest tests/contract/presentation/test_cohort_receipt_scopes.py tests/contract/presentation/test_receipt_scopes.py tests/contract/presentation/test_relational_receipt_scopes.py tests/contract/presentation/test_aggregate_receipt_scopes.py tests/contract/presentation/test_composer_scopes.py tests/integration/analytics/test_receipt_cohorts.py tests/integration/analytics/test_customer_event_boundaries.py tests/integration/analytics/test_sequence_filters.py tests/integration/analytics/test_aggregate_filters.py tests/integration/analytics/test_relational_filters.py tests/integration/analytics/test_columnar_filters.py -q
pnpm --filter @custometry/web test
pnpm --filter @custometry/web typecheck
uv run --locked python tests/integration/analytics/run_retail_filters.py --image sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4 --test-file test_retail_cohort_saved.py
pnpm exec playwright test --config tests/e2e/ms-006-composer/playwright.config.ts cohort-filters.spec.ts filters.spec.ts relational-filters.spec.ts aggregate-filters.spec.ts
uv run --locked python -m tools.check --scope local
git diff --check
```

No retained41746 migration/rebuild/restart or user data removal occurred. Raw logs
stay temporary; this redacted evidence and tests retain failures/results without
credentials or raw provider rows. Historical receipts remain immutable.
