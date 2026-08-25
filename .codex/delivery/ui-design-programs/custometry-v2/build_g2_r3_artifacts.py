#!/usr/bin/env python3
"""Build active-contract G2 r3 with corrected auth representatives and standard bindings."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PROGRAM_DIR = Path(__file__).resolve().parent
ROOT = PROGRAM_DIR.parents[3]
sys.path.insert(0, str(PROGRAM_DIR))

import build_g2_r2_artifacts as legacy  # noqa: E402

LEGACY_BUILD_FAMILIES = legacy.build_families
LEGACY_BUILD_FOUNDATION_INHERITANCE = legacy.build_foundation_inheritance


G2 = PROGRAM_DIR / "artifacts/g2-r3"
EVIDENCE = PROGRAM_DIR / "evidence/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3"
INTAKE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r4/ui-program-intake.json"
BASELINE_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r4/platform-ui-baseline.json"
G1_BINDINGS_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g1-r3/promoted-requirement-bindings.json"
G3_PROOF_SEED_REL = ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g2-r3/g3-rendered-proof-input-seed.json"
G3_SOURCE_CAPTURE_REL = ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v3-metadata/equivalence/candidate-web-1920-ru-default.png"


def patch_document(path: Path, transform) -> None:
    document = legacy.load(path)
    transform(document)
    legacy.write_json(path, document)


def build_foundation_inheritance(
    families: list[dict[str, Any]],
    screens_by_id: dict[str, dict[str, Any]],
    baseline: dict[str, Any],
    baseline_hash: str,
) -> list[dict[str, Any]]:
    result = LEGACY_BUILD_FOUNDATION_INHERITANCE(families, screens_by_id, baseline, baseline_hash)
    standard = baseline["standard_contract"]
    for item in result:
        item.update({
            "standard_revision_id": standard["standard_revision_id"],
            "clause_inventory_sha256": standard["clause_inventory_sha256"],
            "applicability_policy": "deterministic_exact_identity_match_with_typed_exceptions",
        })
    return result


def build_families(screens, intake_by_id):
    families, assignment = LEGACY_BUILD_FAMILIES(screens, intake_by_id)
    auth_family = next(
        (family for family in families if {"UI-AUTH-001", "UI-AUTH-004"}.issubset(family["screen_ids"])),
        None,
    )
    if not isinstance(auth_family, dict):
        raise ValueError("one corrected auth family does not cover UI-AUTH-001 and UI-AUTH-004")
    auth_family["representative_screen_ids"] = ["UI-AUTH-001", "UI-AUTH-004"]
    auth_family["decision_origin"] = legacy.product_ref(
        ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r4/ui-program-intake.json#/screens"
    )
    auth_family["workload_budget"] = {
        "max_screens": len(auth_family["screen_ids"]),
        "max_screen_state_pairs": sum(
            len(legacy.screen_state_ids(intake_by_id[screen_id][1]))
            for screen_id in auth_family["screen_ids"]
        ),
        "rationale": "One auth-shell family with distinct sign-in and recovery representatives; shared grammar does not imply identical composition.",
    }
    return families, assignment


def main() -> None:
    legacy.G2 = G2
    legacy.EVIDENCE = EVIDENCE
    legacy.INTAKE_REL = INTAKE_REL
    legacy.BASELINE_REL = BASELINE_REL
    legacy.BASELINE_PATH = BASELINE_REL
    legacy.G1_BINDINGS_REL = G1_BINDINGS_REL
    legacy.G3_PROOF_SEED_REL = G3_PROOF_SEED_REL
    legacy.G3_SOURCE_CAPTURE_REL = G3_SOURCE_CAPTURE_REL
    legacy.build_families = build_families
    legacy.build_foundation_inheritance = build_foundation_inheritance
    legacy.main()

    def replace_paths(value: Any) -> Any:
        if isinstance(value, str):
            return value.replace("/artifacts/g2-r2/", "/artifacts/g2-r3/")
        if isinstance(value, list):
            return [replace_paths(item) for item in value]
        if isinstance(value, dict):
            return {key: replace_paths(item) for key, item in value.items()}
        return value

    for shard in sorted((G2 / "journeys").glob("*.json")):
        legacy.write_json(shard, replace_paths(legacy.load(shard)))
    journey_index = legacy.load(G2 / "journeys-index.json")
    for entry in journey_index["entries"]:
        entry["sha256"] = legacy.sha256(ROOT / entry["path"])
    legacy.write_json(G2 / "journeys-index.json", journey_index)

    for path in [
        G2 / "screens-index.json",
        G2 / "journeys-index.json",
        G2 / "families-index.json",
        G2 / "waves-index.json",
        G2 / "coverage-profiles.json",
        G2 / "promoted-structure-bindings.json",
        ROOT / G3_PROOF_SEED_REL,
    ]:
        patch_document(path, lambda document: document.update({"program_revision": 4}))

    program = legacy.load(legacy.PROGRAM)
    program["revision"] = 4
    program["journeys"] = replace_paths(program["journeys"])
    for source in program["source_contracts"]:
        if "/artifacts/g2-r3/journeys/" in source.get("path", ""):
            source["sha256"] = legacy.sha256(ROOT / source["path"])
    program["artifact_indexes"] = {
        kind: legacy.evidence_ref(G2 / f"{kind}-index.json")
        for kind in ("screens", "journeys", "families", "waves")
    }
    proof_seed_ref = legacy.evidence_ref(ROOT / G3_PROOF_SEED_REL)
    program["g3_rendered_proof"]["review_board"] = proof_seed_ref
    program["g3_rendered_proof"]["inheritance_report"] = proof_seed_ref
    auth_family = next(f for f in program["families"] if {"UI-AUTH-001", "UI-AUTH-004"}.issubset(f["screen_ids"]))
    if auth_family["representative_screen_ids"] != ["UI-AUTH-001", "UI-AUTH-004"]:
        raise ValueError("auth representative invariant regressed")
    for screen in program["screens"]:
        screen_id = screen["screen_ref"]["expected_id"]
        if screen_id in {"UI-AUTH-001", "UI-AUTH-004"}:
            screen["representative"] = True
    legacy.write_json(legacy.PROGRAM, program)
    legacy.write_json(G2 / "ui-design-program.snapshot.json", program)

    summary_path = EVIDENCE / "structure-exact-cover-evidence.json"
    summary = legacy.load(summary_path)
    summary.update({
        "program_revision": 4,
        "stage_instance_id": "G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3",
        "auth_family_invariant": {
            "family_id": auth_family["family_id"],
            "representative_screen_ids": ["UI-AUTH-001", "UI-AUTH-004"],
            "routes": {"UI-AUTH-001": "/auth/sign-in", "UI-AUTH-004": "/auth/recovery"},
            "distinct_composition_required": True,
            "status": "passed",
        },
        "program_snapshot": legacy.evidence_ref(G2 / "ui-design-program.snapshot.json"),
    })
    summary["counts"]["representatives"] = sum(len(f["representative_screen_ids"]) for f in program["families"])
    summary["checks"]["representatives_exact_cover_families"] = all(
        family["representative_screen_ids"]
        and set(family["representative_screen_ids"]).issubset(family["screen_ids"])
        for family in program["families"]
    )
    legacy.write_json(summary_path, summary)
    legacy.write_json(G2 / "structure-summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
