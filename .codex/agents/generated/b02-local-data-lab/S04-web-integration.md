---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b02-s04-local-data-lab-web-integration
scope: "Integrate safe B02 profile metadata and lifecycle guidance into local documentation and the bounded optional-demo consumer contract, then verify the real browser surface."
spec_version: 0.8.2-draft
requirement_ids: [JOURNEY-001, AC-014, AC-016]
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
      why: B02 Web/docs integration scope
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
      why: predecessor and current-stage authority
    - path: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S03-adapters.md
      why: accepted profile, lifecycle, and adapter behavior
  task_entrypoints:
    - path: docs/architecture/documentation-platform.md
      why: local docs visibility, build, route, and security contract
      inspect_symbols: [public documentation, local docs, visibility, help]
    - path: docs/architecture/workstreams/b01-experience-platform-module.md
      why: shell, onboarding integration, localization, and browser ownership
      inspect_symbols: [UI and documentation, Ports and adapters, Data ownership]
    - path: docs-site/mkdocs.yml
      why: local documentation navigation and build input
      inspect_symbols: [nav, theme, plugins]
  conditional_bundles:
    docs_sources:
      read_when: implementing profile guide, reset guide, or contextual help
      paths: [docs-site/docs/en/**, docs/user-guide/**, docs/runbooks/**]
    consumer_contract:
      read_when: integrating profile metadata with a generated API/mock or onboarding surface
      paths: [docs/contracts/data-lab/**, packages/contracts/**, apps/web/**]
  consult_if_needed:
    - path: custometry-technical-blueprint-human-ru.md
      read_when: optional-demo wording or user expectation is ambiguous
skill_routing:
  - skill: ui-ux-pro-max
    role: primary
    use_when: making the local guide and optional-demo metadata compact, accessible, and understandable
  - skill: browser-qa-evidence
    role: companion_or_terminal_reviewer
    use_when: verifying the real local docs/browser flow, console, network, keyboard, and responsive behavior
change_ownership:
  owned_paths: [docs-site/docs/en/**, docs/user-guide/**, docs/runbooks/**, docs/contracts/data-lab/**, tests/e2e/data_lab/**, tests/accessibility/data_lab/**, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S04-web-integration.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md]
  foreign_exclusions: [B01 shell/component redesign, B03 authorization/workspace implementation, product-domain code, data generation, migrations, production docs visibility policy, Penpot, unrelated worktree changes]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
file_manifest:
  expected_primary_touches: [docs-site/docs/en/**, docs/user-guide/**, docs/runbooks/**, tests/e2e/data_lab/**, tests/accessibility/data_lab/**, docs/architecture/workstreams/b02-local-data-lab-stage-reports/S04-web-integration.md, docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md]
  possible_secondary_touches: [docs/contracts/data-lab/**, packages/contracts/**, apps/web/**, docs-site/mkdocs.yml]
  expected_deletions: []
validation_strategy:
  depth: browser
  acceptance_surfaces: [local docs route, profile guide, reset guidance, optional-demo metadata, accessibility, console, network]
  evidence_target: docs/architecture/workstreams/b02-local-data-lab-stage-reports/S04-web-integration.md
  tests_only_allowed_reason: null
proof_boundary:
  label: b02-s04-local-docs-and-consumer-browser
  exclusions: [first-admin authorization, workspace creation, generator runtime, clean-host install, benchmark evidence, release readiness]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: executable
  enabled: true
  workstream_id: B02
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b02-local-data-lab-plan.md
  prompt_pack_dir: .codex/agents/generated/b02-local-data-lab
  stage_ledger: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
  stage_id: S04
  predecessor_gate:
    stage_id: S03
    allowed_statuses: [accepted, superseded]
  state_preconditions:
    - S03 is accepted or explicitly superseded in the ledger.
    - The ledger status is active, current stage is S04, and only S04 has next_allowed true.
    - Accepted profile metadata and lifecycle errors are available without secrets.
    - B01 integration ownership is agreed, or the stage is bounded to the existing local documentation surface.
    - A real local browser surface can be started and inspected.
  required_source_hashes: {}
  branch_policy:
    default_branch: main
    separate_branch_requested: true
    allowed_branch: codex/b02-local-data-lab
    per_stage_branches: forbidden
  next_stage_rule:
    candidate_stage: S05
    unlock_on: accepted
    authority: stage_ledger
---

# Objective

Make B02 usable without exposing infrastructure internals. Add concise local
documentation for profile selection, sizes, scenarios, benchmark warnings,
golden verification, reset, and migration troubleshooting. Expose only safe
versioned profile metadata to the optional-demo consumer boundary. Verify the
real local browser route, keyboard/accessibility behavior, console, network,
and responsive layout while leaving first-admin and workspace authorization to
their owners.

## Non-goals

- Do not redesign the Experience Platform shell or documentation system.
- Do not implement first-admin, workspace creation, invites, or authorization.
- Do not start benchmark generation from the browser.
- Do not expose credentials, host paths, raw runtime environment, or internal
  migration details.
- Do not claim S03 adapters pass on a clean host.

## Verified current context

- Fact: S03 accepts the profile, reset, migration, and golden-evidence adapter
  behavior.
- Fact: local `/docs` is a required offline browser surface.
- Fact: B02 owns safe profile descriptions, while B01/B03 own presentation and
  authorization of first-run workflows.
- Assumption: the existing docs shell can render the guide without a new
  product component; verify the current implementation.
- Unknown/blocker: if an optional-demo product control is not yet implemented,
  S04 may accept the versioned consumer contract plus real docs browser proof,
  but it must record product onboarding UI as deferred to its owner.

## Context acquisition

Read S03 evidence and the documentation visibility contract first. Inspect only
the current docs navigation, relevant generated contract, and optional existing
consumer surface. Capture browser evidence before making a visual claim.
Expand to B01/B03 code only when a bounded integration point already exists and
ownership is explicit.

## Requirements

### Must

- Document `smoke`, `demo`, and `benchmark` purpose, current size, seed,
  opt-in behavior, support status, and resource warning.
- Document safe bootstrap, profile mismatch, golden verification, exact
  installation-scoped reset, migration failure, and recovery guidance.
- State clearly that reset deletes only the installation-owned demo-source
  volume and never authorizes global cleanup.
- State clearly that benchmark existence is not performance or support proof.
- Present scenario coverage and proof limits without promising downstream
  analytical correctness.
- Expose only safe profile ID, display keys, counts, status, warning, and
  selection eligibility through the consumer contract.
- Keep IDs locale-neutral and all visible strings localization-ready.
- If a product control exists, preserve B01 layout, keyboard, focus, reduced
  motion, loading, error, and route semantics; B02 supplies data only.
- Verify the docs route and any bounded control in a real browser at supported
  widths with keyboard navigation and accessible names.
- Inspect console and network for errors, remote assets, secrets, PII, or
  unexpected requests.
- Add focused browser/accessibility tests and update docs indexes/navigation.

### Should

- Use compact tables and progressive disclosure rather than long warning
  blocks.
- Include copyable commands that avoid secret values.
- Link troubleshooting to stable error codes from S01.

## Forbidden actions

- Do not publish internal prompts, ledgers, architecture notes, raw logs, or
  secrets in public docs.
- Do not label benchmark as recommended/default.
- Do not allow browser-side metadata to authorize reset or profile generation.
- Do not invent a new route, component library, color token, or motion rule
  outside B01.
- Do not use screenshots alone as browser evidence.
- Do not infer commit, push, deploy, or release authority.

## Work plan and stop gates

1. Verify S03 acceptance and docs/consumer ownership.
2. Capture the existing local docs and optional consumer surface.
3. Implement the smallest guide, navigation, contract, and bounded UI changes.
4. Add browser/accessibility coverage and validate localization/visibility.
5. Run a real browser flow at normal and compact desktop widths.
6. Inspect console, network, keyboard, focus, links, and command accuracy.
7. Record deferred product-onboarding ownership if no authorized control exists.
8. Write S04 evidence, validate, then authorize only S05.

Stop if docs visibility would leak internal content, B01/B03 ownership is
unclear, browser startup is unavailable, commands are unsafe, or a visible
control implies authorization B02 does not own.

## Contracts and side effects

Repository effects are limited to docs, generated consumer schemas/examples,
bounded existing UI integration, tests, report, and ledger. Browser execution
may start the local application but may not trigger benchmark or destructive
reset. Classify:

- docs visibility and route changes;
- profile metadata DTO/schema;
- optional control defaults and error behavior;
- localization keys and accessibility semantics;
- browser storage, logs, network, and redaction;
- command/runbook compatibility.

No database mutation or external network side effect is needed for S04.

## Validation and evidence

- Local gates:
  - documentation build and link checks;
  - focused contract and localization tests;
  - focused browser and accessibility tests;
  - `uv run python -m tools.custometry_quality.check_docs_links`
  - `uv run python -m tools.custometry_quality.check_i18n_parity`
  - `uv run python -m tools.custometry_quality.browser_smoke --help`
  - `uv run python -m tools.custometry_quality.validate_staged_workstream`
- Real-boundary evidence: real local browser screenshots/trace as supporting
  evidence, keyboard path, accessible names, console, network, and responsive
  smoke.
- Evidence location:
  `docs/architecture/workstreams/b02-local-data-lab-stage-reports/S04-web-integration.md`.
- Explicit exclusions: first-admin authorization, workspace creation,
  clean-host Compose, benchmark performance, production deployment, release.

## Acceptance criteria

- [ ] Local docs explain profiles, scenarios, verification, migration, reset,
      warnings, and proof limits accurately.
- [ ] Public/internal visibility rules are preserved.
- [ ] Safe profile metadata is versioned and contains no secret or authority.
- [ ] Optional product integration, if present, stays within B01/B03 contracts.
- [ ] Real browser keyboard, focus, links, responsive, console, and network
      evidence passes.
- [ ] Commands are copyable, bounded, and do not include secret values.
- [ ] Deferred onboarding UI ownership is explicit if not implemented.
- [ ] S04 evidence is durable and the ledger authorizes only S05.

## Result and handoff

Write docs/browser evidence, contract impact, deferred ownership, and the ledger
update in English. The Russian user report names visible outcomes, requirement
IDs, changed files, actual browser checks, screenshots or trace locations,
console/network result, exclusions, residual risks, and exact S05 prompt. Do
not claim clean-host or benchmark readiness.
