# Template — development direction

> Level 1 outline under the [framework](README.md). Describe the whole area before selecting detail.

## Identity

| Shared metadata | Value |
|---|---|
| `schema_version`, `framework_ref` | `custometry-planning/v1`; `<path + version>` |
| `artifact_kind`, `doc_id`, `title` | `direction`; `<DIR-id>`; `<title>` |
| `version`, `planning_status` | `0.1.0`; `draft` |
| `parent_ref`, `direction_ref` | `<MAP-id + path + version>`; `<own DIR-id>` |
| `baseline_ref`, `requirement_refs` | `<revision and evidence>`; `<source revisions + IDs>` |
| `decision_refs`, `supersedes_ref` | `<references>`; null |

## Intent and scope

| Item | Description |
|---|---|
| Purpose and beneficiaries | `<what this area enables>` |
| Required final capabilities | `<link obligations rather than redefining them>` |
| Included / excluded | `<explicit boundary>` |
| Existing context ownership | `<accepted architecture sources>` |
| Preserved decisions / holds | `<source and effect>` |
| Observable direction completion | `<coverage and cross-direction acceptance conditions>` |

## Current state in plain language

<Explain how the existing parts work together and what the owner can actually do.
Separate observed code from verified behavior. State baseline limitations.>

Insert the framework's current-state evidence table.

## Large-task decomposition

| Workstream ID + path + version | Intended result | Included capabilities | Existing parts to reuse | Gap to close | Ordering rationale |
|---|---|---|---|---|---|
| `<reference>` | `<outcome>` | `<scope>` | `<evidence>` | `<remaining work>` | `<dependency / priority>` |

## Interfaces and integration

Insert the dependency table. Identify other directions that provide or consume
results. Identify integration outcomes that cannot be proven inside this direction.
Record potential parallel work with prerequisites; leave agent dispatch to the owner.

## Decisions and next decomposition

Insert the decision table. Owner review must resolve the direction boundary,
large-task completeness, priorities and the selected next workstream. Remaining
unknowns name a resolution action and what they block. No dates or capacities are
invented to populate the plan.

## Revision history

Insert the change-history table; link exact accepted decision evidence.

## Mandatory documentation handoff

Apply the framework's [document synchronization rules](README.md#mandatory-document-synchronization)
in this same unit: update parent/child and dependency links, affected source references,
versions, decisions, indexes and execution evidence as applicable. Do not wait for
an owner reminder. Identify any authority or unresolved-decision blocker explicitly;
do not claim completion while a required documentation update remains outstanding.
