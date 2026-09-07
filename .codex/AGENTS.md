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
   `delivery-orchestrator`; then read the selected ticket or accepted milestone plan/journal
   and its declared context. A trivial explicit repair may execute directly. Create a platform
   Goal only when the user or platform explicitly authorizes it.

For Web UI work, preserve the requirements and current inventory in
`custometry-ui-blueprint-ru.md` and the product blueprints. The final interactive
pilot in `docs/architecture/ui/target-pilot/` is the accepted target UI concept:
its shown composition, navigation, analytical interactions, and visual language
are authority, not merely inspiration. ADR-0007 owns frontend technology.
Existing production code is current-state evidence; it is not automatically
conformant with the pilot. Complete product coverage remains the goal, with
bounded implementation units under the selected ticket or milestone route for remaining gaps.

The owner authorized removal of the G0-G6 program and its generated materials
on 2026-09-04. Their historical record remains in Git, as explained in
`docs/architecture/ui/ui-program-retirement.md`. Do not restore a G-stage
workflow, family boards, certification receipts, or the retired program's prompt-pack/ledger route.
The previous Linear/Penpot direction and W19-W23, W29/W30 execution routes
remain retired or superseded. Historical evidence never makes them executable.

Live Figma inspection, mutation, creation, and design-to-code are not active
Custometry routes and must not be installed or suggested. A supplied Figma
export or screenshot is ordinary native-image evidence; request an export when
the only source is a live target. Historical Figma references, if encountered,
are evidence only and never execution authority.

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
Use the repository `tools.custometry_quality.stage_ledger` CLI described in
[tooling gates](../docs/architecture/tooling-gates.md#7-stage-journal-transactions)
for exclusive claim, pause, resume and receipt-backed completion. The supported
scope is one canonical journal in a local POSIX Git checkout; separate checkouts
are not a shared concurrent execution target. `validate_prompt_packs` is the
portable read-only gate; a structural pass alone does not execute a stage.
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
- Keep work inside the selected ticket or milestone-stage scope; preserve foreign worktree changes; do not
  publish, deploy, use secrets, or perform external/irreversible work without
  explicit authority.
- Evidence must match the changed boundary. Source tests do not prove database,
  browser, Compose, recovery, performance, or release behavior.

## Local routing and verification

The global skill router selects technical skills. Custometry-specific routes:

| Trigger | Primary skill |
|---|---|
| Reusable procedure prompt or explicitly justified prompt pack | `prompt-manager` after `delivery-orchestrator` |
| Product-wide Web UI coverage | Use the hierarchical planning framework with the owner to scope the selected milestone or independent-ticket route against existing requirements, target pilot and surface inventory; do not recreate the retired G0-G6 program |
| Current Custometry Web implementation | Execute the selected ready ticket or ledger-allowed milestone stage, using the active implementation-source contract and boundary-matched browser proof |
| Faithful local Product Design prototype | `product-design:image-to-code` for an inspectable image/export or `product-design:url-to-code` for an authorized live URL; do not substitute these for ordinary ticket-governed production implementation |
| UX/product-flow critique | `product-design:audit`; keep its verdict separate from fidelity and runtime readiness |
| Source-to-prototype fidelity | `product-design:design-qa`; normalize source and implementation viewport/state and keep runtime readiness with `browser-qa-evidence` |
| Browser-depth ticket | `browser-qa-evidence`; declare it in `validation.proof_skills`, and add `playwright-cli` when terminal automation is needed |

Load a `better-*` craft skill only when the ticket decision, changed surface,
observed defect, or required proof materially crosses that domain. Do not load
the whole craft set merely because a screen contains text, spacing, color, and
controls. Mixed UX, fidelity, and runtime work may reuse one safe browser
mechanic and redacted evidence set, but each skill returns its own verdict.
The user's selected Browser, Chrome, or `playwright-cli` mechanic wins.
Current Web work follows
[`docs/architecture/ui/custometry-web-implementation-source-contract-v1.md`](../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md)
and the selected ready ticket or accepted milestone plan and ledger-allowed stage.

The initial brief and later corrections remain the authority for desired
product meaning. Repository sources constrain current-state compatibility but
must not silently downgrade the accepted pilot to a visual-only reference.
Ask the owner only about material, non-derivable product or design changes;
routine implementation and boundary-matched proof do not need repeated
program-stage acceptance.

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
