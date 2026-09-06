---
doc_id: ARCH-PLANNING-FRAMEWORK-001
doc_version: 2
status: accepted
visibility: internal
ship: false
owner: architecture
requirement_ids: []
proof_boundary:
  label: accepted-planning-and-documentation-process
  exclusions: [execution-readiness, implementation, release]
---

# Hierarchical planning framework — 1.0.0

The owner accepted the concept, structural templates and planning workflow on
2026-09-06, then explicitly requested documentation adoption, removal of the
fictional example, mandatory document links/maintenance, project AGENTS routing,
and a local main-branch commit. This is the accepted 1.0.0 process across development
directions. It does not select product work, initialize a milestone, authorize
implementation, or certify an executable pack.

## Templates and owner checkpoints

| Document | Purpose | Main owner decision |
|---|---|---|
| [Project map](01-project-map-template.md) | Navigation across development directions | Are the directions and boundaries useful? |
| [Direction](02-direction-template.md) | Level 1 scope and decomposition | Is the intended capability complete and correctly bounded? |
| [Workstream](03-workstream-template.md) | Level 2 large task and milestone sequence | Are the proposed outcomes and dependencies appropriate? |
| [Milestone](04-milestone-template.md) | Bounded implementation plan | Is the result, tradeoff and acceptance boundary agreed? |
| [Stage prompt](05-stage-prompt-template.md) | One executable part of a milestone | Is delegated freedom and any reserved checkpoint clear? |
| [Iteration journal](06-iteration-journal-template.md) | Canonical execution state plus iteration evidence | Is progress and unfinished work understandable? |

Templates are copy-and-fill outlines. Angle-bracket values are placeholders,
not assertions, working links, valid IDs or default decisions. All required
sections must be completed; use `not_applicable` with a reason where conditional.
An unresolved value is allowed in a draft only with a question, resolution path
and the specific action it blocks. Implementation documents remain English under
repository policy; discussion and owner-facing summaries remain Russian.

## 1. Hierarchy and responsibility

`project map -> direction -> workstream -> milestone -> stage prompt`

The journal belongs to the milestone alongside its prompt pack. It is not another
planning level. Extra workstream depth is permitted only when a distinct scope
needs decomposition; record the reason. A milestone always ends in demonstrable
behavior or a verifiable engineering result. Stage prompts describe execution.
Existing bounded contexts and accepted requirements constrain this hierarchy;
organizational directions do not create new software service boundaries.

The owner participates before each selected branch is decomposed further and
controls agent organization and execution delegation. Agents prepare options,
explain consequences, maintain links and carry out agreed technical bookkeeping.
Approval of one level does not imply approval of unwritten child plans or permission
to execute them. Clear natural-language decisions suffice; no magic approval text.

## 2. Shared metadata for instantiated planning documents

Use this metadata in project maps, directions, workstreams and milestone plans.
Stage prompts and journals use the existing pack profile, described below.

| Field | Type / allowed value | Rule |
|---|---|---|
| `schema_version` | `custometry-planning/v1` | Documented structural schema; semantic fields are checked at handoff; no dedicated machine validator is claimed |
| `framework_ref` | `{path, version}` | Exact adopted framework version; draft references remain proposals |
| `artifact_kind` | `project_map`, `direction`, `workstream`, `milestone` | Meaning is independent of nesting depth |
| `doc_id` | Stable unique string | Prefixes: `MAP`, `DIR`, `WS`, `MS`; never reuse retired IDs |
| `title` | Human-readable string | Describe the intended outcome or area |
| `version` | `major.minor.patch` | Content version; separate from schema version and Git revision |
| `planning_status` | `draft`, `in_review`, `accepted`, `superseded`, `archived` | Acceptance applies to this exact content version |
| `parent_ref` | `{id, path, version}` or null | Null only for project map; one decomposition parent |
| `direction_ref` | Stable direction ID or null | Required below direction; root map uses null |
| `baseline_ref` | `{commit, evidence_refs}` | Full inspected commit; record relevant uncommitted deltas separately |
| `requirement_refs` | List of `{source, revision, ids}` | Selected normative clauses; empty only with an explanation |
| `decision_refs` | List of stable decision references | Include owner acceptance and applicable architecture decisions |
| `supersedes_ref` | Reference or null | Replacement identity, exact version and migration reason |
| `execution_ref` | Ledger reference or null | Milestones only; authoring links may remain explicitly proposed |

