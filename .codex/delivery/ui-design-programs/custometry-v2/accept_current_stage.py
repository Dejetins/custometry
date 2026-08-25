#!/usr/bin/env python3
"""Prepare a durable accepted-current / pending-next ledger boundary."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected one ledger fragment, observed {count}: {old}")
    return text.replace(old, new, 1)


def update_detail(text: str, stage_id: str, old: str, new: str) -> str:
    heading = f"### `{stage_id}`\n\n"
    if text.count(heading) != 1:
        raise SystemExit(f"detail heading is not unique: {stage_id}")
    before, after = text.split(heading, 1)
    if "\n\n### `" in after:
        block, remainder = after.split("\n\n### `", 1)
        suffix = "\n\n### `" + remainder
    else:
        block, suffix = after, ""
    block = replace_once(block, old, new)
    return before + heading + block + suffix


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--from-stage", required=True)
    parser.add_argument("--to-stage", required=True)
    parser.add_argument("--transition-ref", required=True)
    parser.add_argument("--transition-sha256", required=True)
    parser.add_argument("--prior-transition-sha256")
    parser.add_argument("--owner-decision")
    args = parser.parse_args()
    ledger = Path(args.ledger).resolve()
    candidate = Path(args.candidate).resolve()
    text = ledger.read_text(encoding="utf-8")
    text = replace_once(text, f"current_stage: {args.from_stage}", f"current_stage: {args.to_stage}")
    text = replace_once(text, "Next stage allowed: false", "Next stage allowed: true")

    lines = text.splitlines()
    matched = 0
    for index, line in enumerate(lines):
        if not line.startswith(f"| {args.from_stage} |"):
            continue
        columns = [item.strip() for item in line.strip().strip("|").split("|")]
        if columns[4] != "in_progress":
            raise SystemExit("from-stage row is not in_progress")
        columns[4] = "accepted"
        if args.owner_decision is not None:
            columns[8] = args.owner_decision
        lines[index] = "| " + " | ".join(columns) + " |"
        matched += 1
    if matched != 1:
        raise SystemExit(f"expected one from-stage row, observed {matched}")
    text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    prior_hash = args.prior_transition_sha256 or "none"
    text = update_detail(
        text,
        args.from_stage,
        f"- transition_receipt_sha256: `{prior_hash}`",
        f"- transition_receipt_sha256: `{args.transition_sha256}`",
    )
    expected_ref = f"- incoming_transition_receipt: `{args.transition_ref}`"
    expected_hash = f"- incoming_transition_receipt_sha256: `{args.transition_sha256}`"
    if expected_ref not in text:
        text = update_detail(
            text, args.to_stage, "- incoming_transition_receipt: `none`", expected_ref,
        )
    if expected_hash not in text:
        text = update_detail(
            text, args.to_stage, "- incoming_transition_receipt_sha256: `none`", expected_hash,
        )
    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.write_text(text, encoding="utf-8")
    print(f"source_sha256={sha256(ledger)}")
    print(f"candidate_sha256={sha256(candidate)}")


if __name__ == "__main__":
    main()
