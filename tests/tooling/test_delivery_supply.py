"""Synthetic hostile-input tests; no hosted producer/scanner/signature proof."""

from __future__ import annotations

import copy
import io
import json
import tarfile
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pytest
import yaml

from tools.custometry_quality import delivery_supply as supply

SUBJECT = "sha256:" + "a" * 64
NOW = datetime(2026, 9, 8, tzinfo=timezone.utc)


def scan_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    report: dict[str, Any] = {
        "CreatedAt": NOW.isoformat(),
        "SchemaVersion": 2,
        "ArtifactType": "container_image",
        "Metadata": {"RepoDigests": ["ghcr.io/dejetins/custometry-api@" + SUBJECT]},
        "Results": [{"Vulnerabilities": []}],
    }
    db = {
        "Version": "0.74.0",
        "VulnerabilityDB": {
            "Version": 2,
            "UpdatedAt": NOW.isoformat(),
            "NextUpdate": (NOW + timedelta(hours=12)).isoformat(),
        },
    }
    return report, db


def test_fresh_subject_bound_scan() -> None:
    report, db = scan_inputs()
    assert supply.vulnerability_result(report, db, SUBJECT, NOW)["status"] == "pass"


@pytest.mark.parametrize(
    "change",
    [
        "stale-report",
        "stale-db",
        "future-db",
        "expired-db",
        "wrong-version",
        "wrong-subject",
        "empty-results",
    ],
)
def test_reject_unusable_scanner_evidence(change: str) -> None:
    report, db = scan_inputs()
    if change == "stale-report":
        report["CreatedAt"] = (NOW - timedelta(hours=25)).isoformat()
    if change == "stale-db":
        db["VulnerabilityDB"]["UpdatedAt"] = (NOW - timedelta(hours=25)).isoformat()
    if change == "future-db":
        db["VulnerabilityDB"]["UpdatedAt"] = (NOW + timedelta(hours=1)).isoformat()
    if change == "expired-db":
        db["VulnerabilityDB"]["NextUpdate"] = NOW.isoformat()
    if change == "wrong-version":
        db["Version"] = "0.1.0"
    if change == "wrong-subject":
        report["Metadata"]["RepoDigests"] = []
    if change == "empty-results":
        report["Results"] = []
    with pytest.raises(ValueError):
        supply.vulnerability_result(report, db, SUBJECT, NOW)


@pytest.mark.parametrize("severity", ["CRITICAL", "UNKNOWN", None])
def test_unresolved_severity_blocks_supply(severity: str | None) -> None:
    report, db = scan_inputs()
    report["Results"][0]["Vulnerabilities"] = [{"Severity": severity}]
    assert supply.vulnerability_result(report, db, SUBJECT, NOW)["status"] == "fail"


def test_sbom_binding_requires_scanner_source_not_caller_label() -> None:
    bom = {"bomFormat": "CycloneDX", "metadata": {"component": {"type": "container"}}}
    source = {"type": "image", "metadata": {"repoDigests": ["repo@" + SUBJECT]}}
    assert (
        supply.bind_sbom(copy.deepcopy(bom), source, SUBJECT)["metadata"]["properties"][0]["value"]
        == SUBJECT
    )
    with pytest.raises(ValueError):
        supply.bind_sbom(bom, {"type": "image"}, SUBJECT)


def archive(
    path: Path,
    *,
    value: bytes = b"content",
    mtime: int = 0,
    name: str = "app/file",
    mode: int = 0o644,
) -> None:
    with tarfile.open(path, "w") as stream:
        item = tarfile.TarInfo(name)
        item.size = len(value)
        item.mtime = mtime
        item.mode = mode
        stream.addfile(item, io.BytesIO(value))


def test_compare_all_content_but_explain_timestamp_only(tmp_path: Path) -> None:
    first, second = tmp_path / "first.tar", tmp_path / "second.tar"
    archive(first)
    archive(second, mtime=1234)
    a = supply.filesystem_inventory(first)
    assert supply.compare(a, supply.filesystem_inventory(second))["status"] == "pass"
    archive(second, value=b"changed")
    assert supply.compare(a, supply.filesystem_inventory(second))["changed_paths"] == ["app/file"]
    archive(second, mode=0o755)
    assert supply.compare(a, supply.filesystem_inventory(second))["status"] == "fail"


