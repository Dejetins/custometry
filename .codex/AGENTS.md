---
doc: agents
schema_version: agents-md/v1
version: "1.0"
status: active
language: en
user_report_language: ru
user_report_language_policy: always
scope: project
role: project_delivery_adapter
delivery_contract: /Users/daniildegtyarev/.codex/skills/delivery-orchestrator/references/delivery-contract-v1.md
prompt_pack_contract: /Users/daniildegtyarev/.codex/skills/prompt-manager/references/prompt-pack-artifacts-v1.md
---

# Custometry Delivery Adapter

## Source Order

Follow platform instructions, current user authority, root `AGENTS.md`, this
adapter, `custometry-technical-blueprint-ru.md`, accepted architecture and ADRs,
the ready ticket and its declared sources, then implementation and tests. Use
`custometry-technical-blueprint-human-ru.md` as the required explanatory mirror
and stop on material conflict in favor of the higher-priority source.

This adapter narrows the global router for Custometry. It defines project
sources, representation, commands, proof, and safety; it does not create
delivery or publication authority.

## Delivery Contract

Custometry adopts Global Delivery Contract v1 through `delivery_contract` in
front matter. Use it for non-trivial or authority-unclear work, then read only
the selected specification, ticket, plan, and declared context. A specification
exists only when behavior or its proof seam is unresolved. Plans, ledgers, and
reusable prompt packs are exceptional and exist only when the global contract
or user explicitly selects them.

Preserve modular-monolith-first direction, PostgreSQL state truth, Valkey's
cache/delivery role, immutable artifacts, transactional outbox, workspace
isolation, local-first topology, and a locale-neutral core. `apps/*` compose;
`packages/*` own domain/application contracts and ports; adapters implement
ports. Domain/application code must not import framework, SQL-driver, or
filesystem implementations or read another bounded context's private tables.

## Execution Units

| situation | execution unit | authoritative artifact |
|---|---|---|
| Behavior and proof are settled | One ready ticket | `.codex/delivery/tickets/` using `.codex/agents/ticket_template.md` |
| Behavior or proof seam is unresolved | One specification slice | `.codex/delivery/specs/` using `.codex/agents/spec_template.md` |
| Several dependent slices need a frontier | One ready ticket at a time | `.codex/delivery/graphs/` records topology and path ownership; ticket front matter owns status |
| An exceptional current prompt pack is authorized | One ledger-allowed stage | The linked `plan_doc`, `prompt_pack_dir`, and `stage_ledger` |
| Tiny explicit repair has settled scope and proof | Direct repair | Current user request plus repository contracts |

Tickets declare `delivery_contract: global/v1`, map `requirement_ids` to the
normative blueprint, use `Bxx`/`Wxx` workstream IDs, and record terminal proof
with `.codex/agents/iteration_report_template.md`. Custometry keeps no standing
program plan, parallel status register, or generated prompt-pack inventory.

## Skill Routing

The global table remains the default. These rows narrow Custometry behavior.

| trigger | route | use_when | do_not_use_when |
|---|---|---|---|
| Artifact choice or unclear execution authority | `delivery-orchestrator` | Delivery topology is non-trivial or no ready ticket settles the work | A tiny explicit repair already has bounded paths and proof |
| DDD or cross-context design | `architecture-design` | A bounded context, ports/adapters, ADR, dependency, or rollout is unresolved; read `docs/architecture/bounded-context-map.md` before cross-context writes | Reviewing an accepted design without changing it |
| Product-wide Custometry UI program or all-screen atlas | `ui-design-program`; add interface-craft and browser skills only at their gated evidence stages | The request authorizes complete route/overlay/system-surface coverage, information architecture, journeys/states, families/waves, scaling from an accepted HTML pilot, exact screen contracts, responsive-Web anchors, or owner review gates | A component catalog, one settled route or component, production implementation, historical design-tool work, or execution of an active prompt-pack triad |
| Reusable prompt or exceptional prompt pack | `prompt-manager` | The global router selected a reusable staged artifact | Routine ticket execution or an unaccepted plan |
| Current staged workflow | `staged-plan-runner` | A current source selects a consistent prompt-pack triad and allowed stage | A pack is merely present, historical, or inconsistent |
| Compatibility-sensitive ticket | `contract-impact-analysis` | API, port, DTO/schema, persistence, config, identity/cache, browser default, migration, or rollback may change | The ticket proves no relied-upon contract is touched |
| Backend gates | `backend-quality-gates` | Package/app checks or failing local Python gates need triage; use the smallest profile in `docs/architecture/tooling-gates.md` | A green local gate would be used as database, browser, Compose, recovery, or release proof |
| Interface craft for an authorized current surface | Use only the crossed domain skills from `better-accessibility`, `better-layout`, `better-writing`, `better-typography`, `better-colors`, or `better-ui`; combine them only when the review actually crosses several domains | A ready ticket or selected specification asks to review or implement interface craft, accessibility, layout, copy, typography, color, visual polish, icons, or motion within the current Custometry UI contract | Overriding the normative product/UI blueprints, selecting historical Penpot, mutating a design target without exact authority, or claiming browser/runtime proof |
| HTML-first UI foundation or component catalog | `better-ui`; add only the crossed craft skill and `browser-qa-evidence` when real-browser proof is required | A current ticket authorizes reusable React/HTML components, CSS tokens, catalog states, screen manifests, or browser-accepted compositions | Product-policy decisions, backend semantics, or claims beyond the observed browser boundary |
| Screenshot-led UX audit | `product-design:audit`; add `ui-ux-pro-max` only for unresolved design direction | The ticket asks for a captured-flow critique | Browser runtime proof or mutation of the accepted HTML source |
| Browser-depth ticket | `browser-qa-evidence`; add `playwright-cli` for terminal automation | `validation.proof_skills` names browser proof | Static-only work or design-source inspection; `playwright` is a legacy-artifact alias |
| Readiness or production-risk review | `pre-ship-gate` or `production-risk-review` | The ticket asks for the corresponding review boundary | Publishing or deploying; `publish-ci-deploy` is not a Custometry route |

