"""Bind source-built Arrow dependencies to the actual selected image filesystem."""
from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any

from . import delivery_bundle as bundle
from .gate_sbom import SUBJECT_PROPERTY

PREFIX = "app/.venv/lib/python3.12/site-packages/"


def arrow_sbom(provenance: dict[str, Any], pins: dict[str, Any], pins_sha: str,
               inventory: list[dict[str, Any]], subject: str,
               license_declarations: dict[str, Any] | None = None,
               compilation: dict[str, Any] | None = None) -> dict[str, Any]:
    bundle.require(re.fullmatch(r"sha256:[a-f0-9]{64}", subject) is not None)
    bundle.require(provenance.get("schema_version") == 1 and provenance.get("pins_sha256") == pins_sha
                   and provenance.get("arrow") == pins["arrow"]
                   and provenance.get("native_sources") == pins["native"], "DELIVERY_NATIVE_SOURCE_MISMATCH")
    bundle.require(provenance.get("internal_native") == pins["internal_native"], "DELIVERY_NATIVE_SOURCE_MISMATCH")
    files = bundle.unique(provenance["native_files"], "path")
    actual = {row["path"]: row for row in inventory}
    expected = {path.removeprefix(PREFIX) for path in actual if path.startswith(PREFIX + "pyarrow/")
                and re.search(r"\.so(?:\.|$)", path)}
    bundle.require(set(files) == expected and bool(files), "DELIVERY_NATIVE_COVERAGE")
    for path, declared in files.items():
        bundle.safe_path(path)
        row = actual[PREFIX + path]
        bundle.require(row.get("sha256") == declared["sha256"] and row.get("size_bytes") == declared["size_bytes"],
                       "DELIVERY_SUBJECT_MISMATCH")
    notices: dict[str, list[dict[str, Any]]] = {}
    for notice in provenance["native_notices"]:
        bundle.safe_path(notice["path"])
        observed = actual.get("app/notices/pyarrow-native/" + notice["path"], {})
        bundle.require(observed.get("sha256") == notice["sha256"] and observed.get("size_bytes") == notice["size_bytes"],
                       "DELIVERY_NATIVE_NOTICE_MISSING")
        notices.setdefault(notice["component"], []).append(notice)
    bundle.require(set(notices) == {row["name"] for row in pins["native"]} | {"arrow-internal"}, "DELIVERY_NATIVE_NOTICE_MISSING")
    compiled = provenance["compilation"]
    observed_compiled = actual.get("app/notices/pyarrow-compilation-inputs.json", {})
    bundle.require(observed_compiled.get("sha256") == compiled["sha256"]
                   and observed_compiled.get("size_bytes") == compiled["size_bytes"], "DELIVERY_NATIVE_COVERAGE")
    bundle.require(compilation is not None, "DELIVERY_NATIVE_COVERAGE")
    assert compilation is not None
    compiled_bytes = (json.dumps(compilation, sort_keys=True, separators=(",", ":")) + "\n").encode()
    bundle.require(bundle.digest(compiled_bytes) == compiled["sha256"] and len(compiled_bytes) == compiled["size_bytes"],
                   "DELIVERY_NATIVE_COVERAGE")
    validate_compilation(compilation, pins)
    if license_declarations is not None:
        bundle.require(set(license_declarations) == {row["name"] for row in pins["native"]}, "DELIVERY_NATIVE_LICENSE_MISMATCH")
        validate_runtime_license_scope(compilation, provenance, pins)
    options = provenance["cmake_options"]
    bundle.require(all(options.get("ARROW_" + name) == "ON" for name in ("IPC", "PARQUET", "FILESYSTEM", "COMPUTE", "DATASET"))
                   and all(options.get("ARROW_" + name) == "OFF" for name in ("FLIGHT", "S3", "GCS", "AZURE", "GANDIVA"))
                   and options.get("PARQUET_REQUIRE_ENCRYPTION") == "OFF"
                   and options.get("CMAKE_INSTALL_RPATH") == "$ORIGIN", "DELIVERY_NATIVE_PROFILE")
    components: list[dict[str, Any]] = []
    for source in pins["native"]:
        component = {"type": "library", "name": source["name"], "version": source["version"],
                     "purl": source["purl"], "cpe": source["cpe"],
                     "bom-ref": "custometry-native:" + source["name"],
                     "properties": [{"name": "custometry:native:source-archive-sha256", "value": source["sha256"]},
                                    {"name": "custometry:native:build-pins-sha256", "value": pins_sha}]}
        if license_declarations is not None:
            declaration = license_declarations[source["name"]]
            bundle.require(declaration["source_sha256"] == source["sha256"]
                           and bool(declaration["notice_sha256"])
                           and all(any(notice["sha256"] == expected for notice in notices[source["name"]])
                                   for expected in declaration["notice_sha256"]), "DELIVERY_NATIVE_LICENSE_MISMATCH")
            component["licenses"] = [{"expression": declaration["expression"]}]
        components.append(component)
    for source in pins["internal_native"]:
        component = {"type": "library", "name": source["name"], "version": source["version"],
                     "purl": source["purl"], "bom-ref": "custometry-arrow-vendored:" + source["name"],
                     "licenses": [{"expression": source["declared_runtime_license"]}],
                     "properties": [{"name": "custometry:native:source-archive-sha256", "value": pins["arrow"]["sha256"]},
                                    {"name": "custometry:native:build-pins-sha256", "value": pins_sha},
                                    {"name": "custometry:native:compilation-sha256", "value": compiled["sha256"]}]}
        if "cpe" in source:
            component["cpe"] = source["cpe"]
        components.append(component)
    return {"bomFormat": "CycloneDX", "specVersion": "1.6", "version": 1,
            "metadata": {"properties": [{"name": SUBJECT_PROPERTY, "value": subject}]},
            "components": components}


