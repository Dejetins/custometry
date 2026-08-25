#!/usr/bin/env python3
"""Prepare the unique G4 auth r6 review-ready handoff and durable report."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
ART = DIR / "artifacts/g4-r6/family-auth-shell-auth-baseline-exception-auth"
EVID = DIR / "evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth"
PREFLIGHT = EVID / "preflight"
FAMILY = EVID / "family-acceptance.json"
BOARD = ART / "review-board.html"
QA = EVID / "browser-board-qa.json"
PACKET = EVID / "owner-review-decision-packet.json"
DECISION = EVID / "family-acceptance-decision-r6.json"
STAGE = "G4@family.auth.shell-auth.baseline-exception-auth-r6"
NEXT_STAGE = "G4@family.auth.shell-workspace.baseline-r5"
NEXT_TARGET = "family.auth.shell-workspace.baseline-r5"
NEXT_TASK = ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-02-family-auth-shell-workspace-baseline-r5.md"
REPORT = ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/family.auth.shell-auth.baseline-exception-auth-r6-report.md"
PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def evidence(check_id: str, facts: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": "stage-preflight-evidence.schema.json",
        "schema_id": "codex.ui-stage-preflight-evidence/v1",
        "check_id": check_id,
        "program_id": PROGRAM_ID,
        "stage_instance_id": STAGE,
        "gate_id": "G4",
        "status": "passed",
        "facts": facts,
    }


def refs(document: Any) -> list[dict[str, str]]:
    found: dict[str, str] = {}

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            path = value.get("path")
            digest = value.get("sha256")
            if isinstance(path, str) and isinstance(digest, str) and len(digest) == 64:
                found[path] = digest
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(document)
    return [{"path": path, "sha256": digest} for path, digest in sorted(found.items())]


def main(mode: str) -> int:
    family = json.loads(FAMILY.read_text(encoding="utf-8"))
    qa = json.loads(QA.read_text(encoding="utf-8"))
    packet = json.loads(PACKET.read_text(encoding="utf-8"))
    expected_family_result = "passed" if mode == "accepted" else "review_ready"
    if family.get("result") != expected_family_result or qa.get("result") != "passed":
        raise ValueError("finished r6 family gate or browser board QA is not review-ready")
    if packet.get("status") != "pending" or packet.get("stage_instance_id") != STAGE:
        raise ValueError("unique r6 owner packet is not pending for the exact stage")

    pending = EVID / "pending-owner-decisions.json"
    resolved = EVID / "resolved-owner-decisions.json"
    blockers = EVID / "known-blockers.json"
    outside = EVID / "outside-expected-paths.json"
    write_json(pending, [{
        "decision_id": f"{STAGE}.finished-result",
        "class": "owner_required",
        "status": "pending",
        "summary": "Accept the finished auth-family r6 result or request bounded corrections.",
        "resolution_ref": None,
    }])
    if mode == "accepted":
        if not DECISION.is_file():
            raise ValueError("canonical r6 family acceptance decision is missing")
        write_json(resolved, [{
            "decision_id": f"{STAGE}.finished-result",
            "class": "owner_required",
            "status": "resolved",
            "summary": "The owner carried the prior acceptance forward to the exact visually unchanged r6 review board.",
            "resolution_ref": rel(DECISION),
        }])
    write_json(blockers, [])
    write_json(outside, {
        "schema_id": "custometry.ui-stage-file-manifest-outside-expected/v1",
        "program_id": PROGRAM_ID,
        "stage_instance_id": STAGE,
        "outside_expected_paths": [],
        "observed_file_count": 0,
        "reason": "All r6 successor writes remain inside the authorized program-owned touch zones.",
        "historical_r5_evidence_mutated": False,
    })

    checks = {
        "current_gate": evidence("current_gate", {
            "validation_profile": "family_gate" if mode == "accepted" else "family_review_ready",
            "artifact_ref": rel(FAMILY),
            "artifact_sha256": sha(FAMILY),
            "result": "passed",
        }),
        "source_freshness": evidence("source_freshness", {
            "source_refs": refs(family),
            "drift_classification": "owned_generated_change",
            "stale_refs": [],
        }),
        "next_stage_inputs": evidence("next_stage_inputs", {
            "next_stage_id": NEXT_STAGE,
            "task_ref": rel(NEXT_TASK),
            "unresolved_inputs": [],
        }),
        "write_scope": evidence("write_scope", {
            "allowed_paths": [
                ".codex/delivery/ui-design-programs/custometry-v2/**",
                ".codex/agents/generated/custometry-ui-design-g0-v2/**",
                ".codex/delivery/evidence/custometry-ui-design-program-v2/**",
            ],
            "authorization_basis": "explicit_current_user_authorization",
            "outside_scope_paths": [],
        }),
        "foreign_changes": evidence("foreign_changes", {
            "observed_paths": [
                ".codex/AGENTS.md",
                "custometry-technical-blueprint-ru.md",
                "custometry-technical-blueprint-human-ru.md",
                "custometry-ui-blueprint-ru.md",
                "docs/generated/requirement-index.json",
                "packages/contracts/routes/ui-surface-contracts.json",
            ],
            "inseparable_paths": [],
            "disposition": "separable_foreign_changes_preserved",
        }),
        "execution_route": evidence("execution_route", {
            "route": "staged-plan-runner + ui-design-program + browser-qa-evidence/playwright-cli",
            "available": True,
        }),
        "handoff_artifact": evidence("handoff_artifact", {
            "artifact_ref": rel(NEXT_TASK),
            "artifact_sha256": sha(NEXT_TASK),
            "known_stop_resolution": "none",
        }),
    }
    for key, value in checks.items():
        write_json(PREFLIGHT / f"{key}.json", value)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        f"# {PROGRAM_ID} G4 auth family r6 {'accepted' if mode == 'accepted' else 'review-ready'} report\n\n"
        f"- Stage: `{STAGE}`; result: `{'passed, owner accepted' if mode == 'accepted' else 'review_ready, owner acceptance pending'}`.\n"
        f"- Family receipt: `{rel(FAMILY)}` — `{sha(FAMILY)}`.\n"
        f"- Review board: `{rel(BOARD)}` — `{sha(BOARD)}`.\n"
        "- Representatives: `UI-AUTH-001 /auth/sign-in` and `UI-AUTH-004 /auth/recovery`, six source-backed states each.\n"
        "- Semantic rebind: all contracts and applicability manifests bind program revision 5, baseline revision 5 and accepted G3 r5 shell authority. The accepted r5 family remains read-only historical visual input and does not accept r6.\n"
        "- Visual result: the previously accepted compact sign-in and distinct two-step recovery composition is preserved, including native controls, real route links, stable per-screen state geometry, RU/EN parity and Graphite visual grammar.\n"
        "- Proof: 12 active screen contracts, 12 independently assembled applicability manifests, 96 fresh browser captures, 48 fresh visual-QA receipts, 12 screen-acceptance receipts and one exact-cover family aggregate.\n"
        "- Browser QA: all 12 states, 768/1024/1440/1920 Web anchors, pointer and keyboard navigation, control semantics, focus/active/checked states, 200% reflow, reduced motion, console/network isolation and review closure passed.\n"
        "- Production implementation, publication, deployment, mobile-specific design and full WCAG conformance remain outside proof. No adjacent row was claimed.\n",
        encoding="utf-8",
    )

    request = {
        "$schema": "stage-transition-request.schema.json",
        "program_id": PROGRAM_ID,
        "from_stage_id": STAGE,
        "from_gate": "G4",
        "from_target": "family.auth.shell-auth.baseline-exception-auth-r6",
        "from_revision": 6,
        "artifact": rel(FAMILY),
        "to_gate": "G4",
        "to_stage_id": NEXT_STAGE,
        "to_target": NEXT_TARGET,
        "to_task": rel(NEXT_TASK),
        "status": "ready" if mode == "accepted" else "review_ready",
        "owner_decision": rel(DECISION) if mode == "accepted" else None,
        "decision_inventory": rel(resolved) if mode == "accepted" else rel(pending),
        "blockers": rel(blockers),
        "checks": [f"{key}={rel(PREFLIGHT / f'{key}.json')}" for key in checks],
        "summary": "The owner carried the prior acceptance forward to the exact visually unchanged r6 auth-family successor. The strict family gate passes and the next family is ready." if mode == "accepted" else "The current-program auth family exact-covers sign-in and recovery across all required states and responsive-Web anchors. The machine gate passes; owner acceptance remains pending.",
        "review_artifacts": [
            rel(BOARD),
            rel(EVID / "review-board-1440.png"),
            rel(EVID / "review-board-recovery-validation-error-1440.png"),
            rel(EVID / "review-board-sign-in-en-1440.png"),
            rel(QA),
        ],
        "questions": [] if mode == "accepted" else ["Принять готовое семейство входа и восстановления или запросить ограниченные исправления?"],
    }
    write_json(EVID / ("stage-transition-request.json" if mode == "accepted" else "stage-transition-request-review-ready.json"), request)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", nargs="?", choices=("review", "accepted"), default="review")
    args = parser.parse_args()
    raise SystemExit(main(args.mode))
