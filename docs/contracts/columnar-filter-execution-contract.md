---
doc_id: CONTRACT-COLUMNAR-FILTER-EXECUTION-001
title: Flat columnar filter execution contract
doc_version: 3
visibility: internal
ship: false
owner: analytics
requirement_ids: [FILTER-001, FILTER-003, FILTER-004, FILTER-005, FILTER-006, FILTER-016, FILTER-017, FILTER-018]
status: accepted
proof_boundary:
  label: local-flat-columnar-substrate
  exclusions: [mounted-provider, full-C04, relational-sequence-population, browser-proof, production]
---

# Flat columnar filter execution

[MS-009](../architecture/planning/milestones/MS-009/plan.md) implements a bounded
substrate of the [governed authoring target](analytical-authoring-contract.md).
It does not replace that target, existing Store filters or schema-v1 reads.
The owner explicitly authorized DuckDB in the [continuation addendum](../../.codex/delivery/evidence/WS-004/owner-continuation-addendum-2026-10-07.md).

## Trust and ownership

Semantic Model owns `FlatFilterRegistry` and published `FilterFieldVersion`
projections. They bind dataset/entity, stable and version IDs, types, permitted
operators, NULL behavior and optional observation-availability columns. A registry
projection must contain only fields the current actor may use. This is not a new
registry publication endpoint or a claim of general catalog/facet capability.

Analytics owns `FlatFilterRequest` and execution identity. A trusted
`FlatFilterAccess` implementation resolves current workspace/actor/dataset policy,
verified artifact binding, registry, explicit resource policy, root identity column
and mandatory row ceiling. These grants are server-only public port outputs, never
HTTP payloads or caller-supplied authorization flags. Integration must provide a
real authorization adapter; this milestone does not install an allow-all adapter.
The engine checks the binding and reauthorizes before returning. A changed grant
or revocation discards the result. PostgreSQL remains the control database.

## Input and calculation

Only a published materialized Parquet binding under the configured artifact root
is admitted. Directory-relative no-follow opens reject symlink traversal; files
must be regular and bounded. SHA-256 covers the exact in-memory bytes decoded.
Parquet metadata row/uncompressed-size preflight precedes decoding. String dictionaries
remain encoded in batches of at most 512 rows; expanded bytes are calculated before
dictionary casts and accumulated against the decoded-byte budget. Cancellation is
checked after each decoded batch. Selected field types must match exactly, with
unique non-null string root IDs.
No arbitrary path, connector read, implicit type coercion or client SQL is exposed.

The compiler generates internal column aliases and closed operators and binds every
value. Boolean predicates execute in DuckDB, including the mandatory row ceiling;
user NOT/OR cannot widen it. Decimal operands remain exact Decimal values; floats,
nonfinite or out-of-precision operands fail before input reads. Known field NULL
uses its versioned `not_matched` or `unknown` policy. Observation unavailable is
always unknown, including `is_null`. NOT unknown remains unknown. Counts describe
only the authorized universe; unknown members are not confirmed matches.

Identity includes canonical Boolean child order, typed operands, registry/field
versions and semantics, artifact ID/content, current policy, actor, root identity,
resource policy and engine version. No old workspace identity is changed. The
result is an exact flat-membership projection with coverage, not an estimated or
sampled preview and not a durable published report artifact.

## Isolation, limits and failure

Each operation gets its own in-memory connection. External access, automatic and
community/unsigned extensions, persistent secrets and Python replacement scans
are disabled; configuration is locked, disk spill is disabled, memory/threads
come from trusted policy. Plans are bounded by depth/node/value limits before
artifact reads. A monitor interrupts active engine work for cancellation/deadline,
repeats interruption to close query-start races, and joins before connection close.
Cancellation/deadline are checked around input reads and before delivery.

These are bounded generated queries and defense-in-depth settings, not an OS
sandbox for untrusted SQL or a hard process RSS limit. A single Arrow decode batch and trusted
access-port calls are not preempted by DuckDB interruption; metadata/input bounds
limit admission, dictionary expansion is preflighted, and cancellation is checked
at each batch boundary. Future remote
providers must supply their own I/O timeout contract. No latency/SLO claim is made.
Failures expose stable codes rather than DuckDB SQL, paths or provider rows.

