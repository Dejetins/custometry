# MS-009-S01 independent review

Reviewer: read-only QA subagent `01a1158b-dd7c-7503-be8d-4ada8acf5e70`.
Scope: new semantic/analytics contracts, DuckDB input/compiler/engine, integration
tests and declared bounded milestone. No reviewer writes or recursive reviews.

Initial verdict: one P1, introduced dictionary-encoded Parquet expansion could
allocate a full Arrow table before checking decoded bytes. Reviewer reproduced
10,000 rows of 4096-character strings: file 17,014 bytes, metadata total_byte_size
12,350 bytes, decoded table 41,000,000 bytes. OOM was not induced. This blocked
AC-04 despite 43 passing tests. No other material findings in inspected scope.

Repair: dictionary-preserving string decode (including root ID), schema preflight,
512-row batches, columnar expanded-byte accounting before string casts, cumulative
output budget and cancellation at each decode boundary. Added expansion/cancel
regressions. No old schema/serializer changes.

Focused independent follow-up: P1 closed; no new blockers in bounded flat substrate.
Reviewer ran `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest tests/integration/analytics/test_columnar_filters.py -q -p no:cacheprovider`:
45 passed. Actual files refreshed before verdict.

Residual: a native decode batch is not preemptible by DuckDB interrupt; dictionaries,
decoder buffers and intermediate objects are not enclosed in a hard RSS sandbox.
The engine memory setting is not a whole-process memory guarantee. These limits
are documented and not claimed as achieved. Mounted provider/API/browser/full C04
and production are outside this review. Parent separately ran types/docs/local.
