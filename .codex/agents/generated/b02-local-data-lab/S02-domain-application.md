---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b02-s02-local-data-lab-domain-application
scope: "Implement and prove the deterministic, framework-independent Local Data Lab policy core and fixture semantics defined by S01."
spec_version: 0.8.2-draft
requirement_ids: [TEST-INV-009, TEST-INV-010, TEST-INV-011, TEST-INV-012, TEST-INV-013, TEST-INV-016, TEST-INV-026, TEST-INV-028, TEST-INV-031, TEST-INV-033, AC-021, AC-022]
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
      why: B02 implementation and proof boundary
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
      why: predecessor and current-stage authority
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S01-ux-contract.md
      why: accepted schemas, compatibility, and failure semantics
  task_entrypoints:
    - path: custometry-technical-blueprint-ru.md
      why: normative data and test invariants represented by fixture semantics
      inspect_symbols: [TEST-INV-009, TEST-INV-010, TEST-INV-011, TEST-INV-012, TEST-INV-013, TEST-INV-016, TEST-INV-026, TEST-INV-028, TEST-INV-031, TEST-INV-033, AC-021, AC-022]
    - path: docs/architecture/workstreams/b02-local-data-lab-module.md
      why: pure model, invariants, commands, and ports
      inspect_symbols: [State and contract model, Invariants, Commands queries and events]
    - path: tests/golden/verify_retail_demo.py
      why: current canonical evidence verification behavior
      inspect_symbols: [canonical_digest, main]
  conditional_bundles:
    accepted_schemas:
      read_when: implementing profile, manifest, evidence, or error models
      paths: [docs/contracts/data-lab/**]
    current_fixture_inputs:
      read_when: preserving current profile and scenario behavior
      paths: [deploy/demo-source/profiles/*.json, tests/golden/retail-demo-manifest.json, tests/golden/retail-demo-evidence.sql]
  consult_if_needed:
    - path: docs/architecture/bounded-context-map.md
      read_when: a proposed implementation path could violate DDD ownership
skill_routing:
  - skill: architecture-design
    role: primary
    use_when: preserving dependency direction and framework-independent policies
  - skill: backend-quality-gates
    role: companion_or_terminal_reviewer
    use_when: running focused Python and fixture tests and classifying failures
change_ownership:
  owned_paths: [tools/custometry_quality/validate_fixture_manifest.py, tools/custometry_quality/data_lab/**, tests/unit/data_lab/**, tests/tooling/test_fixture_manifest*.py, deploy/demo-source/profiles/*.json, tests/golden/retail-demo-manifest.json, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S02-domain-application.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md]
  foreign_exclusions: [PostgreSQL adapter scripts, Compose, migrations, product-domain packages, Web UI, production data, Penpot, unrelated worktree changes]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [tools/custometry_quality/data_lab/**, tests/unit/data_lab/**, tests/tooling/test_fixture_manifest*.py, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S02-domain-application.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md]
  possible_secondary_touches: [tools/custometry_quality/validate_fixture_manifest.py, deploy/demo-source/profiles/*.json, tests/golden/retail-demo-manifest.json]
  expected_deletions: []
validation_strategy:
  depth: integration
  acceptance_surfaces: [profile parsing, deterministic policies, canonical evidence, fixture semantics, negative invariants]
  evidence_target: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S02-domain-application.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b02-s02-deterministic-policy-core
  exclusions: [PostgreSQL execution, Compose lifecycle, migration execution, browser behavior, benchmark target-host evidence, release readiness]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B02
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b02-local-data-lab-plan.md
  prompt_pack_dir: .codex/agents/generated/b02-local-data-lab
  stage_ledger: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
  stage_id: S02
  predecessor_gate:
    stage_id: S01
    allowed_statuses: [accepted, superseded]
  state_preconditions:
    - S01 is accepted or explicitly superseded in the ledger.
    - The ledger status is active, current stage is S02, and only S02 has next_allowed true.
    - S01 schemas, examples, compatibility rules, and errors are stable.
    - No runtime adapter or shared product-context change is required for the pure core.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b02-local-data-lab
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S03
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Implement the smallest framework-independent B02 policy core that validates
profiles and manifests, normalizes golden evidence, enforces deterministic
inputs, represents reset/migration decisions without performing them, and
proves the fixture semantics required by the accepted S01 contract. Provide
direct tests for source namespaces, SCD intervals, time/currency/grain rules,
calendar edges, extraction-failure inputs, promotion overlap, and structural
metric shapes without implementing downstream business calculations.

## Non-goals

- Do not connect to PostgreSQL or Docker.
- Do not edit Compose, migration runners, shell lifecycle, or product Web code.
- Do not implement ingestion, semantic modeling, analytics, forecasting,
  promotions, or report behavior.
- Do not generate the full benchmark dataset.
- Do not accept SQL scripts or current manifest output as integration proof.

## Verified current context

- Fact: S01 defines the accepted profile, manifest, canonical evidence, error,
  reset, migration, and consumer contracts.
- Fact: B02 is infrastructure and must not import product-domain packages.
- Fact: current verification canonicalizes JSON with sorted keys and compact
  separators before SHA-256.
- Assumption: pure policy code may live under
  `tools/custometry_quality/data_lab/` because B02 is a contributor/runtime
  fixture module, not a product bounded context; confirm the S01 file manifest.
- Unknown/blocker: any fixture that requires a new business definition must be
  delegated to the owning workstream rather than invented here.

## Context acquisition

Read accepted S01 evidence and schemas first. Inspect only the existing verifier
and profile/manifest inputs required for parity. Use the blueprint requirement
IDs to construct tests, not to import the complete product specification into
code comments. Stop when implementing a fixture requires an unresolved metric,
identity, calendar, or promotion policy.

## Requirements

### Must

- Parse and validate each profile against the accepted schema with
  deterministic, locale-neutral error codes.
- Reject unknown profiles, schema drift, invalid counts, invalid seed, invalid
  status, inconsistent opt-in flags, and benchmark without explicit
  confirmation.
- Parse and validate fixture manifests, grains, keys, timezone, currency,
  synthetic PII classes, expected counts/KPIs/scenarios, and SHA-256 format.
- Canonicalize evidence deterministically and prove byte/hash stability under
  dictionary insertion-order differences and repeated runs.
- Make randomness, current time, timezone, locale, and currency explicit
  inputs; no ambient clock or random seed is allowed.
- Add direct fixture-policy tests for source-namespace collisions, SCD overlap
  and gap witnesses, leap day, ISO week 53, incomplete periods, multiple
  currencies, anonymous/returned/cancelled receipts, missing products, header
  versus item grain, canonical customer and period-key inputs, overlapping
  promotions, multi-channel promotions, and immutable audience inputs.
- Represent failed/aborted multi-table extraction and watermark/session
  scenarios as inputs for B05 without claiming ingestion behavior.
- Represent additive, semi-additive, distinct, and ratio test shapes without
  calculating domain metrics owned by B06/B07.
- Preserve current accepted demo evidence or intentionally version the contract
  and document migration.
- Keep tests deterministic across supported Python versions and CPU counts.

### Should

- Use immutable dataclasses or equivalent explicit value objects.
- Keep validation and normalization pure and separately testable.
- Prefer parameterized/property tests for invalid boundaries and repeatability.

## Forbidden actions

- Do not use real emails, names, loyalty cards, customer exports, or secrets.
- Do not rely on Python hash randomization, filesystem enumeration order,
  current locale, current time, or database default ordering.
- Do not silently coerce unknown values to zero or false.
- Do not merge duplicate source IDs without source namespace.
- Do not accept overlapping SCD intervals as a valid canonical join case.
- Do not claim downstream invariants pass because the fixture exists.
- Do not add a dependency without explicit need and repository approval.

## Work plan and stop gates

1. Verify S01 acceptance and exact owned paths.
2. Implement profile/manifest/evidence value objects and validators.
3. Implement canonical serialization and deterministic hash calculation.
4. Add deterministic scenario descriptors and direct witnesses.
5. Add positive, negative, repeatability, and compatibility tests.
6. Compare actual demo manifest/hash behavior and classify any drift.
7. Run focused lint, type, and test gates; inspect failures by ownership.
8. Write the S02 report, then update the ledger and authorize only S03.

Stop if accepted schemas are incomplete, deterministic behavior cannot be
proven, a business policy is missing, current golden data would require a
silent breaking change, or a shared file cannot be edited safely.

## Contracts and side effects

This stage changes internal Python and fixture contracts only. It performs no
database, network, Docker, filesystem-deletion, or external side effect.
Classify changes to:

- Python validation APIs and error codes;
- JSON profile/manifest compatibility;
- evidence canonicalization and hash identity;
- scenario identifiers and meanings;
- test fixture paths and import boundaries;
- logs and exception redaction.

Persisted or public contract changes require an explicit version and migration
note. Pure code must not import FastAPI, SQLAlchemy, Docker SDK, or product
domain modules.

## Validation and evidence

- Local gates:
  - focused profile/manifest/evidence unit and property tests;
  - `uv run ruff check tools/custometry_quality tests/unit/data_lab tests/tooling`
  - `uv run pyright`
  - `uv run pytest -q tests/unit/data_lab tests/tooling/test_fixture_manifest.py`
  - `uv run python -m tools.custometry_quality.validate_fixture_manifest`
  - `uv run python -m tools.custometry_quality.check_ddd_boundaries`
  - `uv run python -m tools.custometry_quality.validate_staged_workstream`
- Real-boundary evidence: deterministic repeated process execution may be used
  for canonical-byte proof, but no PostgreSQL or Docker claim is allowed.
- Evidence location:
  `docs/architecture/workstreams/b02-local-data-lab-stage-reports/S02-domain-application.md`.
- Explicit exclusions: SQL generation, PostgreSQL grants, migrations, reset,
  Compose, browser, performance, and release readiness.

## Acceptance criteria

- [ ] Accepted profiles and manifests validate; required invalid variants fail
      with stable locale-neutral codes.
- [ ] Repeated canonical evidence is byte-identical and hash-identical.
- [ ] Ambient randomness, clock, locale, timezone, and ordering are absent.
- [ ] Required structural edge scenarios have direct tests and witnesses.
- [ ] Source namespace and SCD rules are preserved.
- [ ] Multi-currency and structural metric fixtures do not invent downstream
      metric truth.
- [ ] DDD boundaries, lint, types, and focused tests pass.
- [ ] Contract impact and proof exclusions are complete.
- [ ] The S02 report is durable and the ledger authorizes only S03.

## Result and handoff

Write implementation evidence, file manifest, contract classifications, and the
ledger update in English. The Russian user report names the implemented policy
core, requirement IDs, actual gates, any golden drift, proof exclusions,
residual risks, and the exact S03 prompt. Do not claim database or runtime
readiness.
