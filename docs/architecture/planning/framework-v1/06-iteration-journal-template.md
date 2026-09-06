# Template — milestone iteration journal

> Non-executable outline under the [framework](README.md).
> One journal combines canonical stage state with readable iteration history.
> It is the triad's `stage_ledger`; do not create a separate progress ledger.

## Binding and baseline

| Item | Value |
|---|---|
| Milestone ID / accepted plan version | `<MS-id / version>` |
| Source commit or immutable snapshot | `<actual verified baseline>` |
| `plan_doc`, `prompt_pack_dir`, `stage_ledger` | `<exact triad paths>` |
| Profile / schema / validator | `<current supported profile>` |
| Execution mode and authority | `<manual_sequential and actual owner source>` |
| Exclusive claim/update capability | `<existing mechanism and current evidence, or unavailable>` |

## Canonical machine record

When instantiated with the bundled profile, use exactly one
`<!-- prompt-pack-ledger:v1 -->` marker followed immediately by a JSON fence.
The following is a field outline, not a valid ledger object. Full contract fields
come from the [stage prompt template](05-stage-prompt-template.md).

| JSON field | Initial draft value / obligation |
|---|---|
| `schema_version` | `prompt-pack-ledger/v1` |
| `prompt_pack_execution` | Exact `plan_doc`, `prompt_pack_dir`, `stage_ledger` paths |
| `execution_mode` | `manual_sequential` unless separately authorized |
| `ledger_status`, `current_stage` | `draft`, null |
| `stages` | Nonempty ordered collection of exact stage contracts and state rows |
| `claim_capability` | Omit while unresolved; required before entry-ready claims |

| Each stage row | Initial draft value / obligation |
|---|---|
| `contract` | Exact copy of its prompt's `stage_contract` |
| `status`, `execution_allowed`, `current_authority` | `pending`, false, true |
| `executor_claim`, `claimed_at`, `transition_receipt` | null, null, null |
| `decision_packet` | null or `{question, resume_condition, resolution_evidence}` |

All rows start disallowed in this conservative outline. The author may enable one
dependency-free entry after prerequisites and real authority are resolved. Unknown
owner decisions remain `pending` and disallowed, never draft `needs_input`.
Do not manufacture claim capability, execution receipts or accepted stage rows.

## Iteration history

Append one row after each meaningful attempt; a stage may have multiple iterations.
Iteration IDs are immutable and scoped to the milestone. They are not extra stages.

| Iteration ID / date | Stage + contract revision | Attempt / changed paths | Checks and actual results | Evidence reference | Deviation / unresolved work | Next action |
|---|---|---|---|---|---|---|
| `<MS-id-I001>` | `<stage>` | `<observed actions>` | `<pass/fail/unavailable/not_run>` | `<immutable report>` | `<facts>` | `<bounded action>` |

The table is an evidence history, not the current status source. Keep raw logs,
secrets, cookies, provider payloads and environment dumps outside durable records.
Short immutable reports can use the following body:

| Report field | Required content |
|---|---|
| Identity | Milestone, stage, iteration, exact source and contract revision |
| Scope | Created/modified/deleted paths, unexpected paths with reason, excluded foreign changes |
| Observations | Exact commands/actions, results and boundary-matched evidence |
| Requirement coverage | Milestone criterion IDs satisfied or still unproven |
| Deviations | Approved changes, failed attempts, blockers and unresolved questions |
| Handoff | Next required inputs, residual risks, receipt reference |

## Decisions during execution

Current blocking questions live in the relevant stage row's decision packet.
Keep a readable decision history with exact owner answer, date, affected plan/stage
version and evidence link. Reference that history from the row. An answer satisfies
only its stated question; it does not broaden scope or bypass checks.

## Lifecycle and revisions

Use the installed `staged-plan-runner/references/ledger-lifecycle-v1.md` as the
transition authority. The runner owns activation, claims and execution mutations;
the template author owns only unclaimed draft fields. State changes must use a
verified exclusive updater, not a read/write/read imitation of locking.

Preserve terminal rows, old contracts, iteration history and immutable receipts.
Hard-blocked or superseded stages need the canonical revision/replacement mapping.
Changed plan or evidence inputs require impact review before new readiness claims.
Do not reset an existing journal to `draft` or overwrite an executing prompt.

## Final acceptance stage

Its report maps every required milestone criterion to actual evidence, checks
cross-stage integration, lists residual limits and records the owner's result
decision. While that decision is required and pending, use the canonical runner
input/receipt behavior. The journal can become `completed` only after all required
obligations have satisfying outcomes. An unresolved required criterion prevents
closure; a scope reduction needs a plan amendment and owner acceptance.

## Construction and verification references

Current installed authoring sources:

- `/Users/daniildegtyarev/.codex/skills/prompt-manager/references/prompt-pack-artifacts-v1.md`
- `/Users/daniildegtyarev/.codex/skills/prompt-manager/references/artifact-validation-v1.md`
- `/Users/daniildegtyarev/.codex/skills/staged-plan-runner/references/ledger-lifecycle-v1.md`
- `/Users/daniildegtyarev/.codex/skills/prompt-manager/references/transition-receipt-v1.md`

Resolve installed paths on the execution host; these paths document this framework's
source, not portable runtime configuration. For a real bundled-profile pack use:

```sh
python3 <installed-prompt-manager>/scripts/validate_pack.py --root <authorized-root> --ledger <actual-ledger> --check draft
python3 <installed-prompt-manager>/scripts/validate_pack.py --root <authorized-root> --ledger <actual-ledger> --check entry --stage <stage-id>
```

Require exit 0 and matching JSON `status: pass`; exit 1 means failed validation,
exit 2 means unavailable/invalid invocation. The validator is read-only. These
outlines have not been instantiated and cannot be called `draft_valid` or entry-ready.

## Mandatory documentation handoff

Apply the framework's [document synchronization rules](README.md#mandatory-document-synchronization)
in this same unit: update parent/child and dependency links, affected source references,
versions, decisions, indexes and execution evidence as applicable. Do not wait for
an owner reminder. Identify any authority or unresolved-decision blocker explicitly;
do not claim completion while a required documentation update remains outstanding.
