#!/usr/bin/env python3
"""Materialize the revision-2 prompt/ledger control plane from the valid r1 ledger."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
LEDGER = PROGRAM_DIR / "stage-ledger.md"
PROMPT_DIR = ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2"
SKILL_SCRIPTS = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")
sys.path.insert(0, str(SKILL_SCRIPTS))
from validate_stage_ledger import parse_ledger  # noqa: E402


PLAN = ".codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json"
PACK = ".codex/agents/generated/custometry-ui-design-g0-v2"
LEDGER_REL = ".codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md"
IMPACT = ".codex/delivery/ui-design-programs/custometry-v2/evidence/reconciliation-r2/change-impact-receipt.json"
R2_OWNER = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/visual-authority-decision-v2.json"
R2_INTAKE = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/ui-program-intake.json"
R2_BASELINE = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/platform-ui-baseline.json"
R2_RECON = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/requirement-reconciliation.json"
R2_CAPS = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/capability-intake.json"

R2_STAGES = [
    {
        "id": "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2", "gate": "G0", "target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
        "prompt": f"{PACK}/01-g0-authoritative-sources-r2.md", "title": "Authoritative sources and platform baseline reconciliation r2",
        "report": ".codex/delivery/evidence/custometry-ui-design-program-v2/g0-r2-execution-report.md",
        "transition": ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/stage-transition.json",
        "dependencies": "—", "owner": "N/A", "execution": "true", "supersedes": "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r1",
        "proof": "documentation authority, complete candidate file/hash provenance, current-source freshness, promoted-requirement reconciliation, accepted platform-baseline contracts, and control-plane validation; no target-screen design, browser runtime, implementation, accessibility-conformance, responsive-behavior, performance, publication, deployment, or mobile-specific proof",
        "touches": ".codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**, custometry-ui-blueprint-ru.md, docs/generated/requirement-index.json",
    },
    {
        "id": "G1@atlas-r2", "gate": "G1", "target": "atlas-r2",
        "prompt": f"{PACK}/11-g1-complete-screen-atlas-r2.md", "title": "Complete exact-cover screen and capability atlas r2",
        "report": ".codex/delivery/evidence/custometry-ui-design-program-v2/g1-r2-atlas-report.md",
        "transition": ".codex/delivery/ui-design-programs/custometry-v2/evidence/g1-r2/stage-transition.json",
        "dependencies": "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2", "owner": "N/A", "execution": "true", "supersedes": "G1@atlas-r1",
        "proof": "machine-rendered exact-cover screen and capability atlas, promoted-requirement binding, source reconciliation, deterministic rendering, and static contract validation; no target-screen design, browser runtime, implementation, accessibility-conformance, responsive-behavior, performance, publication, or deployment proof",
        "touches": ".codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**",
    },
    {
        "id": "G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2", "gate": "G2", "target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
        "prompt": f"{PACK}/21-g2-structure-r2.md", "title": "Journeys, families, and bounded waves r2",
        "report": ".codex/delivery/evidence/custometry-ui-design-program-v2/g2-r2-structure-report.md",
        "transition": ".codex/delivery/ui-design-programs/custometry-v2/evidence/g2-r2/stage-transition.json",
        "dependencies": "G1@atlas-r2", "owner": "N/A", "execution": "true", "supersedes": "G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r1",
        "proof": "machine-validated journey, family, coverage, representative, workload-budget, wave, and exact baseline-inheritance structure; no target-screen design, browser runtime, implementation, accessibility-conformance, responsive-behavior, performance, publication, or deployment proof",
        "touches": ".codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**",
    },
    {
        "id": "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2", "gate": "G3", "target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
        "prompt": f"{PACK}/31-g3-foundations-shell-r2.md", "title": "Foundations and application shell realization r2",
        "report": ".codex/delivery/evidence/custometry-ui-design-program-v2/g3-r2-foundations-shell-report.md",
        "transition": ".codex/delivery/ui-design-programs/custometry-v2/evidence/g3-r2/stage-transition.json",
        "dependencies": "G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2", "owner": "required", "execution": "false", "supersedes": "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r1",
        "proof": "finished foundations and shell review board with mode-correct browser, responsive-Web, and accessibility-smoke evidence; no production implementation, deployment, performance, or full WCAG conformance proof",
        "touches": ".codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**",
    },
    {
        "id": "G6@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2", "gate": "G6", "target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
        "prompt": f"{PACK}/61-g6-handoff-r2.md", "title": "Cross-program QA and implementation handoff r2",
        "report": ".codex/delivery/evidence/custometry-ui-design-program-v2/g6-r2-handoff-report.md",
        "transition": ".codex/delivery/ui-design-programs/custometry-v2/evidence/g6-r2/stage-transition.json",
        "dependencies": "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2", "owner": "required", "execution": "false", "supersedes": "G6@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r1",
        "proof": "cross-program review board, critical-journey proof, and reproducible implementation handoff; no publication, deployment, production, or full WCAG conformance proof",
        "touches": ".codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**",
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def visual_block() -> str:
    authority = json.loads((ROOT / PLAN).read_text(encoding="utf-8"))["visual_authority"]
    return "\n".join(f"  {key}: {value}" for key, value in authority.items() if key != "product_semantics_scope")


def prompt_body(stage: dict[str, str]) -> str:
    gate = stage["gate"]
    next_allowed = "true" if gate in {"G0", "G1", "G2"} else "false"
    entrypoints = {
        "G0": f"[{R2_OWNER}, {R2_RECON}, {R2_INTAKE}, {R2_BASELINE}]",
        "G1": f"[{PLAN}, {R2_INTAKE}, {R2_CAPS}, .codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/stage-transition.json]",
        "G2": f"[{PLAN}, .codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r2/screens-index.json, .codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r2/journeys-index.json]",
        "G3": f"[{PLAN}, {R2_BASELINE}, .codex/delivery/ui-design-programs/custometry-v2/evidence/g2-r2/stage-transition.json]",
        "G6": f"[{PLAN}, .codex/delivery/ui-design-programs/custometry-v2/evidence/g3-r2/stage-transition.json]",
    }[gate]
    tasks = {
        "G0": "Reconcile current canonical sources, all 74 pilot-candidate-v2 files and hashes, 68 OWNER-REC entries, 13 RECON-ADD requirements, conflicts, later-stage obligations, the canonical UI blueprint, and the revision-2 intake/platform baseline. Validate G0 and assemble only the adjacent G1 transition.",
        "G1": "After the exact incoming G0 r2 transition validates, rebuild the deterministic screen, journey, and capability atlas. Exact-cover 175 screens, 9 journeys, 22 capabilities, every OWNER-REC disposition, and all 13 RECON-ADD bindings; assemble only the adjacent G2 transition.",
        "G2": "Build source-backed journeys, criticality, families, representatives, coverage profiles, workload-bounded waves, and exact platform-baseline inheritance. This task remains unclaimed under the current authorization.",
        "G3": "Realize the accepted platform baseline and representative shell with canonical browser, responsive-Web, and accessibility-smoke evidence. This task is future-only and requires the validated G2 transition.",
        "G6": "Assemble final cross-program QA, critical-journey proof, and implementation handoff after all generated G4/G5 rows are accepted. This task is future-only.",
    }[gate]
    acceptance = {
        "G0": "intake_ready, baseline_ready, draft, source freshness, prompt/ledger synchronization, G0 gate, and the G0-to-G1 transition all pass; G1 remains unclaimed",
        "G1": "the live indexes exact-cover every intake screen, journey, capability, OWNER-REC disposition, and RECON-ADD binding exactly once; atlas_gate and the G1-to-G2 transition pass; G2 remains unclaimed",
        "G2": "journeys, families, coverage, representatives, waves, budgets, and baseline inheritance pass structure_gate",
        "G3": "program_ready plus canonical browser and finished-result review evidence pass before owner review",
        "G6": "handoff_ready completes with program_complete true only after exact family/wave coverage",
    }[gate]
    return f"""---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: {stage['id']}
