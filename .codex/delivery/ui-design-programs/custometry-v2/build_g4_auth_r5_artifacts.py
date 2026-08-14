#!/usr/bin/env python3
"""Build the G4 r5 auth family through the revision-parameterized canonical builder."""

from __future__ import annotations

import argparse

import build_g4_auth_r4_artifacts as builder


builder.REVISION = 5
builder.REVISION_TAG = "r5"
builder.ART = builder.PROGRAM_DIR / "artifacts/g4-r5/family-auth-shell-auth-baseline-exception-auth"
builder.EVID = builder.PROGRAM_DIR / "evidence/g4-r5/family-auth-shell-auth-baseline-exception-auth"
builder.BASE_CONTRACT = builder.PROGRAM_DIR / "artifacts/g3-r4/representative-shell-contract.json"
builder.TARGET = builder.ART / "screens/auth-family.html"
builder.SNAPSHOT = builder.ART / "ui-design-program.snapshot.json"
builder.FAMILY_REVISION_ID = f"{builder.FAMILY_ID}-r5"
builder.STAGE_ID = f"G4@{builder.FAMILY_REVISION_ID}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("bootstrap", "bind", "proof-requests", "review"))
    args = parser.parse_args()
    {
        "bootstrap": builder.bootstrap,
        "bind": builder.bind,
        "proof-requests": builder.proof_requests,
        "review": builder.review,
    }[args.mode]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
