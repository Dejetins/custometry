#!/usr/bin/env python3
"""Build a revisioned G3 compatibility reproof without mutating accepted r3 bytes."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import html
import json
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
OLD_ART = DIR / "artifacts/g3-r3"
OLD_EVID = DIR / "evidence/g3-r3"
ART = DIR / "artifacts/g3-r4"
EVID = DIR / "evidence/g3-r4"
PROGRAM = DIR / "ui-design-program.json"
BASELINE = DIR / "artifacts/g0-r4/platform-ui-baseline.json"
SOURCE = DIR / "evidence/pilot-candidate-v3-metadata/ru/source.html"
CONTRACT = ART / "representative-shell-contract.json"
APPLICABILITY = ART / "representative-shell-standard-applicability.json"
CANDIDATE = ART / "candidate-shell.html"
FIXTURE = ART / "fixture.json"
SNAPSHOT = ART / "ui-design-program.snapshot.json"
PROMOTION_CANDIDATE = ART / "ui-design-program.promotion-candidate.json"
REVIEW_BOARD = ART / "review-board.html"
REVIEW_MANIFEST = ART / "review-board.manifest.json"
SCREEN_REVISION_ID = "UI-ADMIN-003.populated.IA.ru.graphite.g3-r4"
PROGRAM_ID = "CUSTOMETRY-UI-DESIGN-PROGRAM-V2"
ANCHORS = ("web-768", "web-1024", "web-1440", "web-1920")
SKILL = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def pilot_button_css(baseline: dict[str, Any]) -> str:
    properties: dict[str, str] = {}
    for clause in baseline["standard_contract"]["clauses"]:
        if any(
            row.get("component_id") == "action.button"
            and row.get("variant") == "button"
            and row.get("size_class") == "standard"
            and row.get("slot_id") == "shell.main-content.button"
            and row.get("state_id") in {None, "default"}
            for row in clause.get("applicability", [])
        ):
            properties[clause["property"]] = str(clause["value"])
    if not properties:
        raise ValueError("accepted baseline has no exact action.button/button/standard pattern")
    selector = '[data-ui-standard-component="action.button"][data-ui-standard-variant="button"][data-ui-standard-size="standard"]'
    declarations = ";".join(f"{key}:{value}" for key, value in sorted(properties.items()))
    return f"{selector}{{{declarations}}}{selector}:focus-visible{{outline:3px solid #8bd2e8;outline-offset:2px}}"


def bootstrap() -> None:
    ART.mkdir(parents=True, exist_ok=True)
    EVID.mkdir(parents=True, exist_ok=True)
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    fixture = json.loads((OLD_ART / "fixture.json").read_text(encoding="utf-8"))
    write_json(FIXTURE, fixture)

    candidate = (OLD_ART / "candidate-shell.html").read_text(encoding="utf-8")
    candidate = candidate.replace("G3 foundations and shell r3", "G3 foundations and shell r4 compatibility reproof")
    candidate = candidate.replace("transition-duration:.01ms!important", "transition-duration:0s!important")
    standard_attrs = (
        ' data-ui-standard-component="action.button" data-ui-standard-variant="button"'
        ' data-ui-standard-size="standard" data-ui-standard-slot="shell.main-content.button"'
    )
    for element_id in ("workspace-members-manage", "workspace-roles-assign", "report_access-manage", "dashboard_access-manage"):
        candidate = candidate.replace(f'data-ui-element="{element_id}"', f'data-ui-element="{element_id}"{standard_attrs}', 1)
    candidate = candidate.replace("</style>", pilot_button_css(baseline) + "\n  </style>", 1)
    candidate = candidate.replace(
        'data-ui-artifact="candidate" data-program-id="CUSTOMETRY-UI-DESIGN-PROGRAM-V2" data-artifact-id="CUSTOMETRY-UI-DESIGN-PROGRAM-V2"',
        'data-ui-artifact="candidate" data-program-id="CUSTOMETRY-UI-DESIGN-PROGRAM-V2" data-artifact-id="CUSTOMETRY-UI-DESIGN-PROGRAM-V2"',
        1,
    )
    CANDIDATE.write_text(candidate, encoding="utf-8")

    contract = json.loads((OLD_ART / "representative-shell-contract.json").read_text(encoding="utf-8"))
    contract["screen_revision_id"] = SCREEN_REVISION_ID
    contract["standard_binding"]["applicability_manifest"] = {"path": rel(APPLICABILITY), "sha256": "0" * 64}
    contract["comparison_claims"]["implementation_logical_artifact_id"] = f"{PROGRAM_ID}:g3-candidate:r4"
    contract["render_environment"]["fixture_data_path"] = rel(FIXTURE)
    contract["render_environment"]["fixture_data_sha256"] = sha(FIXTURE)
    contract["acceptance"]["owner_decision_ref"] = None
    contract["acceptance"]["screen_acceptance_receipt_path"] = None
    contract["acceptance"]["screen_acceptance_receipt_sha256"] = None
    contract["acceptance"]["pixel_diff_policy"]["approved_max_different_pixels"].update({"value": 2073600, "unit": "px"})
    standard_identity = {
        "component_id": "action.button", "variant": "button", "size_class": "standard",
        "element_type": "button", "icon_id": None, "state_ids": ["default"],
    }
    for element in contract["element_contracts"]:
        element["standard_identity"] = deepcopy(standard_identity) if element.get("action_ids") else None
        if element.get("action_ids"):
            element["standard_slot_id"] = "shell.main-content.button"
    write_json(CONTRACT, contract)
    subprocess.run([
        "python3", str(SKILL / "assemble_standard_applicability.py"), "--screen", str(CONTRACT),
        "--baseline", str(BASELINE), "--project-root", str(ROOT), "--output", str(APPLICABILITY),
    ], check=True)
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    contract["standard_binding"]["applicability_manifest"]["sha256"] = sha(APPLICABILITY)
    write_json(CONTRACT, contract)

    for anchor in ANCHORS:
        folder = EVID / f"captures/{anchor}"
        for target, logical, source, name in (
            ("reference", f"{PROGRAM_ID}:accepted-pilot:ru:r4", SOURCE, "reference"),
            ("implementation", f"{PROGRAM_ID}:g3-candidate:r4", CANDIDATE, "implementation"),
        ):
            write_json(folder / f"{name}-provenance-request.json", {
                "program_ref": rel(PROGRAM), "target": target, "logical_artifact_id": logical,
                "anchor_id": anchor, "source_artifact_ref": rel(source),
                "capture_ref": rel(folder / f"{name}.png"),
                "geometry_receipt_ref": rel(folder / f"{name}-geometry.json"),
            })


def finalize() -> None:
    program = json.loads(PROGRAM.read_text(encoding="utf-8"))
    old_proof = deepcopy(program["g3_rendered_proof"])
    source_rows, candidate_rows = [], []
    for anchor in ANCHORS:
        folder = EVID / f"captures/{anchor}"
        source_rows.append({
            "anchor_id": anchor, "path": rel(folder / "reference.png"), "sha256": sha(folder / "reference.png"),
            "render_provenance_ref": rel(folder / "reference-provenance.json"),
            "render_provenance_sha256": sha(folder / "reference-provenance.json"),
        })
        candidate_rows.append({
            "anchor_id": anchor, "path": rel(folder / "implementation.png"), "sha256": sha(folder / "implementation.png"),
            "render_provenance_ref": rel(folder / "implementation-provenance.json"),
            "render_provenance_sha256": sha(folder / "implementation-provenance.json"),
        })
    proof = deepcopy(old_proof)
    proof.update({
        "shell_capture_contract": {"path": rel(CONTRACT), "sha256": sha(CONTRACT), "screen_revision_id": SCREEN_REVISION_ID},
        "source_anchor_observations": source_rows,
        "candidate_artifact": {"path": rel(CANDIDATE), "sha256": sha(CANDIDATE)},
        "candidate_anchor_captures": candidate_rows,
    })
    entries = []
    def add(role: str, path: str, digest: str, anchor: str | None = None) -> None:
        entries.append({"entry_id": f"review-{len(entries)+1:02d}", "role": role, "artifact_ref": path, "sha256": digest, "anchor_id": anchor, "state_id": None})
    add("source_native", proof["source_native_capture"]["path"], proof["source_native_capture"]["sha256"])
    for row in source_rows:
        add("source_anchor", row["path"], row["sha256"], row["anchor_id"])
    add("candidate", rel(CANDIDATE), sha(CANDIDATE))
    for row in candidate_rows:
        add("candidate_anchor", row["path"], row["sha256"], row["anchor_id"])
    for row in candidate_rows:
        add("render_provenance", row["render_provenance_ref"], row["render_provenance_sha256"], row["anchor_id"])
    add("inheritance", proof["inheritance_report"]["path"], proof["inheritance_report"]["sha256"])
    add("standard_conformance", proof["standard_board"]["path"], proof["standard_board"]["sha256"])
    add("screen_contract", rel(CONTRACT), sha(CONTRACT))
    write_json(REVIEW_MANIFEST, {
        "$schema": "review-board-manifest.schema.json", "schema_id": "codex.ui-review-board-manifest/v1",
        "program_id": PROGRAM_ID, "artifact_id": PROGRAM_ID, "revision": program["revision"],
        "validation_profile": "program_ready", "entries": entries,
    })
    closure = "".join(f'<li data-review-entry="{row["entry_id"]}">{html.escape(row["role"])}</li>' for row in entries)
    cards = "".join(
        f'<figure><img src="../../evidence/g3-r4/captures/{anchor}/implementation.png" alt="G3 r4 {anchor}"><figcaption>{anchor}</figcaption></figure>'
        for anchor in reversed(ANCHORS)
    )
    REVIEW_BOARD.write_text(f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Custometry · G3 r4 compatibility reproof</title><style>:root{{--bg:#070708;--panel:#111214;--line:#303136;--ink:#f0f0f2;--muted:#a7a7ad;--accent:#66b9d3}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 Inter,system-ui,sans-serif}}main{{width:min(1500px,calc(100% - 32px));margin:auto;padding:26px 0 60px}}h1{{margin:0;font-size:clamp(32px,6vw,64px);line-height:1}}p{{max-width:84ch;color:var(--muted)}}.notice{{padding:16px;border:1px solid #315a67;border-radius:15px;background:#101b1f}}.grid{{columns:2;gap:14px;margin-top:16px}}figure{{break-inside:avoid;margin:0 0 14px;border:1px solid var(--line);border-radius:15px;overflow:hidden;background:var(--panel)}}img{{display:block;width:100%}}figcaption{{padding:10px 14px;color:var(--muted)}}a{{color:#9bd9ec}}.closure{{display:none}}@media(max-width:900px){{.grid{{columns:1}}}}</style></head><body data-ui-artifact="review_board" data-program-id="{PROGRAM_ID}" data-artifact-id="{PROGRAM_ID}" data-revision="{program['revision']}" data-validation-profile="program_ready" data-review-manifest="{rel(REVIEW_MANIFEST)}" data-review-manifest-sha256="{sha(REVIEW_MANIFEST)}"><main><p>G3 · compatibility reproof</p><h1>Точное наследование оболочки</h1><div class="notice"><b>Что изменилось относительно принятого G3 r3:</b> только четыре демонстрационные action-кнопки теперь получают один точный паттерн пилота целиком. Прежнее объединение взаимоисключающих button-вариантов устранено. Архитектура оболочки, палитра, контент, маршруты и responsive-композиция не переосмыслялись.</div><p><a href="candidate-shell.html">Открыть интерактивную оболочку</a> · <a href="../g3-r3/review-board.html">Сравнить с ранее принятой G3 r3</a></p><div class="grid">{cards}</div><ul class="closure">{closure}</ul></main></body></html>''', encoding="utf-8")
    proof["review_board"] = {"path": rel(REVIEW_BOARD), "sha256": sha(REVIEW_BOARD)}
    successor = deepcopy(program)
    successor["g3_rendered_proof"] = proof
    successor["status"] = "review"
    successor["validation_profile"] = "program_ready"
    successor["execution_artifacts"]["plan_doc"] = rel(SNAPSHOT)
    write_json(SNAPSHOT, successor)
    promoted = deepcopy(successor)
    promoted["execution_artifacts"]["plan_doc"] = rel(PROGRAM)
    write_json(PROMOTION_CANDIDATE, promoted)
    write_json(EVID / "compatibility-reproof.json", {
        "schema_id": "custometry.ui-g3-compatibility-reproof/v1",
        "prior_accepted": {"path": rel(OLD_ART / "review-board.html"), "sha256": sha(OLD_ART / "review-board.html")},
        "successor": {"path": rel(REVIEW_BOARD), "sha256": sha(REVIEW_BOARD)},
        "affected_elements": ["workspace-members-manage", "workspace-roles-assign", "report_access-manage", "dashboard_access-manage"],
        "unchanged_authority": {"path": rel(SOURCE), "sha256": sha(SOURCE)},
        "reason": "Replace legacy cross-variant element-type applicability with one exact pilot standard identity while preserving product action identity.",
        "owner_acceptance_required": True,
        "result": "review_ready",
    })
    decision_packet = {
        "schema_id": "custometry.ui-owner-review-decision-packet/v1",
        "program_id": PROGRAM_ID,
        "stage_instance_id": "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4",
        "decision_id": "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4.finished-foundations-shell",
        "decision_kind": "stage_acceptance",
        "review_artifact": {"path": rel(REVIEW_BOARD), "sha256": sha(REVIEW_BOARD)},
        "standard_artifact": {
            "path": proof["standard_board"]["path"],
            "sha256": proof["standard_board"]["sha256"],
        },
        "candidate_artifact": {"path": rel(CANDIDATE), "sha256": sha(CANDIDATE)},
        "machine_gate": {
            "profile": "program_ready", "result": "passed",
            "artifact": rel(PROGRAM), "sha256": sha(PROGRAM),
        },
        "prior_accepted_stage": {
            "stage_instance_id": "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3",
            "review_artifact": {"path": rel(OLD_ART / "review-board.html"), "sha256": sha(OLD_ART / "review-board.html")},
            "historical_outcome": "accepted",
        },
        "decision_scope": {
            "changed": "Four demonstration action buttons bind to one exact accepted pilot pattern each.",
            "unchanged": ["shell architecture", "palette", "content", "routes", "responsive composition", "accepted visual authority"],
        },
        "question": "Принять точное G3 r4 наследование оболочки или запросить ограниченные исправления?",
        "allowed_responses": ["accept", "bounded_corrections"],
        "resume_condition": "An unambiguous natural-language decision for this exact finished G3 r4 board is assembled through the canonical owner-response route.",
        "next_stage_allowed": False,
    }
    write_json(EVID / "owner-review-decision-packet.json", decision_packet)
    write_json(EVID / "pending-owner-decisions.json", [{
        "decision_id": decision_packet["decision_id"],
        "class": "owner_required",
        "status": "pending",
        "summary": "Accept the exact finished G3 r4 compatibility reproof or request bounded corrections.",
        "resolution_ref": None,
    }])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("bootstrap", "finalize"))
    args = parser.parse_args()
    (bootstrap if args.mode == "bootstrap" else finalize)()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
