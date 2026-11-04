# MS-004 S05 validation

Technical checks are complete; finished-result owner acceptance remains pending. Commands
run in the canonical checkout after `source scripts/activate-toolchain.sh`, using
the existing locked toolchain. No dependencies were installed.

## Completed execution

- `MS004_S03_EVIDENCE_PATH=/tmp/ms004-s05-api-corpus.json uv run --locked python tests/integration/presentation/run_s03.py --image 5d004e058f52`: passed. Real integration corpus: 1 passed in 341.73s; retained legacy suites: 2 passed in 7.45s. No skips. The later local rename of a monkeypatch guard for typing does not alter executed semantics. See [corpus](api-corpus.json).
- `uv run --locked pytest -q tests/unit/presentation tests/contract/presentation tests/contract/analytics tests/unit/analytics tests/unit/identity_access`: 108 passed in 0.80s.
- `uv run --locked pyright apps/api/src tests/integration`: 0 errors, 0 warnings after the local test guard rename.
- Focused Ruff checks on the changed contract, Presentation service and integration test: passed.
- `corepack pnpm --filter @custometry/web test`: 85 tests in 20 files passed before final context/label refinements.
- `node apps/web/scripts/generate-pilot.mjs --check`: passed.
- Web typecheck: passed before the complete browser run.
- `MS004_S04_CORPUS_OUT=/tmp/ms004-s05-browser-corpus.json corepack pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/ms-004-workspace/playwright.config.ts`: 14 passed in 12.1m. Seven scenarios per 1920x1080 and 768x1024, with additional 400x900 desktop reflow. No retries, API interception or substituted calculation data. Evidence copied to [full browser run](browser/full-corpus.json) before another run could replace the output directory.

The full browser pass precedes final delayed-response tests and any consequent
context-generation correction, plus unit-label localization. Its product source
hashes are recorded in `browser/full-source-state.json`. Final targeted checks
below cover changed paths; unchanged math and API proof are reused explicitly.

## Disclosed development failures

- Initial API rerun failed because the new TestClient check incorrectly used the
  Vite `/api` prefix against the directly mounted app. Correct `/reports` paths
  passed the complete rerun above.
- One contract hash test failed before regeneration of the reports client; all
  108 focused checks passed after generators were run.
- Earlier browser authoring failures used the wrong English button name, sampled
  results before readiness, selected base_definition for a creator and observed a
  stale Saved notice before asynchronous Save completion. Explicit API/busy and
  result readiness predicates corrected these test errors.
- The narrow inspector remained unfocused after actual visibility; this was a
  product defect caused by the asynchronous portal mount, corrected with a callback
  ref and re-proven in both the targeted test and full browser run.
- The temporary standalone browser-test TypeScript config initially lacked Vite
  module resolution from the external test folder; explicit existing package
  paths resolved it. This was a scratch check configuration error.

## Reuse and boundaries

[Reuse analysis](reused-calculation-evidence.json) binds S02 SQL-oracle/corpus proof
to unchanged arithmetic, artifact and harness bytes. Ten retained service methods
match after normalization of three public method renames; current access/verification
seams are proved by the new API run. The owner did not request redundant full
calculation execution. S01 migration/settings proof remains within its unchanged
source boundary, while S05 repeats fiscal pin/adoption through API and browser.

No real browser proof is inferred from unit mocks. Actual browser observations
record expected denied responses separately from unexpected errors and contain no
cookies, tokens or raw provider payloads. Disposable fixtures own their processes,
databases/artifacts and cleanup; no original-checkout or unrelated runtime cleanup.

## Final source checks after repairs