Each template inherits this table. Its metadata panel records values; the table
is the field definition source. Do not copy execution state into planning metadata.

## 3. Tables shared across levels

Each document uses the following compact tables where its template calls for them.
Use stable row IDs scoped by document, e.g. `MS-010/AC-01` or `DIR-001/DEC-02`.

**Current-state evidence**

| Claim ID | Capability / requirement | Observation | Evidence + revision | Gap / uncertainty | Next resolution |
|---|---|---|---|---|---|
| `<id>` | `<scope>` | `documented_only / code_observed / boundary_verified / unknown` | `<source or observed check>` | `<remaining gap>` | `<bounded investigation>` |

These labels describe evidence strength, not completion percentages. Every runtime
claim names its tested boundary. A failed read is `unknown`, never proof of absence.

**Dependencies and shared boundaries**

| Dependency ID | Provider ID + path + required version | Required output / contract | Consumer | Needed before | Proof of satisfaction | Shared write / integration owner |
|---|---|---|---|---|---|---|
| `<id>` | `<reference>` | `<specific capability>` | `<reference>` | `decomposition / execution / acceptance` | `<check or evidence>` | `<role or unresolved>` |

Distinguish informational references from blocking dependencies. Hard dependency
graphs must be acyclic. Cross-direction work has one primary parent; other
directions reference it. Never duplicate the same implementation obligation.
Potential parallelism is a planning observation, not a dispatch instruction.

**Decisions and owner review**

| Decision ID | Question | Options and consequences | Agent recommendation + basis | Decider | Blocks | Decision + source + date + covered version |
|---|---|---|---|---|---|---|
| `<id>` | `<material question>` | `<real alternatives>` | `<proposal>` | `owner / delegated role` | `<specific action>` | `<unresolved or actual decision>` |

**Change history**

| Version | Date | Change and reason | Affected references / evidence | Approval or delegated basis |
|---|---|---|---|---|
| `0.1.0` | `<date>` | Initial draft | `<references>` | Draft requested; content not accepted |

## 4. Progressive agreement and mandatory decisions

| Gate | Decisions and evidence required | Permitted next action |
|---|---|---|
| Project map agreed | Direction coverage/boundaries, preserved priorities/holds, selected direction, owner decision | Detail the selected direction |
| Direction structure agreed | Scope/exclusions, relation to other directions, current-state gaps, selected branch, owner decision | Decompose the selected workstream |
| Workstream structure agreed | Immediate-child outcomes/order, hard dependencies, shared contracts, investigation needs, owner decision | Detail the selected child workstream or milestone |
| Milestone plan agreed | Bounded result, acceptance, compatibility/migration/rollback where affected, proof inputs, delegated freedom, owner checkpoints | Prepare its pack and draft journal when authorized |
| Pack structurally valid | Real triad, profile validation, independent review, source mapping; unresolved inputs explicitly disallow execution | Review or finish entry preparation; structural pass is not execution permission |
| Stage entry ready | Current sources, satisfied dependencies, resolved decisions, actual exclusive updater, owner execution authority | Claim and run the one allowed stage using the runner |
| Milestone closed | All required stage outcomes, integration proof, exact criterion-to-evidence coverage, owner result acceptance | Record the closure in the journal; select the next work with the owner |

The closure checkpoint is part of this accepted owner-involved workflow.
Intermediate owner checkpoints are set explicitly in each milestone; the template
does not require approval for every reversible technical step. Missing downstream
outputs assigned to earlier stages are deferred dependencies, not owner questions.
Independent, already-authorized work may continue while a decision is pending.

## 5. Versions, changes and links

- `major`: changes agreed outcome, scope, acceptance, authority or relied-upon
  external/persisted contract. `minor`: adds compatible detail or optional work
  within the accepted boundary. `patch`: editorial correction with no meaning change.
