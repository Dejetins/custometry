# Template — large task or workstream

> Level 2 outline under the [framework](README.md). Repeat this kind only with a stated decomposition reason.

## Identity

| Shared metadata | Value |
|---|---|
| `schema_version`, `framework_ref` | `custometry-planning/v1`; `<path + version>` |
| `artifact_kind`, `doc_id`, `title` | `workstream`; `<WS-id>`; `<title>` |
| `version`, `planning_status` | `0.1.0`; `draft` |
| `parent_ref`, `direction_ref` | `<DIR-or-WS-id + path + version>`; `<DIR-id>` |
| `baseline_ref`, `requirement_refs` | `<revision and evidence>`; `<source revisions + IDs>` |
| `decision_refs`, `supersedes_ref` | `<references>`; null |

## Outcome and implementation overview

- User or engineering outcome: `<demonstrable capability>`.
- Scope and exclusions: `<boundaries within parent>`.
- Current behavior and reusable components: `<plain explanation with evidence>`.
- Required change and architecture constraints: `<current versus proposed>`.
- Additional decomposition depth, if used: `<reason or not_applicable>`.

Insert the framework's current-state evidence table.

## Immediate-child sequence

| Child kind | Child ID + path + version | Result at closure | Entry dependencies | Main unknown to resolve | Required proof boundary | Contribution to workstream completion |
|---|---|---|---|---|---|---|
| `workstream / milestone` | `<reference>` | `<observable result>` | `<specific provider>` | `<uncertainty>` | `<API / data / browser / other>` | `<coverage>` |

List immediate children only. A nested workstream owns its own child registry;
link descendants for traceability without presenting them as direct children.

Each milestone must be small enough to review its result coherently. Split it when
independent outcomes, unresolved contracts or proof environments need different
acceptance decisions; stage count alone is not a sizing rule.

## Contract and sequencing decisions

| Boundary | Existing owner / source | Required decision or change | Compatibility impact | Needed before child outcome |
|---|---|---|---|---|
| `<boundary>` | `<reference>` | `<proposal or preserved decision>` | `none / compatible-change / breaking-change / unknown` | `<reference>` |

Insert the dependency table. Name shared migrations, clients, shell or configuration
that prevent independent edits. Identify who will integrate cross-child outcomes
as a responsibility; the owner chooses agents later.

## Workstream acceptance allocation

| Requirement / parent obligation | Immediate-child coverage | Cross-child integration proof | Uncovered remainder / explicit deferral |
|---|---|---|---|
| `<reference>` | `<references>` | `<criterion and owner>` | `<remaining work or none>` |

## Owner review and next child

Insert the decision table. Discuss child boundaries, order, contract choices,
explicit deferrals and the next workstream or milestone to detail. Owner acceptance here approves
this structure; it does not accept a child's unwritten implementation plan.

## Revision history

Insert the change-history table.

## Mandatory documentation handoff

Apply the framework's [document synchronization rules](README.md#mandatory-document-synchronization)
in this same unit: update parent/child and dependency links, affected source references,
versions, decisions, indexes and execution evidence as applicable. Do not wait for
an owner reminder. Identify any authority or unresolved-decision blocker explicitly;
do not claim completion while a required documentation update remains outstanding.
