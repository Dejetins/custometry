# C04 general provider dependency decision

Status: proposed; owner dependency authorization required. No dependency declaration,
lock update, download, installation or new provider execution has been performed.
This is a decision packet, not another execution journal or accepted milestone.

## Concrete decision

Authorize one new runtime dependency, `duckdb`, for the remaining C04 provider work,
with an exact compatible release pinned through the existing `uv.lock`. Scope the
change to `apps/api/pyproject.toml`, the workspace lock and project-local `.venv`;
follow with isolated tests in the current disposable API/browser harness. Do not
change global runtimes, retained server 41746, production, deployments or unrelated
dependencies. Preserve foreign lock changes and review the resolved lock diff.

DuckDB is already selected by the normative stack (technical blueprint §18.2,
FILTER-006/017); it is missing from the current project dependency declarations and
runtime. The current WS-004 authority explicitly excludes new dependencies. General
execution therefore cannot be claimed merely from adding scopes or AST contracts.
The installed PyArrow is useful for interchange, but does not establish the required
typed relational/temporal evaluation and resource-preflight proof. Row-wise Python
or browser filtering is not a permissible substitute under FILTER-018.

## Proposed implementation boundary after authorization

- Semantic public contracts own versioned FilterField/relationship/event policies,
  typed v2 scopes/operands and pinned relative-time/population references.
- Analytics owns normalized plan, current-policy revalidation, typed execution,
  three-valued match state, coverage and immutable result identity.
- A DuckDB infrastructure adapter consumes only authorized, verified Arrow/materialized
  inputs. Use per-operation connections and generated typed plans, never arbitrary
  user SQL or unvalidated identifiers. Disable external access and automatic extension
  loading; enforce resource/cancellation policy and verify the configured restrictions.
- PostgreSQL remains the control database; DuckDB is an execution adapter. Public
  ports preserve context boundaries. No private cross-context table reads.
- Composer consumes actual capabilities/catalog/facets, supported preview/estimate,
  general scopes and authoritative comparison outputs. Unsupported source history or
  population providers retain explicit blockers until genuine inputs are available.

The adapter is a proposed design, not verified execution. Official DuckDB documents
Python in-memory connections and typed data ingestion, and provides external-access
and resource controls; those controls still require repository tests and do not by
themselves authorize or secure an input. References checked 2026-10-07:
[Python API](https://duckdb.org/docs/current/clients/python/overview),
[configuration](https://duckdb.org/docs/current/configuration/overview),
[securing DuckDB](https://duckdb.org/docs/current/operations_manual/securing_duckdb/overview).

## Acceptance and recovery

Before advancing dependent outcomes, require semantic truth-table/null/unknown tests,
correlation and cardinality proof, exact decimal/ratio behavior, current permission
and forbidden-input tests, cancellation/resource-denial checks and real columnar
execution evidence. Then add API/browser scope, facet, window/population and cache/
manifest identity tests against actual supported inputs. Keep old v1 and current
Store subset semantics unchanged. A successful import alone proves none of these.

If authorization is denied or absent, retain the completed MS-008 foundation, do not
install or claim full C04, and continue only independent authorized contracts/design
work. C05–C11 dependent acceptance cannot bypass missing provider semantics. This
request does not lift forecasting holds or other owner decisions.

Parent: [WS-004](../../../../docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md).
Current basis: [provider inspection](../MS-008/preparation/provider-inspection.md),
[MS-008-S02 evidence](../MS-008/MS-008-S02/report.md),
[owner authority](owner-continuation-2026-10-07.md).
