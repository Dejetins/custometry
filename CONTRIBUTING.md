# Contributing to Custometry

Custometry is developed in a public repository. Never commit credentials, customer data, private topology, production payloads, browser state, or raw environment dumps.

## Workflow

1. Read `AGENTS.md`, `.codex/AGENTS.md`, and the requirement IDs relevant to the change.
2. Bootstrap the exact repository toolchain once, then activate it in every shell:

   ```bash
   scripts/bootstrap-toolchain.sh
   source scripts/activate-toolchain.sh
   ```

   The activation contract requires Node from `.node-version`/`.nvmrc`, pnpm from
   `package.json#packageManager`, and uv from `.uv-version`. It fails instead of
   silently using another globally active version.

3. Select the smallest sufficient development runtime:

   - `fast-loop` is partially implemented for host Web,
     framework-independent Python, and focused tests; generated contract mocks
     and the unified CLI remain target capabilities;
   - `hybrid` is the target host Web/API plus containerized stateful
     infrastructure mode and is not implemented yet;
   - `full-stack` is implemented for clean disposable Foundation Compose and
     real browser/network proof;
   - `release` is the protected immutable-artifact acceptance contract, not an
     available accepted end-user bundle or an ordinary developer loop.

   The current implementation and target commands are tracked in the
   [development runtime contract](docs/architecture/development-runtime-contract.md).
   Do not rebuild the complete stack for every source edit, and do not use a
   lower mode to claim a higher proof boundary.

4. Start a short-lived branch named `codex/<workstream>-<iteration>` or an equivalent contributor branch.
5. Keep the change bounded to one coherent outcome. Do not create a long-lived `develop` or per-context integration branch.
6. Enable the repository hooks once per checkout:

   ```bash
   git config core.hooksPath .githooks
   ```

   Hooks activate the exact repository Node, pnpm, and uv pins before running
   their quality profile. They do not inherit an incompatible ambient
   Node/pnpm selection from the shell that launched Git.

7. Run the local gate before opening a pull request:

   ```bash
   uv run --locked python -m tools.check --scope local
   ```

8. Open a pull request to protected `main`. Required checks must pass; the default merge strategy is squash with linear history.

## Repository language

Write repository-authored engineering artifacts in English: architecture, ADRs, contracts, plans, prompts, ledgers, iteration reports, runbooks, templates, code comments, and contributor documentation. The existing normative `*-ru.md` product blueprints and declared localized product content under `docs-site/docs/<locale>/**` are explicit exceptions. Refer to Russian blueprint requirements by stable ID and explain them in English.

Durable evidence and handoffs are English. Unless the user explicitly requests another language for the current task, only the final user-facing completion report is written in Russian.

## Contract changes

Changes to APIs, ports, DTOs/events, persisted schemas, configuration defaults, identities, retry/idempotency semantics, browser-visible behavior, logs/audit, alerts, migrations, or rollout gates require explicit compatibility classification. Breaking changes require migration, rollback, verification, and documentation.

Normative product requirements are added to `custometry-technical-blueprint-ru.md` first and mirrored in `custometry-technical-blueprint-human-ru.md` in the same pull request. Generated indexes are updated deterministically; CI checks drift and never commits generated files.

## Evidence

Passing unit tests does not prove database, browser, Compose, recovery, supply-chain, or performance readiness. Use the nearest real boundary required by the change. The gate matrix and proof boundaries are documented in `docs/architecture/tooling-gates.md`.

Do not create a detailed workstream plan, prompt pack, or stage ledger unless that workflow has been explicitly approved. When staged execution is approved, the only durable execution sources are `plan_doc + prompt_pack_dir + stage_ledger`.
