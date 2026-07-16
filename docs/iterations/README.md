# Iteration journals

This directory is reserved for self-contained, bounded reports that do not belong to a staged architecture plan.

`docs/iterations/**` contains contributor/internal evidence. These files are not included in the standard product `/docs`, `/help`, or installation artifact.

For staged work, the execution journal is the plan-local `stage_ledger`:

```text
docs/architecture/<area>/<plan-slug>-stage-reports/<plan-slug>-stage-ledger.md
```

It is linked to the `plan_doc` and `.codex/agents/generated/<plan-slug>/`. Do not create a parallel journal, `GOAL.md`, or raw transcript as a fourth source of truth.

Standalone reports use the name `YYYY-MM-DD-<bounded-topic>.md`. They must contain scope, requirement IDs, a file manifest, actual checks, contract classification, blockers, residual risks, and the next step. Runtime logs, secrets, cookies, and raw provider payloads must not be stored here.
