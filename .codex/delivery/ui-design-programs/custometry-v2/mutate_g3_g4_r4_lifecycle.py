#!/usr/bin/env python3
"""Build deterministic CAS candidates for the G3 r4 -> auth G4 r5 lifecycle."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
LEDGER = DIR / "stage-ledger.md"
G3 = "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4"
G4 = "G4@family.auth.shell-auth.baseline-exception-auth-r5"
NEXT_G4 = "G4@family.auth.shell-workspace.baseline-r4"
G3_EVID = DIR / "evidence/g3-r4"
G4_EVID = DIR / "evidence/g4-r5/family-auth-shell-auth-baseline-exception-auth"
sys.path.insert(0, str(DIR))
from build_g3_r4_active_semantic_migration import render_ledger, sha  # noqa: E402
sys.path.insert(0, "/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")
from validate_stage_ledger import parse_ledger  # noqa: E402


def ref(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load() -> tuple[dict, list[dict[str, str]], dict[str, dict[str, str]]]:
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


def exact_file(path: Path) -> tuple[str, str]:
    if not path.is_file():
        raise ValueError(f"required lifecycle artifact is missing: {path}")
    return ref(path), sha(path)


def claim(front: dict, rows: list[dict[str, str]], details: dict[str, dict[str, str]], stage_id: str, label: str) -> None:
    target = row(rows, stage_id)
    if front.get("ledger_status") != "active" or front.get("current_stage") != stage_id or target["Status"] != "pending":
        raise ValueError("claim source state is not the exact pending active frontier")
    now = datetime.now(timezone.utc).replace(microsecond=0)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    target["Status"] = "in_progress"
    target["Executor claim"] = f"codex-root-{label}-{stamp}"
    target["Claimed at"] = now.isoformat().replace("+00:00", "Z")


def g3_review_ready(front: dict, rows: list[dict[str, str]], details: dict[str, dict[str, str]]) -> None:
    target = row(rows, G3)
    if target["Status"] != "in_progress":
        raise ValueError("G3 review_ready requires its claimed in_progress row")
    packet_ref, _ = exact_file(G3_EVID / "owner-review-decision-packet.json")
    transition_ref, transition_hash = exact_file(G3_EVID / "stage-transition-review-ready.json")
    target["Status"] = "needs_input"
    details[G3].update({
        "decision_packet": packet_ref,
        "resume_condition": "owner_accepts_or_requests_bounded_corrections_for_exact_finished_g3_r4_board",
        "resume_evidence_ref": "none",
        "resume_evidence_sha256": "none",
        "transition_receipt": transition_ref,
        "transition_receipt_sha256": transition_hash,
    })
    target["Transition receipt"] = transition_ref
    front.update({"ledger_status": "awaiting_input", "current_stage": G3, "Next stage allowed": "false"})


def g3_resume(front: dict, rows: list[dict[str, str]], details: dict[str, dict[str, str]]) -> None:
    target = row(rows, G3)
    response_ref, response_hash = exact_file(G3_EVID / "owner-input-response-acceptance-r4.json")
    if front.get("ledger_status") != "awaiting_input" or target["Status"] != "needs_input":
        raise ValueError("G3 resume requires the exact awaiting_input row")
    target["Status"] = "in_progress"
    details[G3].update({"resume_evidence_ref": response_ref, "resume_evidence_sha256": response_hash})
    front.update({"ledger_status": "active", "current_stage": G3, "Next stage allowed": "false"})


def g3_accept(front: dict, rows: list[dict[str, str]], details: dict[str, dict[str, str]]) -> None:
    target = row(rows, G3)
    next_row = row(rows, G4)
    decision_ref, _ = exact_file(G3_EVID / "stage-acceptance-decision-r4.json")
    transition_ref, transition_hash = exact_file(G3_EVID / "stage-transition.json")
    if target["Status"] != "in_progress" or next_row["Status"] != "pending":
        raise ValueError("G3 acceptance source state is invalid")
    target.update({"Status": "accepted", "Owner decision": decision_ref, "Transition receipt": transition_ref})
    details[G3].update({"transition_receipt": transition_ref, "transition_receipt_sha256": transition_hash, "execution_allowed": "false"})
    details[G4].update({
        "execution_allowed": "true",
        "incoming_transition_receipt": transition_ref,
        "incoming_transition_receipt_sha256": transition_hash,
    })
    front.update({"ledger_status": "active", "current_stage": G4, "Next stage allowed": "false"})


def g4_review_ready(front: dict, rows: list[dict[str, str]], details: dict[str, dict[str, str]]) -> None:
    target = row(rows, G4)
    if target["Status"] != "in_progress":
        raise ValueError("G4 review_ready requires its claimed in_progress row")
    packet_ref, _ = exact_file(G4_EVID / "owner-review-decision-packet-correction-r5-03.json")
    transition_ref, transition_hash = exact_file(G4_EVID / "stage-transition.json")
    board_ref, _ = exact_file(DIR / "artifacts/g4-r5/family-auth-shell-auth-baseline-exception-auth/review-board.html")
    target.update({"Status": "needs_input", "Evidence": board_ref, "Transition receipt": transition_ref})
    details[G4].update({
        "decision_packet": packet_ref,
        "resume_condition": "owner_accepts_or_requests_bounded_corrections_for_exact_finished_auth_family_r5_board",
        "resume_evidence_ref": "none", "resume_evidence_sha256": "none",
        "transition_receipt": transition_ref, "transition_receipt_sha256": transition_hash,
    })
    front.update({"ledger_status": "awaiting_input", "current_stage": G4, "Next stage allowed": "false"})


def g4_resume_corrections(front: dict, rows: list[dict[str, str]], details: dict[str, dict[str, str]]) -> None:
    """Resume the same unaccepted G4 revision from a canonical bounded-correction response."""
    target = row(rows, G4)
    response_ref, response_hash = exact_file(G4_EVID / "owner-input-response-corrections-r5-03.json")
    if (
        front.get("ledger_status") != "awaiting_input"
        or front.get("current_stage") != G4
        or target["Status"] != "needs_input"
    ):
        raise ValueError("G4 correction resume requires the exact awaiting_input row")
    target["Status"] = "in_progress"
    details[G4].update({
        "resume_evidence_ref": response_ref,
        "resume_evidence_sha256": response_hash,
        "transition_receipt_sha256": "none",
    })
    front.update({"ledger_status": "active", "current_stage": G4, "Next stage allowed": "false"})


def g4_resume_acceptance(front: dict, rows: list[dict[str, str]], details: dict[str, dict[str, str]]) -> None:
    """Resume the exact review-ready row from the canonical visual-acceptance response."""
    target = row(rows, G4)
    response_ref, response_hash = exact_file(G4_EVID / "owner-input-response-acceptance-r5-03.json")
    if (
        front.get("ledger_status") != "awaiting_input"
        or front.get("current_stage") != G4
        or target["Status"] != "needs_input"
    ):
        raise ValueError("G4 acceptance resume requires the exact awaiting_input row")
    target["Status"] = "in_progress"
    details[G4].update({
        "resume_evidence_ref": response_ref,
        "resume_evidence_sha256": response_hash,
        "transition_receipt_sha256": "none",
    })
    front.update({"ledger_status": "active", "current_stage": G4, "Next stage allowed": "false"})


def g4_accept(front: dict, rows: list[dict[str, str]], details: dict[str, dict[str, str]]) -> None:
    """Accept G4 only from the canonical owner decision and strict ready transition."""
    target = row(rows, G4)
    next_row = row(rows, NEXT_G4)
    decision_ref, _ = exact_file(G4_EVID / "family-acceptance-decision-r5-03.json")
    transition_ref, transition_hash = exact_file(G4_EVID / "stage-transition.json")
    if (
        front.get("ledger_status") != "active"
        or front.get("current_stage") != G4
        or target["Status"] != "in_progress"
        or next_row["Status"] != "pending"
    ):
        raise ValueError("G4 acceptance source state is invalid")
    target.update({"Status": "accepted", "Owner decision": decision_ref, "Transition receipt": transition_ref})
    next_dependencies = [
        item.strip() for item in next_row["Dependencies"].split(",") if item.strip()
    ]
    if G4 not in next_dependencies:
        next_dependencies.append(G4)
    next_row["Dependencies"] = ", ".join(next_dependencies)
    details[G4].update({
        "transition_receipt": transition_ref,
        "transition_receipt_sha256": transition_hash,
        "execution_allowed": "false",
    })
    details[NEXT_G4].update({
        "execution_allowed": "true",
        "incoming_transition_receipt": transition_ref,
        "incoming_transition_receipt_sha256": transition_hash,
    })
    front.update({"ledger_status": "active", "current_stage": NEXT_G4, "Next stage allowed": "false"})


def g4_refresh_review_ready(front: dict, rows: list[dict[str, str]], details: dict[str, dict[str, str]]) -> None:
    """Refresh the exact assembled transition hash after the review-ready CAS."""
    target = row(rows, G4)
    transition_ref, transition_hash = exact_file(G4_EVID / "stage-transition.json")
    if (
        front.get("ledger_status") != "awaiting_input"
        or front.get("current_stage") != G4
        or target["Status"] != "needs_input"
    ):
        raise ValueError("G4 review-ready refresh requires the exact awaiting_input row")
    target["Transition receipt"] = transition_ref
    details[G4].update({"transition_receipt": transition_ref, "transition_receipt_sha256": transition_hash})
    front["Next stage allowed"] = "false"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("claim-g3", "g3-review-ready", "g3-resume", "g3-accept", "claim-g4", "g4-resume-corrections", "g4-resume-acceptance", "g4-review-ready", "g4-refresh-review-ready", "g4-accept"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--validation-ledger-self-ref", action="store_true")
    args = parser.parse_args()
    front, rows, details = load()
    if args.mode == "claim-g3":
        claim(front, rows, details, G3, "g3-r4")
    elif args.mode == "g3-review-ready":
        g3_review_ready(front, rows, details)
    elif args.mode == "g3-resume":
        g3_resume(front, rows, details)
    elif args.mode == "g3-accept":
        g3_accept(front, rows, details)
    elif args.mode == "claim-g4":
        claim(front, rows, details, G4, "g4-auth-r5")
    elif args.mode == "g4-resume-corrections":
        g4_resume_corrections(front, rows, details)
    elif args.mode == "g4-resume-acceptance":
        g4_resume_acceptance(front, rows, details)
    elif args.mode == "g4-refresh-review-ready":
        g4_refresh_review_ready(front, rows, details)
    elif args.mode == "g4-accept":
        g4_accept(front, rows, details)
    else:
        g4_review_ready(front, rows, details)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    rendered = render_ledger(front, rows, details)
    if args.validation_ledger_self_ref:
        canonical = f"stage_ledger: {ref(LEDGER)}"
        self_ref = f"stage_ledger: {ref(args.output.resolve())}"
        if canonical not in rendered:
            raise ValueError("canonical stage_ledger frontmatter is missing")
        rendered = rendered.replace(canonical, self_ref, 1)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"source_sha256={sha(LEDGER)}")
    print(f"candidate_sha256={sha(args.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
