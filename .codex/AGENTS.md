# Custometry Delivery Adapter

This repository adopts Global Delivery Contract v1 at
`/Users/daniildegtyarev/.codex/skills/delivery-orchestrator/references/delivery-contract-v1.md`.
The global contract chooses artifacts; global AGENTS.md owns authority. This adapter
defines only Custometry sources of truth, representation, proof, and safety.

## Local sources of authority

Within the inherited instruction order, Custometry product and engineering
sources are the normative machine blueprint, accepted architecture/ADRs, then
the selected ready ticket or accepted milestone plan/journal and their declared sources. Compare implementation/tests against
those sources. Preserve blueprint MUST/SHOULD/MAY modality when translating
requirements into role outputs; cite stable IDs. Root `AGENTS.md` owns
repository artifact-language conventions.

## Start and local sources

When starting work depends on an external or volatile input, identify the exact
target from the request or ticket and check its availability with a bounded
read-only call. If unavailable, report that input gap and continue independent
work. Skip this check for tasks that do not depend on such an input.

1. Read root `AGENTS.md`, this adapter, and the user request.
2. When product requirements or architecture are affected, read the relevant IDs
   in `custometry-technical-blueprint-ru.md`, their explanation in the human mirror,
   and the smallest affected architecture source. A trivial text or instruction
   repair with settled scope does not require unrelated blueprint reading.
3. Use `docs/architecture/README.md` for architecture navigation and
   `docs/architecture/tooling-gates.md` for local commands.
4. After delivery classification, read the selected ticket or accepted milestone
   plan/journal and its declared context. `delivery-orchestrator` supplies the global artifact-selection procedure.

For Web UI work, use `custometry-ui-blueprint-ru.md` for requirements and inventory,
[the preserved target pilot](../docs/architecture/ui/target-pilot/README.md) for its
accepted demonstrated composition, interactions and visual language, and ADR-0007
for frontend architecture. Production code is current-state evidence; verify
conformance at the changed boundary using the
[Web implementation source contract](../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md).

The previous G0-G6 and W19-W23/W29/W30 execution routes remain retired. Their
removal is recorded in [the retirement record](../docs/architecture/ui/ui-program-retirement.md).
Do not revive them through the new milestone framework. Live Figma and Penpot
are not active routes; use the inherited global source/skill restrictions.

## Hierarchical planning and execution

The owner adopted the [planning framework](../docs/architecture/planning/framework-v1/README.md)
on 2026-09-06. This is the required planning form across development directions:
project map -> direction -> workstream -> milestone -> stage prompt. Use its
per-level templates, stable IDs, exact-version links, current-state evidence,
mandatory decisions and owner review before detailing each selected branch.
Agent assignment and parallel execution remain the owner's decisions.

This owner-selected topology justifies milestone plans and packs under Global
Delivery Contract v1. Route accepted milestone authoring through `prompt-manager`
and execution through `staged-plan-runner`, with exactly one allowed stage unless
explicit Goal authority permits continuation. The milestone's plan, prompt pack
and iteration journal form the canonical triad; the journal alone owns stage state.
Do not create a ticket that duplicates that same unit's mutable execution state.
Existing independent tickets and explicit tiny repairs keep their selected route.
No retired G0-G6 pack, board, certification or ledger is reactivated.

Documentation maintenance is mandatory and included in the authorized unit.
Without waiting for an owner reminder, maintain reciprocal parent/child links,
provider/consumer references, required versions and approval evidence, triad bindings,
iteration evidence, affected canonical docs and navigation/generated indexes.
Apply the framework's synchronization checklist and record checks at handoff.
A required update left unresolved prevents the affected completion/readiness claim;
identify its concrete authority/input blocker and continue independent work.
Material decisions remain with the owner; routine link/index bookkeeping is delegated.

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
  Hierarchical plans and milestone packs use the accepted framework and current
  user authority. Keep one execution-state source per unit; no duplicate status
  register or generated prompt-pack inventory is maintained.
- Planning documents live under `docs/architecture/planning/`; milestone journals
  under `.codex/delivery/ledgers/`; prompts under `.codex/agents/generated/`.
  Follow the framework's exact storage and validation rules.

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

## Local routing and verification

Use the global Skill Routing table. For a Custometry browser-depth unit,
use `browser-qa-evidence` through the selected ticket or stage proof contract;
the selected browser mechanic follows the shared browser contract.

Role TOMLs select expertise boundaries and handoffs; they do not create
authority or repeat product specifications. Before a grouped profile outside a
hook/CI, source `scripts/activate-toolchain.sh`; then run the smallest relevant
profile from `docs/architecture/tooling-gates.md`.

## Durable output

Repository delivery artifacts are specs, tickets, justified coordination
artifacts, ADRs, contracts and redacted evidence. Exclude transcripts, sessions
and temporary runtime data. Add requirement IDs and contract impact to
non-trivial reports.
