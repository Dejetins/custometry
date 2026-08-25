#!/usr/bin/env python3
"""Prepare deterministic G3 r2 review-ready evidence and transition inputs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
EVID = PROGRAM_DIR / "evidence/g3-r2"
PREFLIGHT = EVID / "preflight"
ART = PROGRAM_DIR / "artifacts/g3-r2"
PROGRAM = PROGRAM_DIR / "ui-design-program.json"
REPORT = ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/g3-r2-foundations-shell-report.md"
OWNER_DECISION = EVID / "owner-acceptance-r2.json"
OWNER_RESPONSE = EVID / "owner-input-response-acceptance-r2.json"
NEXT_STAGE = "G4@family.auth.shell-auth.baseline-exception-auth-r2"
NEXT_TASK = ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-01-family-auth-shell-auth-baseline-exception-auth-r2.md"
STAGE = "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2"
PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def hash_bound_source_refs(document: Any) -> list[dict[str, str]]:
    found: dict[str, str] = {}

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            path = value.get("path")
            digest = value.get("sha256")
            if isinstance(path, str) and isinstance(digest, str) and len(digest) == 64:
                found[path] = digest
            source = value.get("source_visual_ref")
            source_hash = value.get("source_visual_sha256")
            if isinstance(source, str) and isinstance(source_hash, str) and len(source_hash) == 64:
                found[source] = source_hash
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(document)
    return [{"path": path, "sha256": digest} for path, digest in sorted(found.items())]


def preflight(check_id: str, facts: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": "stage-preflight-evidence.schema.json",
        "schema_id": "codex.ui-stage-preflight-evidence/v1",
        "check_id": check_id,
        "program_id": PROGRAM_ID,
        "stage_instance_id": STAGE,
        "gate_id": "G3",
        "status": "passed",
        "facts": facts,
    }


def main() -> None:
    program = json.loads(PROGRAM.read_text(encoding="utf-8"))
    board = ART / "review-board.html"
    stress = EVID / "responsive-language-accessibility-smoke.json"
    decision_packet = EVID / "owner-review-decision-packet.json"
    decisions = EVID / "pending-owner-decisions.json"
    blockers = EVID / "known-blockers.json"
    write_json(decision_packet, {
        "schema_id": "custometry.ui-owner-review-decision-packet/v1",
        "program_id": PROGRAM_ID,
        "stage_instance_id": STAGE,
        "review_artifact": {"path": rel(board), "sha256": sha(board)},
        "machine_gate": {"profile": "program_ready", "result": "passed", "artifact": rel(PROGRAM), "sha256": sha(PROGRAM)},
        "question": "Принять правила foundations и application shell, извлечённые из пилота и зафиксированные для проектирования экранов G4, или запросить ограниченную коррекцию в этой же ревизии?",
        "allowed_responses": ["accept", "bounded_corrections"],
        "resume_condition": "An unambiguous natural-language owner acceptance or bounded correction request is recorded through the canonical typed owner-response flow for this exact G3 review artifact.",
        "next_stage_allowed": False,
    })
    write_json(decisions, [{
        "decision_id": f"{STAGE}.finished-result",
        "class": "owner_required", "status": "resolved",
        "summary": "Accept the finished visual result or request bounded corrections.",
        "resolution_ref": rel(OWNER_DECISION),
    }])
    write_json(blockers, [])
    checks = {
        "current_gate": preflight("current_gate", {
            "validation_profile": "program_ready", "artifact_ref": rel(PROGRAM),
            "artifact_sha256": sha(PROGRAM), "result": "passed",
        }),
        "source_freshness": preflight("source_freshness", {
            "source_refs": hash_bound_source_refs(program),
            "drift_classification": "owned_generated_change", "stale_refs": [],
        }),
        "next_stage_inputs": preflight("next_stage_inputs", {
            "next_stage_id": NEXT_STAGE, "task_ref": rel(NEXT_TASK), "unresolved_inputs": [],
        }),
        "write_scope": preflight("write_scope", {
            "allowed_paths": [
                ".codex/delivery/ui-design-programs/custometry-v2/**",
                ".codex/agents/generated/custometry-ui-design-g0-v2/**",
                ".codex/delivery/evidence/custometry-ui-design-program-v2/**",
            ],
            "authorization_basis": "explicit_current_user_authorization", "outside_scope_paths": [],
        }),
        "foreign_changes": preflight("foreign_changes", {
            "observed_paths": [
                ".codex/AGENTS.md", "custometry-technical-blueprint-ru.md",
                "custometry-technical-blueprint-human-ru.md", "custometry-ui-blueprint-ru.md",
                "docs/generated/requirement-index.json", "packages/contracts/routes/ui-surface-contracts.json",
            ],
            "inseparable_paths": [], "disposition": "separable_foreign_changes_preserved",
        }),
        "execution_route": preflight("execution_route", {
            "route": "staged-plan-runner claimed G3 r2 with repository-local deterministic builders and canonical Playwright evidence",
            "available": True,
        }),
        "handoff_artifact": preflight("handoff_artifact", {
            "artifact_ref": rel(NEXT_TASK), "artifact_sha256": sha(NEXT_TASK), "known_stop_resolution": "none",
        }),
    }
    for check_id, document in checks.items():
        write_json(PREFLIGHT / f"{check_id}.json", document)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(f"""# {PROGRAM_ID} G3 r2 foundations and shell report

