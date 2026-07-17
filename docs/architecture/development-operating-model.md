---
doc_id: ARCH-DEVELOPMENT-OPERATING-MODEL-001
title: Custometry development operating model
doc_version: 7
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: engineering
requirement_ids: [DOC-RULE-008]
status: accepted
proof_boundary:
  label: repository-development-policy
  exclusions: [github-protection-proof, ci-run-proof, product-runtime-proof]
---

# Custometry Development and Acceptance Model

## 1. Outcome-oriented development

Custometry evolves through contract-backed vertical slices. A slice starts from
an observable user or operator outcome and reaches the nearest real boundary
needed to prove it. UI-first means that the route, states, accessibility, and
user feedback are designed early; it does not permit manually invented mock
contracts or postpone domain invariants indefinitely.

Progress is not measured by the number of screens, layers, documents, stages,
or generated prompts. A slice is complete only when its declared behavior,
failure modes, documentation, compatibility disposition, and evidence agree.

## 2. Sources and artifact selection

The normative sources are:

1. `custometry-technical-blueprint-ru.md` for machine-readable product rules;
2. `custometry-technical-blueprint-human-ru.md` for the synchronized human mirror;
3. `custometry-ui-blueprint-ru.md` for UI/UX requirements;
4. accepted architecture documents and ADRs;
5. implementation, schemas, tests, and observed evidence.

Global Delivery Contract v1 selects the smallest sufficient delivery artifact:

- direct execution for a trivial, explicit, low-risk repair;
- one ready vertical ticket for one bounded observable outcome;
- a specification before tickets when behavior, invariants, failure semantics,
  or the proof seam remain materially unresolved;
- an exceptional plan, ledger, or reusable procedure only when real
  multi-ticket coordination, risky external state, approval checkpoints, or a
  genuinely repeated method requires it.

Custometry keeps no standing program plan, generated prompt-pack inventory, or
parallel stage ledger. One ready ticket is one execution unit and is the only
repository-local source of current scope, blockers, repair authority, and
acceptance evidence. Goal mode is optional runtime orchestration; it is not a
file-backed planning layer.

## 3. Ticket lifecycle

Tickets live in `.codex/delivery/tickets/` and use these states:

| State | Meaning |
|---|---|
| `draft` | The outcome or boundary is not executable yet. |
| `ready` | Scope, dependencies, commands, and proof boundary are sufficient. |
| `active` | The ticket is the current execution unit. |
| `blocked` | A specific technical condition prevents safe progress and has durable evidence. |
| `accepted` | The declared outcome is proven at its stated boundary. |
| `superseded` | Another named decision or ticket replaces the outcome. |

A blocked ticket records the technical blocker, existing evidence, and the next
safe action. It does not invent an internal approver. An executor may repair an
in-scope defect discovered by its own proof boundary and must rerun invalidated
evidence. Escalation is limited to normative product changes, material scope
changes, external or irreversible effects, secrets or production authority,
and writes outside the declared scope.

## 4. Architecture and contract rules

Custometry remains a modular monolith with ports and adapters:

- `apps/*` are composition roots;
- `packages/*` own domain and application behavior plus required ports;
- adapters implement ports and are wired at composition roots;
- domain/application code does not import framework, SQL-driver, queue, or
  filesystem implementations;
- a context does not read another context's private tables.

Before implementation, identify the relevant bounded context in
[bounded-context-map.md](./bounded-context-map.md). Classify changes to APIs,
ports, DTOs/events, persisted schemas, configuration/defaults, identities,
caches, idempotency/retry, external effects, browser behavior, migrations,
rollback, observability, and performance as `none`, `compatible-change`,
`breaking-change`, or `unknown`.

## 5. Development runtime modes

Use the smallest runtime that can prove the ticket boundary. The exact commands
and current implementation status live in
[development-runtime-contract.md](./development-runtime-contract.md).

| Mode | Purpose | Cannot prove by itself |
|---|---|---|
| `fast-loop` | Pure policies, schemas, generated clients, components, focused tests | Real persistence, image, or network behavior |
| `hybrid` | Host application code with real containerized stateful adapters | Complete shipped topology |
| `full-stack` | Disposable Compose lifecycle and real Edge/API/browser boundary | Release provenance or production hardening |
| `release` | Immutable candidate, target install/update, recovery, supply chain, and performance | A broader production rollout without explicit authority |

## 6. Evidence

Evidence follows the changed boundary:

| Surface | Minimum meaningful proof |
|---|---|
| Domain policy | Focused unit/property/invariant tests |
| Port or adapter | Contract test plus the real adapter boundary |
| API | Real request with auth/RBAC/error/DTO behavior when applicable |
| PostgreSQL | Upgrade, repeat behavior, supported rollback/downgrade, and integrity checks |
| Web | Real browser flow, console/network inspection, responsive/a11y/en/ru smoke |
| Compose | Clean start, health, restart/failure behavior, stop, and post-conditions |
| Recovery | Observed drill and integrity verification |
| Performance | Reproducible corpus/environment, baseline, threshold, and result |
| Release | CI, immutable identity/provenance, install/update, and post-start smoke |

Passing source tests never proves database, browser, Compose, recovery,
performance, supply-chain, or release behavior. Terminal ticket evidence is a
compact redacted record under `.codex/delivery/evidence/`; it does not copy raw
logs, credentials, cookies, environment dumps, or provider payloads.

## 7. Git and publication

- `main` is protected and potentially releasable.
- Product changes normally use one short-lived branch and one pull request.
- Required checks must pass; squash merge preserves linear history.
- No long-lived `develop`, per-stage branches, broad force-push, or hidden
  integration branch is used.
- Publication, merge, release, deployment, secrets, and production actions
  require explicit authority and the repository runbook.

Run the smallest focused checks first, then the applicable grouped profile from
[tooling-gates.md](./tooling-gates.md). Local green is not GitHub CI evidence;
GitHub CI is not runtime, recovery, performance, or release evidence unless the
workflow actually observes those boundaries.

## 8. Language and documentation

Repository-authored engineering artifacts are English. The normative Russian
blueprints and declared localized product documentation are explicit
exceptions. Product obligations are added to the machine blueprint first and
mirrored synchronously; architecture and tickets refer to stable requirement
IDs instead of duplicating normative prose.

Local `/docs` and `/help` remain product capabilities governed by
[documentation-platform.md](./documentation-platform.md). Contributor
architecture, tickets, and evidence are not automatically shipped to users.
