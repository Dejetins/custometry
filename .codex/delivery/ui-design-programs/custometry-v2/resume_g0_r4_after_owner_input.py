#!/usr/bin/env python3
"""Build a deterministic same-row G0 r4 resume candidate after owner input."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


STAGE_ID = "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4"
RESPONSE_REF = (
    ".codex/delivery/ui-design-programs/custometry-v2/evidence/g0-r4/"
    "owner-input-response-acceptance-r4.json"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(source: str, response_sha256: str) -> str:
    if source.count("ledger_status: awaiting_input") != 1:
        raise ValueError("source ledger must be awaiting exactly one owner input")
    if source.count(f"current_stage: {STAGE_ID}") != 1:
        raise ValueError("source ledger current_stage mismatch")
    source = source.replace("ledger_status: awaiting_input", "ledger_status: active", 1)

    lines = source.splitlines()
    indexes = [i for i, line in enumerate(lines) if line.startswith(f"| {STAGE_ID} |")]
    if len(indexes) != 1:
        raise ValueError("source ledger must contain exactly one G0 r4 row")
    columns = [part.strip() for part in lines[indexes[0]].strip("|").split("|")]
    if columns[4] != "needs_input":
        raise ValueError("G0 r4 must be needs_input before resumption")
    if not columns[9] or columns[9] == "—":
        raise ValueError("G0 r4 executor claim must be preserved")
    columns[4] = "in_progress"
    lines[indexes[0]] = "| " + " | ".join(columns) + " |"
    source = "\n".join(lines) + ("\n" if source.endswith("\n") else "")

    start = source.index(f"### `{STAGE_ID}`")
    end = source.find("\n### `", start + len(STAGE_ID))
    if end < 0:
        end = len(source)
    section = source[start:end]
    replacements = {
        "- resume_evidence_ref: `none`": f"- resume_evidence_ref: `{RESPONSE_REF}`",
        "- resume_evidence_sha256: `none`": f"- resume_evidence_sha256: `{response_sha256}`",
    }
    for old, new in replacements.items():
        if section.count(old) != 1:
            raise ValueError(f"G0 r4 detail must contain exactly one {old}")
        section = section.replace(old, new, 1)
    return source[:start] + section + source[end:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project_root.resolve()
    response = root / RESPONSE_REF
    if not response.is_file():
        raise ValueError("canonical owner input response is missing")
    candidate = build(args.ledger.read_text(encoding="utf-8"), sha256(response))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(candidate, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
