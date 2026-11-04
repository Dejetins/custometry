# MS-015-S01 result

Requirement boundary: COMPARE-002/005/011 and FILTER-004/017 compatibility; bounded
month-based zone provider. Whole C04 and C05–C11 remain required work.

Semantic v2 calendars pin IANA TZif bytes/hash/package version while v1 UTC calendars
remain unchanged. Public inputs cannot supply rules; atomic CAS and actor-bound replay
retain their prior semantics. Replay occurs before rule resolution. Analytics groups
aware receipt instants by pinned local dates, validates midnight boundaries, records
actual elapsed seconds, and conservatively intersects UTC source completeness.
Current company default updates do not repin old blocks. Explicit block adoption is
an ordinary scoped calendar reference and respects ancestor locks. UI shows zone,
UTC boundaries, elapsed hours and source-coverage limitations.

Impact: additive v2 input/profile and non-UTC context readers; old readers reject v2.
No database migration, backfill, deployment or retained-runtime mutation. The exact
locked tzdata version is now a direct API dependency. Reader-before-writer rollout;
rollback preserves v2 payloads for compatible readers rather than stripping fields.

[Verification](verification.md), [independent review](review.md) and
[baseline-relative owned paths](manifest.json) provide the acceptance evidence.
Canonical state belongs only to the [journal](../../../ledgers/MS-015.md).
Next: continue remaining C04 providers and C05–C11 under existing owner authority.
