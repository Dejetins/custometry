"""Candidate producer checks on synthetic image subjects; no supply/runtime claims."""

from __future__ import annotations

import copy
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

import pytest

from tools.custometry_quality import delivery_bundle as bundle

ROOT = Path(__file__).resolve().parents[2]


def test_frozen_image_inventory_matches_current_source_bytes() -> None:
    expected = json.loads((ROOT / "deploy/compose/delivery-image-inventory.json").read_bytes())
    api_mappings = re.findall(
        r"^COPY --chown=10001:10001 (\S+) (\S+)$", (ROOT / "apps/api/Dockerfile").read_text(), re.M
    )
    api_mappings.append(
        ("apps/api/src/custometry_api", "/app/.venv/lib/python3.12/site-packages/custometry_api")
    )
    web_mappings = [
        ("apps/web/public", "/usr/share/nginx/html"),
        ("apps/web/nginx.conf", "/etc/nginx/nginx.conf"),
        ("deploy/edge/nginx.conf", "/etc/nginx/edge.conf"),
        ("LICENSE", "/usr/share/nginx/html/notices/Custometry-LICENSE"),
    ]
    for image_role, mappings in (("api", api_mappings), ("web", web_mappings)):
        for item in expected[image_role]:
            candidates = [
                (ROOT / src / item["path"][len(dst.lstrip("/")) + 1 :])
                if item["path"] != dst.lstrip("/")
                else ROOT / src
                for src, dst in mappings
                if item["path"] == dst.lstrip("/") or item["path"].startswith(dst.lstrip("/") + "/")
            ]
            matches = [
                p
                for p in candidates
                if p.is_file() and bundle.digest(p.read_bytes()) == item["sha256"]
            ]
            assert len(matches) == 1, item["path"]


def candidate(*, demo: bool = True) -> tuple[dict[str, Any], dict[str, bytes]]:
    record = json.loads((ROOT / "tests/tooling/fixtures/delivery-manifest.valid.json").read_bytes())
    record["images"]["postgres"]["index_digest"] = bundle.POSTGRES_DIGEST
    record["profiles"] = ["core", "migration", *(["demo"] if demo else [])]
    config = bundle.configuration(record)
    record["services"] = bundle.service_records(config)
    record["resources"] = bundle.resource_records(config)
    payload: dict[str, bytes] = {
        bundle.CONFIG: bundle.canonical(config),
        bundle.ENV: bundle.projection(record),
        "delivery-verification-policy.json": (
            ROOT / "deploy/compose/delivery-verification-policy.json"
        ).read_bytes(),
        "evidence/sbom.json": b'{"synthetic":true}',
    }
    if demo:
        for name in bundle.DEMO_FILES:
            payload["demo/init/" + name] = (ROOT / "deploy/demo-source/init" / name).read_bytes()
    record["files"] = [
        bundle.file_record(name, raw, "config") for name, raw in sorted(payload.items())
    ]
    record["evidence"][0]["file"] = next(
        f for f in record["files"] if f["path"] == "evidence/sbom.json"
    )
    expected = json.loads((ROOT / "deploy/compose/delivery-image-inventory.json").read_bytes())
    for image_role in ("api", "web"):
        record["images"][image_role]["embedded_files"] = copy.deepcopy(expected[image_role])
    record["images"]["web"]["embedded_files"].extend(
        bundle.file_record(name, b"synthetic built asset", "asset")
        for name in expected["web_generated_required"]
    )
    record["migrations"]["revisions"] = copy.deepcopy(expected["migration_chain"])
    record["migrations"]["support_files"] = copy.deepcopy(expected["migration_support"])
    for key in ("head", "read_head", "write_head"):
        record["migrations"][key] = expected["migration_chain"][-1]["revision"]
    return record, payload


@pytest.mark.parametrize("demo", [True, False])
def test_complete_candidate_portable_payload(demo: bool, tmp_path: Path) -> None:
    record, payload = candidate(demo=demo)
    bundle.check_payload(record, payload)
    source = tmp_path / "source"
    bundle.write_new(source, payload)
    output = tmp_path / "outside-checkout"
    bundle.prepare(record, source, output)
    assert bundle.payload_files(output) == payload
    assert stat.S_IMODE((output / bundle.ENV).stat().st_mode) == 0o600
    config = json.loads((output / bundle.CONFIG).read_bytes())
    assert all("build" not in s for s in config["services"].values())
    assert ("demo-source-db" in config["services"]) is demo