- `corepack pnpm --filter @custometry/web test`: 85 tests / 20 files passed, 1.70s.
- `corepack pnpm --filter @custometry/web typecheck`: passed (`tsc --noEmit`), also the package lint command.
- `corepack pnpm --filter @custometry/web exec tsc --project /tmp/ms004-s05-browser-tsconfig.json --noEmit`: passed for the actual browser spec/config sources. The scratch config extends apps/web/tsconfig.json and resolves existing contracts, Vite and plugin-react packages explicitly; it installs nothing.
- `node apps/web/scripts/generate-pilot.mjs --check`: passed.
- `uv run --locked ruff check packages/contracts/presentation/workspace.py packages/presentation/application/workspace.py tests/integration/presentation/test_workspace_s03.py tests/e2e/ms-004-workspace/scenario.py`: passed.
- `uv run --locked pyright apps/api/src tests/integration tests/e2e/ms-004-workspace/scenario.py`: 0 errors / 0 warnings. A new-version advertisement is not an installation or a diagnostic. Initial fixture unused-handler diagnostics were resolved by the same explicit decorated-handler reference pattern already used in this fixture.
- `uv run --locked pytest -q tests/unit/presentation tests/contract/presentation tests/contract/analytics tests/unit/analytics tests/unit/identity_access`: 108 passed in 0.75s on final Python bytes.
- `uv run --locked python -m tools.custometry_quality.generate_docs_index`: passed, 73 contributor documents; no index drift.
- `uv run --locked python -m tools.check --scope local`: passed.
- `uv run --locked python -m tools.custometry_quality.validate_prompt_packs`: passed, four journals; active S05 preserved.
- `git diff --check`: passed for tracked changes.

The initial delayed-response run passed actual logout/body protection and failed
saved-context restoration after obsolete Apply completion. Its actual UI failure
is preserved under `browser/delayed-before`. The context-generation repair is
retested on both viewport projects in the final focused browser run. The fixture
holds only the exact production response body after sending headers/one byte;
there are no mocked API responses or replacement metric values. Its release state
must show `held:false,timed_out:false`, proving the test explicitly released it.

## Final focused browser execution

`MS004_S04_CORPUS_OUT=/tmp/ms004-s05-focused-corpus.json corepack pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/ms-004-workspace/playwright.config.ts --grep 'S05 reader|S05 late production|S05 Reload saved|workset catalog'`:
**10 passed in 4.5m**, no retries or skipped tests. Five cases per viewport:
Saved View pair, temporal/table/tooltip/Focus/delta/no-run parity, actual delayed
result JSON after logout, actual delayed Apply after explicit Reload saved, and
RU catalog/copy/six grains/fiscal adoption/keyboard with final localized chart/table
assertions and captures. The same final source bytes passed both projects.

The browser evidence and admitted corpus are copied under `browser/final/` and
`browser/final-corpus.json`; no later run can overwrite that durable copy.

A bounded additional fiscal run on 1920 passed (1 test, 1.6m) after the label/context
repairs. Subsequent visual inspection found the Focus/rail clipping and table
ellipsis described in [repair assessment](repair-review.md). Those captured outputs
remain under `browser/pre-layout-demo` as pre-layout evidence, not the final demo.

After the CSS-only correction, Web typecheck, the standalone actual browser-source
TypeScript check, native-pilot generation check, docs-index check and local profile
all passed again. No Python/API recalculation is claimed from these static checks;
its unchanged evidence remains valid.


## Final layout and demonstration verification

`MS004_S04_CORPUS_OUT=/tmp/ms004-s05-layout-corpus.json corepack pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/ms-004-workspace/playwright.config.ts --grep 'S05 reader temporal|S05 fiscal multi-workset'`:
**4 passed in 4.5m** (1920 and 768). It repeats complete temporal artifact parity,
Focus keyboard and explicit full-visibility/hit-test/no-cell-clipping assertions,
plus real fiscal settings/adoption, equal/different store identities, immutable
old snapshots and compute-free reopen. Final captures reside in
`browser/layout-final/`; the final admitted source corpus is
`browser/layout-final-corpus.json`. These are the owner demonstration's images.

The final fixture completed with exit 0 and its labelled Docker container list
was empty. The [browser manifest](browser-manifest.json) records zero page errors
and unexpected API failures in all successful runs. Expected 401 revocation and
409 conflict cases remain explicitly classified. Read-only visual inspection
confirmed the final 1920 fiscal table and 1920/768 Focus geometry; the 400px
scenario is desktop reflow, not a mobile-device certification.

Tracked whitespace and all task-owned untracked Markdown/JSON whitespace checks
passed. The final report, criterion matrix, demonstration, ownership/browser
manifests and source bindings are checked before the receipt-backed pause. No
owner acceptance or release/deployment proof is asserted.

The UI blueprint inventory was reconciled after the coordinator identified its
stale “plan, not implemented form” wording. The historical 2026-09-20 requirement
is retained, the accepted plan label now names editorial 0.2.1, and a dated
2026-09-21 S04/S05 local implementation note explicitly awaits owner acceptance.
Product requirements_revision remains unchanged; no C02/C03 or deployment claim.