- Before first acceptance, versions may remain `0.x.y`; approval still binds an
  exact version. A substantive amendment is `draft` or `in_review` until accepted.
  Prior acceptance survives only for its previous content, not the candidate.
- Preserve accepted bytes in Git or an immutable snapshot before replacement.
  Draft-only working copies must not become the source of an executing pack.
- A patch may inherit acceptance only under explicit delegated editorial authority;
  record that basis. Scope, requirement, criterion or checkpoint changes return to
  owner review regardless of the editor's chosen version number.
- Use repository-relative paths for the planning layout and pair every
  authoritative reference with stable ID and exact content version. Record an
  immutable commit or content digest for pack inputs. Do not use `latest` for execution.
- Parent changes trigger an impact check on linked children; unaffected children
  stay accepted at their recorded basis. Record compatibility/revalidation decisions
  for affected links before dependent execution. Reparenting preserves the child ID
  and records the old/new parents and ownership changes.
- A child registry contains links and intended outcomes, never manually maintained
  child statuses. Any summary of progress is derived, dated and points to its source.
- A completed implementation is historical evidence for a specified scope/revision.
  New requirements create a new amendment or milestone; they do not erase old evidence
  or silently transfer old proof to new behavior.

## 6. Execution integration and single sources of truth

The milestone plan is `plan_doc`; its prompts occupy `prompt_pack_dir`; its
iteration journal is `stage_ledger`. These are exactly the three execution
artifacts defined by the installed Prompt Pack Artifacts v1 contract. Reports and
immutable receipts are evidence linked from the journal, not extra control registers.

| Information | Canonical source |
|---|---|
| Product obligations | Machine blueprint and accepted source contracts |
| Planned scope and owner decisions | Exact accepted planning document version |
| Stage status, claims, blockers, next-stage permission | Milestone journal's canonical ledger record |
| Executed commands and observations | Referenced immutable iteration/stage evidence |
| Milestone closure | Final acceptance stage and its receipt in the same journal |
| Direction / workstream progress | Derived from child evidence; no parallel mutable status table |
| Existing independent ticket execution | Existing ticket and its evidence under the current adapter |

Milestone packs are the execution route for this hierarchical workflow. This does
not convert old tickets to stages or reactivate retired UI packs. Any authorized migration
must choose a single execution authority for each unit; a ticket and ledger must
not both maintain that unit's current status. Direct tiny repairs can retain the
current ticket route outside a milestone pack. The owner decides that boundary.

Default execution mode remains `manual_sequential`; Goal mode needs explicit
authority. Agent assignment and concurrency remain owner-controlled. No schedule,
resource capacity, model choice or automatic cross-milestone continuation is implied.

## 7. Storage and validation

Required instance layout (create actual instances only within authorized planning or execution):

```text
docs/architecture/planning/project-map.md
docs/architecture/planning/directions/<direction-id>/direction.md
docs/architecture/planning/directions/<direction-id>/workstreams/<workstream-id>.md
docs/architecture/planning/milestones/<milestone-id>/plan.md
.codex/agents/generated/<milestone-id>/<stage-id>.md
.codex/delivery/ledgers/<milestone-id>.md
.codex/delivery/evidence/<milestone-id>/<stage-id>/<iteration-id>.md
```

Flat stable milestone IDs keep links stable when grouping changes. Nested workstream
documents can use the same directory and explicit parent links without deep paths.
The ledger/profile owns execution path resolution; bundled-profile paths are relative
to the ledger except the prompt's ledger locator, which is prompt-relative.

The owner adopted the following choices on 2026-09-06. Their acceptance does not
waive real inputs, current-source checks or exclusive update requirements.

| ID | Accepted decision | Consequence |
|---|---|---|
| FRAME/DEC-01 | Four planning kinds plus stage execution; optional repeated workstream depth | Each immediate-child registry records its actual kind and one parent |
| FRAME/DEC-02 | Semantic versions with exact-version acceptance | Material amendments return to owner review; editorial freedom must be delegated |
| FRAME/DEC-03 | Owner review at each selected decomposition and milestone closure | Intermediate stage checkpoints remain selectable |
| FRAME/DEC-04 | One journal/pack per milestone; ticket route retained for separate bounded work | No unit has duplicate mutable ticket and ledger status |
| FRAME/DEC-05 | Required paths and current bundled pack profile | Resolve an actual exclusive updater before any entry-ready handoff |
| FRAME/DEC-06 | Document links and synchronized maintenance are mandatory | Agents update affected documentation without owner reminders |