Official implementation references: [Python API](https://duckdb.org/docs/current/clients/python/overview),
[settings](https://duckdb.org/docs/current/configuration/overview), and
[security model](https://duckdb.org/docs/current/operations_manual/securing_duckdb/overview).
Local behavior must be proved by tests; documentation alone is not execution proof.

## Compatibility and remaining work

Public HTTP routes, composer UI, old snapshots and old result serializers are
unchanged (`none`). New isolated port/DTOs and project dependency are additive
(`compatible-change`) for current consumers; no existing consumer is rerouted.
Rollback can leave these unused files/dependency without reinterpreting stored data.
No persistence migration is required or performed.

Correlated relationships, aggregate/window operands, behavioral sequences,
population references, registry search/facets, comparison expansion and mounted
API/browser save/reopen remain C04 obligations. Unsupported node kinds are rejected,
never downgraded to a flat approximation. Tests use disposable Parquet artifacts and
real DuckDB; synthetic fixtures prove engine semantics, not provider completeness.

## Published retail provider — MS-010

[MS-010](../architecture/planning/milestones/MS-010/plan.md) adds the genuine
`PublishedRetailFilterAccess` composition adapter. Identity reauthenticates current
analysis run/read permission and resolves the department/object Store ceiling.
Semantic Model resolves only published `retail-report/v1` Receipt data with declared
single source namespace and composite source/receipt primary key. Field versions
cover `source_system_id`, `store_id`, `status`, `currency`, `receipt_date`; the first
is mandatory source provenance. No customer PII, arbitrary channel or event-history
capability is inferred. Dataset/publication/field definitions pin registry identity.

Artifact Lifecycle's public `admit_filter_input` checks workspace, committed state,
entity and content binding and returns a `MaterializedFilterBinding`; it does not
read rows. The existing columnar engine verifies its exact bytes. Analytics never
reads Artifact or Identity private tables. The port is currently internal and no
new HTTP route, report serializer or composer editor is mounted by this unit.

An explicitly empty Identity Store universe compiles to an unsatisfiable mandatory
predicate. `None` means no additional Store restriction; an empty tuple never does.
Published non-PII field catalog and execution require both analysis.read and run in
this bounded adapter. A later read-only searchable catalog needs its own explicit
read permission path. Tests use real published intake/control/Identity/artifacts
and compare membership against independent read-only source SQL. Test resource
limits are explicit harness values, not production workspace policy defaults.

## Mounted composer path — MS-011

[MS-011](../architecture/planning/milestones/MS-011/plan.md) connects the published
Receipt subset to composer catalog, exact preview and bounded facet endpoints.
All read current Identity `view_snapshot`/analysis.read permission; computation
also keeps existing analysis.run and creator checks. Facets apply the mandatory
ceiling before grouping, search and pagination (maximum 50 values, offset 1000).
Preview returns counts, never raw membership IDs. HTTP disconnect signals evaluator
cancellation; the browser aborts replaced previews and ignores stale responses.

Queries may persist `receipt_filter` with `receipt-filter/v1`, pinned registry and
typed expression. Existing absent-filter serialization and calculation identity
remain unchanged. New inputs require a compatible reader; old readers reject them
without dropping fields. DuckDB computes membership; Arrow applies that membership
to the existing receipt calculation input. Source freshness retains the original
input observation time. Current policy, registry, engine and resource versions
participate in filter identity; layout remains outside analytical identity.

Trusted local configuration sets a default maximum of 1,000,000 rows, 64 MiB input,
128 MiB engine memory and 10 seconds; bounds hash into a resource-policy version.
These are conservative local admission limits, not normative latency promises or
a completed general workspace-policy management UI. PostgreSQL remains state truth.
Read previews cover the whole authorized dataset and label that scope explicitly;
period and metric eligibility continue to be shown by the block context.

The block builder separates draft conditions from applied settings; Reset and Undo
operate on the draft, and the final builder commit revalidates the document. Search
uses only the bounded published catalog; nested AND/OR and NOT remain typed trees.
Full relational/event/population authoring and Focus integration remain later C04
obligations, not capabilities inferred from this mounted flat subset.

Filtered workspace preflight and execution use Artifact Lifecycle's bounded reader:
all input/supporting byte sizes and canonical Parquet row/uncompressed sizes are
checked before any Python rows are materialized. String dictionary expansion has
a separate decoded-size check. Preflight/verification decode only Store identities;
full filtered calculation uses the admitted input. The legacy absent-filter path
retains its existing reader. Pending filter Apply disables builder commit, and
server definition validation remains separate from preview.
