---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b01-s01-experience-platform-ux-contract
scope: "Freeze versioned B01 route, shell, token, component, motion, system-surface, Help, localization, accessibility, generated-mock, and Focus contracts before implementation."
spec_version: 0.8.2-draft
requirement_ids: [A11Y-001, A11Y-002, A11Y-003, A11Y-004, A11Y-005, A11Y-006, A11Y-007, A11Y-008, A11Y-009, A11Y-010, HELP-001, HELP-002, HELP-003, HELP-004, I18N-001, I18N-002, I18N-003, I18N-004, I18N-005, I18N-006, I18N-007, I18N-008, I18N-009, I18N-010, I18N-011, MOTION-001, MOTION-002, MOTION-003, MOTION-004, MOTION-005, MOTION-006, MOTION-007, MOTION-008, MOTION-009, MOTION-010, MOTION-011, MOTION-012, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, THEME-001, THEME-002, THEME-003, THEME-004, THEME-005, THEME-006, THEME-007, THEME-008, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, UX-JOURNEY-001, UX-JOURNEY-002, UX-JOURNEY-006]
language:
  implementation: en
  repository_artifacts: en
  user_completion_report: ru
context_sources:
  always_read:
    - path: AGENTS.md
      why: repository contract
    - path: .codex/AGENTS.md
      why: validation and artifact policy
    - path: docs/architecture/workstreams/b01-experience-platform-plan.md
      why: scope and stage boundaries
    - path: docs/architecture/development-runtime-contract.md
      why: mode selection, mock/real configuration, escalation, and release isolation
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
      why: sole stage-state authority
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/S00-discovery.md
      why: accepted current-state and file manifest
  task_entrypoints:
    - path: docs/architecture/workstreams/b01-experience-platform-module.md
      why: DDD ownership and ports
    - path: docs/architecture/documentation-platform.md
      why: docs/help information architecture and visibility
    - path: docs/architecture/program/requirement-matrix.json
      why: exact requirements and evidence profiles
  consult_if_needed:
    - path: custometry-technical-blueprint-ru.md
      read_when: exact route, motion, accessibility, or UI invariant is disputed
skill_routing:
  - skill: architecture-design
    role: primary
    use_when: freezing DDD boundaries, ports, schemas, and compatibility rules
  - skill: ui-ux-pro-max
    role: companion
    use_when: defining the Frost token/component, density, motion, accessibility, and responsive contracts
  - skill: contract-impact-analysis
    role: companion
    use_when: classifying route, DTO, schema, default, and browser-visible compatibility
