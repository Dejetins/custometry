---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b02-s05-local-data-lab-real-boundary-proof
scope: "Produce fresh, reproducible B02 clean-install, PostgreSQL, migration, golden, restart, reset/reseed, isolation, and resource evidence on the supported local host."
spec_version: 0.8.2-draft
requirement_ids: [GAP-019, TEST-INV-009, TEST-INV-010, TEST-INV-011, TEST-INV-033, TEST-INV-040, AC-014, AC-016, AC-021]
language:
  implementation: en
  repository_artifacts: en
  agent_report: en
  user_completion_report: ru
context_sources:
  always_read:
    - path: AGENTS.md
      why: repository discovery and real-boundary evidence contract
    - path: .codex/AGENTS.md
      why: normative repository safety, proof, and reporting rules
    - path: docs/architecture/workstreams/b02-local-data-lab-plan.md
      why: B02 runtime acceptance, cleanup, and proof limits
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
      why: predecessor and current-stage authority
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S04-web-integration.md
      why: accepted adapter consumer and documentation state
  task_entrypoints:
    - path: deploy/compose/bootstrap.sh
      why: exact clean install, profile, URL, down, and reset lifecycle
      inspect_symbols: [usage, data-profile, allow-large-data, reset-demo-data, down]
    - path: compose.yaml
      why: target services, networks, volumes, health, resources, and image identities
      inspect_symbols: [control-db, demo-source-db, migrate, api, web, edge, networks, volumes]
    - path: tests/golden/retail-demo-manifest.json
      why: expected real demo counts, KPIs, scenarios, and evidence hash
      inspect_symbols: [profile, seed, expected_counts, expected_kpis, expected_evidence_sha256, scenarios]
  conditional_bundles:
    runtime_tools:
      read_when: selecting exact lifecycle and recovery commands
      paths: [tools/custometry_quality/compose_lifecycle.py, tools/custometry_quality/validate_migration_lifecycle.py, tools/custometry_quality/gate_performance.py, docs/runbooks/**]
    foundation_evidence:
      read_when: confirming supported host/toolchain/Docker prerequisites
      paths: [docs/architecture/workstreams/w00-repository-foundation.md, docs/architecture/workstreams/**foundation**]
  consult_if_needed:
    - path: custometry-technical-blueprint-ru.md
      read_when: runtime result conflicts with acceptance or benchmark requirements
skill_routing:
  - skill: backend-performance-evidence
    role: primary
    use_when: measuring reproducible generation/runtime resource behavior and preventing unsupported performance claims
  - skill: backend-quality-gates
    role: companion_or_terminal_reviewer
    use_when: verifying focused backend, database, migration, and runtime gates
change_ownership:
  owned_paths: [docs/architecture/workstreams/b02-local-data-lab-stage-reports/S05-real-boundary-proof.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md, stage-owned ignored runtime evidence]
  foreign_exclusions: [implementation changes except a separately diagnosed B02 defect, product-domain code, production deployment, whole-product backup/restore, firewall/CNI changes, Penpot, unrelated worktree changes]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [docs/architecture/workstreams/b02-local-data-lab-stage-reports/S05-real-boundary-proof.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md]
  possible_secondary_touches: [B02 implementation files only after a recorded root-cause defect and focused fix, docs/runbooks/**]
  expected_deletions: [stage-owned ignored runtime evidence after durable redacted summary is complete]
validation_strategy:
  depth: performance
  acceptance_surfaces: [clean Compose install, PostgreSQL separation, migration head, golden hash, restart, reset/reseed, negative isolation, resource envelope]
  evidence_target: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S05-real-boundary-proof.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b02-s05-supported-local-host-runtime
  exclusions: [production firewall/CNI, multi-host workers, whole-product backup/restore, downstream analytical correctness, production deployment, final release readiness]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B02
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b02-local-data-lab-plan.md
  prompt_pack_dir: .codex/agents/generated/b02-local-data-lab
  stage_ledger: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
  stage_id: S05
  predecessor_gate:
    stage_id: S04
    allowed_statuses: [accepted, superseded]
  state_preconditions:
    - S04 is accepted or explicitly superseded in the ledger.
    - The ledger status is active, current stage is S05, and only S05 has next_allowed true.
    - W00 supported-host and toolchain evidence remains valid.
    - Exactly one healthy Docker engine is reachable.
    - Runtime cleanup identity, disk budget, secrets location, and allowed profiles are confirmed.
    - Explicit large-data authority exists before any benchmark profile execution.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b02-local-data-lab
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S06
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Produce fresh real-boundary evidence that B02 works from a clean supported local
installation. Prove separate PostgreSQL services, migrations, deterministic
smoke/demo generation, accepted golden hash, restart/persistence, exact
reset/reseed, reader isolation, profile mismatch, unsupported remote topology,
and bounded resource behavior. Measure rather than infer. Run benchmark only
with explicit large-data authority and report its support status honestly.

## Non-goals

- Do not redesign or broadly refactor implementation during a proof stage.
- Do not run benchmark without explicit authorization, disk budget, and cleanup
  plan.
- Do not claim production firewall/CNI, multi-host, Kubernetes, or remote-worker
  support.
- Do not claim whole-product backup/restore or downstream analytics correctness.
- Do not deploy or publish.

## Verified current context

- Fact: S04 acceptance means contracts, deterministic core, adapters, and local
  docs/browser integration have passed their narrower boundaries.
- Fact: `AC-014` and `AC-016` require clean installation and stable golden
  behavior, not static declarations.
- Fact: the benchmark profile target is large and has no valid SLO before a
  comparable target-host baseline.
- Assumption: W00 provides a supported Apple Silicon M3 Pro Foundation baseline;
  verify current host, tool versions, and Docker engine before execution.
- Unknown/blocker: benchmark feasibility and target-host support remain unknown
  until measured with explicit authority.

## Context acquisition

Read the accepted S04 report and exact lifecycle commands. Inspect current
runtime state without exposing secret values. Record host architecture,
effective CPU/memory limits, Docker/Compose versions, image digests, project
name, ports, profile, seed, and disk budget. If the environment differs from
the supported W00 baseline, stop or classify the evidence as non-accepting.

## Requirements

### Must

- Start from no B02 installation-owned containers or volumes while preserving
  all foreign Docker state.
- Capture redacted host/tool/runtime identity and exact commands.
- Perform clean smoke installation, control migration, readiness, profile
  generation, and evidence verification.
- Prove control/demo databases use separate services, databases, credentials,
  volumes, and networks; verify no unintended host publication.
- Prove least-privilege demo reader can read accepted source tables and cannot
  write, create, alter, or administer.
- Perform clean demo installation and match accepted counts, KPIs, scenario
  witnesses, schema version, and evidence SHA-256.
- Repeat a clean demo generation and prove identical canonical evidence.
- Restart without reset and prove persistence plus unchanged evidence.
- Prove profile mismatch fails with safe reset guidance.
- Reset only the exact installation-owned demo volume, reseed, and reproduce
  the same golden evidence.
- Exercise migration upgrade and accepted recovery path on the real Compose
  boundary; clearly exclude whole-product backup/restore.
- Run negative egress/topology probes relevant to B02 and prove remote-worker
  configuration is rejected.
- Capture elapsed time, CPU/memory/disk observations, temp/evidence bytes, and
  cleanup result without making an unsupported SLO claim.
- If benchmark is authorized, measure generation/verification/cleanup with the
  blueprint counts and comparable method; otherwise record it as an explicit
  v1 milestone blocker, not a silent skip.
- Inspect logs and evidence for secrets, real PII, tokens, and host-path leaks.

### Should

- Use a scripted receipt with timestamps and command exit status.
- Capture before/after Docker and disk inventories for owned resources.
- Rerun the focused local gate after runtime proof to detect drift.

## Forbidden actions

- Do not use global Docker prune, broad volume deletion, or foreign project
  cleanup.
- Do not print or commit secret file contents or runtime environment values.
- Do not alter expected golden values to make a failed run pass.
- Do not reuse an existing dirty demo volume for clean-install evidence.
- Do not extrapolate performance from smoke/demo to benchmark.
- Do not report unavailable benchmark evidence as passed.
- Do not infer commit, push, merge, deploy, or release authority.

## Work plan and stop gates

1. Verify S04 acceptance, host prerequisites, Docker identity, authorization,
   disk budget, and exact cleanup scope.
2. Capture pre-run owned/foreign runtime inventory.
3. Run clean smoke lifecycle and migration/golden checks.
4. Run clean demo lifecycle, golden evidence, negative grants, and isolation.
5. Repeat clean demo, then restart/persist and profile-mismatch checks.
6. Perform exact reset/reseed/re-verification.
7. Run benchmark only if authorized; otherwise record the milestone blocker.
8. Capture resource, logs/redaction, and post-cleanup evidence.
9. Rerun focused gates and write the S05 report.
10. Update the ledger only after evidence review and authorize only S06.

Stop on an unknown Docker engine, insufficient disk, unsafe cleanup identity,
secret exposure, golden drift, migration ambiguity, foreign-state impact,
unbounded resource use, or unavailable required benchmark authority.

## Contracts and side effects

This stage has deliberate local effects:

- exact Compose project containers, networks, secrets references, and volumes;
- control/demo PostgreSQL data;
- migration and read-only verification queries;
- installation-scoped demo reset;
- stage-owned temporary evidence;
- optional benchmark data only with explicit authority.

Define timeouts, retry classes, interruption handling, unknown-state
reconciliation, cleanup, and redaction before each effect. A failed or
interrupted step must not trigger blind retry of reset or benchmark. Keep the
durable report free of secret values and raw sensitive payloads.

## Validation and evidence

- Local gates:
  - focused B02 unit, integration, migration, golden, and browser tests;
  - `uv run python -m tools.custometry_quality.validate_fixture_manifest`
  - `uv run python -m tools.custometry_quality.validate_migration_lifecycle`
  - the repository-approved Compose lifecycle command for clean runtime proof;
  - `uv run python -m tools.custometry_quality.gate_performance`
  - `uv run python -m tools.custometry_quality.validate_staged_workstream`
- Real-boundary evidence: clean smoke/demo Compose runs, PostgreSQL queries,
  migration head, reader-negative tests, golden hash, repeat run, restart,
  reset/reseed, topology/egress negatives, resource receipt, and exact cleanup.
- Evidence location:
  `docs/architecture/workstreams/b02-local-data-lab-stage-reports/S05-real-boundary-proof.md`.
- Explicit exclusions: production firewall/CNI, remote workers, Kubernetes,
  whole-product backup/restore, downstream analytical truth, deployment, final
  release readiness.

## Acceptance criteria

- [ ] Clean smoke and demo installations succeed on the supported host.
- [ ] Control/demo separation and reader least privilege are proven.
- [ ] Migration head and accepted recovery behavior are proven.
- [ ] Demo counts, KPIs, scenarios, and SHA-256 match on two clean runs.
- [ ] Restart preserves data and evidence.
- [ ] Profile mismatch fails closed; exact reset/reseed reproduces evidence.
- [ ] Foreign Docker state is unchanged and owned runtime state is cleaned or
      deliberately preserved with a recorded reason.
- [ ] Resource measurements are comparable and make no unsupported claim.
- [ ] Benchmark is either measured under explicit authority or recorded as a
      blocking milestone gap.
- [ ] Logs/evidence contain no secrets or real PII.
- [ ] S05 report is complete and the ledger authorizes only S06.

## Result and handoff

Write the redacted runtime receipt, measurements, hashes, cleanup, proof
boundary, and ledger update in English. The Russian completion report begins
with the real outcome, lists exact accepted and failed checks, golden hash,
benchmark status, resource evidence, exclusions, blockers, residual risks, and
the exact S06 prompt. Do not claim broader release readiness.
