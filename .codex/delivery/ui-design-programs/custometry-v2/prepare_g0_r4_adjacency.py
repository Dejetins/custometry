#!/usr/bin/env python3
"""Prepare the unique G0 r4 -> G1 r3 adjacency before transition assembly."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"expected exactly one ledger fragment, observed {text.count(old)}: {old}")
    return text.replace(old, new, 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--candidate", required=True)
    args = parser.parse_args()
    ledger = Path(args.ledger).resolve()
    candidate = Path(args.candidate).resolve()
    text = ledger.read_text(encoding="utf-8")
    old_row = (
        "| G1@atlas-r3 | G1 | atlas-r3 | .codex/agents/generated/custometry-ui-design-g0-v2/12-g1-complete-screen-atlas-r3.md | pending | "
        "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3 |"
    )
    new_row = old_row.replace(
        "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3",
        "G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4",
    )
    text = replace_once(text, old_row, new_row)
    g0_r3_heading = "### `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3`\n\n"
    if text.count(g0_r3_heading) != 1:
        raise SystemExit("G0 r3 detail block is not unique")
    before, after = text.split(g0_r3_heading, 1)
    block, remainder = after.split("\n\n### `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4`", 1)
    block = replace_once(block, "- current_authority: `true`", "- current_authority: `false`")
    text = before + g0_r3_heading + block + "\n\n### `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4`" + remainder

    g0_r4_heading = "### `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4`\n\n"
    if text.count(g0_r4_heading) != 1:
        raise SystemExit("G0 r4 detail block is not unique")
    before, after = text.split(g0_r4_heading, 1)
    block, remainder = after.split("\n\n### `G1@atlas-r3`", 1)
    block = replace_once(block, "- current_authority: `false`", "- current_authority: `true`")
    text = before + g0_r4_heading + block + "\n\n### `G1@atlas-r3`" + remainder

    heading = "### `G1@atlas-r3`\n\n"
    if text.count(heading) != 1:
        raise SystemExit("G1 r3 detail block is not unique")
    before, after = text.split(heading, 1)
    block, remainder = after.split("\n### `", 1)
    block = replace_once(block, "- execution_allowed: `false`", "- execution_allowed: `true`")
    text = before + heading + block + "\n### `" + remainder
    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.write_text(text, encoding="utf-8")
    print(f"source_sha256={sha256(ledger)}")
    print(f"candidate_sha256={sha256(candidate)}")


if __name__ == "__main__":
    main()
