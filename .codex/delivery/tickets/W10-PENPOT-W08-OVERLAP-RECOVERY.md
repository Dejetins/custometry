---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.2-draft
ticket_id: W10-PENPOT-W08-OVERLAP-RECOVERY
status: accepted
workstream_id: W10
summary: "Repair the confirmed W08 visual composition defect in the canonical Penpot baseline: nine W08 delta boards currently cover pre-existing sibling content on their stable route frames."
requirement_ids: [UC-027, METRIC-017, METRIC-018, METRIC-019, METRIC-020, DISCOUNT-017, DISCOUNT-018, METHOD-009, METHOD-010, METHOD-011, METHOD-012, METHOD-013, METHOD-014, PVM-001, PVM-002, PVM-003, PVM-004, PVM-005, PVM-006, V1-AC-032, V1-AC-033, V1-AC-034, V1-AC-035, V1-AC-036]
blockers: [W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION, W08-PENPOT-ANALYTICS-BASELINE-RECOVERY, W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/agents/iteration_report_template.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/system-design.md
  - docs/contracts/ui-route-contract.md
  - docs/contracts/ui-surface-contract.md
  - docs/generated/requirement-index.json
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-route-contracts.schema.json
  - packages/contracts/routes/ui-surface-contracts.json
  - packages/contracts/routes/ui-surface-contracts.schema.json
  - .codex/delivery/tickets/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
  - .codex/delivery/evidence/W08-PENPOT-092-DISCOUNT-METHODOLOGY-DELTA-IMPLEMENTATION.md
  - .codex/delivery/tickets/W08-PENPOT-ANALYTICS-BASELINE-RECOVERY.md
  - .codex/delivery/evidence/W08-PENPOT-ANALYTICS-BASELINE-RECOVERY.md
  - .codex/delivery/tickets/W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT.md
  - .codex/delivery/evidence/W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT.md
  - .codex/delivery/tickets/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
external_write_scope:
  provider: penpot
  file_id: 7cd71457-8d32-8044-8008-549f83bb4645
  expected_start_revision: 196
  allowed_operations: [edit_existing_target_frames, remove_obsolete_nonstable_sibling_boards, edit_design_annotations]
  forbidden_operations: [create_or_replace_file, create_or_delete_stable_id_frames, rename_stable_ids, create_components, create_component_board, create_frames, edit_existing_component_examples, edit_prototype_flows, change_product_scope, change_route_identity, edit_other_penpot_files]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W10-PENPOT-W08-OVERLAP-RECOVERY.md
    - .codex/delivery/evidence/W10-PENPOT-W08-OVERLAP-RECOVERY.md
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
    - .codex/delivery/tickets/W08-PENPOT-ANALYTICS-BASELINE-RECOVERY.md
    - .codex/delivery/evidence/W08-PENPOT-ANALYTICS-BASELINE-RECOVERY.md
    - .codex/delivery/tickets/W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT.md
    - .codex/delivery/evidence/W09-ORGANIZATION-ACCESS-CONTRIBUTOR-CONTRACT.md
    - .codex/delivery/tickets/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: [product-design:audit]
  commands:
    - confirm W08, W08 analytics baseline recovery, and W09 are accepted with passed terminal evidence
    - compute one ordered SHA-256 fingerprint over every context_sources file before the first Penpot write and compare it again immediately before the terminal verdict
    - confirm Penpot currentFile.fileId equals 7cd71457-8d32-8044-8008-549f83bb4645 and current revision equals 196 immediately before the first write
    - verify, before mutation, that each listed stable route frame has exactly one direct W08 child board and all named obsolete direct sibling boards; stop without writes on any mismatch
    - retain the visible W08 delta board as the single integrated content composition and remove only the named obsolete non-stable sibling boards which it currently covers
    - individually export and visually review UI-DATA-008, UI-DATA-010, UI-DATA-013, UI-DATA-014, UI-DATA-021, UI-DATA-022, UI-AN-010, UI-AN-012, and UI-AN-014 after the final write
    - run a global stable-frame geometry, sibling containment, z-order, and export-candidate audit; exclude only visually confirmed intentional overlay states
    - confirm all 110 route frames, 25 overlay/state frames, and 5 system surfaces retain stable unique UI-IDs with no duplicate, missing, orphaned, renamed, or deleted stable UI-ID
    - reconfirm UI-AN-002 and UI-AN-011 preserve their accepted recovery compositions without new clipping or overlap
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - git diff --check
  proof_boundary: canonical-penpot-W08-baseline-visual-overlap-recovery
  evidence_target: .codex/delivery/evidence/W10-PENPOT-W08-OVERLAP-RECOVERY.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W10-PENPOT-W08-OVERLAP-RECOVERY.md]
