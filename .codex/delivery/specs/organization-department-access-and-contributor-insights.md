---
artifact_kind: delivery_spec
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
status: accepted
---

# Organization, Department Access, and Contributor Insights Specification

## Problem and user-visible outcome

Custometry currently separates platform roles, object access, row/data
ceilings, and PII grants, but it does not represent the customer's real
organizational hierarchy. A workspace therefore cannot assign every employee
to a department, give departments governed default data/reporting scopes,
delegate bounded responsibility to department leaders, or preserve department
ownership when an employee transfers or leaves.

The target capability adds an organization tree inside each company workspace,
department-owned reporting spaces, explicit cross-department grants, and a
privacy-safe People & Creators directory. An authorized user can discover the
reports, dashboards, research, and expertise of creators they are allowed to
see. A department leader or explicitly higher organizational leader can see a
bounded contribution summary for people in their assigned unit/subtree. A
technical administrator does not receive employee activity or business-data
access merely because they administer the platform.

The intended first-release user outcomes are:

- every active workspace member has exactly one effective primary organizational
  unit;
- the organization may contain company, division, department, and team units
  without cycles;
- functional role, organizational membership, leadership scope, data access,
  object access, and PII permission remain independent inputs to authorization;
- each department has a durable hub containing its curated reporting catalog,
  available governed data products, creators, and recent publications;
- a published resource can be owned by a department even when a named employee
  created it, so corporate knowledge survives transfer or departure;
- administrators may grant users or organizational units bounded access to
  another department's reports or data without duplicating physical datasets;
- creator and activity counts are computed only after authorization filtering
  and cannot reveal hidden objects;
- managers can inspect privacy-safe activity for their explicit unit/subtree,
  while ordinary users see only their own extended activity and other users'
  public, authorized creator profiles.

## Domain model and ownership

The capability extends the existing `Identity & Workspace` bounded context,
renamed conceptually to `Identity, Organization & Access`; it does not require a
new deployable service in the modular monolith. That context owns:

- `OrgUnit` stable identity and immutable/effective-dated versions;
- `OrgMembershipAssignment` with exactly one effective primary unit per active
  workspace member in v1;
- `OrgLeadershipAssignment` with `unit`, `subtree`, or `workspace` scope;
- department data/access policy versions and cross-department grants;
- resource ownership bindings and transfer/departure decisions;
- effective-access decisions and explainable policy traces.

Presentation & Reports owns Department Hub and People & Creators composition,
but reads only public projections from Identity, Semantic Model, Methodology &
Research, Analytics, and Presentation resource catalogs. Audit remains an
append-only accountability context and is not queried directly as an employee
analytics database. A dedicated privacy-safe `ContributorActivityProjection`
is built from redacted domain events and governed by Identity & Access policy.

The minimum conceptual records are:

```yaml
org_unit_version:
  org_unit_id: uuid
  org_unit_key: opaque_immutable_string
  workspace_id: uuid
  version: integer
  unit_type: company|division|department|team
  parent_org_unit_id: uuid|null
  display_name: string
  status: active|inactive|merged
  effective_from: timestamp_utc
  effective_to: timestamp_utc|null
  successor_org_unit_id: uuid|null

org_membership_assignment:
  assignment_id: uuid
  workspace_membership_id: uuid
  org_unit_id: uuid
  assignment_kind: primary
  effective_from: timestamp_utc
  effective_to: timestamp_utc|null

org_leadership_assignment:
  leadership_assignment_id: uuid
  workspace_membership_id: uuid
  org_unit_id: uuid
  scope_mode: unit|subtree|workspace
  permission_bundle_key: string
  effective_from: timestamp_utc
  effective_to: timestamp_utc|null

department_data_policy_version:
  policy_version_id: uuid
  org_unit_id: uuid
  grants: []
  row_column_ceiling_refs: []
  pii_ceiling: none|explicit_separate_grant
  descendant_inheritance: none|include_descendants
  status: draft|published|deprecated

resource_ownership_binding:
  resource_type: report|dashboard|research|analysis|segment|forecast
  resource_id: uuid
  creator_principal_id: uuid
  owner_type: principal|org_unit|workspace_legacy
  owner_id: uuid
  effective_from: timestamp_utc

cross_department_grant:
  subject_type: principal|org_unit
  subject_id: uuid
  resource_scope: object|collection|data_product
  resource_ref: object
  actions: [view_snapshot, comment, export, fork, edit, run, manage_access]
  reason: string
  approved_by: uuid
  expires_at: timestamp_utc|null
```

