---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b01-s03-experience-platform-adapters
scope: "Implement generated and local B01 adapters for routing, browser history, preferences, localization, docs/help, assets, system errors, and contract-backed mock services."
spec_version: 0.8.2-draft
requirement_ids: [AC-028, AC-029, HELP-001, HELP-002, HELP-003, HELP-004, I18N-001, I18N-002, I18N-003, I18N-004, I18N-005, I18N-006, I18N-007, I18N-008, I18N-009, I18N-010, I18N-011, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, THEME-001, THEME-002, THEME-003, THEME-004, THEME-005, THEME-006, THEME-007, THEME-008]
language:
  implementation: en
  repository_artifacts: en
  user_completion_report: ru
context_sources:
  always_read:
    - path: AGENTS.md
      why: repository and Git discipline
    - path: .codex/AGENTS.md
      why: adapter, validation, and proof rules
    - path: docs/architecture/workstreams/b01-experience-platform-plan.md
      why: scope and adapter proof boundary
    - path: docs/architecture/development-runtime-contract.md
      why: Fast Loop versus Hybrid adapter boundary and release isolation
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
      why: sole execution-state authority
    - path: docs/architecture/workstreams/b01-experience-platform-stage-reports/S02-domain-application.md
      why: accepted ports, policies, and remaining adapter work
  task_entrypoints:
    - path: packages/contracts
      why: generated-client and mock authority
    - path: apps/web
      why: adapter and composition entrypoints
    - path: docs-site
      why: local docs and Help delivery
    - path: docs/architecture/documentation-platform.md
      why: visibility and offline rules
skill_routing:
  - skill: architecture-design
    role: primary
    use_when: keeping adapters outside policy core and reconciling trust boundaries
  - skill: contract-impact-analysis
    role: companion
    use_when: adapter reality exposes schema or default drift
  - skill: backend-quality-gates
    role: companion
    use_when: Python generators or validators are touched
change_ownership:
  owned_paths: [B01 adapters and generated-client/mock tooling identified by S01/S02, docs-site B01 integration, B01 adapter tests, docs/architecture/workstreams/b01-experience-platform-stage-reports/S03-adapters.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md]
  foreign_exclusions: [downstream service implementations, business persistence, production notification or email, Penpot, other ledgers, commit and deployment]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [B01 adapter and generator sources/tests, docs/architecture/workstreams/b01-experience-platform-stage-reports/S03-adapters.md, docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md]
  possible_secondary_touches: [accepted B01 schemas/examples, docs/help metadata, generated indexes]
  expected_deletions: []
validation_strategy:
  depth: integration
  acceptance_surfaces: [generated client/mock parity, router/history integration, local docs/help build, localization bundle, storage and error mapping, offline asset checks]
  evidence_target: docs/architecture/workstreams/b01-experience-platform-stage-reports/S03-adapters.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b01-adapter-integration
  exclusions: [composed production UI, complete browser journeys, real downstream services, canonical Penpot authority, deployment and release]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B01
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b01-experience-platform-plan.md
  prompt_pack_dir: .codex/agents/generated/b01-experience-platform
  stage_ledger: docs/architecture/workstreams/b01-experience-platform-stage-reports/b01-experience-platform-stage-ledger.md
  stage_id: S03
  predecessor_gate:
    stage_id: S02
    allowed_statuses: [accepted, superseded]
  state_preconditions:
    - S02 is accepted or explicitly superseded in the ledger.
    - The ledger is active, current stage is S03, and only S03 has next_allowed true.
    - Application ports and focused invariant tests are stable.
    - Generated artifacts can be reproduced from accepted schemas without manual edits.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b01-experience-platform
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S04
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Implement the B01 adapters that connect accepted policy/application ports to
the router and browser history, local preference persistence and API seams,
localization bundles and formatters, docs/help indexes, offline assets, safe
system-error mapping, and generated contract-backed mock services. Prove
generation, parity, failure, and visibility behavior before composing the full
Web experience.

## Non-goals

- Do not build full page layouts or accept browser journeys.
- Do not create real B03–B13 service behavior.
- Do not use a mock server as authorization, business truth, or release proof.
- Do not start or invent Hybrid infrastructure when no accepted real adapter
  requires it; record the deferral instead.
- Do not add remote runtime dependencies, fonts, icons, analytics scripts, or
  CDN assets.
- Do not mutate Penpot.

## Verified current context

- Fact: S02 provides tested framework-independent ports and policies.
- Fact: S01 schemas and examples are the source for clients and mocks.
- Fact: local `/docs` and `/help` must obey visibility and offline delivery
  boundaries.
- Fact: browser storage may hold safe preferences but never authorization,
  secrets, PII, execution truth, or durable analytical results.
- Fact: raw backend errors and denied metadata must not reach system surfaces,
  command search, route lists, Help, logs, or telemetry.
- Fact: generated mocks remain Fast Loop evidence; Hybrid is used only when a
  real stateful/API adapter is available and part of the accepted claim.

## Context acquisition

Read S02 evidence and inspect the exact adapter targets, generator commands,
docs-site build, route/help/localization sources, and current package
boundaries. Verify generated files are either reproducible committed artifacts
or deterministic build outputs according to repository policy. Inspect
licenses and local bundling for any proposed font or icon asset. Stop if an
adapter requires an unaccepted downstream schema, secret, or Internet access.

