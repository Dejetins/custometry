---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b02-s03-local-data-lab-adapters
scope: "Implement and verify B02 PostgreSQL, Compose, migration, fixture-generation, reader-grant, safe-reset, and golden-evidence adapters against the accepted S01/S02 contracts."
spec_version: 0.8.2-draft
requirement_ids: [TEST-INV-010, TEST-INV-011, TEST-INV-012, TEST-INV-013, TEST-INV-016, TEST-INV-026, TEST-INV-028, TEST-INV-031, TEST-INV-033, AC-016, AC-021, AC-022]
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
      why: adapter scope, ownership, rollback, and proof boundary
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
      why: predecessor and current-stage authority
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S02-domain-application.md
      why: accepted deterministic core and fixture semantics
  task_entrypoints:
    - path: compose.yaml
      why: control/demo PostgreSQL services, volumes, networks, images, health, and resources
      inspect_symbols: [control-db, demo-source-db, migrate, networks, volumes, secrets]
    - path: deploy/compose/bootstrap.sh
      why: lifecycle, profile selection, migration, reset, and startup behavior
      inspect_symbols: [reset-demo-data, data_profile, allow_benchmark, compose up]
    - path: deploy/demo-source/init/030_seed.sql
      why: current deterministic relational generation adapter
      inspect_symbols: [CUSTOMETRY_DATA_PROFILE, seed, inserts]
  conditional_bundles:
    adapter_sources:
      read_when: implementing schema, grants, evidence, profile, or migration behavior
      paths: [deploy/demo-source/init/010_create_reader.sh, deploy/demo-source/init/015_profile.sh, deploy/demo-source/init/020_schema.sql, deploy/demo-source/init/040_grants.sql, tests/golden/retail-demo-evidence.sql, tests/golden/verify_retail_demo.py, migrations/env.py, migrations/versions/0001_foundation_metadata.py]
    accepted_contracts:
      read_when: checking adapter parity with S01/S02
      paths: [docs/contracts/data-lab/**, tools/custometry_quality/data_lab/**]
  consult_if_needed:
    - path: docs/architecture/development-operating-model.md
      read_when: runtime evidence, migration, or shared-file ownership is unclear
skill_routing:
  - skill: architecture-design
    role: primary
    use_when: preserving port/adapter direction and database ownership
  - skill: backend-quality-gates
    role: companion_or_terminal_reviewer
    use_when: verifying SQL, migrations, lifecycle scripts, and integration tests
change_ownership:
  owned_paths: [deploy/demo-source/**, tests/golden/**, tests/integration/data_lab/**, tests/recovery/data_lab/**, tools/custometry_quality/validate_fixture_manifest.py, tools/custometry_quality/validate_migration_lifecycle.py, compose.yaml, deploy/compose/bootstrap.sh, migrations/versions/0001_foundation_metadata.py, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S03-adapters.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md]
  foreign_exclusions: [future context migrations, product-domain code, B01 UI, production backup/restore, CI/release policy, real customer data, Penpot, unrelated worktree changes]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [deploy/demo-source/**, tests/golden/**, tests/integration/data_lab/**, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S03-adapters.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md]
  possible_secondary_touches: [compose.yaml, deploy/compose/bootstrap.sh, tools/custometry_quality/validate_fixture_manifest.py, tools/custometry_quality/validate_migration_lifecycle.py, migrations/versions/0001_foundation_metadata.py, tests/recovery/data_lab/**]
  expected_deletions: []
validation_strategy:
  depth: runtime
  acceptance_surfaces: [PostgreSQL schema, least-privilege reader, deterministic seed, migrations, reset refusal, golden evidence, Compose topology]
  evidence_target: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S03-adapters.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b02-s03-disposable-postgresql-adapters
  exclusions: [clean-host install, supported-host benchmark, browser behavior, whole-product backup/restore, production firewall, release readiness]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B02
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b02-local-data-lab-plan.md
  prompt_pack_dir: .codex/agents/generated/b02-local-data-lab
  stage_ledger: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
  stage_id: S03
  predecessor_gate:
    stage_id: S02
    allowed_statuses: [accepted, superseded]
  state_preconditions:
    - S02 is accepted or explicitly superseded in the ledger.
    - The ledger status is active, current stage is S03, and only S03 has next_allowed true.
    - Accepted S01 schemas and S02 deterministic policies are available.
    - Docker or PostgreSQL integration prerequisites are available for the selected bounded tests.
    - Shared Compose, bootstrap, and migration hunks have explicit ownership.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b02-local-data-lab
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S04
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Make the accepted B02 contracts real at the disposable PostgreSQL adapter
boundary. Complete deterministic profile generation, schema/grants, evidence
collection, migration lifecycle, Compose separation, and installation-scoped
reset behavior. Prove adapter parity and failure semantics without claiming
clean-host, browser, benchmark, whole-product recovery, or release readiness.

## Non-goals

- Do not implement product-domain tables or calculations.
- Do not run the full clean-host acceptance sequence reserved for S05.
- Do not implement whole-product backup/restore.
- Do not publish database ports broadly or weaken network separation.
- Do not change B01 product UI or first-run authorization.
- Do not use production data or credentials.

## Verified current context

- Fact: S01 provides versioned profile/manifest/error/lifecycle contracts.
- Fact: S02 provides deterministic validation and evidence-normalization
  policies.
- Fact: current Compose uses separate control/demo services, networks, volumes,
  and secrets.
- Fact: current reset logic verifies persisted project identity and Compose
  volume labels before deletion.
- Assumption: disposable integration runs may create exact stage-owned
  containers and volumes; verify explicit authorization and cleanup scope.
- Unknown/blocker: any migration beyond Foundation metadata requires the owning
  context and cannot be invented by B02.

## Context acquisition

Read accepted S02 evidence, then trace each port to its current adapter. Inspect
only the SQL, shell, migration, Compose, and tests involved in a failing or
changed contract. Record whether each observed behavior comes from static
configuration, a disposable PostgreSQL test, or a still-unverified clean-host
path.

## Requirements

### Must

- Keep control and demo-source PostgreSQL in distinct services, databases,
  credentials, volumes, and internal networks.
- Pin supported PostgreSQL image identity and record migration head.
- Create a least-privilege demo reader distinct from the database owner; prove
  allowed reads and denied writes/administration.
- Select only known profiles and require explicit large-data confirmation for
  benchmark.
- Generate identical smoke/demo rows and evidence for identical profile, seed,
  image, and schema versions.
- Ensure profile change on initialized data fails with reset guidance rather
  than silently mutating state.
- Keep all identifiers, UTC timestamps, currency, grains, keys, source
  namespaces, SCD cases, returns/cancellations, unknowns, calendar edges,
  promotions, and structural metric fixtures aligned with S01/S02.
- Collect evidence through a read-only, stable-order query and validate counts,
  KPIs, scenario keys/witnesses, schema version, and canonical hash.
- Prove clean empty-control migration upgrade and bounded downgrade/re-upgrade
  for Foundation metadata on disposable state.
- Prove migration failure never reports readiness and does not alter future
  context ownership.
- Prove reset refuses unsafe project names, absent/mismatched labels, foreign
  volumes, and non-demo targets.
- Add focused integration/recovery tests with exact cleanup.
- Preserve current golden output or version the manifest and explain every
  accepted change.

### Should

- Keep SQL generation set-based and deterministic.
- Make scripts fail fast with bounded waits and actionable safe errors.
- Use exact project names and labels rather than broad Docker discovery.

## Forbidden actions

- Do not run global prune, delete all volumes, or remove foreign containers.
- Do not print secret values or commit runtime environment files.
- Do not grant demo reader write, owner, superuser, or cross-database access.
- Do not combine control and demo schemas in one database.
- Do not mark benchmark accepted because its SQL path exists.
- Do not hide migration or golden drift by updating expected values without
  source and contract review.
- Do not infer commit, push, deploy, or release authority.

## Work plan and stop gates

1. Verify S02 acceptance, runtime prerequisites, shared-file ownership, and
   exact disposable cleanup scope.
2. Map each accepted port to SQL, shell, Compose, migration, and verifier
   adapters.
3. Implement the smallest adapter changes and focused negative paths.
4. Run schema/grant/profile/golden/migration/reset integration tests.
5. Run deterministic repeat and profile-mismatch checks.
6. Inspect logs/output for secret, host-path, and PII leakage.
7. Classify contract and migration impact; document rollback and cleanup.
8. Write S03 evidence, validate, then authorize only S04.

Stop if the Docker/PostgreSQL boundary is unavailable, cleanup cannot be proven
safe, expected golden output drifts without an approved contract change,
migration ownership is ambiguous, or secrets/real data are detected.

## Contracts and side effects

Authorized effects are limited to explicitly named disposable PostgreSQL
containers, databases, and installation-owned volumes created for S03.
Define:

- destination and exact project identity;
- credentials source without revealing values;
- bounded startup/migration/query timeouts;
- idempotency for empty initialization and explicit behavior on non-empty
  volumes;
- retryable versus terminal failures;
- unknown-state reconciliation after interrupted migration or reset;
- cleanup command and ownership verification;
- logs/audit/redaction;
- migration/downgrade behavior.

Classify every changed service name, network, volume, profile default, CLI,
schema, grant, migration, evidence query, and hash contract.

## Validation and evidence

- Local gates:
  - focused shell/static/SQL tests;
  - focused disposable PostgreSQL integration tests;
  - `uv run python -m tools.custometry_quality.validate_fixture_manifest`
  - `uv run python -m tools.custometry_quality.validate_migration_lifecycle`
  - `uv run python -m tools.custometry_quality.compose_lifecycle --help`
  - `uv run python -m tools.custometry_quality.check_ddd_boundaries`
  - `uv run python -m tools.custometry_quality.validate_staged_workstream`
- Real-boundary evidence: disposable PostgreSQL service, migrations, reader
  grants, deterministic seed/evidence, and reset refusal paths.
- Evidence location:
  `docs/architecture/workstreams/b02-local-data-lab-stage-reports/S03-adapters.md`.
- Explicit exclusions: clean host, persisted installation upgrade, browser,
  full benchmark, production network/firewall, backup/restore, and release.

## Acceptance criteria

- [ ] Control and demo databases remain independently isolated and healthy.
- [ ] Reader permissions are least-privilege and proven positive/negative.
- [ ] Smoke/demo generation is deterministic for repeated clean runs.
- [ ] Golden counts, KPIs, scenario witnesses, and SHA-256 match accepted
      manifests.
- [ ] Profile mismatch and benchmark confirmation fail closed.
- [ ] Foundation migration upgrade and bounded disposable downgrade/re-upgrade
      pass.
- [ ] Unsafe reset cases refuse deletion; exact owned reset succeeds in the
      bounded integration environment.
- [ ] No secret, real PII, foreign state, or ownership leak is present.
- [ ] Focused gates pass, S03 evidence is durable, and only S04 is authorized.

## Result and handoff

Write adapter evidence, exact commands, created runtime identities, cleanup,
contract impact, and ledger update in English. The Russian user report states
the actual PostgreSQL boundary proven, requirement IDs, changed files, checks,
golden hash, cleanup result, exclusions, residual risks, and exact S04 prompt.
Do not claim clean-host, browser, benchmark, recovery, or release readiness.
