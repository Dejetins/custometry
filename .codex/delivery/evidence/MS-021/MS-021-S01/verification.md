# MS-021 verification

Only the servicing c67c checkout changed. Retained localhost41746 and its data were
preserved. Genuine provider and browser work used owned disposable PostgreSQL/source
publication/API fixtures; no production writes, delivery or broad Git operations.

## Observed checks

- Focused backend suite:230 passed in6.74s, including aggregate SQL/old correlated/
  flat filters, scope composition and publication metadata cases. After review,
  two new publication-day regressions failed before the repair; the final8 Semantic
  plus2 scope cases passed in1.78s. These counts overlap, not additive unique coverage.
- Genuine retail aggregate provider test:passed initially in6.89s and after the
  publication-day repair in14.07s. Real source/control PostgreSQL, intake/publication,
  immutable Artifact/current Identity and DuckDB/HTTP; independent source SQL counts.
  Verified metadata/cutoffs, preview/facets, row ceilings, revocation, current grant
  changes, forged definitions, strict old reader, workspace and CSRF boundaries.
- Frontend:34 tests in7 files passed in4.05s. Aggregate count/distinct/ratio/windows,
  draft/reset/undo/abort, no-closed-day explanation, input focus and existing relational/
  temporal/composer behavior. TypeScript passed. Focused Ruff and Pyright passed
  (zero errors); generated workspace client is synchronized.
- Final real browser command:pnpm exec playwright test --config
  tests/e2e/ms-006-composer/playwright.config.ts aggregate-filters.spec.ts
  relational-filters.spec.ts filters.spec.ts. Three scenarios passed in3.2m,
  individually57.3s/53.8s/58.4s, one worker, retries0, fresh fixture.
  Count/distinct/ratio with independent windows and row predicates, inherited locked
  scopes, real Apply/Save/reload, title/copy identity, old v1/v2 behavior and RU/EN
  coverage were asserted. Count-only genuine history remains unknown; Boolean root
  alternative confirms actual members and positive source-derived revenue.
- Four attached screenshots were visually inspected.390px editor dates, wrapping,
  controls and actions remain usable. Saved EN/RU explicitly shows0 confirmed and
  5000 unknown receipts, null metric rows and incomplete-history explanation.

Generated documentation index, grouped `tools.check --scope local` and
`git diff --check`:pass. Observed profile:local; no CI/release claim.

## Failures and proof limits

Initial provider test used a search string that actually matched the localized
published label; corrected its unmatched-query fixture. Initial browser assertion
was case-sensitive for the distinct count label; corrected matching. A subsequent
aggregate-only browser run passed before the final provider repair.

The first final combined browser attempt failed aggregate Save at the capture proxy's
10s route.fetch timeout, and old flat-filter saved reload at a20s table expectation;
relational passed. Sanitized trace fields showed flat Save200, report GET200, one
result read200/aborted delivery and other reads/preflight pending at test expiry.
No response denial was observed there, but latency cause is not established.
The fixture was discarded, not blindly replayed after ambiguous Save. Explicit60s
capture/response and saved-table waits now bound these functional checks, leaving
10s UI actions/global configuration intact. Final fresh-fixture run passed all three.
This supports functional correctness only; performance regression/latency acceptance
is unproven and remains C10. Raw request headers/traces are not durable evidence.

Financial metric operands, intraday/relative windows, sequences/populations and full
FILTER-014/C04/C05–C11 remain required. No complete business history, CI/release or
production readiness claim follows from these local proofs.