`OrgUnit` hierarchy is an organizational model, not authorization by itself.
Leadership and inheritance are explicit assignments. A parent position grants
subtree visibility only when its leadership assignment uses `subtree` or
`workspace` scope.

## Authorization and data semantics

Effective access is the intersection of:

1. functional permission bundles;
2. active workspace and primary organizational membership;
3. explicit leadership or delegated organizational scope;
4. department data policy and explicit cross-department grants;
5. object/version access policy;
6. row, column, export, and PII ceilings.

No single input may bypass the others. In particular:

- a department leader is not a global platform role;
- a Workspace Administrator can manage organization configuration but receives
  no employee-activity or business-content access unless separately assigned;
- report snapshot access does not grant access to the underlying dataset,
  analysis editor, drill-down rows, or PII;
- cross-department grants are allow-only, bounded, reasoned, expiring where
  appropriate, and never raise a subject above their functional/PII ceiling;
- counts, search results, activity summaries, and creator cards are filtered
  before pagination and aggregation so hidden-object existence is not leaked;
- new active memberships require a primary department; migrated legacy members
  may temporarily use the root company unit with
  `needs_department_assignment=true` without any access expansion.

The access decision is conceptually:

```text
effective_access = functional_permissions
                 AND organization_scope
                 AND data_policy
                 AND object_policy
                 AND row_column_pii_ceiling
```

## Reporting ownership and lifecycle

Personal drafts remain principal-owned. By default, publication transfers the
new immutable report/dashboard/research version to the creator's effective
primary department while preserving `created_by` and all co-author/reviewer
bindings. A versioned presentation policy may explicitly choose a different
allowed owner.

Employee transfer, suspension, and departure must be effective-dated and
audited:

- old department-derived access ends at the effective boundary;
- explicit grants are re-evaluated rather than silently carried forward;
- historical artifacts retain the author's organizational snapshot at creation
  and publication time;
- department-owned published resources remain available to the department;
- principal-owned drafts are reassigned, archived, or retained under an
  explicit administrator decision;
- merge/closure never hard-deletes units, ownership, or historical attribution;
- a successor mapping is required before an active unit with members/resources
  can be closed or merged.

Existing published resources migrate as `workspace_legacy` ownership until an
administrator performs an auditable assignment. Migration must not silently
expose or revoke existing content.

## Contributor directory and activity privacy

The People & Creators directory is a governed discovery surface, not an
employee-performance leaderboard. The public authorized profile may show:

- avatar/initials, display name, title, primary department, and platform role
  labels safe for the viewer;
- visible published dashboards, reports, research, and expertise domains;
- contribution labels such as active creator, maintainer, or reviewer;
- access-filtered counts and recent visible publications.

The extended self/manager view may add bounded 30/90-day summaries for
published or materially updated resources, maintained active content,
co-authorship, review/approval, resolved collaboration, and governed usage.

The following are excluded from v1 and should not be represented as product
requirements: employee ranking, productivity score, working-hours inference,
exact login surveillance, raw search/query history, recipient email lists,
hidden draft titles, or automatic HR/performance decisions.

`ContributorActivityProjection` stores period aggregates and safe resource
references, not raw audit payloads. The employee may see their own extended
summary. A leader may see individual summaries only inside the explicit
leadership scope and with `organization.activity.read`. Higher-level access is
expressed through `subtree`/`workspace` assignments, not inferred from a title.

## UI and route outcome

This capability requires durable deep links and cannot be represented only as
tabs inside the current access page. The target UI adds six routes after the
W08 design baseline:

