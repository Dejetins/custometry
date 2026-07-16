---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b01-s02-experience-platform-domain-application
scope: "Implement and verify the framework-independent B01 route, navigation, system-surface, localization, motion, preference, and Focus application policy core."
spec_version: 0.8.2-draft
requirement_ids: [I18N-001, I18N-002, I18N-003, I18N-008, I18N-009, I18N-010, I18N-011, MOTION-001, MOTION-002, MOTION-003, MOTION-004, MOTION-005, MOTION-006, MOTION-007, MOTION-008, MOTION-009, MOTION-010, MOTION-011, MOTION-012, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, TEST-INV-022, TEST-INV-023, TEST-INV-042, TEST-INV-050, TEST-INV-051, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003]
language:
  implementation: en
  repository_artifacts: en
  user_completion_report: ru
context_sources:
  always_read:
    - path: AGENTS.md
      why: repository change discipline
    - path: .codex/AGENTS.md
      why: DDD, validation, and reporting rules
    - path: docs/architecture/workstreams/b01-experience-platform-plan.md
      why: implementation and proof boundary
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
      why: sole execution-state authority
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/S01-ux-contract.md
      why: accepted contracts and exact owned paths
  task_entrypoints:
    - path: docs/architecture/workstreams/b01-experience-platform-module.md
      why: domain/application boundary
    - path: packages/contracts
      why: shared contract types and schemas
    - path: apps/web
      why: composition seam only, not framework implementation in this stage
skill_routing:
  - skill: architecture-design
    role: primary
    use_when: preserving dependency direction and ports
  - skill: backend-quality-gates
    role: companion
    use_when: verifying any Python policy or validation code
  - skill: contract-impact-analysis
    role: companion
    use_when: an accepted S01 contract needs adjustment
change_ownership:
  owned_paths: [B01 framework-independent policy and application packages identified by S01, their focused tests, docs/architecture/workstreams/b01-experience-platform-stage-reports/S02-domain-application.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md]
  foreign_exclusions: [React rendering and CSS, external adapters, downstream business contexts, Penpot, other ledgers, publish and deploy]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [B01 policy/application sources and tests named by S01, docs/architecture/workstreams/b01-experience-platform-stage-reports/S02-domain-application.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md]
  possible_secondary_touches: [accepted B01 contracts and examples when a verified defect requires a compatible correction]
  expected_deletions: []
validation_strategy:
  depth: integration
  acceptance_surfaces: [unit and property invariants, contract examples, DDD boundaries, route and identity policy, deterministic state transitions]
  evidence_target: docs/architecture/workstreams/b01-experience-platform-stage-reports/S02-domain-application.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b01-policy-core
  exclusions: [React behavior, browser history runtime, network adapters, local docs runtime, real accessibility, canonical Penpot authority]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B01
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b01-experience-platform-plan.md
  prompt_pack_dir: .codex/agents/generated/b01-experience-platform
  stage_ledger: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
  stage_id: S02
  predecessor_gate:
    stage_id: S01
    allowed_statuses: [accepted, superseded]
  state_preconditions:
    - S01 is accepted or explicitly superseded in the ledger.
    - The ledger is active, current stage is S02, and only S02 has next_allowed true.
    - Accepted schemas, examples, compatibility rules, and exact implementation paths exist.
    - Any S01 contract correction is classified before implementation.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b01-experience-platform
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S03
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Implement the framework-independent policy and application core behind the B01
contracts. Deliver deterministic route resolution, navigation restoration,
system-surface mapping, localization and formatting policy, motion selection,
preference transitions, shell state, and Focus/Explore state transitions
through explicit ports. Prove invariants without relying on React, DOM,
browser history, storage, or network adapters.

## Non-goals

- Do not implement React components, CSS, router bindings, browser storage, API
  clients, docs renderers, or service workers.
- Do not implement downstream domain data or authorization policy.
- Do not redefine accepted S01 contracts for implementation convenience.
- Do not add a UI state library unless the accepted core cannot be expressed
  through existing language/runtime primitives and the dependency is approved.

## Verified current context

- Fact: S01 defines versioned data contracts and examples for every owned
  policy family.
- Fact: B01 core must remain independent of Web frameworks and external I/O.
- Fact: workspace, route, translation, Help, error, and token identities are
  locale-neutral.
- Fact: server permission decisions remain authoritative even when the core
  computes presentation visibility.
- Fact: Focus inherited/result filters and presentation controls have distinct
  identity semantics.

## Context acquisition

Read the accepted S01 report and inspect only the named schemas, examples, and
target packages. Trace existing dependency rules and test conventions. Build
tests from invariants and invalid examples before implementation. If a contract
is contradictory or cannot be implemented without browser/framework coupling,
stop and classify the contract issue rather than weakening the boundary.

