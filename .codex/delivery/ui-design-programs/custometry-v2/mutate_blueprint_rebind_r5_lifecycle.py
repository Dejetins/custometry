#!/usr/bin/env python3
"""Build deterministic CAS candidates for the blueprint-rebind r5 G0-G3 lifecycle."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
LEDGER = DIR / "stage-ledger.md"
sys.path.insert(0, str(DIR))
from build_blueprint_rebind_r5 import render_ledger  # noqa: E402

sys.path.insert(0, "/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")
from validate_stage_ledger import parse_ledger  # noqa: E402


STAGES = {
    "g0": "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5",
    "g1": "G1@atlas-r4",
    "g2": "G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4",
    "g3": "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5",
    "g4": "G4@family.auth.shell-auth.baseline-exception-auth-r6",
    "g4w": "G4@family.auth.shell-workspace.baseline-r5",
    "g4c": "G4@family.core.shell-workspace.baseline-r5",
    "g4dq": "G4@family.dq.shell-workspace.baseline-r5",
    "g4an": "G4@family.an.shell-workspace.baseline-r5",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load() -> tuple[dict[str, str], list[dict[str, str]], dict[str, dict[str, str]]]:
    parsed, errors = parse_ledger(LEDGER)
    if errors:
        raise ValueError("ledger parse failed: " + "; ".join(errors))
    return dict(parsed["frontmatter"]), [dict(row) for row in parsed["rows"]], {
        key: dict(value) for key, value in parsed["details"].items()
    }


def row(rows: list[dict[str, str]], stage_id: str) -> dict[str, str]:
    matches = [item for item in rows if item["Stage instance"] == stage_id]
    if len(matches) != 1:
        raise ValueError(f"stage row is not unique: {stage_id}")
    return matches[0]


def claim(front: dict[str, str], rows: list[dict[str, str]], stage_id: str, label: str) -> None:
    target = row(rows, stage_id)
    if front.get("ledger_status") != "active" or front.get("current_stage") != stage_id or target["Status"] != "pending":
        raise ValueError("claim source state is not the exact pending active frontier")
    now = datetime.now(timezone.utc).replace(microsecond=0)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    target["Status"] = "in_progress"
    target["Executor claim"] = f"codex-root-{label}-{stamp}"
    target["Claimed at"] = now.isoformat().replace("+00:00", "Z")


def accept(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
    stage_id: str, next_stage_id: str, *, prepared: bool = False,
) -> None:
    target = row(rows, stage_id)
    next_row = row(rows, next_stage_id)
    transition = ROOT / target["Transition receipt"]
    if target["Status"] != "in_progress" or next_row["Status"] != "pending" or (not prepared and not transition.is_file()):
        raise ValueError("acceptance source state or transition receipt is invalid")
    transition_hash = "none" if prepared else sha(transition)
    target["Status"] = "accepted"
    details[stage_id].update({
        "transition_receipt": ref(transition),
        "transition_receipt_sha256": transition_hash,
        "execution_allowed": "false",
    })
    details[next_stage_id].update({
        "execution_allowed": "true",
        "incoming_transition_receipt": ref(transition),
        "incoming_transition_receipt_sha256": transition_hash,
    })
    front.update({"ledger_status": "active", "current_stage": next_stage_id, "Next stage allowed": "false"})


def g3_review_ready(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g3"]
    target = row(rows, stage_id)
    evidence_dir = DIR / "evidence/g3-r5"
    packet = evidence_dir / "owner-review-decision-packet.json"
    transition = evidence_dir / "stage-transition-review-ready.json"
    board = DIR / "artifacts/g3-r5/review-board.html"
    for path in (packet, transition, board):
        if not path.is_file():
            raise ValueError(f"G3 review-ready artifact is missing: {path}")
    target.update({"Status": "needs_input", "Evidence": ref(board), "Transition receipt": ref(transition)})
    details[stage_id].update({
        "decision_packet": ref(packet),
        "resume_condition": "owner_accepts_or_requests_bounded_corrections_for_exact_finished_g3_r5_board",
        "resume_evidence_ref": "none",
        "resume_evidence_sha256": "none",
        "transition_receipt": ref(transition),
        "transition_receipt_sha256": sha(transition),
    })
    front.update({"ledger_status": "awaiting_input", "current_stage": stage_id, "Next stage allowed": "false"})


def g3_resume(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g3"]
    target = row(rows, stage_id)
    response = DIR / "evidence/g3-r5/owner-input-response-acceptance-r5.json"
    if (
        front.get("ledger_status") != "awaiting_input"
        or front.get("current_stage") != stage_id
        or target["Status"] != "needs_input"
        or not response.is_file()
    ):
        raise ValueError("G3 resume requires the exact accepted awaiting-input frontier")
    target["Status"] = "in_progress"
    details[stage_id].update({
        "resume_evidence_ref": ref(response),
        "resume_evidence_sha256": sha(response),
    })
    front.update({"ledger_status": "active", "current_stage": stage_id, "Next stage allowed": "false"})


def g3_accept(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g3"]
    next_stage_id = STAGES["g4"]
    target = row(rows, stage_id)
    next_row = row(rows, next_stage_id)
    evidence_dir = DIR / "evidence/g3-r5"
    decision = evidence_dir / "stage-acceptance-decision-r5.json"
    transition = evidence_dir / "stage-transition.json"
    if (
        front.get("ledger_status") != "active"
        or front.get("current_stage") != stage_id
        or target["Status"] != "in_progress"
        or next_row["Status"] != "pending"
        or not decision.is_file()
        or not transition.is_file()
    ):
        raise ValueError("G3 acceptance source state or exact evidence is invalid")
    target.update({
        "Status": "accepted",
        "Owner decision": ref(decision),
        "Transition receipt": ref(transition),
    })
    transition_hash = sha(transition)
    details[stage_id].update({
        "transition_receipt": ref(transition),
        "transition_receipt_sha256": transition_hash,
        "execution_allowed": "false",
    })
    details[next_stage_id].update({
        "execution_allowed": "true",
        "incoming_transition_receipt": ref(transition),
        "incoming_transition_receipt_sha256": transition_hash,
    })
    front.update({"ledger_status": "active", "current_stage": next_stage_id, "Next stage allowed": "false"})


def g4_review_ready(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]], *, prepared: bool,
) -> None:
    stage_id = STAGES["g4"]
    target = row(rows, stage_id)
    evidence_dir = DIR / "evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth"
    artifact_dir = DIR / "artifacts/g4-r6/family-auth-shell-auth-baseline-exception-auth"
    packet = evidence_dir / "owner-review-decision-packet.json"
    transition = evidence_dir / "stage-transition-review-ready.json"
    board = artifact_dir / "review-board.html"
    family = evidence_dir / "family-acceptance.json"
    required = (packet, board, family) if prepared else (packet, transition, board, family)
    valid_frontier = (
        (front.get("ledger_status") == "active" and target["Status"] == "in_progress")
        if prepared
        else (
            (front.get("ledger_status") == "active" and target["Status"] == "in_progress")
            or (front.get("ledger_status") == "awaiting_input" and target["Status"] == "needs_input")
        )
    )
    if front.get("current_stage") != stage_id or not valid_frontier:
        raise ValueError("G4 review-ready requires the exact claimed current row")
    for path in required:
        if not path.is_file():
            raise ValueError(f"G4 review-ready artifact is missing: {path}")
    transition_hash = "none" if prepared else sha(transition)
    target.update({
        "Status": "needs_input",
        "Evidence": ref(board),
        "Transition receipt": ref(transition),
        "Owner decision": "required",
    })
    details[stage_id].update({
        "decision_packet": ref(packet),
        "resume_condition": "owner_accepts_or_requests_bounded_corrections_for_exact_finished_g4_auth_r6_board",
        "resume_evidence_ref": "none",
        "resume_evidence_sha256": "none",
        "transition_receipt": ref(transition),
        "transition_receipt_sha256": transition_hash,
    })
    front.update({"ledger_status": "awaiting_input", "current_stage": stage_id, "Next stage allowed": "false"})


def g4w_review_ready(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]], *, prepared: bool,
) -> None:
    stage_id = STAGES["g4w"]
    target = row(rows, stage_id)
    evidence_dir = DIR / "evidence/family.auth.shell-workspace.baseline-r5"
    packet = evidence_dir / "owner-review-decision-packet.json"
    transition = evidence_dir / "stage-transition-review-ready.json"
    board = DIR / "artifacts/g4-r5/family-auth-shell-workspace-baseline/review-board.html"
    family = evidence_dir / "family-acceptance.json"
    required = (packet, board, family) if prepared else (packet, transition, board, family)
    valid_frontier = (
        front.get("ledger_status") == "active" and target["Status"] == "in_progress"
    ) if prepared else (
        (front.get("ledger_status") == "active" and target["Status"] == "in_progress")
        or (front.get("ledger_status") == "awaiting_input" and target["Status"] == "needs_input")
    )
    if front.get("current_stage") != stage_id or not valid_frontier:
        raise ValueError("G4 workspace review-ready requires the exact claimed current row")
    for path in required:
        if not path.is_file():
            raise ValueError(f"G4 workspace review-ready artifact is missing: {path}")
    target.update({"Status":"needs_input","Evidence":ref(board),"Transition receipt":ref(transition),"Owner decision":"required"})
    details[stage_id].update({
        "decision_packet":ref(packet),
        "resume_condition":"owner_accepts_or_requests_bounded_corrections_for_exact_finished_g4_workspace_r5_board",
        "resume_evidence_ref":"none","resume_evidence_sha256":"none",
        "transition_receipt":ref(transition),
        "transition_receipt_sha256":"none" if prepared else sha(transition),
    })
    front.update({"ledger_status":"awaiting_input","current_stage":stage_id,"Next stage allowed":"false"})


def g4_resume(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g4"]
    target = row(rows, stage_id)
    response = DIR / "evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth/owner-input-response-acceptance-r6.json"
    if (
        front.get("ledger_status") != "awaiting_input"
        or front.get("current_stage") != stage_id
        or target["Status"] != "needs_input"
        or not response.is_file()
    ):
        raise ValueError("G4 resume requires the exact accepted awaiting-input frontier")
    target["Status"] = "in_progress"
    details[stage_id].update({
        "resume_evidence_ref": ref(response),
        "resume_evidence_sha256": sha(response),
    })
    front.update({"ledger_status": "active", "current_stage": stage_id, "Next stage allowed": "false"})


def g4w_resume(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id=STAGES["g4w"]; target=row(rows,stage_id)
    response=DIR/"evidence/family.auth.shell-workspace.baseline-r5/owner-input-response-acceptance-r5.json"
    if front.get("ledger_status")!="awaiting_input" or front.get("current_stage")!=stage_id or target["Status"]!="needs_input" or not response.is_file():
        raise ValueError("G4 workspace resume requires the exact accepted awaiting-input frontier")
    target["Status"]="in_progress"
    details[stage_id].update({"resume_evidence_ref":ref(response),"resume_evidence_sha256":sha(response)})
    front.update({"ledger_status":"active","current_stage":stage_id,"Next stage allowed":"false"})


def g4c_resume(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g4c"]
    target = row(rows, stage_id)
    evidence_dir = DIR / "evidence/family.core.shell-workspace.baseline-r5"
    response = evidence_dir / "owner-input-response-requested-changes-kpi-pilot-row-r5.json"
    decision = evidence_dir / "family-review-requested-changes-kpi-pilot-row-r5.json"
    if (
        front.get("ledger_status") != "awaiting_input"
        or front.get("current_stage") != stage_id
        or target["Status"] != "needs_input"
        or not response.is_file()
        or not decision.is_file()
    ):
        raise ValueError("G4 core correction resume requires the exact awaiting-input frontier")
    target.update({"Status": "in_progress", "Owner decision": ref(decision)})
    details[stage_id].update({
        "resume_evidence_ref": ref(response),
        "resume_evidence_sha256": sha(response),
    })
    front.update({"ledger_status": "active", "current_stage": stage_id, "Next stage allowed": "false"})


def g4c_acceptance_resume(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g4c"]
    target = row(rows, stage_id)
    evidence_dir = DIR / "evidence/family.core.shell-workspace.baseline-r5"
    response = evidence_dir / "owner-input-response-acceptance-r5.json"
    decision = evidence_dir / "family-acceptance-decision-r5.json"
    if (
        front.get("ledger_status") != "awaiting_input"
        or front.get("current_stage") != stage_id
        or target["Status"] != "needs_input"
        or not response.is_file()
        or not decision.is_file()
    ):
        raise ValueError("G4 core acceptance resume requires the exact accepted awaiting-input frontier")
    target.update({"Status": "in_progress", "Owner decision": ref(decision)})
    details[stage_id].update({
        "resume_evidence_ref": ref(response),
        "resume_evidence_sha256": sha(response),
    })
    front.update({"ledger_status": "active", "current_stage": stage_id, "Next stage allowed": "false"})


def g4c_review_ready(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]], *, prepared: bool,
) -> None:
    stage_id = STAGES["g4c"]
    target = row(rows, stage_id)
    evidence_dir = DIR / "evidence/family.core.shell-workspace.baseline-r5"
    transition = evidence_dir / "stage-transition-review-ready.json"
    board = DIR / "artifacts/g4-r5/family-core-shell-workspace-baseline/review-board.html"
    packet = evidence_dir / "owner-review-decision-packet.md"
    family = evidence_dir / "family-acceptance.json"
    required = (packet, board, family) if prepared else (packet, transition, board, family)
    valid_frontier = (
        front.get("ledger_status") == "active" and target["Status"] == "in_progress"
    ) if prepared else (
        (front.get("ledger_status") == "active" and target["Status"] == "in_progress")
        or (front.get("ledger_status") == "awaiting_input" and target["Status"] == "needs_input")
    )
    if front.get("current_stage") != stage_id or not valid_frontier:
        raise ValueError("G4 core review-ready requires the exact current row")
    for path in required:
        if not path.is_file():
            raise ValueError(f"G4 core review-ready artifact is missing: {path}")
    target.update({
        "Status": "needs_input",
        "Evidence": ref(board),
        "Transition receipt": ref(transition),
        "Owner decision": "required",
    })
    details[stage_id].update({
        "decision_packet": ref(packet),
        "resume_condition": "owner_accepts_or_requests_bounded_corrections_for_exact_finished_g4_core_r5_board",
        "resume_evidence_ref": "none",
        "resume_evidence_sha256": "none",
        "transition_receipt": ref(transition),
        "transition_receipt_sha256": "none" if prepared else sha(transition),
    })
    front.update({"ledger_status": "awaiting_input", "current_stage": stage_id, "Next stage allowed": "false"})


def g4w_ready_provisional(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]], *, prepared: bool,
) -> None:
    stage_id=STAGES["g4w"]; next_stage_id="G4@family.core.shell-workspace.baseline-r5"
    target=row(rows,stage_id); next_row=row(rows,next_stage_id)
    transition=DIR/"evidence/family.auth.shell-workspace.baseline-r5/stage-transition.json"
    if front.get("ledger_status")!="active" or front.get("current_stage")!=stage_id or target["Status"]!="in_progress" or next_row["Status"]!="pending":
        raise ValueError("G4 workspace ready provisional requires the resumed current row and pending successor")
    if not prepared and not transition.is_file():
        raise ValueError("G4 workspace ready provisional requires a readable transition receipt")
    transition_hash="none" if prepared else sha(transition)
    target["Transition receipt"]=ref(transition)
    details[stage_id].update({"transition_receipt":ref(transition),"transition_receipt_sha256":transition_hash})
    dependencies=[item.strip() for item in next_row["Dependencies"].split(",") if item.strip()]
    if stage_id not in dependencies: dependencies.append(stage_id)
    next_row["Dependencies"]=", ".join(dependencies)
    details[next_stage_id].update({"execution_allowed":"true","incoming_transition_receipt":ref(transition),"incoming_transition_receipt_sha256":transition_hash})


def g4w_accept(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id=STAGES["g4w"]; next_stage_id="G4@family.core.shell-workspace.baseline-r5"
    target=row(rows,stage_id); next_row=row(rows,next_stage_id)
    evidence_dir=DIR/"evidence/family.auth.shell-workspace.baseline-r5"
    decision=evidence_dir/"family-acceptance-decision-r5.json"; transition=evidence_dir/"stage-transition.json"
    if front.get("ledger_status")!="active" or front.get("current_stage")!=stage_id or target["Status"]!="in_progress" or next_row["Status"]!="pending" or not decision.is_file() or not transition.is_file():
        raise ValueError("G4 workspace acceptance source state or exact evidence is invalid")
    target.update({"Status":"accepted","Owner decision":ref(decision),"Transition receipt":ref(transition)})
    transition_hash=sha(transition)
    details[stage_id].update({"transition_receipt":ref(transition),"transition_receipt_sha256":transition_hash,"execution_allowed":"false"})
    dependencies=[item.strip() for item in next_row["Dependencies"].split(",") if item.strip()]
    if stage_id not in dependencies: dependencies.append(stage_id)
    next_row["Dependencies"]=", ".join(dependencies)
    details[next_stage_id].update({"execution_allowed":"true","incoming_transition_receipt":ref(transition),"incoming_transition_receipt_sha256":transition_hash})
    front.update({"ledger_status":"active","current_stage":next_stage_id,"Next stage allowed":"false"})


def g4c_ready_provisional(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]], *, prepared: bool,
) -> None:
    stage_id = STAGES["g4c"]
    next_stage_id = "G4@family.data.shell-workspace.baseline-r5"
    target = row(rows, stage_id)
    next_row = row(rows, next_stage_id)
    transition = DIR / "evidence/family.core.shell-workspace.baseline-r5/stage-transition.json"
    if front.get("ledger_status") != "active" or front.get("current_stage") != stage_id or target["Status"] != "in_progress" or next_row["Status"] != "pending":
        raise ValueError("G4 core ready provisional requires the resumed current row and pending successor")
    if not prepared and not transition.is_file():
        raise ValueError("G4 core ready provisional requires a readable transition receipt")
    transition_hash = "none" if prepared else sha(transition)
    target["Transition receipt"] = ref(transition)
    details[stage_id].update({"transition_receipt": ref(transition), "transition_receipt_sha256": transition_hash})
    dependencies = [item.strip() for item in next_row["Dependencies"].split(",") if item.strip()]
    if stage_id not in dependencies:
        dependencies.append(stage_id)
    next_row["Dependencies"] = ", ".join(dependencies)
    if prepared:
        details[next_stage_id]["execution_allowed"] = "true"
    else:
        details[next_stage_id].update({"execution_allowed": "true", "incoming_transition_receipt": ref(transition), "incoming_transition_receipt_sha256": transition_hash})


def g4c_accept(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g4c"]
    next_stage_id = "G4@family.data.shell-workspace.baseline-r5"
    target = row(rows, stage_id)
    next_row = row(rows, next_stage_id)
    evidence_dir = DIR / "evidence/family.core.shell-workspace.baseline-r5"
    decision = evidence_dir / "family-acceptance-decision-r5.json"
    transition = evidence_dir / "stage-transition.json"
    if front.get("ledger_status") != "active" or front.get("current_stage") != stage_id or target["Status"] != "in_progress" or next_row["Status"] != "pending" or not decision.is_file() or not transition.is_file():
        raise ValueError("G4 core acceptance source state or exact evidence is invalid")
    target.update({"Status": "accepted", "Owner decision": ref(decision), "Transition receipt": ref(transition)})
    transition_hash = sha(transition)
    details[stage_id].update({"transition_receipt": ref(transition), "transition_receipt_sha256": transition_hash, "execution_allowed": "false"})
    dependencies = [item.strip() for item in next_row["Dependencies"].split(",") if item.strip()]
    if stage_id not in dependencies:
        dependencies.append(stage_id)
    next_row["Dependencies"] = ", ".join(dependencies)
    details[next_stage_id].update({"execution_allowed": "true", "incoming_transition_receipt": ref(transition), "incoming_transition_receipt_sha256": transition_hash})
    front.update({"ledger_status": "active", "current_stage": next_stage_id, "Next stage allowed": "false"})


def g4dq_resume(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g4dq"]
    target = row(rows, stage_id)
    evidence_dir = DIR / "evidence/family.dq.shell-workspace.baseline-r5"
    response = evidence_dir / "owner-input-response-acceptance-r5.json"
    decision = evidence_dir / "family-acceptance-decision-r5.json"
    if (
        front.get("ledger_status") != "awaiting_input"
        or front.get("current_stage") != stage_id
        or target["Status"] != "needs_input"
        or not response.is_file()
        or not decision.is_file()
    ):
        raise ValueError("G4 data-quality acceptance resume requires the exact accepted awaiting-input frontier")
    target.update({"Status": "in_progress", "Owner decision": ref(decision)})
    details[stage_id].update({
        "resume_evidence_ref": ref(response),
        "resume_evidence_sha256": sha(response),
    })
    front.update({"ledger_status": "active", "current_stage": stage_id, "Next stage allowed": "false"})


def g4dq_ready_provisional(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]], *, prepared: bool,
) -> None:
    stage_id = STAGES["g4dq"]
    next_stage_id = "G4@family.an.shell-workspace.baseline-r5"
    target = row(rows, stage_id)
    next_row = row(rows, next_stage_id)
    evidence_dir = DIR / "evidence/family.dq.shell-workspace.baseline-r5"
    decision = evidence_dir / "family-acceptance-decision-r5.json"
    transition = evidence_dir / "stage-transition.json"
    if (
        front.get("ledger_status") != "active"
        or front.get("current_stage") != stage_id
        or target["Status"] != "in_progress"
        or next_row["Status"] != "pending"
        or not decision.is_file()
        or (not prepared and not transition.is_file())
    ):
        raise ValueError("G4 data-quality ready provisional requires the resumed current row and pending successor")
    transition_hash = "none" if prepared else sha(transition)
    target.update({"Transition receipt": ref(transition), "Owner decision": ref(decision)})
    details[stage_id].update({
        "transition_receipt": ref(transition),
        "transition_receipt_sha256": transition_hash,
    })
    dependencies = [item.strip() for item in next_row["Dependencies"].split(",") if item.strip()]
    if stage_id not in dependencies:
        dependencies.append(stage_id)
    next_row["Dependencies"] = ", ".join(dependencies)
    if prepared:
        details[next_stage_id]["execution_allowed"] = "false"
    else:
        details[next_stage_id].update({
            "execution_allowed": "true",
            "incoming_transition_receipt": ref(transition),
            "incoming_transition_receipt_sha256": transition_hash,
        })


def g4dq_accept(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g4dq"]
    next_stage_id = "G4@family.an.shell-workspace.baseline-r5"
    target = row(rows, stage_id)
    next_row = row(rows, next_stage_id)
    evidence_dir = DIR / "evidence/family.dq.shell-workspace.baseline-r5"
    decision = evidence_dir / "family-acceptance-decision-r5.json"
    transition = evidence_dir / "stage-transition.json"
    if (
        front.get("ledger_status") != "active"
        or front.get("current_stage") != stage_id
        or target["Status"] != "in_progress"
        or next_row["Status"] != "pending"
        or not decision.is_file()
        or not transition.is_file()
    ):
        raise ValueError("G4 data-quality acceptance requires the resumed current row and exact evidence")
    target.update({"Status": "accepted", "Owner decision": ref(decision), "Transition receipt": ref(transition)})
    transition_hash = sha(transition)
    details[stage_id].update({
        "transition_receipt": ref(transition),
        "transition_receipt_sha256": transition_hash,
        "execution_allowed": "false",
    })
    dependencies = [item.strip() for item in next_row["Dependencies"].split(",") if item.strip()]
    if stage_id not in dependencies:
        dependencies.append(stage_id)
    next_row["Dependencies"] = ", ".join(dependencies)
    details[next_stage_id].update({
        "execution_allowed": "true",
        "incoming_transition_receipt": ref(transition),
        "incoming_transition_receipt_sha256": transition_hash,
    })
    front.update({"ledger_status": "active", "current_stage": next_stage_id, "Next stage allowed": "false"})


def g4dq_transition_assembly(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    g4dq_ready_provisional(front, rows, details, prepared=True)
    details["G4@family.an.shell-workspace.baseline-r5"]["execution_allowed"] = "true"


def g4an_review_ready(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]], *, prepared: bool,
) -> None:
    stage_id = STAGES["g4an"]
    target = row(rows, stage_id)
    evidence_dir = DIR / "evidence/family.an.shell-workspace.baseline-r5"
    transition = evidence_dir / "stage-transition-review-ready.json"
    board = DIR / "artifacts/g4-r5/family-an-shell-workspace-baseline/review-board.html"
    packet = evidence_dir / "owner-review-decision-packet.md"
    family = evidence_dir / "family-acceptance.json"
    required = (packet, board, family) if prepared else (packet, transition, board, family)
    valid_frontier = (
        front.get("ledger_status") == "active" and target["Status"] == "in_progress"
    ) if prepared else (
        (front.get("ledger_status") == "active" and target["Status"] == "in_progress")
        or (front.get("ledger_status") == "awaiting_input" and target["Status"] == "needs_input")
    )
    if front.get("current_stage") != stage_id or not valid_frontier:
        raise ValueError("G4 analytics research review-ready requires the exact current row")
    for path in required:
        if not path.is_file():
            raise ValueError(f"G4 analytics research review-ready artifact is missing: {path}")
    target.update({
        "Status": "needs_input",
        "Evidence": ref(board),
        "Transition receipt": ref(transition),
        "Owner decision": "required",
    })
    details[stage_id].update({
        "decision_packet": ref(packet),
        "resume_condition": "owner_accepts_or_requests_bounded_corrections_for_exact_finished_g4_analytics_research_r5_board",
        "resume_evidence_ref": "none",
        "resume_evidence_sha256": "none",
        "transition_receipt": ref(transition),
        "transition_receipt_sha256": "none" if prepared else sha(transition),
    })
    front.update({"ledger_status": "awaiting_input", "current_stage": stage_id, "Next stage allowed": "false"})


def g4an_resume(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g4an"]
    target = row(rows, stage_id)
    evidence_dir = DIR / "evidence/family.an.shell-workspace.baseline-r5"
    response = evidence_dir / "owner-input-response-acceptance-r5.json"
    decision = evidence_dir / "family-acceptance-decision-r5.json"
    if (
        front.get("ledger_status") != "awaiting_input"
        or front.get("current_stage") != stage_id
        or target["Status"] != "needs_input"
        or not response.is_file()
        or not decision.is_file()
    ):
        raise ValueError("G4 analytics research acceptance resume requires the exact accepted awaiting-input frontier")
    target.update({"Status": "in_progress", "Owner decision": ref(decision)})
    details[stage_id].update({
        "resume_evidence_ref": ref(response),
        "resume_evidence_sha256": sha(response),
    })
    front.update({"ledger_status": "active", "current_stage": stage_id, "Next stage allowed": "false"})


def g4an_ready_provisional(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]], *, prepared: bool,
) -> None:
    stage_id = STAGES["g4an"]
    next_stage_id = "G4@family.seg.shell-workspace.baseline-r5"
    target = row(rows, stage_id)
    next_row = row(rows, next_stage_id)
    evidence_dir = DIR / "evidence/family.an.shell-workspace.baseline-r5"
    decision = evidence_dir / "family-acceptance-decision-r5.json"
    transition = evidence_dir / "stage-transition.json"
    if (
        front.get("ledger_status") != "active"
        or front.get("current_stage") != stage_id
        or target["Status"] != "in_progress"
        or next_row["Status"] != "pending"
        or not decision.is_file()
        or (not prepared and not transition.is_file())
    ):
        raise ValueError("G4 analytics research ready provisional requires the resumed current row and pending successor")
    transition_hash = "none" if prepared else sha(transition)
    target.update({"Transition receipt": ref(transition), "Owner decision": ref(decision)})
    details[stage_id].update({
        "transition_receipt": ref(transition),
        "transition_receipt_sha256": transition_hash,
    })
    dependencies = [item.strip() for item in next_row["Dependencies"].split(",") if item.strip()]
    if stage_id not in dependencies:
        dependencies.append(stage_id)
    next_row["Dependencies"] = ", ".join(dependencies)
    if prepared:
        details[next_stage_id]["execution_allowed"] = "true"
    else:
        details[next_stage_id].update({
            "execution_allowed": "true",
            "incoming_transition_receipt": ref(transition),
            "incoming_transition_receipt_sha256": transition_hash,
        })


def g4an_accept(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g4an"]
    next_stage_id = "G4@family.seg.shell-workspace.baseline-r5"
    target = row(rows, stage_id)
    next_row = row(rows, next_stage_id)
    evidence_dir = DIR / "evidence/family.an.shell-workspace.baseline-r5"
    decision = evidence_dir / "family-acceptance-decision-r5.json"
    transition = evidence_dir / "stage-transition.json"
    if (
        front.get("ledger_status") != "active"
        or front.get("current_stage") != stage_id
        or target["Status"] != "in_progress"
        or next_row["Status"] != "pending"
        or not decision.is_file()
        or not transition.is_file()
    ):
        raise ValueError("G4 analytics research acceptance requires the resumed current row and exact evidence")
    target.update({"Status": "accepted", "Owner decision": ref(decision), "Transition receipt": ref(transition)})
    transition_hash = sha(transition)
    details[stage_id].update({
        "transition_receipt": ref(transition),
        "transition_receipt_sha256": transition_hash,
        "execution_allowed": "false",
    })
    dependencies = [item.strip() for item in next_row["Dependencies"].split(",") if item.strip()]
    if stage_id not in dependencies:
        dependencies.append(stage_id)
    next_row["Dependencies"] = ", ".join(dependencies)
    details[next_stage_id].update({
        "execution_allowed": "true",
        "incoming_transition_receipt": ref(transition),
        "incoming_transition_receipt_sha256": transition_hash,
    })
    front.update({"ledger_status": "active", "current_stage": next_stage_id, "Next stage allowed": "false"})


def g4_accept(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g4"]
    next_stage_id = "G4@family.auth.shell-workspace.baseline-r5"
    target = row(rows, stage_id)
    next_row = row(rows, next_stage_id)
    evidence_dir = DIR / "evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth"
    decision = evidence_dir / "family-acceptance-decision-r6.json"
    transition = evidence_dir / "stage-transition.json"
    if (
        front.get("ledger_status") != "active"
        or front.get("current_stage") != stage_id
        or target["Status"] != "in_progress"
        or next_row["Status"] != "pending"
        or not decision.is_file()
        or not transition.is_file()
    ):
        raise ValueError("G4 acceptance source state or exact evidence is invalid")
    target.update({
        "Status": "accepted",
        "Owner decision": ref(decision),
        "Transition receipt": ref(transition),
    })
    transition_hash = sha(transition)
    details[stage_id].update({
        "transition_receipt": ref(transition),
        "transition_receipt_sha256": transition_hash,
        "execution_allowed": "false",
    })
    details[next_stage_id].update({
        "execution_allowed": "true",
        "incoming_transition_receipt": ref(transition),
        "incoming_transition_receipt_sha256": transition_hash,
    })
    front.update({"ledger_status": "active", "current_stage": next_stage_id, "Next stage allowed": "false"})


def g4_ready_provisional(
    front: dict[str, str], rows: list[dict[str, str]], details: dict[str, dict[str, str]],
) -> None:
    stage_id = STAGES["g4"]
    next_stage_id = "G4@family.auth.shell-workspace.baseline-r5"
    target = row(rows, stage_id)
    next_row = row(rows, next_stage_id)
    transition = DIR / "evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth/stage-transition.json"
    if (
        front.get("ledger_status") != "active"
        or front.get("current_stage") != stage_id
        or target["Status"] != "in_progress"
        or next_row["Status"] != "pending"
    ):
        raise ValueError("G4 ready provisional requires the resumed current row and pending successor")
    if not transition.is_file():
        raise ValueError("G4 ready provisional requires a readable seed transition receipt")
    transition_hash = sha(transition)
    target["Transition receipt"] = ref(transition)
    details[stage_id].update({
        "transition_receipt": ref(transition),
        "transition_receipt_sha256": transition_hash,
    })
    details[next_stage_id].update({
        "execution_allowed": "true",
        "incoming_transition_receipt": ref(transition),
        "incoming_transition_receipt_sha256": transition_hash,
    })


def refresh_transition(
    rows: list[dict[str, str]], details: dict[str, dict[str, str]], stage_id: str, next_stage_id: str,
) -> None:
    target = row(rows, stage_id)
    transition = ROOT / target["Transition receipt"]
    if target["Status"] != "accepted" or not transition.is_file():
        raise ValueError("transition refresh requires an accepted stage and readable receipt")
    transition_hash = sha(transition)
    details[stage_id]["transition_receipt_sha256"] = transition_hash
    details[next_stage_id].update({
        "incoming_transition_receipt": ref(transition),
        "incoming_transition_receipt_sha256": transition_hash,
    })


def repair_g2_paths(rows: list[dict[str, str]], details: dict[str, dict[str, str]]) -> None:
    stage_id = STAGES["g2"]
    target = row(rows, stage_id)
    report = ".codex/delivery/evidence/custometry-ui-design-program-v2/g2-r4-structure-report.md"
    transition = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g2-r4/stage-transition.json"
    if target["Status"] != "in_progress":
        raise ValueError("G2 path repair requires the claimed current row")
    target["Evidence"] = report
    target["Transition receipt"] = transition
    details[stage_id]["report_path"] = report
    details[stage_id]["transition_receipt"] = transition


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=(
        "claim-g0", "prepare-g0", "accept-g0", "refresh-g0", "claim-g1", "prepare-g1", "accept-g1",
        "claim-g2", "repair-g2-paths", "prepare-g2", "accept-g2", "claim-g3", "g3-review-ready",
        "g3-resume", "g3-accept", "claim-g4", "claim-g4w", "g4-resume", "g4-ready-provisional", "g4-accept",
        "g4-review-ready-prepare", "g4-review-ready", "g4w-review-ready-prepare", "g4w-review-ready",
        "g4w-resume", "g4w-ready-provisional-prepare", "g4w-ready-provisional", "g4w-accept",
        "g4c-resume", "g4c-review-ready-prepare", "g4c-review-ready", "g4c-acceptance-resume",
        "g4c-ready-provisional-prepare", "g4c-ready-provisional", "g4c-accept",
        "g4dq-resume", "g4dq-ready-provisional-prepare", "g4dq-ready-provisional", "g4dq-transition-assembly", "g4dq-accept",
        "claim-g4an", "g4an-review-ready-prepare", "g4an-review-ready", "g4an-resume",
        "g4an-ready-provisional-prepare", "g4an-accept",
    ))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--validation-ledger-self-ref", action="store_true")
    args = parser.parse_args()
    front, rows, details = load()
    if args.mode.startswith("claim-"):
        key = args.mode.removeprefix("claim-")
        claim(front, rows, STAGES[key], f"blueprint-rebind-r5-{key}")
    elif args.mode in {"prepare-g0", "accept-g0"}:
        accept(front, rows, details, STAGES["g0"], STAGES["g1"], prepared=args.mode.startswith("prepare-"))
    elif args.mode == "refresh-g0":
        refresh_transition(rows, details, STAGES["g0"], STAGES["g1"])
    elif args.mode in {"prepare-g1", "accept-g1"}:
        accept(front, rows, details, STAGES["g1"], STAGES["g2"], prepared=args.mode.startswith("prepare-"))
    elif args.mode in {"prepare-g2", "accept-g2"}:
        accept(front, rows, details, STAGES["g2"], STAGES["g3"], prepared=args.mode.startswith("prepare-"))
    elif args.mode == "repair-g2-paths":
        repair_g2_paths(rows, details)
    elif args.mode == "g3-review-ready":
        g3_review_ready(front, rows, details)
    elif args.mode == "g3-resume":
        g3_resume(front, rows, details)
    elif args.mode == "g3-accept":
        g3_accept(front, rows, details)
    elif args.mode in {"g4-review-ready-prepare", "g4-review-ready"}:
        g4_review_ready(front, rows, details, prepared=args.mode.endswith("prepare"))
    elif args.mode in {"g4w-review-ready-prepare", "g4w-review-ready"}:
        g4w_review_ready(front, rows, details, prepared=args.mode.endswith("prepare"))
    elif args.mode == "g4w-resume":
        g4w_resume(front, rows, details)
    elif args.mode == "g4c-resume":
        g4c_resume(front, rows, details)
    elif args.mode == "g4c-acceptance-resume":
        g4c_acceptance_resume(front, rows, details)
    elif args.mode in {"g4c-review-ready-prepare", "g4c-review-ready"}:
        g4c_review_ready(front, rows, details, prepared=args.mode.endswith("prepare"))
    elif args.mode in {"g4w-ready-provisional-prepare", "g4w-ready-provisional"}:
        g4w_ready_provisional(front, rows, details, prepared=args.mode.endswith("prepare"))
    elif args.mode == "g4w-accept":
        g4w_accept(front, rows, details)
    elif args.mode in {"g4c-ready-provisional-prepare", "g4c-ready-provisional"}:
        g4c_ready_provisional(front, rows, details, prepared=args.mode.endswith("prepare"))
    elif args.mode == "g4c-accept":
        g4c_accept(front, rows, details)
    elif args.mode == "g4dq-resume":
        g4dq_resume(front, rows, details)
    elif args.mode in {"g4dq-ready-provisional-prepare", "g4dq-ready-provisional"}:
        g4dq_ready_provisional(front, rows, details, prepared=args.mode.endswith("prepare"))
    elif args.mode == "g4dq-transition-assembly":
        g4dq_transition_assembly(front, rows, details)
    elif args.mode == "g4dq-accept":
        g4dq_accept(front, rows, details)
    elif args.mode in {"g4an-review-ready-prepare", "g4an-review-ready"}:
        g4an_review_ready(front, rows, details, prepared=args.mode.endswith("prepare"))
    elif args.mode == "g4an-resume":
        g4an_resume(front, rows, details)
    elif args.mode == "g4an-ready-provisional-prepare":
        g4an_ready_provisional(front, rows, details, prepared=True)
    elif args.mode == "g4an-accept":
        g4an_accept(front, rows, details)
    elif args.mode == "g4-resume":
        g4_resume(front, rows, details)
    elif args.mode == "g4-ready-provisional":
        g4_ready_provisional(front, rows, details)
    elif args.mode == "g4-accept":
        g4_accept(front, rows, details)
    else:
        claim(front, rows, STAGES["g4"], "blueprint-rebind-r5-g4-auth-r6")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    rendered = render_ledger(front, rows, details)
    if args.validation_ledger_self_ref:
        canonical = f"stage_ledger: {ref(LEDGER)}"
        candidate = f"stage_ledger: {ref(args.output.resolve())}"
        if canonical not in rendered:
            raise ValueError("canonical stage_ledger frontmatter is missing")
        rendered = rendered.replace(canonical, candidate, 1)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"source_sha256={sha(LEDGER)}")
    print(f"candidate_sha256={sha(args.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
