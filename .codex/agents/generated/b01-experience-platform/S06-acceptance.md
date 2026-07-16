---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b01-s06-experience-platform-acceptance
scope: "Reconcile B01 requirements, contracts, browser evidence, documentation, rollback, and independent cold review, then complete the workstream only with no unresolved blocker."
spec_version: 0.8.2-draft
requirement_ids: [AC-028, AC-029, GAP-021, GAP-034, GAP-035, GAP-046, RISK-010, TEST-INV-022, TEST-INV-023, TEST-INV-042, TEST-INV-050, TEST-INV-051, UX-JOURNEY-001, UX-JOURNEY-002, UX-JOURNEY-006, V1-AC-007, V1-AC-017, V1-AC-018]
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
      why: cold review and validation requirements
    - path: docs/architecture/program/custometry-program-plan.md
      why: milestone, dependency, and acceptance authority
    - path: docs/architecture/workstreams/b01-experience-platform-plan.md
      why: B01 completion criteria and proof boundary
    - path: docs/architecture/development-runtime-contract.md
      why: final mode/evidence reconciliation and release isolation
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
      why: sole execution-state authority
  task_entrypoints:
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/S05-real-boundary-proof.md
      why: nearest accepted browser evidence and residual risks
    - path: docs/architecture/program/requirement-matrix.json
      why: exact B01 primary ownership and acceptance evidence
    - path: docs/architecture/documentation-platform.md
      why: final public/internal docs visibility boundary
  conditional_bundles:
    stage_evidence:
      read_when: reconciling stage exits and requirement evidence
      paths: [docs/architecture/workstreams/b01-experience-platform-stage-reports/S00-discovery.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/S01-ux-contract.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/S02-domain-application.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/S03-adapters.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/S04-web-integration.md]
    implementation_diff:
      read_when: reviewing final contract, browser, security, accessibility, or documentation risk
      paths: [apps/web/**, packages/contracts/**, B01-owned UI packages, docs-site/**]
skill_routing:
  - skill: architecture-review
    role: primary
    use_when: conducting the required independent cold review of architecture, contracts, evidence, and docs drift
  - skill: pre-ship-gate
    role: companion_or_terminal_reviewer
    use_when: assessing handoff readiness without publishing
  - skill: browser-qa-evidence
    role: companion
    use_when: determining whether final changes invalidate S05 browser proof
change_ownership:
  owned_paths: [docs/architecture/workstreams/b01-experience-platform-stage-reports/S06-acceptance.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md, narrowly scoped B01 acceptance fixes and documentation indexes]
  foreign_exclusions: [new product features, other workstream acceptance, program milestone changes without authority, Penpot mutation, commit, push, merge, deploy]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [docs/architecture/workstreams/b01-experience-platform-stage-reports/S06-acceptance.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md]
  possible_secondary_touches: [B01 plan/module, B01 implementation/tests/docs, architecture and docs indexes]
  expected_deletions: []
validation_strategy:
  depth: delivery
  acceptance_surfaces: [requirement traceability, stage evidence, contract impact, browser freshness, accessibility and localization, docs visibility, rollback, cold review, grouped gates]
  evidence_target: docs/architecture/workstreams/b01-experience-platform-stage-reports/S06-acceptance.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b01-workstream-acceptance
  exclusions: [other workstream acceptance, product_foundation closure, product release, production deployment, recovery, performance SLO, firewall/CNI, supply chain, canonical Penpot authority]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B01
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b01-experience-platform-plan.md
  prompt_pack_dir: .codex/agents/generated/b01-experience-platform
  stage_ledger: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
  stage_id: S06
  predecessor_gate:
    stage_id: S05
    allowed_statuses: [accepted, superseded]
  state_preconditions:
    - S05 is accepted or explicitly superseded in the ledger.
    - The ledger is active, current stage is S06, and only S06 has next_allowed true.
    - All S00-S05 reports and linked evidence exist and match the final relevant source state.
    - An independent cold reviewer is available, or an explicitly approved and labelled cold self-review fallback is allowed.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b01-experience-platform
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: null
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Decide whether B01 is genuinely complete. Reconcile every B01-primary
requirement with implementation and acceptance evidence, verify stage and
browser evidence freshness, contracts, accessibility, localization, route and
Help privacy, documentation visibility, rollback, file ownership, and release
contribution, then obtain an independent cold review. Complete the ledger only
when no required blocker remains.

## Non-goals

- Do not add new Experience Platform features.
- Do not accept another workstream, product foundation, or the full release.
- Do not use S06 to hide missing S05 browser evidence.
- Do not confirm or mutate Penpot.
- Do not commit, push, merge, deploy, or release.

## Verified current context

- Fact: S05 is the nearest real-browser evidence and must match the final
  browser-affecting state.
- Fact: the B01 module owns exactly its primary matrix requirements; the plan
  may reference contributors only for explicit verification.
- Fact: an independent cold review is required for architecture, plans, prompt
  packs, and final acceptance artifacts.
- Fact: B01 completion contributes to several milestones but terminates none.
- Fact: accepted B01 S05 evidence is Full Stack evidence, not Release
  acceptance; release remains outside B01.
- Assumption to verify: any S06-only documentation edit does not invalidate
  browser evidence; implementation or visible-copy changes do.

## Context acquisition

Read the ledger and S05 first. Inspect earlier stage reports only for the
requirement, contract, or risk being reconciled. Compare the final module,
plan, contracts, implementation, generated artifacts, tests, docs/help output,
and requirement matrix. Give the cold reviewer the accepted trio, all stage
reports, final diff, requirement allocation, exact evidence inventory, and
proof boundary without coaching toward a positive verdict.

## Requirements

### Must

- Verify S00–S05 are accepted or validly superseded with explicit replacement
  evidence.
- Verify the B01 module requirement IDs exactly equal all B01-primary matrix
  rows and the plan covers them without unrouted ownership.
- Map every B01-primary requirement to implementation evidence, acceptance
  evidence, milestone contribution, residual risk, and final disposition.
- Confirm route/workspace/query/history/guard/Focus identities and compatibility
  semantics remain stable and locale-neutral.
- Confirm system surfaces, Help, command search, route lists, logs, and browser
  evidence do not leak denied metadata or sensitive values.
- Confirm Frost tokens/components, compact density, sidebar behavior, motion,
  reduced motion, responsive/reflow, and loading/refresh semantics match
  accepted contracts.
- Confirm en/ru catalogs, formatting, fallback, and docs/help visibility are
  complete and local/offline.
- Confirm generated clients/mocks still derive from accepted schemas and mock
  mode cannot appear as real production readiness.
- Confirm accessibility evidence covers semantics, keyboard, focus,
  non-hover access, contrast/non-color meaning, 200% zoom/reflow, screen-reader
  smoke, and reduced motion; state any manual-audit residual honestly.
- Confirm final contract-impact classifications, migrations, defaults,
  deprecations, and rollback paths.
- Confirm S05 source/runtime identity still matches final browser-affecting
  state; rerun affected journeys if not.
- Confirm S00–S05 record the correct runtime mode, S05 includes clean Full
  Stack migration/readiness/network/restart/cleanup evidence, and no stage
  relabels Fast Loop or Hybrid evidence as Full Stack or Release.
- Run focused checks, canonical pyright targets, and the smallest applicable
  grouped local gate.
- Obtain independent cold review with verdict, blockers, fixed items,
  follow-up checks, and residual risks.
- Write S06 evidence and set the ledger to `completed`, `current_stage: null`,
  and no next-allowed stage only after all required blockers are resolved.

### Should

- Link durable evidence rather than duplicating browser traces.
- Keep the acceptance report readable while preserving exact requirement and
  command traceability.
- Record deferred downstream integrations as explicit consumer work, not B01
  defects when B01 contracts and mock boundaries are accepted.

## Forbidden actions

- Do not mark a requirement accepted without its required evidence class.
- Do not relabel screenshots, component tests, mocks, or source declarations as
  real browser or downstream-service proof.
- Do not change requirement ownership, dependencies, milestone gates, or
  expected evidence merely to satisfy validation.
- Do not let the author act as an unlabelled independent reviewer.
- Do not accept stale S05 evidence after a browser-visible change.
- Do not expose internal docs, plans, prompts, ledgers, secrets, or raw evidence
  through public `/docs` or `/help`.
- Do not stage or publish foreign changes.

## Work plan and stop gates

1. Verify S05 acceptance, final diff scope, and browser evidence freshness.
2. Reconcile stage status and every B01-primary requirement.
3. Review routes/identity, contracts, tokens/components, motion, locale,
   accessibility, docs/help, privacy, generated mocks, rollback, and milestone
   contribution, including mode and escalation evidence.
4. Run focused checks, canonical pyright targets, and grouped local gates.
5. Assign one terminal independent cold reviewer with complete bounded inputs.
6. Fix only in-scope blockers; rerun affected checks and browser journeys.
7. Write S06 report with verdict, fixed blockers, follow-up checks, and
   residual risks.
8. Complete the ledger only when no required blocker remains.

Stop with `blocked` if any requirement lacks evidence, S05 is stale, route or
metadata privacy is uncertain, accessibility or locale parity has a required
defect, generated artifacts drift, Full Stack lifecycle/restart/cleanup is
missing, a development override entered S05, public docs leak internal content,
cold review has an unresolved blocker, or foreign changes cannot be separated.

## Contracts and side effects

Acceptance work is limited to documentation, indexes, tests, and narrowly
scoped blocker fixes. A runtime or browser-visible fix invalidates affected S05
evidence until rerun. No external service, design tool, commit, publish,
deployment, or release side effect is authorized. The only staged state effect
is the final ledger transition.

## Validation and evidence

- Run all focused checks named by S01–S05 for changed surfaces.
- Run requirement-matrix generation/check, route, localization, docs/link,
  contract drift, DDD, staged-work, agent artifact, type, lint, and test gates.
- Run canonical pyright targets for the validator/tooling and B01 TypeScript
  typecheck targets; record exact commands rather than using a vague
  whole-repository claim.
- Run `uv run python -m tools.check --scope local` after focused fixes.
- Reuse S05 only when final changes cannot affect it; otherwise rerun the
  invalidated browser journeys and console/network checks.
- Write evidence to
  `docs/architecture/workstreams/b01-experience-platform-stage-reports/S06-acceptance.md`.
- Explicitly exclude product foundation, downstream business correctness,
  deployment, recovery, performance SLO, firewall/CNI, supply chain, Penpot,
  and final release.

## Acceptance criteria

- [ ] Every B01-primary requirement has correct implementation and acceptance
      evidence plus a final disposition.
- [ ] Module, plan, prompt, ledger, route, contract, localization, and docs
      metadata are synchronized.
- [ ] All stage gates are terminal and required evidence is present and fresh.
- [ ] Route/history/Focus, metadata privacy, tokens/components, motion,
      responsive density, i18n, accessibility, docs/help, and mock boundaries
      have no unresolved required defect.
- [ ] Contract impact, migration, deprecation, rollback, and milestone
      contribution are explicit.
- [ ] Runtime-mode evidence is correctly classified, S05 proves Full Stack,
      and B01 makes no Release-readiness claim.
- [ ] Final file manifest contains no unexplained or foreign changes.
- [ ] Focused checks, canonical pyright targets, and grouped local gates pass.
- [ ] Independent cold review has no unresolved blocker.
- [ ] S06 report records verdict, fixed blockers, follow-up checks, exclusions,
      and residual risks.
- [ ] Ledger is completed with no current or next-allowed stage.

## Result and handoff

Return status, cold-review verdict, requirement/evidence reconciliation,
contract impact, browser freshness decision, exact validation commands,
created/modified/deleted/outside-scope file manifest, fixed blockers, residual
risks, exclusions, and ledger completion. If blocked, keep B01 incomplete and
state the exact evidence or authority needed. If accepted, hand off only the
program owner for the next explicitly authorized workstream decision.
