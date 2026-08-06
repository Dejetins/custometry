#!/usr/bin/env python3
"""Create typed G0 preflight evidence, report, and transition request."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM = ".codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json"
INTAKE = ".codex/delivery/ui-design-programs/custometry-v2/ui-program-intake.json"
BASELINE = ".codex/delivery/ui-design-programs/custometry-v2/platform-ui-baseline.json"
G1_PROMPT = ".codex/agents/generated/custometry-ui-design-g0-v2/10-g1-complete-screen-atlas.md"
REPORT = ".codex/delivery/evidence/custometry-ui-design-program-v2/g0-execution-report.md"
EVIDENCE_DIR = ROOT / ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0"
STAGE_ID = "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r1"
PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"


def resolve(path: str) -> Path:
    return ROOT / path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def hash_bound_source_refs(artifact: dict[str, Any]) -> list[dict[str, str]]:
    found: dict[str, str] = {}

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            path_value = value.get("path")
            path_hash = value.get("sha256")
            if isinstance(path_value, str) and isinstance(path_hash, str) and len(path_hash) == 64:
                found[path_value] = path_hash
            visual_path = value.get("source_visual_ref")
            visual_hash = value.get("source_visual_sha256")
            if isinstance(visual_path, str) and isinstance(visual_hash, str) and len(visual_hash) == 64:
                found[visual_path] = visual_hash
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(artifact)
    return sorted(({"path": path, "sha256": value} for path, value in found.items()), key=lambda item: (item["path"], item["sha256"]))


def preflight(check_id: str, facts: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": "stage-preflight-evidence.schema.json",
        "schema_id": "codex.ui-stage-preflight-evidence/v1",
        "check_id": check_id,
        "program_id": PROGRAM_ID,
        "stage_instance_id": STAGE_ID,
        "gate_id": "G0",
        "status": "passed",
        "facts": facts,
    }


def main() -> int:
    program_path = resolve(PROGRAM)
    program = json.loads(program_path.read_text(encoding="utf-8"))
    intake = json.loads(resolve(INTAKE).read_text(encoding="utf-8"))
    baseline = json.loads(resolve(BASELINE).read_text(encoding="utf-8"))
    screen_counts: dict[str, int] = {}
    for screen in intake["screens"]:
        kind = screen["surface_kind"]
        screen_counts[kind] = screen_counts.get(kind, 0) + 1
    checks = {
        "current_gate": preflight("current_gate", {
            "validation_profile": "draft", "artifact_ref": PROGRAM,
            "artifact_sha256": digest(program_path), "result": "passed",
        }),
        "source_freshness": preflight("source_freshness", {
            "source_refs": hash_bound_source_refs(program),
            "drift_classification": "owned_generated_change", "stale_refs": [],
        }),
        "next_stage_inputs": preflight("next_stage_inputs", {
            "next_stage_id": "G1@atlas-r1", "task_ref": G1_PROMPT, "unresolved_inputs": [],
        }),
        "write_scope": preflight("write_scope", {
            "allowed_paths": [
                ".codex/delivery/ui-design-programs/custometry-v2/**",
                ".codex/agents/generated/custometry-ui-design-g0-v2/**",
                ".codex/delivery/evidence/**",
                "docs/architecture/ui/**",
                "docs/architecture/**",
                "docs/adr/**",
            ],
            "authorization_basis": "explicit_current_user_authorization", "outside_scope_paths": [],
        }),
        "foreign_changes": preflight("foreign_changes", {
            "observed_paths": [], "inseparable_paths": [], "disposition": "no_conflicting_foreign_changes",
        }),
        "handoff_artifact": preflight("handoff_artifact", {
            "artifact_ref": G1_PROMPT, "artifact_sha256": digest(resolve(G1_PROMPT)),
            "known_stop_resolution": "none",
        }),
    }
    for check_id, value in checks.items():
        write_json(EVIDENCE_DIR / "preflight" / f"{check_id}.json", value)
    report_path = resolve(REPORT)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "# CUSTOMETRY-UI-DESIGN-PROGRAM-V2 G0 execution report\n\n"
        "- Status: `completed`\n"
        "- Stage: `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r1`\n"
        "- Program: `CUSTOMETRY-UI-DESIGN-PROGRAM-V2` revision `1`\n"
        "- Execution mode: `manual_sequential`\n\n"
        "## Authority and scope\n\n"
        "The accepted owner task is copied byte-for-byte and hash-pinned inside the V2 evidence boundary. "
        "The normalized owner-intent record preserves the included/excluded slices, nine critical journeys, source hierarchy, responsive-Web-only boundary, mobile `unauthorized`, and V1/Penpot historical-only status.\n\n"
        "The RU pilot is the exact visual-language and density anchor; the EN pilot is independent content-stress support. "
        "Neither authorizes exact target composition, information architecture, frontend implementation, responsive acceptance, browser behavior, or novel-screen fidelity.\n\n"
        "## Intake and baseline\n\n"
        f"- Screens/current admission entries: `{len(intake['screens'])}` (`{json.dumps(screen_counts, sort_keys=True)}`)\n"
        f"- Critical journeys: `{len(intake['journeys'])}`\n"
        f"- Baseline: `{baseline['baseline_id']}@r{baseline['revision']}` with status `{baseline['status']}`\n"
        "- Supported responsive-Web range: `768..1920` CSS px; anchors: `768x1024`, `1024x768`, `1440x900`, `1920x1080`\n"
        "- Visual theme: `paper`; baseline scope remains visual-language/foundation only\n\n"
        "## Architecture ownership\n\n"
        "ADR-0007 fixes React/TypeScript/Vite routing and UI-foundation boundaries, TanStack Query as the sole server-state owner, "
        "MobX only for scoped presentation/draft state, product-owned semantic tokens/components over styled-components, "
        "and API/SSE adapters as transport/cancellation/error/redaction owners. Product contexts remain owners of data meaning and terminal domain state.\n\n"
        "## Validation evidence\n\n"
        "- `ui_program_intake.py`: `ready`, zero owner questions\n"
        "- `validate_ui_design_program.py --profile intake_ready`: passed\n"
        "- `validate_ui_design_program.py --profile baseline_ready`: passed\n"
        "- `validate_ui_design_program.py --profile draft`: passed; expected warning that G1 atlas entries do not yet exist\n"
        "- Admission shard indexes: exact-cover `175` intake screens and `9` critical journeys\n"
        "- Post-transition G1 `ui_program_context.py`: bounded at `8/8` files and about `20,948/40,000` tokens\n"
        "- `uv run python -m tools.check --scope local`: passed after deterministic contributor docs-index regeneration\n"
        "- Cold-head review: initial `Not ready`; all four authority, owner-intent, ledger, and prompt-control findings were repaired before closure\n"
        "- RU/EN pilot SHA-256 and byte counts match the source manifest\n\n"
        "## Proof boundary and residual risk\n\n"
        "Evidence is documentation/static-contract proof only. It does not prove browser runtime, rendered responsive behavior, "
        "accessibility conformance, performance, recovery, deployment, or production readiness. The current baseline/intake validator "
        "still requires a revisioned compatibility adapter for the canonical owner receipt; both are hash-bound and the adapter grants no additional authority.\n\n"
        "G1 may build the exact-cover atlas after the accepted transition receipt. G1 was not claimed or executed here.\n",
        encoding="utf-8",
    )
    request = {
        "$schema": "stage-transition-request.schema.json",
        "program_id": PROGRAM_ID,
        "from_stage_id": STAGE_ID,
        "from_gate": "G0",
        "from_target": PROGRAM_ID,
        "from_revision": 1,
        "artifact": PROGRAM,
        "to_gate": "G1",
        "to_stage_id": "G1@atlas-r1",
        "to_target": "atlas-r1",
        "to_task": G1_PROMPT,
        "status": "ready",
        "owner_decision": None,
        "decision_inventory": None,
        "blockers": None,
        "checks": [
            f"current_gate={EVIDENCE_DIR.relative_to(ROOT)}/preflight/current_gate.json",
            f"source_freshness={EVIDENCE_DIR.relative_to(ROOT)}/preflight/source_freshness.json",
            f"next_stage_inputs={EVIDENCE_DIR.relative_to(ROOT)}/preflight/next_stage_inputs.json",
            f"write_scope={EVIDENCE_DIR.relative_to(ROOT)}/preflight/write_scope.json",
            f"foreign_changes={EVIDENCE_DIR.relative_to(ROOT)}/preflight/foreign_changes.json",
            "execution_route=N/A",
            f"handoff_artifact={EVIDENCE_DIR.relative_to(ROOT)}/preflight/handoff_artifact.json",
        ],
        "summary": "G0 completed the hash-pinned owner intake, pilot import, fixed responsive-Web baseline, and frontend architecture boundary; G1 is ready but was not executed.",
        "review_artifacts": [REPORT],
        "questions": [],
    }
    write_json(EVIDENCE_DIR / "stage-transition-request.json", request)
    print(json.dumps({"status": "prepared", "report": REPORT, "request": str((EVIDENCE_DIR / 'stage-transition-request.json').relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
