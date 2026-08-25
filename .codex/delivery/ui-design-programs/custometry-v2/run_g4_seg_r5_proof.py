#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PROGRAM = ROOT / ".codex/delivery/ui-design-programs/custometry-v2"
ARTIFACT = PROGRAM / "artifacts/g4-r5/family-seg-shell-workspace-baseline"
EVIDENCE = PROGRAM / "evidence/family.seg.shell-workspace.baseline-r5"
SKILL = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program")
PILOT = PROGRAM / "evidence/pilot-candidate-v3-metadata/ru/source.html"
PROGRAM_PATH = ARTIFACT / "ui-design-program.snapshot.json"
STATES = ("initial", "loading", "populated", "error", "permission_denied", "recovery")
ANCHORS = ("web-768", "web-1440", "web-1920")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def run(*args: str) -> None:
    subprocess.run([str(item) for item in args], cwd=ROOT, check=True)


def run_observational(*args: str) -> None:
    completed = subprocess.run([str(item) for item in args], cwd=ROOT, check=False)
    if completed.returncode not in {0, 1}:
        raise subprocess.CalledProcessError(completed.returncode, args)


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def capture(state: str, anchor: str) -> None:
    contract = ARTIFACT / f"states/{state}/screen-contract.json"
    candidate = ARTIFACT / f"states/{state}/screen.html"
    out = EVIDENCE / f"states/{state}/captures/{anchor}"
    out.mkdir(parents=True, exist_ok=True)
    ref_geometry = out / "reference-geometry.json"
    ref_png = out / "reference.png"
    impl_geometry = out / "implementation-geometry.json"
    impl_png = out / "implementation.png"
    pilot_url = f"http://127.0.0.1:4173/{rel(PILOT)}"
    candidate_url = f"http://127.0.0.1:4173/{rel(candidate)}"
    tool = SKILL / "scripts/ui_design_tool.py"
    run(sys.executable, tool, "capture", "--", "--url", pilot_url, "--contract", contract, "--anchor-id", anchor,
        "--target", "reference", "--source-artifact", rel(PILOT), "--logical-artifact-id", "custometry-pilot-v3-ru",
        "--output", ref_geometry, "--screenshot", ref_png, "--executable-path", CHROME, "--project-root", ROOT)
    run(sys.executable, tool, "capture", "--", "--url", candidate_url, "--contract", contract, "--anchor-id", anchor,
        "--target", "implementation", "--source-artifact", rel(candidate),
        "--logical-artifact-id", f"UI-SEG-001.{state}.AN.ru.graphite.r5-candidate",
        "--output", impl_geometry, "--screenshot", impl_png, "--executable-path", CHROME, "--project-root", ROOT)

    provenance = SKILL / "scripts/assemble_render_provenance.py"
    ref_request = out / "reference-provenance-request.json"
    ref_receipt = out / "reference-provenance.json"
    dump(ref_request, {"program_ref": rel(PROGRAM_PATH), "target": "reference",
                       "logical_artifact_id": "custometry-pilot-v3-ru", "anchor_id": anchor, "source_artifact_ref": rel(PILOT),
                       "capture_ref": rel(ref_png), "geometry_receipt_ref": rel(ref_geometry)})
    run(sys.executable, provenance, "--request", ref_request, "--project-root", ROOT, "--output", ref_receipt)
    impl_request = out / "implementation-provenance-request.json"
    impl_receipt = out / "implementation-provenance.json"
    dump(impl_request, {"program_ref": rel(PROGRAM_PATH), "target": "implementation",
                        "logical_artifact_id": f"UI-SEG-001.{state}.AN.ru.graphite.r5-candidate", "anchor_id": anchor,
                        "source_artifact_ref": rel(candidate), "capture_ref": rel(impl_png), "geometry_receipt_ref": rel(impl_geometry)})
    run(sys.executable, provenance, "--request", impl_request, "--project-root", ROOT, "--output", impl_receipt)

    raster = out / "raster.json"
    run_observational(sys.executable, tool, "compare", "--", "--reference", ref_png, "--implementation", impl_png, "--output", raster,
        "--diff-image", out / "diff.png", "--screen-revision-id", f"UI-SEG-001.{state}.AN.ru.graphite.r5", "--anchor-id", anchor,
        "--channel-threshold", "0", "--approved-max-different-pixels", "0", "--comparison-purpose", "visual_language_conformance",
        "--reference-logical-artifact-id", "custometry-pilot-v3-ru",
        "--implementation-logical-artifact-id", f"UI-SEG-001.{state}.AN.ru.graphite.r5-candidate",
        "--visual-authority-ref", rel(PILOT), "--visual-authority-sha256", sha(PILOT),
        "--reference-render-provenance", ref_receipt, "--implementation-render-provenance", impl_receipt, "--project-root", ROOT)
    visual = out / "visual-qa.json"
    run(sys.executable, SKILL / "scripts/assemble_visual_qa_receipt.py", "--contract", contract,
        "--reference-geometry", ref_geometry, "--implementation-geometry", impl_geometry,
        "--raster-receipt", raster, "--project-root", ROOT, "--output", visual)


