#!/usr/bin/env python3
"""Enable one pending visual row and bind its already assembled incoming receipt."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"expected one fragment: {old}")
    return text.replace(old, new, 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--stage-id", required=True)
    parser.add_argument("--transition-ref", required=True)
    parser.add_argument("--transition-sha256", required=True)
    args = parser.parse_args()
    ledger = Path(args.ledger).resolve()
    candidate = Path(args.candidate).resolve()
    text = ledger.read_text(encoding="utf-8")
    heading = f"### `{args.stage_id}`\n\n"
    if text.count(heading) != 1:
        raise SystemExit("pending detail block is not unique")
    before, after = text.split(heading, 1)
    block, remainder = after.split("\n\n### `", 1)
    block = replace_once(block, "- execution_allowed: `false`", "- execution_allowed: `true`")
    block = replace_once(block, "- incoming_transition_receipt: `none`", f"- incoming_transition_receipt: `{args.transition_ref}`")
    block = replace_once(block, "- incoming_transition_receipt_sha256: `none`", f"- incoming_transition_receipt_sha256: `{args.transition_sha256}`")
    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.write_text(before + heading + block + "\n\n### `" + remainder, encoding="utf-8")
    print(f"source_sha256={sha256(ledger)}")
    print(f"candidate_sha256={sha256(candidate)}")


if __name__ == "__main__":
    main()