gate_id: {gate}
target_id: {stage['target']}
title: {stage['title']}
report_path: {stage['report']}
proof_boundary: {stage['proof']}
expected_touch_zones: {stage['touches']}
blocker_policy: needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for owner_required product meaning; hard-block only unsafe or unrecoverable conditions
decision_packet: none
resume_condition: none
resume_evidence_ref: none
Next stage allowed: {next_allowed}
execution_allowed: {stage['execution']}
transition_receipt: {stage['transition']}
incoming_transition_receipt: none
incoming_transition_receipt_sha256: none
runtime_profile: codex.ui-stage-runtime-profiles/v1@1.6.0
execution_mode: goal_driven
goal_artifact_required: false
current_stage: {stage['id']}
rendered_review_target: {'none' if gate in {'G0','G1','G2'} else 'finished_visuals_only'}
known_stop_resolution: none
owner_review_target: {'non_visual_summary_for_G0-G2' if gate in {'G0','G1','G2'} else 'finished_visuals_only_for_G3-G6'}
plan_doc: {PLAN}
prompt_pack_dir: {PACK}
stage_ledger: {LEDGER_REL}

visual_authority:
{visual_block()}

prompt_pack_execution:
  plan_doc: {PLAN}
  prompt_pack_dir: {PACK}
  stage_ledger: {LEDGER_REL}

