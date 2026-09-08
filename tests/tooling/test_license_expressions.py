"""Real SPDX choice/conjunction semantics must never admit unlisted obligations."""

import json
from pathlib import Path

import pytest

from tools.custometry_quality import gate_licenses


@pytest.mark.parametrize(
    ("expression", "codes"),
    [
        ("MIT AND BSD-3-Clause", []),
        (" AND ".join(["(MIT OR BSD-3-Clause)"] * 7), ["license-not-allowed"]),
        ("MIT OR LGPL-2.1-only", []),
        ("MIT AND (BSD-3-Clause OR LGPL-2.1-only)", []),
        ("MIT AND PSF-2.0", ["license-not-allowed"]),
        ("MIT AND LGPL-2.1-only", ["license-review-required"]),
        ("MIT AND AGPL-3.0-only", ["license-denied"]),
        ("MIT AND UNKNOWN", ["license-unknown"]),
        ("MIT AND", ["license-not-allowed"]),
        ("MIT WITH Unknown-exception", ["license-not-allowed"]),
        ("(MIT OR BSD-3-Clause) AND PSF-2.0", ["license-not-allowed"]),
    ],
)
def test_expression_preserves_every_required_obligation(
    tmp_path: Path, expression: str, codes: list[str]
) -> None:
    (tmp_path / "bom.json").write_text(json.dumps({
        "bomFormat": "CycloneDX",
        "components": [
            {"type": "library", "name": "real-package", "licenses": [{"expression": expression}]},
            {"type": "operating-system", "name": "distribution-descriptor"},
        ],
    }))
    (tmp_path / "policy.json").write_text(json.dumps({
        "schema_version": 1,
        "allowed": ["MIT", "BSD-3-Clause"],
        "denied": ["AGPL-3.0-only"],
        "review_required": ["LGPL-2.1-only"],
    }))
    result = gate_licenses.check(tmp_path, Path("bom.json"), Path("policy.json"))
    assert [finding.code for finding in result.findings] == codes
    assert result.details["components_evaluated"] == 1