## Requirements

### Must

- Implement router and history adapters for workspace-aware routes, safe query,
  deep links, Back/Forward, replace/push, workspace switch, dirty guard, and
  route-backed Focus origin restoration.
- Implement generated API client and development mock adapters from accepted
  schemas and examples, including stable errors, latency/failure fixtures, and
  explicit mock-mode disclosure.
- Implement explicit mock/real mode selection that fails closed on invalid
  configuration and cannot be enabled in a production or release build.
- Prove generated client, server-example, and mock payload parity and fail on
  manual drift.
- Implement safe preference persistence/API seams with schema version,
  optimistic revision, migration/default handling, and invalid-state cleanup.
- Implement en/ru bundle loading, fallback, interpolation, pluralization,
  formatting context, missing-key diagnostics, and parity checks.
- Implement docs/help metadata loading, route/field mapping, search indexing,
  visibility filtering, local/offline asset delivery, and missing/forbidden
  failure behavior.
- Implement stable error-to-system-surface mapping with safe reason/action
  codes and trace ID handling.
- Implement semantic token and local icon/font asset pipelines with deterministic
  builds, license/provenance records, and no remote runtime fetch.
- Keep adapters behind S02 ports and prevent reverse imports into policy core.
- Add integration tests for success, invalid schema, stale preference,
  forbidden route/help metadata, missing catalog, mock error, history
  restoration, offline build, and remote-asset negatives.
- Ensure logs and generated fixtures contain no secrets, cookies, tokens, raw
  PII, private browser state, or denied object metadata.

### Should

- Use contract-generated factories instead of large static fixtures.
- Make mock latency and failures deterministic and explicitly configured.
- Keep docs/help indexes content-addressed or otherwise reproducibly versioned.
- Detect stale generated output in CI rather than silently regenerating it.

## Forbidden actions

- Do not hand-edit generated clients or mock DTOs.
- Do not call arbitrary external URLs or allow runtime remote assets.
- Do not persist auth tokens, full API errors, filter values, or sensitive
  content in local preference storage.
- Do not let client filtering substitute for server authorization.
- Do not add downstream database or business adapters to B01.
- Do not weaken visibility, localization, contract, or DDD validators.
- Do not infer commit, push, deploy, or release authority.

## Work plan and stop gates

1. Verify S02 acceptance, adapter ownership, generator commands, and dirty-file
   separation.
2. Implement deterministic generation and parity checks first.
3. Implement router/history and preference adapters with negative paths.
4. Implement localization, docs/help, and system-error adapters.
5. Implement offline token/icon/font asset pipeline with provenance.
6. Add integration and failure tests for every port and visibility boundary.
7. Run generation drift, contract, route, docs, localization, DDD, type, lint,
   and focused test gates.
8. Build local docs/help artifacts and inspect for internal/sensitive leakage.
9. If an accepted real adapter exists, run its Hybrid boundary and record
   actual infrastructure identity; otherwise record why S03 remains Fast
   Loop/integration-harness evidence.
10. Write S03 evidence, then update the ledger and unlock only S04 if accepted.

Stop on manual generated drift, unaccepted downstream contract, remote runtime
dependency, secret or metadata leak, unsafe browser storage, reverse dependency
into the core, non-reproducible build, or unresolved adapter failure.

## Contracts and side effects

Authorized effects are repository-local generation, docs/help build output,
and isolated adapter tests. Any local storage or browser-history behavior is
tested through bounded fakes or integration harnesses, not accepted as a full
browser journey. No production service, external account, email, database,
deployment, or design-tool mutation is authorized. Contract corrections require
classification and regenerated artifacts.

## Validation and evidence

- Prove clean regeneration produces no uncommitted drift.
- Run generated client/mock parity and invalid-example tests.
- Run router/history, preference migration, system-error, localization, and
  docs/help integration tests.
- Build local docs/help and check visibility, links, offline assets, and search
  metadata.
- Run DDD, contract drift, route, localization, docs, staged-work, type, lint,
  and focused test gates.
- Record commands, generation inputs/outputs, licenses, failures, exclusions,
  and file manifest in
  `docs/architecture/workstreams/b01-experience-platform-stage-reports/S03-adapters.md`.
- S03 does not claim composed UI, real-browser accessibility, or downstream
  service correctness. Fast Loop mock evidence is not Hybrid, Full Stack, or
  Release evidence.

## Acceptance criteria

- [ ] Every accepted S02 port has a bounded adapter or an explicit later-stage
      composition disposition.
- [ ] Clients and mocks regenerate from one contract source with zero drift.
- [ ] Router/history, preferences, localization, docs/help, system-error, and
      asset adapters have positive and negative integration evidence.
- [ ] Offline/local delivery and visibility boundaries are enforced.
- [ ] No secret, PII, denied metadata, remote asset, or unsafe storage behavior
      is present.
- [ ] Dependency direction remains valid.
- [ ] Focused gates pass and evidence states its non-browser proof boundary.
- [ ] Ledger transition occurs before handoff and only S04 is unlocked.

## Result and handoff

Report status, adapter and generator files, contract changes, generation/parity
proof, integration tests, licenses, file manifest, blockers, residual risks,
and exact proof exclusions. Hand off S04 only after accepted evidence and
ledger synchronization.