def validate_compilation(compilation: dict[str, Any], pins: dict[str, Any]) -> None:
    bundle.require(compilation.get("schema_version") == 2
                   and compilation.get("method") == "ninja-complete-deps-and-ar-members/v2", "DELIVERY_NATIVE_COVERAGE")
    inputs = bundle.unique(compilation["inputs"], "path")
    objects = bundle.unique(compilation["objects"], "path")
    coverage = bundle.unique(compilation["internal_coverage"], "name")
    bundle.require(bool(objects) and set(coverage) == {row["name"] for row in pins["internal_native"]}, "DELIVERY_NATIVE_COVERAGE")
    referenced: set[str] = set()
    for row in objects.values():
        bundle.require(type(row["dependency_count"]) is int and row["dependency_count"] == len(row["inputs"])
                       and bool(row["inputs"]) and all(key in inputs for key in row["inputs"]), "DELIVERY_NATIVE_COVERAGE")
        referenced.update(row["inputs"])
    bundle.require(referenced == set(inputs), "DELIVERY_NATIVE_COVERAGE")
    for component in pins["internal_native"]:
        selected: dict[str, Any] = {}
        for item in component["files"]:
            key = "arrow-source/" + item["path"]
            if key in inputs:
                bundle.require(inputs[key] == {**item, "path": key}, "DELIVERY_NATIVE_SOURCE_MISMATCH")
                selected[key] = inputs[key]
        observed = coverage[component["name"]]
        expected_objects = sorted(row["path"] for row in objects.values() if set(row["inputs"]) & selected.keys())
        bundle.require(bool(selected) and observed["inputs"] == sorted(selected)
                       and sorted(observed["objects"]) == expected_objects and bool(expected_objects), "DELIVERY_NATIVE_COVERAGE")


