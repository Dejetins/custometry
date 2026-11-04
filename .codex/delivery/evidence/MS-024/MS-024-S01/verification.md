# MS-024-S01 verification

All work is scoped to servicing c67c. Retained41746 and original project data are
preserved. No publication, deployment or production migration occurred.

- Actual trusted synthetic Parquet/DuckDB:22 cohort cases. Receipt grain, multiple
  receipts per customer, receipts outside history window, anonymous NOT unknown,
  orphan failure, forbidden events, negatives/multiple leaves, main/prelude/facet
  parameter order, cross-leaf node/scope/step collisions, global nodes/depth/values/
  correlations and summed work, registry origins, current authorization and old
  reader refusal. Real EXPLAIN JSON contains one MATERIALIZED cohort CTE per leaf
  and CTE_SCAN consumers. This is plan evidence, not a latency benchmark.
- Final focused backend:198 passed in2.07s, including those22 plus customer-event,
  sequence, aggregate, relational, flat input, Semantic, identity and saved-scope
  regressions. New API/backend focused Ruff and Pyright pass; TypeScript consumer
  check passes. Deterministic workspace/composer generators and documentation index
  regenerated; grouped tools.check --scope local and git diff --check pass. This
  is local proof, not ci/release or production readiness.
- Genuine owned fresh source/control PostgreSQL, publication, Artifact, Identity,
  native Parquet/DuckDB and HTTP:1 passed in5.35s via
  uv run --locked python tests/integration/analytics/run_retail_filters.py
  --image sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4
  --test-file test_retail_cohort_provider.py.
  Independent source SQL matches selected receipt totals and store1 restrictions.
  Receipt and paginated item facets match source totals; item oracle joins valid
  products to reproduce the established publication eligibility. The first item
  oracle included5 quarantined orphan-product rows (14199 versus14194); source
  quality rules and prior provider evidence established the cause. Corrected SQL,
  not executor behavior or budgets, resolved that oracle mismatch.
- Genuine HTTP checks catalog schemas/exact event cutoffs, receipt grain, no raw
  membership IDs, forged event/registry bridge denial, forbidden Customer facets
  and Receipt.customer_id facets, old-reader denial, no-store, cookie CSRF, empty/
  foreign scopes, view-only read/run separation, policy change during admitted input
  reading, ordinary catalog revocation and revocation exactly during the late
  retail_aggregate_projection bridge read. The latter returns401 after the repair.
- Independent review found2 P2s: customer IDs accessible through Receipt facets and
  missing Identity recheck after bridge IO. Trusted facet allowlist + identity pin
  and metadata-free current Identity recheck close them. Actual Parquet customer-key
  facet regression was red before the fix and green afterward. Genuine HTTP tests
  explicitly exercise both repairs. No checks are presented as full C04 completion.

S01 does not widen saved ReceiptSelection or mount UI. S02 must prove mixed scopes,
locks, persistence, exact windows and the real Apply/Save/reopen browser flow.
