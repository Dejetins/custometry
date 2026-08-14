#!/usr/bin/env python3
"""Prepare an atomic claim candidate for the ledger-selected current row."""

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
    parser.add_argument("--claim-id", required=True)
    parser.add_argument("--claimed-at", required=True)
    args = parser.parse_args()
    ledger = Path(args.ledger).resolve()
    candidate = Path(args.candidate).resolve()
    text = ledger.read_text(encoding="utf-8")
    if f"current_stage: {args.stage_id}" not in text:
        raise SystemExit("requested stage is not the ledger current_stage")
    if text.count("Next stage allowed: true") != 1:
        raise SystemExit("ledger does not expose exactly one claimable boundary")

    lines = text.splitlines()
    matched = 0
    for index, line in enumerate(lines):
        if not line.startswith(f"| {args.stage_id} |"):
            continue
        columns = [item.strip() for item in line.strip().strip("|").split("|")]
        if len(columns) != 11:
            raise SystemExit("stage row shape is invalid")
        if columns[4] != "pending" or columns[9] != "—" or columns[10] != "—":
            raise SystemExit("stage row is not pending and unclaimed")
        columns[4] = "in_progress"
        columns[9] = args.claim_id
        columns[10] = args.claimed_at
        lines[index] = "| " + " | ".join(columns) + " |"
        matched += 1
    if matched != 1:
        raise SystemExit(f"expected one stage row, observed {matched}")
    rendered = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    rendered = rendered.replace("Next stage allowed: true", "Next stage allowed: false", 1)
    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.write_text(rendered, encoding="utf-8")
    print(f"source_sha256={sha256(ledger)}")
    print(f"candidate_sha256={sha256(candidate)}")


if __name__ == "__main__":
    main()
