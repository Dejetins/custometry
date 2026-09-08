"""A bounded component review cannot bypass policy or its actual evidence bindings."""

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from tools.custometry_quality import gate_licenses, license_reviews


def fixture(root: Path, license_id: str = "LGPL-2.1-only") -> dict[str, Any]:
    component = {"name": "library", "version": "1", "purl": "pkg:generic/library@1",
                 "licenses": [{"license": {"id": license_id}}]}
    (root / "bom.json").write_text(json.dumps({"bomFormat": "CycloneDX", "components": [component]}))
    (root / "policy.json").write_text(json.dumps({"schema_version": 1, "allowed": ["MIT"],
        "denied": ["AGPL-3.0-only"], "review_required": ["LGPL-2.1-only"]}))
    (root / "evidence.txt").write_text("Fixture evidence; not an actual distribution/legal review.\n")
    evidence = {"path": "evidence.txt", "sha256": hashlib.sha256((root / "evidence.txt").read_bytes()).hexdigest(),
                "size_bytes": (root / "evidence.txt").stat().st_size}
    return {
        "schema_version": 1, "subjects": ["sha256:" + "a" * 64],
        "policy_sha256": hashlib.sha256((root / "policy.json").read_bytes()).hexdigest(),
        "sbom_sha256": hashlib.sha256((root / "bom.json").read_bytes()).hexdigest(),
        "components": [{
            "name": "library", "version": "1", "purl": "pkg:generic/library@1",
            "declaration_sha256": license_reviews.declaration_digest(component), "review": evidence,
            "obligations": [{"kind": kind, "status": "verified", "evidence": [evidence]}
                            for kind in ["notice", "corresponding-source", "relinking"]],
        }],
    }


@pytest.mark.parametrize("mutation", [
    "none", "subject", "policy", "sbom", "version", "license", "evidence", "unfulfilled", "no-source", "no-relinking",
])
def test_review_requires_exact_context_and_every_obligation(tmp_path: Path, mutation: str) -> None:
    record = fixture(tmp_path)
    if mutation == "subject":
        record["subjects"] = ["sha256:" + "b" * 64]
    elif mutation in {"policy", "sbom"}:
        record[mutation + "_sha256"] = "b" * 64
    elif mutation == "version":
        record["components"][0]["version"] = "2"
    elif mutation == "license":
        record["components"][0]["declaration_sha256"] = "b" * 64
    elif mutation == "evidence":
        (tmp_path / "evidence.txt").write_text("altered")
    elif mutation == "unfulfilled":
        record["components"][0]["obligations"][0]["status"] = "pending"
    elif mutation in {"no-source", "no-relinking"}:
        index = 1 if mutation == "no-source" else 2
        record["components"][0]["obligations"].pop(index)
    (tmp_path / "review.json").write_text(json.dumps(record))
    result = gate_licenses.check(tmp_path, Path("bom.json"), Path("policy.json"),
        reviews=Path("review.json"), expected_subjects=["sha256:" + "a" * 64])
    assert result.ok is (mutation == "none")
    # The original default gate still blocks this license without explicit review.
    assert not gate_licenses.check(tmp_path, Path("bom.json"), Path("policy.json")).ok


@pytest.mark.parametrize("license_id", ["AGPL-3.0-only", "SSPL-1.0", "UNKNOWN", "sha256:1234", "LicenseRef-unknown"])
def test_review_cannot_admit_prohibited_or_unresolved_licenses(tmp_path: Path, license_id: str) -> None:
    record = fixture(tmp_path, license_id)
    (tmp_path / "review.json").write_text(json.dumps(record))
    assert not gate_licenses.check(tmp_path, Path("bom.json"), Path("policy.json"),
        reviews=Path("review.json"), expected_subjects=["sha256:" + "a" * 64]).ok