context:
  always_read: [AGENTS.md, .codex/AGENTS.md, {LEDGER_REL}]
  task_entrypoints: {entrypoints}
  conditional_bundles: [Read only the live ledger-bound context_manifest and named triggered bundles.]
  consult_if_needed: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/ui-route-contracts.json, packages/contracts/routes/ui-surface-contracts.json]

skills:
  primary: ui-design-program
  companions: []

validation_strategy:
  proof_boundary: {stage['proof']}
  evidence_target: {stage['report']}
  commands: [ui_program_context, validate_ui_design_program, validate_stage_ledger, assemble_stage_transition, validate_stage_transition]

file_manifest:
  expected_touch_zones: [{stage['touches']}]
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

Execute only `{stage['id']}` when the ledger independently selects and claims it. {tasks}

## Context / Current State

Revision 1 remains immutable historical evidence. Revision 2 uses the current canonical product/UI sources and the candidate only as visual-language/platform-baseline authority. Responsive Web is required; mobile-specific IA remains unauthorized.

## Requirements

Run `ui_program_context.py --ledger {LEDGER_REL} --project-root <root>` before claim, validate the exact incoming transition when present, claim atomically, regenerate context immediately, and consume only the emitted manifest. Preserve foreign changes and all authority limits.

# Context acquisition protocol

Read only the bounded post-claim manifest, exact pointers, and triggered bundles. Expand only for a named failed binding or validator error.

# Reading manifest

Respect the live profile limits of 16 files and approximately 600k estimated tokens.

# Work plan

1. Revalidate git status, triad, ledger, and incoming transition.
2. Claim only this stage and regenerate the ledger-bound context.
3. Build only the stage-owned deterministic artifacts and evidence.
4. Run the emitted gate, ledger, source-freshness, exact-cover, and adjacent-transition checks.
5. Update the ledger before reporting; never claim the adjacent stage without independent authorization.

# Acceptance criteria

{acceptance}.

# Implementation constraints

Do not rewrite r1 artifacts or receipts, hand-edit generated receipts, infer target-screen composition from the candidate, grant fixture/legend-threshold/mobile/production authority, mutate production code, publish, deploy, commit, push, create a PR, use secrets, or perform external side effects.

# Quality gates

Run the live profile-emitted commands, stage-specific deterministic builders/validators, `source scripts/activate-toolchain.sh`, and the smallest applicable repository local gate.

# Adjacent-stage preflight

Validate both the current gate and the exact adjacent transition receipt. Current-gate success alone never allows the next stage.

# Final output

Report stage status, changed paths, exact ledger state, validation results, proof boundary, excluded foreign changes, residual risks, and one safe next action in Russian.

## Execution control

Keep decision policy, file manifest, transition receipt, and `Next stage allowed` synchronized with the ledger. G0-G2 have no routine owner acceptance. Never infer acceptance from readiness alone.
"""


def render_detail(stage: dict[str, str], *, current_authority: str, invalidated: str, superseded_by: str, supersedes: str, historical: str) -> str:
    return f"""### `{stage['id']}`