change_ownership:
  owned_paths: [docs/contracts/experience-platform/**, B01-owned token and component contract sources, B01-owned route/help/localization schema sources, docs/architecture/workstreams/b01-experience-platform-stage-reports/S01-ux-contract.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md]
  foreign_exclusions: [business context schemas, stable authorization policy, product calculations, Penpot mutation, other workstream ledgers, commit, push, merge, deploy]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [B01 contract schemas and examples identified by S00, docs/architecture/workstreams/b01-experience-platform-stage-reports/S01-ux-contract.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md]
  possible_secondary_touches: [docs/contracts/README.md, docs/architecture/README.md, route/help/localization validator fixtures]
  expected_deletions: []
validation_strategy:
  depth: integration
  acceptance_surfaces: [JSON Schema or TypeScript contract validation, route and metadata validators, token/component catalog checks, accessibility scenario review, generated example parity]
  evidence_target: docs/architecture/workstreams/b01-experience-platform-stage-reports/S01-ux-contract.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b01-contract-freeze
  exclusions: [implemented React behavior, real browser acceptance, real downstream services, canonical Penpot authority, product milestone acceptance]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B01
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b01-experience-platform-plan.md
  prompt_pack_dir: .codex/agents/generated/b01-experience-platform
  stage_ledger: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
  stage_id: S01
  predecessor_gate:
    stage_id: S00
    allowed_statuses: [accepted, superseded]
  state_preconditions:
    - S00 is accepted or explicitly superseded in the ledger.
    - The ledger is active, current stage is S01, and only S01 has next_allowed true.
    - S00 defines exact owned paths, provisional consumers, risks, and browser evidence matrix.
    - Any contract that depends on unresolved Penpot authority is represented in source-backed semantics and blocks design-file mutation only.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b01-experience-platform
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S02
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Freeze the smallest complete set of versioned B01 contracts required to build
the Experience Platform without ambiguity. Define semantic Frost tokens,
component anatomy and states, route/history and workspace identity, system
surfaces, motion and reduced motion, Help and localization metadata,
accessibility behavior, preferences, generated API/mock examples, and
route-backed Focus/Explore semantics.

## Non-goals

- Do not implement React components, routers, adapters, or application runtime.
- Do not design downstream business screens in detail.
- Do not promote provisional downstream schemas to accepted service contracts.
- Do not use Penpot as authority or mutate a design file.
- Do not add dependencies before the contract demonstrates need, license,
  offline compatibility, and ownership.

## Verified current context

- Fact: S00 contains the accepted inventory, requirement routing, consumer
  seams, and exact file manifest.
- Fact: route IDs, translation IDs, Help IDs, error codes, token names, and
  component variant names must remain locale-neutral.
- Fact: authorization is server-owned; client visibility cannot be the only
  enforcement.
- Fact: Focus/Explore is route-backed and presentation state must not alter
  analytical result identity.
- Fact: ECharts is the only v1 Web chart engine, behind product-owned
  `ChartSpec`; B01 defines layout seams, not analytical series semantics.
- Fact: S01 must freeze Fast Loop mock/real disclosure and the escalation
  contract for Hybrid, Full Stack, and Release without claiming target-only
  developer capabilities exist.

## Context acquisition

Read S00 first. Inspect only the contract and validation entrypoints it names.
For each proposed contract, trace at least one producer, consumer, error path,
versioning rule, example, and acceptance surface. Compare route, UI, motion,
Help, i18n, and accessibility requirements against the matrix. Stop when a
decision changes business meaning, authorization, analytical identity, or
requires unconfirmed Penpot authority.

## Requirements

### Must

- Define the canonical route manifest fields: route ID, workspace path,
  capability, permission scope, title key, Help target, safe query policy,
  parent/origin behavior, and system-state mapping.
- Define immutable `workspaceKey`, deep-link, Back/Forward, workspace-switch,
  dirty-guard, and return-to-origin rules.
- Define Focus/Explore inheritance, local draft filters, Apply/Reset/Undo,
  result-versus-presentation identity, chart/table parity metadata, and direct
  deep-link fallback.
- Define Frost semantic color, typography, spacing, radius, border, elevation,
  icon, density, focus, status, chart-container, and motion tokens.
- Define component anatomy, variants, sizes, interactive states, keyboard
  behavior, accessible names, content constraints, and responsive rules for
  shell, navigation, buttons, inputs, tabs, menus, popovers, drawers, dialogs,
  tables, compact KPI groups, Result Trust summary, status, and loading.
- Define expanded icon-and-label and collapsed icon-only sidebar behavior with
  stable order, accessible tooltips, persistence, and animation.
- Define the complete motion matrix and reduced-motion substitution.
- Define 403, 404, session-expired, maintenance, and upgrade-required schemas
  with safe messages and actions that do not leak denied metadata.
- Define en/ru catalog structure, fallback, interpolation, pluralization,
  number/date/currency/timezone formatting, missing-key behavior, and parity
  checks.
- Define local `/docs` and permission-aware `/help` metadata, search, route and
  field mapping, visibility, offline delivery, and forbidden-content behavior.
- Define user preference DTO/versioning and optimistic concurrency without
  storing authorization or sensitive data in browser state.
- Define generated client/mock schemas and examples, explicit mock-mode
  disclosure, error examples, and parity checks.
- Define versioned development-mode configuration and disclosure: accepted
  values, default resolution, mock/real selection, production rejection,
  error behavior, and the evidence mode required by each representative flow.
- Define accessibility acceptance for semantics, keyboard, focus, screen
  reader, contrast, non-color meaning, 200% zoom/reflow, text scaling, reduced
  motion, and non-hover access.
- Record compatibility, migration, rollback, error, and deprecation policy for
  every stable browser-facing identifier or schema.

### Should

- Keep contracts framework-independent and serializable.
- Reuse existing repository schema and validation conventions.
- Define a minimal representative component set before adding specialized
  variants.
- Include valid and invalid examples for every externally consumed schema.

## Forbidden actions

- Do not hardcode raw visual values in screen contracts when a semantic token
  exists.
- Do not encode translated text as an identifier.
- Do not place permission truth, result identity, or durable execution state in
  presentation contracts.
- Do not create hand-authored mock shapes that cannot be generated from the
  accepted schema.
- Do not make runtime mode implicit, allow a development mode in production,
  or use Fast Loop evidence to satisfy a Hybrid, Full Stack, or Release claim.
- Do not use remote fonts, CDN scripts, runtime-loaded icons, or Internet
  dependencies.
- Do not change the canonical blueprint meaning to fit an implementation
  convenience.
- Do not infer commit, push, merge, deploy, or release authority.

## Work plan and stop gates

1. Verify S00 acceptance, requirement scope, and exact contract manifest.
2. Freeze ubiquitous language and ownership for every contract family.
3. Define route, history, workspace, Focus, and navigation-guard schemas.
4. Define Frost tokens, component variants, density, responsive, and motion
   contracts.
5. Define system surfaces, Help/docs, localization, preferences, generated
   client/mock contracts, and runtime-mode configuration/disclosure.
6. Define accessibility and browser acceptance scenarios alongside contracts.
7. Add schemas, examples, compatibility rules, and focused validators/tests.
8. Review cross-context dependencies and classify contract impact.
9. Write S01 evidence, then update the ledger and unlock only S02 if accepted.

Stop on ambiguous ownership, an authorization or metadata-leak risk, a
locale-dependent identity, inaccessible required interaction, unversioned mock
shape, missing migration rule, or a design decision that cannot be resolved
without the deferred Penpot authority.

## Contracts and side effects

Contract edits are durable repository changes but have no runtime or external
side effect in S01. For each schema record version, owner, compatibility,
consumer, producer, examples, invalid cases, defaults, errors, migration, and
rollback. New dependencies are not authorized by this prompt. Any proposal
that changes API, persisted preference, browser URL, cache/request identity, or
authorization-visible behavior must receive an explicit contract-impact class.

## Validation and evidence

- Validate all JSON Schema, TypeScript types, examples, route metadata,
  localization catalogs, docs/help metadata, and token/component manifests.
- Run contract drift, DDD boundary, route registry, docs visibility/link,
  localization, staged-work, and agent artifact checks as applicable.
- Exercise generated valid/invalid examples without claiming browser behavior.
- Record exact files, commands, contract classifications, decisions, and
  exclusions in
  `docs/architecture/workstreams/b01-experience-platform-stage-reports/S01-ux-contract.md`.
- A green contract suite proves schemas and examples, not React, browser,
  accessibility-runtime, or downstream-service correctness.

## Acceptance criteria

- [ ] Route/history/workspace/Focus and guard contracts are complete and
      locale-neutral.
- [ ] Frost tokens and component anatomy/states cover the representative shell
      and system surfaces without raw-value bypass.
- [ ] Motion and reduced-motion matrices are explicit.
- [ ] Help/docs, en/ru, preferences, system surfaces, and generated mocks have
      schemas, examples, errors, and visibility rules.
- [ ] Fast Loop mock/real configuration, production rejection, and
      Hybrid/Full Stack/Release escalation rules are versioned and testable.
- [ ] Accessibility behavior is part of each relevant component and journey
      contract.
- [ ] Every stable identifier/schema has compatibility, migration, and rollback
      treatment.
- [ ] Valid and invalid examples pass focused validation.
- [ ] No Penpot authority, downstream domain truth, or browser acceptance is
      implied.
- [ ] Ledger transition occurs before handoff and only S02 is unlocked.

## Result and handoff

Report status, exact contract files, compatibility classes, generated examples,
validation evidence, rejected alternatives, blockers, and residual risks.
Hand off S02 only with an accepted S01 report and synchronized ledger.
