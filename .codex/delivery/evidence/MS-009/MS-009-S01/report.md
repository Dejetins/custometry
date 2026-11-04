# MS-009-S01 — typed columnar execution substrate

AC-01–05 are technically verified within the bounded MS-009 plan. The journal owns
acceptance. This is not full C04 or a mounted composer/provider completion.

Added the approved DuckDB 1.5.6 dependency, published flat-field projection and
closed typed filter request/grant/resource/result contracts. The real adapter
admits integrity-checked materialized Parquet through a trusted current-policy port,
compiles generated parameterized plans and enforces a separate row ceiling. It
preserves exact decimals, NULL/unknown distinctions and coverage, pins semantic
and authorization identity, rechecks access before delivery and uses isolated
connections with forbidden external access/extensions/config changes, resource
preflight, cancellation and sanitized failures.

Independent review found and closed dictionary expansion before size checking;
[review](review.md) preserves the finding and follow-up. [Verification](verification.md)
records actual commands, failed attempts, 45 adapter tests, 72 combined tests,
Ruff/strict types and local profile. No runtime/user-data reset or publication.

## Contract impact

- New semantic projection and analytics port/DTOs: compatible-change, additive
  isolated contracts. Old Store/v1/v2 serializers and callers stay unchanged.
- API/browser/persistence/old result identity: none; no endpoint mounted, no
  schema migration, no rewrite of reports or snapshots.
- Runtime dependency: compatible-change in local project; lock delta preserves
  previous versions. No production delivery proof.
- Security/resource boundary: new verified input and execution path, independently
  reviewed; hard RSS sandbox and single-decode preemption are not claimed.

Requirement contribution: FILTER-001/003/004/005/006/016/017/018, strictly the flat
substrate parts mapped in plan AC-01–05. General registry/facets, relational/sequence/
aggregate/windows/population, comparisons and composer integration remain open.

## Owned file manifest and synchronization

Created:
- `packages/contracts/semantic/filter_fields.py`
- `packages/contracts/analytics/columnar_filters.py`
- `packages/analytics_core/infrastructure/columnar_filters.py`
- `tests/integration/analytics/test_columnar_filters.py`
- `docs/contracts/columnar-filter-execution-contract.md`
- MS-009 plan/prompt/journal/preparation/evidence/receipt and WS-004 authority addendum
  plus preserved WS-004 v0.2.4 snapshot (authorized preparation).

Modified owned hunks: `apps/api/pyproject.toml`, `uv.lock` (DuckDB only),
WS-004 v0.2.5 child binding, `docs/architecture/README.md` navigation,
`docs/README.md` generated index. No deletions. No product files outside declared
stage zones. Authority/parent preparation preceded the claim and is separately
identified; earlier dirty checkout work and completed journals/receipts unchanged.

Parent/child and triad links, exact plan hash, requirement revision, capability
implementation digests and contributor index synchronized. Current authorization
resolves the old dependency restriction without modifying immutable past evidence.

## Continuation

Implement genuine published-input/registry capabilities and composer-facing provider
integration next under the same owner continuation authority. Do not represent a
trusted test admission fixture as a production adapter. Preserve Forecasting holds,
old report data and all previous stage acceptance boundaries. No renewed dependency
or technical-plan acceptance is needed. C04 and C05–C11 remain unfinished.
