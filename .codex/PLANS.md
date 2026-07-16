---
registry_schema_version: 1
program_plan: docs/architecture/program/custometry-program-plan.md
execution_mode: goal_driven
active_workstreams:
  - workstream_id: B01
    plan_doc: docs/architecture/workstreams/b01-experience-platform-plan.md
    prompt_pack_dir: .codex/agents/generated/b01-experience-platform
    stage_ledger: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
---

# Custometry Long-Horizon Plan Registry

This file is a compact registry for active multi-iteration work. It is not a task prompt, historical log, or replacement for the machine blueprint, architecture plan, prompt pack, or stage ledger.

## Usage

Update this file only when an active workstream, checkpoint, blocker, or durable next action changes. Keep detailed stage evidence in the plan-local stage ledger and reports.

For ordinary bounded tasks, do not load or update this file.

## Project baseline

- normative specification: `custometry-technical-blueprint-ru.md`, `0.8.2-draft`;
- explanatory mirror: `custometry-technical-blueprint-human-ru.md`;
- repository state: Foundation scaffold with minimal local Web/API/control-PostgreSQL health/docs runtime; no product vertical slice;
- release sequence: `repository_foundation` → `product_foundation` →
  `vertical_alpha` → `public_mvp` → `v1_feature_freeze` → `v1_target`;
- the canonical dependency graph, release gates, requirement allocation, and
  artifact links live in
  `docs/architecture/program/custometry-program-plan.md`;
- every staged workstream uses exactly one linked
  `plan_doc + prompt_pack_dir + stage_ledger`.
- every B01–B13 and W14 iteration is executed by one Codex Goal; the Goal
  re-reads the ledger after each accepted stage and never supplies stage
  authority itself.

## Active staged workstreams

| Workstream | Plan | Prompt pack | Stage ledger |
|---|---|---|---|
| `B01` Experience Platform | `docs/architecture/workstreams/b01-experience-platform-plan.md` | `.codex/agents/generated/b01-experience-platform` | `docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md` |

The stage ledger remains the sole current-stage authority. Goal runtime state
is ephemeral and does not replace the staged trio. Every other initial ledger
remains dormant. Executable prompt content alone is not execution authority.

## Accepted development sequence

The canonical W00/B01–B13/W14 order and milestone gates are defined by the
Program Plan. `docs/architecture/development-operating-model.md` explains the
shared S00–S06 model. This registry records only currently active or blocked
workstreams and deliberately does not duplicate `current_stage`, which belongs
only to the stage ledger.

## Activated workstream

The complete preparation set and M3 Pro Foundation proof passed independent
cold review and bounded follow-up fixes. B01 Experience Platform is the sole
active workstream, and its ledger permits only S00 Discovery. Penpot access and
canonical file authority remain a separate decision and are not asserted by
this registry.

## Open blueprint decisions

- `OPEN-007`: customer ID completeness threshold for customer analytics;
- `OPEN-008`: minimum supported history for each forecast target.

These are not blockers for repository scaffolding and must not receive invented defaults.