def accept_screen(state: str) -> None:
    contract = ARTIFACT / f"states/{state}/screen-contract.json"
    args = [sys.executable, SKILL / "scripts/assemble_screen_acceptance.py", "--contract", contract]
    for anchor in ANCHORS:
        args.extend(["--anchor-receipt", EVIDENCE / f"states/{state}/captures/{anchor}/visual-qa.json"])
    args.extend(["--output", EVIDENCE / f"states/{state}/screen-acceptance.json"])
    run(*args)


def family() -> None:
    screen_rows = []
    for state in STATES:
        path = EVIDENCE / f"states/{state}/screen-acceptance.json"
        screen_rows.append((state, path))
    manifest_path = EVIDENCE / "review-board-manifest.json"
    entries = []
    for state, path in screen_rows:
        for role in ("screen_acceptance", "standard_conformance"):
            entries.append({"entry_id": f"{role}.{state}", "role": role, "artifact_ref": rel(path), "sha256": sha(path),
                            "anchor_id": None, "state_id": f"UI-SEG-001.{state}"})
    manifest = {"$schema": "review-board-manifest.schema.json", "schema_id": "codex.ui-review-board-manifest/v1",
                "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V2", "artifact_id": "family.seg.shell-workspace.baseline-r5",
                "revision": 5, "validation_profile": "family_review_ready", "entries": entries}
    dump(manifest_path, manifest)
    board = ARTIFACT / "review-board.html"
    cards = []
    labels = {"initial": "Начальное состояние", "loading": "Загрузка", "populated": "Рабочий список", "error": "Ошибка", "permission_denied": "Ограничение доступа", "recovery": "Восстановление"}
    for state, _ in screen_rows:
        image = f"../../../evidence/family.seg.shell-workspace.baseline-r5/states/{state}/captures/web-1440/implementation.png"
        cards.append(f'<article class="card"><div class="tag">{labels[state]}</div><img src="{image}" alt="Сегменты: {labels[state]}">'
                     f'<div class="evidence" data-review-entry="screen_acceptance.{state}">Экран и действия проверены</div>'
                     f'<div class="evidence" data-review-entry="standard_conformance.{state}">Visual language и responsive-Web проверены</div></article>')
    board.write_text(f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Custometry · Segmentation family</title>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#070708;color:#f0f0f2;font-family:Inter,system-ui,sans-serif}}main{{max-width:1540px;margin:auto;padding:40px}}.eyebrow{{color:#8bd2e8;text-transform:uppercase;letter-spacing:.14em;font-size:12px}}h1{{font-size:42px;margin:10px 0}}.lead{{color:#a7a7ad;max-width:820px;line-height:1.55}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-top:28px}}.card{{border:1px solid #303136;border-radius:16px;background:#111214;overflow:hidden;box-shadow:0 12px 34px #0008}}.tag{{padding:14px 16px;color:#8bd2e8;font-weight:700}}img{{display:block;width:100%;height:auto;border-block:1px solid #303136}}.evidence{{display:inline-block;margin:12px 0 12px 16px;color:#c9cbd0;font-size:12px}}@media(max-width:980px){{.grid{{grid-template-columns:1fr}}main{{padding:24px}}}}</style></head>
<body data-ui-artifact="review_board" data-program-id="CUSTOMETRY-UI-DESIGN-PROGRAM-V2" data-artifact-id="family.seg.shell-workspace.baseline-r5" data-revision="5" data-validation-profile="family_review_ready" data-review-manifest="{rel(manifest_path)}" data-review-manifest-sha256="{sha(manifest_path)}"><main><div class="eyebrow">Family review · Segmentation</div><h1>Сегменты без потери контекста</h1><p class="lead">Шесть обязательных состояний списка сегментов, безопасные действия управления/экспорта/продолжения и Result Trust. Responsive Web проверяется на 768, 1440 и 1920 px; mobile-specific композиция не входит в scope.</p><section class="grid">{''.join(cards)}</section></main></body></html>''', encoding="utf-8")
    request = EVIDENCE / "family-acceptance-request.json"
    dump(request, {"$schema": "family-acceptance-request.schema.json", "program_path": rel(PROGRAM_PATH), "family_id": "family.seg.shell-workspace.baseline",
                   "family_revision_id": "family.seg.shell-workspace.baseline-r5", "revision": 5,
                   "screen_acceptance_paths": [rel(path) for _, path in screen_rows], "review_board_path": rel(board), "owner_decision_ref": None})
    run(sys.executable, SKILL / "scripts/assemble_family_acceptance.py", "--request", request, "--project-root", ROOT,
        "--output", EVIDENCE / "family-acceptance.json")


if __name__ == "__main__":
    selected = tuple(sys.argv[1:]) or STATES
    if selected == ("family",):
        family()
        raise SystemExit(0)
    for item in selected:
        if item not in STATES:
            raise SystemExit(f"unknown state: {item}")
        for anchor_id in ANCHORS:
            capture(item, anchor_id)
        accept_screen(item)
    if set(selected) == set(STATES):
        family()