def test_inventory_never_extracts_traversal(tmp_path: Path) -> None:
    path = tmp_path / "bad.tar"
    archive(path, name="../outside")
    with pytest.raises(ValueError):
        supply.filesystem_inventory(path)
    assert not (tmp_path.parent / "outside").exists()


def test_index_digest_and_exact_child_checked(monkeypatch: pytest.MonkeyPatch) -> None:
    child = supply.bundle.canonical({"config": {"digest": SUBJECT}, "layers": [{"size": 12}]})
    child_digest = "sha256:" + supply.bundle.digest(child)
    raw = supply.bundle.canonical(
        {
            "manifests": [
                {"digest": child_digest, "platform": {"os": "linux", "architecture": "arm64"}}
            ]
        }
    )
    digest = "sha256:" + supply.bundle.digest(raw)

    def command(*args: str) -> bytes:
        return raw if "@" + digest in args[4] else child

    monkeypatch.setattr(supply, "run", command)
    result = supply.inspect_index("ghcr.io/dejetins/custometry-api", digest, "arm64")
    assert result["digest"] == child_digest and result["compressed_bytes"] == 12
    with pytest.raises(ValueError):
        supply.inspect_index("ghcr.io/dejetins/custometry-api", digest, "amd64")


@pytest.mark.parametrize("mode", ["absent", "identical", "different", "expired", "duplicate", "prior-attempt", "legacy"])
def test_provider_reconcile_never_overwrites(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, mode: str
) -> None:
    archive = tmp_path / "delivery.zip"
    archive.write_bytes(b"signed-bytes")
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as z:
        z.writestr("delivery.zip", b"other" if mode in {"different", "prior-attempt", "legacy"} else archive.read_bytes())
    raw = stream.getvalue()
    item = {
        "name": "custometry-delivery-0.1.0-ms001.12-12-1",
        "expired": mode == "expired",
        "workflow_run": {"id": 12},
        "size_in_bytes": len(raw),
        "id": 10,
        "digest": "sha256:" + supply.bundle.digest(raw),
    }
    if mode == "legacy":
        item["name"] = "custometry-delivery-0.1.0-ms001.12"
    items = [] if mode == "absent" else [item] * (2 if mode == "duplicate" else 1)

    def command(*args: str) -> bytes:
        return raw if args[-1].endswith("/zip") else json.dumps([{"artifacts": items}]).encode()

    monkeypatch.setattr(supply, "run", command)
    output = tmp_path / "output"
    if mode in {"different", "expired", "duplicate", "prior-attempt", "legacy"}:
        with pytest.raises(ValueError):
            supply.reconcile(archive, 12, 2 if mode == "prior-attempt" else 1, output)
        assert not output.exists()
    else:
        supply.reconcile(archive, 12, 2 if mode == "prior-attempt" else 1, output)
        assert f"exists={'false' if mode == 'absent' else 'true'}" in output.read_text()


def test_preparation_cannot_publish_bundle_on_git_merge() -> None:
    workflow = yaml.safe_load(
        (supply.ROOT / ".github/workflows/publish-candidates.yml").read_text()
    )
    for name in ("supply_native", "supply_bundle"):
        assert workflow["jobs"][name]["if"] == "${{ false }}"
    assert workflow["jobs"]["supply_bundle"]["permissions"] == {
        "contents": "read",
        "actions": "read",
        "id-token": "write",
    }
    assert workflow["jobs"]["api_image"]["permissions"]["packages"] == "write"
    assert {
        r["architecture"]
        for r in workflow["jobs"]["supply_native"]["strategy"]["matrix"]["include"]
    } == supply.PLATFORMS


