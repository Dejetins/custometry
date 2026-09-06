# Template — milestone implementation plan

> Bounded plan under the [framework](README.md). This becomes `plan_doc` only after acceptance and authorized pack preparation.

## Identity

| Shared metadata | Value |
|---|---|
| `schema_version`, `framework_ref` | `custometry-planning/v1`; `<path + version>` |
| `artifact_kind`, `doc_id`, `title` | `milestone`; `<MS-id>`; `<result title>` |
| `version`, `planning_status` | `0.1.0`; `draft` |
| `parent_ref`, `direction_ref` | `<WS-id + path + version>`; `<DIR-id>` |
| `baseline_ref`, `requirement_refs` | `<revision and evidence>`; `<source revisions + IDs>` |
| `decision_refs`, `supersedes_ref` | `<references>`; null |
| `execution_ref` | null until authorized pack preparation; then exact journal reference |

## 1. Result and boundaries

| Item | Definition |
|---|---|
| Before / after | `<current limitation -> observable result>` |
| Included / excluded | `<bounded scope and explicit non-goals>` |
| Preserved implementation | `<existing components and evidence>` |
| Requirement clauses | `<exact IDs and selected clauses without weakening modality>` |
| Unproven or missing inputs | `<source / target / fixture / decision; blocks which action>` |
| Authority | `<planning, implementation and publication authority distinguished>` |

Insert current-state evidence and dependency tables from the framework.

## 2. Implementation decisions

| Decision / boundary | Current design | Proposed change and rationale | Owner / source | Compatibility | Migration / recovery | Required proof |
|---|---|---|---|---|---|---|
| `<ID>` | `<observed>` | `<planned>` | `<reference>` | `<classification>` | `<action or justified N/A>` | `<boundary>` |

Cover affected API/data/event contracts, persistence, identity/access, concurrency,
idempotency, failure behavior, resource limits and UI states. Unaffected areas use
one justified exclusion; do not add architecture ceremony merely to fill rows.
Material business rules and thresholds come from accepted sources or owner decisions.

## 3. Work breakdown and ownership

| Stage ID | Bounded result | Dependencies | Expected owned paths / zones | Shared writer constraint | Output consumed by later work |
|---|---|---|---|---|---|
| `<MS-id-S01>` | `<result>` | `<IDs>` | `<verified paths or explicit zones>` | `<constraint>` | `<output>` |

Include integration and final acceptance work. Mark conditional investigations
before dependent implementation. Potential parallel tasks may be identified inside
an authorized stage; stage advancement itself follows the selected ledger lifecycle.
The owner determines agent assignments and whether parallelism is used.

## 4. Acceptance and proof allocation

| Criterion ID | Requirement / owner intent | Observable criterion | Proving stage | Exact check / real environment | Required evidence | Acceptance authority |
|---|---|---|---|---|---|---|
| `<MS-id/AC-01>` | `<reference>` | `<testable statement>` | `<ID>` | `<known command or input gap>` | `<expected report/receipt>` | `<technical / owner>` |

Include negative/failure cases and cross-component integration where relevant.
Specify what successful checks cannot prove. Do not claim production readiness
from local proof or UI behavior from mocks. Final closure includes owner acceptance;
name any earlier owner checkpoint explicitly.

## 5. Execution and repair envelope

| Field | Value |
|---|---|
| Allowed / forbidden changes | `<paths, behavior and effects>` |
| Delegated technical decisions | `<reversible choices agent may settle>` |
| Decisions reserved to owner | `<scope, product choices, material tradeoffs>` |
| In-scope repair | `<permitted repair and invalidated checks to rerun>` |
| Rollout / rollback constraints | `<when relevant; exact source>` |
| Publication / deployment | `<separate authority and target, or outside scope>` |
| Documentation effects | `<canonical docs changed by delivered behavior>` |
| Sensitive-data handling | `<redaction and allowed evidence>` |

## 6. Execution artifact binding

| Field | Planned path / binding |
|---|---|
| `plan_doc` | `<this accepted plan; immutable version and commit/digest>` |
| `prompt_pack_dir` | `<authorized directory>` |
| `stage_ledger` | `<canonical journal>` |
| Validation profile | `<schema, existing validator, commands, result and receipt contract>` |
| Claim/update mechanism | `<verified existing implementation and evidence, or unresolved>` |
| Execution mode | `manual_sequential` unless explicitly authorized otherwise |

These fields may be proposed while planning. Do not claim `draft_valid` until actual
triad files validate; do not claim entry readiness without real updater evidence.

## 7. Owner decision packet and history

Insert the decision and change-history tables. Record acceptance of the exact
milestone plan version. Link subsequent execution and closure evidence to the journal
without maintaining a second milestone implementation status here.

## Mandatory documentation handoff

Apply the framework's [document synchronization rules](README.md#mandatory-document-synchronization)
in this same unit: update parent/child and dependency links, affected source references,
versions, decisions, indexes and execution evidence as applicable. Do not wait for
an owner reminder. Identify any authority or unresolved-decision blocker explicitly;
do not claim completion while a required documentation update remains outstanding.
