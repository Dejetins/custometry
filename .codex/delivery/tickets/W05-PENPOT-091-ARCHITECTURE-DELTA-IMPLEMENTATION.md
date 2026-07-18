---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.1-draft
ticket_id: W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION
status: ready
workstream_id: W05
summary: Update the canonical Penpot file from the accepted revision-124 audit baseline to complete product 0.9.1 and UI 0.6.1 design coverage, without changing product or route contracts.
requirement_ids: [UC-001, UC-002, UC-003, UC-004, UC-005, UC-006, UC-007, UC-008, UC-009, UC-010, UC-011, UC-012, UC-013, UC-014, UC-015, UC-016, UC-017, UC-018, UC-019, UC-020, UC-021, UC-022, UC-023, UC-024, UC-025, UC-026, OUTLIER-001, OUTLIER-002, OUTLIER-003, OUTLIER-004, OUTLIER-005, OUTLIER-006, OUTLIER-007, OUTLIER-008, OUTLIER-009, OUTLIER-010, OUTLIER-011, OUTLIER-012, SEGMENT-001, SEGMENT-002, SEGMENT-003, SEGMENT-004, SEGMENT-005, SEGMENT-006, SEGMENT-007, SEGMENT-008, SEGMENT-009, SEGMENT-010, SEGMENT-011, SEGMENT-012, SEGMENT-013, SEGMENT-014, SEGMENT-015, SEGMENT-016, SEGMENT-017, SEGMENT-018, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, TEST-INV-049, TEST-INV-050, TEST-INV-052, TEST-INV-053, TEST-INV-054, TEST-INV-055, TEST-INV-056, TEST-INV-057, TEST-INV-058, TEST-INV-059, TEST-INV-061, TEST-INV-062, TEST-INV-063, TEST-INV-064, TEST-INV-065, AC-041, AC-042, AC-043, AC-044, AC-045, V1-AC-029, V1-AC-030, V1-AC-031]
blockers: [W03-PENPOT-ARCHITECTURE-DELTA-AUDIT, W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/agents/iteration_report_template.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/system-design.md
  - docs/architecture/bounded-context-map.md
  - docs/contracts/ui-route-contract.md
  - docs/contracts/ui-surface-contract.md
  - docs/generated/requirement-index.json
  - .codex/delivery/tickets/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
  - .codex/delivery/evidence/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
  - .codex/delivery/tickets/W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT.md
  - .codex/delivery/evidence/W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT.md
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-route-contracts.schema.json
  - packages/contracts/routes/ui-surface-contracts.json
  - packages/contracts/routes/ui-surface-contracts.schema.json
  - packages/localization/locales/en/route-titles.json
  - packages/localization/locales/ru/route-titles.json
external_write_scope:
  provider: penpot
  file_id: 7cd71457-8d32-8044-8008-549f83bb4645
  expected_start_revision: 124
  allowed_operations: [create_components, create_frames, create_variants, edit_existing_target_frames, edit_prototype_flows, edit_design_annotations]
  forbidden_operations: [create_or_replace_file, delete_stable_id_frames, rename_stable_ids, change_product_scope, change_route_identity, edit_other_penpot_files]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
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
    - .codex/delivery/tickets/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
    - .codex/delivery/evidence/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
    - .codex/delivery/tickets/W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT.md
    - .codex/delivery/evidence/W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: ["product-design:audit"]
  commands:
    - confirm W03-PENPOT-ARCHITECTURE-DELTA-AUDIT and W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT are accepted and both evidence verdicts are passed
    - record one SHA-256 fingerprint for the complete ordered context_sources set before the first Penpot write and compare it again before verdict
    - confirm Penpot currentFile.fileId equals 7cd71457-8d32-8044-8008-549f83bb4645 and current revision equals 124 before the first write
    - record start and end Penpot revision plus page, local-component, route-frame, overlay/state-frame, system-surface, duplicate-ID, and named-flow counts
    - reconcile every route and non-route surface against the current machine-readable contract set after the final Penpot write
    - perform individual visual review for every one of the 110 route frames, 25 overlay/state frames, and 5 system-surface frames at the final revision
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - git diff --check
  proof_boundary: canonical-penpot-product-0.9.1-ui-0.6.1-architecture-delta-and-visual-coverage
  evidence_target: .codex/delivery/evidence/W05-PENPOT-091-ARCHITECTURE-DELTA-IMPLEMENTATION.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

The canonical Penpot file is updated in place from the accepted revision-124
baseline to a complete, internally consistent visual representation of product
specification `0.9.1-draft` and UI specification `0.6.1-draft`. All 110 route
frames, 25 overlays, 5 system surfaces, 19 cross-surface capabilities, required
component families, and eight representative flows have explicit design
coverage. Existing stable IDs and the Frost design language are preserved.

# Non-goals

- Do not repeat W03 as a read-only audit or rewrite W03/W04 evidence.
- Do not change product requirements, route identities, permissions, UI
  contracts, localization, architecture, or implementation status.
- Do not implement Web, API, persistence, workers, analytics, email, XLSX, or
  runtime behavior and do not claim browser or accessibility-runtime proof.
- Do not add another color theme, customer-specific fork, mobile application,
  B2B ontology, future connector UI, or post-v1 analytical method.
- Do not add automatic-K, Gaussian Mixture, HDBSCAN, Isolation Forest, or
  multivariate anomaly detection to the v1 design.

# External write authority and guards

The only authorized external mutation target is the existing canonical Penpot
file `7cd71457-8d32-8044-8008-549f83bb4645`. The ticket authorizes in-place
Penpot writes necessary for its outcome; it does not authorize creating or
replacing a file. Before the first design read/write, confirm both predecessor
tickets are terminal with passed evidence, the file ID matches, and the live
revision is exactly `124`. If the revision differs, the Penpot MCP is
unavailable, the file cannot be enumerated, or another editor changes the file
during execution, stop as `blocked` before making further writes.

Record one ordered fingerprint over every `context_sources` file before the
first Penpot write and repeat it immediately before verdict. Repository input
drift is a blocker. The Penpot revision is expected to increase because this is
a write ticket; evidence must distinguish the observed start revision, the
agent's own write sequence, and the final revision.

Use this exact command at both fingerprint checkpoints and record only the
final digest:

```bash
shasum -a 256 AGENTS.md .codex/AGENTS.md .codex/agents/iteration_report_template.md custometry-technical-blueprint-ru.md custometry-technical-blueprint-human-ru.md custometry-ui-blueprint-ru.md docs/architecture/system-design.md docs/architecture/bounded-context-map.md docs/contracts/ui-route-contract.md docs/contracts/ui-surface-contract.md docs/generated/requirement-index.json .codex/delivery/tickets/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md .codex/delivery/evidence/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md .codex/delivery/tickets/W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT.md .codex/delivery/evidence/W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT.md packages/contracts/routes/ui-routes.json packages/contracts/routes/ui-route-contracts.json packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json packages/contracts/routes/ui-surface-contracts.schema.json packages/localization/locales/en/route-titles.json packages/localization/locales/ru/route-titles.json | shasum -a 256
```

Repository contracts are fixed inputs. A newly discovered product, route,
permission, privacy, or ownership ambiguity is recorded as a blocker for a
separate decision; it is never resolved by silently changing Penpot semantics.

# Work and repair boundary

Use `ui-ux-pro-max` as the primary execution skill and the Penpot MCP as the
design writer. Add `product-design:audit` only for the declared final visual
proof boundary. Work in the canonical file and preserve all compatible
foundations, components, stable route IDs, page ownership, and the single Frost
theme. In-scope visual repairs may correct density, alignment, button-label
centering, collisions, clipping, navigation-icon behavior, and component-state
consistency where required by the current contracts.

Execute the design delta in this order:

1. Create or extend the missing component families identified by W03:
   research/comments, governed file import, metric presentation,
   BrandProfile/CompanyPack, resource access policy, and `C23 Data Treatment &
   Segmentation`. Reuse existing Frost tokens and owned primitives.
2. Add `UI-OVR-025` Data Treatment and Sensitivity Drawer. Update
   `UI-AN-002`, `UI-AN-011`, `UI-AN-012`, and `UI-SEG-001...003` to expose the
   governed population, quantile/IQR/MAD, flag/exclude/winsorize, impact,
   shared-`vs LY`, Result Trust, progress, privacy, and fit/assignment states.
3. Add the eighth prototype flow from population selection through treatment,
   method/group-count selection, preview, publication, and Result Trust.
4. Add `UI-OVR-024` Discussion and Comments Drawer plus `UI-AN-013...014`
   Research Library/Detail, including treatment/segment evidence in research
   blocks and an explicit comment-versus-finding boundary.
5. Add `UI-DATA-021...031`: methodology, governed CSV/XLSX import, MetricGroup,
   and NumberFormat lifecycle frames.
6. Add `UI-ADMIN-013...018`: workspace brand assignment, BrandProfile,
   CompanyPack, and report/dashboard resource-access policy frames.
7. Reconcile and visually inspect all route, overlay, system, component, state,
   responsive, locale, accessibility-annotation, reduced-motion, and prototype
   coverage at the final revision. Repair only contract-compatible defects.

The treatment workflow must make `Flag` the default and require an impact
acknowledgement before `Exclude` or `Winsorize`. It must disclose method,
population/grain/window/peer scope, fitted bounds, affected customer/order/value
share, before/after metric delta, shared versus independent LY bounds, DQ
separation, and limitations. Published/viewer surfaces are inspect-only and
resolve the pinned treatment version through Result Trust.

The segmentation workflow must support rule/RFM, quantile/equal-width/custom
buckets, stratified distributions, and exact-K KMeans with explicit final group
count. It must expose ordered labels, ties/missing handling, resolved bounds,
features, scaling/imputation, seed, fit versus assignment population, member
count/value share, profiles, stability, silhouette/applicability limitations,
distance/confidence where available, immutable membership identity, progress,
cancellation, permission, and PII-safe states.

# Acceptance evidence

- The final Penpot evidence records the canonical file ID, start revision
  `124`, end revision, repository fingerprint, exact changed/created frame and
  component IDs, and any repaired compatible defect.
- The final structural scan contains exactly 110 unique route IDs, 25 unique
  overlay IDs, and 5 unique system-surface IDs, with no missing, duplicate,
  orphaned, or silently renamed stable ID. All 19 route-backlog frames and both
  `UI-OVR-024...025` exist.
- Every cross-surface capability and every `UC-001...UC-026` binding resolves
  to its declared route/overlay/system/component rationale. `C23` and all eight
  representative prototype flows are present and named.
- Individual visual review covers all 140 route/overlay/system frames at the
  final revision. Evidence records pass/fail per stable ID and confirms no
  clipping, unintended overlap, broken parallel alignment, excessive KPI or
  header whitespace, uncentered button labels, hidden-sidebar abbreviation, or
  inconsistent Frost component state remains.
- Expanded navigation shows icon plus label; collapsed navigation shows only
  accessible Apple-style icons with tooltip/accessible-name annotations and a
  discoverable restore control.
- Responsive samples, EN/RU text pressure, contrast, keyboard/focus notes,
  table/chart alternatives, Result Trust, return-to-origin, loading/error/
  forbidden/empty/stale states, and reduced-motion annotations are explicitly
  reviewed. This is design evidence, not browser/runtime proof.
- Route/surface validators, both JSON Schemas, delivery-ticket validation, and
  `git diff --check` pass against unchanged repository contracts.
- The evidence verdict is `passed` only when the complete target is present.
  Partial useful design work leaves the ticket `active` or records a truthful
  `blocked` state; it is never accepted by count extrapolation.
