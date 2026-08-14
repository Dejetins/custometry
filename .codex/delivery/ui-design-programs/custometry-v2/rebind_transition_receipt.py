#!/usr/bin/env python3
"""Prepare a CAS candidate that rebinds one outgoing/incoming transition pair."""

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
    parser.add_argument("--old-sha256", required=True)
    parser.add_argument("--new-sha256", required=True)
    parser.add_argument("--expected-count", type=int, default=2)
    args = parser.parse_args()
    ledger = Path(args.ledger).resolve()
    candidate = Path(args.candidate).resolve()
    text = ledger.read_text(encoding="utf-8")
    old = f"`{args.old_sha256}`"
    new = f"`{args.new_sha256}`"
    count = text.count(old)
    if count != args.expected_count:
        raise SystemExit(f"expected {args.expected_count} exact transition hash bindings, observed {count}")
    rendered = text.replace(old, new)
    candidate.parent.mkdir(parents=True, exist_ok=True)
    candidate.write_text(rendered, encoding="utf-8")
    print(f"source_sha256={sha256(ledger)}")
    print(f"candidate_sha256={sha256(candidate)}")


if __name__ == "__main__":
    main()
