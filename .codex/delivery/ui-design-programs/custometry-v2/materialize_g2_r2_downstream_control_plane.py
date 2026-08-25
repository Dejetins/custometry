#!/usr/bin/env python3
"""Materialize deterministic current-authority G4/G5 rows after G2 structure."""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
PROGRAM = PROGRAM_DIR / "ui-design-program.json"
LEDGER = PROGRAM_DIR / "stage-ledger.md"
PACK = ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2"
RUNTIME_PROFILE = "codex.ui-stage-runtime-profiles/v1@1.6.0"
PLAN_REL = ".codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json"
PACK_REL = ".codex/agents/generated/custometry-ui-design-g0-v2"
LEDGER_REL = ".codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md"
TOUCH_ZONES = ".codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**"
BLOCKER_POLICY = "needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions"
G3_ID = "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2"
G6_ID = "G6@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        handle.write(value)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def visual_block(authority: dict[str, Any]) -> str:
    fields = (
        "source_visual_ref",
        "source_visual_sha256",
        "source_evidence_mode",
        "owner_decision_ref",
        "screen_acceptance_scope",
        "visual_language_scope",
        "reusable_foundation_scope",
        "inheritance_policy",
        "mobile_scope",
    )
    return "\n".join(f"  {field}: {authority[field]}" for field in fields)


def prompt_text(
    *,
    stage_id: str,
    gate: str,
    target_id: str,
    title: str,
    report_path: str,
    transition_path: str,
    evidence_target: str,
    dependency_kind: str,
    acceptance: str,
    authority: dict[str, Any],
) -> str:
    proof = (
        "finished family review board with exact representative screen/state coverage, canonical browser evidence, responsive-Web proof, and accessibility smoke; no production implementation, deployment, performance, or full WCAG conformance proof"
        if gate == "G4"
        else "finished wave review board with exact screen coverage, canonical browser evidence, responsive-Web proof, and accessibility smoke; no production implementation, deployment, performance, or full WCAG conformance proof"
    )
    return f"""---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: {stage_id}
gate_id: {gate}
target_id: {target_id}
title: {title}
report_path: {report_path}
proof_boundary: {proof}
expected_touch_zones: {TOUCH_ZONES}
blocker_policy: {BLOCKER_POLICY}
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for owner_required product meaning or finished-result review; hard-block only unsafe or unrecoverable conditions
decision_packet: none
resume_condition: none
resume_evidence_ref: none
Next stage allowed: false
execution_allowed: false
transition_receipt: {transition_path}
incoming_transition_receipt: none
incoming_transition_receipt_sha256: none
runtime_profile: {RUNTIME_PROFILE}
execution_mode: goal_driven
goal_artifact_required: false
current_stage: {stage_id}
rendered_review_target: finished_visuals_only
known_stop_resolution: none
owner_review_target: finished_visuals_only_for_G3-G6
plan_doc: {PLAN_REL}
prompt_pack_dir: {PACK_REL}
stage_ledger: {LEDGER_REL}

visual_authority:
{visual_block(authority)}

prompt_pack_execution:
  plan_doc: {PLAN_REL}
  prompt_pack_dir: {PACK_REL}
  stage_ledger: {LEDGER_REL}

context:
  always_read: [AGENTS.md, .codex/AGENTS.md, {LEDGER_REL}]
  task_entrypoints: [{PLAN_REL}, {evidence_target}]
  conditional_bundles: [Read only the live ledger-bound context_manifest and named triggered bundles.]
  consult_if_needed: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md]

skills:
  primary: ui-design-program
  companions: [browser-qa-evidence, playwright-cli]

validation_strategy:
  proof_boundary: {proof}
  evidence_target: {report_path}
  commands: [ui_program_context, validate_ui_design_program, playwright-cli, validate_stage_ledger, assemble_stage_transition, validate_stage_transition]

file_manifest:
  expected_touch_zones: [{TOUCH_ZONES}]
  foreign_changes_excluded: true

safety:
  recoverable_input_policy: needs_input_and_resume_same_stage
  hard_blocker_policy: terminal_blocked_only_for_unsafe_or_unrecoverable_state
  mobile_scope: unauthorized_unless_exact_user_authorization_is_cited
  agent_self_acceptance: prohibited
  repeated_write_authorization: prohibited_when_current_task_already_authorizes_owned_paths

owner_interaction:
  raw_json_review: prohibited_by_default
  full_screen_inventory_review: prohibited_by_default
  max_questions_per_checkpoint: 3
  magic_acceptance_string_required: false
---

# Task

Execute only `{stage_id}` when the ledger independently selects and claims it. Complete one bounded {dependency_kind} review unit from the accepted G2 structure and G3 foundations.

## Context / Current State

Use the accepted revision-2 product intent, exact platform baseline, visual-language authority limits, responsive-Web contract, and mobile scope `unauthorized`. Do not infer exact target composition from the candidate.

## Requirements

Run the ledger-bound context workflow before claim, validate the exact incoming transition, claim atomically, regenerate context, and consume only the emitted manifest. Produce finished visuals and canonical browser evidence before owner review.

# Context acquisition protocol

Read only the bounded post-claim manifest, exact pointers, and triggered bundles. Expand only for a named failed binding or validator error.

# Reading manifest

Respect the live profile limits of 16 files and approximately 600k estimated tokens.

# Work plan

1. Revalidate status, triad, ledger, and incoming transition.
2. Claim only this row and regenerate context.
3. Build the exact bounded {dependency_kind} artifacts and browser evidence.
4. Assemble the typed review board and strict gate evidence.
5. Enter `needs_input` with `review_ready`; accept only after natural-language owner acceptance is canonically recorded.

# Acceptance criteria

{acceptance}

# Implementation constraints

Do not change product semantics, accepted baseline authority, mobile scope, production code, publication state, deployment, secrets, or another family/wave. Do not hand-edit receipts.

# Quality gates

Run the emitted runtime-profile commands, canonical `playwright-cli` evidence, the strict aggregate validator, ledger validation, and adjacent transition validation.

# Adjacent-stage preflight

Current-gate success alone never allows the next row. G4 closes from one exact-cover family aggregate; G5 closes from one exact-cover wave aggregate.

# Final output

Show the finished review board, material exceptions, concise validation boundary, and at most three genuine owner questions. Keep raw JSON and hashes in linked evidence.
"""


