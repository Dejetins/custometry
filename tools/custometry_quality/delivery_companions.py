"""Mandatory v2 source-part closure; data validation never permits product execution."""
from __future__ import annotations

import hashlib
import re
import shutil
import stat
import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import delivery_bundle as bundle

ROOT = bundle.ROOT
POLICY_PATH = ROOT / "deploy/compose/delivery-verification-policy.v2.json"


def policy() -> dict[str, Any]:
    return bundle.STRUCTURE.read_contract(POLICY_PATH, policy=True, reader_major=2)


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def validate_paths(names: list[str]) -> None:
    files: set[str] = set()
    directories: set[str] = set()
    spelling: dict[str, str] = {}
    for name in names:
        bundle.safe_path(name)
        folded = name.casefold()
        bundle.require(folded not in files and folded not in directories, "DELIVERY_COMPANION_DUPLICATE")
        parts = name.split("/")
        for length in range(1, len(parts) + 1):
            prefix = "/".join(parts[:length])
            key = prefix.casefold()
            bundle.require(key not in spelling or spelling[key] == prefix, "DELIVERY_COMPANION_DUPLICATE")
            spelling[key] = prefix
            if length < len(parts):
                bundle.require(key not in files, "DELIVERY_COMPANION_DUPLICATE")
                directories.add(key)
        files.add(folded)


def validate_descriptors(record: dict[str, Any], *, now: datetime | None = None) -> None:
    bundle.validate_record(record)
    bundle.require(record["schema_version"] == "custometry-delivery/v2", "DELIVERY_READER_UNSUPPORTED")
    limits = policy()["companions"]
    observed = now or datetime.now(timezone.utc)
    bundle.require(observed.tzinfo is not None)
    ids: set[int] = set()
    names: set[str] = set()
    paths: set[str] = set()
    all_paths: list[str] = []
    count = total = 0
    producer = record["producer"]
    prefix = f"custometry-delivery-sources-{record['delivery_version']}-{producer['run_id']}-"
    for index, part in enumerate(record["companions"], 1):
        bundle.require(part["part"] == index, "DELIVERY_COMPANION_IDENTITY")
        # An exact unchanged part from an earlier failed attempt can be reused;
        # the main signed descriptor binds its actual provider identity and expiry.
        pattern = re.escape(prefix) + r"([1-9][0-9]*)-" + f"{index:02d}"
        match = re.fullmatch(pattern, part["artifact_name"])
        bundle.require(match is not None and int(match[1]) <= producer["run_attempt"], "DELIVERY_COMPANION_IDENTITY")
        bundle.require(part["artifact_id"] not in ids and part["artifact_name"] not in names, "DELIVERY_COMPANION_IDENTITY")
        ids.add(part["artifact_id"])
        names.add(part["artifact_name"])
        expires = datetime.fromisoformat(part["expires_at"].replace("Z", "+00:00"))
        bundle.require(expires > observed, "DELIVERY_COMPANION_EXPIRED")
        total_part = 0
        for file in part["files"]:
            name = bundle.safe_path(file["path"])
            bundle.require(name.casefold() not in paths, "DELIVERY_COMPANION_DUPLICATE")
            paths.add(name.casefold())
            all_paths.append(name)
            total_part += file["size_bytes"]
            count += 1
        bundle.require(total_part == part["expanded_bytes"], "DELIVERY_COMPANION_SIZE")
        total += total_part
    bundle.require(count <= limits["entries"] and total <= limits["total_expanded_bytes"], "DELIVERY_LIMIT")
    # File identities use one logical delivery namespace, even when retained
    # physically in distinct part directories.
    validate_paths(all_paths + [item["path"] for item in record["files"]] + sorted(bundle.ENVELOPE))


