"""Measure authenticated uncompressed layer tar streams, not allocated disk usage."""
from __future__ import annotations

import gzip
import hashlib
import json
import re
import tarfile
from pathlib import Path
from typing import Any

from . import delivery_bundle as bundle

GZIP = {"application/vnd.oci.image.layer.v1.tar+gzip", "application/vnd.docker.image.rootfs.diff.tar.gzip"}
RAW = {"application/vnd.oci.image.layer.v1.tar", "application/vnd.docker.image.rootfs.diff.tar"}


def observe(archive: Path, child_digest: str, architecture: str, *, limit: int = 1073741824) -> dict[str, Any]:
    # Local POSIX CLI, with an absolute deadline across the complete operation.
    from .delivery_set import absolute_deadline

    with absolute_deadline(300):
        return _observe(archive, child_digest, architecture, limit)


def _observe(archive: Path, child_digest: str, architecture: str, limit: int) -> dict[str, Any]:
    bundle.require(archive.is_file() and not archive.is_symlink() and architecture in {"amd64", "arm64"})
    bundle.require(re.fullmatch(r"sha256:[a-f0-9]{64}", child_digest) is not None)
    with tarfile.open(archive) as saved:
        members = saved.getmembers()
        bundle.require(len(members) <= 16384 and len({m.name for m in members}) == len(members), "DELIVERY_LIMIT")
        by_name = {m.name: m for m in members}

        def member(digest: str, size: int | None = None) -> tarfile.TarInfo:
            bundle.require(re.fullmatch(r"sha256:[a-f0-9]{64}", digest) is not None)
            item = by_name.get("blobs/sha256/" + digest[7:])
            bundle.require(item is not None and item.isfile(), "DELIVERY_OCI_ARCHIVE_REQUIRED")
            assert item is not None
            bundle.require(size is None or item.size == size, "DELIVERY_SUBJECT_MISMATCH")
            return item

        def document(digest: str, size: int | None = None) -> dict[str, Any]:
            item = member(digest, size)
            bundle.require(0 < item.size <= 1048576, "DELIVERY_LIMIT")
            stream = saved.extractfile(item)
            assert stream is not None
            raw = stream.read(1048577)
            bundle.require("sha256:" + hashlib.sha256(raw).hexdigest() == digest, "DELIVERY_SUBJECT_MISMATCH")
            return json.loads(raw)

        manifest = document(child_digest)
        bundle.require(manifest.get("schemaVersion") == 2 and isinstance(manifest.get("layers"), list))
        configuration = manifest["config"]
        config = document(configuration["digest"], configuration["size"])
        bundle.require(config.get("os") == "linux" and config.get("architecture") == architecture, "DELIVERY_SUBJECT_MISMATCH")
        rootfs = config["rootfs"]
        bundle.require(rootfs.get("type") == "layers" and len(rootfs["diff_ids"]) == len(manifest["layers"]))
        observations: list[dict[str, Any]] = []
        total = 0
        for descriptor, diff_id in zip(manifest["layers"], rootfs["diff_ids"], strict=True):
            encoding = descriptor["mediaType"]
            bundle.require(encoding in GZIP | RAW, "DELIVERY_LAYER_ENCODING_UNSUPPORTED")
            item = member(descriptor["digest"], descriptor["size"])
            bundle.require(0 < item.size <= limit, "DELIVERY_LIMIT")
            compressed = saved.extractfile(item)
            assert compressed is not None
            digest = hashlib.sha256()
            while block := compressed.read(1048576):
                digest.update(block)
            bundle.require("sha256:" + digest.hexdigest() == descriptor["digest"], "DELIVERY_SUBJECT_MISMATCH")
            original = saved.extractfile(item)
            assert original is not None
            stream = gzip.GzipFile(fileobj=original) if encoding in GZIP else original
            digest = hashlib.sha256()
            size = 0
            with stream:
                while block := stream.read(1048576):
                    size += len(block)
                    total += len(block)
                    bundle.require(total <= limit, "DELIVERY_LIMIT")
                    digest.update(block)
            bundle.require("sha256:" + digest.hexdigest() == diff_id, "DELIVERY_SUBJECT_MISMATCH")
            observations.append({"descriptor_digest": descriptor["digest"], "descriptor_bytes": item.size,
                                 "media_type": encoding, "diff_id": diff_id, "uncompressed_tar_bytes": size})
        bundle.require(bool(observations))
        return {"method": "oci-verified-uncompressed-layer-tar-bytes/v1", "subject": child_digest,
                "configuration_digest": configuration["digest"], "os": "linux", "architecture": architecture,
                "compressed_layer_bytes": sum(row["descriptor_bytes"] for row in observations),
                "uncompressed_layer_tar_bytes": total, "layers": observations}
