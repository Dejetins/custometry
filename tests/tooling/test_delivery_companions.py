"""Hostile v2 metadata/ZIP fixtures; no real signature or provider acceptance."""
from __future__ import annotations

import copy
import io
import stat
import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from tools.custometry_quality import delivery_bundle as bundle
from tools.custometry_quality import delivery_companions as companions

from .test_delivery_bundle_producer import candidate

NOW = datetime(2026, 9, 8, tzinfo=timezone.utc)


@pytest.mark.parametrize("names", [["A/x", "a/y"], ["a", "a/b"], ["a/b", "a"], ["a/b", "A/B"]])
def test_path_prefix_collisions_fail_before_writing(names: list[str]) -> None:
    with pytest.raises(ValueError):
        companions.validate_paths(names)


def fixture(tmp_path: Path) -> tuple[dict[str, Any], Path]:
    record, _ = candidate()
    record["schema_version"] = "custometry-delivery/v2"
    record["compatibility"]["reader_major"] = 2
    producer = record["producer"]
    data = b"opaque corresponding source; never recursively unpacked"
    archive = tmp_path / "part.zip"
    with zipfile.ZipFile(archive, "w") as output:
        output.writestr("sources/component.tar.gz", data)
    record["companions"] = [{
        "part": 1,
        "artifact_name": f"custometry-delivery-sources-{record['delivery_version']}-{producer['run_id']}-{producer['run_attempt']}-01",
        "artifact_id": 1, "provider_sha256": companions.sha(archive),
        "archive_bytes": archive.stat().st_size, "expanded_bytes": len(data),
        "expires_at": "2026-12-07T00:00:00Z",
        "files": [{"path": "sources/component.tar.gz", "sha256": bundle.digest(data), "size_bytes": len(data)}],
    }]
    return record, archive


def test_new_reader_requires_explicit_major_and_preserves_old_schema(tmp_path: Path) -> None:
    record, _ = fixture(tmp_path)
    path = tmp_path / "manifest.json"
    path.write_bytes(bundle.canonical(record))
    with pytest.raises(ValueError, match="DELIVERY_READER_UNSUPPORTED"):
        bundle.STRUCTURE.read_contract(path)
    assert bundle.STRUCTURE.read_contract(path, reader_major=2) == record
    assert companions.policy()["limits"]["archive_bytes"] == 134217728
    assert companions.policy()["limits"]["file_bytes"] == 67108864
    companions.validate_descriptors(record, now=NOW)


@pytest.mark.parametrize("wide", [False, True])
@pytest.mark.parametrize("tamper", [False, True])
def test_streaming_data_descriptor_and_zip64(tmp_path: Path, wide: bool, tamper: bool) -> None:
    record, archive = fixture(tmp_path)
    part = record["companions"][0]
    data = b"opaque corresponding source; never recursively unpacked"

    class Unseekable(io.BytesIO):
        def seek(self, *args: Any, **kwargs: Any) -> int:
            raise io.UnsupportedOperation("fixture requires streaming ZIP")

    stream = Unseekable()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as output:
        with output.open(part["files"][0]["path"], "w", force_zip64=wide) as entry:
            entry.write(data)
    raw = bytearray(stream.getvalue())
    if tamper:
        offset = raw.index(b"PK\x07\x08") + 4
        raw[offset] ^= 1
    archive.write_bytes(raw)
    part["archive_bytes"] = len(raw)
    part["provider_sha256"] = companions.sha(archive)
    if tamper:
        with pytest.raises(ValueError):
            companions.verify_zip(archive, part, tmp_path / "verified")
        assert not (tmp_path / "verified").exists()
    else:
        companions.verify_zip(archive, part, tmp_path / "verified")
        assert (tmp_path / "verified" / part["files"][0]["path"]).read_bytes() == data


def test_primary_and_companion_paths_cannot_collide(tmp_path: Path) -> None:
    record, _ = fixture(tmp_path)
    record["companions"][0]["files"][0]["path"] = record["files"][0]["path"]
    with pytest.raises(ValueError):
        companions.validate_descriptors(record, now=NOW)


