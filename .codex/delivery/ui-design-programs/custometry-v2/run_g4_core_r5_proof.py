#!/usr/bin/env python3
"""Capture and assemble the owned G4 core-overview proof chain."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[4]
PROGRAM_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = PROGRAM_DIR / "artifacts/g4-r5/family-core-shell-workspace-baseline"
EVIDENCE_DIR = PROGRAM_DIR / "evidence/family.core.shell-workspace.baseline-r5"
PROGRAM = PROGRAM_DIR / "ui-design-program.json"
SOURCE_VISUAL = PROGRAM_DIR / "evidence/pilot-candidate-v3-metadata/ru/source.html"
SOURCE_VISUAL_REF = ".codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v3-metadata/ru/source.html"
SOURCE_VISUAL_SHA = "b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700"
SCRIPT_DIR = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")
UI_TOOL = SCRIPT_DIR / "ui_design_tool.py"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE_URL = "http://127.0.0.1:4173"

STATES = ("initial", "loading", "populated", "error", "permission_denied", "recovery")
ANCHORS = ("web-768", "web-1024", "web-1440", "web-1920")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(args: list[str], *, allowed: tuple[int, ...] = (0,)) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if result.returncode not in allowed:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(args[:4])}")
    return result


def capture(
    *,
    url: str,
    contract: Path,
    anchor: str,
    target: str,
    source_artifact: Path,
    logical_artifact_id: str,
    geometry: Path,
    screenshot: Path,
) -> None:
    run([
        "python3", str(UI_TOOL), "capture", "--",
        "--url", url,
        "--contract", rel(contract),
        "--anchor-id", anchor,
        "--target", target,
        "--source-artifact", rel(source_artifact),
        "--logical-artifact-id", logical_artifact_id,
        "--output", rel(geometry),
        "--screenshot", rel(screenshot),
        "--executable-path", CHROME,
        "--project-root", ".",
    ])


def render_provenance(
    *, target: str, logical_id: str, anchor: str, source: Path,
    capture_path: Path, geometry: Path, output: Path,
) -> None:
    request = output.with_name(f"{target}-render-provenance-request.json")
    write_json(request, {
        "program_ref": rel(PROGRAM),
        "target": target,
        "logical_artifact_id": logical_id,
        "anchor_id": anchor,
        "source_artifact_ref": rel(source),
        "capture_ref": rel(capture_path),
        "geometry_receipt_ref": rel(geometry),
    })
    run([
        "python3", str(SCRIPT_DIR / "assemble_render_provenance.py"),
        "--request", rel(request), "--project-root", ".", "--output", rel(output),
    ])


def prove_anchor(state: str, anchor: str) -> Path:
    contract = ARTIFACT_DIR / "states" / state / "screen-contract.json"
    candidate = ARTIFACT_DIR / "states" / state / "screen.html"
    contract_value = json.loads(contract.read_text(encoding="utf-8"))
    revision_id = contract_value["screen_revision_id"]
    reference_id = contract_value["comparison_claims"]["reference_logical_artifact_id"]
    implementation_id = contract_value["comparison_claims"]["implementation_logical_artifact_id"]
    out = EVIDENCE_DIR / "states" / state / anchor
    out.mkdir(parents=True, exist_ok=True)

    reference_geometry = out / "reference-geometry.json"
    implementation_geometry = out / "implementation-geometry.json"
    reference_image = out / "reference.png"
    implementation_image = out / "implementation.png"
    reference_provenance = out / "reference-render-provenance.json"
    implementation_provenance = out / "implementation-render-provenance.json"
    raster = out / "raster-diff.json"
    visual_qa = out / "visual-qa.json"

    capture(
        url=f"{BASE_URL}/{SOURCE_VISUAL_REF}", contract=contract, anchor=anchor,
        target="reference", source_artifact=SOURCE_VISUAL,
        logical_artifact_id=reference_id, geometry=reference_geometry,
        screenshot=reference_image,
    )
    capture(
        url=f"{BASE_URL}/{rel(candidate)}", contract=contract, anchor=anchor,
        target="implementation", source_artifact=candidate,
        logical_artifact_id=implementation_id, geometry=implementation_geometry,
        screenshot=implementation_image,
    )
    render_provenance(
        target="reference", logical_id=reference_id, anchor=anchor, source=SOURCE_VISUAL,
        capture_path=reference_image, geometry=reference_geometry, output=reference_provenance,
    )
    render_provenance(
        target="implementation", logical_id=implementation_id, anchor=anchor, source=candidate,
        capture_path=implementation_image, geometry=implementation_geometry,
        output=implementation_provenance,
    )

    compare = run([
        "python3", str(UI_TOOL), "compare", "--",
        "--reference", rel(reference_image),
        "--implementation", rel(implementation_image),
        "--output", rel(raster),
        "--screen-revision-id", revision_id,
        "--anchor-id", anchor,
        "--channel-threshold", "0",
        "--approved-max-different-pixels", "0",
        "--comparison-purpose", "visual_language_conformance",
        "--reference-logical-artifact-id", reference_id,
        "--implementation-logical-artifact-id", implementation_id,
        "--visual-authority-ref", SOURCE_VISUAL_REF,
        "--visual-authority-sha256", SOURCE_VISUAL_SHA,
        "--reference-render-provenance", rel(reference_provenance),
        "--implementation-render-provenance", rel(implementation_provenance),
        "--project-root", ".",
        "--diff-image", rel(out / "diff.png"),
    ], allowed=(0, 1))
    if not raster.is_file():
        raise RuntimeError(f"raster receipt was not produced: {compare.stderr}")

    run([
        "python3", str(SCRIPT_DIR / "assemble_visual_qa_receipt.py"),
        "--contract", rel(contract),
        "--reference-geometry", rel(reference_geometry),
        "--implementation-geometry", rel(implementation_geometry),
        "--raster-receipt", rel(raster),
        "--project-root", ".",
        "--output", rel(visual_qa),
    ])
    run([
        "python3", str(SCRIPT_DIR / "validate_ui_design_program.py"),
        "--profile", "visual_acceptance", "--project-root", ".", rel(visual_qa),
    ])
    return visual_qa


def prove_state(state: str) -> Path:
    receipts: list[Path] = []
    for anchor in ANCHORS:
        receipt = prove_anchor(state, anchor)
        receipts.append(receipt)
        print(json.dumps({"state": state, "anchor": anchor, "result": "passed"}), flush=True)
    contract = ARTIFACT_DIR / "states" / state / "screen-contract.json"
    acceptance = EVIDENCE_DIR / "states" / state / "screen-acceptance.json"
    command = [
        "python3", str(SCRIPT_DIR / "assemble_screen_acceptance.py"),
        "--contract", rel(contract),
    ]
    for receipt in receipts:
        command.extend(["--anchor-receipt", rel(receipt)])
    command.extend(["--output", rel(acceptance)])
    run(command)
    run([
        "python3", str(SCRIPT_DIR / "validate_ui_design_program.py"),
        "--profile", "screen_acceptance", "--project-root", ".", rel(acceptance),
    ])
    print(json.dumps({"state": state, "screen_acceptance": "passed"}), flush=True)
    return acceptance


def wait_for_server() -> None:
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            with urlopen(f"{BASE_URL}/{SOURCE_VISUAL_REF}", timeout=1) as response:
                if response.status == 200:
                    return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError("loopback evidence server did not become ready")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", choices=STATES, action="append")
    args = parser.parse_args()
    selected = tuple(args.state or STATES)
    if sha256(SOURCE_VISUAL) != SOURCE_VISUAL_SHA:
        raise RuntimeError("visual authority hash drifted")
    server_log = EVIDENCE_DIR / "loopback-server.log"
    server_log.parent.mkdir(parents=True, exist_ok=True)
    with server_log.open("w", encoding="utf-8") as log:
        server = subprocess.Popen(
            ["python3", "-m", "http.server", "4173", "--bind", "127.0.0.1"],
            cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, text=True,
        )
        try:
            wait_for_server()
            for state in selected:
                prove_state(state)
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=5)
    print(json.dumps({"result": "passed", "states": list(selected), "anchors": list(ANCHORS)}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
