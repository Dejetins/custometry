# MS-020-S01 result

Added an explicit aggregate execution request over the existing bounded isolated
DuckDB engine. Semantic count/count_distinct definitions pin relationship, grain,
field versions, unit and null/empty/returns/time policies. Trusted CountInput binds
coverage, observation/knowledge cutoffs and evidence identity. Old saved receipt and
relational readers remain unchanged and reject new aggregate nodes.

The executor supports same-parent scoped counts, composite distinct grain, UTC-date
half-open windows, compatible scoped/window operands and exact count ratios. Ratios
use bounded decimal cross-products; no floating division or zero-denominator value.
Current child/root ceilings precede counts; incomplete histories, unknown relevant
properties/predicates and unavailable ratios preserve three-valued membership.

Impact: compatible additive execution/Semantic capability; no existing provider API,
generated editor schema, persistence or calendar change. No migration/production work.
The first temporal capability is explicit UTC date fields with midnight boundaries;
intraday and relative/calendar windows are not inferred. Financial metric operands,
genuine provider/HTTP/editor/Save mounting and remaining C04/C05–C11 follow.

[Verification](verification.md), [review](review.md), [owned manifest](manifest.json).
The [journal](../../../ledgers/MS-020.md) alone owns acceptance.
