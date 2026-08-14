#!/usr/bin/env python3
"""Synchronize active contract assets and create the preclaim r3 draft inputs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = ROOT / ".codex/delivery/ui-design-programs/custometry-v2"
SKILL_ASSETS = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program/assets")
G0_R2 = PROGRAM_DIR / "artifacts/g0-r2"
G0_R3 = PROGRAM_DIR / "artifacts/g0-r3"
EVIDENCE = PROGRAM_DIR / "evidence/compatibility-migration-r3"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, *, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if compact:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    else:
        text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    path.write_text(text + "\n", encoding="utf-8")


def main() -> int:
    copied: list[dict[str, str]] = []
    for source in sorted(SKILL_ASSETS.iterdir()):
        if not source.is_file():
            continue
        target = PROGRAM_DIR / source.name
        shutil.copyfile(source, target)
        copied.append(
            {
                "source": str(source),
                "source_sha256": sha256(source),
                "target": str(target.relative_to(ROOT)),
                "target_sha256": sha256(target),
            }
        )
    baseline = json.loads((G0_R2 / "platform-ui-baseline.json").read_text(encoding="utf-8"))
    baseline.update(
        {
            "contract_profile": "codex.platform-ui-baseline/v1@2.0.0",
            "revision": 3,
            "status": "draft",
            "standard_contract": {
                "standard_revision_id": "custometry.platform-baseline.v2.r3.standard.r1",
                "source_inventory": {
                    "inventory_id": "custometry.pilot-standard-source-inventory.r3",
                    "revision": 1,
                    "path": ".codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r3/ui-standard-source-inventory.json",
                    "sha256": "0" * 64,
                },
                "clause_inventory_sha256": "0" * 64,
                "clauses": [],
                "source_dispositions": [],
                "applicability_policy": {
                    "derivation": "deterministic_exact_identity_match",
                    "clause_dispositions": [
                        "conforms", "accepted_exception", "source_backed_not_applicable"
                    ],
                    "exception_policy": "typed_narrow_source_bound_owner_acceptance",
                    "delegated_design_boundary": "screen_specific_composition_only",
                },
            },
        }
    )
    baseline_path = G0_R3 / "platform-ui-baseline.json"
    write_json(baseline_path, baseline, compact=True)
    intake = json.loads((G0_R2 / "ui-program-intake.json").read_text(encoding="utf-8"))
    intake.update(revision=3, status="draft", baseline_contract=baseline)
    intake_path = G0_R3 / "ui-program-intake.json"
    write_json(intake_path, intake, compact=True)
    plan_path = PROGRAM_DIR / "ui-design-program.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan.update(
        {
            "contract_profile": "codex.ui-design-program/v1@2.0.0",
            "revision": 3,
            "status": "draft",
            "validation_profile": "draft",
        }
    )
    plan["input_contracts"] = {
        "intake": {"path": str(intake_path.relative_to(ROOT)), "sha256": sha256(intake_path)},
        "baseline": {"path": str(baseline_path.relative_to(ROOT)), "sha256": sha256(baseline_path)},
    }
    write_json(plan_path, plan, compact=True)
    provenance = {
        "schema_id": "codex.ui-program-contract-copy-provenance/v1",
        "source_registry": {
            "path": str(SKILL_ASSETS / "contract-versions.json"),
            "sha256": sha256(SKILL_ASSETS / "contract-versions.json"),
        },
        "copies": copied,
        "draft_inputs": [
            {"path": str(intake_path.relative_to(ROOT)), "sha256": sha256(intake_path)},
            {"path": str(baseline_path.relative_to(ROOT)), "sha256": sha256(baseline_path)},
            {"path": str(plan_path.relative_to(ROOT)), "sha256": sha256(plan_path)},
        ],
        "status": "preclaim_draft_pending_G0_standard_capture_and_owner_checkpoint",
    }
    write_json(EVIDENCE / "program-contract-copy-provenance.json", provenance)
    print(
        json.dumps(
            {
                "copied_assets": len(copied),
                "program_sha256": sha256(plan_path),
                "intake_sha256": sha256(intake_path),
                "baseline_sha256": sha256(baseline_path),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
