# Template — milestone stage prompt

> Non-executable authoring outline under the [framework](README.md).
> An instantiated prompt uses the current Prompt Pack Artifacts v1 profile. This
> template does not create a stage or give permission to run commands.

## Machine header to materialize

The bundled profile uses JSON between frontmatter delimiters. Populate the header
from the same stage contract stored in the journal; exact values must match.
Do not put mutable stage status, claims or current decision answers in the prompt.

```json
{
  "schema_version": "stage-prompt/v1",
  "prompt_pack_execution": {
    "plan_doc": "<accepted plan path, relative to ledger>",
    "prompt_pack_dir": "<prompt directory, relative to ledger>",
    "stage_ledger": "<journal locator, relative to this prompt>"
  },
  "stage_contract": {
    "id": "<MS-id-S01>",
    "title": "<one bounded result>",
    "prompt_path": "<path relative to ledger>",
    "report_path": "<path relative to ledger>",
    "receipt_dir": "<unique immutable receipt directory relative to ledger>",
    "depends_on": [],
    "expected_touches": ["zone: named bounded responsibility"],
    "acceptance_criteria": ["<observable criterion with milestone criterion ID>"],
    "proof_boundary": "<exact boundary and exclusions>",
    "validation": {
      "profile": "<resolved current profile>",
      "checks": ["<actual command or observation required>"],
      "requires_user_acceptance": false
    },
    "entry_inputs": []
  }
}
```

The boolean is populated from the milestone's actual checkpoints, not copied as
a policy default; it must be true for the final owner-acceptance stage. Entry inputs
use `{path, producer_stage}`: null producer for existing inputs, a dependency ID for
future outputs. A draft may declare future inputs; entry requires them to exist.

## Task and current state

<Name the exact milestone version, stage result, preserved behavior, relevant
requirements and why this stage is needed. Explain observed versus proposed state.>

Read applicable AGENTS instructions and the current journal before acting. Follow
the canonical runner lifecycle. Do not claim or execute until current authority,
entry inputs, dependencies and exclusive update capability pass preflight.

## Context acquisition

| Group | Sources | Purpose / condition |
|---|---|---|
| Always read | `<minimal authoritative sources>` | `<what they establish>` |
| Task entrypoints | `<verified paths>` | `<where relevant implementation starts>` |
| Conditional | `<bounded source bundle>` | `<specific uncertainty triggering it>` |

Stop discovery when scope, contracts, proof and blockers are understood. Expand
only for a named uncertainty. No whole-repository audit is implied by this stage.

## Scope and delegated freedom

- Implement: `<specific included behavior>`.
- Preserve / exclude: `<existing invariants and non-goals>`.
- Allowed paths and shared ownership: `<verified paths, inseparable-change handling>`.
- Technical decisions delegated: `<bounded reversible choices>`.
- Owner decisions and checkpoints: `<IDs; read actual answers from journal>`.
- Publication or external effects: `<exact existing authority or outside scope>`.

## Work and verification

<Describe the bounded implementation sequence, contract consumers, documentation
effects, meaningful checks, migration/recovery proof where relevant and redaction.>

Use only relevant installed skills at the point their boundary is crossed; name
them and their purpose in the instantiated prompt. Preserve foreign changes.
Repair in-scope defects and rerun invalidated checks. Record scope changes and
unresolved decisions before crossing the affected boundary.

## Handoff

Write redacted iteration evidence and the profile's immutable transition receipt.
The runner updates the journal under its verified exclusive mechanism. Report
actual paths, checks/results, proof limits and next-stage input readiness. Permission
to start the next stage is separate from this stage's success. Never auto-continue
across milestones or activate Goal mode from this template.

## Mandatory documentation handoff

Apply the framework's [document synchronization rules](README.md#mandatory-document-synchronization)
in this same unit: update parent/child and dependency links, affected source references,
versions, decisions, indexes and execution evidence as applicable. Do not wait for
an owner reminder. Identify any authority or unresolved-decision blocker explicitly;
do not claim completion while a required documentation update remains outstanding.
