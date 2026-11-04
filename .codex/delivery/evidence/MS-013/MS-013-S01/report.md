# MS-013-S01 — explicit period comparison

Composer blocks and inherited context now support actual previous/custom period
comparison through the current pinned UTC month-based provider. Results disclose
both ranges, elapsed time/date counts, overlap/duration differences, evaluated dates,
coverage, values, exact Decimal deltas and explicit unavailable reasons. There is
no hidden duration normalization or replacement of missing values with zero.

New optional versioned settings and immutable embedded artifacts preserve absent-field
legacy serialization, normalization and calculation output. Both sides use the same
current-authorized input projection, mandatory metric rules and pinned definitions.
The artifact pins request, policy, filter, dataset, metrics and calendar. Existing
result manifest/persistence protects it; no new database or migration was introduced.

The editor distinguishes inherit and explicit none/local settings. Unrelated edits
preserve old query/context precedence. Tables/charts read server paired buckets;
custom/previous modes never use a previous-year label. Existing HTTP validation,
abort/stale guards, saved locks and immutable result references remain in force.

Boundary impact: compatible-change in current optional API/contracts and UI; old
readers explicitly reject new settings rather than drop them. Reader-before-writer
rollout and preservation of new bytes are required for rollback. No permission
expansion, publication, deployment or production migration is claimed.

Owned paths and exact pre-stage hashes are in manifest.json. Prior work, receipts
and retained user data are preserved. [Verification](verification.md) and
[review](review.md) describe observed proof, test repairs and boundaries. Only the
canonical journal owns acceptance. This contributes COMPARE-001–011/013 at the
current provider boundary; other calendar/timezone/DST, population and remaining
C04/C05–C11 work continues under existing authority.
