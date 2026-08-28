---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W35-WEB-NOTIFICATION-INBOX
status: accepted
workstream_id: W35
summary: Implement the global UI-NOTIFY-001 Notification Inbox production route with truthful acknowledgement, deep links, and browser proof.
requirement_ids: [NOTIFY-001, NOTIFY-003, NOTIFY-004, NOTIFY-005, NOTIFY-007, RBAC-002, A11Y-001, I18N-001]
blockers: []
context_sources: [AGENTS.md, .codex/AGENTS.md, docs/architecture/ui/custometry-web-implementation-source-contract-v1.md, custometry-technical-blueprint-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/ui-route-contracts.json, packages/contracts/routes/ui-surface-contracts.json, .codex/delivery/tickets/W31-WEB-PRODUCTION-SHELL-ROUTING.md, .codex/delivery/specs/in-app-notification-inbox.md, .codex/delivery/tickets/W37-INAPP-NOTIFICATION-INBOX-API.md]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W35-WEB-NOTIFICATION-INBOX.md, .codex/delivery/evidence/W35-WEB-NOTIFICATION-INBOX.md, apps/web/src/features/notifications/**, apps/web/src/app/routes/features/notifications.tsx, apps/web/tests/notifications/**, tests/e2e/web-notifications/**, tests/accessibility/web-notifications/**]
  forbidden_write_paths: [.codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/**, apps/api/**, migrations/**, deploy/**]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: browser
  proof_skills: [contract-impact-analysis, better-accessibility, browser-qa-evidence, playwright-cli]
  commands: [source scripts/activate-toolchain.sh && pnpm --filter @custometry/web lint && pnpm --filter @custometry/web test && pnpm --filter @custometry/web build, source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-notifications/playwright.config.ts, uv run python -m tools.custometry_quality.validate_route_registry, uv run python -m tools.custometry_quality.validate_delivery_tickets, uv run python -m tools.check --scope local, git diff --check]
  proof_boundary: production-ui-notify-001-with-real-adapter-or-explicit-unavailable-boundary-and-real-browser-observation
  evidence_target: .codex/delivery/evidence/W35-WEB-NOTIFICATION-INBOX.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W35-WEB-NOTIFICATION-INBOX.md]
---

# Outcome

`UI-NOTIFY-001` at `/notifications` renders a production global inbox with
severity/category/read/acknowledged/resolved filters, deduplication groups,
details, permission-aware acknowledgement, and safe deep links through typed
application adapters.

# Non-goals

- Do not implement notification delivery, backend acknowledgement persistence,
  preference management, email, or another notification surface.
- Do not publish, deploy, create mobile-specific design, or claim full WCAG.

# Work and repair boundary

Own only the notifications feature and its route module. The notify G4 family
was unaccepted at cutover, so inherit G3 and normative semantics. Owner review
is required only for a material new direction, baseline exception, or
non-derivable product meaning.

# Acceptance evidence

Focused tests cover filtering, dedupe, acknowledgement permission, safe deep
links, loading, empty, stale/degraded, forbidden, and failed states.
Playwright CLI observes critical inbox behavior at 768 and 1920 CSS px in
RU/EN with keyboard/accessibility and console/network smoke, and the report
separates adapter fixtures from real API/runtime evidence.
