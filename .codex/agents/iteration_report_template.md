---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.8.2-draft
ticket_id: <WORKSTREAM-VERB-NOUN>
proof_boundary: <exact-observed-boundary>
proof_skills: [<skills used at the declared proof boundary>]
verdict: passed | superseded
redaction: <what was removed or why no sensitive data was present>
executed_checks: [<exact command or action>]
observations: [<redacted observed result>]
---

# <Ticket> Evidence

> Compact evidence for one terminal ticket. It is not another execution-state
> source or a replacement for the product specification.

## Outcome and scope

- outcome: <what is now observably true, or why the ticket was superseded>;
- requirement IDs: [<IDs>];
- included: <behavior/paths>;
- exclusions: <what this evidence does not prove>.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
|---|---|---|
| `<exact check>` | pass / fail / superseded | <observed fact or repository path> |

## Verdict

<`passed` for an accepted ticket; `superseded` with the replacement/reason for a
superseded ticket. State residual risk and next safe action if any.>