@pytest.mark.parametrize("failure", ["parent", "duplicate_part", "duplicate_id", "case_collision", "future_attempt", "expired", "sum"])
def test_descriptor_failure_prevents_any_materialization(tmp_path: Path, failure: str) -> None:
    record, _ = fixture(tmp_path)
    part = record["companions"][0]
    if failure == "parent":
        part["files"][0]["path"] = "a/../x"
    elif failure in {"duplicate_part", "duplicate_id", "case_collision"}:
        extra = copy.deepcopy(part)
        extra["part"] = 2
        extra["artifact_name"] = extra["artifact_name"][:-2] + "02"
        extra["artifact_id"] = 2
        extra["files"][0]["path"] = "sources/other.tar.gz"
        if failure == "duplicate_part":
            extra["part"] = 1
        if failure == "duplicate_id":
            extra["artifact_id"] = 1
        if failure == "case_collision":
            extra["files"][0]["path"] = "Sources/Component.tar.gz"
        record["companions"].append(extra)
    elif failure == "future_attempt":
        part["artifact_name"] = part["artifact_name"].rsplit("-", 2)[0] + "-999999-01"
    elif failure == "expired":
        part["expires_at"] = "2026-09-07T00:00:00Z"
    elif failure == "sum":
        part["expanded_bytes"] += 1
    with pytest.raises(ValueError):
        companions.validate_descriptors(record, now=NOW)


@pytest.mark.parametrize("failure", [None, "tampered", "missing", "extra", "symlink", "duplicate", "header_size", "truncated", "file_hash"])
def test_streamed_zip_closure_and_cleanup(tmp_path: Path, failure: str | None) -> None:
    record, archive = fixture(tmp_path)
    part = record["companions"][0]
    if failure in {"missing", "extra", "symlink", "duplicate"}:
        mode = "w" if failure in {"missing", "symlink"} else "a"
        with zipfile.ZipFile(archive, mode) as output:
            if failure == "missing":
                output.writestr("wrong", b"no")
            elif failure == "symlink":
                info = zipfile.ZipInfo(part["files"][0]["path"])
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                output.writestr(info, b"outside")
            else:
                output.writestr("extra" if failure == "extra" else part["files"][0]["path"], b"duplicate")
    elif failure in {"tampered", "header_size", "truncated"}:
        data = bytearray(archive.read_bytes())
        if failure == "tampered":
            data[60] ^= 1
        elif failure == "header_size":
            struct.pack_into("<I", data, 22, 1)
        else:
            del data[-20:]
        archive.write_bytes(data)
    elif failure == "file_hash":
        part["files"][0]["sha256"] = "0" * 64
    part["provider_sha256"] = companions.sha(archive)
    part["archive_bytes"] = archive.stat().st_size
    output = tmp_path / "private"
    if failure:
        with pytest.raises((ValueError, zipfile.BadZipFile)):
            companions.verify_zip(archive, part, output)
        assert not output.exists()
    else:
        companions.verify_zip(archive, part, output)
        target = output / part["files"][0]["path"]
        assert companions.sha(target) == part["files"][0]["sha256"]
        assert stat.S_IMODE(target.stat().st_mode) == 0o600
        assert stat.S_IMODE(output.stat().st_mode) == 0o700


@pytest.mark.parametrize("failure", [None, "foreign_run", "foreign_commit", "foreign_origin", "expired", "provider_hash"])
def test_authenticated_provider_observation_is_bound(tmp_path: Path, failure: str | None) -> None:
    record, _ = fixture(tmp_path)
    part = record["companions"][0]
    metadata: dict[str, Any] = {
        "id": part["artifact_id"], "name": part["artifact_name"],
        "digest": "sha256:" + part["provider_sha256"], "size_in_bytes": part["archive_bytes"],
        "expires_at": part["expires_at"], "expired": False,
        "archive_download_url": "https://api.github.com/repos/Dejetins/custometry/actions/artifacts/1/zip",
        "workflow_run": {"id": record["producer"]["run_id"], "head_sha": record["source"]["commit"], "head_branch": "main"},
    }
    if failure == "foreign_run":
        metadata["workflow_run"]["id"] += 1
    elif failure == "foreign_commit":
        metadata["workflow_run"]["head_sha"] = "0" * 40
    elif failure == "foreign_origin":
        metadata["archive_download_url"] = "https://foreign.invalid/payload"
    elif failure == "expired":
        metadata["expired"] = True
    elif failure == "provider_hash":
        metadata["digest"] = "sha256:" + "0" * 64
    if failure:
        with pytest.raises(ValueError):
            companions.verify_provider(part, metadata, record, now=NOW)
    else:
        companions.verify_provider(part, metadata, record, now=NOW)
