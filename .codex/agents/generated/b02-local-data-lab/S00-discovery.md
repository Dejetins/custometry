---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b02-s00-local-data-lab-discovery
scope: "Freeze the B02 Local Data Lab facts, ownership, requirement routing, consumer needs, fixture coverage, and proof gaps without implementing or running the lab."
spec_version: 0.8.2-draft
requirement_ids: [AC-014, AC-016]
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
    - path: docs/architecture/program/custometry-program-plan.md
      why: canonical workstream dependencies and release milestones
    - path: docs/architecture/workstreams/b02-local-data-lab-plan.md
      why: accepted B02 staged scope
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
      why: sole current-stage authority
  task_entrypoints:
    - path: custometry-technical-blueprint-ru.md
      why: normative requirements and golden-dataset boundary
      inspect_symbols: [JOURNEY-001, GAP-019, TEST-INV-040, AC-014, AC-016, section 22.3, section 23.4]
    - path: docs/architecture/workstreams/b02-local-data-lab-module.md
      why: ownership, ports, invariants, and proof boundary
      inspect_symbols: [Identity and purpose, Invariants, Acceptance boundary]
    - path: compose.yaml
      why: declared control and demo-source runtime topology
      inspect_symbols: [control-db, demo-source-db, networks, volumes]
  conditional_bundles:
    current_fixture_sources:
      read_when: source inventory needs exact counts, seed, scenarios, migrations, reset, or evidence behavior
      paths: [deploy/demo-source/profiles/smoke.json, deploy/demo-source/profiles/demo.json, deploy/demo-source/profiles/benchmark.json, tests/golden/retail-demo-manifest.json, deploy/compose/bootstrap.sh, migrations/versions/0001_foundation_metadata.py]
    requirement_routing:
      read_when: primary or supporting ownership is unclear
      paths: [docs/architecture/program/requirement-matrix.json, docs/architecture/program/requirement-routing.json]
  consult_if_needed:
    - path: custometry-technical-blueprint-human-ru.md
      read_when: product meaning is ambiguous after the machine blueprint is inspected
skill_routing:
  - skill: architecture-design
    role: primary
    use_when: reviewing module boundaries, ownership, ports, and dependencies
  - skill: contract-impact-analysis
    role: companion_or_terminal_reviewer
    use_when: classifying current or proposed profile, schema, reset, migration, and evidence contracts
change_ownership:
  owned_paths: [docs/architecture/workstreams/b02-local-data-lab-module.md, docs/architecture/workstreams/b02-local-data-lab-plan.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S00-discovery.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md]
  foreign_exclusions: [runtime implementation, fixture data changes, migrations, Compose changes, B01 product UI, B03-B13 domain code, Penpot, unrelated worktree changes]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [docs/architecture/workstreams/b02-local-data-lab-stage-reports/S00-discovery.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md]
  possible_secondary_touches: [docs/architecture/workstreams/b02-local-data-lab-module.md, docs/architecture/workstreams/b02-local-data-lab-plan.md]
  expected_deletions: []
validation_strategy:
  depth: integration
  acceptance_surfaces: [architecture ownership, requirement routing, source inventory, contract classification, staged ledger]
  evidence_target: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S00-discovery.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b02-s00-source-anchored-discovery
  exclusions: [implementation, PostgreSQL runtime, Compose runtime, browser behavior, benchmark evidence, release readiness]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B02
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b02-local-data-lab-plan.md
  prompt_pack_dir: .codex/agents/generated/b02-local-data-lab
  stage_ledger: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
  stage_id: S00
  predecessor_gate:
    stage_id: null
    allowed_statuses: []
  state_preconditions:
    - W00 is accepted with reproducible toolchain and Foundation evidence.
    - The user has explicitly authorized B02 activation.
    - The ledger status is active, current stage is S00, and only S00 has next_allowed true.
    - .codex/PLANS.md registers B02 with this exact trio.
    - The worktree has been reviewed and all foreign changes are identified.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b02-local-data-lab
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S01
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Produce a cold, source-anchored B02 discovery report that freezes the Local
Data Lab boundary before implementation. Confirm the current profile, Compose,
PostgreSQL, migration, reset, golden-evidence, and consumer facts; reconcile
them with the requirement matrix; classify contract risks; and define the
smallest safe S01 input. This stage supports `AC-014` and `AC-016` but does not
claim either criterion is satisfied.

## Non-goals

- Do not edit runtime code, SQL, fixtures, migrations, Compose, CI, or product
  UI.
- Do not start Docker, PostgreSQL, the Web application, or the benchmark
  profile.
- Do not accept current manifests or scripts as runtime evidence.
- Do not assign product-domain ownership to B02.
- Do not activate S01 automatically.

## Verified current context

- Fact: B02 has hard dependency `W00` and soft coordination dependency `B01`.
- Fact: the repository declares separate `control-db` and `demo-source-db`
  services and current `smoke`, `demo`, and `benchmark` profiles.
