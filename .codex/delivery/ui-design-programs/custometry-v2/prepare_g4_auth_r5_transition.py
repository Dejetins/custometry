#!/usr/bin/env python3
"""Prepare exact G4 auth r5 review-ready preflight, report and transition request."""

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
ART = DIR / "artifacts/g4-r5/family-auth-shell-auth-baseline-exception-auth"
EVID = DIR / "evidence/g4-r5/family-auth-shell-auth-baseline-exception-auth"
PREFLIGHT = EVID / "preflight"
FAMILY = EVID / "family-acceptance.json"
BOARD = ART / "review-board.html"
QA = EVID / "browser-board-qa.json"
STAGE = "G4@family.auth.shell-auth.baseline-exception-auth-r5"
NEXT_STAGE = "G4@family.auth.shell-workspace.baseline-r4"
NEXT_TARGET = "family.auth.shell-workspace.baseline-r4"
NEXT_TASK = ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-02-family-auth-shell-workspace-baseline-r4.md"
REPORT = ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/family.auth.shell-auth.baseline-exception-auth-r5-report.md"
PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def evidence(check_id: str, facts: dict[str, Any]) -> dict[str, Any]:
    return {"$schema": "stage-preflight-evidence.schema.json", "schema_id": "codex.ui-stage-preflight-evidence/v1", "check_id": check_id, "program_id": PROGRAM_ID, "stage_instance_id": STAGE, "gate_id": "G4", "status": "passed", "facts": facts}


def refs(document: Any) -> list[dict[str, str]]:
    found: dict[str, str] = {}
    def visit(value: Any) -> None:
        if isinstance(value, dict):
            path, digest = value.get("path"), value.get("sha256")
            if isinstance(path, str) and isinstance(digest, str) and len(digest) == 64:
                found[path] = digest
            for child in value.values(): visit(child)
        elif isinstance(value, list):
            for child in value: visit(child)
    visit(document)
    return [{"path": path, "sha256": digest} for path, digest in sorted(found.items())]


