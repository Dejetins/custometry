# MS-011-S01 — mounted retail filter authoring

The composer now persists `receipt-filter/v1` inputs and applies them to genuine
published Receipt data through the current Identity/Semantic/Artifact provider and
isolated DuckDB. Catalog search, bounded facets and exact preview use current
access; preview never exposes membership IDs. The editor separates draft and
applied state, supports nested Boolean groups, Reset/Undo, and blocks builder commit
while Apply is pending. Saved chart/table results pin filter and policy identity.

[Verification](verification.md), [independent review](review.md) and the
[baseline-relative owned manifest](manifest.json) define the proof and change scope.
The canonical journal alone records acceptance. Historical MS-005–MS-010 receipts,
user data and unaffected baseline changes remain intact. Modified existing files
contain prior work; only the described additions belong to this stage.

## Contract impacts

HTTP/catalog/query inputs and composer persistence are additive for new clients.
New readers accept old bytes and preserve absent-filter values/identity; old readers
reject new fields rather than weaken them. Over-budget composer Store discovery now
rejects before decoding (`breaking-change` for previously unbounded oversized
inputs), an intentional implementation of admission policy. Ordinary admitted
inputs keep their previous semantics. New config bounds are local safety limits,
not production SLOs or proof of general workspace-policy management. No DB schema
or migration change. PostgreSQL remains control truth; DuckDB evaluates filters,
Arrow projects membership, and existing analytics computes metric values.

Security fix found in review: move resource checks before all full data loading,
including the initial Store permission universe. UI race fix: pending Apply and
server validation disable commit/mutation until the resolved input is available.

Requirements contributed: FILTER-001–012 and FILTER-016–018, only the declared
published Receipt flat subset. Full C04 and C05–C11 are still obligations. Continue
with typed hierarchy integration and remaining comparison/provider capabilities
under the existing owner delegation; milestone completion is not task completion.

Final browser verification: six real-provider scenarios passed after repairing a
builder readiness race (advance was possible before metric context loaded). Required
input readiness now gates navigation/commit. Backend 158 tests, frontend 18 tests,
type checks and local profile pass. The manifest excludes this evidence directory
and the canonical ledger, whose transitions are separately hash-bound by the updater.
