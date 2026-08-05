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

For an external or volatile target that determines whether work can begin, use
the global first-boundary probe after reading the root instructions, this
adapter, and the smallest task or ticket envelope that identifies the target.
Penpot evidence is historical only: preserve truthful references, but never
select Penpot as an active design source, mutation route, or delivery target.

1. Read root `AGENTS.md`, this adapter, and the user request.
2. Read the relevant IDs in `custometry-technical-blueprint-ru.md`, its human
   mirror, and the smallest linked architecture document.
3. Use `docs/architecture/README.md` for architecture navigation and
   `docs/architecture/tooling-gates.md` for local commands.
4. For non-trivial or authority-unclear executable work, use
   `delivery-orchestrator`; then read only the selected ticket and its declared
   context. A trivial explicit repair may execute directly. Create a platform
   Goal only when the user or platform explicitly authorizes it.

For product-wide Web UI work, use `custometry-ui-blueprint-ru.md` only as the
pre-G0 product/UI requirements and current-inventory source. The previous
Linear/Penpot target and W19-W23 route are retired. W03-W10 remain historical
evidence, and W18 remains superseded; none is current visual authority or an
execution route. Initialize `ui-design-program` only after the detailed product
path is exact and an accepted pilot or bounded pre-G0 proposal establishes the
visual authority. Current visual proof must come from the program-selected
evidence mode and real browser evidence required by the active gate.

## Custometry representation

- Specs live under `.codex/delivery/specs/` when needed and use
  `.codex/agents/spec_template.md`.
- Tickets live under `.codex/delivery/tickets/`, use
  `.codex/agents/ticket_template.md`, declare `delivery_contract: global/v1`,
  and map `requirement_ids` to the normative machine blueprint.
- Terminal ticket evidence uses `.codex/agents/iteration_report_template.md`:
  a redacted record that names the ticket, proof boundary, checks,
  observations, and verdict.
- Ticket graphs live under `.codex/delivery/graphs/` only when several
  dependent slices need one explicit ready frontier. A graph records topology
  and path ownership; ticket frontmatter remains the sole status authority.
- Tickets use `Bxx`/`Wxx` workstream IDs and are checked with
  `uv run python -m tools.custometry_quality.validate_delivery_tickets`.
- `uv run python -m tools.custometry_quality.validate_delivery_contract`
  validates the portable repository adapter. A local environment audit may
  add `--contract <installed-path>` to resolve the global source and supplying
  skill; CI does not depend on a developer-home path.
- A specification is created only when behavior or its proof seam is unresolved.
  A plan, ledger, or reusable procedure prompt is exceptional and is created
  only when the global contract classifies it as necessary for the current
  delivery topology. Custometry keeps no standing program plan, parallel
  status register, or generated prompt-pack inventory.

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
| Product-wide multi-screen Web UI program | `ui-design-program` when the user authorizes complete all-screen/journey/family/wave work rather than one ticket-local screen; use its pre-G0 intake, stage-specific read sets, exact family/wave aggregates, and HTML/browser evidence route |
| Browser-depth ticket | `browser-qa-evidence`; declare it in `validation.proof_skills`, and add `playwright-cli` when terminal automation is needed |

For an authorized UI program, the user supplies the initial detailed product
path and later reviews finished visual checkpoints. The agent owns hashes,
artifact identities, routine program-owned writes, prompt/ledger mechanics,
and technical confirmation. G1/G2 have no routine owner acceptance gate;
G3-G6 use `review_ready` before natural-language acceptance. This exception
permits the UI program's draft triad during G0 bootstrap but does not create a
standing repository-wide plan outside the authorized program paths.
The initial brief and later corrections remain the sole authority for desired
product meaning; repository sources constrain current-state compatibility but
do not silently redefine the user's intent or create repeated scope questions.

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
