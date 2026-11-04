# MS-022-S01-R1 result

A separate sequence-filter-execution/v1 capability now compiles ordered events into
the existing authorized DuckDB plan. Semantic definitions and trusted grants pin
native UTC event-time fields, meaning, exact observation/knowledge snapshots and
coverage evidence. Old flat/correlated/aggregate DTOs are unchanged and reject the
new nodes. No API, report-persistence, calendar control or browser capability changed.

Positive steps enforce strict time order, inclusive elapsed gaps and fixed or
publication-relative half-open windows. Negative steps require a preceding positive
anchor, evaluate only the requested interval/window and certify absence only with
complete authorized observations. Same-property/session equality across positive
steps validates types, versions and field equality capability. Unknown values/time/
history remain unknown; confirmed positive paths can survive incomplete history.

Admission hashes exact Parquet bytes, validates native timestamp(us,UTC)/known-column
schema and converts timestamps to exact integer microseconds without row-wise event
execution. Root/child ceilings, relationship keys, current grant recheck and existing
cancellation/resource limits remain. Candidate-path preflight includes the negative
probe fanout and its version participates in sequence identity.

Contract impact: additive unmounted internal Semantic/Analytics capability and trusted
reader projection. No old-schema widening, persistence migration or production action.
Actual Parquet/DuckDB tests are foundation proof; genuine publication/HTTP and mounted
report authoring follow. Full FILTER-015/C04 and C05–C11 remain outstanding.

The original S01 copied an incorrect plan body before product changes. Its blocked
instance, prompt/claim and exact historical plan remain preserved; corrected0.1.1 and
unique replacement S01-R1 were reconciled under the existing exclusive mechanism and
independently reviewed. No retrospective acceptance of S01 is claimed.

[Verification](verification.md), [review](review.md), [manifest](manifest.json),
[canonical journal](../../../ledgers/MS-022.md),
[reconciliation](../reconciliation/authoring-error.md).
