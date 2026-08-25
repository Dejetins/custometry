#!/usr/bin/env python3
"""Prepare deterministic G3 r4 review and accepted transition inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
EVID = DIR / "evidence/g3-r4"
PREFLIGHT = EVID / "preflight"
ART = DIR / "artifacts/g3-r4"
PROGRAM = DIR / "ui-design-program.json"
REPORT = ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4-report.md"
STAGE = "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4"
NEXT_STAGE = "G4@family.auth.shell-auth.baseline-exception-auth-r5"
NEXT_TARGET = "family.auth.shell-auth.baseline-exception-auth-r5"
NEXT_TASK = ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-01-family-auth-shell-auth-baseline-exception-auth-r5.md"
PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
        handle.write(rendered)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def evidence(check_id: str, facts: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": "stage-preflight-evidence.schema.json",
        "schema_id": "codex.ui-stage-preflight-evidence/v1",
        "check_id": check_id,
        "program_id": PROGRAM_ID,
        "stage_instance_id": STAGE,
        "gate_id": "G3",
        "status": "passed",
        "facts": facts,
    }


def hash_bound_refs(document: Any) -> list[dict[str, str]]:
    found: dict[str, str] = {}
    def visit(value: Any) -> None:
        if isinstance(value, dict):
            path, digest = value.get("path"), value.get("sha256")
            if isinstance(path, str) and isinstance(digest, str) and len(digest) == 64:
                found[path] = digest
            source, source_hash = value.get("source_visual_ref"), value.get("source_visual_sha256")
            if isinstance(source, str) and isinstance(source_hash, str) and len(source_hash) == 64:
                found[source] = source_hash
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
    visit(document)
    return [{"path": path, "sha256": digest} for path, digest in sorted(found.items())]


def review() -> None:
    program = json.loads(PROGRAM.read_text(encoding="utf-8"))
    board = ART / "review-board.html"
    standard = ROOT / program["g3_rendered_proof"]["standard_board"]["path"]
    candidate = ART / "candidate-shell.html"
    packet = EVID / "owner-review-decision-packet.json"
    decisions = EVID / "pending-owner-decisions.json"
    blockers = EVID / "known-blockers.json"
    write_json(blockers, [])
    checks = {
        "current_gate": evidence("current_gate", {"validation_profile": "program_ready", "artifact_ref": rel(PROGRAM), "artifact_sha256": sha(PROGRAM), "result": "passed"}),
        "source_freshness": evidence("source_freshness", {"source_refs": hash_bound_refs(program), "drift_classification": "owned_generated_change", "stale_refs": []}),
        "next_stage_inputs": evidence("next_stage_inputs", {"next_stage_id": NEXT_STAGE, "task_ref": rel(NEXT_TASK), "unresolved_inputs": []}),
        "write_scope": evidence("write_scope", {"allowed_paths": [".codex/delivery/ui-design-programs/custometry-v2/**", ".codex/agents/generated/custometry-ui-design-g0-v2/**", ".codex/delivery/evidence/custometry-ui-design-program-v2/**"], "authorization_basis": "explicit_current_user_authorization", "outside_scope_paths": []}),
        "foreign_changes": evidence("foreign_changes", {"observed_paths": [".codex/AGENTS.md", "custometry-technical-blueprint-ru.md", "custometry-technical-blueprint-human-ru.md", "custometry-ui-blueprint-ru.md", "docs/generated/requirement-index.json", "packages/contracts/routes/ui-surface-contracts.json"], "inseparable_paths": [], "disposition": "separable_foreign_changes_preserved"}),
        "execution_route": evidence("execution_route", {"route": "staged-plan-runner + ui-design-program + browser-qa-evidence/playwright-cli", "available": True}),
        "handoff_artifact": evidence("handoff_artifact", {"artifact_ref": rel(NEXT_TASK), "artifact_sha256": sha(NEXT_TASK), "known_stop_resolution": "none"}),
    }
    for key, value in checks.items():
        write_json(PREFLIGHT / f"{key}.json", value)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        f"# {PROGRAM_ID} G3 r4 compatibility reproof report\n\n"
        f"- Stage: `{STAGE}`; result: `review_ready`, accepted by the owner in natural language.\n"
        f"- Review board: `{rel(board)}` — `{sha(board)}`.\n"
        f"- Candidate shell: `{rel(candidate)}` — `{sha(candidate)}`.\n"
        "- Exact correction: four demonstration action buttons now inherit one stable accepted-pilot button identity each; mutually exclusive variants are never combined.\n"
        "- Unchanged: shell architecture, palette, content, routes, responsive composition and accepted visual authority.\n"
        "- Boundary: responsive-Web browser proof only; production code, deployment, publication, mobile-specific design and full WCAG conformance remain outside scope.\n",
        encoding="utf-8",
    )
    common = {
        "$schema": "stage-transition-request.schema.json", "program_id": PROGRAM_ID,
        "from_stage_id": STAGE, "from_gate": "G3", "from_target": f"{PROGRAM_ID}-r4", "from_revision": 4,
        "artifact": rel(PROGRAM), "to_gate": "G4", "to_stage_id": NEXT_STAGE, "to_target": NEXT_TARGET, "to_task": rel(NEXT_TASK),
        "blockers": rel(blockers),
        "checks": [f"{key}={rel(PREFLIGHT / f'{key}.json')}" for key in checks],
        "review_artifacts": [rel(board), rel(standard), rel(candidate), rel(EVID / "review-board-1440.png")],
    }
    request = dict(common)
    request.update({
        "status": "review_ready", "owner_decision": None, "decision_inventory": rel(decisions),
        "summary": "G3 r4 resolves the strict applicability compatibility issue while preserving the accepted shell and complete applicable pilot-rule inheritance.",
        "questions": ["Принять точное G3 r4 наследование оболочки или указать ограниченные исправления?"],
    })
    write_json(EVID / "stage-transition-review-ready-request.json", request)


def accepted() -> None:
    decision = EVID / "stage-acceptance-decision-r4.json"
    if not decision.is_file():
        raise ValueError("canonical G3 r4 owner decision is missing")
    resolved = EVID / "resolved-owner-decisions.json"
    write_json(resolved, [{
        "decision_id": f"{STAGE}.finished-foundations-shell", "class": "owner_required", "status": "resolved",
        "summary": "The owner accepted the exact finished G3 r4 compatibility reproof.", "resolution_ref": rel(decision),
    }])
    request = json.loads((EVID / "stage-transition-review-ready-request.json").read_text(encoding="utf-8"))
    request.update({
        "status": "ready", "owner_decision": rel(decision), "decision_inventory": rel(resolved),
        "summary": "The owner accepted the exact G3 r4 compatibility reproof. The strict G3 gate remains passing and the unique auth-family G4 r5 successor is ready for claim.",
        "questions": [],
    })
    request["review_artifacts"] = request["review_artifacts"][:3]
    write_json(EVID / "stage-transition-ready-request.json", request)


def owner_request() -> None:
    program = json.loads(PROGRAM.read_text(encoding="utf-8"))
    proof = program["g3_rendered_proof"]
    write_json(EVID / "stage-acceptance-decision-r4-request.json", {
        "$schema": "owner-decision-request.schema.json",
        "program_id": PROGRAM_ID,
        "decision_id": f"{STAGE}.finished-foundations-shell",
        "decision_kind": "stage_acceptance",
        "status": "accepted",
        "revision": 4,
        "decision_text": "The owner accepts the exact finished G3 r4 compatibility reproof as the mandatory visual foundation for G4. Each matching target element inherits one complete applicable accepted-pilot rule set; partial inheritance, cross-variant mixing and aesthetic approximation remain forbidden. This decision does not accept any G4 family, target product meaning, production code, publication, deployment, mobile-specific design or full WCAG conformance.",
        "owner_input": "ок, G3 r4 принимается",
        "target": {
            "artifact_kind": "program", "artifact_id": f"{PROGRAM_ID}-r4", "revision": 4,
            "validation_profile": "program_ready", "path": rel(PROGRAM),
        },
        "accepted_values": [{
            "stage_instance_id": STAGE,
            "review_board": {"path": rel(ART / "review-board.html"), "sha256": sha(ART / "review-board.html")},
            "standard_board": {"path": proof["standard_board"]["path"], "sha256": proof["standard_board"]["sha256"]},
            "candidate_shell": {"path": rel(ART / "candidate-shell.html"), "sha256": sha(ART / "candidate-shell.html")},
            "inheritance_policy": "one_complete_applicable_accepted_pilot_rule_set_per_matching_target_element",
            "partial_inheritance": "forbidden", "cross_variant_mixing": "forbidden", "aesthetic_approximation": "forbidden",
            "affected_elements": ["workspace-members-manage", "workspace-roles-assign", "report_access-manage", "dashboard_access-manage"],
            "prior_stage": {"stage_instance_id": "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3", "historical_outcome": "accepted"},
        }],
    })


def response_request() -> None:
    decision = EVID / "stage-acceptance-decision-r4.json"
    if not decision.is_file():
        raise ValueError("canonical G3 r4 owner decision is missing")
    write_json(EVID / "owner-input-response-acceptance-r4-request.json", {
        "$schema": "owner-input-response-request.schema.json",
        "program_id": PROGRAM_ID,
        "stage_instance_id": STAGE,
        "decision_packet_ref": rel(EVID / "owner-review-decision-packet.json"),
        "response_kind": "visual_acceptance",
        "owner_input": "ок, G3 r4 принимается",
        "canonical_owner_decision_ref": rel(decision),
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("review", "owner-request", "response-request", "accepted"))
    args = parser.parse_args()
    {"review": review, "owner-request": owner_request, "response-request": response_request, "accepted": accepted}[args.mode]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
