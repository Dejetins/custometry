# MS-015 verification

Checkout: `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`.
Retained runtime41746 and user data were not changed. Integration/browser databases
were task-owned disposable PostgreSQL. Proof profile is local, not CI/release.

## Focused checks

- 95 backend tests pass: `test_zoned_calendar.py`, `test_year_comparison.py`,
  `test_temporal_resolution.py`, `test_temporal_projection.py`,
  `test_workspace_calculation.py` under `tests/unit/analytics/`, plus
  `tests/contract/presentation/test_temporal_scopes.py` and `test_workspace.py`.
- 23 frontend tests pass: mounted `composer-temporal-editor.test.tsx`,
  `temporal-comparison.test.tsx`, `composer-state.test.ts`.
- Frontend typecheck, focused Ruff and Pyright pass; Python typecheck has zero errors.
- Generated client/contract equality, docs index, `check --scope local` and
  `git diff --check` pass.

The tests exercise spring23h/fall25h/ordinary24h; Havana repeated midnight's earliest
instant; Apia skipped date and SaoPaulo missing midnight (including interior period
boundaries); half-open edge receipts producing exact110 vs previous1; missing one
intersecting source date makes local coverage unavailable without altering raw totals;
pinned replay without a package read; invalid zone, altered hash and supplied-rule
rejection. Actual frozen pre-MS014 results keep identical bytes/hashes. The preserved
pre-MS015 Semantic reader accepts identical v1 bytes and rejects new v2 profiles.
Scope test proves explicit adoption and rejection above a locked ancestor calendar.

## Real Semantic and browser boundary

The disposable Semantic suite passed2 focused scenarios (8 deselected) and checks real authenticated API, Origin/CSRF, roles,
CAS/idempotency and workspace access, plus v2 rules persistence, invalid zone and
caller-rule rejection. Committed v2 replay still succeeds after the rules provider
is made unavailable; key/body and stale-revision conflicts remain409. Both old/new
immutable versions remain exactly readable.

Playwright target41747/API58147, Chromium1440x1000, real published source/artifacts,
Identity/Semantic/Analytics and PostgreSQL. Captured upstream bodies are forwarded
unchanged, never mocked. Initial dedicated scenario passed; final combined
`timezone.spec.ts temporal.spec.ts` passed2 scenarios in1.1m. Company settings create
America/New_York; reapplying the old UTC block keeps its request/artifact hashes.
A new block uses that default; explicit adoption yields identical local totals.
Real Save/reload preserves reference, values, zone and actual25h vs24h display.
Previous/custom-period and inherited comparison regression also passes.

The sanitized `timezone-dst.png` shows one local date, UTC04:00→nextUTC05:00,25h;
previousday24h, raw668.22 vs958.02, delta−289.8, conservative coverage and descriptive
comparison. It was visually inspected; no raw trace/auth/provider payload is durable.

Initial TS check found optional generated v1 timezone; using its existing UTC default
fixed it. No implementation/runtime timeout was changed. Existing broader C10 timing
investigation remains open; no SLO or speedup claim is made.

Other calendar families/provider calendar maps/population axes, remaining general
filter providers, export/delivery parity and full C04/C05–C11 remain obligations.

Independent review found and cleared one inherited fixed-UTC editor label; final RU/EN
regressions pass. This copy-only change does not alter the proven runtime behavior.
