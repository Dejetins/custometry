---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b01-s00-experience-platform-discovery
scope: "Freeze the verified B01 current state, ownership, requirement routing, consumer seams, browser matrix, risks, and exact implementation manifest without implementing product behavior."
spec_version: 0.8.2-draft
requirement_ids: [AC-028, AC-029, GAP-021, GAP-034, GAP-035, GAP-046, RISK-010, TEST-INV-022, TEST-INV-023, TEST-INV-042, TEST-INV-050, TEST-INV-051]
language:
  implementation: en
  repository_artifacts: en
  user_completion_report: ru
context_sources:
  always_read:
    - path: AGENTS.md
      why: repository workflow and reporting contract
    - path: .codex/AGENTS.md
      why: normative staged-work, validation, and proof rules
    - path: docs/architecture/program/custometry-program-plan.md
      why: B01 dependencies, milestones, and activation authority
    - path: docs/architecture/workstreams/b01-experience-platform-plan.md
      why: B01 scope and stage contract
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
      why: sole stage-state authority
  task_entrypoints:
    - path: docs/architecture/workstreams/b01-experience-platform-module.md
      why: ownership and DDD boundary
    - path: docs/architecture/program/requirement-matrix.json
      why: exact B01 requirement allocation and evidence classes
    - path: docs/architecture/repository-layout.md
      why: current repository and Web scaffold facts
    - path: docs/architecture/documentation-platform.md
      why: local docs/help visibility boundary
  consult_if_needed:
    - path: custometry-technical-blueprint-ru.md
      read_when: requirement meaning or UI invariant is disputed
    - path: custometry-technical-blueprint-human-ru.md
      read_when: a concise explanatory mirror is needed
skill_routing:
  - skill: architecture-design
    role: primary
    use_when: resolving B01 boundaries, contracts, and phased seams
  - skill: ui-ux-pro-max
    role: companion
    use_when: checking layout, accessibility, interaction, responsive, or motion implications
change_ownership:
  owned_paths: [docs/architecture/workstreams/b01-experience-platform-stage-reports/S00-discovery.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md]
  foreign_exclusions: [implementation code, other workstream artifacts, normative blueprint meaning, Penpot mutation, commit, push, merge, deploy]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [docs/architecture/workstreams/b01-experience-platform-stage-reports/S00-discovery.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md]
  possible_secondary_touches: [docs/architecture/workstreams/b01-experience-platform-plan.md, docs/architecture/workstreams/b01-experience-platform-module.md]
  expected_deletions: []
validation_strategy:
  depth: integration
  acceptance_surfaces: [requirement traceability, repository inventory, route and UI contract inventory, ownership boundaries, staged-work validation]
  evidence_target: docs/architecture/workstreams/b01-experience-platform-stage-reports/S00-discovery.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b01-discovery-only
  exclusions: [implemented Web behavior, browser acceptance, canonical Penpot authority, downstream domain readiness, product milestone acceptance]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B01
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b01-experience-platform-plan.md
  prompt_pack_dir: .codex/agents/generated/b01-experience-platform
  stage_ledger: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
  stage_id: S00
  predecessor_gate:
    stage_id: null
    allowed_statuses: []
  state_preconditions:
    - W00 Repository Foundation is accepted with current reproducible tool and M3 Pro evidence.
    - The B01 ledger is active, current stage is S00, and only S00 has next_allowed true.
    - The preparation set and independent cold review are complete.
    - The working tree has been inventoried and foreign changes are identified.
  required_source_hashes:
    custometry-technical-blueprint-ru.md: sha256:07db448e334b7c7605b6b86269b1e9d4d2c12ee277685932da2fd174e6f669f8
    custometry-technical-blueprint-human-ru.md: sha256:c5294770a968e4b5fa02709f1ecdadc5f70784fb422c1deb2e6ca26931ea2dc9
    .codex/AGENTS.md: sha256:20f418851e479dec1460d3c12274cad8d8beefc71464d02a7ba575d99cd00e9c
    docs/architecture/program/custometry-program-plan.md: sha256:4c0cfb0b364943f6092d6fe335aba96dca2ac8dead36e9015b913b73ee16c3e2
    docs/architecture/program/requirement-matrix.json: sha256:7cc3dc669f252dcfede0ffa5556f2103ee30b44e3e1b1d6f8cdfa0a73895a854
    docs/architecture/workstreams/b01-experience-platform-module.md: sha256:3e3dd41d6658b2d423bfc47ca7d3cb934de7616e35065a3bbdfc51e8fd75672d
    docs/architecture/workstreams/b01-experience-platform-plan.md: sha256:e6b7121ecceb7c343e1aded208d7b46d5dfc4841971619f0825afcc523df4325
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b01-experience-platform
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S01
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Create the verified B01 discovery baseline. Reconcile the normative UI and
experience requirements with the current repository, identify what truly
exists, define ownership and integration seams, map all B01-primary
requirements to S01–S06, and produce an exact implementation and evidence
manifest. Do not implement the Experience Platform in this stage.

## Non-goals

- Do not create or refactor application code.
- Do not invent stable API contracts owned by B03–B13.
- Do not select, confirm, or mutate a canonical Penpot file.
- Do not treat screenshots, previous chat claims, or planned files as current
  implementation evidence.
- Do not activate S01, publish, deploy, or claim milestone readiness.

## Verified current context

- Fact: B01 owns the shared Web shell and presentation contracts, not business
  calculations, analytical truth, authorization policy, or persistence owned
  by later contexts.