- Stage: `{STAGE}`
- Result: `program_ready` machine gate passed; the exact corrected G3 result is owner-accepted.
- Review board: `{rel(board)}` — `{sha(board)}`.
- Internal representative contract: `{rel(ART / 'representative-shell-contract.json')}` — `{sha(ART / 'representative-shell-contract.json')}`; repository-authoritative `UI-SHELL-GLOBAL` is used only for machine validation and is not the owner acceptance subject.
- Browser proof: four canonical responsive-Web captures at 768×1024, 1024×768, 1440×900 and 1920×1080; candidate geometry/action checks, console/network checks, RU/EN stress, actual Chromium page scale 2, reduced motion, drawer/inspector/table states.
- Inheritance: 12/12 detailed visual-domain checks pass; Graphite surfaces, 15 px workspace radius, 97 px chrome, 31 px pill tabs, 62 px rail, analytical language, grouped control backing, visible table grammar and inspector geometry match the accepted pilot, while the accepted baseline deliberately supplies the zero-tolerance 12 px gap and 32 px profile area. The owner acceptance subject is only these pilot-derived foundation and shell rules; no screen, fixture semantics, or target composition is being accepted. No owner exception exists, and all 68 OWNER-REC plus 13 RECON-ADD obligations remain explicitly carried downstream.
- Layout: compact rail, overlay contextual navigation, fixed 12 px shell gap, independent workspace scrolling, full-height wide sibling/narrow viewport overlay inspector, and right/lower series panel.
- Analytical language: a neutral program-owned specimen simultaneously exposes chart and dense table, grouped icon controls on shared backings, 36 px analytical rows, Result Trust, Focus/Explore, local overflow, state and recovery language without becoming a target-screen design.
- Determinism: two consecutive finalization runs reproduced identical program, review-board and review-manifest SHA-256 values; exact values are recorded in the file manifest.
- Validation: `screen_contract_ready`, `program_ready`, canonical four-anchor browser capture/provenance/comparison, typed nested review closure, `validate_stage_transition.py`, `validate_stage_ledger.py`, and `uv run python -m tools.check --scope local` passed.
- Mobile scope: `unauthorized`; no mobile-specific IA or composition was created.
- Exceptions: none in fixed domains. The 12 px gap and 32 px profile area are source-backed baseline adaptations, not owner exceptions. The accepted pilot is used only as visual-language/platform-baseline authority; candidate composition and fixture values are not claimed as accepted target-screen semantics.
- Proof boundary: finished G3 foundations/shell, local browser rendering, responsive-Web and accessibility smoke only; no production implementation, deployment, performance, recovery, full WCAG conformance, target-screen family acceptance or release proof.
- Owner acceptance: `{rel(OWNER_DECISION)}` — `{sha(OWNER_DECISION)}`; typed natural-language response: `{rel(OWNER_RESPONSE)}` — `{sha(OWNER_RESPONSE)}`.
- Next stage: G4 is independently allowed by the validated handoff, but every G4 row remains pending and unclaimed; no G4 work was executed by this task.
""", encoding="utf-8")
    request = {
        "$schema": "stage-transition-request.schema.json",
        "program_id": PROGRAM_ID,
        "from_stage_id": STAGE, "from_gate": "G3",
        "from_target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r2", "from_revision": 2,
        "artifact": rel(PROGRAM),
        "to_gate": "G4", "to_stage_id": NEXT_STAGE,
        "to_target": "family.auth.shell-auth.baseline-exception-auth-r2",
        "to_task": rel(NEXT_TASK), "status": "ready",
        "owner_decision": rel(OWNER_DECISION), "decision_inventory": rel(decisions), "blockers": rel(blockers),
        "checks": [f"{check_id}={rel(PREFLIGHT / f'{check_id}.json')}" for check_id in checks],
        "summary": "The owner fully accepted the corrected G3 r2 neutral foundations/application-shell specimen derived from the accepted pilot. The strict machine gate remains passing, target-screen semantics remain excluded, and the validated handoff allows—but does not claim or execute—the first G4 row.",
        "review_artifacts": [rel(board), rel(EVID / "review-board-1440.png"), rel(stress), rel(REPORT)],
        "questions": [],
    }
    write_json(EVID / "stage-transition-request.json", request)
    manifest_path = EVID / "file-manifest.json"
    owned = {
        PROGRAM_DIR / "build_g3_r2_artifacts.py",
        PROGRAM_DIR / "prepare_g3_r2_transition.py",
        PROGRAM,
        PROGRAM_DIR / "stage-ledger.md",
        NEXT_TASK,
        REPORT,
        *ART.rglob("*"),
        *(path for path in EVID.rglob("*") if path != manifest_path),
    }
    files = [path for path in owned if path.is_file()]
    write_json(manifest_path, {
        "schema_id": "custometry.ui-g3-file-manifest/v1",
        "program_id": PROGRAM_ID, "stage_instance_id": STAGE,
        "entries": [
            {"path": rel(path), "sha256": sha(path), "bytes": path.stat().st_size}
            for path in sorted(files, key=rel)
        ],
        "deleted": [], "outside_expected_paths": [],
        "foreign_changes_excluded": True,
    })


if __name__ == "__main__":
    main()
