# Iteration journals

This directory is reserved for self-contained, bounded historical or audit
reports that are not terminal ticket evidence.

`docs/iterations/**` contains contributor/internal evidence. These files are not included in the standard product `/docs`, `/help`, or installation artifact.

For current delivery work, the ticket under `.codex/delivery/tickets/` owns
execution state and links its evidence. Do not create a standing plan registry,
generated prompt inventory, `GOAL.md`, or raw transcript as another source of
truth.

Standalone reports use the name `YYYY-MM-DD-<bounded-topic>.md`. They must contain scope, requirement IDs, a file manifest, actual checks, contract classification, blockers, residual risks, and the next step. Runtime logs, secrets, cookies, and raw provider payloads must not be stored here.
