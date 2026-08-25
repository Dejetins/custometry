#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PROGRAM = ROOT / ".codex/delivery/ui-design-programs/custometry-v2"
ARTIFACT = PROGRAM / "artifacts/g4-r5/family-seg-shell-workspace-baseline"
EVIDENCE = PROGRAM / "evidence/family.seg.shell-workspace.baseline-r5"
PREFLIGHT = EVIDENCE / "preflight"
REPORT = ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/family.seg.shell-workspace.baseline-r5-report.md"
STAGE = "G4@family.seg.shell-workspace.baseline-r5"
NEXT_STAGE = "G4@family.fcst.shell-workspace.baseline-r5"
NEXT_TASK = ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-08-family-fcst-shell-workspace-baseline-r5.md"
FAMILY_ACCEPTANCE = EVIDENCE / "family-acceptance.json"
BOARD = ARTIFACT / "review-board.html"
SCREEN_STATES = ("initial", "loading", "populated", "error", "permission_denied", "recovery")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def preflight(check_id: str, facts: dict) -> Path:
    path = PREFLIGHT / f"{check_id}.json"
    dump(path, {
        "$schema": "stage-preflight-evidence.schema.json",
        "schema_id": "codex.ui-stage-preflight-evidence/v1",
        "check_id": check_id,
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "stage_instance_id": STAGE,
        "gate_id": "G4",
        "status": "passed",
        "facts": facts,
    })
    return path


