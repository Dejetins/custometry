# MS-022 sequence verification

Servicing c67c checkout only. Tests use owned synthetic immutable Parquet files and
actual Arrow/DuckDB. Identity/Semantic grants are trusted synthetic seams. No genuine
publication/HTTP/browser/production claim; retained41746 runtime/data unchanged.

## Checks

- Initial18 sequence cases:15 passed,3 negative-step cases exposed a DuckDB internal
  binding error in multiply correlated CTEs. The shared safe executor still returned
  a typed execution failure. Authorized child CTEs now remain uncorrelated; every
  positive path, negative probe and unknown-time fallback explicitly enforces parent
  keys. All18 then passed. No optimizer disabling or row-wise Python fallback.
- Expanded26 cases exposed an event at the global exclusive window end affecting a
  negative step. Added explicit upper-window restriction;96 sequence/aggregate/
  correlated cases passed. With cancellation/integrity cases,165 focused cases passed.
- Independent review identified missing negative-probe fanout in work estimation and
  missing field equality capability checks for property bindings. Both reproduced as
  failing actual-Parquet regressions. After fixes, final167 cases passed in6.99s,
  including30 sequence cases. Counts overlap, not additive independent coverage.
- Final command:uv run --locked pytest -q
  tests/integration/analytics/test_sequence_filters.py
  tests/integration/analytics/test_aggregate_filters.py
  tests/integration/analytics/test_relational_filters.py
  tests/integration/analytics/test_columnar_filters.py
  tests/unit/analytics/test_bounded_filter_inputs.py
  tests/unit/analytics/test_filter_cancellation.py
  tests/unit/analytics/test_receipt_filter_identity.py
  tests/contract/presentation/test_aggregate_receipt_scopes.py
  tests/contract/presentation/test_relational_receipt_scopes.py
  tests/contract/presentation/test_receipt_scopes.py.

Observed cases include equal/reverse timestamps, exact microsecond gaps, complete/
incomplete negative intervals, global and anchor half-open boundaries, a subsequent
positive after negative completion, unknown timestamps/properties, hidden roots and
child events, publication-relative bounds/identity, property bindings, Boolean NOT/OR,
strict old readers, forged definitions/cutoffs/scopes, native timestamp and known-column
schema mismatches, changed current authorization/evidence, work/correlation ceilings,
cancellation and byte-integrity failure.

No performance assertion follows from the work preflight test: it proves rejection
under declared resource policy, not measured latency/throughput. C10 remains open.

Final focused Ruff and Pyright:pass, zero errors. Generated documentation index and
grouped `tools.check --scope local`:pass. `git diff --check`:pass. These establish
the local profile, not CI/release or production delivery. Initial static failures
were unformatted tests and missing container type annotations; corrected without
relaxing checks. Independent review cleared the two repaired boundary findings.
