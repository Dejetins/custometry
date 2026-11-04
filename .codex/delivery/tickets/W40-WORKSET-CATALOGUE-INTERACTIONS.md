---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.11.0-draft
ticket_id: W40-WORKSET-CATALOGUE-INTERACTIONS
status: accepted
workstream_id: W40
summary: Create empty named worksets and manage workset visibility and metric membership
  through explicit menus and catalogue.
requirement_ids:
- METRIC-025
- METRIC-026
- METRIC-027
- REPORT-018
- REPORT-019
- A11Y-001
- I18N-001
blockers: []
context_sources:
- AGENTS.md
- .codex/AGENTS.md
- custometry-ui-blueprint-ru.md
- docs/adr/0007-responsive-web-frontend-platform.md
- docs/architecture/ui/references/mindbox-metrics-2026-09-17/follow-up-2026-09-24/README.md
change_scope:
  allowed_write_paths:
  - apps/api/src/custometry_api/reports/**
  - packages/presentation/**
  - packages/contracts/**
  - tests/unit/presentation/**
  - tests/integration/presentation/**
  - docs/contracts/analytical-authoring-contract.md
  - apps/web/src/features/reports/**
  - tests/e2e/report-loading/**
  - .codex/delivery/tickets/W40-WORKSET-CATALOGUE-INTERACTIONS.md
  - .codex/delivery/evidence/W40-WORKSET-CATALOGUE-INTERACTIONS/**
  - docs/architecture/ui/references/mindbox-metrics-2026-09-17/**
  - custometry-ui-blueprint-ru.md
  - docs/README.md
  forbidden_write_paths:
  - deploy/**
  - .codex/delivery/ledgers/**
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills:
  - browser-qa-evidence
  - contract-impact-analysis
  commands:
  - focused frontend unit tests
  - frontend typecheck and build
  - real API browser interaction checks
  - uv run python -m tools.check --scope local
  - git diff --check
  proof_boundary: local-preview-real-api-workset-and-catalogue-interactions
  evidence_target: .codex/delivery/evidence/W40-WORKSET-CATALOGUE-INTERACTIONS/report.md
escalation_triggers:
- normative_product_change
- material_user_scope_change
- external_or_irreversible_side_effect
- secrets_or_production_authority
- write_outside_allowed_scope
evidence:
- .codex/delivery/evidence/W40-WORKSET-CATALOGUE-INTERACTIONS/report.md
---

# Outcome

Owner authorized implementation on 2026-09-24. Ordinary creation produces an empty named personal workset. Adopt the observed Mindbox interaction principles within existing Custometry contracts. Explicit copy remains distinct from creation. Preserve Apply and Save, permissions, limits and server revision checks.

# Non-goals

No backend schema change, vendor metric invention, publication or milestone mutation.

# Acceptance evidence

Verify named empty creation, cancellation, visibility, rename/delete, catalogue membership and keyboard dismissal against the local API. Record focused tests and browser observations in the evidence target.

## Owner follow-up: report library organization

The owner accepted the UI-RPT-001 table-based library and separate creation section on 2026-09-30. This frontend follow-up preserves existing routes and saved data. Its current subset includes title/date/status, search, date filters, sorting and browser-local favorites. Author/type/Mine filters, report rename/copy/delete and blank creation remain pending backend capabilities, explicitly documented in the [evidence](../evidence/W40-WORKSET-CATALOGUE-INTERACTIONS/report.md#owner-follow-up-report-library).

## Owner follow-up: one editor for creation and editing (2026-10-03)

The owner authorized one configured editor for new and existing reports, including
blank and sales-template initialization and first Save. This extends the earlier
frontend-only scope above: native configured creation requires Presentation API,
contracts, persistence and focused tests. It does not authorize publication,
reseeding, or changes to existing test reports. No report is persisted on editor
entry or calculation; first Save atomically creates its first version and companion
view. Creator, dataset access and idempotency are enforced server-side.

Evidence remains in the linked W40 report. This follow-up supersedes the earlier
blank-creation limitation and backend-schema non-goal only for this bounded flow.

## Accepted follow-up: direct inspector catalogue (2026-10-03)

The owner approved exposing all available metrics in the inspector with grouped
checkboxes, catalogue-wide search and the source label. Selection updates the
existing draft and automatic calculation; no extra add-metric modal. Loading,
retryable failure, empty availability and empty selection are distinct. Existing
card order/settings remain available. API contracts and dataset contents are
unchanged. Current proof is recorded in the [evidence report](../evidence/W40-WORKSET-CATALOGUE-INTERACTIONS/report.md#direct-inspector-catalogue-2026-10-03).

The 2026-10-03 owner-reported comparison/display select alignment repair uses
the shared base-select styling; see the existing evidence report's
“Select value alignment repair” entry. No product/API contract change.

Owner follow-up 2026-10-06: rename the library creation card to New report and
remove the receipt-sales template card for now. UI-RPT-002 creation semantics
remain unchanged; browser verification is recorded in the evidence report under
“Report creation entry simplification”.

## Owner follow-up: structural editor regrouping (2026-10-06)

`CUSTOMETRY-REPORT-EDITOR-STRUCTURAL-REGROUPING` v1.0 selects this existing
independent unit for bounded UI-RPT-002 implementation. Both creation and editing
retain the shared configured editor. Separate report identity, page navigation,
data context, worksets/cards and visualization controls without changing visual
tokens, card internals or result renderers. Preserve automatic refresh, saved
reports and test datasets. No publication, deployment or milestone-ledger update.
The [relocation map and verification](../evidence/W40-WORKSET-CATALOGUE-INTERACTIONS/report.md#structural-editor-regrouping-2026-10-06)
and [canonical UI hierarchy](../../../custometry-ui-blueprint-ru.md#editor-structural-regrouping-2026-10-06)
record scope and evidence; existing ticket status is not new owner acceptance.
