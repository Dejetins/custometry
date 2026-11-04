---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.11.0-draft
ticket_id: W41-COMPOSER-CANVAS-LAYOUT
status: accepted
workstream_id: W41
summary: Move and resize chart and table blocks directly within their section and reclaim unused block space.
requirement_ids: [ANALYTICAL-DOC-002, DASHBOARD-001, DASHBOARD-006, A11Y-001]
blockers: []
context_sources: [AGENTS.md, .codex/AGENTS.md, custometry-ui-blueprint-ru.md, docs/architecture/ui/target-pilot/README.md, docs/adr/0007-responsive-web-frontend-platform.md]
change_scope:
  allowed_write_paths: [apps/web/src/features/reports/**, .codex/delivery/tickets/W41-COMPOSER-CANVAS-LAYOUT.md, .codex/delivery/evidence/W41-COMPOSER-CANVAS-LAYOUT/**, custometry-ui-blueprint-ru.md]
  forbidden_write_paths: [deploy/**, .codex/delivery/ledgers/**]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills: [better-layout, better-accessibility, browser-qa-evidence]
  commands: [focused frontend tests, frontend build, uv run --locked python -m tools.check --scope local, git diff --check]
  proof_boundary: local-composer-canvas-with-existing-test-data
  evidence_target: .codex/delivery/evidence/W41-COMPOSER-CANVAS-LAYOUT/report.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W41-COMPOSER-CANVAS-LAYOUT/report.md]
---

# Outcome

Owner authorized direct block movement/resizing and removal of routine timezone
and empty-status whitespace on 2026-10-08. This independent UI unit does not
resume the stopped WS-004 milestone sequence. Source baseline is the running
c67c checkout, preserving prior uncommitted work.

Move chart/table blocks within their section without changing inherited scopes;
resize grid blocks, reflow neighbors, preserve locks, undo/redo and saved snapshots.
Use keyboard alternatives and existing placement persistence. Preserve errors,
loading and meaningful calculation limitations. No dependencies or publication.

# Non-goals

No cross-section scope changes, new providers, publication or milestone resumption.

# Acceptance evidence

See the linked evidence report for native pointer, keyboard alternatives,
responsive, history and real API save/reopen checks, plus focused tests and build.
