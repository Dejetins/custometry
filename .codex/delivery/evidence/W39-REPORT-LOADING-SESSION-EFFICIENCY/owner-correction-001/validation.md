# Correction validation

All commands ran from the repository root with `source scripts/activate-toolchain.sh`.
No automatic retries were configured. Production source was unchanged after the
final build; subsequent edits only adapt tests and append documentation.

| Command | Observed result |
| --- | --- |
| `corepack pnpm --filter @custometry/web test` | 87/87, [log](unit-final.log) |
| `corepack pnpm --filter @custometry/web build` | TypeScript + Vite pass, [log](build-final.log) |
| `W39_CORRECTION_PHASE=after corepack pnpm exec playwright test --config tests/e2e/report-loading/correction.config.ts` | 6/6, [log](responsive-final.log) |
| `corepack pnpm exec playwright test --config tests/e2e/report-loading/regression.config.ts --project 1920` | 7/8 initially ([log](desktop-initial.log)); temporal test observed retained table before new values arrived |
| Same regression command with `--project 1920 --grep "reader temporal"` | 1/1 after polling the unchanged expected values, [log](parity-final.log) |
| Same regression command with `--project 768` | 6/8 ([log](narrow-initial.log)); two harness failures below |
| Same regression command with `--project 768 --grep "reader pair\|workset catalog"` | 2/2 after fixes, [log](narrow-targeted.log) |
| `uv run --locked python -m tools.check --scope local` | PASS, [log](local.log) |
| `node apps/web/scripts/generate-pilot.mjs --check` | exit 0, [log](generator.log) |
| `git diff --check` | exit 0, [log](diff.log) |

Final applicable browser coverage: 6 targeted production-preview scenarios and
16 distinct regression scenarios across 1920/768, with targeted reruns as listed.
No inference of an uninterrupted 16-test green run is made.

Earlier failed attempts, retained here for attribution:

- Baseline login initially used the independent request fixture; browser cookies
  were absent. Corrected to the browser context request client before capture.
- TypeScript flagged inferred locale/union types during implementation; explicit
  plot props typing and unit lookup were corrected before the successful build.
- Inspector portal originally reused `.mw`; duplicate selectors were removed.
- Responsive audit assumed a plot existed while Table was selected; nullable
  geometry fixed that test. A genuine narrow focus-restoration ordering issue
  was corrected by restoring focus after removing inert.
- Four responsive tests attempted to serialize `expect.any(Number)` in
  `toHaveJSProperty`; replaced by measured height and actual resize assertion.
- New legacy fixture has no usable source result, so graph-ready was an invalid
  assertion. HTTP 200 and the explicit no-data state are checked instead.
- Retained table rows satisfy row-count checks before a new saved view loads;
  exact-value polling now waits for the same expected values, without weakening
  data parity. Temporal regression then passed.
- Narrow helper initially waited for visibility of deliberately hidden report
  content while the dock was open; it now waits for attachment and closes dock.
  That failed run was interrupted. Its disposable 41741/58141 processes were
  stopped before retry; existing 41746/API and owner ports were untouched.
- Final narrow pair failure was Chromium `Network.getResponseBody` buffer loss;
  the test now captures a clone of the actual browser fetch, as the temporal
  test already did. Catalog test tried role lookup while content was inert;
  it now closes the dock before asserting the workset controls. Both passed.

[Identity](identity.json), [169 frozen inputs](frozen-input-check.json) and
[23 backend files](backend-source-check.json) are independently hashed. The old
backend/idle proof is reused for unchanged source only; no new load qualification.
