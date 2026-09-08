"""Native compilation and vulnerability bindings reject missing/altered evidence."""
from __future__ import annotations

import copy
import json
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest

from tools.custometry_quality import delivery_native as native

SUBJECT = "sha256:" + "a" * 64


def compilation_fixture() -> tuple[dict[str, Any], dict[str, Any]]:
    row: dict[str, Any] = {"path": "cpp/vendored/header.h", "sha256": "b" * 64, "size_bytes": 10}
    key = "arrow-source/" + row["path"]
    pins = {"internal_native": [{"name": "example", "files": [row]}]}
    proof = {"schema_version": 2, "method": "ninja-complete-deps-and-ar-members/v2",
             "inputs": [{**row, "path": key}],
             "objects": [{"path": "arrow-build/object.o", "inputs": [key], "dependency_count": 1}],
             "internal_coverage": [{"name": "example", "inputs": [key], "objects": ["arrow-build/object.o"]}]}
    return pins, proof


@pytest.mark.parametrize("failure", [None, "hash", "missing_input", "missing_object", "missing_component", "object_binding"])
def test_compilation_coverage(failure: str | None) -> None:
    pins, proof = compilation_fixture()
    if failure == "hash":
        proof["inputs"][0]["sha256"] = "c" * 64
    elif failure == "missing_input":
        proof["inputs"] = []
    elif failure == "missing_object":
        proof["objects"] = []
    elif failure == "missing_component":
        proof["internal_coverage"] = []
    elif failure == "object_binding":
        proof["objects"][0]["inputs"] = []
    if failure:
        with pytest.raises(ValueError):
            native.validate_compilation(proof, pins)
    else:
        native.validate_compilation(proof, pins)


def report_fixture(now: datetime) -> dict[str, Any]:
    return {"descriptor": {"name": "grype", "version": "0.118.0",
                           "db": {"status": {"valid": True, "schemaVersion": "v6.1.9", "built": now.isoformat()}},
                           "configuration": {"only-fixed": False, "only-notfixed": False, "exclude": []}},
            "source": {"type": "sbom-file", "target": "/actual/sbom.json"}, "matches": []}


@pytest.mark.parametrize("failure", ["tool", "subject", "stale", "future", "filtered", "ignored"])
def test_grype_binding_fails_closed(failure: str) -> None:
    now = datetime.now(timezone.utc)
    report = report_fixture(now)
    if failure == "tool":
        report["descriptor"]["version"] = "0.1.0"
    elif failure == "subject":
        report["source"]["target"] = "/different/sbom.json"
    elif failure in {"stale", "future"}:
        report["descriptor"]["db"]["status"]["built"] = (now + timedelta(hours=-25 if failure == "stale" else 1)).isoformat()
    elif failure == "filtered":
        report["descriptor"]["configuration"]["only-fixed"] = True
    else:
        report["ignoredMatches"] = [{"vulnerability": {"id": "not silently ignored"}}]
    with pytest.raises(ValueError):
        native.grype_result(report, SUBJECT, "/actual/sbom.json", now)


def test_raw_critical_and_unknown_remain_failures() -> None:
    now = datetime.now(timezone.utc)
    report = report_fixture(now)
    assert native.grype_result(report, SUBJECT, "/actual/sbom.json", now)["status"] == "pass"
    for severity in ("Critical", "Unknown", None):
        changed = copy.deepcopy(report)
        changed["matches"] = [{"vulnerability": {"severity": severity}}]
        assert native.grype_result(changed, SUBJECT, "/actual/sbom.json", now)["status"] == "fail"


@pytest.mark.parametrize("failure", [None, "external_iobuf", "unknown", "another_critical", "subject"])
def test_exact_folly_resolution_keeps_raw_findings(failure: str | None) -> None:
    pins, proof = compilation_fixture()
    source = "cpp/src/arrow/vendored/ProducerConsumerQueue.h"
    old_key = proof["inputs"][0]["path"]
    key = "arrow-source/" + source
    pins["internal_native"][0].update(name="folly", version="2021.02.15.00", purl="pkg:generic/folly@2021.02.15.00")
    pins["internal_native"][0]["files"][0]["path"] = source
    proof["inputs"][0]["path"] = key
    proof["objects"][0]["inputs"] = [key]
    proof["internal_coverage"][0].update(name="folly", inputs=[key])
    assert old_key != key
    if failure == "external_iobuf":
        external = "builder-system/usr/include/folly/io/IOBuf.h"
        proof["inputs"].append({"path": external, "sha256": "c" * 64, "size_bytes": 20})
        proof["objects"][0]["inputs"].append(external)
        proof["objects"][0]["dependency_count"] = 2
    digest = native.bundle.digest((json.dumps(proof, sort_keys=True, separators=(",", ":")) + "\n").encode())
    cpe = "cpe:2.3:a:facebook:folly:2021.02.15.00:*:*:*:*:*:*:*"
    component = {"name": "folly", "version": "2021.02.15.00", "purl": "pkg:generic/folly@2021.02.15.00", "cpe": cpe,
                 "properties": [{"name": "custometry:native:compilation-sha256", "value": digest}]}
    sbom = {"components": [component], "metadata": {"properties": [{"name": native.SUBJECT_PROPERTY, "value": SUBJECT}]}}
    now = datetime.now(timezone.utc)
    report = report_fixture(now)
    report["matches"] = [{"vulnerability": {"id": "CVE-2021-24036", "severity": "Critical", "namespace": "nvd:cpe"},
                          "artifact": {"name": "folly", "version": component["version"], "purl": component["purl"], "cpes": [cpe]}}]
    if failure in {"unknown", "another_critical"}:
        report["matches"].append({"vulnerability": {"id": "unresolved", "severity": "Unknown" if failure == "unknown" else "Critical"},
                                  "artifact": {"name": "other"}})
    original = copy.deepcopy(report)
    if failure in {"external_iobuf", "subject"}:
        with pytest.raises(ValueError):
            native.folly_applicability(report, sbom, proof, pins, "sha256:" + "d" * 64 if failure == "subject" else SUBJECT)
    else:
        raw = native.grype_result(report, SUBJECT, "/actual/sbom.json", now)
        result = native.apply_resolutions(raw, report, native.folly_applicability(report, sbom, proof, pins, SUBJECT))
        assert result["critical"] == raw["critical"] >= 1
        assert result["status"] == ("pass" if failure is None else "fail")
        assert len(result["resolutions"]) == 1
    assert report == original
