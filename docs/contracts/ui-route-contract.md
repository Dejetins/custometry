---
doc_id: CONTRACT-UI-ROUTE-001
title: Executable UI route contract
doc_version: 3
product_spec_version: 0.9.1-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [UC-025, UC-026, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, RBAC-002, RBAC-006, OUTLIER-001, SEGMENT-001]
status: accepted
proof_boundary:
  label: executable-route-contract-static
  exclusions: [router-implementation, api-authorization, browser-behavior, penpot-generation]
---

# Executable UI Route Contract

## Purpose

Custometry separates stable route identity from executable page policy:

- `packages/contracts/routes/ui-routes.json` is the compact identity registry;
- `packages/contracts/routes/ui-route-contracts.json` is the complete execution
  manifest for route guards, permissions, state, history, and design status;
- `packages/contracts/routes/ui-route-contracts.schema.json` is the portable
  JSON Schema for agents, generators, and external tooling;
- `packages/contracts/routes/ui-surface-contracts.json` maps routes, overlays,
  system surfaces, and cross-surface capabilities to all UI-visible use cases;
- `packages/contracts/routes/ui-surface-contracts.schema.json` is its portable
  coverage schema;
- `tools.custometry_quality.validate_route_registry` enforces repository-local
  semantic parity that JSON Schema cannot express by itself.

The split is intentional. URL identity, localization, generated navigation, and
redirect consumers should not change merely because a page gains a state,
permission, or Penpot status. Conversely, agents must not reconstruct route
security and history behavior from prose or role names.

## Authority and precedence

1. The normative product blueprint owns route, authorization, privacy, and
   lifecycle requirements.
2. The UI blueprint owns the page inventory, role hints, interaction, and design
   contract.
3. The identity registry owns canonical route IDs, paths, title keys, release,
   and implementation status.
4. The executable manifest owns machine-readable route execution metadata.
5. The UI surface manifest owns requirement-to-surface coverage and the
   route-versus-overlay-versus-component decision boundary.
6. The schemas and validator reject drift; they do not create product behavior.

Role hints are discoverability metadata only. Runtime authorization always uses
the central policy service and repeats sensitive checks in API/workers.

## Identity registry contract

The identity registry remains schema `2.0.0` and contains only:

- `id`;
- canonical `path`;
- locale-neutral `title_key`;
- target `release`;
- `status` (`planned`, `foundation`, or `implemented`).

Foundation utility routes remain separate from the 110 product route-level
pages. A stable path rename later requires deterministic redirects, deprecation,
telemetry, bookmark migration, and rollback.

## Executable manifest contract

The manifest is one atomically versioned file. Each of the 110 identity routes
has exactly one record with:

- route family and shell profile;
- stable navigation group and surface kind;
- UI role hints;
- authorization mode, minimum entry permission alternatives, action
  permissions, and object-scope flag;
- named guard, state, navigation, and safe-query profiles;
- Focus/Explore applicability;
- normative requirement references and UI blueprint ID;
- implementation status and Penpot frame synchronization status.

Shared profiles are declared once in the same manifest. A consumer resolves a
route by ID and then resolves the named profiles. Missing profiles, duplicate
routes, unknown permissions/roles/requirements, or identity drift are invalid.

## Authorization modes

| Mode | Meaning |
|---|---|
| `public` | no authenticated principal is required; input/redirect safety and endpoint-specific abuse controls still apply |
| `authenticated` | authenticated global surface without workspace resolution |
| `global_permission` | authenticated installation/global surface requiring any declared entry permission |
| `workspace_membership` | valid workspace resolution and membership; no additional route permission, but actions may require one |
| `workspace_permission` | membership plus any declared entry permission |
| `workspace_object_access` | membership plus access to the exact version/snapshot/block |
| `workspace_permission_or_object_access` | permission-based authoring/operations or explicitly granted object read/comment access |

`entry_permissions_any` defines the minimum alternatives for entering the
surface. `action_permissions` enumerates possible actions and never grants them.
The API evaluates the exact action, resource, row/data, PII, export, and policy
ceilings at execution time.

## Profile resolution

1. Load the complete manifest and verify `schema_version`.
2. Find exactly one route by ID or canonical path.
3. Verify that its identity fields match the compact registry.
4. Resolve guard, state, navigation, and query profiles by name.
5. Evaluate family/shell and protected guard before fetching resource data.
6. Use role hints only to construct stable navigation discoverability.
7. Evaluate `authorization.mode` and entry permissions through the policy API.
8. Render only after authorization; forbidden responses never reuse denied
   cached titles, counts, facets, or content.
9. Apply action permissions independently when the user invokes an action.

## History and query safety

Semantic resource changes, deep-linkable tabs, and Focus/Explore push history.
Presentation-only changes may replace the current entry. Menus, popovers, and
transient overlays do not alter the canonical route.

Only keys named by the resolved query profile are allowed. Raw PII, secrets,
source query values, and unredacted filter values are always forbidden. Durable
complex filters use an authorized Saved View ID; short-lived complex state uses
an opaque reference when the profile allows it.

Dirty editor navigation must guard sidebar navigation, workspace switch,
browser Back, reload, and close. Focus/Explore restores origin route, block,
scroll, and keyboard focus through Close, Escape, or browser Back.

## State and refresh behavior

The resolved state profile defines the minimum page states; an implementation
may add a more specific state only when it does not replace a required one.
Refreshable protected pages retain their last authorized result while showing
local freshness/loading. They must drop cached data immediately when current
authorization no longer permits it.

`status: planned` is not implementation evidence. Penpot `baseline_verified`
means only that the frame passed the declared design structural/visual review;
it does not prove browser behavior or accessibility.

## Validation and change rules

The repository validator checks:

- exact route coverage derived from the UI blueprint, currently 110 unique
  IDs/paths/title keys, without treating that number as a permanent ceiling;
- identity fields against the compact registry;
- roles against the UI blueprint row;
- product/UI/schema version agreement;
- route family, shell, profile references, authorization-mode invariants, and
  workspace-prefix rules;
- permission catalog and route permissions against the normative product
  permission catalog;
- requirement references against stable product requirement IDs;
- English/Russian title parity;
- all `UC-001...UC-026` surface bindings and references;
- overlay, system-surface, and cross-surface capability parity with the UI
  blueprint;
- the W03 historical 91 verified plus 19 backlog route-frame boundary, while
  later overlay/component deltas are tracked independently.

Product specification `0.9.1-draft` adds governed population treatment and
bucket/stratified/KMeans segmentation without introducing a new durable route.
Those behaviors attach to existing analytics, segmentation, and research
routes through executable requirement references plus reusable overlay and
capability contracts. A future standalone route still requires the route
decision criteria rather than a count-driven expansion.

Changing an identity path or field after a stable consumer exists is a route
compatibility change. Adding a profile/permission/state under the executable
manifest is compatible only when existing consumers can resolve the schema
version; otherwise publish a new schema version and deterministic migration.

## Agent usage

Agents should load the identity registry, executable route manifest, UI surface
manifest, and both schemas as one contract set. They first resolve the use case
to routes/overlays/capabilities through the surface manifest, then select a
route by stable ID, resolve profiles, read its requirement IDs, and consult the
matching UI blueprint row for screen-specific content/components. Agents must
not infer permission from a page title, role hint, navigation visibility,
Penpot frame, or workspaceKey.
