# MS-023 verification

Only servicing c67c changed. Retained41746 and existing data preserved. Genuine provider
proof uses owned fresh source/control PostgreSQL, intake/publication, immutable Artifact,
current Identity and actual native Parquet/DuckDB. No production/publication/deploy action.

- Genuine provider command:uv run --locked python tests/integration/analytics/run_retail_filters.py
  --image sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4
  --test-file test_retail_customer_event_provider.py. Final:1 passed in15.05s.
  Independent source SQL verifies observed customer universe and two strictly ordered
  completed receipts within365 elapsed days, both unrestricted and store1. Unknown
  absence remains unknown. Catalog/preview metadata and exact cutoffs, empty access,
  foreign workspace, forged event-time field, old endpoint refusal, no membership IDs,
  no-store caching, CSRF, view-only preview denial, mid-read policy change and catalog
  GET session revocation were exercised through real services/HTTP.
- Initial genuine run failed resource preflight: anonymous null-customer receipts were
  grouped into an artificial parent fanout. Nullable edges now exclude explicitly
  unlinked rows from relationship fanout. Input rows/bytes and all other work limits
  remain enforced; no budget increase. Actual-Parquet100-unlinked-row regression passes.
- Final focused backend:200 passed in8.09s. Includes9 customer boundary cases,7 new
  Semantic cases, prior event/aggregate/relational/flat/admission/cancellation/identity
  and receipt-scope regressions. Earlier43 focused cases overlap this count.
  Composite namespace/customer keys were checked: a null optional customer key is
  unlinked, missing required namespace and nonnull orphans still fail. Mandatory
  universe cannot be weakened by a user true/NOT expression. Old nullable reader rejects.
- Focused Ruff/Pyright:pass, zero errors. TypeScript client check:pass. Deterministic
  workspace/composer client and documentation index regenerated. Grouped
  tools.check --scope local and git diff --check:pass. Initial static failures were
  fixture registration annotation and policy-string type inference; corrected without
  weakening checks. Observed profile is local, not CI/release.

No mounted sequence authoring, saved receipt-cohort projection, full Customer universe,
complete business/property history or performance/production-readiness claim.
