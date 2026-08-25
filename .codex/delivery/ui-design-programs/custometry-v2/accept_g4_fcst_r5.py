#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROGRAM = ROOT / ".codex/delivery/ui-design-programs/custometry-v2"
LEDGER = PROGRAM / "stage-ledger.md"
ARTIFACT = PROGRAM / "artifacts/g4-r5/family-fcst-shell-workspace-baseline"
EVIDENCE = PROGRAM / "evidence/family.fcst.shell-workspace.baseline-r5"
PREFLIGHT = EVIDENCE / "preflight"
REPORT = ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/family.fcst.shell-workspace.baseline-r5-report.md"
STAGE = "G4@family.fcst.shell-workspace.baseline-r5"
NEXT_STAGE = "G4@family.promo.shell-workspace.baseline-r5"
NEXT_PROMPT = ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-09-family-promo-shell-workspace-baseline-r5.md"
BOARD = ARTIFACT / "review-board.html"
DECISION = EVIDENCE / "family-acceptance-decision-r5.json"
RESPONSE = EVIDENCE / "owner-input-response-acceptance-r5.json"
TRANSITION = EVIDENCE / "stage-transition.json"
FAMILY = EVIDENCE / "family-acceptance.json"
OWNER_INPUT = "Окей, принимаю это."
STATES = ("initial", "loading", "populated", "error", "permission_denied", "recovery")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_once(text: str, before: str, after: str) -> str:
    count = text.count(before)
    if count != 1:
        raise ValueError(f"expected one occurrence, observed {count}: {before[:120]!r}")
    return text.replace(before, after, 1)


def update_row(text: str, stage_id: str, updates: dict[int, str]) -> str:
    rows = text.splitlines()
    index = next(i for i, line in enumerate(rows) if line.startswith(f"| {stage_id} |"))
    cells = [cell.strip() for cell in rows[index].strip().strip("|").split("|")]
    for position, value in updates.items():
        cells[position] = value
    rows[index] = "| " + " | ".join(cells) + " |"
    return "\n".join(rows) + ("\n" if text.endswith("\n") else "")


def update_detail(text: str, stage_id: str, updates: dict[str, str]) -> str:
    heading = f"### `{stage_id}`\n"
    start = text.index(heading)
    next_heading = text.find("\n### `", start + len(heading))
    end = len(text) if next_heading == -1 else next_heading
    block = text[start:end]
    for key, value in updates.items():
        lines = block.splitlines()
        matches = [i for i, line in enumerate(lines) if line.startswith(f"- {key}: `")]
        if len(matches) != 1:
            raise ValueError(f"detail {stage_id}.{key} expected once, observed {len(matches)}")
        lines[matches[0]] = f"- {key}: `{value}`"
        block = "\n".join(lines) + ("\n" if block.endswith("\n") else "")
    return text[:start] + block + text[end:]


def owner_requests() -> None:
    dump(EVIDENCE / "family-acceptance-decision-r5-request.json", {
        "$schema": "owner-decision-request.schema.json",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "decision_id": f"{STAGE}.finished-result",
        "decision_kind": "family_acceptance",
        "status": "accepted",
        "revision": 5,
        "decision_text": "The owner explicitly accepted the complete HTML review board shown for the G4 Forecast family. Acceptance covers UI-FCST-001 in all six required states, the four responsive-Web anchors, both visible isolated actions, Result Trust, and applicable pilot visual-language inheritance. It does not authorize production implementation, publication, deployment, mobile-specific design, another G4 family, G5, G6, or full WCAG conformance.",
        "owner_input": OWNER_INPUT,
        "target": {
            "artifact_kind": "review_board",
            "artifact_id": "family.fcst.shell-workspace.baseline-r5",
            "revision": 5,
            "validation_profile": "family_review_ready",
            "path": rel(BOARD),
        },
        "accepted_values": [{
            "stage_instance_id": STAGE,
            "screen_ids": ["UI-FCST-001"],
            "required_states": list(STATES),
            "responsive_web_anchors": [768, 1024, 1440, 1920],
            "source_bound_fixture_action_count": 2,
            "result_trust_visible": True,
            "mobile_scope": "unauthorized",
            "production_implementation": "not_accepted_by_this_decision",
        }],
    })
    dump(EVIDENCE / "owner-input-response-acceptance-r5-request.json", {
        "$schema": "owner-input-response-request.schema.json",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "stage_instance_id": STAGE,
        "decision_packet_ref": rel(EVIDENCE / "owner-review-decision-packet.md"),
        "response_kind": "visual_acceptance",
        "owner_input": OWNER_INPUT,
        "canonical_owner_decision_ref": rel(DECISION),
    })


