#!/usr/bin/env python3
"""Capture and assemble the owned G4 reports proof chain."""

from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
source = HERE / "run_g4_an_r5_proof.py"
spec = importlib.util.spec_from_file_location("g4_rpt_proof", source)
if spec is None or spec.loader is None:
    raise RuntimeError("G4 proof runner cannot be loaded")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.ARTIFACT_DIR = HERE / "artifacts/g4-r5/family-rpt-shell-workspace-baseline"
base.EVIDENCE_DIR = HERE / "evidence/family.rpt.shell-workspace.baseline-r5"

if __name__ == "__main__":
    raise SystemExit(base.main())