@pytest.mark.parametrize(
    "change",
    [
        "duplicate-service",
        "cycle",
        "missing-service",
        "wrong-role",
        "platform-duplicate",
        "wrong-postgres",
        "duplicate-path",
        "case-collision",
        "extra-resource",
        "missing-resource",
        "dangling-capability",
        "migration-cycle",
        "migration-head",
        "migration-bytes",
        "evidence-drift",
        "resource-path",
        "wrong-config",
        "extra-file",
        "missing-file",
        "env-drift",
        "policy-drift",
    ],
)
def test_rejects_semantic_substitution(change: str) -> None:
    record, payload = candidate()
    if change == "duplicate-service":
        record["services"].append(copy.deepcopy(record["services"][0]))
    elif change == "cycle":
        record["services"][0]["depends_on"] = ["api"]
    elif change == "missing-service":
        record["services"].pop()
    elif change == "wrong-role":
        record["services"][0]["image"] = "postgres"
    elif change == "platform-duplicate":
        record["images"]["api"]["platforms"][1]["architecture"] = "amd64"
    elif change == "wrong-postgres":
        record["images"]["postgres"]["index_digest"] = "sha256:" + "b" * 64
    elif change == "duplicate-path":
        record["files"].append(copy.deepcopy(record["files"][0]))
    elif change == "case-collision":
        item = copy.deepcopy(record["files"][0])
        item["path"] = item["path"].upper()
        record["files"].append(item)
    elif change == "extra-resource":
        record["resources"].append(dict(record["resources"][0], id="extra"))
    elif change == "missing-resource":
        record["resources"].pop()
    elif change == "dangling-capability":
        record["capabilities"][0]["services"] = ["unknown"]
    elif change == "migration-cycle":
        record["migrations"]["revisions"][0]["down_revision"] = "0001_fixture"
    elif change == "migration-head":
        record["migrations"]["head"] = "0002_other"
    elif change == "migration-bytes":
        record["migrations"]["revisions"][0] = copy.deepcopy(record["migrations"]["revisions"][0])
        record["migrations"]["revisions"][0]["file"]["sha256"] = "b" * 64
    elif change == "evidence-drift":
        record["evidence"][0]["file"] = dict(record["evidence"][0]["file"], sha256="b" * 64)
    elif change == "resource-path":
        record["resources"][0]["location"] = "../../outside"
    elif change == "wrong-config":
        payload[bundle.CONFIG] = b'{"services":{"api":{"build":"."}}}'
    elif change == "extra-file":
        payload["secret.txt"] = b"sensitive"
    elif change == "missing-file":
        del payload[bundle.CONFIG]
    elif change == "env-drift":
        payload[bundle.ENV] = payload[bundle.ENV].replace(b"0.1.0", b"0.2.0")
    elif change == "policy-drift":
        payload["delivery-verification-policy.json"] = b"{}"
    with pytest.raises(ValueError):
        bundle.check_payload(record, payload)


def test_hash_correct_hostile_config_still_fails() -> None:
    record, payload = candidate()
    config = json.loads(payload[bundle.CONFIG])
    config["services"]["api"]["volumes"] = ["/:/host"]
    payload[bundle.CONFIG] = bundle.canonical(config)
    record["files"] = [
        bundle.file_record(f["path"], payload[f["path"]], f["role"]) for f in record["files"]
    ]
    with pytest.raises(bundle.BundleError):
        bundle.check_payload(record, payload)


@pytest.mark.parametrize(
    "name", ["../x", "/tmp/x", "C:/x", "a//b", "a/./b", "a/%20", "a\\b", "a/", "a\x00b"]
)
def test_unsafe_paths_rejected(name: str) -> None:
    with pytest.raises(bundle.BundleError):
        bundle.safe_path(name)