The [repository adapter](../../../../.codex/AGENTS.md),
[delivery ADR](../../../adr/0003-agent-delivery-model.md) and
[operating model](../../development-operating-model.md) adopt this workflow.
Older retired packs and their state remain historical. Existing independent tickets
retain their own evidence and are not converted implicitly. Existing broad roadmaps
are supporting sequence proposals until a selected branch is reconciled into this
hierarchy with the owner.

### Mandatory document synchronization

Document relationships are required deliverables, not optional editorial cleanup.
Every agent creating, changing, executing or closing a planning unit must perform
this synchronization within the same authorized unit, without an owner reminder:

1. Read the selected document, its recorded parent, immediate-child registry and
   affected provider/consumer contracts. Bound further reading by actual impact.
2. Maintain both parent-to-child registry links and the child's exact `parent_ref`.
   Register a new document in its parent and relevant navigation index. A root map
   is registered in the architecture index. No orphaned planning documents.
3. Record blocking dependencies with provider ID, path/version, required output and
   satisfaction evidence. Update affected consumer references when a provider changes;
   preserve prior version bindings unless compatibility or revalidation is recorded.
4. Keep requirement/decision references, content versions, approval basis and change
   history aligned with the actual change. Record semantic differences; never silently
   broaden accepted scope, weaken criteria or reuse stale approval/evidence.
5. Synchronize the milestone plan, prompt contracts and canonical journal according
   to the pack lifecycle. Preserve active claims, terminal history and immutable
   receipts. The runner alone mutates activated execution state under exclusivity.
6. Update affected canonical requirements/mirrors, architecture/contracts, runbooks,
   user documentation and generated indexes when the authorized work changes their
   meaning. A no-impact finding is recorded briefly; unrelated documents need no edit.
7. Check real links, exact version/ID bindings, reciprocal parent/child membership,
   hard-dependency cycles, criterion coverage and the chosen source of execution state.
   Unresolved target paths are permitted only as explicit draft outputs with producer
   dependencies; they are never presented as current working links.
8. Include changed documentation and checks in the handoff. Required synchronization
   is part of completion. If a material owner decision, write boundary, unavailable
   source or execution claim prevents an update, record the exact gap and keep the
   dependent completion/readiness claim open; continue independent authorized work.

Owner review still controls substantive plan decisions. Agents settle mechanical
link, index and authorized version bookkeeping themselves. Do not request repeated
permission to perform documentation maintenance already covered by the task.

### Required verification

The author checks the eight synchronization obligations above and records evidence
in the unit's journal/report, or an adoption report for framework changes. Current
repository commands are defined in [tooling gates](../../tooling-gates.md): use the
Markdown/governance checks as applicable, including `generate_docs_index --check`,
`check_docs_links`, and affected delivery/profile checks. Those tools check only
their implemented boundaries; manually verify the planning fields and reciprocal
version bindings they do not yet parse. Do not describe this schema as automatically
enforced. A future dedicated validator is a separately scoped tooling change.

For actual packs, resolve and run the selected Prompt Pack Artifacts v1 validator,
perform its required independent review, and verify actual exclusive-update evidence.
A source-check pass or acceptance of this framework does not provide a runtime
executor or make an incomplete pack runnable.

## 8. Adoption and provenance

| Version | Date | Decision / change | Evidence |
|---|---|---|---|
| 0.1.0 | 2026-09-06 | Structural draft reviewed; nested-child representation and first-level checkpoint corrected | Historical authoring review; no execution was created |
| 1.0.0 | 2026-09-06 | Owner accepted the structure and requested adoption, mandatory links/maintenance and example removal | [Adoption evidence](adoption-evidence.md) |

The draft directory and fictional example are removed. New template instances
start as drafts; their content and later implementation need their own authority.
