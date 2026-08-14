#!/usr/bin/env python3
"""Build the deterministic same-row G3 r3 resume candidate after owner acceptance."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


STAGE_ID = "G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"expected one ledger fragment: {old}")
    return text.replace(old, new, 1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--response", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project_root.resolve()
    response = root / args.response
    if not response.is_file():
        raise ValueError("canonical owner input response is missing")
    response_hash = sha256(response)
    source = args.ledger.read_text(encoding="utf-8")
    source = replace_once(source, "ledger_status: awaiting_input", "ledger_status: active")
    lines = source.splitlines()
    rows = [i for i, line in enumerate(lines) if line.startswith(f"| {STAGE_ID} |")]
    if len(rows) != 1:
        raise ValueError("G3 r3 row is not unique")
    columns = [part.strip() for part in lines[rows[0]].strip("|").split("|")]
    if columns[4] != "needs_input" or columns[9] in {"", "—"}:
        raise ValueError("G3 r3 must be needs_input with its executor claim preserved")
    columns[4] = "in_progress"
    lines[rows[0]] = "| " + " | ".join(columns) + " |"
    source = "\n".join(lines) + ("\n" if source.endswith("\n") else "")
    heading = f"### `{STAGE_ID}`\n\n"
    before, after = source.split(heading, 1)
    block, tail = after.split("\n\n### `", 1)
    block = replace_once(block, "- resume_evidence_ref: `none`", f"- resume_evidence_ref: `{args.response}`")
    block = replace_once(block, "- resume_evidence_sha256: `none`", f"- resume_evidence_sha256: `{response_hash}`")
    output = before + heading + block + "\n\n### `" + tail
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(f"source_sha256={sha256(args.ledger)}")
    print(f"candidate_sha256={sha256(args.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
