"""Whole-set source/license proof uses actual verified companion bytes."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from tools.custometry_quality import delivery_bundle as bundle
from tools.custometry_quality import delivery_obligations as obligations
from tools.custometry_quality import license_reviews


def fixture(root: Path, failure: str | None) -> dict[str, Any]:
    main = root / "main"
    main.mkdir()
    source = root / "companions/01/sources/library.tar.gz"
    source.parent.mkdir(parents=True)
    source.write_bytes(b"opaque fixture source; not actual license compliance")
    source_record = bundle.file_record("sources/library.tar.gz", source.read_bytes(), "source")
    files: list[dict[str, Any]] = []

    def write(name: str, raw: bytes) -> dict[str, Any]:
        target = main / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        record = bundle.file_record(name, raw, "evidence")
        files.append(record)
        return {key: record[key] for key in ("path", "sha256", "size_bytes")}

    notice = write("notices/library.txt", b"Synthetic notice and review; this test grants no real approval.")
    source_evidence = {key: source_record[key] for key in ("path", "sha256", "size_bytes")}
    images: dict[str, Any] = {}
    closure: list[dict[str, Any]] = []
    for role in ("api", "web", "postgres"):
        platforms: list[dict[str, Any]] = []
        for architecture in ("amd64", "arm64"):
            subject = "sha256:" + bundle.digest((role + architecture).encode())
            platforms.append({"architecture": architecture, "digest": subject})
            component = {"name": "library", "version": "1", "purl": "pkg:generic/library@1",
                         "licenses": [{"license": {"id": "LGPL-2.1-only"}}]}
            sbom: dict[str, Any] = {"bomFormat": "CycloneDX", "specVersion": "1.6", "components": [component],
                    "metadata": {"properties": [{"name": "custometry:subject-digest", "value": subject}]}}
            if failure == "sbom_subject":
                sbom["metadata"]["properties"] = []
            bom = write(f"evidence/{role}-{architecture}-sbom.json", json.dumps(sbom).encode())
            review: dict[str, Any] = {"schema_version": 2, "subjects": [subject], "sbom_sha256": bom["sha256"],
                      "policy_sha256": bundle.digest((bundle.ROOT / "deploy/license-policy.json").read_bytes()),
                      "components": [{"name": "library", "version": "1", "purl": component["purl"],
                                      "declaration_sha256": license_reviews.declaration_digest(component), "review": notice,
                                      "obligations": [{"kind": kind, "status": "verified", "evidence": [evidence]}
                                                      for kind, evidence in (("notice", notice), ("corresponding-source", source_evidence), ("relinking", notice))]}]}
            if failure == "missing_obligation":
                review["components"][0]["obligations"].pop(1)
            review_name = f"evidence/{role}-{architecture}-review.json"
            write(review_name, json.dumps(review).encode())
            closure.append({"subject": subject, "sbom_path": bom["path"], "reviews_path": review_name})
        images[role] = {"platforms": platforms}
    record = {"files": files, "companions": [{"part": 1, "files": [source_record]}],
              "images": images, "license_closure": closure}
    if failure == "changed_source":
        source.write_bytes(b"modified source")
    elif failure == "missing_source":
        source.unlink()
    elif failure == "unbound_source":
        record["companions"] = []
    elif failure == "missing_subject":
        closure.pop()
    elif failure == "linked_source":
        other = source.with_name("other")
        source.rename(other)
        source.symlink_to(other)
    return record


@pytest.mark.parametrize("failure", [None, "changed_source", "missing_source", "unbound_source", "missing_subject",
                                    "linked_source", "missing_obligation", "sbom_subject"])
def test_whole_set_obligations_are_bound_before_promotion(tmp_path: Path, failure: str | None) -> None:
    record = fixture(tmp_path, failure)
    if failure:
        with pytest.raises(ValueError):
            obligations.verify(record, tmp_path)
    else:
        obligations.verify(record, tmp_path)


def test_legacy_review_cannot_resolve_unsigned_relative_evidence_in_v2(tmp_path: Path) -> None:
    record = fixture(tmp_path, None)
    raw = b"unsigned legacy relative evidence"
    extra = tmp_path / "main/evidence/legacy-evidence.txt"
    extra.write_bytes(raw)
    legacy = {"path": extra.name, "sha256": bundle.digest(raw), "size_bytes": len(raw)}
    for declaration in record["license_closure"]:
        path = tmp_path / "main" / declaration["reviews_path"]
        review = json.loads(path.read_bytes())
        review["schema_version"] = 1
        review["components"][0]["review"] = legacy
        for obligation in review["components"][0]["obligations"]:
            obligation["evidence"] = [legacy]
        data = json.dumps(review).encode()
        path.write_bytes(data)
        item = next(row for row in record["files"] if row["path"] == declaration["reviews_path"])
        item.update(sha256=bundle.digest(data), size_bytes=len(data))
    record["companions"] = []
    with pytest.raises(ValueError, match="DELIVERY_LICENSE_CLOSURE_INVALID"):
        obligations.verify(record, tmp_path)