## Project Sources

| path | authority / use |
|---|---|
| `custometry-technical-blueprint-ru.md` | Normative machine product specification and requirement IDs |
| `custometry-technical-blueprint-human-ru.md` | Required explanatory mirror |
| `custometry-ui-blueprint-ru.md` | UI/UX requirement source |
| `packages/contracts/routes/ui-routes.json` | Current stable route identities for all-screen reconciliation |
| `packages/contracts/routes/ui-route-contracts.json` | Route roles, permissions, states, profiles, and source traceability |
| `packages/contracts/routes/ui-surface-contracts.json` | Overlay, system-surface, cross-surface capability, and use-case coverage |
| `docs/architecture/ui/custometry-contract-compiled-ui-prototyping-plan-v1.md` | Accepted HTML-first mechanics, reuse direction, and pilot acceptance boundary |
| `docs/architecture/ui/custometry-linear-ui-migration-registry-v1.json` | Current transition status and exact linked UI sources |
| `docs/architecture/README.md` | Architecture navigation |
| `docs/architecture/tooling-gates.md` | Local command and proof profiles |
| `docs/architecture/bounded-context-map.md` | Required before adding cross-context dependencies |
| `.codex/agents/spec_template.md` | Specification shape |
| `.codex/agents/ticket_template.md` | Ticket shape and status contract |
| `.codex/agents/iteration_report_template.md` | Redacted terminal ticket evidence shape |

For product-wide Custometry UI planning, compile the complete atlas from the
normative UI blueprint plus the route, route-contract, and surface-contract
registries. The blueprint's statement that a global all-route catalog is not a
prerequisite means that every route need not be visually designed or added to
a component catalog before slice work; it does not waive the complete
screen-atlas and coverage control plane. Historical inventories and the
accepted HTML pilot provide only their declared route/family evidence.
Mobile-specific composition remains unauthorized without exact current user
authorization; narrow responsive Web is not permission to invent a mobile UI.

For authenticated Web transition work, also read
`docs/architecture/ui/linear-workspace-ui-transition-standard-v1.md`, the
selected Custometry specification under `.codex/delivery/specs/`, and the
applicable node in
`.codex/delivery/graphs/custometry-linear-workspace-ui-transition-v1.json`.
W10 is historical Penpot identity/domain evidence; W18 is superseded and must
not execute. Browser runtime requires separate evidence.

## Prompt Pack And Ledger Contract

An exceptional current prompt pack must follow `prompt_pack_contract` and
cross-link `plan_doc`, `prompt_pack_dir`, `stage_ledger`, its selected ticket,
and `.codex/agents/iteration_report_template.md` evidence. No repository-local
prompt or ledger template is implied unless a current accepted artifact names
an existing path.

Use `required_keywords` for compact domain vocabulary and `required_literals`
only for exact strings. Keep pre-implementation context to the declared ticket
sources and normally no more than eight files or roughly 35k-50k tokens. Stop
reading when scope, contracts, documentation, proof boundary, and blockers are
known. Do not create `GOAL.md` unless the user explicitly asks for it.

## Safety And Evidence

- For an external or volatile first boundary, perform the smallest read-only
  identity/readiness probe after root instructions, this adapter, and the task
  envelope; it does not replace the full pre-write guard.
- Historical design-tool evidence is retained truthfully but is never an active
  UI source or execution route. Current visual work is performed through
  repository-owned HTML/React components and observed browser evidence.
- Keep work inside ticket scope and preserve foreign changes. Do not publish,
  deploy, use secrets, or perform external, irreversible, or paid work without
  explicit authority.
- Classify non-trivial API, port, DTO/schema, persistence, config,
  identity/cache, side-effect, browser, migration, rollback, and performance
  impact as `none`, `compatible-change`, `breaking-change`, or `unknown`.
- Evidence must match the changed boundary. Source tests do not prove database,
  browser, Compose, recovery, performance, or release behavior.
- Before a grouped profile outside a hook or CI, source
  `scripts/activate-toolchain.sh`, then run the smallest relevant profile from
  `docs/architecture/tooling-gates.md`.
- Validate tickets with
  `uv run python -m tools.custometry_quality.validate_delivery_tickets` and the
  portable adapter with
  `uv run python -m tools.custometry_quality.validate_delivery_contract`. A
  local audit may add `--contract <installed-path>`; CI must not depend on a
  developer-home path.
- Role TOMLs select expertise boundaries and handoffs only; they do not create
  authority or repeat product specifications.

## Output Contract

Repository-authored engineering artifacts are English. Normative `*-ru.md`
blueprints and localized product docs are exceptions. Durable output may
include specs, tickets, justified coordination artifacts, ADRs, contracts, and
redacted evidence; never persist transcripts, browser state, cookies,
credentials, environment dumps, provider payloads, sessions, or temporary
runtime data.

Non-trivial reports state requirement IDs, actual scope, contract impact,
validation and observed proof boundary, residual risk, and next safe action.
All final user-facing reports must always be written in Russian; this rule has
no language override.
