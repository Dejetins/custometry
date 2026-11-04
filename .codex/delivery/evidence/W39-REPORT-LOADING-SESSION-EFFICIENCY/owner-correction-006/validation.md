# Correction 006 validation

Commands run after `source scripts/activate-toolchain.sh` in c67c.

- `corepack pnpm --filter @custometry/web build`: PASS TypeScript + Vite; existing chunk-size advisory remains.
- `corepack pnpm --filter @custometry/web test`: PASS 21 files, 106 tests. These are existing focused source tests, not a new automated menu suite.
- Real in-app Browser: PASS at 1480x969, 2688x1575 and 400x900 for header geometry, title draft/restore, menu Tab/Escape, adjacent status, workset Add guard, inspector entry and cached card selection. Final build additionally verified matching aria-controls/panel ID and no console errors. [Observed details](report.md).
- `uv run --locked python -m tools.check --scope local`: PASS `check:local (observed=true)`.
- `node apps/web/scripts/generate-pilot.mjs --check`: PASS exit0.
- `git diff --check`: PASS exit0.
- Hash comparison: 169 inherited frozen paths and 23 qualified backend files unchanged.

No owner report Save, production delivery or renewed performance campaign. Browser checks used the real local platform in an independent tab; the original user tab was preserved. Viewport override reset. No API payloads, credentials or browser storage are retained here.
