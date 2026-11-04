# MS-012-S01 — Receipt hierarchy

Published Receipt conditions can now be authored at document/chapter/page/section/
block scope, linked directly to other blocks, explicitly replaced by an allowed
same-field descendant, and locked persistently. Current permissions still intersect
outside the expression. Effective queries drive actual computation, persisted
results and the context inspector; unrelated blocks retain their result identity.
The existing editor separates draft, settings Apply and backend-validated scope commit.

`composer-scopes/v2` is additive for new readers; preserved v1 bytes and resolver
semantics remain unchanged. Old readers reject v2 rather than discard constraints.
Affected boundary classification: compatible-change for current API/readers/UI,
explicit old-reader rejection for v2; no DB migration, permission relaxation or
production/deployment claim. Pure canonical expression meaning is shared through a
contract helper rather than a cross-context infrastructure import.

Owned changes extend scope DTOs/resolution, copy/delete/query invalidation, generated
contracts and scoped editor integration; exact baseline-relative paths are in
manifest.json. Mixed existing files retain previous work. Evidence and canonical
ledger are excluded from the manifest because their immutable receipt/transaction
bindings record them separately. Historical receipts and user data are preserved.

[Verification](verification.md) and [review](review.md) describe actual proof and
repairs. The canonical journal alone owns acceptance. This closes only Receipt
hierarchy integration, not full C04. Relational/aggregate/sequence/population,
expanded temporal comparison and C05–C11 remain required work under the same authority.
