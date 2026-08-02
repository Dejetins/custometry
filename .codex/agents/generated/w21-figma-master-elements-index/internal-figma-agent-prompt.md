---
artifact_kind: executor_prompt
delivery_contract: global/v1
prompt_schema_version: 1
ticket_id: W21-FIGMA-MASTER-ELEMENTS-INDEX
workstream_id: W21
target_agent: internal_figma_platform_agent
codex_role: prompt_preparation_and_returned_artifact_review_only
direct_codex_figma_mcp_writes: forbidden
expected_evidence_target: .codex/delivery/evidence/W21-FIGMA-MASTER-ELEMENTS-INDEX.md
---

# Task

Create or update one dedicated Master Elements Index frame in the existing
Figma file:

```text
Custometry platform web ui
https://www.figma.com/design/ghv0Cv3ddqMvv3zFVvR22p/Custometry-platform-web-ui
```

You are the internal Figma platform agent and own the Figma-side creation work.
Codex is only the assistant that prepared this prompt and will later review the
returned artifacts; Codex must not perform direct Figma MCP writes for this
ticket.

This task is index-first. Do not create product screens, detail maps, route
frames, or a full prototype in this slice.

# Authoritative Sources

Use these repository sources as the source of truth and preserve their
requirement IDs, route IDs, and localized product copy:

- `AGENTS.md`
- `.codex/AGENTS.md`
- `.codex/delivery/specs/custometry-linear-workspace-ui-transition.md`
- `.codex/delivery/tickets/W19-LINEAR-REFERENCE-COMPLETION.md`
- `.codex/delivery/tickets/W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE.md`
- `custometry-technical-blueprint-ru.md`
- `custometry-technical-blueprint-human-ru.md`
- `custometry-ui-blueprint-ru.md`
- `docs/architecture/ui/linear-workspace-ui-transition-standard-v1.md`
- `docs/architecture/ui/linear-workspace-reference-manifest-v1.json`
- `docs/architecture/ui/custometry-linear-ui-migration-registry-v1.json`
- `packages/contracts/routes/ui-routes.json`
- `packages/contracts/routes/ui-route-contracts.json`
- `packages/contracts/routes/ui-surface-contracts.json`

The Roehub Figma file is a process reference only:

```text
https://www.figma.com/design/GBzmB9evtzqnAYNjp9W1sr/Roehub-Authenticated-Platform-UI
```

Use it to understand the index/map workflow, not as Custometry source content.

# Safety Rules

- Before editing, confirm the file identity and target page.
- Create exactly one index frame named `IDX-000 — Master Elements Index`.
- If an index frame already exists, update it in place. Do not duplicate it.
- If multiple index-like frames exist, stop and report their node IDs instead
  of merging or deleting them silently.
- Preserve the two existing large frames as context. Do not delete or redraw
  them in this task.
- Do not mark any row `accepted`; use `draft`, `planned`, or `review` unless
  product-owner approval is explicitly provided in the task input.
- Do not add optional/future features as required startup primitives.
- Do not create detail map frames or screen frames in this slice.

# Required Index Frame

Create a large, readable frame:

```text
IDX-000 — Master Elements Index
```

The index is not a screen. It is the design contract that governs later detail
maps and screens. It must contain these sections:

1. Source header
2. Status legend
3. Master primitive registry
4. Cross-surface capability registry
5. Overlay and system-state registry
6. Route-family coverage matrix
7. Role/access matrix
8. Required state matrix
9. Detail map plan
10. Product review queue
11. Duplicate/clipping/overlap audit
12. Next safe action

# Master Primitive Registry

Create stable primitive IDs beginning with `PRIM-001`. Each row must include:

- `primitive_id`
- `name`
- `type`: foundation, control, navigation, data-display, feedback, overlay,
  policy, chart, table, editor, operation, admin, auth, route-shell
- `source_ids`: requirement IDs, `UI-CAP-*`, `UI-OVR-*`, `UI-SYS-*`, route IDs,
  or component IDs `C00-C25`
- `domain_maps`: `MAP-01`, `MAP-02`, etc.
- `coverage`: required, optional, forbidden, conditional
- `required_states`: loading, empty, error, stale/degraded, forbidden,
  pending/review, success/failure, role/action unavailable
- `role_access`: IA, WA, DS, AN, ML, OP, VW, allowed, admin-only, explicit-grant,
  self/leader/grantee
- `figma_status`: draft, planned, review, accepted
- `product_review_state`: pending, needs-product-review, approved, rejected
- `notes`

Use the UI blueprint component families `C00-C25` as the initial component
coverage spine:

```text
C00 Components Index
C01 Button
C02 Icon Button & Menu Item
C03 Text Field & Textarea
C04 Select & Combobox
C05 Date, Time & Period
C06 Choice Controls
C07 App Sidebar & Nav Item
C08 Breadcrumb, Tabs, Pagination & Stepper
C09 Badge, Status & Avatar
C10 Card, KPI Card & Section
C11 Modal, Drawer & Popover
C12 Data Grid
C13 Filter Builder
C14 Chart Frame & Table Alternative
C15 Feedback, Empty & Skeleton
C16 Progress & ETA
C17 Result Trust
C18 Pipeline Node, Port & Edge
C19 Report Block
C20 Promotion Range Timeline
C21 Operations Status & Attempt Timeline
C22 Focus / Explore Surface & Toolbars
C23 Population Treatment & Segmentation Diagnostics
C24 Discount Components, Cap & PVM
C25 Organization, Access & People
```