@pytest.mark.parametrize("tampered", [False, True])
def test_installed_license_metadata_must_match_observed_filesystem(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, tampered: bool
) -> None:
    data = b"Name: example\nVersion: 1\nClassifier: License :: OSI Approved :: MIT License\n"
    location = "app/site-packages/example-1.dist-info/METADATA"
    notice = "app/site-packages/example-1.dist-info/licenses/LICENSE"
    supply.save(tmp_path / "selected-filesystem.json", [
        {"path": location, "size_bytes": len(data), "sha256": supply.bundle.digest(data)},
        {"path": notice, "size_bytes": 10, "sha256": "b" * 64},
    ])
    document = {"components": [{"name": "example", "version": "1"}]}
    raw = {"artifacts": [{
        "name": "example", "version": "1", "type": "python",
        "locations": [{"path": "/" + location}],
        "metadata": {"sitePackagesRootPath": "/app/site-packages", "files": [
            {"path": "example-1.dist-info/licenses/LICENSE"},
        ]},
    }]}

    def command(*args: str) -> bytes:
        if args[1] == "create":
            return b"a" * 64
        if args[1] == "cp":
            Path(args[-1]).write_bytes(data + (b"tampered" if tampered else b""))
        return b""

    monkeypatch.setattr(supply, "run", command)
    if tampered:
        with pytest.raises(ValueError, match="DELIVERY_SUBJECT_MISMATCH"):
            supply.normalize_python_licenses(document, raw, "fixture", tmp_path)
        assert "licenses" not in document["components"][0]
    else:
        observations = supply.normalize_python_licenses(document, raw, "fixture", tmp_path)
        assert observations[0]["notice_files"][0]["path"] == notice
        assert document["components"][0]["licenses"] == [{"expression": "MIT"}]


@pytest.mark.parametrize(
    "name", ["../delivery.zip", "/delivery.zip", "folder/delivery.zip", "manifest.json"]
)
def test_transport_accepts_only_fixed_opaque_payload(name: str) -> None:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr(name, b"opaque inner ZIP")
    raw = stream.getvalue()
    with pytest.raises(ValueError):
        supply.unwrap_transport(raw, "sha256:" + supply.bundle.digest(raw))


def test_transport_rejects_symlink_and_wrong_provider_hash() -> None:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        info = zipfile.ZipInfo("delivery.zip")
        info.create_system = 3
        info.external_attr = 0o120777 << 16
        archive.writestr(info, b"outside")
    raw = stream.getvalue()
    with pytest.raises(ValueError):
        supply.unwrap_transport(raw, SUBJECT)
    with pytest.raises(ValueError):
        supply.unwrap_transport(raw, "sha256:" + supply.bundle.digest(raw))


@pytest.mark.parametrize("failure", [None, "method", "subject", "architecture", "total", "cap"])
def test_unpacked_size_binding_and_cap(failure: str | None) -> None:
    record = {"digest": SUBJECT, "architecture": "arm64", "unpacked_bytes": 24}
    observation: dict[str, Any] = {"method": "oci-verified-uncompressed-layer-tar-bytes/v1", "subject": SUBJECT,
                   "architecture": "arm64", "os": "linux", "compressed_layer_bytes": 12,
                   "uncompressed_layer_tar_bytes": 24,
                   "layers": [{"descriptor_bytes": 12, "uncompressed_tar_bytes": 24}]}
    if failure == "cap":
        record["unpacked_bytes"] = observation["uncompressed_layer_tar_bytes"] = 367001601
        observation["layers"][0]["uncompressed_tar_bytes"] = 367001601
    elif failure == "total":
        observation["uncompressed_layer_tar_bytes"] = 25
    elif failure is not None:
        observation[failure] = "untrusted"
    if failure:
        with pytest.raises(ValueError):
            supply.validate_image_size(observation, record, "api")
    else:
        supply.validate_image_size(observation, record, "api")


def test_supplement_preserves_raw_report_when_applicability_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    from .test_delivery_native import report_fixture

    report = report_fixture(datetime.now(timezone.utc))
    report["source"]["target"] = str((tmp_path / "supplemental-sbom.json").resolve())
    report["matches"] = [{"vulnerability": {"id": "CVE-2021-24036", "severity": "Critical"}}]
    (tmp_path / "native-sbom.json").write_text("{}")
    (tmp_path / "compilation-inputs.json").write_text("{}")

    def scanner(*args: str) -> bytes:
        assert args[:2] == ("grype", "--config")
        assert args[2].endswith("deploy/compose/grype.yaml")
        return json.dumps(report).encode()

    def rejected(*args: Any) -> list[dict[str, Any]]:
        raise supply.bundle.BundleError("DELIVERY_APPLICABILITY_UNPROVEN")

    monkeypatch.setattr(supply, "run", scanner)
    monkeypatch.setattr(supply.delivery_native, "folly_applicability", rejected)
    with pytest.raises(ValueError, match="DELIVERY_APPLICABILITY_UNPROVEN"):
        supply.scan_supplement({"components": []}, SUBJECT, tmp_path)
    assert supply.load(tmp_path / "grype.json") == report
    binding = supply.load(tmp_path / "grype-binding.json")
    assert binding["report_sha256"] == supply.sha(tmp_path / "grype.json")
    assert binding["sbom_sha256"] == supply.sha(tmp_path / "supplemental-sbom.json")


