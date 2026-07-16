---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b02-s01-local-data-lab-contract
scope: "Freeze and validate the versioned profile, fixture manifest, reset, migration, benchmark-warning, documentation, and optional-demo consumer contracts for B02."
spec_version: 0.8.2-draft
requirement_ids: [JOURNEY-001, GAP-019, TEST-INV-040]
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
    - path: docs/architecture/workstreams/b02-local-data-lab-plan.md
      why: accepted B02 scope and stage gates
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
      why: predecessor and current-stage authority
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S00-discovery.md
      why: accepted source, ownership, coverage, and risk baseline
  task_entrypoints:
    - path: custometry-technical-blueprint-ru.md
      why: canonical data rules, onboarding behavior, CPU policy, golden fixtures, and benchmark targets
      inspect_symbols: [JOURNEY-001, GAP-019, TEST-INV-040, section 22.3, section 23.4]
    - path: docs/architecture/workstreams/b02-local-data-lab-module.md
      why: profile, manifest, reset, migration, port, and consumer definitions
      inspect_symbols: [State and contract model, Ports and adapters, Documentation and consumer integration]
    - path: deploy/compose/bootstrap.sh
      why: current profile selection and reset command semantics
      inspect_symbols: [data_profile, allow_benchmark, reset-demo-data]
  conditional_bundles:
    current_contracts:
      read_when: exact profile, manifest, SQL schema, or verifier behavior is needed
      paths: [deploy/demo-source/profiles/smoke.json, deploy/demo-source/profiles/demo.json, deploy/demo-source/profiles/benchmark.json, tests/golden/retail-demo-manifest.json, tests/golden/retail-demo-evidence.sql, tests/golden/verify_retail_demo.py]
    experience_consumer:
      read_when: defining local docs or optional-demo presentation metadata
      paths: [docs/architecture/workstreams/b01-experience-platform-module.md, docs/architecture/documentation-platform.md]
  consult_if_needed:
    - path: custometry-technical-blueprint-human-ru.md
      read_when: user-facing profile or onboarding wording remains ambiguous
skill_routing:
  - skill: architecture-design
    role: primary
    use_when: defining versioned ports, schemas, ownership, and dependency direction
  - skill: contract-impact-analysis
    role: companion_or_terminal_reviewer
    use_when: classifying profile, fixture, CLI, persisted-volume, migration, and consumer compatibility
