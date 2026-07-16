#!/usr/bin/env python3
"""Validate and canonicalize an immutable Custometry release manifest."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path


MAX_MANIFEST_BYTES = 4096
REQUIRED_KEYS = (
    "CUSTOMETRY_VERSION",
    "CUSTOMETRY_API_IMAGE",
    "CUSTOMETRY_WEB_IMAGE",
)
SEMVER_IDENTIFIER = r"(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
SEMVER_PATTERN = re.compile(
    rf"(?:0|[1-9][0-9]*)\."
    rf"(?:0|[1-9][0-9]*)\."
    rf"(?:0|[1-9][0-9]*)"
    rf"(?:-{SEMVER_IDENTIFIER}(?:\.{SEMVER_IDENTIFIER})*)?"
    rf"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)
IMAGE_PATTERNS = {
    "CUSTOMETRY_API_IMAGE": re.compile(
        r"ghcr\.io/dejetins/custometry-api@sha256:[0-9a-f]{64}"
    ),
    "CUSTOMETRY_WEB_IMAGE": re.compile(
        r"ghcr\.io/dejetins/custometry-web@sha256:[0-9a-f]{64}"
    ),
}
LINE_PATTERN = re.compile(r"([A-Z][A-Z0-9_]*)=([ -~]+)")


class ManifestError(ValueError):
    """Raised when a release manifest is not safe to consume."""


def parse_manifest(raw: bytes) -> dict[str, str]:
    if len(raw) > MAX_MANIFEST_BYTES:
        raise ManifestError(f"file exceeds {MAX_MANIFEST_BYTES} bytes")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise ManifestError("file must contain ASCII text only") from error

    if any(
        character != "\n" and (ord(character) < 32 or ord(character) == 127)
        for character in text
    ):
        raise ManifestError("control characters are forbidden")

    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if not lines or any(not line for line in lines):
        raise ManifestError("blank or missing lines are forbidden")

    values: dict[str, str] = {}
    for line_number, line in enumerate(lines, start=1):
        match = LINE_PATTERN.fullmatch(line)
        if match is None:
            raise ManifestError(f"line {line_number} must use exact KEY=value syntax")
        key, value = match.groups()
        if key not in REQUIRED_KEYS:
            raise ManifestError(f"line {line_number} contains unknown key {key}")
        if key in values:
            raise ManifestError(f"line {line_number} duplicates key {key}")
        values[key] = value

    missing = [key for key in REQUIRED_KEYS if key not in values]
    if missing:
        raise ManifestError(f"missing required key {missing[0]}")

    if SEMVER_PATTERN.fullmatch(values["CUSTOMETRY_VERSION"]) is None:
        raise ManifestError("CUSTOMETRY_VERSION must be valid SemVer without a v prefix")
    for key, pattern in IMAGE_PATTERNS.items():
        if pattern.fullmatch(values[key]) is None:
            raise ManifestError(
                f"{key} must be the expected GHCR repository pinned by a lowercase sha256 digest"
            )
    return values


def write_canonical_manifest(path: Path, values: dict[str, str]) -> None:
    path_parent = path.parent
    if not path_parent.is_dir():
        raise ManifestError(f"output directory does not exist: {path_parent}")

    payload = "".join(f"{key}={values[key]}\n" for key in REQUIRED_KEYS).encode("ascii")
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=path_parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(payload)
            temporary.flush()
            os.fsync(temporary.fileno())
        temporary_path.chmod(0o600)
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def validate_manifest(input_path: Path, output_path: Path) -> None:
    if not input_path.is_file():
        raise ManifestError(f"input file does not exist: {input_path}")
    if input_path.resolve() == output_path.resolve():
        raise ManifestError("input and canonical output paths must differ")
    values = parse_manifest(input_path.read_bytes())
    write_canonical_manifest(output_path, values)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_path", type=Path)
    arguments = parser.parse_args()
    try:
        validate_manifest(arguments.input_path, arguments.output_path)
    except (ManifestError, OSError) as error:
        print(f"Invalid release manifest {arguments.input_path}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
