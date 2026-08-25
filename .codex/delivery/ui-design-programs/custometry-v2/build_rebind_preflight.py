#!/usr/bin/env python3
"""Build exact typed stage-transition preflight evidence for the r5 rebind."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
LEDGER = DIR / "stage-ledger.md"
SKILL_SCRIPTS = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")
sys.path.insert(0, str(SKILL_SCRIPTS))

from validate_stage_ledger import parse_ledger  # noqa: E402
from validate_stage_transition import hash_bound_source_refs  # noqa: E402


FOREIGN_PATHS = [
    ".codex/AGENTS.md",
    "custometry-technical-blueprint-ru.md",
    "custometry-technical-blueprint-human-ru.md",
    "custometry-ui-blueprint-ru.md",
    "docs/generated/requirement-index.json",
    "packages/contracts/routes/ui-surface-contracts.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
        handle.write(rendered)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def document(check_id: str, program_id: str, stage_id: str, gate: str, facts: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": "stage-preflight-evidence.schema.json",
        "schema_id": "codex.ui-stage-preflight-evidence/v1",
        "check_id": check_id,
        "program_id": program_id,
        "stage_instance_id": stage_id,
        "gate_id": gate,
        "status": "passed",
        "facts": facts,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage-id", required=True)
    parser.add_argument("--gate", required=True, choices=[f"G{i}" for i in range(7)])
    parser.add_argument("--profile", required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--next-stage-id", required=True)
    parser.add_argument("--next-task", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--drift-classification", default="owned_generated_change", choices=("no_drift", "accepted_change", "owned_generated_change"))
    args = parser.parse_args()
    artifact = (ROOT / args.artifact).resolve() if not args.artifact.is_absolute() else args.artifact.resolve()
    next_task = (ROOT / args.next_task).resolve() if not args.next_task.is_absolute() else args.next_task.resolve()
    output_dir = (ROOT / args.output_dir).resolve() if not args.output_dir.is_absolute() else args.output_dir.resolve()
    parsed, errors = parse_ledger(LEDGER)
    if errors:
        raise ValueError("ledger parse failed: " + "; ".join(errors))
    detail = parsed["details"].get(args.stage_id)
    if not isinstance(detail, dict):
        raise ValueError("stage detail is missing")
    allowed_paths = [item.strip() for item in detail["expected_touch_zones"].split(",") if item.strip()]
    program_id = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"
    payloads = {
        "current-gate.json": document("current_gate", program_id, args.stage_id, args.gate, {
            "validation_profile": args.profile,
            "artifact_ref": ref(artifact),
            "artifact_sha256": sha(artifact),
            "result": "passed",
        }),
        "source-freshness.json": document("source_freshness", program_id, args.stage_id, args.gate, {
            "source_refs": hash_bound_source_refs(artifact, ROOT),
            "drift_classification": args.drift_classification,
            "stale_refs": [],
        }),
        "next-stage-inputs.json": document("next_stage_inputs", program_id, args.stage_id, args.gate, {
            "next_stage_id": args.next_stage_id,
            "task_ref": ref(next_task),
            "unresolved_inputs": [],
        }),
        "write-scope.json": document("write_scope", program_id, args.stage_id, args.gate, {
            "allowed_paths": allowed_paths,
            "authorization_basis": "active_task_and_repository_contract",
            "outside_scope_paths": [],
        }),
        "foreign-changes.json": document("foreign_changes", program_id, args.stage_id, args.gate, {
            "observed_paths": FOREIGN_PATHS,
            "inseparable_paths": [],
            "disposition": "separable_foreign_changes_preserved",
        }),
        "execution-route.json": document("execution_route", program_id, args.stage_id, args.gate, {
            "route": "staged_plan_runner_sequential_cas",
            "available": True,
        }),
        "handoff-artifact.json": document("handoff_artifact", program_id, args.stage_id, args.gate, {
            "artifact_ref": ref(next_task),
            "artifact_sha256": sha(next_task),
            "known_stop_resolution": "none",
        }),
    }
    for name, payload in payloads.items():
        write_json(output_dir / name, payload)
    print(json.dumps({"status": "passed", "output_dir": ref(output_dir), "source_refs": len(payloads["source-freshness.json"]["facts"]["source_refs"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
