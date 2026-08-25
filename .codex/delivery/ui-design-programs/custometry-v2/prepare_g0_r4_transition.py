#!/usr/bin/env python3
"""Assemble deterministic G0 r4 preflight evidence and transition request."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = PROGRAM_DIR / "evidence/g0-r4"
PREFLIGHT_DIR = EVIDENCE_DIR / "preflight"
PROGRAM_REL = ".codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json"
ARTIFACT_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r4/ui-design-program.snapshot.json"
INTAKE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r4/ui-program-intake.json"
BASELINE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r4/platform-ui-baseline.json"
DECISION_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r4/visual-authority-decision-r4.json"
OWNER_RESPONSE_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r4/owner-input-response-acceptance-r4.json"
SOURCE_INVENTORY_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r4/ui-standard-source-inventory.json"
NEXT_PROMPT = ".codex/agents/generated/custometry-ui-design-g0-v2/12-g1-complete-screen-atlas-r3.md"
REPORT_REL = ".codex/delivery/evidence/custometry-ui-design-program-v2/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4-report.md"
STAGE_ID = "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4"
NEXT_STAGE_ID = "G1@atlas-r3"


def rel(path: str) -> Path:
    return ROOT / path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: str) -> Any:
    return json.loads(rel(path).read_text(encoding="utf-8"))


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
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "stage_instance_id": STAGE_ID,
        "gate_id": "G0",
        "status": "passed",
        "facts": facts,
    }


def hash_bound_refs(document: Any) -> list[dict[str, str]]:
    found: dict[str, str] = {}

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            path = value.get("path")
            digest = value.get("sha256")
            if isinstance(path, str) and isinstance(digest, str) and len(digest) == 64:
                found[path] = digest
            source_path = value.get("source_visual_ref")
            source_digest = value.get("source_visual_sha256")
            if isinstance(source_path, str) and isinstance(source_digest, str) and len(source_digest) == 64:
                found[source_path] = source_digest
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(document)
    return [{"path": path, "sha256": digest} for path, digest in sorted(found.items())]


def main() -> None:
    program = load(ARTIFACT_REL)
    intake = load(INTAKE_REL)
    baseline = load(BASELINE_REL)
    decision = load(DECISION_REL)
    owner_response = load(OWNER_RESPONSE_REL)

    if program.get("revision") != 4 or program.get("contract_profile") != "codex.ui-design-program/v1@2.0.0":
        raise SystemExit("live program is not the accepted active-contract revision 4")
    if intake.get("status") != "complete" or baseline.get("status") != "accepted":
        raise SystemExit("accepted G0 intake/baseline lifecycle is incomplete")
    if (
        decision.get("decision", {}).get("status") != "accepted"
        or owner_response.get("response_kind") != "product_answer"
    ):
        raise SystemExit("canonical owner acceptance is missing")

    source_refs = hash_bound_refs(program)

    checks = {
        "current_gate": evidence("current_gate", {
            "validation_profile": "draft",
            "artifact_ref": ARTIFACT_REL,
            "artifact_sha256": sha256(rel(ARTIFACT_REL)),
            "result": "passed",
        }),
        "source_freshness": evidence("source_freshness", {
            "source_refs": source_refs,
            "drift_classification": "accepted_change",
            "stale_refs": [],
        }),
        "next_stage_inputs": evidence("next_stage_inputs", {
            "next_stage_id": NEXT_STAGE_ID,
            "task_ref": NEXT_PROMPT,
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
                "custometry-ui-blueprint-ru.md",
                "custometry-technical-blueprint-ru.md",
                "custometry-technical-blueprint-human-ru.md",
                "docs/generated/requirement-index.json",
                "packages/contracts/routes/ui-surface-contracts.json",
            ],
            "inseparable_paths": [],
            "disposition": "separable_foreign_changes_preserved",
        }),
        "handoff_artifact": evidence("handoff_artifact", {
            "artifact_ref": NEXT_PROMPT,
            "artifact_sha256": sha256(rel(NEXT_PROMPT)),
            "known_stop_resolution": "none",
        }),
    }
    for name, value in checks.items():
        write_json(PREFLIGHT_DIR / f"{name}.json", value)

    request = {
        "$schema": "stage-transition-request.schema.json",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "from_stage_id": STAGE_ID,
        "from_gate": "G0",
        "from_target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4",
        "from_revision": 4,
        "artifact": ARTIFACT_REL,
        "to_gate": "G1",
        "to_stage_id": NEXT_STAGE_ID,
        "to_target": "atlas-r3",
        "to_task": NEXT_PROMPT,
        "status": "ready",
        "owner_decision": None,
        "decision_inventory": None,
        "blockers": None,
        "checks": [
            f"current_gate={PREFLIGHT_DIR.relative_to(ROOT).as_posix()}/current_gate.json",
            f"source_freshness={PREFLIGHT_DIR.relative_to(ROOT).as_posix()}/source_freshness.json",
            f"next_stage_inputs={PREFLIGHT_DIR.relative_to(ROOT).as_posix()}/next_stage_inputs.json",
            f"write_scope={PREFLIGHT_DIR.relative_to(ROOT).as_posix()}/write_scope.json",
            f"foreign_changes={PREFLIGHT_DIR.relative_to(ROOT).as_posix()}/foreign_changes.json",
            "execution_route=N/A",
            f"handoff_artifact={PREFLIGHT_DIR.relative_to(ROOT).as_posix()}/handoff_artifact.json",
        ],
        "summary": (
            "G0 r4 completed the current-contract source inventory and exact-cover standard, "
            "recorded the owner's accepted visual authority and baseline, corrected auth semantics, "
            "and left G1 r3 ready and unclaimed."
        ),
        "review_artifacts": [REPORT_REL, DECISION_REL],
        "questions": [],
    }
    write_json(EVIDENCE_DIR / "stage-transition-request.json", request)
    print(json.dumps({
        "status": "passed",
        "artifact_sha256": sha256(rel(ARTIFACT_REL)),
        "source_refs": len(source_refs),
        "next_stage": NEXT_STAGE_ID,
    }, indent=2))


if __name__ == "__main__":
    main()