change_ownership:
  owned_paths: [docs/contracts/data-lab/**, deploy/demo-source/profiles/*.json, tests/golden/retail-demo-manifest.json, docs/architecture/workstreams/b02-local-data-lab-module.md, docs/architecture/workstreams/b02-local-data-lab-plan.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S01-ux-contract.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md]
  foreign_exclusions: [runtime SQL implementation, Compose service changes, control-plane migrations, product onboarding authorization, B01 component internals, B03-B13 schemas, Penpot, unrelated worktree changes]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [docs/contracts/data-lab/**, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S01-ux-contract.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md]
  possible_secondary_touches: [deploy/demo-source/profiles/*.json, tests/golden/retail-demo-manifest.json, docs/architecture/workstreams/b02-local-data-lab-module.md, docs/architecture/workstreams/b02-local-data-lab-plan.md]
  expected_deletions: []
validation_strategy:
  depth: integration
  acceptance_surfaces: [JSON contracts, fixture manifest, lifecycle CLI, migration policy, consumer metadata, compatibility]
  evidence_target: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S01-ux-contract.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b02-s01-versioned-contracts
  exclusions: [implemented generator, real PostgreSQL behavior, destructive reset execution, browser proof, benchmark performance, release readiness]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B02
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b02-local-data-lab-plan.md
  prompt_pack_dir: .codex/agents/generated/b02-local-data-lab
  stage_ledger: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
  stage_id: S01
  predecessor_gate:
    stage_id: S00
    allowed_statuses: [accepted, superseded]
  state_preconditions:
    - S00 is accepted or explicitly superseded in the ledger.
    - The ledger status is active, current stage is S01, and only S01 has next_allowed true.
    - S00 requirement routing, ownership, and source inventory remain current.
    - Shared contract paths have an identified owner and no unsafe foreign overlap.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b02-local-data-lab
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S02
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Define the complete versioned contract for B02 before generator or adapter
implementation. Produce machine-valid profile and golden-manifest schemas,
stable lifecycle/error semantics, migration and persisted-volume rules,
benchmark resource warnings, safe local-documentation metadata, and a bounded
optional-demo consumer contract. Preserve B05 ownership of canonical data
rules while making `JOURNEY-001`, `GAP-019`, and `TEST-INV-040` testable by
later stages.

## Non-goals

- Do not implement seed generation, SQL adapters, Compose changes, or
  migrations.
- Do not execute reset, start containers, or generate benchmark rows.
- Do not implement first-admin, workspace, or authorization behavior.
- Do not establish analytical metric definitions.
- Do not change route or component contracts owned by B01 without an accepted
  coordination decision.

## Verified current context

- Fact: S00 must identify the accepted B02 requirement and ownership boundary.
- Fact: current profile JSON files declare schema version, profile, status,
  seed, opt-in flags, and counts.
- Fact: the current demo manifest additionally declares timezone, currency,
  grains, keys, synthetic PII classes, expected counts, KPIs, scenarios, and an
  evidence hash.
- Fact: changing a persisted data profile currently requires reset rather than
  implicit reseeding.
- Assumption: contract files may be added under `docs/contracts/data-lab/`
  because they are repository-authored internal contracts; confirm this against
  S00 ownership before editing.
- Unknown/blocker: exact consumer fields for first-run demo selection must be
  agreed with B01/B03 without moving authorization into B02.

## Context acquisition

Start from the accepted S00 report and current source schemas. Read no more than
the listed sources plus the exact consumer contract files required to resolve a
field. Compare the proposed schema with current JSON and SQL behavior. Stop if
a field would encode business semantics owned by another workstream or if a
breaking default cannot be approved.

## Requirements

### Must

- Define a strict `DatasetProfile` schema with stable profile ID, schema
  version, seed, counts, opt-in, large-data confirmation, status, and resource
  warning fields.
- Define a strict `FixtureManifest` and canonical evidence schema covering
  profile identity, timezone, currency, grain, keys, synthetic PII class,
  counts, structural KPIs, scenarios, and evidence SHA-256.
- Define canonical JSON normalization, number/date representation, key
  ordering, and hashing behavior.
- Define valid and invalid examples for `smoke`, `demo`, and `benchmark`.
- Define compatibility rules for adding fields/scenarios and breaking rules for
  seed, grain, key, default, evidence serialization, or scenario-meaning
  changes.
- Define lifecycle commands and stable error categories for bootstrap, profile
  mismatch, large-data confirmation, migration failure, unsafe reset,
  evidence drift, and unsupported remote topology.
- Define persisted-volume identity and the exact safe reset authorization
  inputs.
- Define migration lifecycle responsibilities without assigning product
  context tables to B02.
- Define safe profile metadata for `/docs` and optional-demo consumers,
  including size, status, warning, and no-secret behavior.
- Define accessibility/localization expectations for consumer-facing labels
  while keeping IDs locale-neutral.
- Add contract validation tests or validators and record actual results.

### Should

- Use JSON Schema for JSON artifacts and concise Markdown for CLI/error and
  migration semantics.
- Keep `smoke` bounded, `demo` explicit, and `benchmark` double-confirmed.
- Reuse existing repository contract-generation and validation conventions.

## Forbidden actions

- Do not make benchmark the default.
- Do not allow a profile change to mutate an initialized volume.
- Do not put credentials, host paths, tokens, or real PII in profile or
  manifest contracts.
- Do not let B02 define revenue, customer, forecast, or promotion truth.
- Do not silently weaken source-scoped IDs, SCD validity, timezone, currency,
  grain, or primary-key requirements.
- Do not infer commit, push, deploy, or runtime authority.

## Work plan and stop gates

1. Verify S00 acceptance and current contract consumers.
2. Draft schemas, examples, compatibility table, and stable errors.
3. Review profile defaults, persisted-volume semantics, and benchmark warnings.
4. Review optional-demo and docs metadata with B01/B03 boundaries.
5. Add focused schema/negative tests and contract-drift checks.
6. Classify every changed contract dimension and migration need.
7. Write the S01 report with exact S02 implementation inputs.
8. Validate, then update the ledger and authorize only S02.

Stop if consumer authorization is ambiguous, a destructive reset rule lacks a
fail-closed identity check, schemas conflict with current normative data rules,
or a breaking contract lacks explicit authority and migration.

## Contracts and side effects

This stage creates versioned repository contracts only. No database, Docker,
network, or external side effect is authorized. Contract impact must cover:

- JSON profile/manifest/evidence schemas;
- fixture relational schema expectations;
- CLI names, defaults, exit categories, and persisted runtime state;
- migration ownership and compatibility window;
- profile identity and golden hash semantics;
- local docs/consumer fields and localization;
- secret/PII redaction.

Use `compatible-change` only when existing examples remain valid and semantics
are preserved. Mark unresolved runtime or benchmark behavior `unknown`.

## Validation and evidence

- Local gates:
  - focused JSON Schema positive and negative tests;
  - `uv run python -m tools.custometry_quality.validate_fixture_manifest`
  - `uv run python -m tools.custometry_quality.check_contract_drift`
  - `uv run python -m tools.custometry_quality.validate_staged_workstream`
  - `uv run python -m tools.custometry_quality.check_docs_links`
- Real-boundary evidence: none; examples are contract evidence only.
- Evidence location:
  `docs/architecture/workstreams/b02-local-data-lab-stage-reports/S01-ux-contract.md`.
- Explicit exclusions: generator correctness, PostgreSQL, Compose, reset
  deletion, migration execution, browser behavior, and benchmark support.

## Acceptance criteria

- [ ] Profile, manifest, and evidence schemas are strict, versioned, and tested.
- [ ] Valid and invalid examples cover all three profiles and fail-closed paths.
- [ ] Canonical serialization and SHA-256 behavior are unambiguous.
- [ ] Reset identity, profile mismatch, and benchmark confirmation semantics are
      explicit.
- [ ] Data-rule inputs preserve source namespace, SCD, UTC, currency, grain,
      key, return, and unknown-value behavior.
- [ ] Migration ownership does not absorb downstream context schemas.
- [ ] Optional-demo/docs metadata is safe, bounded, and localization-ready.
- [ ] Contract impact, migration, rollback, and proof exclusions are recorded.
- [ ] Focused checks pass and the ledger authorizes only S02.

## Result and handoff

Write durable contracts, S01 evidence, and the ledger update in English. The
Russian completion report states what was frozen, requirement IDs, changed
files, actual checks, compatibility classifications, unresolved decisions,
proof exclusions, and the exact S02 prompt. Do not claim implementation or
runtime behavior.
