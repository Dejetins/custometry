# MS-004-S04 validation

Verification date: 2026-09-21 local / 2026-09-20 UTC. Canonical checkout:
`/Users/daniildegtyarev/.codex/worktrees/575c/Custometry`.
Use `source scripts/activate-toolchain.sh` before the commands below. Existing
Node 24.18.0, pnpm 11.13.0, uv 0.9.26 and installed browsers were reused.
No dependency installation, image build, publication or deployment occurred.

## Source and fixture checks

| Command | Observed outcome |
|---|---|
| `corepack pnpm --filter @custometry/web test` | Passed: 85 tests in 20 files. Includes query/display identity, copied IDs, selected view projection, source preservation and obsolete response-body rejection. |
| `corepack pnpm --filter @custometry/web typecheck` and `corepack pnpm --filter @custometry/web lint` | Both passed, exit 0; both scripts use `tsc --noEmit`. |
| `node apps/web/scripts/generate-pilot.mjs --check` | Passed, exit 0; maintained seam matches generated runtime and original source document. |
| `uv run --locked ruff check tests/e2e/ms-004-workspace` | Passed. |
| `uv run --locked ruff format --check tests/e2e/ms-004-workspace` | Passed: both Python files formatted. |
| `uv run --locked pyright tests/e2e/ms-004-workspace/scenario.py tests/e2e/ms-004-workspace/real_api_fixture.py` | Passed: 0 errors, 0 warnings. Optional tool-update notice did not change the installed runtime. |
| `uv run --locked python -m tools.custometry_quality.generate_docs_index` | Passed; generated navigation is current. |
| `uv run --locked python -m tools.check --scope local` | Passed on source and documentation; final receipt binding is verified separately. |
| `git diff --check` | Passed. |

## Real browser/API proof

```sh
corepack pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/ms-004-workspace/playwright.config.ts
```

The final full invocation ran all eight cases: **6 passed, 2 failed in 5.6m**.
Both failures were the new keyboard catalog check at its initial add-card step.
The test sent Tab/Enter without waiting for the asynchronously loaded catalog
button; no API error or browser exception occurred. Adding an explicit enabled
catalog-button precondition produced **2 passed in 1.6m** on both widths.

Final source review then corrected retained old-card bulk selection on workset
copy/new/remove. The catalog test now selects an old card, copies the workset and
asserts zero selected new cards before proceeding. The exact focused command:

```sh
corepack pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/ms-004-workspace/playwright.config.ts -g 'workset catalog'
```

**2 passed in 1.7m** (1920: 44.5s; 768: 48.5s), exit 0. The six unchanged
successful cases from the full invocation are reused; they were not rerun for
this isolated selection-reset path. All eight defined scenario/viewport pairs
therefore have passing evidence, across these invocations rather than a single
all-green invocation. The final Web unit suite and TypeScript gates also passed.
An earlier 8/8 run predating the reader fix is supplementary only.

[Browser summary](browser-summary.json) binds the eight final observation files.
They record no unexpected API errors and no page exceptions. Expected 401 session
checks/logout and 409 competing-save conflicts are classified separately.
Screenshots under `browser/` were visually inspected at 1920, 768 and 400 widths:
the original dark shell/rail/navigation remains, numeric formatting is readable,
the docked inspector becomes an overlay at 768, controls reflow at 400, and the
revenue/receipt pair has distinct labelled axes. Full data stays available in the
accessible table; this is not a full accessibility certification.

The final focused fixture exited successfully; the S04-owned Docker label returned
no remaining containers. [Corpus](corpus.json) identifies the final focused-run
source/control scope and six admitted bindings. Separate browser invocations use
distinct synthetic workspace/resource IDs; their observations are not relabelled
as one shared database or corpus.

The harness starts its own loopback production API on 58144, Vite on 41744 and a
unique disposable PostgreSQL container with source/control databases. Actual
six-table intake produces admitted artifacts; requests use real Identity sessions
and mounted S03 APIs. There is no browser API interception or mocked runtime.
The fixture POST helper withdraws only the reader's report run grant through
OrganizationService; it leaves functional analyst permissions and analysis data
policy unchanged. This tests **absence of effective run authorization**, not
removal of the functional `analysis.run` permission.

## Development failures and scope corrections

- Empty ECharts axes, an inconsistent copied workset selection and test locator/
  readiness issues were corrected before the final run. No failed iteration is
  counted as a passed check.
- [Viewer denial observation](viewer-denial-observations.json): replacing the
  analyst bundle with pure viewer produced editor GET 403. D06 requires both
  report.read and analysis.read. The coordinator confirmed this as expected
  denial rather than a backend defect; no role bundle or server policy changed.
- [Policy-change observation](policy-change-observations.json): withdrawing both
  report and analysis grants was followed by rejection of the existing view read
  (GET 409); this was outside the unchanged-data-policy no-run scenario.
  The final no-run regression changes only report run authorization, preserving
  result data-policy identity. This exploratory failure is not a terminal pass.
- The first successful no-run save/reopen scenario then failed a text assertion
  comparing innerText with textContent; values matched and only cell whitespace
  differed. The final assertion compares innerText consistently, with an explicit
  non-base period and actual row count.

Observations retain only synthetic resource paths, request methods/statuses and
browser diagnostics. No credentials, cookie values, request bodies or provider
rows are copied into evidence. The two exploratory observation files preserve
the original classifier output; the explanations above record their interpretation.

## Evidence boundary and next work

This is source-backed native-pilot integration and real local API/browser smoke.
It does not replace S02 independent SQL reconciliation or S03 complete API/
transaction/access proof. S05 must consume/extend this actual harness for all
AC-01…11 cases, including same/different-unit comparisons, all fiscal boundaries,
negative access, legacy exact versions, fault/restart recovery and owner review.
No CI, HTTPS packaging, release, installation or production conclusion follows.
