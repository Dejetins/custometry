#!/usr/bin/env python3
"""Run fresh canonical browser capture and G4 r6 auth-family proof."""

from __future__ import annotations

import argparse

import run_g4_auth_r5_proof as proof


proof.ART = proof.DIR / "artifacts/g4-r6/family-auth-shell-auth-baseline-exception-auth"
proof.EVID = proof.DIR / "evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth"
proof.TARGET = proof.ART / "screens/auth-family.html"
proof.REVISION_TAG = "r6"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("capture", "assemble"))
    args = parser.parse_args()
    (proof.capture if args.mode == "capture" else proof.assemble)()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
