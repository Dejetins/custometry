---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W32-WEB-SALES-OVERVIEW
status: accepted
workstream_id: W32
summary: Implement the production UI-AN-003 Sales Overview route with real analytics adapters, truthful result states, and boundary-matched browser proof.
requirement_ids: [UC-004, UC-012, UC-027, DISCOUNT-001, DISCOUNT-004, DISCOUNT-005, DISCOUNT-008, DISCOUNT-009, DISCOUNT-010, DISCOUNT-011, DISCOUNT-012, DISCOUNT-013, DISCOUNT-014, DISCOUNT-015, DISCOUNT-016, DISCOUNT-017, DISCOUNT-018, DISCOUNT-019, PVM-001, PVM-002, PVM-003, PVM-004, PVM-005, PVM-006, METRIC-017, METRIC-019, METHOD-010, METHOD-011, METHOD-012, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, A11Y-001]
blockers: []
context_sources: [AGENTS.md, .codex/AGENTS.md, docs/architecture/ui/custometry-web-implementation-source-contract-v1.md, custometry-technical-blueprint-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/ui-route-contracts.json, packages/contracts/routes/ui-surface-contracts.json, .codex/delivery/tickets/W31-WEB-PRODUCTION-SHELL-ROUTING.md, .codex/delivery/tickets/W16-SALES-CUSTOMER-RFM-API-PROJECTIONS.md]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W32-WEB-SALES-OVERVIEW.md, .codex/delivery/evidence/W32-WEB-SALES-OVERVIEW.md, apps/web/src/features/analytics-sales/**, apps/web/src/app/routes/features/analytics-sales.tsx, apps/web/tests/analytics-sales/**, tests/e2e/web-analytics-sales/**, tests/accessibility/web-analytics-sales/**]
  forbidden_write_paths: [.codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/**, apps/api/**, migrations/**, deploy/**]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: browser
  proof_skills: [contract-impact-analysis, better-accessibility, browser-qa-evidence, playwright-cli]
  commands: [source scripts/activate-toolchain.sh && pnpm --filter @custometry/web lint && pnpm --filter @custometry/web test && pnpm --filter @custometry/web build, source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-analytics-sales/playwright.config.ts, uv run python -m tools.custometry_quality.validate_route_registry, uv run python -m tools.custometry_quality.validate_delivery_tickets, uv run python -m tools.check --scope local, git diff --check]
  proof_boundary: production-ui-an-003-with-real-adapter-or-explicit-unavailable-boundary-and-real-browser-observation
  evidence_target: .codex/delivery/evidence/W32-WEB-SALES-OVERVIEW.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W32-WEB-SALES-OVERVIEW.md]
---

> Source update, 2026-09-04: the G-program was removed. Historical acceptance
> and evidence remain unchanged; they do not prove conformance to the final
> target pilot. Any new work requires its own ready ticket and the current
> Web implementation source contract. Forbidden historical paths remain guards.

# Outcome

`UI-AN-003` at `/w/:workspaceKey/analytics/sales` renders production revenue,
orders, AOV, margin, trend, contribution, product/store/channel breakdown, and
Result Trust behavior through typed application adapters. Loading, empty,
ready, stale/degraded, forbidden, and failed states remain truthful.

# Non-goals

- Do not implement another analytics route, backend analytics computation, or a
  design-only prototype.
- Do not change normative discount/PVM methodology or introduce a new visual
  direction without owner review.
- Do not publish, deploy, add mobile-specific design, or claim full WCAG.

# Work and repair boundary

Implement only the sales feature and its self-registering route module. Future
conformance work follows the preserved target pilot and product semantics;
mocked data is not a production result. Compatible
adapter/test repairs inside owned paths are allowed and invalidate their tests.

# Acceptance evidence

Focused tests cover DTO adaptation, permissions, freshness/trust, filters,
critical result and failure states. Playwright CLI proves the changed flow at
768 and 1920 CSS px, RU/EN, keyboard focus, accessibility smoke, and
console/network behavior against the strongest available real boundary. The
report separates fixture, API, browser, and unproven production-runtime claims.
