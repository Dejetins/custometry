#!/usr/bin/env python3
"""Run canonical browser capture and proof for G4 r5 onboarding."""

from __future__ import annotations

import argparse
import run_g4_auth_r5_proof as proof


proof.ART = proof.DIR / "artifacts/g4-r5/family-auth-shell-workspace-baseline"
proof.EVID = proof.DIR / "evidence/family.auth.shell-workspace.baseline-r5"
proof.TARGET = proof.ART / "screens/onboarding.html"
proof.REVISION_TAG = "r5"
proof.EXPECTED_CONTRACTS = 6


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("capture", "assemble"))
    args = parser.parse_args()
    (proof.capture if args.mode == "capture" else proof.assemble)()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
