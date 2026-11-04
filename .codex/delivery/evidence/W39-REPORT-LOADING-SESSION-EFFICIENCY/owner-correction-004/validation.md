# Correction 004 validation

Run from the repository with `source scripts/activate-toolchain.sh`.

| Command | Result / boundary |
| --- | --- |
| `corepack pnpm --filter @custometry/web build` | PASS: TypeScript + production Vite. Existing >500 kB chunk warning remains. |
| `corepack pnpm --filter @custometry/web test` | PASS: 21 files / 106 tests. |
| `corepack pnpm exec playwright test --config tests/e2e/report-loading/correction004.config.ts` | Initial failures reproduced real stretched-hit defect; final product run passed persistence and reduced-motion. Interaction final rerun below passes. |
| Same Playwright command with `--grep "whole-card"` | PASS: actual coordinates/keyboard/controls/drag, no API requests or blank/busy frames. |
| Same Playwright command with `--grep "real context"` | PASS: added real tooltip/table percentage check plus selection-only Save/reload and stale-context guard. |
| `uv run --locked python -m tools.check --scope local` | PASS `check:local (observed=true)`. Local structural proof only. |
| `node apps/web/scripts/generate-pilot.mjs --check` | PASS generated runtime/source map current. |
| `git diff --check` | PASS. |
| SHA-256 comparisons | PASS: 169 inherited frozen inputs, 23 previously qualified backend files unchanged. |

Logs are appended here as `correction004-*.log`. First/second browser runs retain
failures; the second persistence failure was a fixture setup issue (already
selected average receipt after the preceding real Save), fixed by selecting
revenue before Apply so the test actually exercises selection-only Save.
Third run's drag assertion used a 1480 px rail with only 2 px overflow; the final
interaction rerun uses 900 px and passes. Product pointer activation was fixed by
the scoped active-transform override, not by loosening hit assertions.

Current build manifest SHA-256:
`013701150e9d72a5eb9e80b6d6fddb3771e061c1100b614d647bcc8d8fee9c1e`.
Assets: `index-6iCPac-k.js`, `ReportWorkspace-Bio0lH9o.js`.
See [identity](identity.json), [interaction](interaction-proof.json),
[persistence](persistence-proof.json), [reduced motion](reduced-motion-proof.json).
No inference of production delivery, MS-004 acceptance, or updated load budgets.