def validate_runtime_license_scope(compilation: dict[str, Any], provenance: dict[str, Any], pins: dict[str, Any]) -> None:
    inputs = bundle.unique(compilation["inputs"], "path")
    for component in pins["native"]:
        name = component["name"]
        selected = [path for path in inputs if "/" + name + "_ep" in path]
        bundle.require(bool(selected), "DELIVERY_NATIVE_COVERAGE")
        if name == "lz4":
            prefixes = ("arrow-build/lz4_ep-prefix/src/lz4_ep/lib/", "arrow-build/lz4_ep-install/include/")
            bundle.require(all(path.startswith(prefixes) for path in selected), "DELIVERY_NATIVE_LICENSE_SCOPE")
        elif name == "thrift":
            prefixes = ("arrow-build/thrift_ep-prefix/src/thrift_ep/lib/cpp/src/thrift/", "arrow-build/thrift_ep-install/include/thrift/")
            bundle.require(all((path.startswith(prefixes) or path == "arrow-build/thrift_ep-prefix/src/thrift_ep-build/thrift/config.h")
                               and "windows" not in path.lower() and "socketpair" not in path.lower() for path in selected),
                           "DELIVERY_NATIVE_LICENSE_SCOPE")
        elif name == "rapidjson":
            bundle.require(all(path.startswith("arrow-build/rapidjson_ep/src/rapidjson_ep-install/include/rapidjson/")
                               and "/msinttypes/" not in path for path in selected), "DELIVERY_NATIVE_LICENSE_SCOPE")
    observations = provenance["source_modification_observations"]
    bundle.require({row["source_path"] for row in observations} == {"utf8proc.c", "utf8proc.h", "utf8proc_data.c"}
                   and len(observations) == 3, "DELIVERY_NATIVE_LICENSE_SCOPE")
    for row in observations:
        expected = inputs["arrow-build/utf8proc_ep-prefix/src/utf8proc_ep/" + row["source_path"]]
        bundle.require(row["component"] == "utf8proc" and row["modified"] is False
                       and row["upstream_sha256"] == row["compiled_source_sha256"] == expected["sha256"],
                       "DELIVERY_NATIVE_LICENSE_SCOPE")


def grype_result(report: dict[str, Any], subject: str, expected_input: str, now: datetime) -> dict[str, Any]:
    bundle.require(re.fullmatch(r"sha256:[a-f0-9]{64}", subject) is not None)
    descriptor = report.get("descriptor", {})
    bundle.require(descriptor.get("name") == "grype" and descriptor.get("version") == "0.118.0", "DELIVERY_TOOL_MISMATCH")
    bundle.require(report.get("source") == {"type": "sbom-file", "target": expected_input}, "DELIVERY_SUBJECT_MISMATCH")
    db = descriptor.get("db", {}).get("status", {})
    bundle.require(db.get("valid") is True and db.get("schemaVersion") == "v6.1.9", "DELIVERY_SCAN_STALE")
    built = datetime.fromisoformat(db["built"].replace("Z", "+00:00"))
    bundle.require(built.tzinfo is not None and 0 <= (now - built).total_seconds() <= 24 * 3600, "DELIVERY_SCAN_STALE")
    configuration = descriptor.get("configuration", {})
    bundle.require(configuration.get("only-fixed") is False and configuration.get("only-notfixed") is False
                   and configuration.get("ignore-wontfix") in {"", None} and configuration.get("exclude") == []
                   and not report.get("ignoredMatches"), "DELIVERY_SCAN_FILTERED")
    matches: list[dict[str, Any]] = report["matches"]
    critical = sum(match["vulnerability"].get("severity") == "Critical" for match in matches)
    unknown = sum(match["vulnerability"].get("severity") not in {"Negligible", "Low", "Medium", "High", "Critical"} for match in matches)
    return {"subject": subject, "scanner": "grype-0.118.0", "database_built": db["built"],
            "critical": critical, "unknown_severity": unknown, "findings": len(matches),
            "status": "pass" if not critical and not unknown else "fail"}