## Requirements

### Must

- Implement immutable/value-validated route, workspace, origin, system-surface,
  Help target, locale, motion, preference, and Focus state types.
- Implement route resolution that rejects unknown routes, invalid workspace
  changes, unsafe query fields, forbidden metadata projection, and malformed
  Focus keys.
- Implement navigation intents for push/replace/Back/Forward, dirty guards,
  workspace switches, return-to-origin, and deterministic direct-link fallback.
- Implement Focus draft filters with Apply/Reset/Undo while protecting system
  and locked filters and separating result from presentation identity.
- Implement shell state transitions for expanded/collapsed sidebar,
  persistence intent, active route, command/help affordance, and reduced
  motion.
- Implement system-surface selection from stable reason codes without exposing
  raw backend errors or denied object metadata.
- Implement locale selection, fallback, formatting context, missing-key
  behavior, and catalog-parity policy without locale-dependent IDs.
- Implement named motion-policy selection with exact reduced-motion
  substitutions and no animation of semantically unsafe chart/data changes.
- Implement optimistic preference command/query ports and conflict/error
  semantics without durable adapter logic.
- Keep time, randomness, storage, history, permissions, and external results
  explicit as inputs or ports.
- Provide unit/property/invariant tests for valid and invalid transitions,
  identity stability, deterministic serialization, and forbidden states.
- Keep domain/application packages free of React, router, browser, HTTP,
  database, CSS, and adapter imports.

### Should

- Use small pure functions and immutable state transitions.
- Generate test cases from accepted schema examples where practical.
- Include deterministic serialization witnesses for route and preference
  contracts.

## Forbidden actions

- Do not perform browser, network, filesystem, database, or environment I/O in
  the policy core.
- Do not inspect hidden globals such as locale, timezone, window, history,
  storage, current user, or current workspace.
- Do not hide invalid state through default fallbacks when the contract says to
  fail closed.
- Do not put translated copy, raw colors, DOM selectors, or component instances
  in policy objects.
- Do not weaken DDD checks or tests to permit framework imports.
- Do not infer publish or deploy authority.

## Work plan and stop gates

1. Verify S01 acceptance, package boundaries, and no foreign changes in owned
   paths.
2. Write focused tests for route/workspace identity, navigation, Focus, system
   surfaces, localization, motion, preferences, and shell state.
3. Implement value types and pure policies in dependency order.
4. Implement application ports and orchestration without adapter imports.
5. Validate schemas/examples against core parsing and serialization.
6. Run DDD boundary, type, lint, unit/property, and contract checks.
7. Review contract impact for any correction and update S01 evidence only when
   truth changed.
8. Write S02 evidence, then update the ledger and unlock only S03 if accepted.

Stop on an S01 contradiction, framework leakage, ambient state, locale or
permission identity drift, nondeterministic behavior, unowned schema change, or
unresolved failing invariant.

## Contracts and side effects

The implementation must be side-effect-free except deterministic in-memory
state transitions. Application ports describe effects but do not execute them.
Any accepted contract correction requires classification, migration notes,
updated examples, and focused regression tests. No database, browser, network,
package-manager, external service, or design-tool side effect is authorized.

## Validation and evidence

- Run focused unit/property tests for each invariant family.
- Run TypeScript/Python type and lint gates for touched sources.
- Run contract example validation and DDD boundary checks.
- Run route, localization, and staged-work validators.
- Record exact tests, invalid witnesses, dependency checks, contract changes,
  exclusions, and file manifest in
  `docs/architecture/workstreams/b01-experience-platform-stage-reports/S02-domain-application.md`.
- Passing core tests do not prove browser history, rendering, storage,
  accessibility-runtime, network, or docs/help behavior.

## Acceptance criteria

- [ ] All accepted policy contracts have framework-independent implementations
      or an explicit justified adapter-only disposition.
- [ ] Route, workspace, query, Focus, system-surface, locale, motion,
      preference, and shell invariants have positive and negative tests.
- [ ] Result and presentation identity remain distinct and deterministic.
- [ ] No framework, adapter, I/O, or ambient-state dependency enters the core.
- [ ] Contract corrections are compatible or explicitly blocked.
- [ ] Focused gates and DDD checks pass.
- [ ] S02 evidence records exact proof and exclusions.
- [ ] Ledger transition occurs before handoff and only S03 is unlocked.

## Result and handoff

Report status, implemented types/use cases/ports, contract impact, test and
validation evidence, file manifest, blockers, residual risks, and proof
boundary. Hand off S03 only after accepted S02 evidence and ledger update.
