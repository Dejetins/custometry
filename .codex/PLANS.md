# Custometry Long-Horizon Plan Registry

This file is a compact registry for active multi-iteration work. It is not a task prompt, historical log, or replacement for the machine blueprint, architecture plan, prompt pack, or stage ledger.

## Usage

Update this file only when an active workstream, checkpoint, blocker, or durable next action changes. Keep detailed stage evidence in the plan-local stage ledger and reports.

For ordinary bounded tasks, do not load or update this file.

## Project baseline

- normative specification: `custometry-technical-blueprint-ru.md`, `0.8.2-draft`;
- explanatory mirror: `custometry-technical-blueprint-human-ru.md`;
- repository state: Foundation scaffold with minimal local Web/API/control-PostgreSQL health/docs runtime; no product vertical slice;
- target release sequence: `vertical_alpha` → `public_mvp` → `v1_target`;
- first broad implementation requires an accepted plan with linked prompt pack and stage ledger.

## Active staged workstreams

None. No prompt pack is currently authorized for execution.

## Accepted development sequence

The repository-level order is defined in `docs/architecture/development-operating-model.md`: Foundation → Experience Platform → Local Data Lab → context-by-context vertical slices → hardening → Universal XLSX last. This registry does not expand those blocks into stages.

## Candidate next workstream

After Foundation repository/tooling/runtime acceptance, the next candidate is the Experience Platform: Frost foundations/components, canonical route registry and shell, versioned contract-generated mocks, i18n/accessibility/system states, and the local `/docs` + in-app `/help` foundation.

Creating its detailed `plan_doc`, `prompt_pack_dir`, `stage_ledger` and iteration reports is a separate user-approved task. No such artifacts are created by the current Foundation preparation.

## Open blueprint decisions

- `OPEN-007`: customer ID completeness threshold for customer analytics;
- `OPEN-008`: minimum supported history for each forecast target.

These are not blockers for repository scaffolding and must not receive invented defaults.
