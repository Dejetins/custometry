# Repository Agent Instructions

This file exists for standard `AGENTS.md` discovery.

The normative repository engineering contract is [`.codex/AGENTS.md`](./.codex/AGENTS.md).

For every task in this repository:

1. read this file and `.codex/AGENTS.md` before task actions;
2. treat `custometry-technical-blueprint-ru.md` as the normative product specification;
3. use `custometry-technical-blueprint-human-ru.md` as its required explanatory mirror;
4. for staged work, read the linked `plan_doc`, `prompt_pack_dir`, and `stage_ledger` and take current-stage truth only from the ledger;
5. do not load `.codex/PLANS.md` for an ordinary bounded task unless long-horizon state is relevant.

Repository-authored engineering artifacts are written in English by default:
architecture, ADRs, contracts, plans, prompts, ledgers, iteration reports,
runbooks, templates, code comments, and contributor documentation. The
normative `*-ru.md` product blueprints and localized `docs-site/docs/ru/**`
content are explicit product-language exceptions. Unless the user asks
otherwise for the current task, only the final user-facing completion report is
written in Russian.

The architecture and governance index is [`docs/architecture/README.md`](./docs/architecture/README.md). Before handing off a repository change, run the smallest applicable tools from [`docs/architecture/tooling-gates.md`](./docs/architecture/tooling-gates.md); the default grouped local gate is:

```bash
uv run python -m tools.check --scope local
```

`ci` and `release` are stronger proof profiles. Do not use a green `local` result to claim runtime, browser, recovery, performance, supply-chain or release readiness.

If `.codex/AGENTS.md` cannot be read, follow the platform/global instructions and report the limitation before changing files.
