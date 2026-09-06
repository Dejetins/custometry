---
doc_id: ADR-0003
title: Agent delivery model
doc_version: 3
product_spec_version: 0.9.0-draft
visibility: internal
ship: false
owner: engineering
requirement_ids: [DOC-RULE-008]
status: accepted
proof_boundary:
  label: delivery-governance
  exclusions: [product-runtime-proof, release-readiness]
---

# ADR-0003: Custometry Adapter to Global Ticket-First Delivery

## Amendment — hierarchical planning adopted 2026-09-06

The owner accepted the [hierarchical planning framework](../architecture/planning/framework-v1/README.md)
and required mandatory document links, proactive documentation updates and project
AGENTS routing. This amendment supersedes the earlier restriction that future
planning must always be represented by tickets unless exceptional. The earlier
removal of obsolete S00-S06/G0-G6 workflows and duplicated state remains in force.

New development planning follows project map, direction, workstream and milestone
levels with owner participation at each selected decomposition. Each authorized
milestone uses one accepted plan, prompt pack and iteration journal. The journal
is its sole mutable execution-state source; independent tickets keep their own
state and history. No unit is controlled by both. The canonical pack lifecycle,
exclusive updater and real-boundary evidence requirements remain unchanged.

Agents must update affected documentation, reciprocal hierarchy/dependency links,
versions, decisions, indexes and execution evidence in the same authorized unit,
without owner reminders. The framework owns the exact checklist and templates.
Substantive owner decisions are not inferred from mechanical synchronization.

The sections below retain the earlier decision's rationale and removal history;
this amendment governs any conflicting prospective instruction in them.

## Context

The former static S00-S06 prompt-pack model duplicated execution state across
plans, prompts, ledgers, reports, and validators. It could also expose a real
defect in a proof stage while forbidding the in-scope repair needed to prove the
same accepted behavior. Global Delivery Contract v1 now defines artifact choice
and execution authority for all adapted repositories.

## Decision

Custometry adopts Global Delivery Contract v1 and supplies only its repository
adapter: blueprint requirement mapping, `Bxx`/`Wxx` ticket IDs, local spec,
ticket and evidence templates, a ticket validator, architecture entrypoints,
and proof gates. A ready vertical ticket is one execution unit and the only
repository-local source of its current execution state. A platform Goal is
optional and requires explicit user or platform authority.

An executor may repair a defect found by its own acceptance boundary when the
repair, tests, generated artifacts, and rerun all fit the ticket's declared
scope. The closed escalation list remains product change, material scope
change, external/irreversible action, secrets/production authority, and an
out-of-scope write.

The obsolete standing program plan, generated S00-S06 packs, workstream plans,
stage ledgers, their validators, and the partial B01 implementation are removed.
Git history retains provenance without keeping obsolete artifacts in the active
tree. Future plans, ledgers, or reusable procedure prompts are created only
when the global contract proves that a ticket or specification is insufficient;
they never become a permanent parallel execution system.

## Consequences

- Future work starts from the smallest justified artifact: direct execution,
  one vertical ticket, or a specification followed by tickets.
- Quality tooling validates ticket invariants plus compact, redacted terminal
  evidence records; no legacy staged validator remains in the active toolchain.
- AGENTS.md is a compact routing map; detailed truth lives in indexed docs.
- Product requirements, accepted architecture, Foundation runtime proof, and
  machine-readable requirement/route indexes remain available as the clean
  baseline for the next delivery slice.
