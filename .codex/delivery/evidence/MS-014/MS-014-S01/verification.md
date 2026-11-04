# MS-014 verification

All work ran in `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`.
Disposable source/control PostgreSQL and published retail artifacts were used;
retained 41746 runtime and user data were not touched.

## Focused checks

- Backend temporal/year/workspace/filter identity, temporal/Store/Receipt scopes and
  composer service suite: **93 passed**. Command: `uv run --locked pytest
  tests/unit/analytics/test_year_comparison.py tests/unit/analytics/test_temporal_resolution.py
  tests/unit/analytics/test_temporal_projection.py tests/unit/analytics/test_workspace_calculation.py
  tests/unit/analytics/test_receipt_filter_identity.py tests/contract/presentation/test_temporal_scopes.py
  tests/contract/presentation/test_composer_scopes.py tests/contract/presentation/test_receipt_scopes.py
  tests/unit/presentation/test_composer_service.py -q`.
- Frontend temporal details/editor, mounted Builder, composer state and presentation:
  **38 passed** with `pnpm --filter @custometry/web exec vitest run` and
  `composer-temporal-editor.test.tsx temporal-comparison.test.tsx composer-state.test.ts
  workspace-presentation.test.tsx` under `src/features/reports/`.
- Frontend typecheck, focused Ruff and Pyright: pass, 0 Python type errors/warnings.
- Generated docs index, `check --scope local` and `git diff --check`: pass.

Golden preparation captures actual pre-MS014 synthetic inputs and outputs for legacy,
none, previous_period and custom_period. Current calculation equals every frozen
result including request/artifact hashes; current query serialization matches old
inputs. The actual preserved settings reader rejects new modes. Tests cover leap
exclude/merge/calendar-map denial, calendar/fiscal full range and basis rejection,
ISO year boundary/week53 exclusion/partial/missing map, applicable policy validation,
empty mapping, partial coverage and actual complete-prefix reduction.

The weekly leap-merge regression first failed (two rows), then passed after grouping
repair: one baseline contribution and matching row/total delta. Mounted Builder tests
plus resolver tests cover explicit fiscal override above parent calendar, lock denial,
and unchanged old query/context during unrelated edits.

## Real browser

Target `http://127.0.0.1:41747`, API58147, Chromium1440x1000, actual Identity,
Semantic/Artifact/Analytics and PostgreSQL. Apply/save response bodies are captured
upstream and forwarded unchanged; provider results are never mocked.

Six blocks verify standalone leap-February reference, full calendar and fiscal modes,
explicit same-date mapping, ISO week mapping and comparable elapsed mode. Calendar/
fiscal comparison totals equal the independent real February2024 reference including
Feb29. Explicit mapped range excludes the unmapped leap day within its envelope;
ISO2025 week2 maps to January8–14,2024. Mapped details/limitations are visible. Saved
result refs and rendered amounts survive actual Save, route load and full reload.
`year-calendar-comparison.png` was inspected; it shows 28 vs29 dates, actual totals,
raw delta/percent and duration limitation without normalization.

Final existing regression run (`temporal.spec.ts composer.spec.ts` in the shared
composer Playwright config) passed **4 scenarios**. In the same run, the six-block
Save exceeded the harness's 10s route.fetch timeout. The dedicated year scenario
previously passed once (2.0m) with longer read expectations, and the final focused
run passed **1 scenario (2.7m)** with explicit 60s save/read observation timeouts.
No application timeout or implementation was changed to obtain this evidence. Final
five affected scenarios therefore passed across these runs, with the failed broader
run reported separately rather than relabeled green.

Early test corrections: the unmapped baseline leap-day assertion originally chose an
interval ending before that leap day; widening the observed envelope through March1
made the assertion applicable. The preserved-reader module needed sys.modules
registration for Pydantic forward references. Immediate reload after Save caused
abandoned read requests; the final test waits for saved route load before reload.
A timed-out fixture's task-owned disposable container was removed after its process
ended; retained databases were not affected. Raw traces/log headers stay temporary.

## C10 follow-up boundary

Observed: a six-block saved read exceeded the default20s expectation and Save exceeded
10s in one suite; extended observations completed. Source inspection identified
whole-document preflight per block result read, no-filter preflight decoding complete
canonical history, and repeated save checks. A transient process sample showed native
Parquet decode work while database sessions were idle. These are diagnostic inputs,
not causal attribution or comparable performance measurements. C10 must measure the
paths while preserving current authorization, artifact integrity and CAS. No SLO,
scaling, speedup or production-readiness claim is made here.

Other timezone/DST/calendar profiles, population axes, general filter providers,
export/delivery parity and full C04/C05–C11 remain required work.
