# Template — project planning map

> Adopted template. Fill using the [framework](README.md); no project directions are selected by this template.

## Identity

| Shared metadata | Value |
|---|---|
| `schema_version`, `framework_ref` | `custometry-planning/v1`; `<path + version>` |
| `artifact_kind`, `doc_id`, `title` | `project_map`; `<MAP-id>`; `<title>` |
| `version`, `planning_status` | `0.1.0`; `draft` |
| `parent_ref`, `direction_ref` | null; null |
| `baseline_ref`, `requirement_refs` | `<inspected revision and evidence>`; `<sources or reason>` |
| `decision_refs`, `supersedes_ref` | `<actual references>`; null |

## Purpose and boundaries

<Explain the product horizon this map covers, preserved priorities, explicit holds,
and what is outside it. Keep product requirements in their normative sources.>

## Direction registry

| Direction ID + path + version | Purpose | Included capabilities | Boundary with other directions | Requirement source | Selected for next discussion? |
|---|---|---|---|---|---|
| `<reference>` | `<why>` | `<scope>` | `<interfaces / exclusions>` | `<source + IDs>` | `<owner decision reference or proposed>` |

## Coverage and shared outcomes

| Requirement family / user outcome | Primary direction | Contributing directions | Integration acceptance owner | Unallocated scope / reason |
|---|---|---|---|---|
| `<source>` | `<reference>` | `<references>` | `<responsibility>` | `<gap or none>` |

## State, dependencies and decisions

Insert the framework's current-state, dependency and decision tables. Keep evidence
at direction-summary depth; link detailed investigations. Explain which technical
and product unknowns block selecting or decomposing a direction.

## Owner review packet

- Proposed direction structure and why: `<summary>`.
- Alternatives with materially different boundaries: `<comparison or none>`.
- Decisions needed now: `<decision IDs>`.
- Recommended next branch to detail: `<proposal and basis>`.
- Accepted changes and exact-version decision: `<unresolved until reviewed>`.

## Revision history

Insert the framework's change-history table. This registry is navigation and
coverage; obtain implementation progress from each linked milestone journal.

## Mandatory documentation handoff

Apply the framework's [document synchronization rules](README.md#mandatory-document-synchronization)
in this same unit: update parent/child and dependency links, affected source references,
versions, decisions, indexes and execution evidence as applicable. Do not wait for
an owner reminder. Identify any authority or unresolved-decision blocker explicitly;
do not claim completion while a required documentation update remains outstanding.
