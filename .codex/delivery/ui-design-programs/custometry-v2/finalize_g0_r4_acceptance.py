#!/usr/bin/env python3
"""Finalize the accepted G0 r4 baseline, intake, indexes, and live program."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any


PROGRAM_REL = ".codex/delivery/ui-design-programs/custometry-v2"
ARTIFACT_REL = f"{PROGRAM_REL}/artifacts/g0-r4"
EVIDENCE_REL = f"{PROGRAM_REL}/evidence/g0-r4"
BASELINE_REL = f"{ARTIFACT_REL}/platform-ui-baseline.json"
INTAKE_REL = f"{ARTIFACT_REL}/ui-program-intake.json"
PROGRAM_DOC_REL = f"{PROGRAM_REL}/ui-design-program.json"
PROGRAM_SNAPSHOT_REL = f"{ARTIFACT_REL}/ui-design-program.snapshot.json"
OWNER_DECISION_REL = f"{EVIDENCE_REL}/visual-authority-decision-r4.json"
G0_R2_SNAPSHOT_REL = f"{PROGRAM_REL}/artifacts/g0-r2/ui-design-program.snapshot.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(root: Path, relative: str) -> Any:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def build_index(root: Path, kind: str, values: list[dict[str, Any]], singular: str) -> dict[str, str]:
    entries = []
    for value in sorted(values, key=lambda item: item[f"{singular}_id"]):
        identity = value[f"{singular}_id"]
        target_rel = f"{ARTIFACT_REL}/{kind}/{identity}.json"
        write_json(root / target_rel, {singular: value})
        entries.append({
            "id": identity,
            "path": target_rel,
            "sha256": sha256(root / target_rel),
            "json_pointer": f"/{singular}",
        })
    index_rel = f"{ARTIFACT_REL}/{kind}-index.json"
    write_json(root / index_rel, {
        "$schema": "program-artifact-index.schema.json",
        "schema_id": "codex.ui-program-artifact-index/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "program_revision": 4,
        "index_kind": kind,
        "entries": entries,
    })
    return {"path": index_rel, "sha256": sha256(root / index_rel)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.project_root.resolve()

    owner = load(root, OWNER_DECISION_REL)
    if (
        owner.get("schema_id") != "codex.ui-owner-decision/v1"
        or owner.get("decision_kind") != "visual_authority"
        or owner.get("decision", {}).get("status") != "accepted"
    ):
        raise ValueError("G0 r4 owner decision is not an accepted canonical visual-authority decision")
    payloads = [
        value for value in owner.get("decision", {}).get("accepted_values", [])
        if isinstance(value, dict) and {"source_visual", "visual_authority", "baseline", "standard"}.issubset(value)
    ]
    if len(payloads) != 1:
        raise ValueError("G0 r4 owner decision must contain one exact accepted authority payload")

    baseline = load(root, BASELINE_REL)
    if baseline.get("revision") != 4 or baseline.get("baseline_id") != payloads[0]["baseline"]["baseline_id"]:
        raise ValueError("G0 r4 baseline identity mismatch")
    if baseline.get("standard_contract", {}).get("clause_inventory_sha256") != payloads[0]["standard"]["clause_inventory_sha256"]:
        raise ValueError("G0 r4 standard clause inventory mismatch")
    baseline["status"] = "accepted"
    baseline["source_visual"]["owner_decision_ref"] = OWNER_DECISION_REL
    write_json(root / BASELINE_REL, baseline)

    intake = load(root, INTAKE_REL)
    if intake.get("revision") != 4:
        raise ValueError("G0 r4 intake revision mismatch")
    intake["intake_id"] = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2.intake.v4"
    intake["status"] = "complete"
    intake["pilot"]["owner_decision_ref"] = OWNER_DECISION_REL
    for theme in intake["themes"]:
        theme["source_refs"] = [f"{intake['pilot']['source_visual_ref']}#accepted-visual-language"]
    intake["baseline_contract"] = {
        "baseline_id": baseline["baseline_id"],
        "path": BASELINE_REL,
        "sha256": sha256(root / BASELINE_REL),
    }
    intake["accepted_decisions"] = [{
        "path": ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/visual-authority-decision-v2.json",
        "sha256": sha256(root / ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/visual-authority-decision-v2.json"),
    }]
    owner_source = {
        "path": OWNER_DECISION_REL,
        "sha256": sha256(root / OWNER_DECISION_REL),
        "authority": "accepted revision-4 visual authority, complete inheritance policy, exact baseline/standard, and corrected auth boundary",
        "covers": ["product", "screens", "states", "themes", "assets"],
    }
    legacy_owner_rel = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/visual-authority-decision-v2.json"
    legacy_owner_source = {
        "path": legacy_owner_rel,
        "sha256": sha256(root / legacy_owner_rel),
        "authority": "accepted product scope, critical journeys, historical exclusions, locales, and revision-2 reconciliation authority retained as current semantic input",
        "covers": ["product", "journeys", "screens", "roles", "permissions", "states", "copy", "locales", "themes"],
    }
    intake["source_contracts"] = [owner_source, legacy_owner_source] + [
        source for source in intake["source_contracts"]
        if source.get("path") not in {OWNER_DECISION_REL, legacy_owner_rel}
    ]
    for screen in intake["screens"]:
        if screen["screen_id"] not in {"UI-AUTH-001", "UI-AUTH-004"}:
            continue
        for action in screen["actions"]:
            action["component_id"] = "action.button"
            if action.get("navigation_target") == "/auth/recovery":
                action["navigation_target"] = "UI-AUTH-004"
            elif action.get("navigation_target") == "/auth/sign-in":
                action["navigation_target"] = "UI-AUTH-001"
    write_json(root / INTAKE_REL, intake)

    indexes = {
        "screens": build_index(root, "screens", intake["screens"], "screen"),
        "journeys": build_index(root, "journeys", intake["journeys"], "journey"),
        "families": build_index(root, "families", [], "family"),
        "waves": build_index(root, "waves", [], "wave"),
    }

    program = load(root, G0_R2_SNAPSHOT_REL)
    program["contract_profile"] = "codex.ui-design-program/v1@2.0.0"
    program["revision"] = 4
    program["status"] = "draft"
    program["validation_profile"] = "draft"
    program["input_contracts"] = {
        "intake": {"path": INTAKE_REL, "sha256": sha256(root / INTAKE_REL)},
        "baseline": {"path": BASELINE_REL, "sha256": sha256(root / BASELINE_REL)},
    }
    program["artifact_indexes"] = indexes
    program["visual_authority"] = {
        "source_visual_ref": intake["pilot"]["source_visual_ref"],
        "source_visual_sha256": intake["pilot"]["source_visual_sha256"],
        "source_evidence_mode": intake["pilot"]["source_evidence_mode"],
        "owner_decision_ref": OWNER_DECISION_REL,
        "screen_acceptance_scope": intake["pilot"]["screen_acceptance_scope"],
        "visual_language_scope": intake["pilot"]["visual_language_scope"],
        "reusable_foundation_scope": intake["pilot"]["reusable_foundation_scope"],
        "inheritance_policy": "required",
        "mobile_scope": "unauthorized",
        "product_semantics_scope": "source_registry_only",
    }
    program["scope"]["origin"] = {
        "kind": "product_contract",
        "ref": f"{OWNER_DECISION_REL}#/decision/accepted_values/0/auth_boundary",
    }
    program["screens"] = []
    program["journeys"] = []
    program["families"] = []
    program["waves"] = []
    program["foundation_inheritance"] = []
    program["source_contracts"] = [{
        "path": OWNER_DECISION_REL,
        "authority": "accepted revision-4 visual authority, complete inheritance policy, exact baseline/standard, and corrected auth boundary",
        "required_status": None,
        "sha256": sha256(root / OWNER_DECISION_REL),
        "screen_collections": [],
        "journey_collections": [],
    }] + [
        source for source in program["source_contracts"]
        if source.get("path") != OWNER_DECISION_REL
        and source.get("authority") != "deterministic G2 normalization of accepted G0 transition contracts"
    ]
    write_json(root / PROGRAM_DOC_REL, program)
    write_json(root / PROGRAM_SNAPSHOT_REL, program)
    print(json.dumps({
        "status": "passed",
        "program_revision": 4,
        "screens": len(intake["screens"]),
        "journeys": len(intake["journeys"]),
        "baseline_sha256": sha256(root / BASELINE_REL),
        "intake_sha256": sha256(root / INTAKE_REL),
        "program_sha256": sha256(root / PROGRAM_DOC_REL),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
