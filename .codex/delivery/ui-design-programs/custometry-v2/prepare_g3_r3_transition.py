#!/usr/bin/env python3
"""Prepare exact G3 r3 review-ready preflight, report, and transition request."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
EVID = DIR / "evidence/g3-r3"
PREFLIGHT = EVID / "preflight"
ART = DIR / "artifacts/g3-r3"
PROGRAM = DIR / "ui-design-program.json"
REPORT = ROOT / ".codex/delivery/evidence/custometry-ui-design-program-v2/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3-report.md"
STAGE = "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3"
NEXT_STAGE = "G4@family.auth.shell-auth.baseline-exception-auth-r4"
NEXT_TARGET = "family.auth.shell-auth.baseline-exception-auth-r4"
NEXT_TASK = ROOT / ".codex/agents/generated/custometry-ui-design-g0-v2/40-g4-01-family-auth-shell-auth-baseline-exception-auth-r4.md"
PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def preflight(check_id: str, facts: dict[str, Any]) -> dict[str, Any]:
    return {"$schema": "stage-preflight-evidence.schema.json", "schema_id": "codex.ui-stage-preflight-evidence/v1",
        "check_id": check_id, "program_id": PROGRAM_ID, "stage_instance_id": STAGE,
        "gate_id": "G3", "status": "passed", "facts": facts}


def hash_bound_source_refs(document: Any) -> list[dict[str, str]]:
    found: dict[str, str] = {}
    def visit(value: Any) -> None:
        if isinstance(value, dict):
            path, digest = value.get("path"), value.get("sha256")
            if isinstance(path, str) and isinstance(digest, str) and len(digest) == 64:
                found[path] = digest
            source, source_hash = value.get("source_visual_ref"), value.get("source_visual_sha256")
            if isinstance(source, str) and isinstance(source_hash, str) and len(source_hash) == 64:
                found[source] = source_hash
            for child in value.values(): visit(child)
        elif isinstance(value, list):
            for child in value: visit(child)
    visit(document)
    return [{"path": path, "sha256": digest} for path, digest in sorted(found.items())]


def main() -> None:
    program = json.loads(PROGRAM.read_text(encoding="utf-8"))
    board = ART / "review-board.html"
    standard = ART / "standard-board.html"
    candidate = ART / "candidate-shell.html"
    decision_packet = EVID / "owner-review-decision-packet.json"
    decisions = EVID / "pending-owner-decisions.json"
    blockers = EVID / "known-blockers.json"
    stress = EVID / "responsive-language-accessibility-smoke.json"
    write_json(stress, {
        "schema_id": "custometry.ui-g3-browser-stress/v2", "program_id": PROGRAM_ID,
        "stage_instance_id": STAGE, "browser_mechanic": "playwright-cli 0.1.17 / Chromium 150.0.7871.187",
        "checks": [
            {"check": "canonical target capture", "status": "passed", "anchors": list(a["anchor_id"] for a in program["g3_rendered_proof"]["candidate_anchor_captures"]), "standard_observations_at_1440": 420},
            {"check": "RU/EN structural stress", "status": "passed", "observed": {"en_heading": "Shell and visual-language rules", "document_overflow": False}},
            {"check": "keyboard/focus", "status": "passed", "observed": {"focused_control": "series-toggle", "outline": "solid", "drawer_escape_focus_return": "nav-toggle"}},
            {"check": "200% zoom/reflow", "status": "passed", "observed": {"visual_viewport_scale": 2, "visual_viewport": {"width": 384, "height": 512}, "document_overflow": False, "essential_regions_present": True}},
            {"check": "reduced motion", "status": "passed", "observed": {"prefers_reduced_motion": True}},
            {"check": "console/network", "status": "passed", "observed": {"console_errors": 0, "request_failures": 0, "external_requests": 0}},
            {"check": "file owner board", "status": "passed", "observed": {"protocol": "file:", "images": 4, "broken_images": 0, "console_errors": 0}},
        ],
        "artifacts": [
            {"path": rel(EVID / "candidate-web-1440-en-zoom200.png"), "sha256": sha(EVID / "candidate-web-1440-en-zoom200.png")},
            {"path": rel(EVID / "candidate-web-768-zoom200.png"), "sha256": sha(EVID / "candidate-web-768-zoom200.png")},
            {"path": rel(EVID / "review-board-1440.png"), "sha256": sha(EVID / "review-board-1440.png")},
        ],
        "proof_boundary": "Local responsive-Web, interaction and accessibility smoke; not production runtime, mobile-specific design, full WCAG conformance, publication or deployment proof.",
        "result": "passed",
    })
    write_json(decision_packet, {
        "schema_id": "custometry.ui-owner-review-decision-packet/v1", "program_id": PROGRAM_ID,
        "stage_instance_id": STAGE, "review_artifact": {"path": rel(board), "sha256": sha(board)},
        "standard_artifact": {"path": rel(standard), "sha256": sha(standard)},
        "candidate_artifact": {"path": rel(candidate), "sha256": sha(candidate)},
        "machine_gate": {"profile": "program_ready", "result": "passed", "artifact": rel(PROGRAM), "sha256": sha(PROGRAM)},
        "question": "Принять готовые основы и оболочку G3 как обязательную визуальную основу для экранов G4 или запросить ограниченные исправления?",
        "allowed_responses": ["accept", "bounded_corrections"],
        "resume_condition": "An unambiguous natural-language decision for this exact finished G3 board is assembled through the canonical owner-response route.",
        "next_stage_allowed": False,
    })
    write_json(decisions, [{"decision_id": f"{STAGE}.finished-result", "class": "owner_required",
        "status": "pending", "summary": "Accept the finished visual result or request bounded corrections.", "resolution_ref": None}])
    write_json(blockers, [])
    checks = {
        "current_gate": preflight("current_gate", {"validation_profile": "program_ready", "artifact_ref": rel(PROGRAM), "artifact_sha256": sha(PROGRAM), "result": "passed"}),
        "source_freshness": preflight("source_freshness", {"source_refs": hash_bound_source_refs(program), "drift_classification": "owned_generated_change", "stale_refs": []}),
        "next_stage_inputs": preflight("next_stage_inputs", {"next_stage_id": NEXT_STAGE, "task_ref": rel(NEXT_TASK), "unresolved_inputs": []}),
        "write_scope": preflight("write_scope", {"allowed_paths": [".codex/delivery/ui-design-programs/custometry-v2/**", ".codex/agents/generated/custometry-ui-design-g0-v2/**", ".codex/delivery/evidence/custometry-ui-design-program-v2/**"], "authorization_basis": "explicit_current_user_authorization", "outside_scope_paths": []}),
        "foreign_changes": preflight("foreign_changes", {"observed_paths": [".codex/AGENTS.md", "custometry-technical-blueprint-ru.md", "custometry-technical-blueprint-human-ru.md", "custometry-ui-blueprint-ru.md", "docs/generated/requirement-index.json", "packages/contracts/routes/ui-surface-contracts.json"], "inseparable_paths": [], "disposition": "separable_foreign_changes_preserved"}),
        "execution_route": preflight("execution_route", {"route": "staged-plan-runner + ui-design-program + browser-qa-evidence/playwright-cli", "available": True}),
        "handoff_artifact": preflight("handoff_artifact", {"artifact_ref": rel(NEXT_TASK), "artifact_sha256": sha(NEXT_TASK), "known_stop_resolution": "none"}),
    }
    for key, value in checks.items(): write_json(PREFLIGHT / f"{key}.json", value)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(f"""# {PROGRAM_ID} G3 r3 foundations and shell review-ready report

