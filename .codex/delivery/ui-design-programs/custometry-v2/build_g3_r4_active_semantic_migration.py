#!/usr/bin/env python3
"""Build and apply the revisioned G3 applicability-compatibility control plane."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
LEDGER = DIR / "stage-ledger.md"
PLAN = DIR / "ui-design-program.json"
LOCAL_REGISTRY = DIR / "contract-versions.json"
PROMOTION = DIR / "artifacts/g3-r4/ui-design-program.promotion-candidate.json"
MIGRATION = DIR / "evidence/g3-r4/active-semantic-migration"
PREPARED = MIGRATION / "prepared"
TOPOLOGY = MIGRATION / "successor-topology.json"
REQUEST = MIGRATION / "migration-request.json"
CANDIDATE = MIGRATION / "candidate-stage-ledger.md"
RECEIPT = PREPARED / "historical-control-plane-migration-receipt.json"
SKILL = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program")
sys.path.insert(0, str(SKILL / "scripts"))

from validate_stage_ledger import canonical_sha256, parse_ledger, validate_ledger  # noqa: E402


PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"
ANCHOR = "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3"
G3_SUCCESSOR = "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4"
COLUMNS = (
    "Stage instance", "Gate", "Target ID", "Prompt", "Status", "Dependencies",
    "Evidence", "Transition receipt", "Owner decision", "Executor claim", "Claimed at",
)


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
    if row["Stage instance"] == ANCHOR:
        return G3_SUCCESSOR
    return bump(row["Stage instance"])


def successor_target(row: dict[str, str]) -> str:
    if row["Gate"] in {"G3", "G6"}:
        return f"{PROGRAM_ID}-r4"
    return bump(row["Target ID"])


def successor_prompt(row: dict[str, str]) -> str:
    if row["Gate"] == "G3":
        name = "33-g3-foundations-shell-r4.md"
    elif row["Gate"] == "G6":
        name = "63-g6-handoff-r4.md"
    else:
        old = Path(row["Prompt"]).name
        revision = successor_id(row).rsplit("-r", 1)[1]
        name = re.sub(r"-r[0-9]+\.md$", f"-r{revision}.md", old)
    return f".codex/agents/generated/custometry-ui-design-g0-v2/{name}"


def successor_paths(row: dict[str, str], target: str) -> tuple[str, str]:
    evidence = row["Evidence"]
    transition = row["Transition receipt"]
    old_target = row["Target ID"]
    evidence = evidence.replace(old_target, target)
    if row["Gate"] == "G3":
        transition = transition.replace("/g3-r3/", "/g3-r4/")
    else:
        transition = transition.replace(old_target, target)
    return evidence, transition


def replace_line(text: str, key: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^{re.escape(key)}:\s*.*$")
    if len(pattern.findall(text)) != 1:
        raise ValueError(f"prompt requires one {key} line")
    return pattern.sub(f"{key}: {value}", text)


def build_prompt(
    source_row: dict[str, str], successor: dict[str, Any], detail: dict[str, str], receipt_hash: str | None
) -> None:
    text = (ROOT / source_row["Prompt"]).read_text(encoding="utf-8")
    old_id = source_row["Stage instance"]
    text = text.replace(old_id, successor["stage_instance_id"])
    text = replace_line(text, "target_id", successor["target_id"])
    text = replace_line(text, "title", detail["title"])
    text = replace_line(text, "report_path", detail["report_path"])
    text = replace_line(text, "transition_receipt", detail["transition_receipt"])
    text = replace_line(text, "execution_allowed", detail["execution_allowed"])
    if re.search(r"(?m)^current_stage:", text):
        text = replace_line(text, "current_stage", successor["stage_instance_id"])
    migration_ref = rel(RECEIPT)
    if source_row["Gate"] == "G3":
        text = text.replace("/g3-r3/", "/g3-r4/")
        text = text.replace("g3-r3", "g3-r4")
        text = replace_line(text, "incoming_transition_receipt", migration_ref)
        text = replace_line(text, "incoming_transition_receipt_sha256", receipt_hash or "pending")
    else:
        text = replace_line(text, "incoming_transition_receipt", "none")
        text = replace_line(text, "incoming_transition_receipt_sha256", "none")
    if source_row["Gate"] in {"G3", "G4"}:
        authority = json.loads(PLAN.read_text(encoding="utf-8"))["visual_authority"]
        if re.search(r"(?m)^owner_review_target:", text):
            text = replace_line(text, "owner_review_target", "finished_visuals_only")
        for field in (
            "source_visual_ref", "source_visual_sha256", "source_evidence_mode",
            "owner_decision_ref", "screen_acceptance_scope", "visual_language_scope",
            "reusable_foundation_scope", "inheritance_policy", "mobile_scope",
        ):
            value = authority[field]
            if re.search(rf"(?m)^{re.escape(field)}:", text):
                text = replace_line(text, field, value)
            else:
                text = text.replace("plan_doc:", f"{field}: {value}\nplan_doc:", 1)
    text = text.replace(
        ".codex/delivery/ui-design-programs/custometry-v2/evidence/compatibility-migration-r3/prepared/historical-control-plane-migration-receipt.json",
        migration_ref,
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
    affected = [row for row in current if row["Gate"] in {"G3", "G4", "G5", "G6"}]
    mapping = {row["Stage instance"]: successor_id(row) for row in affected}
    successor_rows: list[dict[str, Any]] = []
    for row in affected:
        deps = [] if row["Dependencies"] in {"—", "-", "none"} else [item.strip() for item in row["Dependencies"].split(",")]
        successor_rows.append({
            "stage_instance_id": mapping[row["Stage instance"]],
            "gate": row["Gate"],
            "target_id": successor_target(row),
            "prompt_ref": successor_prompt(row),
            "status": "pending",
            "dependencies": [mapping.get(item, item) for item in deps],
            "execution_allowed": row["Gate"] == "G3",
            "supersedes_stage": row["Stage instance"],
        })
    topology = {
        "$schema": "historical-control-plane-successor-topology.schema.json",
        "schema_id": "codex.ui-historical-control-plane-successor-topology/v1",
        "program_id": PROGRAM_ID,
        "source_ledger_sha256": sha(LEDGER),
        "target_registry_sha256": sha(SKILL / "assets/contract-versions.json"),
        "ledger_status": "active",
        "current_stage": G3_SUCCESSOR,
        "successor_rows": successor_rows,
    }
    return parsed, {"topology": topology, "validation_errors": full_errors}


def prepare_inputs() -> None:
    parsed, generated = source_and_topology()
    topology = generated["topology"]
    write_json(TOPOLOGY, topology)
    by_source = {item["supersedes_stage"]: item for item in topology["successor_rows"]}
    for source_id, item in by_source.items():
        source_row = next(row for row in parsed["rows"] if row["Stage instance"] == source_id)
        target = item["target_id"]
        evidence, transition = successor_paths(source_row, target)
        detail = dict(parsed["details"][source_id])
        detail.update({
            "title": f"Active semantic compatibility successor {source_row['Gate']}: {target}",
            "report_path": evidence,
            "transition_receipt": transition,
            "transition_receipt_sha256": "none",
            "decision_packet": "none",
            "resume_condition": "none",
            "resume_evidence_ref": "none",
            "resume_evidence_sha256": "none",
            "execution_allowed": str(item["execution_allowed"]).lower(),
            "replaces_stage": "none",
            "repair_evidence_ref": "none",
            "historical_outcome": "none",
            "current_authority": "true",
            "invalidated_by_ref": "none",
            "superseded_by_stage": "none",
            "supersedes_stage": source_id,
            "incoming_transition_receipt": rel(RECEIPT) if source_row["Gate"] == "G3" else "none",
            "incoming_transition_receipt_sha256": "pending" if source_row["Gate"] == "G3" else "none",
        })
        build_prompt(source_row, item, detail, None)
    request = {
        "$schema": "historical-control-plane-migration-request.schema.json",
        "migration_class": "active_semantic_compatibility",
        "program_id": PROGRAM_ID,
        "change_id": "custometry-g3-exact-standard-applicability-r4",
        "change_kind": "g3_realization_inside_accepted_baseline",
        "owner_input": "ок, G3 r4 принимается",
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
    print(json.dumps({"status": "prepared_inputs", "affected_rows": len(topology["successor_rows"]), "errors": len(generated["validation_errors"])}))


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
        target = item["target_id"]
        evidence, transition = successor_paths(source_row, target)
        incoming_ref = receipt_ref if item["gate"] == "G3" else "none"
        incoming_hash = receipt_hash if item["gate"] == "G3" else "none"
        row = {
            "Stage instance": item["stage_instance_id"], "Gate": item["gate"],
            "Target ID": target, "Prompt": item["prompt_ref"], "Status": "pending",
            "Dependencies": "—" if not item["dependencies"] else ", ".join(item["dependencies"]),
            "Evidence": evidence, "Transition receipt": transition,
            "Owner decision": "required", "Executor claim": "—", "Claimed at": "—",
        }
        source_detail = parsed["details"][source_row["Stage instance"]]
        detail = dict(source_detail)
        detail.update({
            "title": f"Active semantic compatibility successor {item['gate']}: {target}",
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
    frontmatter.update({"ledger_status": "active", "current_stage": G3_SUCCESSOR, "Next stage allowed": "false"})
    CANDIDATE.write_text(render_ledger(frontmatter, rows, details), encoding="utf-8")
    print(json.dumps({"status": "candidate_built", "sha256": sha(CANDIDATE)}))


def promote() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    expected_source = receipt["source"]["plan_doc_sha256"]
    expected_successor = receipt["successor_plan_doc"]["sha256"]
    if sha(PROMOTION) != expected_successor:
        raise ValueError("prepared successor plan candidate changed")
    lock = PLAN.with_name(f".{PLAN.name}.write.lock")
    with lock.open("a+b") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            if sha(PLAN) != expected_source:
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
            if sha(PLAN) != expected_successor:
                raise ValueError("promoted successor plan hash mismatch")
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
