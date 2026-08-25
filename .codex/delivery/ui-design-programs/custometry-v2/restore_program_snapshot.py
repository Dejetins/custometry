#!/usr/bin/env python3
"""Atomically restore one hash-pinned program snapshot to the live plan path."""

from __future__ import annotations

import argparse
import hashlib
import os
import tempfile
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--expected-source-sha256", required=True)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()
    source = Path(args.source).resolve()
    target = Path(args.target).resolve()
    if sha256(source) != args.expected_source_sha256:
        raise SystemExit("source snapshot hash mismatch")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("wb", dir=target.parent, prefix=f".{target.name}.", delete=False) as handle:
        handle.write(source.read_bytes())
        temporary = Path(handle.name)
    os.replace(temporary, target)
    print(f"applied_sha256={sha256(target)}")


if __name__ == "__main__":
    main()