def test_payload_symlinks_and_existing_destinations_are_preserved(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.write_text("keep")
    source = tmp_path / "source"
    source.mkdir()
    (source / "link").symlink_to(outside)
    with pytest.raises(bundle.BundleError):
        bundle.payload_files(source)
    with pytest.raises(bundle.BundleError):
        bundle.write_new(source, {"x": b"new"})
    assert outside.read_text() == "keep"
    assert not (source / "x").exists()


def test_deterministic_regular_archive_and_no_overwrite(tmp_path: Path) -> None:
    record, payload = candidate()
    source = tmp_path / "payload"
    bundle.write_new(source, payload)
    signature = tmp_path / "synthetic-signature.json"
    signature.write_bytes(b'{"not_a_signature":true}')
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"
    bundle.pack(record, source, signature, first)
    bundle.pack(record, source, signature, second)
    assert first.read_bytes() == second.read_bytes()
    with zipfile.ZipFile(first) as archive:
        assert set(archive.namelist()) == set(payload) | bundle.ENVELOPE
        for info in archive.infolist():
            assert stat.S_ISREG(info.external_attr >> 16)
            assert not info.is_dir()
        assert archive.read("delivery-manifest.json") == bundle.canonical(record)
        # Read back our own deterministic producer output (not a hostile-input verifier).
        restored = {name: archive.read(name) for name in payload}
    extracted = tmp_path / "extracted"
    bundle.write_new(extracted, restored)
    bundle.check_payload(record, bundle.payload_files(extracted))
    assert stat.S_IMODE((extracted / "demo/init/010_create_reader.sh").stat().st_mode) == 0o755
    with pytest.raises(bundle.BundleError):
        bundle.pack(record, source, signature, first)


def test_assembly_and_independent_stdlib_reader(tmp_path: Path) -> None:
    record, payload = candidate()
    record["evidence"][0]["file"]["role"] = "evidence"
    metadata = {k: v for k, v in record.items() if k not in {"files", "services", "resources"}}
    source = tmp_path / "source"
    bundle.write_new(source, payload)
    output = tmp_path / "assembled"
    bundle.assemble(metadata, source, output)
    assembled = bundle.STRUCTURE.read_contract(output / "delivery-manifest.json")
    bundle.check_payload(assembled, bundle.candidate_payload(assembled, output))
    toolkit = tmp_path / "independently-selected-toolkit"
    paths = [
        "tools/custometry_quality/delivery_bundle.py",
        "deploy/compose/validate-delivery-manifest.py",
        "deploy/compose/validate-release-manifest.py",
        "deploy/compose/delivery-manifest.schema.json",
        "deploy/compose/delivery-verification-policy.json",
        "deploy/compose/compose.candidate.json",
        "deploy/compose/delivery-image-inventory.json",
    ]
    for name in paths:
        target = toolkit / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            str(toolkit / paths[0]),
            "check",
            "--record",
            str(output / "delivery-manifest.json"),
            "--payload",
            str(output),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["code"] == "DELIVERY_CANDIDATE_PREPARED"


def test_real_compose_renders_outside_repository_without_engine(tmp_path: Path) -> None:
    _, payload = candidate()
    output = tmp_path / "candidate"
    bundle.write_new(output, payload)
    result = subprocess.run(
        [
            "docker",
            "compose",
            "--env-file",
            str(output / bundle.ENV),
            "-f",
            str(output / bundle.CONFIG),
            "--profile",
            "demo",
            "--profile",
            "migration",
            "config",
            "--format",
            "json",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "COMPOSE_PROJECT_NAME": "ms001-s02-test",
            "CUSTOMETRY_SECRETS_DIR": str(tmp_path / "external-secrets"),
        },
    )
    assert result.returncode == 0, result.stderr
    config = json.loads(result.stdout)
    assert len(config["services"]) == 6
    assert all("build" not in s for s in config["services"].values())
    demo = config["services"]["demo-source-db"]
    mount = next(v for v in demo["volumes"] if v["type"] == "bind")
    assert mount["source"] == str(output / "demo/init")
    assert mount["read_only"]
    assert (
        config["services"]["api"]["image"]
        == bundle.LEGACY.parse_manifest(payload[bundle.ENV])["CUSTOMETRY_API_IMAGE"]
    )


def test_cli_error_redaction_and_source_capture_fail_closed(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.custometry_quality.delivery_bundle",
            "check",
            "--record",
            str(tmp_path / "secret-dsn"),
            "--payload",
            str(tmp_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "secret-dsn" not in result.stdout + result.stderr
    assert json.loads(result.stdout)["result"] == "fail"
    with pytest.raises(bundle.BundleError):
        bundle.capture("a" * 40, tmp_path / "source.tar")
    assert not (tmp_path / "source.tar").exists()


@pytest.mark.parametrize("helper", [
    "tools/__init__.py", "tools/custometry_quality/__init__.py",
    "tools/custometry_quality/core.py", "tools/custometry_quality/gate_sbom.py",
    "tools/custometry_quality/gate_licenses.py", "tools/custometry_quality/delivery_image_size.py",
])
def test_source_capture_rejects_changed_executed_helper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, helper: str,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()

    def git(*args: str) -> str:
        return subprocess.run(["git", "-C", str(repository), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    git("init", "--quiet")
    for name in bundle.SOURCE_PATHS:
        target = repository / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("original source\n")
    git("add", "--all")
    git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
        "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "fixture")
    commit = git("rev-parse", "HEAD")
    monkeypatch.setattr(bundle, "ROOT", repository)
    bundle.capture(commit, tmp_path / "clean.tar")
    (repository / helper).write_text("changed executed source\n")
    with pytest.raises(bundle.BundleError, match="^DELIVERY_SOURCE_CAPTURE_REQUIRED$"):
        bundle.capture(commit, tmp_path / "dirty.tar")
    assert not (tmp_path / "dirty.tar").exists()
