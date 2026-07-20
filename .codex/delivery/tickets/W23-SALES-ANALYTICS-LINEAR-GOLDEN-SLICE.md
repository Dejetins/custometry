---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W23-SALES-ANALYTICS-LINEAR-GOLDEN-SLICE
status: draft
workstream_id: W23
summary: Deliver one real read-only Sales Analytics golden slice through the new shell and existing REST/SSE projections, including compact metrics, filters, vs LY, chart/data switching, Result Trust, route-backed Focus/Explore, four themes, and measured end-to-end browser behavior.
requirement_ids: [WEB-ARCH-002, WEB-ARCH-004, WEB-PERF-001, WEB-PERF-003, WEB-PERF-004, WEB-PERF-005, WEB-PERF-006, FILTER-001, FILTER-002, FILTER-003, FILTER-004, FILTER-010, COMPARE-001, COMPARE-002, COMPARE-003, FOCUS-001, FOCUS-002, FOCUS-003, FOCUS-004, FOCUS-005, FOCUS-006, FOCUS-007, FOCUS-008, FOCUS-009, FOCUS-010, FOCUS-011, FOCUS-012, CHART-001, CHART-002, CHART-006, THEME-008]
blockers: [W16-SALES-CUSTOMER-RFM-API-PROJECTIONS, W22-WEB-LINEAR-APPLICATION-SHELL]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/delivery/specs/custometry-linear-workspace-ui-transition.md
  - .codex/delivery/tickets/W16-SALES-CUSTOMER-RFM-API-PROJECTIONS.md
  - .codex/delivery/tickets/W22-WEB-LINEAR-APPLICATION-SHELL.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/system-design.md
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-surface-contracts.json
  - packages/contracts/openapi/foundation.openapi.json
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W23-SALES-ANALYTICS-LINEAR-GOLDEN-SLICE.md
    - .codex/delivery/evidence/W23-SALES-ANALYTICS-LINEAR-GOLDEN-SLICE.md
    - apps/web/**
    - packages/ui-foundation/**
    - packages/localization/**
    - tests/e2e/**
    - tests/accessibility/**
    - tests/performance/**
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - docs/**
    - packages/contracts/**
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
  proof_skills: [browser-qa-evidence, backend-performance-evidence, playwright]
  commands:
    - source scripts/activate-toolchain.sh
    - pnpm --filter @custometry/web lint
    - pnpm --filter @custometry/web typecheck
    - pnpm --filter @custometry/web test
    - pnpm --filter @custometry/web build
    - run contract and integration checks declared by the accepted W16 API projection evidence
    - run the real-browser Sales Analytics and Focus Explore journeys against the real local API and PostgreSQL deterministic dataset in all representative themes and states
    - verify URL history Back Escape filters vs LY chart table Result Trust accessibility localization console network and SSE freshness behavior
    - measure end-to-end and client-only dispatch acknowledgement response-to-paint SSE-to-paint INP long tasks and frame cadence with p50 p75 p95 on declared hardware
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uv run python -m tools.custometry_quality.check_i18n_parity
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: real-browser-real-api-postgresql-sales-analytics-focus-explore-golden-slice
  evidence_target: .codex/delivery/evidence/W23-SALES-ANALYTICS-LINEAR-GOLDEN-SLICE.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

One valuable analytics journey proves that the new shell is not merely visual:
it renders real authorized Sales Analytics projections, preserves result trust
and URL state, remains fast and accessible, and supplies evidence for planning
the remaining route clusters.

# Non-goals

- Do not add or change backend endpoints, SQL, analytics methods, permissions,
  or persistence.
- Do not implement authoring, exports, email, XLSX, or all analytics routes.

# Work and repair boundary

Compose only the accepted W16 projection through the W22 shell and existing
ChartSpec/route contracts. Any missing server behavior is a blocker or a new
backend ticket, not client-side business logic. Repair owned presentation and
adapter defects, then rerun every invalidated real-boundary check.

# Acceptance evidence

Evidence records the real dataset/API/runtime identity, authorization persona,
all browser states and themes, traces/screenshots, accessibility and history
checks, performance distributions, rollback exercise, and the route-cluster
decisions that are now supported by facts.