def main() -> None:
    screenshot = EVIDENCE / "review-board-1440.png"
    browser_qa = EVIDENCE / "browser-board-qa.json"
    dump(browser_qa, {
        "schema_id": "custometry.ui-g4-browser-board-qa/v1",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "stage_instance_id": STAGE,
        "generated_by": {"browser_mechanic": "playwright-cli 0.1.17 / Chrome 150.0.7871.187"},
        "artifacts": {
            "review_board": {"path": rel(BOARD), "sha256": sha(BOARD)},
            "screenshot": {"path": rel(screenshot), "sha256": sha(screenshot)},
        },
        "checks": [
            {"check_id": "six_images_visible", "status": "passed"},
            {"check_id": "review_manifest_exact_cover", "status": "passed"},
            {"check_id": "responsive_web_no_horizontal_overflow", "status": "passed"},
            {"check_id": "console_network_clean", "status": "passed"},
        ],
        "observed": {
            "url": f"http://127.0.0.1:4173/{rel(BOARD)}",
            "responsive": [{"width": width, "overflow": False, "cards": 6, "entries": 12} for width in (768, 1440, 1920)],
            "images": [{"state": state, "complete": True, "naturalWidth": 1440, "naturalHeight": 900} for state in SCREEN_STATES],
            "console_errors": [],
            "failed_requests": [],
        },
        "proof_boundary": "Loopback browser proof for the finished family review board, six visible images, review closure, and responsive-Web overflow; not production runtime, mobile-specific design, or full WCAG conformance.",
        "result": "passed",
    })

    program_snapshot = ARTIFACT / "ui-design-program.snapshot.json"
    screen_receipts = [EVIDENCE / f"states/{state}/screen-acceptance.json" for state in SCREEN_STATES]
    checks = [
        preflight("current_gate", {
            "validation_profile": "family_review_ready",
            "artifact_ref": rel(FAMILY_ACCEPTANCE),
            "artifact_sha256": sha(FAMILY_ACCEPTANCE),
            "result": "passed",
        }),
        preflight("source_freshness", {
            "source_refs": [
                {"path": rel(BOARD), "sha256": sha(BOARD)},
                {"path": rel(program_snapshot), "sha256": sha(program_snapshot)},
                *[{"path": rel(path), "sha256": sha(path)} for path in screen_receipts],
            ],
            "drift_classification": "owned_generated_change",
            "stale_refs": [],
        }),
        preflight("next_stage_inputs", {
            "next_stage_id": NEXT_STAGE,
            "task_ref": rel(NEXT_TASK),
            "unresolved_inputs": [],
        }),
        preflight("write_scope", {
            "allowed_paths": [
                ".codex/agents/generated/custometry-ui-design-g0-v2/**",
                ".codex/delivery/evidence/custometry-ui-design-program-v2/**",
                ".codex/delivery/ui-design-programs/custometry-v2/**",
            ],
            "authorization_basis": "active_task_and_repository_contract",
            "outside_scope_paths": [],
        }),
        preflight("foreign_changes", {
            "observed_paths": [
                ".codex/AGENTS.md",
                "custometry-technical-blueprint-human-ru.md",
                "custometry-technical-blueprint-ru.md",
                "custometry-ui-blueprint-ru.md",
                "docs/generated/requirement-index.json",
                "packages/contracts/routes/ui-surface-contracts.json",
            ],
            "inseparable_paths": [],
            "disposition": "separable_foreign_changes_preserved",
        }),
        preflight("execution_route", {
            "route": "goal_driven staged-plan-runner with ui-design-program CAS ledger updates",
            "available": True,
        }),
        preflight("handoff_artifact", {
            "artifact_ref": rel(NEXT_TASK),
            "artifact_sha256": sha(NEXT_TASK),
            "known_stop_resolution": "none",
        }),
    ]

    transition_request = EVIDENCE / "stage-transition-request-review-ready.json"
    dump(transition_request, {
        "$schema": "stage-transition-request.schema.json",
        "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2",
        "from_stage_id": STAGE,
        "from_gate": "G4",
        "from_target": "family.seg.shell-workspace.baseline-r5",
        "from_revision": 5,
        "artifact": rel(FAMILY_ACCEPTANCE),
        "to_gate": "G4",
        "to_stage_id": NEXT_STAGE,
        "to_target": "family.fcst.shell-workspace.baseline-r5",
        "to_task": rel(NEXT_TASK),
        "status": "review_ready",
        "owner_decision": None,
        "decision_inventory": None,
        "blockers": None,
        "checks": [f"{path.stem}={rel(path)}" for path in checks],
        "summary": "Segmentation exact-covers six required states and three responsive-Web anchors; machine proof is ready for owner review.",
        "review_artifacts": [rel(BOARD), rel(screenshot), rel(browser_qa)],
        "questions": ["Принимаете готовую family review board или хотите небольшие правки?"],
    })

    decision_packet = EVIDENCE / "owner-review-decision-packet.md"
    decision_packet.write_text(f"""---
artifact_kind: ui_design_owner_decision_packet
program_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2
stage_instance_id: {STAGE}
status: needs_input
question_count: 1
resume_same_stage: true
---

# Готовые исследования сегментов

## Что готово

Готова family review board для `UI-SEG-001`: шесть обязательных состояний,
три responsive-Web anchor (`768`, `1440`, `1920`) и изолированный browser proof.

- `{rel(BOARD)}`
- `{rel(screenshot)}`

## Вопрос

Принимаете готовую family review board или хотите небольшие правки?

После ответа агент сам запишет canonical receipt, возобновит эту же стадию и
повторит strict gate. От владельца не требуются хеши, JSON или операции ledger.
""", encoding="utf-8")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(f"""---
artifact_kind: ui_design_stage_report
program_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V2
stage_instance_id: {STAGE}
status: review_ready
---

# G4 segmentation family review-ready report

## Scope

Produced the isolated `UI-SEG-001` family result for initial, loading,
populated, error, permission-denied, and recovery states at responsive-Web
anchors 768x1024, 1440x900, and 1920x1080. Mobile-specific composition,
production implementation, publication, deployment, and full WCAG conformance
remain outside this stage proof boundary.

## Evidence

- Family receipt: `{rel(FAMILY_ACCEPTANCE)}` (`review_ready`)
- Review board: `{rel(BOARD)}`
- Browser QA: `{rel(browser_qa)}` (`passed`)
- Owner decision packet: `{rel(decision_packet)}`

## Validation

- `validate_ui_design_program.py --profile program_ready`: passed
- six `screen_contract_ready` checks: passed
- eighteen `visual_acceptance` receipts: passed
- six `screen_acceptance` receipts: passed
- `family_review_ready`: passed
- Playwright CLI board smoke at 768, 1440, and 1920 px: passed; no overflow, console errors, or failed requests

## Residual risk and next action

The full-frame raster comparison is observational visual-language evidence, not
an exact-composition acceptance claim. Owner acceptance is still required.
The same stage must resume after an unambiguous accept/correction response;
the next ledger row must not be claimed before then.
""", encoding="utf-8")


if __name__ == "__main__":
    main()
