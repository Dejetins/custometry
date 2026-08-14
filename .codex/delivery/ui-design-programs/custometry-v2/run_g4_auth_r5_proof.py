#!/usr/bin/env python3
"""Run canonical browser capture and assembled G4 r5 auth-family proof."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[4]
DIR = Path(__file__).resolve().parent
ART = DIR / "artifacts/g4-r5/family-auth-shell-auth-baseline-exception-auth"
EVID = DIR / "evidence/g4-r5/family-auth-shell-auth-baseline-exception-auth"
SOURCE = DIR / "evidence/pilot-candidate-v3-metadata/ru/source.html"
TARGET = ART / "screens/auth-family.html"
SKILL = Path("/Users/daniildegtyarev/.codex/skills/ui-design-program/scripts")
TOOL = SKILL / "ui_design_tool.py"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE_URL = "http://127.0.0.1:4173"
ANCHORS = ("web-768", "web-1024", "web-1440", "web-1920")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> None:
    result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError("command failed: " + " ".join(command) + "\n" + result.stdout)


def contracts() -> list[Path]:
    rows = sorted((ART / "contracts").glob("*.json"))
    if len(rows) != 12:
        raise ValueError(f"expected 12 contracts, observed {len(rows)}")
    return rows


def assert_server() -> None:
    served = urlopen(f"{BASE_URL}/{rel(TARGET)}", timeout=5).read()
    if hashlib.sha256(served).hexdigest() != sha(TARGET):
        raise ValueError("loopback server does not serve the exact r5 target bytes")


def capture_one(contract_path: Path, anchor: str, target_kind: str) -> None:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    screen_id = contract["product_identity"]["screen_id"]
    state_id = contract["product_identity"]["state_id"]
    folder = EVID / "captures" / state_id / anchor
    folder.mkdir(parents=True, exist_ok=True)
    if target_kind == "reference":
        source = SOURCE
        logical = contract["comparison_claims"]["reference_logical_artifact_id"]
        url = f"{BASE_URL}/{rel(SOURCE)}"
    else:
        source = TARGET
        logical = contract["comparison_claims"]["implementation_logical_artifact_id"]
        url = f"{BASE_URL}/{rel(TARGET)}?screen={screen_id}&state={state_id}&lang=ru"
    run([
        "python3", str(TOOL), "capture", "--", "--url", url,
        "--contract", rel(contract_path), "--anchor-id", anchor, "--target", target_kind,
        "--source-artifact", rel(source), "--logical-artifact-id", logical,
        "--output", rel(folder / f"{target_kind}-geometry.json"),
        "--screenshot", rel(folder / f"{target_kind}.png"), "--executable-path", CHROME,
    ])


def capture() -> None:
    assert_server()
    jobs = [(contract, anchor, target) for contract in contracts() for anchor in ANCHORS for target in ("reference", "implementation")]
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(capture_one, *job): job for job in jobs}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                raise RuntimeError(f"capture failed for {futures[future]}: {exc}") from exc
    print(json.dumps({"status": "passed", "browser_captures": len(jobs), "mechanic": "playwright-cli/capture_geometry.cjs"}, indent=2))


def assemble_anchor(contract_path: Path, anchor: str) -> None:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    state_id = contract["product_identity"]["state_id"]
    folder = EVID / "captures" / state_id / anchor
    for target in ("reference", "implementation"):
        run(["python3", str(SKILL / "assemble_render_provenance.py"), "--request", rel(folder / f"{target}-provenance-request.json"), "--project-root", str(ROOT), "--output", rel(folder / f"{target}-provenance.json")])
    run([
        "python3", str(TOOL), "compare", "--", "--reference", rel(folder / "reference.png"),
        "--implementation", rel(folder / "implementation.png"), "--output", rel(folder / "raster.json"),
        "--screen-revision-id", contract["screen_revision_id"], "--anchor-id", anchor,
        "--channel-threshold", str(contract["acceptance"]["pixel_diff_policy"]["channel_threshold"]["value"]),
        "--approved-max-different-pixels", str(contract["acceptance"]["pixel_diff_policy"]["approved_max_different_pixels"]["value"]),
        "--comparison-purpose", contract["comparison_claims"]["required_purpose"],
        "--reference-logical-artifact-id", contract["comparison_claims"]["reference_logical_artifact_id"],
        "--implementation-logical-artifact-id", contract["comparison_claims"]["implementation_logical_artifact_id"],
        "--visual-authority-ref", contract["visual_authority"]["source_visual_ref"],
        "--visual-authority-sha256", contract["visual_authority"]["source_visual_sha256"],
        "--reference-render-provenance", rel(folder / "reference-provenance.json"),
        "--implementation-render-provenance", rel(folder / "implementation-provenance.json"),
        "--project-root", str(ROOT),
    ])
    run([
        "python3", str(SKILL / "assemble_visual_qa_receipt.py"), "--contract", rel(contract_path),
        "--reference-geometry", rel(folder / "reference-geometry.json"),
        "--implementation-geometry", rel(folder / "implementation-geometry.json"),
        "--raster-receipt", rel(folder / "raster.json"), "--project-root", str(ROOT),
        "--output", rel(folder / "visual-qa.json"),
    ])


def assemble() -> None:
    jobs = [(contract, anchor) for contract in contracts() for anchor in ANCHORS]
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(assemble_anchor, *job): job for job in jobs}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                raise RuntimeError(f"anchor assembly failed for {futures[future]}: {exc}") from exc
    output_dir = EVID / "screen-acceptance"
    output_dir.mkdir(parents=True, exist_ok=True)
    for contract_path in contracts():
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        state_id = contract["product_identity"]["state_id"]
        command = ["python3", str(SKILL / "assemble_screen_acceptance.py"), "--contract", rel(contract_path)]
        for anchor in ANCHORS:
            command.extend(["--anchor-receipt", rel(EVID / "captures" / state_id / anchor / "visual-qa.json")])
        command.extend(["--output", rel(output_dir / f"{state_id}.r5.json")])
        run(command)
    print(json.dumps({"status": "passed", "visual_qa_receipts": len(jobs), "screen_acceptance_receipts": 12}, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("capture", "assemble"))
    args = parser.parse_args()
    (capture if args.mode == "capture" else assemble)()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