- Fact: the demo manifest commits deterministic counts, KPIs, scenarios, and an
  evidence SHA-256.
- Fact: the current benchmark manifest is marked implemented but unverified.
- Assumption: no B02 stage report is accepted when this prompt starts; verify
  this from the ledger before proceeding.
- Unknown/blocker: the exact accepted B02 primary and supporting requirement
  rows must be taken from the generated requirement matrix, not inferred from
  the prompt.

## Context acquisition

Read the frontmatter sources in order. Limit initial inspection to the listed
files and at most eight additional files. Expand only when a source fact,
consumer, ownership boundary, or contract classification cannot be resolved.
Record facts, proposals, assumptions, and unknowns separately. If the program
plan, requirement matrix, plan, prompt, and ledger disagree, stop and report
the conflict instead of choosing an authority silently.

## Requirements

### Must

- Reconcile every B02 plan requirement with the canonical routing row,
  disposition, milestone, and expected acceptance evidence.
- Inventory exact existing profile files, seeds, row targets, status flags,
  golden counts, golden KPIs, scenario witnesses, and evidence-normalization
  behavior.
- Inventory control/demo database separation, credentials, grants, networks,
  volumes, published ports, health checks, image pins, resource limits, and
  migration wiring.
- Inventory reset authorization and refusal paths, including project-name and
  Compose-label checks.
- Identify all current and planned consumers across B01 and B03–B13 without
  moving their domain ownership into B02.
- Compare current fixture scenarios with the blueprint golden-dataset list and
  classify each item as present, partial, absent, or consumer-defined later.
- Classify profile, relational schema, golden manifest, evidence hash, reset
  CLI, migration, Compose, docs, and benchmark surfaces as `none`,
  `compatible-change`, `breaking-change`, or `unknown`.
- Define exact S01 decisions, owned paths, foreign exclusions, stop gates, and
  evidence.
- Write `S00-discovery.md` in English and update the ledger only after checks.

### Should

- Prefer tables for coverage, ownership, and contract impact.
- Link exact source paths and requirement IDs.
- Preserve the module definition unless discovery proves a material error.

## Forbidden actions

- Do not modify generated requirement routing to make B02 appear complete.
- Do not normalize a dirty worktree by discarding, stashing, or committing
  foreign changes.
- Do not add dependencies, services, or schemas.
- Do not read or expose local secrets, database password files, tokens, or real
  customer data.
- Do not infer commit, push, merge, deploy, or runtime authority.

## Work plan and stop gates

1. Verify activation, exact trio, branch, dependency, and worktree ownership.
2. Reconcile B02 IDs against the program requirement matrix.
3. Build the source inventory and fixture-coverage matrix.
4. Build the consumer/ownership map and dependency-direction review.
5. Build the contract-impact and proof-gap matrix.
6. Define the exact S01 decisions, file manifest, evidence, and blockers.
7. Run focused staged/docs/link checks.
8. Write the S00 report, then mark S00 accepted and authorize only S01 if every
   exit criterion passes.

Stop with `blocked` if W00 is not accepted, B02 is not active, routing is
inconsistent, a shared-file owner cannot be established, real data or secrets
are present, or the fixture boundary conflicts with a product context.

## Contracts and side effects

This stage is documentation-only. Repository writes are limited to the B02
module/plan/report/ledger paths. Classify all future contract dimensions, but
do not change them. There are no external effects, service calls, migrations,
database writes, retries, or cleanup. The ledger update is the only staged
state transition and must remain auditable.

## Validation and evidence

- Local gates:
  - `uv run python -m tools.custometry_quality.validate_staged_workstream`
  - `uv run python -m tools.custometry_quality.check_docs_links`
  - `uv run python -m tools.custometry_quality.generate_program_requirement_matrix --check`
- Real-boundary evidence: none in S00.
- Evidence location:
  `docs/architecture/workstreams/b02-local-data-lab-stage-reports/S00-discovery.md`.
- Explicit exclusions: PostgreSQL, Docker, migrations, reset, golden output,
  browser, performance, recovery, and release readiness remain unverified.

## Acceptance criteria

- [ ] B02 activation and W00 acceptance are proven from current artifacts.
- [ ] Requirement routing contains no unexplained B02 ID drift.
- [ ] Current fixture/runtime facts are source-linked and separated from
      proposals and unknowns.
- [ ] Current and missing golden scenarios are classified.
- [ ] Control/demo separation, migration, reset, and benchmark risks are
      explicit.
- [ ] Consumer ownership and foreign exclusions are unambiguous.
- [ ] Contract classifications and S01 stop gates are complete.
- [ ] The S00 report passes focused staged/docs checks.
- [ ] The ledger is updated after validation and permits only S01.

## Result and handoff

Write the durable report and ledger update in English. Report to the user in
Russian with outcome, requirement IDs, changed files, review mode, actual
checks, proof exclusions, blockers, residual risks, and the exact next
ledger-authorized prompt. Do not claim implementation or runtime readiness.
