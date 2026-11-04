# Correction 002 validation

Commands run from repository root after `source scripts/activate-toolchain.sh`.
The production preview remained 41746; browser tests used isolated contexts at
127.0.0.1:41746. No user-tab automation or full prior qualification campaign.

| Command | Result |
| --- | --- |
| `corepack pnpm --filter @custometry/web test` | 89/89 pass, including unfinished-set reuse and distinct-copy/data invariants |
| `corepack pnpm --filter @custometry/web build` | TypeScript + production Vite build pass; existing chunk-size advisory remains |
| `corepack pnpm exec playwright test --config tests/e2e/report-loading/correction002.config.ts` | Add/repeated/rapid/configure/copy/real Save-reload passes; initial geometry findings below |
| Same browser command with `--grep "independent docks"` | 8/8 pass after geometry fixes, with header/title/tab and keyboard assertions |
| `uv run --locked python -m tools.check --scope local` | PASS static repository gate, see local log |
| `node apps/web/scripts/generate-pilot.mjs --check` | PASS (exit 0), see generator log |
| `git diff --check` | PASS (exit 0), see diff log |

Logs: [web tests](unit.log), [build](build.log), [initial browser run](browser-initial.log),
[final geometry](geometry.log), [local](local.log), [generator](generator.log), [diff](diff.log).
The Add/persistence path passed before final CSS/header accessibility changes;
its workset logic was unchanged afterward. No uninterrupted nine-test green run
is implied. No auto retries were used.

During validation:

- The first browser invocation used a nonexistent `data-nav-root=data` selector;
  corrected to the source's `system` root before completing that run.
- Initial 768 px geometry found a 3 px margin difference between menu and workspace;
  corrected to the existing narrow 5 px top margin.
- A 400 px test assumed equal workspace height after switching differently sized
  menu groups. Corrected to assert same horizontal allocation and no overlap;
  content-height changes are intended for the stacked layout.
- Independent Browser QA found tabs overlapping the title on legacy400. The
  fixed 40 px row conflicted with the two-row responsive layout. Auto height
  fixed the defect, and direct containment assertions passed for all states.

[Identity](identity.json) records final sources and bundle; [frozen check](frozen-input-check.json)
and [backend check](backend-source-check.json) establish unchanged input boundaries.
Prior backend/idle and frontend load timings are not requalified by this correction.
