---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.0-draft
ticket_id: W03-PENPOT-ARCHITECTURE-DELTA-AUDIT
status: accepted
workstream_id: W03
summary: Audit the canonical Penpot file against the fixed product 0.9.0 and UI 0.6 contract set, classify every required surface, and produce an implementation-ready design delta without editing Penpot.
requirement_ids: [UC-001, UC-002, UC-003, UC-004, UC-005, UC-006, UC-007, UC-008, UC-009, UC-010, UC-011, UC-012, UC-013, UC-014, UC-015, UC-016, UC-017, UC-018, UC-019, UC-020, UC-021, UC-022, UC-023, UC-024, RBAC-002, RBAC-005, RBAC-011, RBAC-012, RBAC-013, RBAC-014, RBAC-015, RBAC-016, RBAC-017, RBAC-018, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, TEST-INV-049, TEST-INV-050, TEST-INV-052, TEST-INV-053, TEST-INV-054, TEST-INV-055, TEST-INV-056, TEST-INV-057, TEST-INV-058, TEST-INV-059, AC-041, AC-042, AC-043, AC-044, AC-045, V1-AC-016, V1-AC-017, V1-AC-018, V1-AC-019, V1-AC-020, V1-AC-021, V1-AC-022, V1-AC-023, V1-AC-024, V1-AC-025]
blockers: []
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - custometry-technical-blueprint-ru.md
  - custometry-technical-blueprint-human-ru.md
  - custometry-ui-blueprint-ru.md
  - docs/architecture/system-design.md
  - docs/architecture/bounded-context-map.md
  - docs/contracts/ui-route-contract.md
  - docs/contracts/ui-surface-contract.md
  - docs/generated/requirement-index.json
  - .codex/delivery/evidence/W02-RECONCILE-UI-SURFACE-CONTRACT.md
  - packages/contracts/routes/ui-routes.json
  - packages/contracts/routes/ui-route-contracts.json
  - packages/contracts/routes/ui-route-contracts.schema.json
  - packages/contracts/routes/ui-surface-contracts.json
  - packages/contracts/routes/ui-surface-contracts.schema.json
  - packages/localization/locales/en/route-titles.json
  - packages/localization/locales/ru/route-titles.json
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
    - .codex/delivery/evidence/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
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
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: ["product-design:audit"]
  commands:
    - confirm W02-RECONCILE-UI-SURFACE-CONTRACT is accepted and its evidence verdict is passed
    - record one SHA-256 fingerprint for the complete ordered context_sources set before Penpot inspection and compare it again before verdict
    - confirm Penpot currentFile.fileId equals 7cd71457-8d32-8044-8008-549f83bb4645 before inspecting design content
    - record the observed Penpot revision at start and end plus page count, local component count, route-frame count, overlay/state-frame count, and system-surface count
    - classify every target route and non-route surface against the fixed machine-readable contract set
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
    - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - git diff --check
  proof_boundary: read-only-canonical-penpot-architecture-delta-and-complete-surface-accounting
  evidence_target: .codex/delivery/evidence/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence:
  - .codex/delivery/evidence/W03-PENPOT-ARCHITECTURE-DELTA-AUDIT.md
---

# Outcome

The canonical Penpot file has a complete, evidence-backed architecture delta
against product specification `0.9.0-draft` and UI specification
`0.6.0-draft`. Every target route, overlay, system surface, cross-surface
capability, foundation/component dependency, and representative flow is either
confirmed compatible, assigned an exact design delta, or recorded as a new
backlog surface. A subsequent write ticket can update Penpot without making
product, route, permission, or surface-ownership decisions.

# Non-goals

- Do not edit Penpot, rename or move its pages, create components or frames, or
  generate exports.
- Do not change product/UI requirements, route contracts, localization,
  architecture, application code, or runtime configuration.
- Do not treat a matching frame count, page count, or frame name as proof of
  component, state, permission, responsive, accessibility, or flow fidelity.
- Do not expand B2B, Yandex Metrica runtime, cloud/SaaS, private activation, or
  other explicit post-v1 scope.

# Requirement closure rule

