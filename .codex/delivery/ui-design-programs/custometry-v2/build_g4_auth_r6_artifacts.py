#!/usr/bin/env python3
"""Build the unique G4 r6 auth successor against current r5 program semantics."""

from __future__ import annotations

import argparse

import build_g4_auth_r4_artifacts as builder


builder.REVISION = 6
builder.REVISION_TAG = "r6"
builder.PROGRAM_REVISION = 5
builder.ART = builder.PROGRAM_DIR / "artifacts/g4-r6/family-auth-shell-auth-baseline-exception-auth"
builder.EVID = builder.PROGRAM_DIR / "evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth"
builder.INTAKE = builder.PROGRAM_DIR / "artifacts/g0-r5/ui-program-intake.json"
builder.BASELINE = builder.PROGRAM_DIR / "artifacts/g0-r5/platform-ui-baseline.json"
builder.BASE_CONTRACT = builder.PROGRAM_DIR / "artifacts/g3-r5/representative-shell-contract.json"
builder.TARGET = builder.ART / "screens/auth-family.html"
builder.SNAPSHOT = builder.ART / "ui-design-program.snapshot.json"
builder.FAMILY_REVISION_ID = f"{builder.FAMILY_ID}-r6"
builder.STAGE_ID = f"G4@{builder.FAMILY_REVISION_ID}"
builder.HISTORICAL_PREDECESSOR_DECISION = (
    builder.PROGRAM_DIR
    / "evidence/g4-r5/family-auth-shell-auth-baseline-exception-auth/family-acceptance-decision-r5-03.json"
)


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
