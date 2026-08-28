---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W34-WEB-OPERATOR-RUNS
status: ready
workstream_id: W34
summary: Implement the UI-OPS-001 Operator Center production route with truthful run lifecycle actions, queue state, and boundary-matched browser proof.
requirement_ids: [UC-010, OPS-001, EXEC-STATE-001, EXEC-STATE-002, EXEC-STATE-006, EXEC-STATE-007, EXEC-CANCEL-005, ADMIN-003, ADMIN-005, A11Y-001, I18N-001]
blockers: []
context_sources: [AGENTS.md, .codex/AGENTS.md, docs/architecture/ui/custometry-web-implementation-source-contract-v1.md, custometry-technical-blueprint-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/ui-route-contracts.json, packages/contracts/routes/ui-surface-contracts.json, .codex/delivery/tickets/W31-WEB-PRODUCTION-SHELL-ROUTING.md, .codex/delivery/specs/operator-runs-api-and-execution-control.md, .codex/delivery/tickets/W36-EXECUTION-CONTROL-OPERATOR-API.md]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W34-WEB-OPERATOR-RUNS.md, .codex/delivery/evidence/W34-WEB-OPERATOR-RUNS.md, apps/web/src/features/operator-runs/**, apps/web/src/app/routes/features/operator-runs.tsx, apps/web/tests/operator-runs/**, tests/e2e/web-operator-runs/**, tests/accessibility/web-operator-runs/**]
  forbidden_write_paths: [.codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/**, apps/api/**, apps/worker_data/**, migrations/**, deploy/**]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: browser
  proof_skills: [contract-impact-analysis, better-accessibility, browser-qa-evidence, playwright-cli]
  commands: [source scripts/activate-toolchain.sh && pnpm --filter @custometry/web lint && pnpm --filter @custometry/web test && pnpm --filter @custometry/web build, source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-operator-runs/playwright.config.ts, uv run python -m tools.custometry_quality.validate_route_registry, uv run python -m tools.custometry_quality.validate_delivery_tickets, uv run python -m tools.check --scope local, git diff --check]
  proof_boundary: production-ui-ops-001-with-real-adapter-or-explicit-unavailable-boundary-and-real-browser-observation
  evidence_target: .codex/delivery/evidence/W34-WEB-OPERATOR-RUNS.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

`UI-OPS-001` at `/w/:workspaceKey/runs` renders an operator-grade list for
queued, running, succeeded, failed, and cancelling runs with filters,
auto-refresh status, queue summary, permitted cancel/retry actions,
human-readable failure, and trace identity through typed adapters.

# Non-goals

- Do not implement the pending OPS design-family gate, worker execution,
  scheduler/queue semantics, or another operations route.
- Do not publish, deploy, create mobile-specific design, or claim full WCAG.

# Work and repair boundary

Own only the operator-runs feature and its route module. Because OPS G4 was
unaccepted at cutover, inherit G3 and normative route semantics. Request owner
review only for a material visual direction, baseline exception, or new product
meaning; ordinary implementation decisions remain agent-decidable.

# Acceptance evidence

Focused tests cover lifecycle transitions, action permissions, refresh, trace
and failure presentation, loading, empty, stale/degraded, forbidden, and failed
states. Playwright CLI covers critical states at 768 and 1920 CSS px, RU/EN,
keyboard/accessibility smoke, and console/network diagnostics against the
strongest available real boundary, with honest runtime exclusions.
