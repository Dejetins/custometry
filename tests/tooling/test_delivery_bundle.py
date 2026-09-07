"""S01 structural contract checks; no signature/archive/runtime claims."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
READER = ROOT / "deploy/compose/validate-delivery-manifest.py"
FIXTURE = ROOT / "tests/tooling/fixtures/delivery-manifest.valid.json"
POLICY = ROOT / "deploy/compose/delivery-verification-policy.json"
SPEC = importlib.util.spec_from_file_location("delivery_structure", READER)
assert SPEC is not None and SPEC.loader is not None
reader = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reader)


def run(path: Path, *, policy: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(READER), str(path), *(["--policy"] if policy else [])],
                          capture_output=True, text=True, check=False)


def test_real_schema_policy_and_fixture() -> None:
    for path, policy in ((FIXTURE, False), (POLICY, True)):
        result = run(path, policy=policy)
        assert result.returncode == 0, result.stdout
        assert json.loads(result.stdout)["code"] == "DELIVERY_STRUCTURE_VALID"


@pytest.mark.parametrize(("keys", "value"), [
    (("schema_version",), "custometry-delivery/v2"),
    (("channel",), "official-release"),
    (("unexpected",), "secret"),
    (("producer", "ref"), "refs/heads/untrusted"),
    (("producer", "run_id"), True),
    (("producer", "run_id"), 0),
    (("source", "commit"), "short-sha"),
    (("images", "api", "repository"), "ghcr.io/attacker/custometry-api"),
    (("images", "web", "index_digest"), "sha256:" + "A" * 64),
    (("images", "api", "platforms", 0, "architecture"), "riscv64"),
    (("files", 0, "path"), "../outside"),
    (("files", 0, "path"), "/absolute"),
    (("files", 0, "path"), "a/../escape"),
    (("files", 0, "path"), "a\\escape"),
    (("files", 0, "path"), "a//b"),
    (("files", 0, "path"), "a/%2e%2e"),
    (("files", 0, "path"), "a/./b"),
    (("files", 0, "path"), "a/"),
    (("files", 0, "size_bytes"), -1),
    (("files", 0, "size_bytes"), 67108865),
    (("files", 0, "sha256"), "a" * 63),
    (("compatibility", "reader_major"), 2),
    (("compatibility", "supported_platforms"), ["linux/amd64"]),
    (("migrations", "starting_state"), "existing-production"),
    (("migrations", "command"), ["sh", "-c", "untrusted"]),
    (("resources_budget", "ram_bytes"), 6442450945),
    (("signature", "subject"), "archive-name"),
])
def test_negative_contract_fields(tmp_path: Path, keys: tuple[str | int, ...], value: Any) -> None:
    fixture: Any = json.loads(FIXTURE.read_text())
    cursor = fixture
    for key in keys[:-1]:
        cursor = cursor[key]
    cursor[keys[-1]] = value
    candidate = tmp_path / "invalid.json"
    candidate.write_text(json.dumps(fixture))
    result = run(candidate)
    assert result.returncode == 2
    assert json.loads(result.stdout)["result"] == "fail"
    assert "secret" not in result.stdout and str(candidate) not in result.stdout


@pytest.mark.parametrize("raw", [
    b'{"schema_version":1,"schema_version":2}',
    b'{"nested":{"x":1,"x":2}}', b'{"a":NaN}', b'{"a":Infinity}', b'{"a":1.5}',
    b'{"a":"\\u00e9"}', b'{"a":"\\u0000"}', b'\xef\xbb\xbf{}', b'{} trailing',
    b'[' * 10000 + b']' * 10000, b' ' * 1048577,
])
def test_bounded_json_reader_rejects_ambiguous_bytes(raw: bytes) -> None:
    with pytest.raises(reader.InvalidDelivery):
        reader.parse_json(raw)


def test_canonical_bytes_and_unknown_schema_keyword() -> None:
    assert reader.canonical_bytes({"z": 2, "a": 1}) == b'{"a":1,"z":2}'
    with pytest.raises(reader.InvalidDelivery):
        reader.check_schema({"unimplemented_validation_keyword": True}, {})
    with pytest.raises(reader.InvalidDelivery):
        reader.check_schema({"$ref": "https://untrusted/schema"}, {})


@pytest.mark.parametrize("field", ["signer", "limits", "origin", "verification", "scanner"])
def test_policy_does_not_allow_relaxation(tmp_path: Path, field: str) -> None:
    policy: dict[str, Any] = json.loads(POLICY.read_text())
    policy[field] = {}
    path = tmp_path / "policy.json"
    path.write_text(json.dumps(policy))
    assert run(path, policy=True).returncode == 2


def test_required_fields_and_identical_array_entries_fail(tmp_path: Path) -> None:
    fixture: dict[str, Any] = json.loads(FIXTURE.read_text())
    del fixture["migrations"]
    path = tmp_path / "fixture.json"
    path.write_text(json.dumps(fixture))
    assert run(path).returncode == 2
    fixture = json.loads(FIXTURE.read_text())
    fixture["files"] *= 2
    path.write_text(json.dumps(fixture))
    assert run(path).returncode == 2