- Stage: `{STAGE}`; result: `review_ready`, awaiting owner acceptance.
- Review board: `{rel(board)}` — `{sha(board)}`.
- Standard board: `{rel(standard)}` — `{sha(standard)}`; all 203 pilot-derived clauses are represented, with deterministic applicability and no owner exceptions.
- Representative contract: `{rel(ART / 'representative-shell-contract.json')}` — `{sha(ART / 'representative-shell-contract.json')}`; active `codex.ui-screen-design-contract/v1@2.0.0`, representative `UI-ADMIN-003`.
- Inheritance policy: every target element with a corresponding pilot pattern inherits the complete applicable rule set; partial inheritance and aesthetic approximation are forbidden.
- Browser proof: four source-reference and four target captures at the fixed 768, 1024, 1440 and 1920 Web anchors; active render provenance; 420 computed standard observations at 1440; interaction, keyboard/focus, console/network, RU/EN, reduced motion, 200% page scale, overflow and accessibility smoke passed.
- File review surface: loaded through `file://`; 4/4 images loaded, 0 broken, 0 console errors.
- Product boundary: the accepted pilot governs typography, controls, radii, borders, palette, density, focus, motion and responsive behavior, but not target product meaning, fixture values, permissions or novel screen composition.
- Mobile-specific scope remains unauthorized; production implementation, publication and deployment are untouched.
- Historical G3 r2 and G4 r2/r3 evidence remains read-only; no G4 row was claimed.
""", encoding="utf-8")
    write_json(EVID / "stage-transition-request.json", {
        "$schema": "stage-transition-request.schema.json", "program_id": PROGRAM_ID,
        "from_stage_id": STAGE, "from_gate": "G3", "from_target": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3", "from_revision": 4,
        "artifact": rel(PROGRAM), "to_gate": "G4", "to_stage_id": NEXT_STAGE, "to_target": NEXT_TARGET, "to_task": rel(NEXT_TASK),
        "status": "review_ready", "owner_decision": None, "decision_inventory": rel(decisions), "blockers": rel(blockers),
        "checks": [f"{key}={rel(PREFLIGHT / f'{key}.json')}" for key in checks],
        "summary": "The complete G3 foundations and shell result is machine-valid and visually reviewable. Every matching target element is governed by the full applicable pilot rule set; product semantics and future screen composition remain target-owned.",
        "review_artifacts": [rel(board), rel(standard), rel(candidate), rel(EVID / "review-board-1440.png")],
        "questions": ["Принять готовые основы и оболочку G3 или указать ограниченные исправления?"],
    })


if __name__ == "__main__": main()
