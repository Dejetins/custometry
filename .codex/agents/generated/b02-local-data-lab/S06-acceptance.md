---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b02-s06-local-data-lab-acceptance
scope: "Perform final B02 traceability, documentation, rollback, cold independent review, and workstream acceptance without expanding the proof boundary."
spec_version: 0.8.2-draft
requirement_ids: [JOURNEY-001, GAP-019, AC-014, AC-016, AC-021, AC-022]
language:
  implementation: en
  repository_artifacts: en
  agent_report: en
  user_completion_report: ru
context_sources:
  always_read:
    - path: AGENTS.md
      why: repository acceptance and reporting contract
    - path: .codex/AGENTS.md
      why: normative validation, cold review, and proof boundaries
    - path: docs/architecture/program/custometry-program-plan.md
      why: dependency and milestone acceptance authority
    - path: docs/architecture/workstreams/b02-local-data-lab-plan.md
      why: B02 completion rule
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
      why: sole stage and evidence state authority
  task_entrypoints:
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S05-real-boundary-proof.md
      why: nearest accepted runtime evidence and remaining blockers
      inspect_symbols: [outcome, evidence, benchmark, cleanup, exclusions, residual risks]
    - path: docs/architecture/program/requirement-matrix.json
      why: exact B02 primary/supporting traceability and evidence contract
      inspect_symbols: [B02, AC-016]
    - path: docs/architecture/documentation-platform.md
      why: public/internal documentation visibility boundary
      inspect_symbols: [visibility, public, internal, local docs]
  conditional_bundles:
    stage_evidence:
      read_when: verifying every exit criterion and contract transition
      paths: [docs/architecture/workstreams/b02-local-data-lab-stage-reports/S00-discovery.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S01-ux-contract.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S02-domain-application.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S03-adapters.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S04-web-integration.md]
    implementation_diff:
      read_when: reviewing final ownership, compatibility, security, migration, or runtime risk
      paths: [deploy/demo-source/**, tests/golden/**, docs/contracts/data-lab/**, tools/custometry_quality/data_lab/**, compose.yaml, deploy/compose/bootstrap.sh, migrations/**]
  consult_if_needed:
    - path: custometry-technical-blueprint-ru.md
      read_when: a traceability or acceptance interpretation is disputed
skill_routing:
  - skill: architecture-review
    role: primary
    use_when: performing the required cold independent architecture, contract, evidence, and docs-drift review
  - skill: pre-ship-gate
    role: companion_or_terminal_reviewer
    use_when: determining whether B02 can be handed off as accepted without publishing
change_ownership:
  owned_paths: [docs/architecture/workstreams/b02-local-data-lab-stage-reports/S06-acceptance.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md, docs/architecture/workstreams/b02-local-data-lab-plan.md, docs/architecture/workstreams/b02-local-data-lab-module.md, B02 documentation and index entries]
  foreign_exclusions: [new product features, unrelated implementation refactors, other workstream ledgers, program milestone changes without authority, commit/push/deploy, Penpot, unrelated worktree changes]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [docs/architecture/workstreams/b02-local-data-lab-stage-reports/S06-acceptance.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md]
  possible_secondary_touches: [docs/architecture/workstreams/b02-local-data-lab-plan.md, docs/architecture/workstreams/b02-local-data-lab-module.md, B02 documentation and index entries]
  expected_deletions: []
validation_strategy:
  depth: delivery
  acceptance_surfaces: [requirement traceability, stage evidence, contract impact, migrations, rollback, docs visibility, cold review, grouped gates]
  evidence_target: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S06-acceptance.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b02-workstream-acceptance
  exclusions: [other workstream acceptance, product release, production deployment, production firewall/CNI, downstream analytical correctness]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B02
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b02-local-data-lab-plan.md
  prompt_pack_dir: .codex/agents/generated/b02-local-data-lab
  stage_ledger: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
  stage_id: S06
  predecessor_gate:
    stage_id: S05
    allowed_statuses: [accepted, superseded]
  state_preconditions:
    - S05 is accepted or explicitly superseded in the ledger.
    - The ledger status is active, current stage is S06, and only S06 has next_allowed true.
    - All S00-S05 reports and linked evidence exist.
    - Required runtime evidence is fresh for the accepted code and contract state.
    - An independent cold reviewer is available, or an explicitly labelled cold self-review fallback is approved.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b02-local-data-lab
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: null
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Decide whether B02 is genuinely complete. Reconcile every routed requirement
with durable stage and real-boundary evidence, verify final contract impact,
migrations, rollback, security, privacy, documentation visibility, file
ownership, and milestone implications, then obtain an independent cold review.
Fix only acceptance blockers within B02 scope, rerun affected checks, and mark
the ledger completed only when no required blocker remains.

## Non-goals

- Do not add new fixture capabilities or product features.
- Do not broaden runtime proof beyond the B02 plan.
- Do not accept another workstream or the full product.
- Do not commit, push, merge, deploy, or release.
- Do not hide a missing benchmark or clean-host proof behind documentation.

## Verified current context

- Fact: S05 is the nearest real-boundary evidence and must match the final
  accepted implementation state.
- Fact: all B02 primary and supporting requirement rows are defined by the
  canonical requirement matrix.
- Fact: cold independent review is required for plans, prompt packs,
  architecture, and acceptance artifacts.
- Assumption: any post-S05 acceptance-only edit does not invalidate runtime
  evidence; prove this by scope or rerun the affected boundary.
- Unknown/blocker: B02 cannot complete a milestone that requires benchmark
  evidence if S05 records benchmark as unverified.

## Context acquisition

Read the ledger and S05 first, then inspect each earlier report only for the
requirement or risk being reconciled. Review the final diff and generated
indexes. Give the independent reviewer the plan, module, stage reports, ledger,
requirement rows, final diff, and proof boundary without coaching toward a
positive verdict.

## Requirements

### Must

- Verify every S00–S05 predecessor is accepted or explicitly superseded with a
  valid replacement.
- Map every B02 plan requirement to implementation and acceptance evidence,
  expected milestone, residual risk, and disposition.
- Confirm `AC-016` has fresh clean-install golden evidence for accepted
  profiles and exact hash identity.
- Confirm `AC-014` evidence is limited to the B02 clean-install subset and does
  not overclaim full product deployment.
- Confirm source namespace, SCD, currency, grain, metric-shape, promotion, and
  calendar fixtures remain inputs rather than false downstream correctness
  claims.
- Confirm control/demo ownership, least-privilege grants, secrets, synthetic
  PII, reset, migrations, rollback, and cleanup are safe.
- Confirm benchmark status and milestone consequences explicitly.
- Confirm local/public documentation visibility excludes internal architecture,
  prompts, ledgers, secrets, and raw evidence.
- Verify final contract-impact classifications and migration compatibility.
- Run the smallest applicable grouped gates plus all checks affected by any
  acceptance fix.
- Obtain independent cold review with verdict, blockers, fixed items,
  follow-up check, and residual risks.
- Write S06 evidence and set the ledger to `completed`, `current_stage: null`,
  and no next-allowed stage only after every required blocker is resolved.

### Should

- Keep the acceptance report concise but fully traceable.
- Link evidence rather than duplicating large runtime receipts.
- Record deferred or non-goal rows explicitly so they cannot be mistaken for
  omissions.

## Forbidden actions

- Do not mark a missing required proof as accepted.
- Do not change expected values, routes, dependencies, or milestones only to
  satisfy validators.
- Do not rely on screenshots, unit tests, static Compose config, or source
  declarations as substitutes for S05 runtime evidence.
- Do not let the author serve as an unlabelled independent reviewer.
- Do not stage or publish foreign changes.
- Do not infer commit, push, merge, deploy, or release authority.

## Work plan and stop gates

1. Verify S05 acceptance, final diff scope, and evidence freshness.
2. Reconcile stage statuses and every requirement-matrix row.
3. Review contracts, migrations, reset/rollback, security/privacy, docs
   visibility, benchmark, and milestone implications.
4. Run focused and grouped applicable gates.
5. Spawn or assign a cold independent reviewer with complete bounded inputs.
6. Fix only in-scope blockers; rerun affected checks and, if necessary, the
   invalidated real boundary.
7. Write the S06 report with verdict and residual risks.
8. Complete the ledger only when no required blocker remains.

Stop with `blocked` if any required evidence is absent/stale, a requirement has
no disposition, benchmark blocks a claimed milestone, cold review finds an
unresolved blocker, docs leak internal/sensitive content, or the final diff
contains foreign changes.

## Contracts and side effects

Acceptance edits are documentation, index, test, or narrowly scoped blocker
fixes only. Any implementation fix is classified and reviewed; if it affects
runtime behavior, S05 evidence is stale until rerun. There are no authorized
external effects beyond read-only review and local validation. Ledger
completion is the sole staged state transition.

## Validation and evidence

- Local gates:
  - all focused checks named by S01–S05 for changed surfaces;
  - `uv run python -m tools.custometry_quality.generate_program_requirement_matrix --check`
  - `uv run python -m tools.custometry_quality.generate_docs_index --check`
  - `uv run python -m tools.custometry_quality.check_contract_drift`
  - `uv run python -m tools.custometry_quality.check_ddd_boundaries`
  - `uv run python -m tools.custometry_quality.validate_staged_workstream`
  - `uv run python -m tools.check --scope local`
- Real-boundary evidence: reuse S05 only when final changes cannot affect it;
  otherwise rerun the affected runtime proof.
- Evidence location:
  `docs/architecture/workstreams/b02-local-data-lab-stage-reports/S06-acceptance.md`.
- Explicit exclusions: other workstreams, product release, production deploy,
  production firewall/CNI, remote workers, and downstream analytical truth.

## Acceptance criteria

- [ ] Every B02 requirement row has a correct disposition and linked evidence.
- [ ] All stage gates are terminal and no evidence is missing or stale.
- [ ] Clean-install golden, database separation, grants, migrations, reset,
      repeatability, restart, and cleanup evidence is accepted.
- [ ] Benchmark status and release-milestone impact are explicit.
- [ ] Contract impact, migration, rollback, security/privacy, and docs
      visibility are complete.
- [ ] Final file manifest contains no foreign or unexplained changes.
- [ ] Focused and grouped gates pass.
- [ ] Independent cold review has no unresolved blocker.
- [ ] S06 report records verdict, fixed blockers, follow-up checks, and residual
      risks.
- [ ] Ledger is completed with no current or next-allowed stage.

## Result and handoff

Write the acceptance report and final ledger transition in English. The Russian
user report leads with `complete` or `blocked`, states requirement and milestone
status, independent-review mode/verdict, fixed blockers, actual checks and
runtime evidence, changed files, proof exclusions, residual risks, and the
program owner who may consider the next workstream. Do not claim full-product
release readiness.
