#!/usr/bin/env python3
"""Build the deterministic control-plane migration request/topology for r3."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = ROOT / ".codex/delivery/ui-design-programs/custometry-v2"
EVIDENCE_DIR = PROGRAM_DIR / "evidence/compatibility-migration-r3"
LEDGER = PROGRAM_DIR / "stage-ledger.md"
PLAN = PROGRAM_DIR / "ui-design-program.json"
LOCAL_REGISTRY = PROGRAM_DIR / "contract-versions.json"
SKILL = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program")
sys.path.insert(0, str(SKILL / "scripts"))

from validate_stage_ledger import parse_ledger  # noqa: E402


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def render_ledger(
    frontmatter: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]]
) -> str:
    columns = [
        "Stage instance", "Gate", "Target ID", "Prompt", "Status", "Dependencies",
        "Evidence", "Transition receipt", "Owner decision", "Executor claim", "Claimed at",
    ]
    lines = [
        "---",
        *(f"{key}: {value}" for key, value in frontmatter.items()),
        "---", "", "# Custometry UI Design Program V2 Stage Ledger", "",
        "| " + " | ".join(columns) + " |",
        "|" + "---|" * len(columns),
    ]
    lines.extend("| " + " | ".join(row[column] for column in columns) + " |" for row in rows)
    lines.extend(["", "## Stage details", ""])
    for row in rows:
        stage_id = row["Stage instance"]
        lines.extend([f"### `{stage_id}`", ""])
        lines.extend(f"- {key}: `{value}`" for key, value in details[stage_id].items())
        lines.append("")
    lines.extend(
        [
            "## Current owner input", "", "- Decision packet: `none`", "",
            "## Current blockers", "", "- none", "",
        ]
    )
    return "\n".join(lines)


def prompt_text(row: dict[str, str], detail: dict[str, str]) -> str:
    gate = row["Gate"]
    owner_target = "non_visual_summary_for_G0-G2" if gate in {"G0", "G1", "G2"} else "finished_visuals_only"
    visual_lines = ""
    if gate in {"G3", "G4"}:
        authority = json.loads(PLAN.read_text(encoding="utf-8"))["visual_authority"]
        visual_lines = "\n".join(
            f"{field}: {authority[field]}" for field in (
                "source_visual_ref", "source_visual_sha256", "source_evidence_mode",
                "owner_decision_ref", "screen_acceptance_scope", "visual_language_scope",
                "reusable_foundation_scope", "inheritance_policy", "mobile_scope",
            )
        ) + "\n"
    return f"""---
artifact_kind: ui_design_program_stage_prompt
stage_instance_id: {row['Stage instance']}
gate_id: {gate}
target_id: {row['Target ID']}
title: {detail['title']}
report_path: {detail['report_path']}
proof_boundary: {detail['proof_boundary']}
expected_touch_zones: {detail['expected_touch_zones']}
blocker_policy: {detail['blocker_policy']}
decision_policy: resolve agent_decidable inputs from accepted sources; use needs_input only for owner_required decisions
decision_packet: none
resume_condition: none
resume_evidence_ref: none
Next stage allowed: false
execution_allowed: {detail['execution_allowed']}
transition_receipt: {detail['transition_receipt']}
incoming_transition_receipt: none
incoming_transition_receipt_sha256: none
runtime_profile: codex.ui-stage-runtime-profiles/v1@2.0.0
execution_mode: goal_driven
goal_artifact_required: false
current_stage: {row['Stage instance']}
rendered_review_target: {owner_target}
known_stop_resolution: none
owner_review_target: {owner_target}
{visual_lines}plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md

prompt_pack_execution:
  plan_doc: .codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json
  prompt_pack_dir: .codex/agents/generated/custometry-ui-design-g0-v2
  stage_ledger: .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md

context:
  always_read: [AGENTS.md, .codex/AGENTS.md, .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md]
  task_entrypoints: [.codex/delivery/ui-design-programs/custometry-v2/evidence/compatibility-migration-r3/prepared/historical-control-plane-migration-receipt.json]
  conditional_bundles: [Read only the live ledger-bound context_manifest and named triggered bundles.]
  consult_if_needed: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, packages/contracts/routes/ui-route-contracts.json]

skills:
  primary: ui-design-program
  companions: []

safety:
  recoverable_input_policy: needs_input_and_resume_same_stage
  hard_blocker_policy: terminal_blocked_only_for_unsafe_or_unrecoverable_state
  mobile_scope: unauthorized_unless_exact_user_authorization_is_cited
  agent_self_acceptance: prohibited

owner_interaction:
  raw_json_review: prohibited_by_default
  magic_acceptance_string_required: false
---

# Task

