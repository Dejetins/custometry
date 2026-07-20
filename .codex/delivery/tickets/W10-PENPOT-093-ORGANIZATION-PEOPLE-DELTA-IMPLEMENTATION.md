---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
ticket_id: W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION
status: accepted
workstream_id: W10
summary: Implement the accepted product 0.9.3 and UI 0.6.3 organization, department access and ownership, and People & Creators delta in the canonical Penpot file from the repaired recovery baseline revision 197.
requirement_ids: [UC-028, UC-029, RBAC-019, RBAC-020, RBAC-021, RBAC-022, RBAC-023, RBAC-024, RBAC-025, RBAC-026, RBAC-027, RBAC-028, TEST-INV-076, TEST-INV-077, TEST-INV-078, TEST-INV-079, TEST-INV-080, TEST-INV-081, TEST-INV-082, TEST-INV-083, TEST-INV-084, TEST-INV-085, TEST-INV-086, TEST-INV-087, TEST-INV-088, V1-AC-037, V1-AC-038, V1-AC-039, V1-AC-040, V1-AC-041, V1-AC-042, V1-AC-043]
blockers: [W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION, W08-PENPOT-ANALYTICS-BASELINE-RECOVERY, W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/agents/iteration_report_template.md
  - .codex/delivery/specs/organization-department-access-and-contributor-insights.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/system-design.md
  - docs/architecture/bounded-context-map.md
  - docs/contracts/ui-route-contract.md
  - docs/contracts/ui-surface-contract.md
  - docs/generated/requirement-index.json
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-route-contracts.schema.json
  - packages/contracts/routes/ui-surface-contracts.json
  - packages/contracts/routes/ui-surface-contracts.schema.json
  - packages/localization/locales/en/route-titles.json
  - packages/localization/locales/ru/route-titles.json
  - .codex/delivery/tickets/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
  - .codex/delivery/evidence/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
  - .codex/delivery/tickets/W08-PENPOT-ANALYTICS-BASELINE-RECOVERY.md
  - .codex/delivery/evidence/W08-PENPOT-ANALYTICS-BASELINE-RECOVERY.md
  - .codex/delivery/tickets/W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT.md
  - .codex/delivery/evidence/W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT.md
external_write_scope:
  provider: penpot
  file_id: 7cd71457-8d32-8044-8008-549f83bb4645
  expected_start_revision: 197
  allowed_operations: [create_components, create_component_board, create_frames, edit_existing_target_frames, edit_existing_component_examples, edit_design_annotations, edit_prototype_flows]
  forbidden_operations: [create_or_replace_file, delete_existing_stable_id_frames, rename_existing_stable_ids, change_product_scope, change_route_identity, edit_other_penpot_files]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - docs/**
    - packages/**
    - apps/**
    - plugins/**
    - deploy/**
    - migrations/**
    - .codex/delivery/tickets/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/tickets/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
    - .codex/delivery/evidence/W06-PENPOT-ANALYTICS-DENSITY-REPAIR.md
    - .codex/delivery/tickets/W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT.md
    - .codex/delivery/evidence/W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT.md
    - .codex/delivery/tickets/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
    - .codex/delivery/tickets/W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT.md
    - .codex/delivery/evidence/W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: [penpot-design-delivery]
  commands:
    - confirm W08 and W09 are accepted with passed terminal evidence
    - compute one ordered SHA-256 fingerprint over every context_sources file before the first Penpot write and compare it again immediately before verdict
    - confirm Penpot currentFile.fileId equals 7cd71457-8d32-8044-8008-549f83bb4645 and current revision equals 197 before the first write
    - individually export and visually review C25, UI-ORG-001, UI-ORG-002, UI-PEOPLE-001, UI-PEOPLE-002, UI-ADMIN-019, UI-ADMIN-020, UI-ADMIN-003, UI-ADMIN-018, UI-RPT-001, UI-DASH-001, and prototype flow 10 after the final write
    - confirm all 116 route frames, 25 overlay/state frames, and 5 system surfaces have unique contract-backed stable UI-IDs with no duplicate missing or orphan IDs
    - validate the C25 local component inventory, named prototype flow 10 structure, keyboard/focus annotations, and non-color-only state treatment
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - git diff --check
  proof_boundary: canonical-penpot-product-0.9.3-ui-0.6.3-organization-access-ownership-and-people-visual-delta
  evidence_target: .codex/delivery/evidence/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md]
---

# Outcome

The canonical Penpot file visibly represents the accepted `0.9.3/0.6.3`
organization, department access/ownership, and privacy-safe People & Creators
contract. Six new route frames, component board C25, Company navigation, and
prototype flow 10 are added without replacing the file, renaming an existing
stable UI-ID, creating a new overlay, or claiming runtime authorization.

# Non-goals

- Do not repeat W08 or W09 as an audit and do not change blueprints,
  architecture, executable contracts, permissions, localization, or product
  meaning.
- Do not implement browser/API/persistence/policy evaluation, migrations,
  activity projections, email/XLSX, or runtime accessibility.
- Do not show employee rankings, productivity scores, exact login surveillance,
  hidden draft titles/counts, raw audit streams, email recipient history, HR
  decisions, or administrator-as-automatic-business-access.
- Do not add HRIS/SCIM/OIDC synchronization, matrix reporting, project teams,
  B2B hierarchy, physical per-department data copies, a second theme, or a new
  chart engine.

# External write authority and guards

The only authorized external target is the existing Penpot file
`7cd71457-8d32-8044-8008-549f83bb4645`. Before writing, verify W08, analytics
baseline recovery, and W09 terminal evidence, exact file ID, exact revision
`197`, and one ordered fingerprint of
all context sources. Stop without writes on any mismatch, Penpot unavailability,
missing source, concurrent revision drift, or unresolved product meaning.
Repeat the identical fingerprint immediately before the terminal verdict.

# Work and repair boundary

Use `penpot-design-delivery` for Penpot inspection, writes, and artifact-level
visual proof. Use `ui-ux-pro-max` only if an unresolved design-direction
decision is within scope. Preserve the Frost tokens, W06 compact density,
icon-and-label expanded sidebar, icon-only collapsed sidebar, centered
controls, stable shell geometry, keyboard-visible focus, non-color-only states,
and existing route identities.

Execute in this order:

1. Add component board `C25 Organization, Ownership & People` after C24. It
   must include compact organization tree/table rows, member and leader scope
   assignments, department/data-policy and cross-department-grant summaries,
   ownership/creator badges, contributor cards plus table alternative,
   manager/self/public activity variants, and accessible empty/denied/
   transferred/inactive/expired states.
2. Update the shell/navigation examples so Company contains `Organization` and
   `People & Creators`; keep Administration configuration separate from
   business browsing. Permission-filtered absence must not reveal hidden
   departments or counts.
3. Create `UI-ORG-001` as a compact tree/table discovery surface with the
   viewer's primary unit, authorized company/division/department/team nodes,
   statuses/successors, filtered member/leader counts, search, and clear open
   action. Include empty organization and unassigned-legacy-member states.
4. Create `UI-ORG-002` as the Department Hub: identity/leadership, curated
   reporting catalog, governed data products, visible creators, recent
   publications, ownership, partial-access disclosure, and no-visible-resource
   state. Counts are visibly access-filtered.
5. Create `UI-PEOPLE-001/002` as compact People & Creators directory/profile
   surfaces. Show authorized published work, department, expertise, creator/
   maintainer/reviewer labels, self/manager/public variants, and bounded 30/90-
   day contribution summaries. Never resemble a leaderboard.
6. Create `UI-ADMIN-019/020` as organization editor/detail routes with structure
   versions, primary assignments, explicit unit/subtree/workspace leadership,
   department policy, bounded grants, transfer/merge/departure lifecycle,
   successor mapping, ownership impact preview, dirty guard, publish, and audit
   deep link.
7. Update only `UI-ADMIN-003`, `UI-ADMIN-018`, `UI-RPT-001`, and `UI-DASH-001`
   to expose primary department, effective-access explanation, department
   owner versus creator, authorized creator discovery, and grant expiry without
   widening their existing purpose or density.
8. Add named prototype flow 10 from organization setup and member/leader
   assignment through policy/ownership preview, Department Hub, People profile,
   authorized report/dashboard discovery, and return to origin. Include one
   denied/expired-grant branch and one transfer/ownership-continuity branch.

An organization node is never presented as authorization by itself. A leader
scope is an explicit assignment. Technical administrator status does not imply
business-content, PII, or employee-activity visibility. Snapshot visibility is
visually distinct from dataset, drill-down, edit, run, export, and PII access.

# Acceptance evidence

- Evidence records exact file ID, start/end revisions, repeated repository
  fingerprint, created/changed board IDs, C25 component IDs, and compatible
  repairs.
- C25, all six new route frames, the four declared existing route frames, and
  flow 10 receive individual visual verdicts from fresh exports.
- The final global reconciliation is exactly `116/25/5`, with no duplicate,
  missing, orphaned, renamed, or deleted stable UI-ID.
- Frost density and sidebar behavior are preserved; text/buttons are aligned;
  no clipping, overlap, unjustified empty space, hidden-count leak, or
  leaderboard treatment remains on target surfaces.
- Manager, self, ordinary viewer, administrator, denied, expired, transfer,
  inactive/merged, empty, and partial-access differences are explicit and do
  not rely on color alone.
- Repository schemas and validators pass. Evidence is Penpot design proof only;
  browser, runtime accessibility, authorization correctness, persistence,
  activity projection, calculation, export, performance, deployment, and
  release proof remain excluded.
