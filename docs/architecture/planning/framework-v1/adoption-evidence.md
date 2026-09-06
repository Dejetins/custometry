---
doc_id: ARCH-PLANNING-FRAMEWORK-ADOPTION-001
doc_version: 1
status: accepted
visibility: internal
ship: false
owner: engineering
requirement_ids: []
proof_boundary:
  label: planning-governance-source-validation
  exclusions: [product-implementation, pack-entry-readiness, runtime, release, remote-publication]
---

# Hierarchical planning framework adoption evidence

## Authority and scope

On 2026-09-06 the owner explicitly accepted the structural framework and requested
its adoption in documentation and project AGENTS instructions, mandatory document
relationships and proactive maintenance, removal of the fictional example and a
local commit on main. This report records that decision; it does not add authority
for product implementation, agent dispatch in future work or remote publication.

The [framework](README.md) is accepted at version 1.0.0. Its six templates remain
blank authoring inputs. No real direction, milestone, prompt pack or journal is
created. Product requirements, pilot authority and application code are preserved.
Requirement IDs are empty because this is an owner-selected engineering process
change, not a new product obligation.

## Compatibility and preservation

Process impact: breaking-change for the superseded ticket-only planning restriction;
existing independent tickets and historical execution evidence are preserved.
API, persistence, runtime and product contract impact: none.

The commit is prepared from verified main `f242d27c6509154d3f9e5c7b5bfed11d21166487`
in an isolated checkout. The shared checkout's prior head was
`80cd0976c434b6db62d3e415bc638cbe4a9468c2`; unrelated modifications are preserved.
Only framework files and necessary routing, architecture, layout, roadmap, Web
execution-source and index changes belong to this adoption. Reversing the process
requires an explicit documentation amendment; no data migration is introduced.

## Validation

| Check | Observed outcome | Boundary |
|---|---|---|
| `source scripts/activate-toolchain.sh` | pass; repository-pinned toolchain active | Local command prerequisites |
| `uv run --locked --offline python -m tools.custometry_quality.generate_docs_index` | pass; 54 contributor documents | Index generation |
| `uv run --locked --offline python -m tools.check --scope local` | pass after source changes and review fixes | Grouped local source/static profile |
| `git diff --check` | pass | Patch whitespace |
| Hierarchy/triad/source review | pass with two corrected Medium findings | Semantic document and routing consistency |
| Shared checkout preservation comparison | 4,058 unrelated changed/deleted/untracked paths preserved | Bytes or continued absence; owned paths excluded |

The first local-profile attempt rejected an environment symlink escaping the
isolated root. Replacing that task-created link with a physical environment copy
resolved the precondition; subsequent full local-profile runs passed. No source
check or runtime failure is suppressed by the successful result.

Cold-head review: completed. Mode: independent subagent. Scope: all new framework
files and the adoption diff against the named main baseline, accepted owner intent,
and installed pack/lifecycle contracts. Verdict: Release after fixes for this
source/governance boundary. Two Medium findings (remaining ticket-only Web planning
route and browser-proof wording limited to tickets) were corrected; no Blocker/High
or unresolved finding remains. Local follow-up checks passed.

The role-routing canary was semantic inspection of the changed architect and
prompt_manager instructions: accepted milestone authoring routes to prompt-manager;
unresolved decomposition retains owner participation; execution remains runner-owned;
required documentation synchronization is included. No live role invocation or
product execution is claimed by that canary.

The framework now defines mandatory reciprocal parent/child links, dependency and
source-version bindings, owner decisions and triad synchronization. Current automated
checks do not parse every proposed planning field: the framework requires explicit
semantic handoff checks and makes no dedicated-validator or exclusive-updater claim.
No milestone is entry-ready solely because these documentation checks passed.

## Handoff

The adopted process and six blank templates are ready for future owner-led planning.
No fictional worked example or task inventory is delivered. Product work, actual
packs/journals, broader agent delegation, remote push and deployment are outside
this adoption. The local commit includes only this change and its necessary source
links; unrelated shared-checkout edits are excluded.
