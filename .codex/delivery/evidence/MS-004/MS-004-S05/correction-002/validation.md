# Correction 002 validation

All commands ran in the canonical checkout with `source scripts/activate-toolchain.sh`.

| Command/check | Observed result |
|---|---|
| `corepack pnpm --filter @custometry/web typecheck` | Pass |
| `corepack pnpm --filter @custometry/web test` | 85 tests / 20 files passed |
| `node apps/web/scripts/generate-pilot.mjs --check` | Pass |
| `uv run --locked python -m tools.custometry_quality.generate_requirement_index` | Pass; generated content unchanged |
| `uv run --locked python -m tools.custometry_quality.generate_docs_index` | Pass; generated content unchanged |
| `uv run --locked python -m tools.check --scope local` | Pass after source/documentation updates |
| `uv run --locked python -m tools.custometry_quality.validate_prompt_packs` | Pass; original plan/prompt and consumed receipt bindings intact |
| `git diff --check` | Pass |
| `corepack pnpm --filter @custometry/web exec playwright test --config /tmp/ms004-correction.config.cjs --grep 'S05 fiscal|workset catalog|reader'` | 5 passed, 3.4 minutes, real live fixture |

Browser configuration reused the existing task-owned API58144/Web41744 without
webServer startup/cleanup. It selected parity/workspace/reader specs, workers1,
retries0, timeout240000, project1920×1080 and output `correction-002/browser`.
The fiscal and workspace tests additionally capture width400. Test fixture setup
uses real production calendar APIs; absence of calendar requests is asserted after
setup, during report reload/reading. Browser manifest includes exact artifact
hashes and safe network observations. All five scenarios had zero page exceptions
and zero unexpected API errors. Fiscal chart and 400px screenshots were inspected.

The successful reader scenario includes production logout and subsequent protected
UI clearing. Unchanged backend/security/calculation evidence is reused according
to the criterion amendment and source reconciliation manifest, not rerun as a
release campaign. No mock API, measured performance claim, deployment or remote
synchronization is part of this correction.

Original review001 report, validation, matrix, manifests, demonstration and receipt
were checked against all receipt hashes and remain byte-for-byte unchanged. The
original `Entry awaits owner input` preflight result preceded the supported resume
with new owner correction evidence; resume then passed under the original claim.
