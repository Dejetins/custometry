# MS-010-S01 — published retail filter provider

AC-01–04 verified within the bounded published-provider scope. Canonical journal
owns stage acceptance. Full C04 and subsequent WS-004 outcomes remain incomplete.

Semantic Model now exposes an explicit versioned Receipt filter projection for
source namespace, Store, status, currency and receipt date from the published
retail profile. Artifact Lifecycle admits current committed workspace/entity/hash
references without materializing rows. The composition adapter resolves current
Identity read/run permission, object and department Store limits, supplies mandatory
namespace/Store predicates and the trusted resource policy to real DuckDB execution.
Changed access or revoked session prevents delivery, including after input admission.

[Verification](verification.md) records 77 focused tests and the real disposable
PostgreSQL/source/Identity/artifact/DuckDB run, independent SQL membership oracle,
negative cases, fixture correction, types/Ruff/local checks. [Independent review](review.md)
found no material security/contract issue in this bounded additive path.

## Scope and contract impacts

New public projection/admission ports, binding type and composition adapter are
`compatible-change`; no prior consumers are rerouted. Existing HTTP APIs, composer
UI, persistence schemas, snapshots and result identities are unchanged (`none`).
No private cross-context table read in product code; owner adapters own DB access.
No dependency change in this milestone, no production migration/publication.

Requirement contributions: FILTER-001/002/003/004/005/006/010/017, only the declared
non-PII retail provider subset. Full searchable registry/facets, correlated/sequence/
aggregate/window/population evaluation and mounted composer integration remain open.

## Owned manifest / documentation

Created: `packages/semantic_model/application/retail_filters.py`,
`apps/api/src/custometry_api/analytics/filter_access.py`,
`tests/unit/semantic/test_retail_filters.py`,
`tests/integration/analytics/test_retail_filter_provider.py`,
`tests/integration/analytics/run_retail_filters.py`, MS-010 triad/preparation/evidence.
Modified owned additions: `packages/contracts/analytics/columnar_filters.py`,
`packages/semantic_model/infrastructure/postgres.py`,
`packages/artifacts/infrastructure/sales.py`,
`docs/contracts/columnar-filter-execution-contract.md` v2,
architecture navigation and contributor index. WS-004 v0.2.6 binding/predecessor
snapshot were authorized preparation before claim. No deletions or foreign rewrites.
Old accepted prompts/journals/receipts remain immutable; only MS-010 journal changes
through its exclusive updater. Parent/child, exact versions and triad links current.

Next: mounted catalog/preview/facets and persisted composer integration under the
same continuation authority, followed by remaining typed C04 capability families.
No repeated owner acceptance is required. No full outcome completion is claimed.
