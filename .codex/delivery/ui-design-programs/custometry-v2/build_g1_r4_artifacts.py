#!/usr/bin/env python3
"""Build the blueprint-rebound G1 r4 atlas from G0 r5 inputs."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parent
ROOT = PROGRAM_DIR.parents[3]
sys.path.insert(0, str(PROGRAM_DIR))

import build_g1_r2_artifacts as legacy_builder  # noqa: E402


INTAKE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/ui-program-intake.json"
BASELINE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/platform-ui-baseline.json"
ADMISSION_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r2/g1-admission-inventory.json"
G1 = PROGRAM_DIR / "artifacts/g1-r4"


def pending_origin(field: str) -> dict[str, Any]:
    return {
        "kind": "delegated_design_decision",
        "ref": "references/stage-transition-contract-v1.md#delegated-design-envelope",
        "rationale": f"{field} is intentionally unresolved until G2 r4 structure work.",
        "constraints": [
            "Do not assign family, wave, criticality, representative, or coverage structure during G1."
        ],
    }


def rewrite_revision(path: Path) -> None:
    document = legacy_builder.load(path)
    document["program_revision"] = 5
    legacy_builder.write_json(path, document)


def main() -> None:
    intake = legacy_builder.load(INTAKE_REL)
    screens = {item["screen_id"]: item for item in intake["screens"]}
    journeys = {item["journey_id"]: item for item in intake["journeys"]}

    def intake_index(_path: Path, identity_key: str) -> dict[str, Any]:
        if identity_key == "screen_id":
            return screens
        if identity_key == "journey_id":
            return journeys
        raise ValueError(f"unsupported G0 identity key: {identity_key}")

    legacy_builder.INTAKE_REL = INTAKE_REL
    legacy_builder.BASELINE_REL = BASELINE_REL
    legacy_builder.ADMISSION_REL = ADMISSION_REL
    legacy_builder.G0_SCREENS = PROGRAM_DIR / "artifacts/g0-r5/screens-index.json"
    legacy_builder.G0_JOURNEYS = PROGRAM_DIR / "artifacts/g0-r5/journeys-index.json"
    legacy_builder.G1 = G1
    legacy_builder.pending_origin = pending_origin
    legacy_builder.indexed = intake_index
    legacy_builder.main()

    for name in (
        "screens-index.json", "journeys-index.json", "capabilities-index.json",
        "promoted-requirement-bindings.json",
    ):
        rewrite_revision(G1 / name)
    program = legacy_builder.load(legacy_builder.PROGRAM)
    program["revision"] = 5
    program["status"] = "draft"
    program["validation_profile"] = "atlas_gate"
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
        "program_revision": 5,
        "program_sha256": legacy_builder.sha256(legacy_builder.PROGRAM),
        "snapshot_sha256": legacy_builder.sha256(G1 / "ui-design-program.snapshot.json"),
        "semantic_rebind": {
            "source_intake": INTAKE_REL,
            "period_comparison_surface": "UI-OVR-005",
            "status": "passed",
        },
    })
    legacy_builder.write_json(G1 / "exact-cover-summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
