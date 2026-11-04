# MS-014-S01 — explicit previous-year policies

The current UTC/month-based retail provider now resolves and renders all five
explicit previous-year modes: same dates, full calendar buckets, ISO weeks, fiscal
periods and comparable elapsed dates. Applicable policies are explicit; unknown
calendar maps fail preflight instead of inventing a leap/ISO53 fallback. Exact mapped
and excluded dates, raw paired values, coverage and immutable identities survive
save/reopen. Full bucket mode retains leap-month length; merged leap dates count the
baseline once even across a weekly boundary. Empty mapping stays unavailable.

Legacy alignment and frozen actual MS-013 previous/custom/none inputs, values and
hashes are preserved. New optional fields are omitted for prior modes; the actual
older settings reader rejects new modes explicitly. Both-period access, mandatory
metric rules and pinned dataset/filter/calendar/metric identity remain unchanged.

The editor distinguishes explicit versus inherited comparison/calendar basis, applies
explicit choices at block context, and preserves old base/context on unrelated edits.
Persisted ancestor locks remain server-enforced. Mapped details, table and chart use
the server artifact; no browser recomputation or silent definition rebase was added.

Contract impact is compatible-change for current readers, with old-reader rejection
of new modes/fields and reader-before-writer rollout. No database migration, new
service, external write, publication, deployment or production delivery was performed.
Exact owned baseline-relative paths are in manifest.json; historical receipts and
retained user data/runtime are preserved.

[Verification](verification.md) and [review](review.md) bound the evidence. The canonical
journal alone owns acceptance. This contributes COMPARE-001–011/013 only for the
mounted provider. Other calendar/timezone/DST profiles, relational/population providers,
full C04 and C05–C11 remain required. The six-block saved-read timeout observation
also remains a C10 investigation input, not a performance acceptance claim.