| Proposed ID | Canonical path | Purpose |
|---|---|---|
| `UI-ORG-001` | `/w/:workspaceKey/organization` | authorized organization tree and department discovery |
| `UI-ORG-002` | `/w/:workspaceKey/organization/:orgUnitKey` | Department Hub with reporting catalog, data products, creators, and activity |
| `UI-PEOPLE-001` | `/w/:workspaceKey/people` | searchable People & Creators directory |
| `UI-PEOPLE-002` | `/w/:workspaceKey/people/:principalId` | privacy-aware creator/employee profile |
| `UI-ADMIN-019` | `/w/:workspaceKey/settings/organization` | organization structure, assignment, lifecycle, and import-ready administration |
| `UI-ADMIN-020` | `/w/:workspaceKey/settings/organization/:orgUnitKey` | unit detail, leaders, members, data policy, delegation, transfer, and audit |

No new overlay is required in the first contract: object access reuses the
existing Resource Access Policy and permission explanation surfaces. Two
cross-surface capabilities are expected:

- organization-scoped access and department ownership;
- contributor directory, activity privacy, and manager scope.

The Penpot delta should add one component board after C24 and one prototype
flow after flow 09. The Department Hub should adapt the useful creator strip
and report-card discovery pattern from the approved reference to Frost tokens,
compact information density, access-filtered counts, keyboard operation, and
non-card table/list alternatives. Required states include empty organization,
unassigned legacy member, no visible resources, partial data access, expired
cross-department grant, transferred/departed employee, inactive/merged unit,
manager versus ordinary-viewer profile, and denied activity detail.

## Invariants, failure behavior, and non-goals

- An active member cannot have two overlapping primary department assignments
  in v1.
- An organization tree cannot contain a cycle or a parent from another
  workspace.
- Access resolution fails closed when hierarchy, policy, or projection state is
  missing/stale beyond its declared boundary.
- Department moves and policy publication use optimistic concurrency and
  versioned impact preview; partial multi-context mutation is reconciled.
- Creator counts and manager activity never reveal inaccessible resource
  identity, content, filters, recipients, PII, or raw audit data.
- Department ownership does not make a resource readable without an effective
  access policy.
- Viewing a safe snapshot does not grant edit, run, source-data, drill-down, or
  export rights.
- PII continues to require an explicit scoped expiring grant and is never
  inherited from department membership, leadership, or administrator status.
- Physical datasets and reports are not duplicated per department.
- HRIS, SCIM, OIDC-group synchronization, matrix/multiple-primary reporting,
  temporary project teams, employee scoring, automated recommendations, and
  HR performance decisions remain future extensions.

## Test and proof seam

The static contract ticket must prove machine/human requirement parity,
architecture ownership, six-route identity/execution/localization parity,
surface/use-case coverage, schemas, docs links/indexes, and the repository
local/CI gates. That proof does not establish UI or runtime behavior.

The Penpot ticket must start from W08's exact accepted terminal revision and
fingerprint the newly synchronized sources. It must visually review every new
route, modified access surface, the new component board, and the new prototype
flow; globally reconcile all stable IDs; and explicitly exclude browser/runtime
proof.

Later implementation must be split into at least two vertical proof seams:

1. organization/access core: persistence, policy resolver, transfer lifecycle,
   data/object/PII intersection, audit, migrations, negative cross-workspace
   tests, and administration browser flow;
2. Department Hub and contributor insights: safe activity projection,
   access-filtered counts/search, reporting ownership/discovery, manager/self
   privacy variants, and real browser/accessibility evidence.

## Decisions and delivery graph

Accepted product decisions:

- one primary department per active member in v1;
- leader scope is an explicit assignment, not a platform role;
- ordinary users see authorized public creator profiles and their own extended
  activity; leaders see extended activity only for their assigned scope;
- Workspace and Installation Administrator roles do not automatically receive
  employee activity or business-data access;
- publication defaults to department ownership while drafts remain personal;
- role, organization, data, object, row/column, and PII access stay independent;
- no leaderboard, employee score, surveillance, or physical data duplication.

Delivery uses a dependency graph rather than a standing plan:

1. W08 finishes the current `0.9.2/0.6.2` Penpot delta and records its terminal
   revision/evidence without context drift.
2. W09 synchronizes product `0.9.3-draft`, UI `0.6.3-draft`, architecture,
   executable route/surface contracts, localization, and acceptance invariants.
3. W10 implements the organization/people UI delta in canonical Penpot from
   the exact W08 terminal revision.
4. Runtime organization/access and contributor-insights vertical tickets are
   created only after W10 acceptance, with separate API/persistence/browser
   proof boundaries.
