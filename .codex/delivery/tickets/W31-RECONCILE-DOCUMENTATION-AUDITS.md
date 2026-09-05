---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W31-RECONCILE-DOCUMENTATION-AUDITS
status: accepted
workstream_id: W31
summary: Publish the corrected audited document set while preserving accepted main
  pilot/governance decisions and existing implementation.
requirement_ids:
- DOC-RULE-008
- DATA-RULE-010
- METRIC-019
- UNIT-ECON-012
- RBAC-013
- RBAC-023
- WEB-ARCH-001
- WEB-ARCH-005
- TEST-INV-020
- V1-AC-067
blockers: []
context_sources:
- AGENTS.md
- .codex/AGENTS.md
- custometry-technical-blueprint-ru.md
- custometry-technical-blueprint-human-ru.md
- custometry-ui-blueprint-ru.md
- docs/architecture/bounded-context-map.md
- docs/adr/0007-responsive-web-frontend-platform.md
- docs/architecture/tooling-gates.md
- docs/architecture/planning/documentation-audit-reconciliation-2026-09-06.md
- docs/architecture/ui/target-pilot/README.md
- docs/architecture/ui/custometry-web-implementation-source-contract-v1.md
change_scope:
  allowed_write_paths:
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/adr/0005-collaboration-measurement-and-compute-reuse.md
  - docs/adr/0006-analytical-document-retail-product-and-time-aware-segmentation.md
  - docs/adr/0007-responsive-web-frontend-platform.md
  - docs/architecture/README.md
  - docs/architecture/bounded-context-map.md
  - docs/architecture/system-design.md
  - docs/architecture/repository-layout.md
  - docs/architecture/development-operating-model.md
  - docs/architecture/documentation-platform.md
  - docs/architecture/runtime-network-installation.md
  - docs/architecture/tooling-gates.md
  - docs/architecture/planning/development-roadmap-v1.md
  - docs/architecture/planning/development-audit-2026-09-04.md
  - docs/architecture/planning/product-capability-discovery-2026-09-05.md
  - docs/architecture/ui/comparable-analytics-platform-capability-audit-v1.md
  - docs/contracts/ui-route-contract.md
  - docs/contracts/ui-surface-contract.md
  - docs/contracts/analytical-authoring-contract.md
  - docs/contracts/source-data-adaptation-contract.md
  - docs/contracts/README.md
  - docs/contracts/artifact-format-contract.md
  - docs/architecture/planning/audit-contract-decisions-2026-09-06.md
  - docs/architecture/planning/documentation-audit-reconciliation-2026-09-06.md
  - docs/generated/requirement-index.json
  - docs/README.md
  - .codex/delivery/tickets/W31-RECONCILE-DOCUMENTATION-AUDITS.md
  - .codex/delivery/evidence/W31-RECONCILE-DOCUMENTATION-AUDITS.md
  - docs/architecture/planning/development-coverage-2026-09-04.json
  - packages/contracts/routes/ui-surface-contracts.json
  forbidden_write_paths:
  - apps/**
  - packages/**/*.py
  - packages/contracts/openapi/**
  - packages/contracts/jsonschema/**
  - packages/contracts/src/**
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/localization/**
  - migrations/**
  - deploy/**
  - plugins/**
  - tests/**
  - tools/**
  - scripts/**
  - AGENTS.md
  - .codex/AGENTS.md
  - docs/architecture/ui/target-pilot/**
  - docs/architecture/ui/custometry-web-implementation-source-contract-v1.md
  - docs/architecture/ui/ui-program-retirement.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: []
  commands:
  - uv run python -m tools.custometry_quality.validate_blueprints
  - uv run python -m tools.custometry_quality.generate_requirement_index --check
  - uv run python -m tools.custometry_quality.generate_docs_index --check
  - uv run python -m tools.custometry_quality.check_docs_links
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.check --scope local
  - uv run --locked python -m tools.check --scope pre-push
  proof_boundary: documentation-semantic-and-static-contract-reconciliation
  evidence_target: .codex/delivery/evidence/W31-RECONCILE-DOCUMENTATION-AUDITS.md
escalation_triggers:
- normative_product_change
- material_user_scope_change
- external_or_irreversible_side_effect
- secrets_or_production_authority
- write_outside_allowed_scope
evidence:
- .codex/delivery/evidence/W31-RECONCILE-DOCUMENTATION-AUDITS.md
---

# Outcome

Apply the reconciliation accepted by the user on 2026-09-06 to the existing
working checkout. Preserve requirement IDs and the accepted published pilot authority,
synchronize machine/human semantics, and correct the affected derived documents.
Document exact remaining contract proposals and compatibility seams rather than
inventing source/privacy/workload values or claiming runtime completion.

# Non-goals

No product code, API/storage migration, dependency update, browser change,
new UI program, forecast resumption, or first
external release selection. Archive corrections are evidence, not runnable
instructions. Preserve the accepted published pilot/source-contract/retirement lineage.

# Work and repair boundary

The accepted review settles documentation repairs; this user instruction
explicitly authorizes their normative synchronization. A new behavioral policy
outside that accepted selection remains proposed. Preserve existing foreign
changes using the captured current-tree baseline, not HEAD. Three independent
work assignments divide blueprint, UI-derived, and contract-proposal ownership;
the root owns other derived docs, integration, generated indexes, and evidence.

# Acceptance evidence

All accepted findings have an applied correction or a concrete linked contract
proposal/compatibility obligation; rejected audit edits remain excluded. Parse
all relevant YAML/JSON fences, verify ID preservation and changed mirror clauses,
run the focused documentation gates and the local grouped profile, and distinguish
pre-existing unrelated failures with baseline evidence. No static result implies
browser/database/security/runtime/release readiness.


# Publication clarification

The user explicitly authorized commit and publication into main, then required
already accepted main decisions to remain. The isolated publication branch is
based on `d5ecbd33c1fd582058ec3514e2084820c8a3f1c2`; the shared local checkout and
its foreign edits remain untouched. Preserve current target-pilot composition,
navigation/interactions, ADR-0007, endpoint/risk-based proof, retired-program
status, Web frontier, and all existing implementation. The full audited set
includes 100 already accepted local product IDs absent from this remote base;
the named authoring/source contracts, research/coverage inputs and matching
surface requirement metadata are the necessary publication closure. No existing
remote requirement ID or executable route/permission is removed.

The initial local-baseline evidence is historical. Refresh compatibility facts
against the implemented Artifact Lifecycle, Execution and in-app Notifications,
and record final source/static and independent review evidence. Publish through
the repository's protected-main PR/required-CI workflow. This authority does not
include deployment, branch-protection changes or adoption of the four proposed
economic/resource/security contracts.
