# MS-014 independent review

Dewey (`01a1165a-8a6a-7fb0-a915-696d7998c29f`) reviewed the new contract, resolver,
projection, UI/inheritance and pre-stage snapshots in read-only mode. Nine direct
backend tests, including four frozen prior outputs, passed during the initial review.
Snapshot SHA checks matched baseline. Browser/provider proof remained executor-owned.

P2: merge only coalesced day buckets, so Feb28/29 across a week boundary duplicated
the comparison date in weekly rows while totals deduplicated it. Added a reproducing
2016-Feb28/29 test (two rows before repair). Group assignment now preserves the one
merge group for all grains: current 10+20, baseline 5, delta25 in one weekly row and
totals. No duplicate baseline or additive inconsistency remains in this case.

P2: Calendar basis was saved in base query and could be overridden by the parent
context even after an explicit Fiscal selection. Added distinct inherit/explicit
basis with atomic local/inherited/base initialization and dirty tracking. Explicit
basis joins comparison in local context; unchanged inputs retain their original
precedence. Mounted Builder and backend resolver tests cover parent calendar -> local
fiscal plus fiscal mode, and locked parent denial; the unchanged edit test also
preserves a base fiscal setting behind a locked calendar ancestor.

Repair-only independent follow-up exercised weekly/day merge, frozen compatibility
and fiscal override/locked denial. Verdict `cleared`, no new actionable findings;
contract impact `compatible-change` within the reviewed boundary. Reviewer did not
run browsers or broad gates. This is not full milestone/workstream/production proof.