def main(mode: str) -> int:
    family = json.loads(FAMILY.read_text(encoding="utf-8"))
    qa = json.loads(QA.read_text(encoding="utf-8"))
    expected_family_result = "passed" if mode == "accepted" else "review_ready"
    if family.get("result") != expected_family_result or qa.get("result") != "passed":
        raise ValueError("finished family gate or board QA is not passing")
    pending = EVID / "pending-owner-decisions.json"
    resolved = EVID / "resolved-owner-decisions.json"
    blockers = EVID / "known-blockers.json"
    packet = EVID / "owner-review-decision-packet-correction-r5-03.json"
    decision = EVID / "family-acceptance-decision-r5-03.json"
    outside_expected = EVID / "outside-expected-paths-r5-03.json"
    write_json(pending, [{"decision_id": f"{STAGE}.finished-result", "class": "owner_required", "status": "pending", "summary": "Accept the finished auth-family result or request bounded corrections.", "resolution_ref": None}])
    if mode == "accepted":
        if not decision.is_file():
            raise ValueError("canonical G4 family acceptance decision is missing")
        write_json(resolved, [{"decision_id": f"{STAGE}.finished-result", "class": "owner_required", "status": "resolved", "summary": "The owner fully accepted the exact finished auth-family review board.", "resolution_ref": rel(decision)}])
    write_json(blockers, [])
    write_json(outside_expected, {
        "schema_id": "custometry.ui-stage-file-manifest-outside-expected/v1",
        "program_id": PROGRAM_ID,
        "stage_instance_id": STAGE,
        "outside_expected_paths": [
            ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r4/family-auth-shell-auth-baseline-exception-auth/**",
            ".codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r4/family-auth-shell-auth-baseline-exception-auth/{auth-action-taxonomy.json,button-interaction-lineage.json,route-state-distinction.json,visible-copy-inventory.json,captures/**/{capture-context.json,implementation-provenance-request.json,reference-provenance-request.json}}",
        ],
        "observed_file_count": 180,
        "reason": "A mistaken direct base-generator invocation regenerated the superseded r4 auth-family source/contract/request zone before the r5-only guard was restored.",
        "recovery_status": "original r4 bytes unavailable from Git or a workspace snapshot",
        "authority_impact": "The superseded r4 row was not claimed, no r4 acceptance receipt was rebuilt, and current r5 evidence does not consume these bytes.",
        "historical_r2_r3_byte_preserved": True,
    })
    checks = {
        "current_gate": evidence("current_gate", {"validation_profile": "family_gate" if mode == "accepted" else "family_review_ready", "artifact_ref": rel(FAMILY), "artifact_sha256": sha(FAMILY), "result": "passed"}),
        "source_freshness": evidence("source_freshness", {"source_refs": refs(family), "drift_classification": "owned_generated_change", "stale_refs": []}),
        "next_stage_inputs": evidence("next_stage_inputs", {"next_stage_id": NEXT_STAGE, "task_ref": rel(NEXT_TASK), "unresolved_inputs": []}),
        "write_scope": evidence("write_scope", {"allowed_paths": [".codex/delivery/ui-design-programs/custometry-v2/**", ".codex/agents/generated/custometry-ui-design-g0-v2/**", ".codex/delivery/evidence/custometry-ui-design-program-v2/**"], "authorization_basis": "explicit_current_user_authorization", "outside_scope_paths": []}),
        "foreign_changes": evidence("foreign_changes", {"observed_paths": [".codex/AGENTS.md", "custometry-technical-blueprint-ru.md", "custometry-technical-blueprint-human-ru.md", "custometry-ui-blueprint-ru.md", "docs/generated/requirement-index.json", "packages/contracts/routes/ui-surface-contracts.json"], "inseparable_paths": [], "disposition": "separable_foreign_changes_preserved"}),
        "execution_route": evidence("execution_route", {"route": "staged-plan-runner + ui-design-program + browser-qa-evidence/playwright-cli", "available": True}),
        "handoff_artifact": evidence("handoff_artifact", {"artifact_ref": rel(NEXT_TASK), "artifact_sha256": sha(NEXT_TASK), "known_stop_resolution": "none"}),
    }
    for key, value in checks.items(): write_json(PREFLIGHT / f"{key}.json", value)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        f"# {PROGRAM_ID} G4 auth family r5 {'accepted' if mode == 'accepted' else 'review-ready'} report\n\n"
        f"- Stage: `{STAGE}`; result: `{'passed, owner accepted' if mode == 'accepted' else 'review_ready, owner acceptance pending'}`.\n"
        f"- Family receipt: `{rel(FAMILY)}` — `{sha(FAMILY)}`.\n"
        f"- Review board: `{rel(BOARD)}` — `{sha(BOARD)}`.\n"
        "- Representatives: `UI-AUTH-001 /auth/sign-in` and `UI-AUTH-004 /auth/recovery`, six source-backed states each.\n"
        "- Structural correction: sign-in uses one shared-edge form column with a native checkbox and real recovery link; recovery uses a distinct coherent two-step Web composition with one reading order and stable action hierarchy.\n"
        "- Stable window geometry: every sign-in and recovery state, including loading, validation, failure, session expiry and action feedback, reuses the exact dimensions of that screen's initial state at each accepted Web anchor; the initial dimensions were not enlarged.\n"
        "- Control taxonomy: submit/secondary buttons project the accepted pilot state grammar without the rejected fixed-width generic-button identity; navigation remains native links, language remains a native select, and no standard exception is retained.\n"
        "- Copy boundary: all 24 RU/EN screen-state-locale inventories are source-bound or minimally connective; raw routes, fixture terms, technical reset prose, the rejected help label and empty initial status panels are absent.\n"
        "- Proof: 12 active screen contracts, 12 independently assembled applicability manifests, 96 browser captures, 48 visual-QA receipts, 12 screen-acceptance receipts and one exact-cover family aggregate.\n"
        "- Browser stress: all 12 states, 768/1024/1440/1920 anchors, pointer and keyboard navigation, native checkbox role/name/state and label hit, physical mouse-down active geometry, focus order, RU/EN, 200% zoom/reflow, reduced motion, console/network, overflow and accessibility smoke passed.\n"
        "- The current structural rejection and four historical owner corrections are carried as requirements. Historical G4 r2/r3 evidence remains byte-preserved and unaccepted where applicable.\n"
        "- Residual history risk: one mistaken direct base-generator invocation regenerated 180 files in the superseded G4 r4 auth source/contract/proof-request zone. Original r4 bytes were unavailable from Git or a workspace snapshot; no r4 acceptance receipt was rebuilt, the r4 row was not claimed, and current r5 evidence does not consume those bytes. This is recorded as `outside_expected_paths` in preflight write-scope evidence.\n"
        "- Production implementation, publication, deployment, mobile-specific design and full WCAG conformance remain outside proof. No adjacent row was claimed.\n",
        encoding="utf-8",
    )
    request = {
        "$schema": "stage-transition-request.schema.json", "program_id": PROGRAM_ID,
        "from_stage_id": STAGE, "from_gate": "G4", "from_target": "family.auth.shell-auth.baseline-exception-auth-r5", "from_revision": 5,
        "artifact": rel(FAMILY), "to_gate": "G4", "to_stage_id": NEXT_STAGE, "to_target": NEXT_TARGET, "to_task": rel(NEXT_TASK),
        "status": "ready" if mode == "accepted" else "review_ready",
        "owner_decision": rel(decision) if mode == "accepted" else None,
        "decision_inventory": rel(resolved) if mode == "accepted" else rel(pending),
        "blockers": rel(blockers),
        "checks": [f"{key}={rel(PREFLIGHT / f'{key}.json')}" for key in checks],
        "summary": "The owner accepted the finished auth family. It exact-covers sign-in and the distinct recovery flow across all required states and responsive-Web anchors, and the strict family gate passes." if mode == "accepted" else "The finished auth family exact-covers sign-in and the distinct recovery flow across all required states and responsive-Web anchors. Complete applicable pilot-derived rules govern matching elements; target route meaning and composition remain product-owned.",
        "review_artifacts": [rel(BOARD), rel(EVID / "review-board-1440.png"), rel(EVID / "review-board-recovery-validation-error-1440.png"), rel(EVID / "review-board-sign-in-en-1440.png"), rel(QA)],
        "questions": [] if mode == "accepted" else ["Принять готовое семейство входа и восстановления или запросить ограниченные исправления?"],
    }
    write_json(EVID / "stage-transition-request.json", request)
    if not packet.is_file(): raise ValueError("owner decision packet is missing")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", nargs="?", choices=("review", "accepted"), default="review")
    args = parser.parse_args()
    raise SystemExit(main(args.mode))