def test_complete_native_evidence_assembly(tmp_path: Path) -> None:
    """Drive actual gates/schema/closure with explicitly synthetic inputs."""
    commit = "b" * 40
    inputs = tmp_path / "inputs"
    inventory = supply.load(supply.ROOT / "deploy/compose/delivery-image-inventory.json")
    now = datetime.now(timezone.utc)
    text = 'example@1.0\nDeclared license: "MIT"\nActual fixture notice text.\n'
    for arch in sorted(supply.PLATFORMS):
        images: dict[str, Any] = {}
        for role in ("api", "web", "postgres"):
            directory = inputs / arch / role
            directory.mkdir(parents=True)
            subject = "sha256:" + supply.bundle.digest((role + arch).encode())
            repo = (
                "docker.io/library/postgres"
                if role == "postgres"
                else "ghcr.io/dejetins/custometry-" + role
            )
            images[role] = {
                "repository": repo,
                "index_digest": supply.bundle.POSTGRES_DIGEST if role == "postgres" else SUBJECT,
                "platform": {
                    "os": "linux",
                    "architecture": arch,
                    "digest": subject,
                    "compressed_bytes": 12,
                    "unpacked_bytes": 24,
                },
            }
            supply.save(directory / "image-size.json", {
                "method": "oci-verified-uncompressed-layer-tar-bytes/v1", "subject": subject,
                "architecture": arch, "os": "linux", "compressed_layer_bytes": 12,
                "uncompressed_layer_tar_bytes": 24,
                "layers": [{"descriptor_bytes": 12, "uncompressed_tar_bytes": 24}],
            })
            bom = {
                "bomFormat": "CycloneDX",
                "specVersion": "1.6",
                "metadata": {
                    "properties": [{"name": "custometry:subject-digest", "value": subject}]
                },
                "components": [
                    {"name": "example", "version": "1", "licenses": [{"license": {"id": "MIT"}}]}
                ],
            }
            supply.save(directory / "sbom.json", bom)
            supply.save(directory / "sbom-raw.json", {"fixture": True})
            supply.save(directory / "sbom-original.json", bom)
            supply.save(directory / "license-metadata.json", {"subject": subject, "normalizations": []})
            report, db = scan_inputs()
            report["CreatedAt"] = now.isoformat()
            report["Metadata"]["RepoDigests"] = [repo + "@" + subject]
            db["VulnerabilityDB"].update(
                UpdatedAt=now.isoformat(), NextUpdate=(now + timedelta(hours=12)).isoformat()
            )
            supply.save(directory / "trivy.json", report)
            supply.save(directory / "trivy-version.json", db)
            supply.save(
                directory / "trivy-db.json",
                {"database_sha256": "c" * 64, "metadata_sha256": "d" * 64},
            )
            supply.save(directory / "gates.json", {"fixture": True})
            if role != "postgres":
                filesystem: list[dict[str, Any]] = [{"path": "synthetic-file", "sha256": "e" * 64}]
                embedded = copy.deepcopy(inventory[role])
                if role == "web":
                    embedded += [
                        supply.bundle.file_record(name, b"synthetic", "asset")
                        for name in inventory["web_generated_required"]
                    ]
                    (directory / "THIRD-PARTY.txt").write_text(text)
                    package = {"name": "example", "version": "1.0", "root": "node_modules/example", "metadata_sha256": "a" * 64}
                    supply.save(directory / "runtime-modules.json", {
                        "schema_version": 1, "packages": [package],
                        "modules": [{"package": package["root"], "chunks": ["chunk.js"]}],
                        "chunks": {"chunk.js": "c" * 64},
                    })
                    supply.save(directory / "runtime-packages.json", {
                        "schema_version": 1, "packages": [{**package, "license": "MIT", "notices": [{"fixture": True}]}],
                    })
                    filesystem.append({"path": "usr/share/nginx/html/chunk.js", "sha256": "c" * 64})
                    for name in ("THIRD-PARTY.txt", "runtime-modules.json", "runtime-packages.json"):
                        file = directory / name
                        filesystem.append({"path": "usr/share/nginx/html/notices/" + name, "sha256": supply.sha(file), "size_bytes": file.stat().st_size})
                    supply.save(directory / "selected-filesystem.json", filesystem)
                    notices, missing = supply.web_graph_sbom(directory, subject)
                    assert not missing
                    supply.save(directory / "web-notices-sbom.json", notices)
                    supply.save(directory / "web-notices-gate.json", {"fixture": True})
                supply.save(directory / "embedded.json", embedded)
                if role != "web":
                    supply.save(directory / "selected-filesystem.json", filesystem)
                for attempt in (1, 2):
                    supply.save(directory / f"rebuild-{attempt}-filesystem.json", filesystem)
                    supply.save(
                        directory / f"comparison-{attempt}.json",
                        supply.compare(filesystem, filesystem),
                    )
                    supply.save(
                        directory / f"build-{attempt}.json",
                        {"source_commit": commit, "source_archive_sha256": "f" * 64},
                    )
        supply.save(
            inputs / arch / "platform.json",
            {
                "source_commit": commit,
                "source_archive_sha256": "f" * 64,
                "architecture": arch,
                "engine_version": "29.6.2",
                "compose_version": "5.3.1",
                "images": images,
            },
        )
    output = tmp_path / "assembled"
    supply.assemble_supply(inputs, output, commit, 123, 1)
    record = supply.load(output / "delivery-manifest.json")
    supply.bundle.check_payload(record, supply.bundle.candidate_payload(record, output))
    assert record["retrieval"]["artifact_name"] == "custometry-delivery-0.1.0-ms001.123-123-1"
    assert len(record["images"]) == 3
    assert record["source"]["commit"] == commit


