# MS-008-S01 — strict scope foundation

Status: technically complete within pure S01 scope; canonical acceptance belongs
to the journal. Whole C04 and mounted S02 behavior are not complete.

## Result and owned paths

Added `packages/contracts/semantic/store_filters.py`, Presentation `scopes.py`
contracts and domain resolver, Analytics `application/store_scopes.py`, and
`tests/contract/presentation/test_composer_scopes.py`. Existing composer payloads
and API readers/writers are unchanged. Foreign checkout changes remain untouched.

The standalone versioned envelope resolves document/chapter/page/section/block
inputs, including nested sections, stable filter ordering, explicit replaceable
ancestor bindings, locks, origins and acyclic direct linked targets. Context fields
inherit independently. Store-set AND/OR/NOT is losslessly reduced only within the
provider-authorized dimension universe; mandatory source constraints remain outside
the expression. Every branch validates values. Dataset versions are pinned and
checked by both resolver and adapter. No business-row evaluator was introduced.

| Criterion | Observation |
|---|---|
| AC-01 | Closed versioned DTOs, unique IDs/order/targets, strict references, complete hierarchy/link DAG validation, unsupported AST rejection |
| AC-02 | Deterministic ancestry/linked order, provenance, locked/nonreplaceable constraint rejection, semantic dataset pin, empty/complement behavior and canonical dependency hash |
| AC-06 | 22 new tests; full Presentation135 passed0.65s; strict Pyright/Ruff/local profile passed; independent review and documentation synchronized |

[Verification](verification.md) records actual outcomes and repairs;
[independent review](review.md) has no remaining material findings. Contract impact:
new standalone public schemas **compatible-change**; existing API/persistence/cache
**none** in S01. S02 must establish compatibility for mounted scope admission and
new normalized identity. Empty-scope resolver output preserves exact legacy query.

Analytical-authoring contract is v21, with bound v20 preserved in preparation evidence.
WS-004 v0.2.3 and architecture/contributor indexes bind this milestone. No UI inventory
claim is added for unmounted behavior. Full FILTER registry/relationship/evaluator,
windows/populations and unsupported comparisons remain explicit C04 blockers.

## S02 handoff

Mount optional scope metadata with omitted-field preservation; resolve trusted
constraints and effective queries through public ports before Apply/Save/read;
carry server-derived dependency hash into real Analytics request/result identity.
Integrate author controls and supported pair/temporal comparison, current permission
and stale-response checks, scope-aware copy/move/delete/history, then prove real
API/browser Save/reopen and C02/C03 regressions in isolated infrastructure. Never
trust client claims of capabilities, policy, digest or locked eligibility. S02 is
permitted by existing owner continuation after actual successor preflight.