# Cross-Surface Capability Registry

Represent all `UI-CAP-001...022` as capability rows and trace them to
primitives and maps:

```text
UI-CAP-001 Workspace routing, guards and return
UI-CAP-002 Searchable typed filters
UI-CAP-003 Previous-year comparison
UI-CAP-004 Metric groups and adaptive formats
UI-CAP-005 ChartSpec visualization
UI-CAP-006 Chart <-> Data table
UI-CAP-007 Focus / Explore
UI-CAP-008 Result Trust
UI-CAP-009 Research composition and findings
UI-CAP-010 Object-scoped comments
UI-CAP-011 Resource access policy
UI-CAP-012 ReportSnapshot and export preflight
UI-CAP-013 Verified-user report email
UI-CAP-014 Progress, ETA and cancellation
UI-CAP-015 Effective brand resolution
UI-CAP-016 Authorized PII-safe rendering
UI-CAP-017 Localization, accessibility and reduced motion
UI-CAP-018 Governed population and outlier treatment
UI-CAP-019 Bucket, stratified and KMeans segmentation
UI-CAP-020 Discount components, cap and PVM trust
UI-CAP-021 Organization-scoped effective access and ownership
UI-CAP-022 Privacy-safe People & Creators
```

# Overlay And System-State Registry

Represent all `25` overlays and `5` system surfaces from
`ui-surface-contracts.json`. The index must include their IDs, kind, mapped
primitive(s), required states, role/access implications, and target detail map.

System surfaces are:

```text
UI-SYS-001 403 Forbidden
UI-SYS-002 404 Not Found
UI-SYS-003 Session expired
UI-SYS-004 Maintenance
UI-SYS-005 Upgrade required
```

# Route-Family Coverage Matrix

Do not draw the `116` route screens in this task. Instead create a matrix that
confirms every route family is accounted for and shows the future map/screen
plan:

```text
Auth/Profile/Onboarding
Overview/Core
Data Foundation
Data Quality
Analytics/Research
Segmentation
Forecasting/Backtests/Monitoring
Promotion Journal
Dashboards
Reports/Exports/Email
Pipelines/Schedules
Runs/Operations
Notifications
Administration/Settings
Organization/People
Help/System
```

For each family, show:

- route ID range or exact IDs;
- primary roles;
- required capabilities;
- required overlays/system states;
- required/optional/forbidden/conditional primitives;
- future detail map ID;
- product review status.

# Detail Map Plan

Create map rows only inside the index frame. Do not create map frames yet.

Use these map IDs and names:

```text
MAP-01 Foundations, tokens, themes, motion, typography
MAP-02 Shell, navigation, command, workspace switcher, route guards
MAP-03 Forms, filters, date/period, comparison, dirty draft
MAP-04 Data Foundation, connections, catalog, file import, semantic model
MAP-05 Metrics, data quality, Data Guide, capability and remediation
MAP-06 Analytics, research, charts, tables, Result Trust, Focus/Explore
MAP-07 Segmentation, population treatment, discounts, PVM
MAP-08 Forecasting, backtests, models, monitoring
MAP-09 Dashboards, reports, comments, exports, email
MAP-10 Pipelines, runs, schedules, progress, operations
MAP-11 Notifications, help, system and error states
MAP-12 Admin, access policies, branding, organization, People & Creators
MAP-13 Auth, onboarding, profile security, recovery
```

Each map row must include `status`, `coverage`, `owner`, `source_ids`,
`blocked_by`, `next_prompt_needed`, and `product_review_state`.

# Required State Matrix

Every important primitive/capability/map must explicitly account for:

- loading
- empty
- error
- stale/degraded
- forbidden
- pending/review
- success/failure
- role/action unavailable

The UI must not hide missing backend/API/permission boundaries behind a pretty
static picture.

# Visual Treatment

Make the index easy to use inside Figma:

- one large organized frame, not several scattered boards;
- sticky-like header area with file identity, source versions, and legend;
- compact tables with clear section labels;
- color-coded statuses, but color must not be the only signal;
- readable at overview zoom and still detailed enough for row-level review;
- no clipping, overlap, placeholder copy, or text outside bounds;
- use Custometry `0.7.0` tokens and four-theme labels, but do not build theme
  matrices yet.

# Returned Report

Return a machine-readable report to Codex with:

```yaml
figma_file:
  url_or_key: <value>
  name: Custometry platform web ui
  checked_target_page: <page>
created_or_updated:
  index_frame:
    name: IDX-000 — Master Elements Index
    node_id: <figma node id>
    status: draft|review
counts:
  primitives: <number>
  capabilities: 22
  overlays: 25
  system_surfaces: 5
  route_families: <number>
  planned_maps: 13
status_summary:
  draft: <number>
  planned: <number>
  review: <number>
  accepted: 0
duplicate_audit:
  duplicate_index_frames: []
  duplicate_primitive_ids: []
  duplicate_map_ids: []
visual_audit:
  clipping: pass|fix_required
  overlap: pass|fix_required
  placeholder_copy: pass|fix_required
  long_ru_copy: pass|fix_required
pending_review:
  - <items>
next_safe_action: <one bounded next map prompt>
```

# Acceptance Bar

The task is ready for Codex review only when the single Master Elements Index
frame exists, traces product requirements to primitives/maps/states/roles, does
not create duplicate index frames, leaves all real map/screen creation for later
tickets, and returns the machine-readable report above.