@pytest.mark.parametrize("store", ["classic", "containerd"])
def test_local_subject_ids_keep_config_and_child_distinct(store: str) -> None:
    child = {"digest": SUBJECT, "config_digest": "sha256:" + "c" * 64, "architecture": "arm64"}
    reference = "ghcr.io/dejetins/custometry-api@" + SUBJECT
    observed: dict[str, Any] = {
        "Id": child["config_digest"] if store == "classic" else SUBJECT,
        "RepoDigests": [reference],
        "Architecture": "arm64",
        "Os": "linux",
    }
    if store == "containerd":
        observed["Descriptor"] = {"digest": SUBJECT}
    supply.check_local_subject(observed, child, reference)
    observed["Id"] = "sha256:" + "f" * 64
    with pytest.raises(ValueError):
        supply.check_local_subject(observed, child, reference)


def test_missing_runtime_notice_never_becomes_license_acceptance() -> None:
    bom, missing = supply.notice_sbom(
        'html-parse-stringify@3.0.1\nDeclared license: "MIT"\nNo root license text found; review required.\n',
        SUBJECT,
    )
    assert missing == ["html-parse-stringify@3.0.1"]
    assert bom["components"][0]["licenses"] == [{"license": {"name": "MIT"}}]


def test_general_evidence_is_distinct_from_strict_manifest_json(tmp_path: Path) -> None:
    value = {"description": "Лицензия\nactual notice", "cvss": 9.8}
    path = tmp_path / "evidence.json"
    supply.save(path, value)
    assert supply.load(path) == value
    with pytest.raises(ValueError):
        supply.bundle.STRUCTURE.parse_json(path.read_bytes())


def test_archived_scanner_binding_requires_verified_config() -> None:
    source: dict[str, Any] = {"type": "image", "metadata": {"imageID": SUBJECT, "repoDigests": []}}
    document = {"bomFormat": "CycloneDX", "metadata": {"component": {"type": "container"}}}
    with pytest.raises(ValueError):
        supply.bind_sbom(copy.deepcopy(document), source, "sha256:" + "d" * 64)
    result = supply.bind_sbom(document, source, "sha256:" + "d" * 64, expected_config=SUBJECT)
    assert result["metadata"]["properties"][0]["value"] == "sha256:" + "d" * 64


