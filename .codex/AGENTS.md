# Custometry Delivery Adapter

This repository adopts Global Delivery Contract v1 at
`/Users/daniildegtyarev/.codex/skills/delivery-orchestrator/references/delivery-contract-v1.md`.
The global contract chooses artifacts and execution authority. This adapter
defines only Custometry sources of truth, representation, proof, and safety.

## Local authority

Precedence is platform instructions, current user authority, root `AGENTS.md`,
this adapter, the normative machine blueprint, accepted architecture/ADRs, a
ready ticket and its declared sources, then implementation and tests. Stop on
a material conflict and follow the higher source.

Repository-created engineering artifacts are English. The `*-ru.md` blueprints
and localized product docs are exceptions. Final user-facing reports are
Russian unless the user requests otherwise.

## Start and local sources

1. Read root `AGENTS.md`, this adapter, and the user request.
2. Read the relevant IDs in `custometry-technical-blueprint-ru.md`, its human
   mirror, and the smallest linked architecture document.
3. Use `docs/architecture/README.md` for architecture navigation and
   `docs/architecture/tooling-gates.md` for local commands.
4. For non-trivial or authority-unclear executable work, use
   `delivery-orchestrator`; then read only the selected ticket and its declared
   context. A trivial explicit repair may execute directly. Create a platform
   Goal only when the user or platform explicitly authorizes it.

## Custometry representation

- Specs live under `.codex/delivery/specs/` when needed and use
  `.codex/agents/spec_template.md`.
- Tickets live under `.codex/delivery/tickets/`, use
  `.codex/agents/ticket_template.md`, declare `delivery_contract: global/v1`,
  and map `requirement_ids` to the normative machine blueprint.
- Terminal ticket evidence uses `.codex/agents/iteration_report_template.md`:
  a redacted record that names the ticket, proof boundary, checks,
  observations, and verdict.
- Tickets use `Bxx`/`Wxx` workstream IDs and are checked with
  `uv run python -m tools.custometry_quality.validate_delivery_tickets`.
- `uv run python -m tools.custometry_quality.validate_delivery_contract`
  validates the portable repository adapter. A local environment audit may
  add `--contract <installed-path>` to resolve the global source and supplying
  skill; CI does not depend on a developer-home path.
- A specification is created only when behavior or its proof seam is unresolved.
  A plan, ledger, or reusable procedure prompt is exceptional and is created
  only when the global contract classifies it as necessary for the current
  delivery topology. Custometry keeps no standing program plan or generated
  prompt-pack inventory.

## Product, scope, and proof

- Preserve modular-monolith-first direction, PostgreSQL state truth, Valkey
  cache/delivery role, immutable artifacts, transactional outbox, workspace
  isolation, local-first topology, and locale-neutral core.
- `apps/*` compose; `packages/*` own domain/application contracts and ports;
  adapters implement ports. Domain/application code does not import framework,
  SQL-driver, or filesystem implementations. Do not read private context tables
  across a bounded-context boundary.
- Read `docs/architecture/bounded-context-map.md` before adding a cross-context
  dependency. Classify non-trivial API, port, DTO/schema, persistence, config,
  identity/cache, side-effect, browser, migration, rollback, and performance
  impact as `none`, `compatible-change`, `breaking-change`, or `unknown`.
- Keep work inside ticket scope; preserve foreign worktree changes; do not
  publish, deploy, use secrets, or perform external/irreversible work without
  explicit authority.
- Evidence must match the changed boundary. Source tests do not prove database,
  browser, Compose, recovery, performance, or release behavior.

## Local routing and verification

The global skill router selects technical skills. Custometry-specific routes:

| Trigger | Primary skill |
|---|---|
| Reusable procedure prompt or explicitly justified prompt pack | `prompt-manager` after `delivery-orchestrator` |
| Browser-depth ticket | `browser-qa-evidence`; declare it in `validation.proof_skills`, and add `playwright` when terminal automation is needed |

Role TOMLs select expertise boundaries and handoffs; they do not create
authority or repeat product specifications. Before a grouped profile outside a
hook/CI, source `scripts/activate-toolchain.sh`; then run the smallest relevant
profile from `docs/architecture/tooling-gates.md`.

## Durable output

Commit durable specs, tickets, justified coordination artifacts, ADRs,
contracts, and redacted evidence. Never commit transcripts, browser state,
cookies, credentials, environment dumps, provider payloads, sessions, or
temporary runtime data. Non-trivial reports state requirement IDs, actual
scope, contract impact, evidence, residual risk, and the next safe action.