def detail_block(
    *,
    stage_id: str,
    title: str,
    report_path: str,
    transition_path: str,
    proof: str,
) -> str:
    return f"""### `{stage_id}`

- title: `{title}`
- report_path: `{report_path}`
- expected_touch_zones: `{TOUCH_ZONES}`
- proof_boundary: `{proof}`
- blocker_policy: `{BLOCKER_POLICY}`
- decision_packet: `none`
- resume_condition: `none`
- resume_evidence_ref: `none`
- resume_evidence_sha256: `none`
- transition_receipt: `{transition_path}`
- transition_receipt_sha256: `none`
- execution_allowed: `false`
- replaces_stage: `none`
- repair_evidence_ref: `none`
- historical_outcome: `none`
- current_authority: `true`
- invalidated_by_ref: `none`
- superseded_by_stage: `none`
- supersedes_stage: `none`
- incoming_transition_receipt: `none`
- incoming_transition_receipt_sha256: `none`

"""


def main() -> None:
    program = load_json(PROGRAM)
    ledger = LEDGER.read_text(encoding="utf-8")
    families = program["families"]
    waves = program["waves"]
    authority = program["visual_authority"]
    family_rows: list[str] = []
    wave_rows: list[str] = []
    detail_blocks: list[str] = []
    g4_ids: list[str] = []
    wave_stage_by_target: dict[str, str] = {}
    family_proof = "finished family review board with exact representative screen/state coverage, canonical browser evidence, responsive-Web proof, and accessibility smoke; no production implementation, deployment, performance, or full WCAG conformance proof"
    wave_proof = "finished wave review board with exact screen coverage, canonical browser evidence, responsive-Web proof, and accessibility smoke; no production implementation, deployment, performance, or full WCAG conformance proof"
    for index, family in enumerate(families, start=1):
        family_id = family["family_id"]
        stage_id = f"G4@{family_id}-r2"
        target_id = f"{family_id}-r2"
        safe = slug(family_id)
        prompt_rel = f"{PACK_REL}/40-g4-{index:02d}-{safe}-r2.md"
        prompt_path = ROOT / prompt_rel
        report_path = f".codex/delivery/evidence/custometry-ui-design-program-v2/g4-r2/{safe}-family-report.md"
        transition_path = f".codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r2/{safe}/stage-transition.json"
        title = f"Family acceptance: {family_id}"
        write_text(
            prompt_path,
            prompt_text(
                stage_id=stage_id,
                gate="G4",
                target_id=target_id,
                title=title,
                report_path=report_path,
                transition_path=transition_path,
                evidence_target=f".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/families/{family_id}.json",
                dependency_kind="family",
                acceptance="The family aggregate exact-covers every declared representative screen/state and passes `family_acceptance` before finished-result review.",
                authority=authority,
            ),
        )
        family_rows.append(
            f"| {stage_id} | G4 | {target_id} | {prompt_rel} | pending | {G3_ID} | {report_path} | {transition_path} | required | — | — |"
        )
        detail_blocks.append(
            detail_block(
                stage_id=stage_id,
                title=title,
                report_path=report_path,
                transition_path=transition_path,
                proof=family_proof,
            )
        )
        g4_ids.append(stage_id)
    for index, wave in enumerate(waves, start=1):
        wave_id = wave["wave_id"]
        stage_id = f"G5@{wave_id}-r2"
        wave_stage_by_target[wave_id] = stage_id
        target_id = f"{wave_id}-r2"
        safe = slug(wave_id)
        prompt_rel = f"{PACK_REL}/50-g5-{index:02d}-{safe}-r2.md"
        prompt_path = ROOT / prompt_rel
        report_path = f".codex/delivery/evidence/custometry-ui-design-program-v2/g5-r2/{safe}-wave-report.md"
        transition_path = f".codex/delivery/ui-design-programs/custometry-v2/evidence/g5-r2/{safe}/stage-transition.json"
        title = f"Wave acceptance: {wave_id}"
        dependencies = [*g4_ids, *(wave_stage_by_target[item] for item in wave["depends_on"])]
        write_text(
            prompt_path,
            prompt_text(
                stage_id=stage_id,
                gate="G5",
                target_id=target_id,
                title=title,
                report_path=report_path,
                transition_path=transition_path,
                evidence_target=f".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r2/waves/{wave_id}.json",
                dependency_kind="wave",
                acceptance="The wave aggregate exact-covers every declared screen and passes `wave_acceptance` before finished-result review.",
                authority=authority,
            ),
        )
        wave_rows.append(
            f"| {stage_id} | G5 | {target_id} | {prompt_rel} | pending | {', '.join(dependencies)} | {report_path} | {transition_path} | required | — | — |"
        )
        detail_blocks.append(
            detail_block(
                stage_id=stage_id,
                title=title,
                report_path=report_path,
                transition_path=transition_path,
                proof=wave_proof,
            )
        )
    table_lines = ledger.splitlines()
    filtered: list[str] = []
    for line in table_lines:
        if line.startswith("| G4@") and line.rstrip().endswith("| — | — |"):
            continue
        if line.startswith("| G5@") and line.rstrip().endswith("| — | — |"):
            continue
        if line.startswith(f"| {G6_ID} "):
            parts = [item.strip() for item in line.strip().strip("|").split("|")]
            parts[5] = ", ".join(wave_stage_by_target[wave["wave_id"]] for wave in waves)
            line = "| " + " | ".join(parts) + " |"
            filtered.extend([*family_rows, *wave_rows])
        filtered.append(line)
    rendered = "\n".join(filtered) + "\n"
    rendered = re.sub(
        r"(?ms)^### `G[45]@[^\n]+-r2`\n.*?(?=^### `)",
        "",
        rendered,
    )
    g6_marker = f"### `{G6_ID}`"
    if g6_marker not in rendered:
        raise ValueError("G6 r2 detail marker is missing")
    rendered = rendered.replace(g6_marker, "".join(detail_blocks) + g6_marker, 1)
    write_text(LEDGER, rendered)
    print(
        json.dumps(
            {
                "status": "passed",
                "families": len(families),
                "g4_rows": len(family_rows),
                "waves": len(waves),
                "g5_rows": len(wave_rows),
                "g6_dependencies": len(waves),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
