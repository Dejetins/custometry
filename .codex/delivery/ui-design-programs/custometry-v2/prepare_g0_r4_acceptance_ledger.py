#!/usr/bin/env python3
"""Prepare the durable accepted-G0 / pending-G1 ledger boundary."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


TRANSITION_REF = ".codex/delivery/ui-design-programs/custometry-v2/evidence/CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4/stage-transition.json"
TRANSITION_SHA256 = "ab0fd87297a9a2ee3e577e279650ab8cd533e13355e4eb34cc4851152d6a6bd7"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected one ledger fragment, observed {count}: {old}")
    return text.replace(old, new, 1)


def replace_in_block(text: str, heading: str, next_heading: str, old: str, new: str) -> str:
    if text.count(heading) != 1:
        raise SystemExit(f"detail heading is not unique: {heading}")
    before, after = text.split(heading, 1)
    block, remainder = after.split(next_heading, 1)
    block = replace_once(block, old, new)
    return before + heading + block + next_heading + remainder


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--candidate", required=True)
    args = parser.parse_args()
    ledger = Path(args.ledger).resolve()
    candidate = Path(args.candidate).resolve()
    text = ledger.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "current_stage: G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4",
        "current_stage: G1@atlas-r3",
    )
    text = replace_once(text, "Next stage allowed: false", "Next stage allowed: true")
    old_row = (
        "| G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4 | G0 | CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4 | "
        ".codex/agents/generated/custometry-ui-design-g0-v2/03-g0-authoritative-sources-r4.md | in_progress |"
    )
    text = replace_once(text, old_row, old_row.replace("| in_progress |", "| accepted |"))

    g0_heading = "### `G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4`\n\n"
    g1_heading = "\n\n### `G1@atlas-r3`"
    text = replace_in_block(
        text,
        g0_heading,
        g1_heading,
        "- transition_receipt_sha256: `none`",
        f"- transition_receipt_sha256: `{TRANSITION_SHA256}`",
    )
    text = replace_in_block(
        text,
        g1_heading.lstrip("\n"),
        "\n\n### `G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3`",
        "- incoming_transition_receipt: `none`",
        f"- incoming_transition_receipt: `{TRANSITION_REF}`",
    )
    text = replace_in_block(
        text,
        g1_heading.lstrip("\n"),
        "\n\n### `G2@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r3`",
        "- incoming_transition_receipt_sha256: `none`",
        f"- incoming_transition_receipt_sha256: `{TRANSITION_SHA256}`",
    )

    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.write_text(text, encoding="utf-8")
    print(f"source_sha256={sha256(ledger)}")
    print(f"candidate_sha256={sha256(candidate)}")


if __name__ == "__main__":
    main()
