# Repository Agent Instructions

This file exists for standard `AGENTS.md` discovery.

The normative repository engineering contract is [`.codex/AGENTS.md`](./.codex/AGENTS.md).

For every task in this repository:

1. read this file and `.codex/AGENTS.md` before task actions;
2. use relevant IDs in `custometry-technical-blueprint-ru.md` when product requirements are affected; it remains the normative product specification;
3. read their explanation in `custometry-technical-blueprint-human-ru.md` when those requirements are in scope; skip unrelated blueprint reading for settled trivial repairs;
4. use `custometry-ui-blueprint-ru.md` for UI requirements and current inventory, `docs/architecture/ui/target-pilot/README.md` for the accepted target UI concept, and ADR-0007 for frontend architecture;
5. resolve the selected execution route: a ready ticket for an independent unit, or the accepted milestone plan and its canonical stage ledger for milestone execution;
6. follow the required hierarchical planning and documentation maintenance rules below.

## Required hierarchical planning and documentation maintenance

Use the accepted [planning framework](docs/architecture/planning/framework-v1/README.md)
for development planning: project map -> direction -> workstream -> milestone ->
stage prompt. Apply its templates, required fields, versions and owner checkpoints.
The owner participates at each selected decomposition level and decides agent
organization. Milestones use an accepted plan, prompt pack and one iteration journal;
independent bounded tickets and tiny repairs retain their declared execution route.

Document links and their maintenance are mandatory. In the same authorized unit,
update reciprocal parent/child links, affected dependencies, source/decision versions,
plan/pack/journal bindings, evidence and relevant documentation/indexes. Agents must
perform this work proactively without waiting for an owner reminder. Follow the
framework's synchronization checklist; stale or missing required links/documentation
prevent the affected completion claim. Do not invent acceptance or mutate a claimed
ledger outside the runner's exclusive update mechanism.

Repository-authored engineering artifacts are written in English by default:
architecture, ADRs, contracts, specifications, tickets, evidence reports,
runbooks, templates, code comments, and contributor documentation. The
normative `*-ru.md` product blueprints and localized `docs-site/docs/ru/**`
content are explicit product-language exceptions.

The architecture and governance index is [`docs/architecture/README.md`](./docs/architecture/README.md). Before handing off a repository change, run the smallest applicable tools from [`docs/architecture/tooling-gates.md`](./docs/architecture/tooling-gates.md); the default grouped local gate is:

```bash
uv run python -m tools.check --scope local
```

`ci` and `release` are stronger proof profiles; report the actual profile and its observed boundary.

If `.codex/AGENTS.md` cannot be read, follow the platform/global instructions and report the limitation before changing files.
