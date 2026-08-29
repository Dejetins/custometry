---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W33-WEB-CONNECTIONS
status: ready
workstream_id: W33
summary: Implement the cohesive UI-DATA-001 connection list and UI-DATA-002 connection editor production slice with governed connector states and browser proof.
requirement_ids: [UC-001, CONNECTOR-001, CONNECTOR-004, A11Y-001, I18N-001]
blockers: []
context_sources: [AGENTS.md, .codex/AGENTS.md, docs/architecture/ui/custometry-web-implementation-source-contract-v1.md, custometry-technical-blueprint-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/ui-route-contracts.json, packages/contracts/routes/ui-surface-contracts.json, .codex/delivery/tickets/W31-WEB-PRODUCTION-SHELL-ROUTING.md, .codex/delivery/tickets/W14-SOURCE-CONNECTION-FILE-IMPORT-KERNEL.md]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W33-WEB-CONNECTIONS.md, .codex/delivery/evidence/W33-WEB-CONNECTIONS.md, apps/web/src/features/connections/**, apps/web/src/app/routes/features/connections.tsx, apps/web/tests/connections/**, tests/e2e/web-connections/**, tests/accessibility/web-connections/**]
  forbidden_write_paths: [.codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/**, apps/api/**, plugins/**, migrations/**, deploy/**]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: browser
  proof_skills: [contract-impact-analysis, better-accessibility, browser-qa-evidence, playwright-cli]
  commands: [source scripts/activate-toolchain.sh && pnpm --filter @custometry/web lint && pnpm --filter @custometry/web test && pnpm --filter @custometry/web build, source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-connections/playwright.config.ts, uv run python -m tools.custometry_quality.validate_route_registry, uv run python -m tools.custometry_quality.validate_delivery_tickets, uv run python -m tools.check --scope local, git diff --check]
  proof_boundary: production-ui-data-001-and-ui-data-002-with-real-adapter-or-explicit-unavailable-boundary-and-real-browser-observation
  evidence_target: .codex/delivery/evidence/W33-WEB-CONNECTIONS.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

`UI-DATA-001` and `UI-DATA-002` provide one production connection-management
slice: searchable status/owner list, governed connector choice, credential
reference handling, parameters/template version, test feedback, validation,
and save-draft behavior through typed application adapters.

# Non-goals

- Do not implement connector backend logic, secret storage, ingestion, or later
  data-catalog routes.
- Do not display raw credentials, invent provider capabilities, publish, deploy,
  create mobile-specific design, or claim full WCAG.

# Work and repair boundary

Own only the connections feature and its route module. Inherit the accepted
data-family reference when applicable; unresolved states use the accepted G3
baseline and normative semantics. A new baseline exception requires owner
review, while routine inheritance does not.

# Acceptance evidence

Focused tests cover permissions, field validation, secret redaction, test/save
outcomes, list filtering, loading, empty, degraded, forbidden, and failed
states. Playwright CLI observes critical list-to-editor flow at 768 and 1920
CSS px in RU/EN with keyboard/accessibility and console/network smoke, clearly
separating adapter fixtures from real API/runtime proof.