---

# Outcome

The nine confirmed W08 composition defects are repaired in place.  Each
stable route frame contains one visible, readable W08 composition instead of a
later child board covering an obsolete sibling panel, table, or chart.

# Non-goals

- Do not perform any W10 implementation, create C25, create the six W10 route
  frames, modify the four W10 target frames, or add flow 10.
- Do not add or delete stable UI-ID frames, components, component boards,
  prototype flows, pages, overlays, or system surfaces.
- Do not alter product blueprints, architecture, executable contracts,
  localization, route identity, permissions, or product meaning.
- Do not modify the accepted W08, W08 recovery, W09, or W10 ticket/evidence
  artifacts.

# External write authority and guards

The only authorized external target is the existing Penpot file
`7cd71457-8d32-8044-8008-549f83bb4645`. Before writing, verify the accepted
predecessor evidence, exact file ID, exact revision `196`, the complete
pre-write target structure, and one ordered SHA-256 fingerprint over every
context source. Stop without writes on a mismatch, MCP unavailability,
concurrent revision drift, missing source, or a different target structure.
Repeat the identical fingerprint immediately before the terminal verdict.

# Repair boundary

Use `ui-ux-pro-max` as the primary execution skill, the Penpot MCP for design
writes, and `product-design:audit` for final visual proof. Preserve Frost
tokens, shell geometry, compact W06 density, all stable route identities,
W08's accepted visual language and semantic information.

For each target below, retain the direct W08 board as the visible integrated
content composition. Remove only the named direct non-stable sibling boards it
currently covers; never remove or rename a stable route, overlay, or system
frame. Rename the retained non-stable W08 child to `Integrated W08 content /`
followed by the stable UI-ID, so its repaired role is explicit.

| Stable route | Retained W08 child | Remove only these obsolete direct siblings |
| --- | --- | --- |
| UI-DATA-008 | `W08 / Discount Methodology Delta` | `Form Panel`, `Form Summary` |
| UI-DATA-010 | `W08 / Discount Methodology Delta` | `Form Panel`, `Form Summary` |
| UI-DATA-013 | `W08 / Discount Methodology Delta` | `Data Table` |
| UI-DATA-014 | `W08 / Discount Methodology Delta` | `Form Panel`, `Form Summary` |
| UI-DATA-021 | `W08 / Discount Methodology Delta` | `Data Table`, `UI-DATA-021 / Contract focus` |
| UI-DATA-022 | `W08 / Discount Methodology Delta` | `Form Panel`, `Form Summary`, `UI-DATA-022 / Contract focus` |
| UI-AN-010 | `W08 / Discount Methodology Golden Slice` | `Primary Chart`, `Data Table` |
| UI-AN-012 | `W08 / Discount Methodology Delta` | `Primary Chart`, `Data Table` |
| UI-AN-014 | `W08 / Discount Methodology Delta` | `Primary Chart`, `Research blocks · narrative · metric group · chart · table · finding · methodology` |

The retained board must be aligned to the removed content's top-left origin,
remain inside the stable route bounds, and have no non-contained direct board
overlap with sibling content after repair. Intentional modal/overlay states are
not targets and must be verified visually rather than inferred from geometry.

# Acceptance evidence

- Evidence records the exact file ID, start/end revisions, repeated repository
  fingerprint, changed and deleted non-stable child board IDs, and the W10
  pre-write incident as historical context only.
- Fresh exports give an individual pass/fail verdict for all nine repaired
  targets; no target shows covered content, clipping, or unexplained overlap.
- Global reconciliation is exactly `110/25/5` with no duplicate, missing,
  orphaned, renamed, or deleted stable UI-ID.
- The required global audit checks root geometry, non-contained sibling
  geometry, z-order, and fresh candidate exports; only visually verified
  intentional overlays may be excluded.
- UI-AN-002 and UI-AN-011 remain visually intact, and repository contracts and
  validators are unchanged and pass. Evidence is Penpot design proof only;
  browser, runtime, accessibility-runtime, authorization, calculation,
  persistence, export, performance, deployment, and release proof are
  excluded.