def folly_applicability(report: dict[str, Any], sbom: dict[str, Any], compilation: dict[str, Any],
                        pins: dict[str, Any], subject: str) -> list[dict[str, Any]]:
    """Resolve only IOBuf's CVE against complete exact-subset compiler evidence.

    Raw matches are never removed. This helper is called only after the native
    SBOM/provenance/compiled bytes have been bound to the selected image.
    """
    validate_compilation(compilation, pins)
    bundle.require(re.fullmatch(r"sha256:[a-f0-9]{64}", subject) is not None
                   and {row["value"] for row in sbom["metadata"]["properties"] if row["name"] == SUBJECT_PROPERTY} == {subject},
                   "DELIVERY_SUBJECT_MISMATCH")
    components = [row for row in sbom["components"] if row.get("name") == "folly"]
    bundle.require(len(components) == 1, "DELIVERY_NATIVE_COVERAGE")
    component = components[0]
    compilation_sha = bundle.digest((json.dumps(compilation, sort_keys=True, separators=(",", ":")) + "\n").encode())
    bundle.require({row["value"] for row in component["properties"] if row["name"] == "custometry:native:compilation-sha256"} == {compilation_sha},
                   "DELIVERY_NATIVE_COVERAGE")
    pinned = [row for row in pins["internal_native"] if row["name"] == "folly"]
    bundle.require(len(pinned) == 1 and component["version"] == pinned[0]["version"] == "2021.02.15.00"
                   and component["purl"] == pinned[0]["purl"] == "pkg:generic/folly@2021.02.15.00"
                   and {row["path"] for row in pinned[0]["files"]} == {"cpp/src/arrow/vendored/ProducerConsumerQueue.h"},
                   "DELIVERY_NATIVE_SOURCE_MISMATCH")
    paths = [value for row in compilation["inputs"] for key in ("path", "resolved_path") if (value := row.get(key))]
    # Complete dependencies include builder system headers and symlink identities.
    # Any IOBuf input invalidates this exact absence proof, irrespective of origin.
    bundle.require(not any("iobuf" in path.lower() for path in paths), "DELIVERY_APPLICABILITY_UNPROVEN")
    bundle.require(not any("/folly/" in path.lower() for path in paths), "DELIVERY_APPLICABILITY_UNPROVEN")
    resolutions: list[dict[str, Any]] = []
    for match in report["matches"]:
        vulnerability = match["vulnerability"]
        artifact = match["artifact"]
        if (vulnerability.get("id") != "CVE-2021-24036" or artifact.get("name") != "folly"
                or artifact.get("version") != component["version"] or artifact.get("purl") != component["purl"]):
            continue
        bundle.require(vulnerability.get("namespace") == "nvd:cpe"
                       and component["cpe"] in artifact.get("cpes", []), "DELIVERY_APPLICABILITY_UNPROVEN")
        resolutions.append({"vulnerability": "CVE-2021-24036", "component_purl": component["purl"],
                            "raw_match_sha256": bundle.digest(json.dumps(match, sort_keys=True, separators=(",", ":")).encode()),
                            "subject": subject, "status": "not_affected", "reason": "vulnerable_code_not_present",
                            "advisory_fix": "https://github.com/facebook/folly/commit/4f304af1411e68851bdd00ef6140e9de4616f7d3",
                            "affected_source": "folly/io/IOBuf.cpp", "observed_subset": "ProducerConsumerQueue.h",
                            "compilation_sha256": compilation_sha})
    return resolutions


def apply_resolutions(raw: dict[str, Any], report: dict[str, Any], resolutions: list[dict[str, Any]]) -> dict[str, Any]:
    """Keep raw counts; accept no unresolved Critical or unknown-severity match."""
    by_hash = {row["raw_match_sha256"]: row for row in resolutions}
    bundle.require(len(by_hash) == len(resolutions))
    critical_resolved = 0
    observed: set[str] = set()
    for match in report["matches"]:
        key = bundle.digest(json.dumps(match, sort_keys=True, separators=(",", ":")).encode())
        if key in by_hash:
            bundle.require(by_hash[key]["subject"] == raw["subject"] and by_hash[key]["status"] == "not_affected")
            observed.add(key)
            critical_resolved += match["vulnerability"].get("severity") == "Critical"
    bundle.require(observed == set(by_hash) and critical_resolved <= raw["critical"])
    remaining = raw["critical"] - critical_resolved
    return {**raw, "critical_applicable": remaining, "resolutions": resolutions,
            "status": "pass" if not remaining and not raw["unknown_severity"] else "fail"}
