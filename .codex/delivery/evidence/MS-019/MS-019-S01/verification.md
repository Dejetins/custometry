# MS-019 verification

Only servicing checkout `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry` changed.
Retained runtime41746 unchanged. Browser uses disposable41747/58147/source/control
PostgreSQL; fixtures remove their containers. No publication/deploy/production writes.

- Focused backend suite:190 passed in0.99s across relational/flat execution, actual
  decimal Parquet storage, scopes, mount, receipt identity, temporal/year/workspace
  calculation and Semantic registry tests. New cases cover strict old readers,
  absent-byte compatibility, mixed registry bridge, malformed scopes/locks, exact
  selection evidence and temporal identity, facet grain/ceilings/search/work bounds.
- Independent review found presentation IDs incorrectly entering composed v2 identity.
  Two valid contract regressions failed on the original implementation and passed
  after request-local rebasing excluded block/source IDs. Related contract and
  Presentation service suite:45 passed in0.16s. This is two additional tests, not
  45 new tests; the earlier190 and follow-up overlap.
- Genuine provider fixture via `run_retail_filters.py --test-file test_retail_relational_provider.py`:
  1 scenario passed in2.91s. Actual intake/publication/Artifact/current Identity and
  Parquet/DuckDB; item facets independently match source SQL for full/store1 scopes.
  Existing genuine auth/CSRF/revocation/current-policy/unknown-history checks included.
- Frontend six focused Vitest files:30 passed in745ms; receipt/relational/scope editors,
  composer state and temporal editors/results. Upgrade, independent/same-item scopes,
  reset/undo, stale preview cancellation, item facets and registry refusal included.
- Real browser suite `relational-filters.spec.ts filters.spec.ts receipt-scopes.spec.ts`:
  3 passed in50.3s. New scenario proves genuine counts/results, mixed scopes, preserved
  locked constraints, explicit unknown values, negative absence and Save/reopen.
  Same-item preview observed4695 confirmed and305 unknown among5000 authorized receipts;
  impossible negative-existence predicate produced no confirmed receipts and null
  result values, not fabricated zero totals.
- Final extended relational browser after identity repair:1 passed in27.3s (test20.8s).
  Adds inherited v2 constraints, title-only edit and duplication before Save; four
  saved result bindings include exact reused result IDs for the duplicate. Reload,
  persisted locks/tampered removal rejection, RU/EN coverage and no pageerrors pass.
- Visual inspection of390px editor conditions/actions and saved result coverage:
  readable controls and expression, contained layout, explicit count grain/history
  limitation. Screenshots below are sanitized fixture evidence, not production proof.
- Ruff/Pyright for changed Python:pass; targeted rerun after identity repair:pass,
  zero errors. Frontend TypeScript, generated contract/docs indexes, local grouped
  gate and `git diff --check`:pass. Actual profile local, not CI/release.

Earlier browser failures exposed an Add-block validation race, fixed by disabling
and guarding Add while validation is pending; a delayed real response regression
proves the guard. Other failures were test synchronization (awaiting previous preview
or editing scopes before block commit); tests now await exact response and installed
block. Narrow screenshot capture initially clipped an overflowing locator; viewport
captures now show the actual scrolled controls. No backend guards were bypassed.

Images: [narrow conditions](correlated-editor-narrow.png),
[narrow actions](correlated-editor-actions-narrow.png), [saved EN](correlated-saved-result.png),
[saved RU](correlated-saved-result-ru.png).
