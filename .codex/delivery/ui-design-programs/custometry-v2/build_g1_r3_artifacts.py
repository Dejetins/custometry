#!/usr/bin/env python3
"""Build the active-contract G1 r3 atlas from the accepted G0 r4 inputs."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parent
ROOT = PROGRAM_DIR.parents[3]
sys.path.insert(0, str(PROGRAM_DIR))

import build_g1_r2_artifacts as legacy_builder  # noqa: E402


INTAKE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r4/ui-program-intake.json"
BASELINE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r4/platform-ui-baseline.json"
ADMISSION_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/g1-admission-inventory.json"
G1 = PROGRAM_DIR / "artifacts/g1-r3"


def ordered_journey_screens(journey: dict[str, Any]) -> list[str]:
    ordered: list[str] = []
    for screen_id in journey.get("entry_screen_ids", []):
        if screen_id not in ordered:
            ordered.append(screen_id)
    for transition in journey.get("transitions", []):
        for key in ("from_screen_id", "to_screen_id"):
            screen_id = transition.get(key)
            if isinstance(screen_id, str) and screen_id not in ordered:
                ordered.append(screen_id)
    for screen_id in journey.get("terminal_screen_ids", []):
        if screen_id not in ordered:
            ordered.append(screen_id)
    return ordered


def build_admission(intake: dict[str, Any]) -> None:
    screens = []
    for index, screen in enumerate(intake["screens"]):
        source_ref = next((ref for ref in screen.get("source_refs", []) if "#" in ref), f"{INTAKE_REL}#/screens/{index}")
        source_path, _, source_pointer = source_ref.partition("#")
        screens.append({
            "screen_id": screen["screen_id"],
            "classification": screen["surface_kind"],
            "source_path": source_path,
            "source_pointer": source_pointer or f"/screens/{index}",
        })
    journeys = [{
        "journey_id": journey["journey_id"],
        "screen_ids": ordered_journey_screens(journey),
    } for journey in intake["journeys"]]
    legacy_builder.write_json(ROOT / ADMISSION_REL, {
        "schema_id": "custometry.ui-g1-admission-inventory/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "program_revision": 4,
        "source_intake": {"path": INTAKE_REL, "sha256": legacy_builder.sha256(ROOT / INTAKE_REL)},
        "screens": screens,
        "journeys": journeys,
    })


def pending_origin(field: str) -> dict[str, Any]:
    return {
        "kind": "delegated_design_decision",
        "ref": "references/stage-transition-contract-v1.md#delegated-design-envelope",
        "rationale": f"{field} is intentionally unresolved until G2 r3 structure work.",
        "constraints": [
            "Do not assign family, wave, criticality, representative, or coverage structure during G1."
        ],
    }


def rewrite_revision(path: Path) -> None:
    document = legacy_builder.load(path)
    document["program_revision"] = 4
    legacy_builder.write_json(path, document)


def main() -> None:
    intake = legacy_builder.load(INTAKE_REL)
    auth = {item["screen_id"]: item for item in intake["screens"] if item["screen_id"] in {"UI-AUTH-001", "UI-AUTH-004"}}
    if set(auth) != {"UI-AUTH-001", "UI-AUTH-004"}:
        raise SystemExit("corrected auth representatives are missing")
    if auth["UI-AUTH-001"].get("route") != "/auth/sign-in" or auth["UI-AUTH-004"].get("route") != "/auth/recovery":
        raise SystemExit("sign-in/recovery route identity regressed")
    state_ids = {state["state_id"] for item in auth.values() for state in item.get("states", [])}
    if "UI-AUTH-001.recovery" in state_ids:
        raise SystemExit("invented UI-AUTH-001.recovery state regressed")

    legacy_builder.INTAKE_REL = INTAKE_REL
    legacy_builder.BASELINE_REL = BASELINE_REL
    legacy_builder.ADMISSION_REL = ADMISSION_REL
    legacy_builder.G0_SCREENS = PROGRAM_DIR / "artifacts/g0-r4/screens-index.json"
    legacy_builder.G0_JOURNEYS = PROGRAM_DIR / "artifacts/g0-r4/journeys-index.json"
    legacy_builder.G1 = G1
    legacy_builder.pending_origin = pending_origin
    legacy_builder.main()

    for name in ("screens-index.json", "journeys-index.json", "capabilities-index.json", "promoted-requirement-bindings.json"):
        rewrite_revision(G1 / name)
    program = legacy_builder.load(legacy_builder.PROGRAM)
    program["revision"] = 4
    program["artifact_indexes"]["screens"] = {
        "path": (G1 / "screens-index.json").relative_to(ROOT).as_posix(),
        "sha256": legacy_builder.sha256(G1 / "screens-index.json"),
    }
    program["artifact_indexes"]["journeys"] = {
        "path": (G1 / "journeys-index.json").relative_to(ROOT).as_posix(),
        "sha256": legacy_builder.sha256(G1 / "journeys-index.json"),
    }
    legacy_builder.write_json(legacy_builder.PROGRAM, program)
    legacy_builder.write_json(G1 / "ui-design-program.snapshot.json", program)
    summary = legacy_builder.load(G1 / "exact-cover-summary.json")
    summary.update({
        "program_revision": 4,
        "program_sha256": legacy_builder.sha256(legacy_builder.PROGRAM),
        "snapshot_sha256": legacy_builder.sha256(G1 / "ui-design-program.snapshot.json"),
        "auth_route_invariant": {
            "UI-AUTH-001": "/auth/sign-in",
            "UI-AUTH-004": "/auth/recovery",
            "forbidden_state": "UI-AUTH-001.recovery",
            "status": "passed",
        },
    })
    legacy_builder.write_json(G1 / "exact-cover-summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
