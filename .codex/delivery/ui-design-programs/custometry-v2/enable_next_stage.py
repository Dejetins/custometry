#!/usr/bin/env python3
"""Prepare a ledger candidate that enables one exact pending adjacent row."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--stage-id", required=True)
    args = parser.parse_args()
    ledger = Path(args.ledger).resolve()
    candidate = Path(args.candidate).resolve()
    text = ledger.read_text(encoding="utf-8")
    row_matches = [line for line in text.splitlines() if line.startswith(f"| {args.stage_id} |")]
    if len(row_matches) != 1 or "| pending |" not in row_matches[0]:
        raise SystemExit("next stage must be one exact pending row")
    heading = f"### `{args.stage_id}`\n\n"
    if text.count(heading) != 1:
        raise SystemExit("next-stage detail block is not unique")
    before, after = text.split(heading, 1)
    if "\n\n### `" in after:
        block, remainder = after.split("\n\n### `", 1)
        suffix = "\n\n### `" + remainder
    else:
        block, suffix = after, ""
    if block.count("- execution_allowed: `false`") != 1:
        raise SystemExit("next-stage execution_allowed is not exactly false")
    block = block.replace("- execution_allowed: `false`", "- execution_allowed: `true`", 1)
    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.write_text(before + heading + block + suffix, encoding="utf-8")
    print(f"source_sha256={sha256(ledger)}")
    print(f"candidate_sha256={sha256(candidate)}")


if __name__ == "__main__":
    main()