def resume_candidate() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    text = replace_once(text, "ledger_status: awaiting_input", "ledger_status: active")
    text = update_row(text, STAGE, {4: "in_progress", 8: rel(DECISION)})
    text = update_detail(text, STAGE, {
        "resume_evidence_ref": rel(RESPONSE),
        "resume_evidence_sha256": sha(RESPONSE),
    })
    (EVIDENCE / "acceptance-resume-candidate.md").write_text(text, encoding="utf-8")


def acceptance_request() -> None:
    request = json.loads((EVIDENCE / "family-acceptance-request-review-ready.json").read_text(encoding="utf-8"))
    request["owner_decision_ref"] = rel(DECISION)
    dump(EVIDENCE / "family-acceptance-request.json", request)
    dump(EVIDENCE / "resolved-owner-decisions.json", [{
        "decision_id": f"{STAGE}.finished-result",
        "class": "owner_required",
        "status": "resolved",
        "summary": "The owner explicitly accepted the complete Forecast r5 HTML review board.",
        "resolution_ref": rel(DECISION),
    }])
    dump(EVIDENCE / "known-blockers.json", [])


def transition_inputs() -> None:
    family = json.loads(FAMILY.read_text(encoding="utf-8"))
    if family.get("result") != "passed" or family.get("owner_decision_ref") != rel(DECISION):
        raise ValueError("strict accepted family aggregate is not current")
    sys.path.insert(0, "/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")
    from validate_stage_transition import hash_bound_source_refs  # type: ignore

    checks = {
        "current_gate": {"validation_profile": "family_gate", "artifact_ref": rel(FAMILY), "artifact_sha256": sha(FAMILY), "result": "passed"},
        "source_freshness": {"source_refs": hash_bound_source_refs(FAMILY, ROOT), "drift_classification": "owned_generated_change", "stale_refs": []},
        "next_stage_inputs": {"next_stage_id": NEXT_STAGE, "task_ref": rel(NEXT_PROMPT), "unresolved_inputs": []},
        "write_scope": {"allowed_paths": [".codex/agents/generated/custometry-ui-design-g0-v2/**", ".codex/delivery/evidence/custometry-ui-design-program-v2/**", ".codex/delivery/ui-design-programs/custometry-v2/**"], "authorization_basis": "active_task_and_repository_contract", "outside_scope_paths": []},
        "foreign_changes": {"observed_paths": [".codex/AGENTS.md", "custometry-technical-blueprint-human-ru.md", "custometry-technical-blueprint-ru.md", "custometry-ui-blueprint-ru.md", "docs/generated/requirement-index.json", "packages/contracts/routes/ui-surface-contracts.json"], "inseparable_paths": [], "disposition": "separable_foreign_changes_preserved"},
        "execution_route": {"route": "goal_driven staged-plan-runner with ui-design-program CAS ledger updates", "available": True},
        "handoff_artifact": {"artifact_ref": rel(NEXT_PROMPT), "artifact_sha256": sha(NEXT_PROMPT), "known_stop_resolution": "none"},
    }
    for check_id, facts in checks.items():
        dump(PREFLIGHT / f"{check_id}.json", {"$schema": "stage-preflight-evidence.schema.json", "schema_id": "codex.ui-stage-preflight-evidence/v1", "check_id": check_id, "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2", "stage_instance_id": STAGE, "gate_id": "G4", "status": "passed", "facts": facts})
    dump(EVIDENCE / "stage-transition-request.json", {
        "$schema": "stage-transition-request.schema.json",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "from_stage_id": STAGE,
        "from_gate": "G4",
        "from_target": "family.fcst.shell-workspace.baseline-r5",
        "from_revision": 5,
        "artifact": rel(FAMILY),
        "to_gate": "G4",
        "to_stage_id": NEXT_STAGE,
        "to_target": "family.promo.shell-workspace.baseline-r5",
        "to_task": rel(NEXT_PROMPT),
        "status": "ready",
        "owner_decision": rel(DECISION),
        "decision_inventory": rel(EVIDENCE / "resolved-owner-decisions.json"),
        "blockers": rel(EVIDENCE / "known-blockers.json"),
        "checks": [f"{key}={rel(PREFLIGHT / f'{key}.json')}" for key in ("current_gate", "source_freshness", "next_stage_inputs", "write_scope", "foreign_changes", "execution_route", "handoff_artifact")],
        "summary": "The owner accepted the complete Forecast HTML review board; the strict family gate and adjacent-stage preflight pass.",
        "review_artifacts": [rel(BOARD), rel(EVIDENCE / "review-board-1440.png"), rel(EVIDENCE / "browser-board-qa.json")],
        "questions": [],
    })
    REPORT.write_text(f"""---
artifact_kind: ui_design_stage_report
program_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2
stage_instance_id: {STAGE}
status: ready
---

# G4 forecast family accepted report

The owner accepted the complete hash-bound HTML review board for `UI-FCST-001`,
covering all six required states and responsive-Web anchors 768, 1024, 1440,
and 1920.

- Family aggregate: `{rel(FAMILY)}` (`passed`)
- Owner decision: `{rel(DECISION)}`
- Owner input response: `{rel(RESPONSE)}`
- Review board: `{rel(BOARD)}`
- Browser QA: `{rel(EVIDENCE / 'browser-board-qa.json')}`
- Transition: `{rel(TRANSITION)}` (`ready` after assembly)

The proof boundary excludes production implementation, publication, deployment,
mobile-specific design, full WCAG conformance, real-data side effects, and the
execution of the adjacent G4 family.
""", encoding="utf-8")


