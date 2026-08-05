---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W21-CONTRACT-COMPILED-UI-PILOT
status: accepted
workstream_id: W21
summary: Prove the accepted contract-compiled UI delivery process on one selected premium Linear-style UI-AN-003 Sales Overview variant, from three isolated explorations through a restricted manifest, deterministic Figma render, read-back audit, bounded repair, product acceptance, and reproducibility rerender.
requirement_ids: [WEB-ARCH-003, WEB-ARCH-005, WEB-ARCH-006, THEME-001, THEME-002, THEME-003, THEME-005, THEME-008, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, FILTER-001, FILTER-002, FILTER-003, FILTER-004, FILTER-010, COMPARE-001, COMPARE-002, COMPARE-003, CHART-001, CHART-002, CHART-006, A11Y-001, A11Y-003]
blockers: []
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - docs/architecture/ui/custometry-contract-compiled-ui-prototyping-plan-v1.md
  - .codex/delivery/specs/custometry-contract-compiled-ui-prototyping-pilot.md
  - custometry-ui-blueprint-ru.md
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-surface-contracts.json
start_probe:
  boundary: exact authorized Figma library hX3nQOtcSdCc97uv26m9eG and product file MXfxuhSFpIczbUtFmOSyPp
  read_only_check: confirm each file is a Figma Design with exactly one Page 1 node 0:1, no top-level children, no local variable collections or variables, and no local paint/text/effect/grid styles before any visual exploration or Figma mutation
  stop_on: [unavailable, identity_mismatch, state_drift]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W21-CONTRACT-COMPILED-UI-PILOT.md
    - .codex/delivery/evidence/W21-CONTRACT-COMPILED-UI-PILOT.md
    - .codex/delivery/evidence/assets/W21-CONTRACT-COMPILED-UI-PILOT/**
    - packages/contracts/ui-design/**
    - tools/custometry_quality/ui_design/**
    - tests/ui_design/**
    - external:figma/hX3nQOtcSdCc97uv26m9eG/**
    - external:figma/MXfxuhSFpIczbUtFmOSyPp/**
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - apps/**
    - packages/analytics_core/**
    - packages/analytics_customer/**
    - packages/analytics_sales/**
    - packages/contracts/routes/**
    - migrations/**
    - deploy/**
    - docs/architecture/ui/linear-workspace-reference-manifest-v1.json
    - .codex/delivery/evidence/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: [figma:figma-use, product-design:ideate, product-design:audit, better-interface]
  commands:
    - preserve the observed empty baseline for both exact Figma files and perform no Figma mutation before one visual direction is explicitly selected
    - generate exactly three separate 1440 by 900 graphite UI-AN-003 success-state explorations from one frozen screen contract using better-interface full coverage and no historical frame input
    - require the product owner to select one exact exploration identity before token component manifest or Figma screen construction
    - prove cross-file variable component publication import and instance creation at the exact authorized boundary before product composition
    - validate canonical and negative fixtures for raw nodes unknown components forbidden actions missing regions detached instances target drift and unknown contract versions
    - require every visible product control to be a registered instance with semantic variable and text-style bindings and no raw rectangle icons
    - render the selected manifest twice into isolated product candidates and compare normalized structural receipts plus bounded visual diff
    - run a four-theme semantic-token sweep and Russian long-copy stress render without claiming four separate aesthetic acceptances
    - record machine conformance product decision implementation readiness exact Figma identities versions digests screenshots repair attempts and exclusions
    - uv run python -m tools.custometry_quality.validate_blueprints
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.validate_repository_layout
    - git diff --check
  proof_boundary: product-owner-selected-machine-conformant-reproducible-two-render-figma-ui-an-003-design-process-pilot
  evidence_target: .codex/delivery/evidence/W21-CONTRACT-COMPILED-UI-PILOT.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W21-CONTRACT-COMPILED-UI-PILOT.md]
---

# Outcome

One premium Linear-style Sales Overview direction is selected from three
contract-equivalent explorations, compiled into a minimum registered library
slice and restricted manifest, and rendered twice into isolated Figma
candidates with machine-conformant equivalent structure and explicit product
acceptance state.

# Non-goals

- Do not use historical Penpot or pre-plan Figma frames as visual input.
- Do not build a global Master Elements Index, all-route foundation, complete
  screen state matrix, runtime shell, or production frontend.
- Do not mutate either canonical Figma file before the product owner selects one
  exact exploration.
- Do not change product semantics, routes, permissions, APIs, analytics,
  persistence, or deployment.
- Do not claim browser, accessibility-runtime, performance, release, or
  production readiness.

# Work and repair boundary

Own the minimum UI-AN-003 token/component/manifest/compiler slice and exact
authorized Figma targets. Codex coordinates all executors and audits their
output. Image generation and Figma scripts cannot widen the frozen screen
contract. After selection, library construction and product rendering remain
separate mutations. Unknown components stop screen rendering. Machine repair
is limited to two attempts and reruns every invalidated check.

# Acceptance evidence

Evidence includes the empty baselines, three exploration identities and prompts,
product selection, exact Figma file/page/node identities, token/registry/manifest
and renderer versions, negative fixtures, before/after inventories, variable and
style bindings, component-instance and detachment audits, screenshots, two
normalized render receipts, visual comparison, repair history, final acceptance
dimensions, explicit non-runtime exclusions, and the `scale`, `change_adapter`,
or `stop` decision.