- title: `{stage['title']}`
- report_path: `{stage['report']}`
- expected_touch_zones: `{stage['touches']}`
- proof_boundary: `{stage['proof']}`
- blocker_policy: `needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions`
- decision_packet: `none`
- resume_condition: `none`
- resume_evidence_ref: `none`
- resume_evidence_sha256: `none`
- transition_receipt: `{stage['transition']}`
- transition_receipt_sha256: `none`
- execution_allowed: `{stage['execution']}`
- replaces_stage: `none`
- repair_evidence_ref: `none`
- historical_outcome: `{historical}`
- current_authority: `{current_authority}`
- invalidated_by_ref: `{invalidated}`
- superseded_by_stage: `{superseded_by}`
- supersedes_stage: `{supersedes}`
- incoming_transition_receipt: `none`
- incoming_transition_receipt_sha256: `none`
"""


def main() -> None:
    parsed, errors = parse_ledger(LEDGER)
    if errors or any(row["Stage instance"].endswith("-r2") or row["Stage instance"] == "G1@atlas-r2" for row in parsed.get("rows", [])):
        raise SystemExit(f"control plane expects the pristine valid r1 frontier; errors={errors}")

    for stage in R2_STAGES:
        atomic_write(ROOT / stage["prompt"], prompt_body(stage))

    successor = {stage["supersedes"]: stage["id"] for stage in R2_STAGES}
    old_rows = []
    old_details = []
    for row in parsed["rows"]:
        stage_id = row["Stage instance"]
        detail = parsed["details"][stage_id]
        old_status = row["Status"]
        row = dict(row)
        if old_status not in {"accepted", "blocked", "skipped"}:
            row["Status"] = "superseded"
        row["Executor claim"] = row["Executor claim"] if old_status == "accepted" else "—"
        row["Claimed at"] = row["Claimed at"] if old_status == "accepted" else "—"
        old_rows.append(row)
        pseudo = {
            "id": stage_id, "title": detail["title"], "report": detail["report_path"],
            "touches": detail["expected_touch_zones"], "proof": detail["proof_boundary"],
            "transition": detail["transition_receipt"], "execution": "false",
        }
        rendered = render_detail(
            pseudo,
            current_authority="false",
            invalidated=IMPACT,
            superseded_by=successor[stage_id],
            supersedes="none",
            historical=(old_status if old_status in {"accepted", "needs_input", "blocked", "skipped", "superseded"} else "superseded"),
        )
        if old_status == "accepted":
            rendered = rendered.replace("- transition_receipt_sha256: `none`", f"- transition_receipt_sha256: `{detail['transition_receipt_sha256']}`")
        old_details.append(rendered)

    rows = old_rows + [{
        "Stage instance": stage["id"], "Gate": stage["gate"], "Target ID": stage["target"],
        "Prompt": stage["prompt"], "Status": "pending", "Dependencies": stage["dependencies"],
        "Evidence": stage["report"], "Transition receipt": stage["transition"],
        "Owner decision": stage["owner"], "Executor claim": "—", "Claimed at": "—",
    } for stage in R2_STAGES]
    columns = ["Stage instance", "Gate", "Target ID", "Prompt", "Status", "Dependencies", "Evidence", "Transition receipt", "Owner decision", "Executor claim", "Claimed at"]
    table = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    table.extend("| " + " | ".join(row[column] for column in columns) + " |" for row in rows)
    details = old_details + [render_detail(stage, current_authority="true", invalidated="none", superseded_by="none", supersedes=stage["supersedes"], historical="none") for stage in R2_STAGES]
    ledger = f"""---
artifact_kind: ui_design_program_stage_ledger
ledger_status: active
execution_mode: goal_driven
goal_artifact_required: false
plan_doc: {PLAN}
prompt_pack_dir: {PACK}
stage_ledger: {LEDGER_REL}
current_stage: G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2
Next stage allowed: true
---

# Custometry UI Design Program V2 Stage Ledger

{chr(10).join(table)}

## Stage details

{chr(10).join(details)}
## Current owner input

- Decision packet: `none`
- Questions: `none`
- Resume condition: `none`

## Current blockers

- `none`

## Latest validation

- Commands: `assemble_change_impact.py; build_g0_r2_artifacts.py; validate_ui_design_program.py --profile intake_ready; validate_ui_design_program.py --profile baseline_ready; validate_ui_design_program.py --profile draft`
- Observed boundary: `revision-2 control-plane bootstrap and static source/artifact coherence only; G0 r2 is pending and unclaimed`
- Result: `passed; r1 dependency closure invalidated by typed impact receipt; one G0 r2 pending executable frontier`

## File manifest summary

- created: [`{R2_OWNER}`, `{R2_INTAKE}`, `{R2_BASELINE}`, `{R2_RECON}`, `{R2_CAPS}`, `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r2/**`, `.codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/**`, revision-2 prompts]
- modified: [`{PLAN}`, `{LEDGER_REL}`]
- deleted: []
- outside_expected_paths: []
- foreign_changes_excluded: true

## Handoff

- Residual risk: `G0 r2 must still reconcile the canonical UI blueprint, rerun source freshness, assemble its adjacent transition, and accept only from a validated ready receipt.`
- Next executor must know: `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2 is the sole pending executable row. Revision-1 artifacts and receipts remain historical and byte-unchanged.`
- Transition receipt: `{R2_STAGES[0]['transition']}`
- Next stage allowed: true
"""
    atomic_write(LEDGER, ledger)
    print(json.dumps({"status": "passed", "prompts": [stage["prompt"] for stage in R2_STAGES], "ledger_sha256": sha256(LEDGER)}, indent=2))


if __name__ == "__main__":
    main()
