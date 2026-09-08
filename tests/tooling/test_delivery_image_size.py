"""Layer-size evidence must bind every descriptor and ordered DiffID."""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import tarfile
from pathlib import Path
from typing import Any

import pytest

from tools.custometry_quality import delivery_image_size as sizes


def fixture(tmp_path: Path, failure: str | None, *, compressed: bool = True) -> tuple[Path, str, int]:
    body = b"uncompressed layer tar fixture" * 100
    raw = gzip.compress(body, mtime=0) if compressed else body
    diff_id = "sha256:" + hashlib.sha256(body).hexdigest()
    config: dict[str, Any] = {"os": "linux", "architecture": "arm64", "rootfs": {"type": "layers", "diff_ids": [diff_id]}}
    if failure == "diff_id":
        config["rootfs"]["diff_ids"] = ["sha256:" + "0" * 64]
    elif failure == "count":
        config["rootfs"]["diff_ids"].append(diff_id)
    elif failure == "platform":
        config["architecture"] = "amd64"
    objects: dict[str, bytes] = {}

    def obj(raw: bytes, media: str) -> dict[str, Any]:
        digest = hashlib.sha256(raw).hexdigest()
        objects["blobs/sha256/" + digest] = raw
        return {"digest": "sha256:" + digest, "size": len(raw), "mediaType": media}

    layer = obj(raw, "application/vnd.oci.image.layer.v1.tar" + ("+gzip" if compressed else ""))
    if failure == "encoding":
        layer["mediaType"] = "application/vnd.oci.image.layer.v1.tar+zstd"
    elif failure == "descriptor_size":
        layer["size"] += 1
    elif failure == "descriptor_digest":
        objects["blobs/sha256/" + layer["digest"][7:]] = raw[:-1] + bytes([raw[-1] ^ 1])
    manifest = {"schemaVersion": 2, "config": obj(json.dumps(config).encode(), "application/vnd.oci.image.config.v1+json"),
                "layers": [layer]}
    child = obj(json.dumps(manifest).encode(), "application/vnd.oci.image.manifest.v1+json")
    output = tmp_path / "saved.tar"
    with tarfile.open(output, "w") as archive:
        for name, raw in objects.items():
            item = tarfile.TarInfo(name)
            item.size = len(raw)
            archive.addfile(item, io.BytesIO(raw))
    return output, child["digest"], len(body)


@pytest.mark.parametrize("failure", [None, "diff_id", "count", "platform", "encoding", "descriptor_size", "descriptor_digest", "limit"])
def test_verified_stream_measurement(tmp_path: Path, failure: str | None) -> None:
    archive, subject, unpacked = fixture(tmp_path, failure)
    if failure:
        with pytest.raises(ValueError):
            sizes.observe(archive, subject, "arm64", limit=10 if failure == "limit" else 1073741824)
    else:
        observed = sizes.observe(archive, subject, "arm64")
        assert observed["uncompressed_layer_tar_bytes"] == unpacked
        assert observed["compressed_layer_bytes"] < unpacked
        assert observed["subject"] == subject


def test_uncompressed_oci_layer(tmp_path: Path) -> None:
    archive, subject, unpacked = fixture(tmp_path, None, compressed=False)
    result = sizes.observe(archive, subject, "arm64")
    assert result["compressed_layer_bytes"] == result["uncompressed_layer_tar_bytes"] == unpacked