def transition_assembly_candidate() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    output = EVIDENCE / "transition-assembly-ledger-candidate.md"
    text = replace_once(text, f"stage_ledger: {rel(LEDGER)}", f"stage_ledger: {rel(output)}")
    text = update_row(text, STAGE, {7: rel(TRANSITION)})
    rows = text.splitlines()
    next_index = next(i for i, line in enumerate(rows) if line.startswith(f"| {NEXT_STAGE} |"))
    next_cells = [cell.strip() for cell in rows[next_index].strip().strip("|").split("|")]
    dependencies = [item.strip() for item in next_cells[5].split(",") if item.strip() and item.strip() != "—"]
    if STAGE not in dependencies:
        dependencies.append(STAGE)
    next_cells[5] = ", ".join(dependencies)
    rows[next_index] = "| " + " | ".join(next_cells) + " |"
    text = "\n".join(rows) + ("\n" if text.endswith("\n") else "")
    text = update_detail(text, STAGE, {
        "transition_receipt": rel(TRANSITION),
        "transition_receipt_sha256": "none",
    })
    text = update_detail(text, NEXT_STAGE, {"execution_allowed": "true"})
    output.write_text(text, encoding="utf-8")


def accepted_candidate() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    text = replace_once(text, f"current_stage: {STAGE}", f"current_stage: {NEXT_STAGE}")
    text = update_row(text, STAGE, {4: "accepted", 6: rel(BOARD), 7: rel(TRANSITION), 8: rel(DECISION)})
    rows = text.splitlines()
    next_index = next(i for i, line in enumerate(rows) if line.startswith(f"| {NEXT_STAGE} |"))
    next_cells = [cell.strip() for cell in rows[next_index].strip().strip("|").split("|")]
    dependencies = [item.strip() for item in next_cells[5].split(",") if item.strip() and item.strip() != "—"]
    if STAGE not in dependencies:
        dependencies.append(STAGE)
    next_cells[5] = ", ".join(dependencies)
    rows[next_index] = "| " + " | ".join(next_cells) + " |"
    text = "\n".join(rows) + ("\n" if text.endswith("\n") else "")
    transition_hash = sha(TRANSITION)
    text = update_detail(text, STAGE, {
        "transition_receipt": rel(TRANSITION),
        "transition_receipt_sha256": transition_hash,
        "execution_allowed": "false",
    })
    text = update_detail(text, NEXT_STAGE, {
        "execution_allowed": "true",
        "incoming_transition_receipt": rel(TRANSITION),
        "incoming_transition_receipt_sha256": transition_hash,
    })
    (EVIDENCE / "accepted-ledger-candidate.md").write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("owner-requests", "resume-candidate", "acceptance-request", "transition-inputs", "transition-assembly-candidate", "accepted-candidate"))
    phase = parser.parse_args().phase
    {
        "owner-requests": owner_requests,
        "resume-candidate": resume_candidate,
        "acceptance-request": acceptance_request,
        "transition-inputs": transition_inputs,
        "transition-assembly-candidate": transition_assembly_candidate,
        "accepted-candidate": accepted_candidate,
    }[phase]()


if __name__ == "__main__":
    main()