def verify_provider(part: dict[str, Any], metadata: dict[str, Any], record: dict[str, Any], *, now: datetime) -> None:
    """Compare a real authenticated REST observation with the signed descriptor."""
    producer = record["producer"]
    workflow = metadata.get("workflow_run", {})
    bundle.require(
        metadata.get("id") == part["artifact_id"]
        and metadata.get("name") == part["artifact_name"]
        and metadata.get("digest") == "sha256:" + part["provider_sha256"]
        and metadata.get("size_in_bytes") == part["archive_bytes"]
        and metadata.get("expires_at") == part["expires_at"]
        and metadata.get("expired") is False
        and workflow.get("id") == producer["run_id"]
        and workflow.get("head_sha") == record["source"]["commit"]
        and workflow.get("head_branch") == "main",
        "DELIVERY_COMPANION_IDENTITY",
    )
    bundle.require(datetime.fromisoformat(part["expires_at"].replace("Z", "+00:00")) > now,
                   "DELIVERY_COMPANION_EXPIRED")
    expected_url = f"https://api.github.com/repos/Dejetins/custometry/actions/artifacts/{part['artifact_id']}/zip"
    bundle.require(metadata.get("archive_download_url") == expected_url, "DELIVERY_COMPANION_ORIGIN")


def verify_zip(archive: Path, part: dict[str, Any], output: Path) -> None:
    """Stream hash/CRC-checked regular files to a new private owned quarantine.

    Source tarballs remain opaque files. No archive member is executed or unpacked
    recursively. Failure removes only this function's newly created directory.
    """
    settings = policy()
    limits = settings["companions"]
    bundle.require(not archive.is_symlink() and archive.is_file())
    bundle.require(archive.stat().st_size == part["archive_bytes"] <= limits["archive_bytes"], "DELIVERY_LIMIT")
    bundle.require(sha(archive) == part["provider_sha256"], "DELIVERY_SUBJECT_MISMATCH")
    expected = bundle.unique(part["files"], "path")
    bundle.require(0 < len(expected) <= limits["entries"])
    validate_paths(list(expected))
    bundle.require(not output.exists() and not output.is_symlink())
    bundle.require(output.parent.is_dir() and output.parent.resolve() == output.parent.absolute())
    output.mkdir(mode=0o700)
    try:
        with archive.open("rb") as raw, zipfile.ZipFile(raw) as container:
            entries = container.infolist()
            bundle.require(len(entries) == len(expected) and set(container.namelist()) == set(expected), "DELIVERY_COMPANION_FILES")
            bundle.require(not container.comment and len({i.filename.casefold() for i in entries}) == len(entries))
            raw.seek(-22, 2)
            eocd_position = raw.tell()
            end_signature, disk, central_disk, disk_count, count, central_size, central_offset, comment = struct.unpack("<4s4H2IH", raw.read(22))
            bundle.require(end_signature == b"PK\x05\x06" and disk == central_disk == comment == 0)
            central_end = eocd_position
            raw.seek(max(0, eocd_position - 20))
            locator = raw.read(20)
            if locator[:4] == b"PK\x06\x07":
                _, locator_disk, zip64_offset, disks = struct.unpack("<4sIQI", locator)
                bundle.require(locator_disk == 0 and disks == 1 and zip64_offset + 56 == eocd_position - 20)
                raw.seek(zip64_offset)
                end64 = raw.read(56)
                bundle.require(len(end64) == 56)
                sig64, record_size, _made, _needed, disk64, central_disk64, disk_count64, count64, size64, offset64 = struct.unpack("<4sQ2H2I4Q", end64)
                bundle.require(sig64 == b"PK\x06\x06" and record_size == 44 and disk64 == central_disk64 == 0)
                bundle.require(disk_count in {0xFFFF, disk_count64} and count in {0xFFFF, count64}
                               and central_size in {0xFFFFFFFF, size64} and central_offset in {0xFFFFFFFF, offset64})
                disk_count, count, central_size, central_offset = disk_count64, count64, size64, offset64
                central_end = zip64_offset
            bundle.require(disk_count == count == len(entries) and central_offset == container.start_dir
                           and central_offset + central_size == central_end)
            intervals: list[tuple[int, int]] = []
            total = 0
            for info in entries:
                mode = info.external_attr >> 16
                bundle.require(not info.is_dir() and stat.S_IFMT(mode) in {0, stat.S_IFREG})
                bundle.require(info.flag_bits & ~0x808 == 0 and info.compress_type in {0, 8})
                bundle.require(0 < info.file_size == expected[info.filename]["size_bytes"] <= limits["file_bytes"], "DELIVERY_LIMIT")
                bundle.require(info.file_size <= max(info.compress_size, 1) * settings["limits"]["compression_ratio"], "DELIVERY_LIMIT")
                raw.seek(info.header_offset)
                header = raw.read(30)
                bundle.require(len(header) == 30)
                signature, _version, flags, compression, _time, _date, crc, compressed, expanded, name_size, extra_size = struct.unpack("<4s5H3I2H", header)
                bundle.require(signature == b"PK\x03\x04" and flags == info.flag_bits and compression == info.compress_type)
                bundle.require(raw.read(name_size) == info.filename.encode("ascii"))
                extra = raw.read(extra_size)
                bundle.require(len(extra) == extra_size)
                zip64_header = expanded == 0xFFFFFFFF or compressed == 0xFFFFFFFF
                if not flags & 8:
                    if expanded == 0xFFFFFFFF or compressed == 0xFFFFFFFF:
                        cursor = 0
                        zip64 = None
                        while cursor + 4 <= len(extra):
                            kind, size = struct.unpack_from("<HH", extra, cursor)
                            cursor += 4
                            value = extra[cursor:cursor + size]
                            bundle.require(len(value) == size)
                            if kind == 1:
                                bundle.require(zip64 is None)
                                zip64 = value
                            cursor += size
                        bundle.require(cursor == len(extra) and zip64 is not None)
                        assert zip64 is not None
                        bundle.require(len(zip64) % 8 == 0 and len(zip64) >= 8 * (
                            int(expanded == 0xFFFFFFFF) + int(compressed == 0xFFFFFFFF)))
                        values = list(struct.unpack("<" + "Q" * (len(zip64) // 8), zip64))
                        if expanded == 0xFFFFFFFF:
                            expanded = values.pop(0)
                        if compressed == 0xFFFFFFFF:
                            compressed = values.pop(0)
                    bundle.require(crc == info.CRC and compressed == info.compress_size and expanded == info.file_size)
                start = info.header_offset
                end = start + 30 + name_size + extra_size + info.compress_size
                if flags & 8:
                    raw.seek(end)
                    first = raw.read(4)
                    signed = first == b"PK\x07\x08"
                    descriptor = raw.read(4) if signed else first
                    wide = zip64_header or info.file_size > 0xFFFFFFFF or info.compress_size > 0xFFFFFFFF
                    descriptor += raw.read(16 if wide else 8)
                    bundle.require(len(descriptor) == (20 if wide else 12))
                    actual_crc, actual_compressed, actual_expanded = struct.unpack("<IQQ" if wide else "<III", descriptor)
                    bundle.require((actual_crc, actual_compressed, actual_expanded)
                                   == (info.CRC, info.compress_size, info.file_size))
                    end += len(descriptor) + (4 if signed else 0)
                bundle.require(0 <= start < end <= container.start_dir)
                intervals.append((start, end))
                target = output / info.filename
                parent = output
                for component in Path(info.filename).parts[:-1]:
                    parent /= component
                    parent.mkdir(exist_ok=True, mode=0o700)
                    parent.chmod(0o700)
                digest = hashlib.sha256()
                length = 0
                with container.open(info) as source, target.open("xb") as destination:
                    target.chmod(0o600)
                    while data := source.read(1048576):
                        length += len(data)
                        total += len(data)
                        bundle.require(length <= info.file_size and total <= limits["expanded_bytes"], "DELIVERY_LIMIT")
                        digest.update(data)
                        destination.write(data)
                bundle.require(length == info.file_size and digest.hexdigest() == expected[info.filename]["sha256"], "DELIVERY_SUBJECT_MISMATCH")
            intervals.sort()
            bundle.require(intervals[0][0] == 0 and intervals[-1][1] == container.start_dir
                           and all(a[1] == b[0] for a, b in zip(intervals, intervals[1:])))
            bundle.require(total == part["expanded_bytes"], "DELIVERY_COMPANION_SIZE")
    except BaseException:
        shutil.rmtree(output)
        raise
