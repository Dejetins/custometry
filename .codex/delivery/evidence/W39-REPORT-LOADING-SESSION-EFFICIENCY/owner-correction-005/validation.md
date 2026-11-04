# Correction 005 validation

Commands run after `source scripts/activate-toolchain.sh` in c67c.

- `corepack pnpm --filter @custometry/web build`: PASS TypeScript + Vite. Existing chunk-size advisory remains.
- `corepack pnpm --filter @custometry/web test`: PASS21 test files,106 tests.
- Real in-app Browser: PASS focused geometry, catalog expansion, on-page display/pair controls, Focus deep link/resize/exit and keyboard restoration at2688/1480/400. Observations in [report](report.md); no new automated browser suite claimed.
- `uv run --locked python -m tools.check --scope local`: PASS `check:local (observed=true)`.
- `node apps/web/scripts/generate-pilot.mjs --check`: PASS (exit0).
- `git diff --check`: PASS (exit0).

No backend/idle/load campaign repeated. Earlier evidence is retained with its original identities.

Hash comparison:169 frozen inherited inputs and23 qualified backend files unchanged.