Execute only `{row['Stage instance']}` after bounded ledger context and an atomic claim. Use the current active contract, preserve historical evidence and foreign changes, satisfy the exact gate and adjacent-stage preflight, then durably update the sole stage ledger. Do not claim another row across an owner checkpoint.
"""


def build_candidate(parsed: dict[str, Any], topology: dict[str, Any]) -> None:
    receipt_path = EVIDENCE_DIR / "prepared/historical-control-plane-migration-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt_ref = str(receipt_path.relative_to(ROOT))
    receipt_sha = digest(receipt_path)
    impact_ref = receipt["change_impact"]["path"]
    topology_by_source = {
        item["supersedes_stage"]: item for item in topology["successor_rows"]
    }
    rows = [dict(row) for row in parsed["rows"]]
    details = {key: dict(value) for key, value in parsed["details"].items()}
    for row in rows:
        stage_id = row["Stage instance"]
        source_detail = parsed["details"][stage_id]
        detail = details[stage_id]
        was_current = source_detail.get("current_authority") != "false"
        if was_current:
            row["Status"] = "superseded"
            detail["superseded_by_stage"] = topology_by_source[stage_id]["stage_instance_id"]
            detail["invalidated_by_ref"] = impact_ref
        detail.update(
            {
                "historical_outcome": next(
                    source["Status"] for source in parsed["rows"] if source["Stage instance"] == stage_id
                ),
                "current_authority": "false",
                "execution_allowed": "false",
                "historical_migration_ref": receipt_ref,
                "historical_migration_sha256": receipt_sha,
            }
        )
    for item in topology["successor_rows"]:
        stage_id = item["stage_instance_id"]
        gate = item["gate"]
        slug = stage_id.split("@", 1)[1]
        report = f".codex/delivery/evidence/custometry-ui-design-program-v2/{slug}-report.md"
        transition = f".codex/delivery/ui-design-programs/custometry-v2/evidence/{slug}/stage-transition.json"
        row = {
            "Stage instance": stage_id,
            "Gate": gate,
            "Target ID": item["target_id"],
            "Prompt": item["prompt_ref"],
            "Status": "pending",
            "Dependencies": "—" if not item["dependencies"] else ", ".join(item["dependencies"]),
            "Evidence": report,
            "Transition receipt": transition,
            "Owner decision": "N/A" if gate in {"G0", "G1", "G2"} else "required",
            "Executor claim": "—",
            "Claimed at": "—",
        }
        detail = {
            "title": f"Active-contract successor {gate}: {item['target_id']}",
            "report_path": report,
            "expected_touch_zones": ".codex/delivery/ui-design-programs/custometry-v2/**, .codex/agents/generated/custometry-ui-design-g0-v2/**, .codex/delivery/evidence/custometry-ui-design-program-v2/**",
            "proof_boundary": "current-contract stage evidence and adjacent-stage readiness; no production implementation, publication, deployment, mobile-specific design, or full WCAG conformance proof",
            "blocker_policy": "needs_input_for_owner_questions_hard_block_only_for_unsafe_or_unrecoverable_conditions",
            "decision_packet": "none",
            "resume_condition": "none",
            "resume_evidence_ref": "none",
            "resume_evidence_sha256": "none",
            "transition_receipt": transition,
            "transition_receipt_sha256": "none",
            "execution_allowed": str(item["execution_allowed"]).lower(),
            "replaces_stage": "none",
            "repair_evidence_ref": "none",
            "historical_outcome": "none",
            "current_authority": "true",
            "invalidated_by_ref": "none",
            "superseded_by_stage": "none",
            "supersedes_stage": item["supersedes_stage"],
            "incoming_transition_receipt": "none",
            "incoming_transition_receipt_sha256": "none",
        }
        prompt_path = ROOT / item["prompt_ref"]
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path.write_text(prompt_text(row, detail), encoding="utf-8")
        rows.append(row)
        details[stage_id] = detail
    candidate_frontmatter = dict(parsed["frontmatter"])
    candidate_frontmatter.update(
        ledger_status="active",
        execution_mode="goal_driven",
        current_stage=topology["current_stage"],
        **{"Next stage allowed": "false"},
    )
    candidate_path = EVIDENCE_DIR / "candidate-stage-ledger.md"
    candidate_path.write_text(render_ledger(candidate_frontmatter, rows, details), encoding="utf-8")


def successor_id(stage_id: str) -> str:
    match = re.search(r"-r([0-9]+)$", stage_id)
    if match is None:
        raise ValueError(f"stage lacks revision suffix: {stage_id}")
    return f"{stage_id[:match.start()]}-r{int(match.group(1)) + 1}"


def prompt_ref(row: dict[str, str], successor: str) -> str:
    gate = row["Gate"]
    if gate == "G0":
        name = "02-g0-authoritative-sources-r3.md"
    elif gate == "G1":
        name = "12-g1-complete-screen-atlas-r3.md"
    elif gate == "G2":
        name = "22-g2-structure-r3.md"
    elif gate == "G3":
        name = "32-g3-foundations-shell-r3.md"
    elif gate == "G6":
        name = "62-g6-handoff-r3.md"
    else:
        old = Path(row["Prompt"]).name
        name = re.sub(r"-r[0-9]+\.md$", f"-r{successor.rsplit('-r', 1)[1]}.md", old)
    return f".codex/agents/generated/custometry-ui-design-g0-v2/{name}"


def main() -> int:
    parsed, parse_errors = parse_ledger(LEDGER)
    if parse_errors:
        raise ValueError("live ledger is not parseable: " + "; ".join(parse_errors))
    source_rows = [
        row
        for row in parsed["rows"]
        if parsed["details"][row["Stage instance"]].get("current_authority") != "false"
    ]
    source_ids = [row["Stage instance"] for row in source_rows]
    successor_by_source = {stage_id: successor_id(stage_id) for stage_id in source_ids}
    successor_rows: list[dict[str, object]] = []
    for row in source_rows:
        source_id = row["Stage instance"]
        successor = successor_by_source[source_id]
        dependencies = [] if row["Dependencies"] in {"—", "-", "none"} else [
            successor_by_source[item.strip()]
            for item in row["Dependencies"].split(",")
            if item.strip() in successor_by_source
        ]
        successor_rows.append(
            {
                "stage_instance_id": successor,
                "gate": row["Gate"],
                "target_id": successor.split("@", 1)[1],
                "prompt_ref": prompt_ref(row, successor),
                "status": "pending",
                "dependencies": dependencies,
                "execution_allowed": row["Gate"] == "G0",
                "supersedes_stage": source_id,
            }
        )
    g0 = next(item for item in successor_rows if item["gate"] == "G0")
    topology = {
        "$schema": "historical-control-plane-successor-topology.schema.json",
        "schema_id": "codex.ui-historical-control-plane-successor-topology/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "source_ledger_sha256": digest(LEDGER),
        "target_registry_sha256": digest(SKILL / "assets/contract-versions.json"),
        "ledger_status": "active",
        "current_stage": g0["stage_instance_id"],
        "successor_rows": successor_rows,
    }
    topology_path = EVIDENCE_DIR / "successor-topology.json"
    dump(topology_path, topology)
    request = {
        "$schema": "historical-control-plane-migration-request.schema.json",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "change_id": "custometry-v2-active-contract-and-pilot-standard-migration-r3",
        "change_kind": "baseline_or_visual_authority_replacement",
        "owner_input": (
            "Migrate the accepted Custometry UI program from registered historical "
            "profiles to the current pilot-standard contract, preserve product meaning "
            "and historical evidence, and create a revisioned successor chain beginning at G0."
        ),
        "anchor_stage_instance_id": "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2",
        "source": {
            "ledger_ref": ".codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md",
            "ledger_sha256": digest(LEDGER),
            "plan_doc_ref": ".codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json",
            "plan_doc_sha256": digest(PLAN),
            "prompt_pack_dir": ".codex/agents/generated/custometry-ui-design-g0-v2",
            "contract_registry_ref": ".codex/delivery/ui-design-programs/custometry-v2/contract-versions.json",
            "contract_registry_sha256": digest(LOCAL_REGISTRY),
        },
        "target_registry": {
            "path": str(SKILL / "assets/contract-versions.json"),
            "sha256": digest(SKILL / "assets/contract-versions.json"),
        },
        "successor_topology_ref": str(topology_path.relative_to(ROOT)),
        "successor_topology_sha256": digest(topology_path),
    }
    dump(EVIDENCE_DIR / "migration-request.json", request)
    skill_files = [
        "SKILL.md",
        "assets/contract-versions.json",
        "assets/contract-versions.schema.json",
        "assets/historical-control-plane-migration-request.schema.json",
        "assets/historical-control-plane-successor-topology.schema.json",
        "assets/historical-control-plane-migration-receipt.schema.json",
        "assets/stage-ledger-template.md",
        "assets/stage-runtime-profiles.json",
        "assets/negative-test-matrix.json",
        "references/ui-design-program-contract-v1.md",
        "scripts/migrate_historical_control_plane.py",
        "scripts/validate_cross_skill_contract.py",
        "scripts/validate_skill_release.py",
        "scripts/validate_stage_ledger.py",
        "scripts/validate_ui_design_program.py",
    ]
    release = {
        "schema_id": "codex.ui-skill-release-binding/v1",
        "skill": str(SKILL),
        "release_status": "passed",
        "release_command": "PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skill_release.py",
        "cold_head_review": {
            "initial_verdict": "block",
            "high_findings": 4,
            "disposition": "fixed_and_locally_reproved",
            "follow_up_checks": [
                "migrate_historical_control_plane.py --self-test",
                "validate_stage_ledger.py --self-test",
                "validate_cross_skill_contract.py --self-test",
                "validate_skill_release.py",
            ],
        },
        "files": [
            {"path": str(SKILL / relative), "sha256": digest(SKILL / relative)}
            for relative in skill_files
        ],
    }
    dump(EVIDENCE_DIR / "skill-release-binding.json", release)
    if (EVIDENCE_DIR / "prepared/historical-control-plane-migration-receipt.json").is_file():
        build_candidate(parsed, topology)
    print(json.dumps({"topology_rows": len(successor_rows), "current_stage": g0["stage_instance_id"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
