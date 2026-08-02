---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W29-HTML-FIRST-UI-FOUNDATION
status: ready
workstream_id: W29
summary: Extract the accepted UI-AN-003 HTML candidate into a versioned repository-owned UI foundation, component registry, screen manifests, and browser catalog; rebuild Sales Overview from those components and prove both same-viewport equivalence and Focus/Explore reuse.
requirement_ids: [WEB-ARCH-003, WEB-ARCH-005, WEB-ARCH-006, THEME-001, THEME-002, THEME-003, THEME-005, THEME-008, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, UI-SHELL-004, UI-SHELL-005, UI-SHELL-006, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, UI-DENSITY-004, FILTER-001, FILTER-002, FILTER-003, FILTER-004, FILTER-010, COMPARE-001, COMPARE-002, COMPARE-003, CHART-001, CHART-002, CHART-006, FOCUS-001, FOCUS-002, FOCUS-003, FOCUS-004, FOCUS-005, FOCUS-006, FOCUS-007, FOCUS-008, FOCUS-009, FOCUS-010, A11Y-001, A11Y-003, A11Y-008, ROUTE-004]
blockers: [W27-UI-AN-003-HTML-CONTRACT-COMPLETION]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/delivery/tickets/W27-UI-AN-003-HTML-CONTRACT-COMPLETION.md
  - .codex/delivery/evidence/W27-UI-AN-003-HTML-CONTRACT-COMPLETION.md
  - docs/architecture/ui/custometry-contract-compiled-ui-prototyping-plan-v1.md
  - .codex/delivery/specs/custometry-contract-compiled-ui-prototyping-pilot.md
  - custometry-ui-blueprint-ru.md
  - apps/web/src/sales-overview-prototype/SalesOverviewPrototype.tsx
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W29-HTML-FIRST-UI-FOUNDATION.md
    - .codex/delivery/evidence/W29-HTML-FIRST-UI-FOUNDATION.md
    - .codex/delivery/evidence/assets/W29-HTML-FIRST-UI-FOUNDATION/**
    - apps/web/src/sales-overview-prototype/**
    - apps/web/src/ui-lab/**
    - apps/web/src/App.tsx
    - apps/web/tests/sales-overview-prototype.test.tsx
    - apps/web/tests/ui-lab/**
    - packages/ui-foundation/**
    - packages/contracts/ui-design/**
    - tools/custometry_quality/ui_design/**
    - tests/ui_design/**
    - tests/e2e/**
    - tests/accessibility/**
    - package.json
    - pnpm-lock.yaml
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - docs/**
    - packages/contracts/routes/**
    - packages/localization/**
    - apps/api/**
    - apps/worker_data/**
    - packages/analytics_core/**
    - packages/analytics_customer/**
    - packages/analytics_sales/**
    - migrations/**
    - deploy/**
    - .codex/delivery/graphs/**
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills: [better-layout, better-ui, better-accessibility, browser-qa-evidence, playwright-cli, contract-impact-analysis]
  commands:
    - confirm W27 ticket status is accepted and its evidence records product_owner_decision accepted, terminal outcome pilot_passed, post-pilot decision scale, and the exact accepted visual source
    - inventory the accepted W27 tokens icons repeated structures variants states responsive rules and deferred runtime capabilities before changing source
    - create versioned semantic token icon component and screen-manifest schemas with stable code identities typed props accessibility metadata and DOM provenance rules
    - build an inspectable browser component catalog that imports the same public components used by screen compositions
    - rebuild accepted Sales Overview Chart Data Result Trust Sidebar and compact states from registered components without copied visible markup or private duplicate components
    - render Focus chart Focus breakdown and Explore composition from the same registry and record shared component IDs imports and DOM provenance
    - source scripts/activate-toolchain.sh
    - pnpm --filter @custometry/web lint
    - pnpm --filter @custometry/web typecheck
    - pnpm --filter @custometry/web test
    - pnpm --filter @custometry/web build
    - uv run python -m tools.custometry_quality.ui_design
    - uv run python -m tools.custometry_quality.ui_design.compile_render_plan --check
    - uv run pytest tests/ui_design
    - run the fresh-browser structural and screenshot-equivalence matrix at 1440 by 900 and 1024 by 768 for the accepted W27 source and rebuilt Sales composition
    - run the four-theme Russian-copy keyboard focus zoom sidebar Trust and Focus Explore browser matrix and record console and request diagnostics
    - uv run python -m tools.custometry_quality.validate_blueprints
    - uv run python -m tools.custometry_quality.generate_requirement_index --check
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uv run python -m tools.custometry_quality.check_i18n_parity
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.validate_delivery_contract
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: accepted-w27-equivalent-repository-owned-ui-foundation-plus-second-composition-browser-reuse-evidence
  evidence_target: .codex/delivery/evidence/W29-HTML-FIRST-UI-FOUNDATION.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

The accepted `UI-AN-003` HTML source is promoted into the repository's reusable
UI delivery substrate. Sales Overview, the browser component catalog, and the
Focus/Explore composition consume the same semantic tokens, icon registry, and
typed components. Same-viewport browser evidence proves that extraction did not
change the accepted visual result and that the second composition is genuine
reuse rather than copied markup.

# Eight-point transition boundary

1. The external-editor acceptance and publication path is discontinued.
2. Prior unpublished artifacts and their evidence remain immutable history and
   are not current delivery inputs.
3. W27 responsive HTML is the sole current visual source for `UI-AN-003`.
4. W29 extracts accepted decisions into semantic CSS tokens and typed reusable
   code components.
5. W29 creates stable code-identity registries, schemas, screen manifests, and
   an inspectable browser component catalog.
6. W29 rebuilds accepted Sales Overview from those components without copied
   visible markup.
7. W29 proves structural provenance and same-viewport screenshot equivalence in
   real browsers.
8. W29 renders Focus/Explore as a second composition from the same registry and
   proves component reuse.

Points 1-3 are accepted repository preconditions established by the
2026-08-02 product decision. This ticket executes and proves points 4-8 as one
ready delivery unit.

# Non-goals

- Do not redesign the accepted W27 composition or introduce new product,
  navigation, data, interaction, or theme decisions.
- Do not implement the full production shell, backend integration, ECharts,
  command palette, typed filter expressions, More actions, or real share,
  email, download, and export side effects.
- Do not migrate all 117 routes or claim production, API, persistence,
  performance, release, or deployment readiness.
- Do not delete or rewrite historical tickets, evidence, screenshots, or
  machine receipts.

# Work and repair boundary

Start from the exact accepted W27 browser source. Extract only visible and
behavioral decisions proven by that slice. Apply the dependency direction
`tokens -> primitives -> analytical patterns -> screen compositions`; catalog
and screen code must import the same public components. Component IDs and
screen manifests are portable repository contracts and must not embed raw
markup, tool-specific node identities, or environment-specific URLs.

Repair in-scope defects only and rerun every invalidated source, schema,
structural, visual, accessibility, and browser check. Stop if equivalence
requires a new product decision or the allowed paths cannot express the
accepted composition without changing a normative contract.

# Acceptance evidence

Terminal evidence records token/component/icon/manifest versions and digests,
the public component inventory, allowed variants and states, screen-to-component
mappings, catalog routes, DOM provenance, shared-import proof, same-viewport
screenshots and comparisons, four-theme and Russian-copy results, keyboard and
focus observations, console/network diagnostics, exact commands, exclusions,
and residual risks. W29 becomes `accepted` only when both the rebuilt Sales
composition and Focus/Explore reuse proof pass. W22 remains `draft` until that
terminal evidence exists.
