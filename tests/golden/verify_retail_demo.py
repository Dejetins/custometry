"""Verify deterministic demo-source evidence against its committed manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def canonical_digest(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    evidence = json.load(sys.stdin)
    if evidence.get("schema_version") != "1.0.0":
        fail(f"unsupported evidence schema: {evidence.get('schema_version')!r}")

    expected_counts = manifest["expected_counts"]
    actual_counts = evidence.get("counts", {})
    if actual_counts != expected_counts:
        fail(f"dataset counts drifted: expected={expected_counts!r}, actual={actual_counts!r}")

    expected_scenarios = set(manifest["scenarios"])
    actual_scenarios = evidence.get("scenarios", {})
    if set(actual_scenarios) != expected_scenarios:
        fail(
            "scenario evidence keys drifted: "
            f"expected={sorted(expected_scenarios)!r}, actual={sorted(actual_scenarios)!r}"
        )
    missing = {name: value for name, value in actual_scenarios.items() if not value}
    if missing:
        fail(f"declared scenarios lack direct evidence: {missing!r}")

    expected_kpis = manifest.get("expected_kpis")
    if expected_kpis is None:
        fail("manifest must commit expected_kpis")
    if evidence.get("kpis") != expected_kpis:
        fail(f"dataset KPI drifted: expected={expected_kpis!r}, actual={evidence.get('kpis')!r}")

    digest = canonical_digest(evidence)
    expected_digest = manifest.get("expected_evidence_sha256")
    if digest != expected_digest:
        fail(f"dataset evidence signature drifted: expected={expected_digest!r}, actual={digest!r}")
    print(f"deterministic demo evidence passed: sha256:{digest}")


if __name__ == "__main__":
    main()
