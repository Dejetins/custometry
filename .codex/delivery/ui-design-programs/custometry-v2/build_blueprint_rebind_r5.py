#!/usr/bin/env python3
"""Build the product-semantics G0 successor control plane for blueprint rebind r5."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
LEDGER = DIR / "stage-ledger.md"
PLAN = DIR / "ui-design-program.json"
LOCAL_REGISTRY = DIR / "contract-versions.json"
ARTIFACTS = DIR / "artifacts/g0-r5"
PROMOTION = ARTIFACTS / "ui-design-program.promotion-candidate.json"
MIGRATION = DIR / "evidence/blueprint-rebind-r5/active-semantic-migration"
PREPARED = MIGRATION / "prepared"
TOPOLOGY = MIGRATION / "successor-topology.json"
REQUEST = MIGRATION / "migration-request.json"
CANDIDATE = MIGRATION / "candidate-stage-ledger.md"
RECEIPT = PREPARED / "historical-control-plane-migration-receipt.json"
SKILL = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program")
sys.path.insert(0, str(SKILL / "scripts"))

from validate_stage_ledger import canonical_sha256, parse_ledger, validate_ledger  # noqa: E402


PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"
ANCHOR = "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4"
G0_SUCCESSOR = "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5"
COLUMNS = (
    "Stage instance", "Gate", "Target ID", "Prompt", "Status", "Dependencies",
    "Evidence", "Transition receipt", "Owner decision", "Executor claim", "Claimed at",
)
SOURCE_HASH_REPLACEMENTS = {
    "cbf4cbcbb3068f1984c5c6c907ecd4d6f9a0639673cf6bd678e9c4280ced6fb6":
        "3ac695caddf50260728e9f40422f14a87e66818557e7ee324021215dd9a38d24",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def bump(value: str) -> str:
    match = re.search(r"-r([0-9]+)$", value)
    if match is None:
        raise ValueError(f"revision suffix required: {value}")
    return value[:match.start()] + f"-r{int(match.group(1)) + 1}"


def successor_id(row: dict[str, str]) -> str:
    return bump(row["Stage instance"])


def successor_target(row: dict[str, str]) -> str:
    return bump(row["Target ID"])


def successor_prompt(row: dict[str, str]) -> str:
    fixed = {
        "G0": "04-g0-authoritative-sources-r5.md",
        "G1": "13-g1-complete-screen-atlas-r4.md",
        "G2": "23-g2-structure-r4.md",
        "G3": "34-g3-foundations-shell-r5.md",
        "G6": "64-g6-handoff-r5.md",
    }
    if row["Gate"] in fixed:
        name = fixed[row["Gate"]]
    else:
        old = Path(row["Prompt"]).name
        revision = successor_id(row).rsplit("-r", 1)[1]
        name = re.sub(r"-r[0-9]+\.md$", f"-r{revision}.md", old)
    return f".codex/agents/generated/custometry-ui-design-g0-v2/{name}"


def successor_paths(row: dict[str, str], target: str) -> tuple[str, str]:
    if row["Gate"] == "G0":
        return (
            ".codex/delivery/evidence/custometry-ui-design-program-v2/g0-r5-source-rebind-report.md",
            ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r5/stage-transition.json",
        )
    if row["Gate"] == "G3":
        return (
            ".codex/delivery/evidence/custometry-ui-design-program-v2/g3-r5-foundations-shell-report.md",
            ".codex/delivery/ui-design-programs/custometry-v2/evidence/g3-r5/stage-transition.json",
        )
    if row["Gate"] == "G6":
        return (
            ".codex/delivery/evidence/custometry-ui-design-program-v2/g6-r5-handoff-report.md",
            ".codex/delivery/ui-design-programs/custometry-v2/evidence/g6-r5/stage-transition.json",
        )
    if row["Stage instance"] == "G4@family.auth.shell-auth.baseline-exception-auth-r5":
        return (
            ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r6/family-auth-shell-auth-baseline-exception-auth/review-board.html",
            ".codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth/stage-transition.json",
        )
    evidence = row["Evidence"].replace(row["Target ID"], target)
    transition = row["Transition receipt"]
    transition = transition.replace(row["Target ID"], target)
    return evidence, transition


def replace_line(text: str, key: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^{re.escape(key)}:\s*.*$")
    if len(pattern.findall(text)) != 1:
        raise ValueError(f"prompt requires one {key} line: {key}")
    return pattern.sub(f"{key}: {value}", text)


def build_prompt(
    source_row: dict[str, str], successor: dict[str, Any], detail: dict[str, str], receipt_hash: str | None
) -> None:
    text = (ROOT / source_row["Prompt"]).read_text(encoding="utf-8")
    text = text.replace(source_row["Stage instance"], successor["stage_instance_id"])
    for key, value in (
        ("target_id", successor["target_id"]),
        ("title", detail["title"]),
        ("report_path", detail["report_path"]),
        ("transition_receipt", detail["transition_receipt"]),
        ("execution_allowed", detail["execution_allowed"]),
    ):
        text = replace_line(text, key, value)
    for key in ("decision_packet", "resume_condition", "resume_evidence_ref"):
        if re.search(rf"(?m)^{re.escape(key)}:", text):
            text = replace_line(text, key, "none")
    if re.search(r"(?m)^current_stage:", text):
        text = replace_line(text, "current_stage", successor["stage_instance_id"])
    receipt_ref = rel(RECEIPT)
    if source_row["Gate"] == "G0":
        text = replace_line(text, "incoming_transition_receipt", receipt_ref)
        text = replace_line(text, "incoming_transition_receipt_sha256", receipt_hash or "pending")
        text = replace_line(text, "rendered_review_target", "none_inherited_visual_baseline")
        text = replace_line(text, "owner_review_target", "none_inherited_visual_baseline")
        text = re.sub(
            r"(?s)# Task\n\n.*\Z",
            "# Task\n\nExecute only `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5` after bounded ledger context and an atomic claim. Rebind the accepted blueprint semantics and current surface contract to the inherited hash-pinned visual baseline, verify exact source coverage and adjacent G1 readiness, then durably update the sole stage ledger. Preserve all accepted visual bytes, historical evidence, and foreign changes. This semantic rebind creates no new visual-authority decision and must not claim G1.\n",
            text,
        )
    else:
        text = replace_line(text, "incoming_transition_receipt", "none")
        text = replace_line(text, "incoming_transition_receipt_sha256", "none")
    text = re.sub(
        r"(?m)^  task_entrypoints:\s*.*$",
        f"  task_entrypoints: [{receipt_ref}]",
        text,
    )
    authority = json.loads(PROMOTION.read_text(encoding="utf-8"))["visual_authority"]
    if source_row["Gate"] in {"G0", "G3", "G4"}:
        for field in (
            "source_visual_ref", "source_visual_sha256", "source_evidence_mode",
            "owner_decision_ref", "screen_acceptance_scope", "visual_language_scope",
            "reusable_foundation_scope", "inheritance_policy", "mobile_scope",
        ):
            value = authority[field]
            if re.search(rf"(?m)^{re.escape(field)}:", text):
                text = replace_line(text, field, value)
            elif source_row["Gate"] != "G0":
                text = text.replace("plan_doc:", f"{field}: {value}\nplan_doc:", 1)
    if source_row["Stage instance"] == "G4@family.auth.shell-auth.baseline-exception-auth-r5":
        text = re.sub(
            r"(?m)^  durable_report:\s*.*$",
            "  durable_report: .codex/delivery/evidence/custometry-ui-design-program-v2/family.auth.shell-auth.baseline-exception-auth-r6-report.md",
            text,
        )
        text = re.sub(
            r"(?s)# Task\n\n.*\Z",
            "# Task\n\nExecute only `G4@family.auth.shell-auth.baseline-exception-auth-r6` after bounded ledger context and an atomic claim. Rebuild the auth family under the current r5 program semantics using accepted r5 artifacts as read-only historical inputs, produce only unique r6 contracts, renders, receipts, decision packet, report, and transition, then stop at the finished-visual owner checkpoint. Preserve foreign changes and never overwrite or revive accepted r5 evidence.\n",
            text,
        )
    path = ROOT / successor["prompt_ref"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def render_ledger(frontmatter: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]]) -> str:
    lines = ["---", *(f"{key}: {value}" for key, value in frontmatter.items()), "---", "", "# Custometry UI Design Program V2 Stage Ledger", ""]
    lines.extend(["| " + " | ".join(COLUMNS) + " |", "|" + "---|" * len(COLUMNS)])
    lines.extend("| " + " | ".join(row[column] for column in COLUMNS) + " |" for row in rows)
    lines.extend(["", "## Stage details", ""])
    for row in rows:
        stage_id = row["Stage instance"]
        lines.extend([f"### `{stage_id}`", ""])
        lines.extend(f"- {key}: `{value}`" for key, value in details[stage_id].items())
        lines.append("")
    lines.extend(["## Current owner input", "", "- Decision packet: `none`", "", "## Current blockers", "", "- none", ""])
    return "\n".join(lines)


def replace_strings(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, str):
        for old, new in replacements.items():
            value = value.replace(old, new)
        return value
    if isinstance(value, list):
        return [replace_strings(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key: replace_strings(item, replacements) for key, item in value.items()}
    return value


def build_successor_inputs() -> None:
    source_dir = DIR / "artifacts/g0-r4"
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    inventory = ARTIFACTS / "ui-standard-source-inventory.json"
    shutil.copyfile(source_dir / "ui-standard-source-inventory.json", inventory)

    baseline = json.loads((source_dir / "platform-ui-baseline.json").read_text(encoding="utf-8"))
    baseline = replace_strings(baseline, {
        **SOURCE_HASH_REPLACEMENTS,
        "custometry.platform-baseline.v3.metadata.r4": "custometry.platform-baseline.v3.metadata.r5",
        "custometry.pilot-standard.v3.metadata.r4": "custometry.pilot-standard.v3.metadata.r5",
        "artifacts/g0-r4/ui-standard-source-inventory.json": "artifacts/g0-r5/ui-standard-source-inventory.json",
    })
    baseline["revision"] = 5
    baseline["standard_contract"]["source_inventory"]["sha256"] = sha(inventory)
    baseline_path = ARTIFACTS / "platform-ui-baseline.json"
    write_json(baseline_path, baseline)

    intake = json.loads((source_dir / "ui-program-intake.json").read_text(encoding="utf-8"))
    intake = replace_strings(intake, {
        **SOURCE_HASH_REPLACEMENTS,
        "CUSTOMETRY-UI-DESIGN-PROGRAM-V2.intake.v4": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2.intake.v5",
        "artifacts/g0-r4/platform-ui-baseline.json": "artifacts/g0-r5/platform-ui-baseline.json",
        "custometry.platform-baseline.v3.metadata.r4": "custometry.platform-baseline.v3.metadata.r5",
    })
    intake["revision"] = 5
    intake["baseline_contract"]["sha256"] = sha(baseline_path)
    for screen in intake["screens"]:
        if screen["screen_id"] != "UI-OVR-005":
            continue
        screen["purpose"] = "Period and comparison editor"
        screen["user_outcomes"] = ["Set shared or block-local grain, current period, and comparison"]
        for region in screen["regions"]:
            region["purpose"] = "Period and comparison editor"
    intake_path = ARTIFACTS / "ui-program-intake.json"
    write_json(intake_path, intake)

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    replacements = {
        **SOURCE_HASH_REPLACEMENTS,
        ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r4/ui-program-intake.json": rel(intake_path),
        ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r4/platform-ui-baseline.json": rel(baseline_path),
        "custometry.platform-baseline.v3.metadata.r4": "custometry.platform-baseline.v3.metadata.r5",
        "cb358d4aac4b53a15bfb3bd6e3b1833ccda78a2e788db558eea837009d590ebe": sha(intake_path),
        "4a32b55fb28e4d07e271a0a37270cfb47255d55650746573c52584e6651e6642": sha(baseline_path),
    }
    plan = replace_strings(plan, replacements)
    plan.update({"revision": 5, "status": "draft", "validation_profile": "draft"})
    plan["input_contracts"] = {
        "intake": {"path": rel(intake_path), "sha256": sha(intake_path)},
        "baseline": {"path": rel(baseline_path), "sha256": sha(baseline_path)},
    }
    write_json(PROMOTION, plan)


def source_and_topology() -> tuple[dict[str, Any], dict[str, Any]]:
    parsed, errors = parse_ledger(LEDGER)
    if errors:
        raise ValueError("source ledger is not parseable: " + "; ".join(errors))
    full_errors = validate_ledger(parsed, LEDGER, ROOT)
    if not full_errors:
        raise ValueError("source ledger unexpectedly passes; semantic migration is not authorized")
    current = [
        row for row in parsed["rows"]
        if parsed["details"][row["Stage instance"]].get("current_authority") != "false"
    ]
    affected = [row for row in current if row["Gate"] in {f"G{i}" for i in range(7)}]
    mapping = {row["Stage instance"]: successor_id(row) for row in affected}
    successor_rows: list[dict[str, Any]] = []
    for row in affected:
        dependencies = [] if row["Dependencies"] in {"—", "-", "none"} else [item.strip() for item in row["Dependencies"].split(",")]
        successor_rows.append({
            "stage_instance_id": mapping[row["Stage instance"]],
            "gate": row["Gate"],
            "target_id": successor_target(row),
            "prompt_ref": successor_prompt(row),
            "status": "pending",
            "dependencies": [mapping.get(item, item) for item in dependencies],
            "execution_allowed": row["Gate"] == "G0",
            "supersedes_stage": row["Stage instance"],
        })
    topology = {
        "$schema": "historical-control-plane-successor-topology.schema.json",
        "schema_id": "codex.ui-historical-control-plane-successor-topology/v1",
        "program_id": PROGRAM_ID,
        "source_ledger_sha256": sha(LEDGER),
        "target_registry_sha256": sha(SKILL / "assets/contract-versions.json"),
        "ledger_status": "active",
        "current_stage": G0_SUCCESSOR,
        "successor_rows": successor_rows,
    }
    return parsed, {"topology": topology, "validation_errors": full_errors}


def prepare_inputs() -> None:
    build_successor_inputs()
    parsed, generated = source_and_topology()
    topology = generated["topology"]
    write_json(TOPOLOGY, topology)
    for item in topology["successor_rows"]:
        source_row = next(row for row in parsed["rows"] if row["Stage instance"] == item["supersedes_stage"])
        evidence, transition = successor_paths(source_row, item["target_id"])
        detail = dict(parsed["details"][source_row["Stage instance"]])
        detail.update({
            "title": f"Blueprint semantic rebind successor {item['gate']}: {item['target_id']}",
            "report_path": evidence,
            "transition_receipt": transition,
            "execution_allowed": str(item["execution_allowed"]).lower(),
        })
        build_prompt(source_row, item, detail, None)
    request = {
        "$schema": "historical-control-plane-migration-request.schema.json",
        "migration_class": "active_semantic_compatibility",
        "program_id": PROGRAM_ID,
        "change_id": "custometry-blueprint-product-semantics-rebind-r5",
        "change_kind": "product_semantics_scope_or_mobile",
        "owner_input": "Да, текущие изменения blueprint актуальны. Перепривяжи UI program через необходимый change-impact маршрут и веди стадии последовательно, останавливаясь на каждом визуальном checkpoint",
        "anchor_stage_instance_id": ANCHOR,
        "source": {
            "ledger_ref": rel(LEDGER), "ledger_sha256": sha(LEDGER),
            "plan_doc_ref": rel(PLAN), "plan_doc_sha256": sha(PLAN),
            "prompt_pack_dir": ".codex/agents/generated/custometry-ui-design-g0-v2",
            "contract_registry_ref": rel(LOCAL_REGISTRY),
            "contract_registry_sha256": sha(LOCAL_REGISTRY),
        },
        "target_registry": {"path": str(SKILL / "assets/contract-versions.json"), "sha256": sha(SKILL / "assets/contract-versions.json")},
        "successor_topology_ref": rel(TOPOLOGY), "successor_topology_sha256": sha(TOPOLOGY),
        "source_validation_errors_sha256": canonical_sha256(generated["validation_errors"]),
        "successor_plan_doc_ref": rel(PROMOTION), "successor_plan_doc_sha256": sha(PROMOTION),
        "successor_plan_target_ref": rel(PLAN),
    }
    write_json(REQUEST, request)
    print(json.dumps({"status": "prepared_inputs", "affected_rows": len(topology["successor_rows"]), "errors": len(generated["validation_errors"]), "plan": sha(PROMOTION)}))


def build_candidate() -> None:
    if not RECEIPT.is_file():
        raise ValueError("canonical migration receipt is missing")
    parsed, errors = parse_ledger(LEDGER)
    if errors:
        raise ValueError("source ledger is not parseable: " + "; ".join(errors))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    topology = json.loads(TOPOLOGY.read_text(encoding="utf-8"))
    receipt_ref, receipt_hash = rel(RECEIPT), sha(RECEIPT)
    impact_ref = receipt["change_impact"]["path"]
    by_source = {item["supersedes_stage"]: item for item in topology["successor_rows"]}
    rows = [dict(row) for row in parsed["rows"]]
    details = {key: dict(value) for key, value in parsed["details"].items()}
    for row in rows:
        stage_id = row["Stage instance"]
        if stage_id not in by_source:
            continue
        source_status = row["Status"]
        row["Status"] = "superseded"
        details[stage_id].update({
            "historical_outcome": source_status,
            "current_authority": "false",
            "execution_allowed": "false",
            "invalidated_by_ref": impact_ref,
            "superseded_by_stage": by_source[stage_id]["stage_instance_id"],
            "historical_migration_ref": receipt_ref,
            "historical_migration_sha256": receipt_hash,
        })
    indexed = {row["Stage instance"]: row for row in parsed["rows"]}
    for item in topology["successor_rows"]:
        source_row = indexed[item["supersedes_stage"]]
        evidence, transition = successor_paths(source_row, item["target_id"])
        incoming_ref = receipt_ref if item["gate"] == "G0" else "none"
        incoming_hash = receipt_hash if item["gate"] == "G0" else "none"
        row = {
            "Stage instance": item["stage_instance_id"], "Gate": item["gate"],
            "Target ID": item["target_id"], "Prompt": item["prompt_ref"], "Status": "pending",
            "Dependencies": "—" if not item["dependencies"] else ", ".join(item["dependencies"]),
            "Evidence": evidence, "Transition receipt": transition,
            "Owner decision": source_row["Owner decision"], "Executor claim": "—", "Claimed at": "—",
        }
        detail = dict(parsed["details"][source_row["Stage instance"]])
        detail.update({
            "title": f"Blueprint semantic rebind successor {item['gate']}: {item['target_id']}",
            "report_path": evidence,
            "decision_packet": "none", "resume_condition": "none",
            "resume_evidence_ref": "none", "resume_evidence_sha256": "none",
            "transition_receipt": transition, "transition_receipt_sha256": "none",
            "execution_allowed": str(item["execution_allowed"]).lower(),
            "replaces_stage": "none", "repair_evidence_ref": "none",
            "historical_outcome": "none", "current_authority": "true",
            "invalidated_by_ref": "none", "superseded_by_stage": "none",
            "supersedes_stage": source_row["Stage instance"],
            "incoming_transition_receipt": incoming_ref,
            "incoming_transition_receipt_sha256": incoming_hash,
        })
        detail.pop("historical_migration_ref", None)
        detail.pop("historical_migration_sha256", None)
        build_prompt(source_row, item, detail, receipt_hash)
        rows.append(row)
        details[item["stage_instance_id"]] = detail
    frontmatter = dict(parsed["frontmatter"])
    frontmatter.update({"ledger_status": "active", "current_stage": G0_SUCCESSOR, "Next stage allowed": "false"})
    CANDIDATE.write_text(render_ledger(frontmatter, rows, details), encoding="utf-8")
    print(json.dumps({"status": "candidate_built", "sha256": sha(CANDIDATE)}))


def promote() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if sha(PROMOTION) != receipt["successor_plan_doc"]["sha256"]:
        raise ValueError("prepared successor plan candidate changed")
    lock = PLAN.with_name(f".{PLAN.name}.write.lock")
    with lock.open("a+b") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            if sha(PLAN) != receipt["source"]["plan_doc_sha256"]:
                raise ValueError("live plan changed before semantic migration promotion")
            with tempfile.NamedTemporaryFile(dir=PLAN.parent, prefix=f".{PLAN.name}.promotion.", delete=False) as temp:
                temp_path = Path(temp.name)
                temp.write(PROMOTION.read_bytes())
                temp.flush()
                os.fsync(temp.fileno())
            os.replace(temp_path, PLAN)
            directory_fd = os.open(PLAN.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    print(json.dumps({"status": "promoted", "sha256": sha(PLAN)}))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "candidate", "promote"))
    args = parser.parse_args()
    {"prepare": prepare_inputs, "candidate": build_candidate, "promote": promote}[args.mode]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