- Fact: the canonical program assigns 86 primary requirements to B01.
- Fact: W00 is the only hard dependency; later service contracts are
  provisional consumers rather than activation dependencies.
- Fact: Penpot authority is explicitly deferred and cannot be inferred from
  prior access or screenshots.
- Assumption to verify: the current Web scaffold is still Foundation-only and
  no hidden route, token, localization, or Help implementation should be
  preserved as stable without inspection.

## Context acquisition

Read the ledger first and fail closed unless S00 is authorized. Inspect the
current branch, dirty files, package manifests, Web entrypoints, UI packages,
docs-site configuration, route/help/localization validators, tests, and current
runtime commands. Search by requirement families and exact symbols rather than
loading the full repository. Read blueprint passages only when generated
requirement metadata and English architecture sources do not resolve meaning.

Build a fact ledger separating implemented, declared, proposed, unknown, and
blocked items. For every claimed existing behavior, record its source path and
nearest available evidence. Stop if current W00 evidence, ownership, or safe
file scope cannot be established.

## Requirements

### Must

- Inventory the current Web, contracts, localization, docs/help, testing, and
  build/runtime surfaces.
- Reconcile all B01-primary matrix rows with a stage and expected evidence.
- Record route, shell, token/component, motion, system-surface, Help, i18n,
  accessibility, generated-mock, Focus, and responsive requirements.
- Identify exact B01-owned paths, shared coordination paths, foreign paths, and
  mixed-file risks.
- Identify provisional consumer seams for B03–B13 without assigning their
  domain behavior to B01.
- Define representative browser journeys for sign-in shell, onboarding shell,
  route navigation, system states, docs/help, sidebar collapse, unsaved-change
  guards, and Focus return.
- Record dependency, package, licensing, offline-asset, and supply-chain
  implications without adding dependencies.
- Classify current and proposed contract changes as `none`,
  `compatible-change`, `breaking-change`, or `unknown`.
- List every unresolved decision with owner, due stage, and blocking rule.
- Write a durable S00 report and update only the ledger state required by the
  accepted outcome.

### Should

- Prefer tables that map requirements to owner, stage, evidence, and risk.
- Identify reusable existing scaffolds before proposing new packages.
- Keep the bounded reading and file manifest small enough for the next stage to
  execute without rediscovery.

## Forbidden actions

- Do not write application, test, schema, generated client, or design-system
  implementation.
- Do not copy a third-party UI kit or icon set without license and provenance
  review.
- Do not encode raw secrets, cookies, tokens, PII, browser storage, or provider
  payloads in evidence.
- Do not modify other workstream plans, ledgers, or prompts.
- Do not broaden staging, revert foreign changes, or use destructive Git.
- Do not infer commit, push, merge, deployment, or release authority.

## Work plan and stop gates

1. Verify ledger authorization, W00 proof, branch, worktree, and owned scope.
2. Inventory current repository surfaces and distinguish declaration from
   implementation and runtime proof.
3. Reconcile the 86 B01-primary requirements into stage/evidence groups.
4. Map route/UI states, consumer seams, contracts, side effects, and security
   boundaries.
5. Define exact primary/secondary file manifests for S01–S05.
6. Define browser, accessibility, locale, motion, and offline evidence matrix.
7. Record risks, open decisions, exclusions, and rollback considerations.
8. Run metadata, requirement, route, docs, and staged-work validators.
9. Write S00 evidence, then update the ledger and unlock only S01 if accepted.

Stop with `blocked` when W00 is stale, a required authority is missing, a
Penpot mutation is necessary, requirement ownership is contradictory, the
working tree cannot be safely separated, or the next-stage manifest depends on
unknown external state.

## Contracts and side effects

This stage changes only B01 discovery documentation and the authorized ledger
transition. It has no browser, database, API, package, external-service, or
design-tool side effect. Proposed contracts must name owner, versioning,
compatibility, migration, error semantics, security context, and acceptance
surface. Unknown downstream schemas remain explicit provisional seams.

## Validation and evidence

- Validate the requirement matrix and generated requirement index.
- Run route, docs metadata/link, localization, agent artifact, and staged-work
  validators that are available in the current repository.
- Run `uv run python -m tools.check --scope local` only after focused findings
  are resolved and report its proof boundary accurately.
- Record exact commands, exit status, source state, and any environmental
  exclusions in
  `docs/architecture/workstreams/b01-experience-platform-stage-reports/S00-discovery.md`.
- No browser or runtime acceptance is claimed in S00.

## Acceptance criteria

- [ ] Current repository facts are separated from declarations and proposals.
- [ ] Every B01-primary requirement has a stage and evidence disposition.
- [ ] Ownership and provisional consumer seams are explicit and DDD-aligned.
- [ ] Exact implementation, test, documentation, and evidence manifests exist.
- [ ] Contract impact, risks, open decisions, and stop gates are recorded.
- [ ] Penpot remains explicitly outside the accepted authority.
- [ ] Focused validators and applicable local gates pass or have honest
      environmental blockers.
- [ ] The S00 report is durable, English, and contains no sensitive data.
- [ ] The ledger is updated before the completion report and only S01 is
      unlocked on acceptance.

## Result and handoff

Return status, contract-impact classification, created/modified/deleted file
manifest, outside-scope files observed, validation evidence, blockers, residual
risks, and the exact ledger transition. If accepted, hand off only S01. If
partial or blocked, keep every successor locked and identify the authority or
evidence needed to resume.
