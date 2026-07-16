---
prompt_name: b07-operations-s00-discovery
scope: Discovery for Operations; no execution while this outline remains disabled.
spec_version: 0.8.2-draft
requirement_ids: &id001
- GAP-036
- AC-027
- AC-030
- AC-040
language:
  implementation: en
  repository_artifacts: en
  agent_report: en
  user_completion_report: ru
context_sources:
  always_read:
  - path: AGENTS.md
    why: repository discovery contract
  - path: .codex/AGENTS.md
    why: normative repository contract
  task_entrypoints:
  - path: custometry-technical-blueprint-ru.md
    why: normative requirement definitions
    inspect_symbols: *id001
  - path: docs/architecture/workstreams/b07-operations-plan.md
    why: workstream scope, dependencies, and evidence contract
    inspect_symbols:
    - S00
    - Discovery
  - path: docs/architecture/workstreams/b07-operations-stage-reports/b07-operations-stage-ledger.md
    why: current execution truth and predecessor gate
    inspect_symbols:
    - S00
  conditional_bundles:
    contract_consumers:
      read_when: a public, persisted, config, identity, artifact, or browser contract may change
      paths:
      - docs/architecture/bounded-context-map.md
      - docs/architecture/development-operating-model.md
  consult_if_needed:
  - path: custometry-technical-blueprint-human-ru.md
    read_when: product meaning or user-facing explanation is ambiguous
skill_routing:
- skill: architecture-design
  role: primary
  use_when: executing the authorized S00 discovery stage
- skill: architecture-review
  role: companion_or_terminal_reviewer
  use_when: performing the required independent review after implementation evidence exists
change_ownership:
  owned_paths:
  - packages/execution
  - packages/notifications
  - apps/scheduler
  - apps/orchestrator
  - apps/reconciler
  - apps/web
  - docs/architecture/workstreams/b07-operations-*
  - .codex/agents/generated/b07-operations/
  foreign_exclusions:
  - unrelated dirty files
  - other workstreams
  - secrets and raw PII
  - production systems
  - Penpot until separately authorized
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches:
  - packages/execution
  - packages/notifications
  - apps/scheduler
  - apps/orchestrator
  - apps/reconciler
  - apps/web
  possible_secondary_touches:
  - docs/architecture
  - docs/contracts
  - tests
  expected_deletions: []
validation_strategy:
  depth: integration
  acceptance_surfaces:
  - discovery
  - requirement traceability
  - contract classification
  - nearest changed real boundary
  evidence_target: docs/architecture/workstreams/b07-operations-stage-reports/S00-discovery.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b07-operations-s00-discovery
  exclusions:
  - later-stage acceptance
  - broader release readiness
  - external mutation without explicit authority
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B07
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b07-operations-plan.md
  prompt_pack_dir: .codex/agents/generated/b07-operations
  stage_ledger: docs/architecture/workstreams/b07-operations-stage-reports/b07-operations-stage-ledger.md
  stage_id: S00
  predecessor_gate:
    stage_id: null
    allowed_statuses: []
  state_preconditions:
  - The ledger is active and names this stage as current.
  - This prompt has been detailed against the implemented repository state and changed to executable/true.
  - All hard dependencies and required decisions have accepted evidence.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: false
    allowed_branch: null
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S01
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

When separately activated and detailed, complete `S00 — Discovery` for `B07 Operations`: Confirm source-anchored scope, ownership, vocabulary, dependencies, risks, and stop gates.

## Non-goals

- Do not execute this outline while `readiness: outline`, `enabled: false`, or the ledger is dormant.
- Do not implement later stages, another workstream's primary requirements, or an external/production side effect.
- Preserve this workstream boundary: Operational email/webhook channels, plugin lifecycle, and user-sent report email are owned by B11 and B10, not this workstream.

## Verified current context

- Fact: the canonical matrix assigns the listed requirement IDs to `B07`.
- Fact: the Program Plan declares hard dependencies ['B01', 'B03', 'B04', 'B06'] and soft dependencies ['B05'].
- Fact: the linked ledger is initially dormant and every stage is disabled.
- Unknown/blocker: the exact repository state, source hashes, and implementation choices must be refreshed immediately before activation.

## Context acquisition

Read the declared sources in order and stop when ownership, requirements, changed contracts, expected files, acceptance surfaces, proof boundary, and blockers are known. Normal budget is eight files. Expand only for a failing check, discovered consumer, or material ambiguity.

## Requirements

### Must

- Preserve every listed requirement's primary ownership and accepted product meaning.
- Confirm source-anchored scope, ownership, vocabulary, dependencies, risks, and stop gates.
- Classify every affected contract dimension and preserve dependency direction.
- Use the nearest meaningful evidence; do not substitute static or mock evidence for a real changed boundary.

### Should

- Keep the implementation slice small enough to review and roll back.
- Reuse accepted repository contracts, fixtures, and Frost components instead of introducing parallel conventions.

## Forbidden actions

- Do not change public, persisted, config, identity, idempotency, artifact, or browser contracts silently.
- Do not expose secrets, PII, cookies, tokens, DSNs, or raw provider payloads.
- Do not infer commit, push, merge, deploy, production, paid-service, or Penpot authority.
- Do not create a second ledger, `GOAL.md`, per-stage branch, worktree, stash, or coordination folder.

## Work plan and stop gates

1. Re-verify the ledger, predecessor, source hashes, dependencies, owned paths, and requirement definitions.
2. Detail this outline into one executable prompt without widening scope.
3. Implement the smallest complete `S00` outcome.
4. Run focused checks and the nearest changed real-boundary evidence.
5. Update the ledger after validation and before the English stage report.

Stop as `blocked` or `partial` when authority, predecessor evidence, a required decision, safe ownership, compatibility path, or boundary evidence is missing.

## Contracts and side effects

Classify API, ports, DTO/events/artifacts, persistence, config/defaults, identity/cache/idempotency, service calls, retry/timeout/unknown state, audit/redaction, browser behavior, operations, migration, and rollback as `none`, `compatible-change`, `breaking-change`, or `unknown`. Durable effects require destination, authority, visibility, dedupe identity, retry classes, reconciliation, and rollback.

## Validation and evidence

- Planned depth: `integration`.
- Evidence target: `docs/architecture/workstreams/b07-operations-stage-reports/S00-discovery.md`.
- Required boundary: the nearest surface actually changed by this stage.
- Explicit exclusions: later stages and broader release readiness.

## Acceptance criteria

- [ ] The authorized `S00` outcome is observable and every listed requirement has traceable evidence.
- [ ] Prompt state is executable only after the ledger and source-hash gates are real.
- [ ] Contract impact, migration, rollback, and side effects are classified.
- [ ] Owned/foreign file manifest is accurate and unrelated changes are preserved.
- [ ] Required checks and real-boundary evidence pass, or the stage is recorded blocked/partial.
- [ ] The ledger is updated before the report; no later stage is implicitly unlocked.

## Result and handoff

Write the durable stage result, evidence, contract impact, file manifest, blocker state, and exact next ledger-allowed action in English. The user-facing completion report is Russian unless requested otherwise. Do not claim implementation, milestone, or release readiness beyond the observed boundary.
