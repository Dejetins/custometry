# Repository Agent Instructions

This file exists for standard `AGENTS.md` discovery.

The normative repository engineering contract is [`.codex/AGENTS.md`](./.codex/AGENTS.md).

Read `.codex/AGENTS.md` before task actions. It owns source selection,
project routing, execution units, proof and documentation maintenance. Use the
current checkout and selected ticket/stage; an existing file or old pack does
not select work or authorize its next stage.

## Required hierarchical planning and documentation maintenance

The accepted [planning framework](docs/architecture/planning/framework-v1/README.md)
remains mandatory for development planning. Apply the adapter's owner checkpoints,
selected execution route and proactive documentation synchronization; bounded
tickets and tiny repairs retain their declared route. Do not duplicate mutable
stage state or infer acceptance from a worker result.

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
