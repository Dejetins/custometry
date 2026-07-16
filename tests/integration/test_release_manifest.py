from __future__ import annotations

import stat
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "deploy/compose/validate-release-manifest.py"
API_IMAGE = "ghcr.io/dejetins/custometry-api@sha256:" + "a" * 64
WEB_IMAGE = "ghcr.io/dejetins/custometry-web@sha256:" + "b" * 64


def manifest(
    *,
    version: str = "0.1.0-dev.0+sha.0123456789ab",
    api_image: str = API_IMAGE,
    web_image: str = WEB_IMAGE,
) -> str:
    return (
        f"CUSTOMETRY_VERSION={version}\n"
        f"CUSTOMETRY_API_IMAGE={api_image}\n"
        f"CUSTOMETRY_WEB_IMAGE={web_image}\n"
    )


def run_validator(
    tmp_path: Path,
    payload: str | bytes,
) -> tuple[subprocess.CompletedProcess[str], Path]:
    input_path = tmp_path / "candidate.env"
    output_path = tmp_path / "canonical.env"
    if isinstance(payload, bytes):
        input_path.write_bytes(payload)
    else:
        input_path.write_text(payload, encoding="ascii")
    completed = subprocess.run(
        ["python3", str(VALIDATOR), str(input_path), str(output_path)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed, output_path


def test_valid_manifest_is_written_in_canonical_order_with_private_mode(tmp_path: Path) -> None:
    payload = (
        f"CUSTOMETRY_WEB_IMAGE={WEB_IMAGE}\n"
        "CUSTOMETRY_VERSION=1.2.3-rc.1+build.7\n"
        f"CUSTOMETRY_API_IMAGE={API_IMAGE}\n"
    )

    completed, output_path = run_validator(tmp_path, payload)

    assert completed.returncode == 0
    assert output_path.read_text(encoding="ascii") == manifest(version="1.2.3-rc.1+build.7")
    assert stat.S_IMODE(output_path.stat().st_mode) == 0o600


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        (manifest(version="$(id)"), "valid SemVer"),
        (manifest(version="1.2.3;id"), "valid SemVer"),
        (
            manifest() + "CUSTOMETRY_EXTRA=unexpected\n",
            "unknown key CUSTOMETRY_EXTRA",
        ),
        (
            manifest() + f"CUSTOMETRY_API_IMAGE={API_IMAGE}\n",
            "duplicates key CUSTOMETRY_API_IMAGE",
        ),
        (
            manifest().replace(f"CUSTOMETRY_WEB_IMAGE={WEB_IMAGE}\n", ""),
            "missing required key CUSTOMETRY_WEB_IMAGE",
        ),
        (
            manifest(api_image="ghcr.io/example/custometry-api@sha256:" + "a" * 64),
            "expected GHCR repository",
        ),
        (
            manifest(api_image="ghcr.io/dejetins/custometry-api:latest"),
            "lowercase sha256 digest",
        ),
        (
            manifest(api_image="ghcr.io/dejetins/custometry-api@sha256:" + "A" * 64),
            "lowercase sha256 digest",
        ),
        (
            manifest(api_image="ghcr.io/dejetins/custometry-api@sha256:" + "a" * 63),
            "lowercase sha256 digest",
        ),
        (
            manifest().replace("CUSTOMETRY_VERSION=", " CUSTOMETRY_VERSION="),
            "exact KEY=value syntax",
        ),
        (
            manifest().replace("CUSTOMETRY_VERSION=", "export CUSTOMETRY_VERSION="),
            "exact KEY=value syntax",
        ),
        (
            manifest().replace("CUSTOMETRY_VERSION=0.1", "CUSTOMETRY_VERSION=0.1\x00"),
            "control characters",
        ),
        (
            manifest().replace("\nCUSTOMETRY_API_IMAGE", "\r\nCUSTOMETRY_API_IMAGE"),
            "control characters",
        ),
    ],
)
def test_invalid_manifest_is_rejected_without_output(
    tmp_path: Path,
    payload: str,
    message: str,
) -> None:
    completed, output_path = run_validator(tmp_path, payload.encode("ascii"))

    assert completed.returncode == 2
    assert message in completed.stderr
    assert not output_path.exists()


def test_non_ascii_and_oversized_manifests_are_rejected(tmp_path: Path) -> None:
    completed, output_path = run_validator(tmp_path, manifest().encode("ascii") + "é".encode())
    assert completed.returncode == 2
    assert "ASCII text only" in completed.stderr
    assert not output_path.exists()

    completed, output_path = run_validator(tmp_path, b"A" * 4097)
    assert completed.returncode == 2
    assert "exceeds 4096 bytes" in completed.stderr
    assert not output_path.exists()
