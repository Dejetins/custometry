# MS-020 verification

Servicing checkout only; retained41746 runtime and existing data unchanged. No browser
or external provider writes. Tests use task-owned temporary immutable Parquet files
and actual isolated DuckDB queries; Identity/Semantic admission grants are synthetic
trusted seams. This is foundation proof, not genuine publication/API/browser proof.

- Initial aggregate cases:24 passed. Expanded aggregate/correlated/facets/decimal/
  flat/scopes suite:124 passed in0.84s, including27 aggregate cases. Two additional
  Boolean three-valued/distinct/revocation cases then brought the aggregate suite
  to29 passing cases in0.40s. Exact publication cutoff/microsecond regression then
  brought the aggregate suite to30 passing cases in0.39s. Counts overlap, not
  additive independent coverage.
- Checked complete empty zero, child/parent half-open windows, nonempty exact counts,
  distinct known-null exclusion versus unknown properties, incomplete relationship
  or observation interval, exact ratio/window-to-window comparisons, zero denominator,
  composite grains, AND/OR/NOT, old-reader refusal and canonical Boolean identity.
- Checked hidden child before aggregation, unavailable property observations,
  root grain and current policy/evidence change rejection, relationship/field/grain/
  as-of/unit/scope/capability binding denial, correlation/value/work/fanout/cancellation
  limits, nonfinite/oversized scalar and non-UTC/naive/intraday/reversed window denial.
- Focused Ruff/Pyright:pass, zero errors. Generated docs index, grouped local gate
  and git diff whitespace check:pass. The observed profile is local, not CI/release.

Initial fixture setup used a Pydantic copy method on a dataclass artifact binding;
corrected to dataclasses.replace before running actual SQL cases. Static failures
were missing list/dictionary type annotations and fixture-import/formatting issues;
corrected without relaxing compiler/type/gate checks. Window boundaries remain
midnight UTC; publication as-of preserves exact aware UTC instants without rounding.

No complete FILTER-014 claim: actual retail publication still lacks certified business
history. Existing MS-019 mounted behavior remains governed by its separate evidence.
