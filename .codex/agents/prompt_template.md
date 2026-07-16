---
prompt_name: <stable-kebab-case-name>
scope: "<one exact outcome and its boundary>"
spec_version: 0.8.2-draft
requirement_ids: [<normative-requirement-id>]
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
      why: selected normative sections and requirement IDs
      inspect_symbols: [<section-heading>, <requirement-id>]
    - path: <path>
      why: <canonical entrypoint reason>
      inspect_symbols: [<symbol-or-concern>]
  conditional_bundles:
    <bundle_name>:
      read_when: <trigger>
      paths: [<path>]
  consult_if_needed:
    - path: custometry-technical-blueprint-human-ru.md
      read_when: product meaning or user-facing explanation is ambiguous
skill_routing:
  - skill: <exact-primary-skill-name>
    role: primary
    use_when: <trigger>
  - skill: <exact-companion-or-review-skill-name>
    role: companion_or_terminal_reviewer
    use_when: <trigger>
change_ownership:
  owned_paths: [<path>]
  foreign_exclusions: [<path-or-rule>]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [<path>]
  possible_secondary_touches: [<path>]
  expected_deletions: []
validation_strategy:
  depth: tests_only | integration | api | browser | runtime | performance | delivery
  acceptance_surfaces: [<surface>]
  evidence_target: <ledger-or-report-path>
  tests_only_allowed_reason: <required-when-tests-only>
proof_boundary:
  label: <exact-boundary>
  exclusions: [<what-this-does-not-prove>]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: null
  execution_mode: goal_driven
  plan_doc: null
  prompt_pack_dir: null
  stage_ledger: null
  stage_id: null
  predecessor_gate:
    stage_id: null
    allowed_statuses: []
  state_preconditions: []
  # Empty only while this prompt is outline/disabled or its ledger is dormant.
  # The active executable current stage must pin at least one reviewed source.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: false
    allowed_branch: null
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: null
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

<State the exact observable outcome. Reference requirement IDs.>

## Non-goals

- <Explicitly excluded scope.>

## Verified current context

- Fact: <current source-anchored fact>.
- Assumption: <bounded assumption and why it is safe>.
- Unknown/blocker: <missing evidence or `none`>.

## Context acquisition

Read in the frontmatter order. For the machine blueprint, read only the `inspect_symbols` sections and requirement IDs selected for this task. Normal budget: `<= 8` files. Stop when ownership, changed contracts, files, acceptance surfaces, proof boundary, and blockers are known. Expand only for a failing check, material ambiguity, or discovered contract consumer.

## Requirements

### Must

- <Required behavior and requirement ID.>

### Should

- <Recommended behavior; deviation requires a decision record.>

## Forbidden actions

- Do not expand beyond owned scope.
- Do not change a public/persisted/config/browser contract silently.
- Do not expose secrets, PII, cookies, tokens, or raw provider payloads.
- Do not infer commit, push, deploy, production, or paid/external side-effect authority.

## Work plan and stop gates

1. <Inspect/confirm the bounded current state.>
2. <Implement the smallest complete change.>
3. <Run focused gates and the nearest meaningful boundary.>
4. For staged work, update the ledger after validation and before the final report.

Stop with `blocked` or `partial` if a required predecessor, authority, contract decision, source, or evidence boundary is missing.

## Contracts and side effects

Classify applicable surfaces as `none`, `compatible-change`, `breaking-change`, or `unknown`. For durable/external effects define destination, authority, visibility, idempotency/dedupe identity, retry classes, timeout, unknown-state reconciliation, audit/redaction, migration, and rollback.

## Validation and evidence

- Local gates: `<commands>`.
- Real-boundary evidence: `<API/database/browser/runtime/adapter/benchmark/delivery evidence>`.
- Evidence location: `<path>`.
- Explicit exclusions: `<what remains unverified>`.

## Acceptance criteria

- [ ] <Observable outcome and requirement ID.>
- [ ] `spec_version`, `requirement_ids`, state/hash preconditions, and branch policy are resolved for every staged prompt.
- [ ] `readiness` and `enabled` agree: `outline/false` or `executable/true`.
- [ ] Contract classification is complete.
- [ ] File manifest and foreign exclusions are accurate.
- [ ] Required evidence exists at the named boundary.
- [ ] Staged ledger is updated before the report, if applicable.

## Result and handoff

Write the durable result, ledger update, evidence, and handoff in English. The final user-facing completion report is Russian unless the user explicitly requests another language. Include outcome, requirement IDs, created/modified/deleted files, contract impact, actual checks/evidence, unverified boundaries, blockers, residual risks, and the next ledger-allowed action. Do not claim a later stage or broader release readiness.