@pytest.mark.parametrize("tamper", [None, "source", "metadata", "chunk", "coverage"])
def test_web_notices_bind_actual_bundled_dependencies(tmp_path: Path, tamper: str | None) -> None:
    import subprocess

    package = "node_modules/.pnpm/example/node_modules/example"
    base = tmp_path / package
    base.mkdir(parents=True)
    raw = json.dumps({"name": "example", "version": "1", "license": "MIT"}).encode()
    (base / "package.json").write_bytes(raw)
    (base / "LICENSE").write_text("Exact fixture upstream text")
    (base / "index.js").write_text("fixture source")
    # Installed but unbundled dependency must not masquerade as shipped code.
    unused = tmp_path / "node_modules/.pnpm/unused/node_modules/unused"
    unused.mkdir(parents=True)
    (unused / "package.json").write_text('{"name":"unused","version":"1","license":"UNKNOWN"}')
    output = tmp_path / "apps/web/dist"
    (output / "notices").mkdir(parents=True)
    (output / "chunk.js").write_text("fixture compiled chunk")
    inventory = {
        "schema_version": 1,
        "packages": [{"name": "example", "version": "1", "root": package, "metadata_sha256": supply.bundle.digest(raw)}],
        "modules": [{"path": package + "/index.js", "sha256": supply.bundle.digest(b"fixture source"), "package": package, "chunks": ["chunk.js"]}],
        "chunks": {"chunk.js": supply.bundle.digest(b"fixture compiled chunk")},
    }
    if tamper == "coverage":
        inventory["packages"] = []
    (output / "notices/runtime-modules.json").write_text(json.dumps(inventory))
    if tamper in {"source", "metadata", "chunk"}:
        target = {"source": base / "index.js", "metadata": base / "package.json", "chunk": output / "chunk.js"}[tamper]
        target.write_bytes(target.read_bytes() + b" ")
    result = subprocess.run(
        ["node", str(supply.ROOT / "deploy/compose/collect-web-notices.mjs")],
        cwd=tmp_path, capture_output=True,
    )
    if tamper is not None:
        assert result.returncode != 0
        assert not (output / "notices/THIRD-PARTY.txt").exists()
    else:
        assert result.returncode == 0, result.stderr.decode()
        notices = (output / "notices/THIRD-PARTY.txt").read_text()
        assert "unused" not in notices
        assert "example@1" in notices and "Exact fixture upstream text" in notices


def test_only_explained_uv_cache_metadata_is_normalized() -> None:
    import base64
    import hashlib

    def rows(seconds: int, inode: int, commit: str | None = None) -> list[dict[str, Any]]:
        cache = supply.evidence_bytes(
            {
                "timestamp": {"secs_since_epoch": seconds, "nanos_since_epoch": 1},
                "directories": {"src": inode},
                "commit": commit,
                "tags": None,
                "env": {},
            }
        )
        entry = supply.UV_CACHE.split("site-packages/", 1)[1]
        record = (
            entry
            + ",sha256="
            + base64.urlsafe_b64encode(hashlib.sha256(cache).digest()).decode().rstrip("=")
            + ","
            + str(len(cache))
            + "\nother.py,sha256=unchanged,12\n"
        ).encode()
        return [
            {
                "path": path,
                "sha256": supply.bundle.digest(raw),
                "size_bytes": len(raw),
                "build_metadata": raw.decode(),
            }
            for path, raw in ((supply.UV_CACHE, cache), (supply.WHEEL_RECORD, record))
        ]

    first, second = rows(1, 100), rows(2, 200)
    result = supply.compare(first, second)
    assert result["status"] == "pass"
    assert set(result["allowed_build_metadata_differences"]) == {
        supply.UV_CACHE,
        supply.WHEEL_RECORD,
    }
    assert supply.compare(first, rows(2, 200, "changed-source"))["status"] == "fail"
    second[1]["build_metadata"] += "tampered.py,,\n"
    with pytest.raises(ValueError):
        supply.compare(first, second)