Frontmatter lists only ticket-level use cases, authorization/routing seams, and
audit acceptance/invariant IDs. It deliberately does not duplicate hundreds of
per-surface requirements. The complete audited requirement set is the union of
every `source.requirement_ids` entry in `ui-route-contracts.json` and every
`requirement_ids` entry in `ui-surface-contracts.json`. The evidence matrix must
resolve that union through `docs/generated/requirement-index.json`; an unknown
or unaccounted ID is a blocker. This keeps one executable source for each
surface and prevents a second stale requirement list in the ticket.

# Work and repair boundary

Use the Penpot MCP only for read-only inspection of the canonical file ID
`7cd71457-8d32-8044-8008-549f83bb4645`. Record the live revision before the
audit; revision drift from the documented observation is expected and is not a
file-identity failure. Before the first Penpot read, confirm W02 is accepted,
its evidence verdict is `passed`, and record one ordered SHA-256 fingerprint of
the bytes of every `context_sources` file. This is one audit input snapshot,
not a prompt-pack pinning system. Repeat the same fingerprint and Penpot
revision observation before verdict. Stop if either changes during the audit.
Also stop before inspecting design content if the MCP is unavailable,
`currentFile.fileId` differs, the file cannot be enumerated, or a required
repository source cannot be loaded.

Use this same command before the first Penpot read and immediately before the
verdict; record only its final digest in evidence:

```bash
shasum -a 256 AGENTS.md .codex/AGENTS.md custometry-technical-blueprint-ru.md custometry-technical-blueprint-human-ru.md custometry-ui-blueprint-ru.md docs/architecture/system-design.md docs/architecture/bounded-context-map.md docs/contracts/ui-route-contract.md docs/contracts/ui-surface-contract.md docs/generated/requirement-index.json .codex/delivery/evidence/W02-RECONCILE-UI-SURFACE-CONTRACT.md packages/contracts/routes/ui-routes.json packages/contracts/routes/ui-route-contracts.json packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json packages/contracts/routes/ui-surface-contracts.schema.json packages/localization/locales/en/route-titles.json packages/localization/locales/ru/route-titles.json | shasum -a 256
```

Treat the repository contract set as fixed. The audit may identify a potential
requirement gap, but it must record that as a blocker for a separate product or
architecture decision instead of changing the contract. Read-only evidence
repairs are limited to this ticket and its evidence record.

# Required audit matrix

The evidence record must account for all of the following with stable IDs,
Penpot page/frame/component references where observed, classification, exact
delta, dependency, and acceptance note:

1. All 110 route-level pages: 91 `baseline_verified` and 19 `backlog` in the
   current contract. Classifications are `compatible`, `needs_delta`,
   `replace`, `missing_backlog`, or `orphan`.
2. All 24 overlays, including route-backed Focus/Explore and the new discussion
   and comments drawer.
3. All 5 system surfaces and all 17 cross-surface capabilities.
4. Foundations and component coverage for Frost tokens, typography, icon
   navigation, collapsed/expanded sidebar, dense KPI strip, context bar,
   reportable blocks, filters, tables, charts/timelines, forms, state surfaces,
   comments, imports, metric presentation, branding, and access policy.
5. Permissions and privacy states for IA, WA, DS, AN, ML, OP, and VW, including
   deny-before-fetch, object access, PII masking, export/send ceilings, file
   imports, metric administration, and global-versus-workspace branding.
6. Research composition, analytical narrative, comments, `vs LY`, searchable
   filters, Result Trust, Chart-to-Data, Focus/Explore, export preflight,
   progress/ETA/cancellation, responsive behavior, localization,
   accessibility, reduced motion, and return-to-origin.
7. Representative prototype flows from UI blueprint section 16.5, plus any
   orphan or duplicate page/frame/component that would obstruct the write
   ticket.

# Acceptance evidence

- The live file ID matches the canonical ID; live revision and structural
  counts are recorded without overwriting the documented baseline observation;
  start/end revision and repository input fingerprint are identical.
- Every ID in all three machine-readable UI contracts is represented exactly
  once in the audit matrix or has an explicit non-frame rationale.
- The evidence separates verified current observations from target
  requirements and recommendations; no planned frame is reported as existing.
- Each required delta names its owning page/component/flow, prerequisite, and
  observable design acceptance condition.
- The evidence recommends a bounded first golden-screen/component slice and a
  safe order for the later Penpot write ticket without creating a standing
  plan, ledger, prompt pack, or platform Goal.
- Repository contract validators and both JSON Schema checks pass unchanged.
- Penpot and all forbidden repository paths remain unmodified.
