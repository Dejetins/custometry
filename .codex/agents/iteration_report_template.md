---
report_name: YYYY-MM-DD-<bounded-topic>
report_type: standalone_iteration
spec_version: 0.8.2-draft
requirement_ids: []
base_revision: <git-sha-or-unborn>
scope: "<bounded non-staged task>"
status: completed | partial | blocked
proof_boundary:
  label: <exact-observed-boundary>
  exclusions: [<what-this-report-does-not-prove>]
---

# <Iteration title>

> This is evidence for one bounded non-staged task. It is not a plan, prompt pack, stage ledger, or replacement for the blueprint.

## Outcome

<What is now observably true.>

## Scope and requirements

- requirement IDs: `<IDs or N/A>`;
- included: <paths/behavior>;
- excluded: <paths/behavior>.

## Verified facts, assumptions, unknowns

- fact: <source/evidence>;
- assumption: <bounded assumption>;
- unknown: <missing evidence or none>.

## Contract impact

| Surface | Old | New | Consumers/evidence | Classification | Migration/rollback | Verification | Unknowns |
|---|---|---|---|---|---|---|---|
| Public API / errors | TBD | TBD | TBD | `unknown` | TBD | TBD | TBD |
| Ports / interfaces | TBD | TBD | TBD | `unknown` | TBD | TBD | TBD |
| DTO / event / artifact schemas | TBD | TBD | TBD | `unknown` | TBD | TBD | TBD |
| Persistence / migrations | TBD | TBD | TBD | `unknown` | TBD | TBD | TBD |
| Config / defaults / feature policies | TBD | TBD | TBD | `unknown` | TBD | TBD | TBD |
| Request hash / cache / identity / idempotency | TBD | TBD | TBD | `unknown` | TBD | TBD | TBD |
| Service auth / timeout / retry / errors | TBD | TBD | TBD | `unknown` | TBD | TBD | TBD |
| External effects / unknown-state reconciliation | TBD | TBD | TBD | `unknown` | TBD | TBD | TBD |
| Logs / metrics / traces / audit / ledger / redaction | TBD | TBD | TBD | `unknown` | TBD | TBD | TBD |
| Alerts / runbooks | TBD | TBD | TBD | `unknown` | TBD | TBD | TBD |
| Browser-visible behavior | TBD | TBD | TBD | `unknown` | TBD | TBD | TBD |
| Benchmark / rollout gates | TBD | TBD | TBD | `unknown` | TBD | TBD | TBD |

## File manifest

- created: []
- modified: []
- deleted: []
- outside expected paths: []
- foreign changes excluded: []
- mixed files/hunks: []

## Verification

| Boundary | Command/action | Result | Evidence | Does not prove |
|---|---|---|---|---|
| Local | TBD | TBD | TBD | TBD |

- proof boundary: `<exact label>`;
- explicit exclusions: `<what remains unverified>`.

## Decisions and deviations

- decision: <none or explicit record>;
- `SHOULD` deviation/ADR: <none or path>.

## Blockers and residual risks

- blockers: none;
- residual risks: <none or explicit risk>.

## Next action

<One bounded action; do not infer authorization.>
