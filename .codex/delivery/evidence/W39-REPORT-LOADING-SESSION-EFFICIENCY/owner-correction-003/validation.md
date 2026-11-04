# Correction 003 validation

All commands run at repository root after `source scripts/activate-toolchain.sh`.
No automatic retries, backend/idle/load or full previous regression campaign.

| Command | Outcome |
| --- | --- |
| `corepack pnpm --filter @custometry/web build` | PASS TypeScript + production Vite; existing chunk-size advisory |
| `corepack pnpm --filter @custometry/web test` | 105/105 PASS, including16 focused presentation cases |
| `corepack pnpm exec playwright test --config tests/e2e/report-loading/correction003.config.ts` | 4/4 PASS:2688/1480/400 geometry and real complete-context cards/hover |
| Same browser command with `--grep "real complete"` | 1/1 PASS; exact current/prior series values unchanged with padded axes |
| `uv run --locked python -m tools.check --scope local` | PASS: static repository profile; see local log |
| `node apps/web/scripts/generate-pilot.mjs --check` | PASS (exit0); see generator log |
| `git diff --check` | PASS (exit0); see diff log |

Logs: [build](build.log), [units](unit.log), [browser](browser.log),
[series parity](series-parity.log), [local](local.log), [generator](generator.log), [diff](diff.log).

Focused unit cases: correct bound metric aggregate, mismatched/malformed/missing
result rejection, positive/negative/zero/small signed formatting, incomplete and
zero-baseline rendering, comparison disabled/unapplied state, and axis bounds for
6–7 counts, constants, zero, negatives, mixed signs, small decimals, empty and
independent unit magnitudes. Nulls are not coerced to0. Percent values are supplied
by the server, not summed/derived in the presentation code.

Real complete-context proof uses existing separately seeded synthetic report
`86d32ae7-c5cb-5a4f-87c9-45d0e33886a0` with transient Apply only. January aggregates
are positive; February receipts aggregate is −3/−1.595744…%; January1 receipts
aggregate is0/0%. All six cards match their own metric changes. Mouse movement onto
real plotted bucket coordinates exposes actual tooltip nodes with corresponding
positive/negative/neutral colors; current and baseline series remain exact server
values. Annual incomplete coverage is separately shown visibly in responsive tests.

The read-only owner January request is recorded in [owner source](owner-jan-source.json).
Original user tabs, unsaved draft, owner report versions, and source seed data were
not mutated. Independent Browser QA is attributed separately in [report](report.md).

Initial attempts: a missing tooltip object brace caused a compile error and was
fixed before the first successful build. A Browser test used an ambiguous global
Context button selector; scoping it to inspector navigation fixed the harness.
Three geometry tests had already passed. The final full four-test run passed.
After screenshot inspection, card metadata was fitted to its10 px row and footer
small text explicitly retained10 px sizing; tiny nonzero signed values retain a
sign through significant-digit formatting. Final build/unit/browser checks used
those changes. No older correction evidence was overwritten.
