from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence, TypeAlias, cast

import yaml


EXIT_OK = 0
EXIT_VALIDATION_FAILED = 1
EXIT_USAGE = 2

JsonScalar: TypeAlias = None | bool | int | float | str
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]


def json_object(value: object, label: str) -> JsonObject:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return cast(JsonObject, value)


def json_list(value: object, label: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    return cast(list[JsonValue], value)


def string_list(value: object, label: str, *, non_empty: bool = False) -> list[str]:
    items = json_list(value, label)
    if (non_empty and not items) or not all(isinstance(item, str) and item for item in items):
        requirement = "a non-empty list of non-empty strings" if non_empty else "a list of non-empty strings"
        raise ValueError(f"{label} must be {requirement}")
    return cast(list[str], items)


def json_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")
    return value


def json_integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{label} must be an integer")
    return value


def json_number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a number")
    return float(value)


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    message: str
    path: str | None = None
    line: int | None = None


@dataclass(slots=True)
class CheckResult:
    check: str
    observed: bool = True
    findings: list[Finding] = field(default_factory=lambda: [])
    details: dict[str, Any] = field(default_factory=lambda: {})

    @property
    def ok(self) -> bool:
        return self.observed and not self.findings

    def add(
        self,
        code: str,
        message: str,
        path: Path | str | None = None,
        line: int | None = None,
    ) -> None:
        self.findings.append(
            Finding(code=code, message=message, path=str(path) if path else None, line=line)
        )

    def merge(self, other: CheckResult) -> None:
        self.observed = self.observed and other.observed
        self.findings.extend(other.findings)
        self.details[other.check] = other.details

    def to_dict(self) -> dict[str, Any]:
        return {
            "check": self.check,
            "status": "passed" if self.ok else "failed",
            "observed": self.observed,
            "findings": [asdict(item) for item in self.findings],
            "details": self.details,
        }


def repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / ".codex/AGENTS.md").is_file():
            return candidate
    raise ValueError(f"repository root not found from {current}")


def require_file(path: Path, result: CheckResult, code: str = "missing-input") -> bool:
    if not path.is_file():
        result.observed = False
        result.add(code, "required file does not exist", path)
        return False
    return True


def require_dir(path: Path, result: CheckResult, code: str = "missing-input") -> bool:
    if not path.is_dir():
        result.observed = False
        result.add(code, "required directory does not exist", path)
        return False
    return True


def load_json(path: Path) -> JsonObject:
    try:
        value = cast(object, json.loads(path.read_text(encoding="utf-8")))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"JSON document root must be an object in {path}")
    return cast(JsonObject, value)


def load_yaml(path: Path) -> JsonObject:
    try:
        value = cast(object, yaml.safe_load(path.read_text(encoding="utf-8")))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"YAML document root must be a mapping in {path}")
    return cast(JsonObject, value)


def parse_frontmatter(path: Path) -> tuple[JsonObject, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing YAML frontmatter in {path}")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"unterminated YAML frontmatter in {path}")
    try:
        data = cast(object, yaml.safe_load(text[4:end]) or {})
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML frontmatter in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"frontmatter must be a mapping in {path}")
    return cast(JsonObject, data), text[end + 5 :]


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_paths(paths: Iterable[Path], root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted((item.resolve() for item in paths), key=lambda item: item.as_posix()):
        rel = path.relative_to(root.resolve()).as_posix()
        digest.update(rel.encode("utf-8") + b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def write_or_check(path: Path, payload: bytes, check: bool, result: CheckResult) -> None:
    if check:
        if not path.is_file():
            result.observed = False
            result.add("generated-artifact-missing", "generated artifact is absent", path)
            return
        if path.read_bytes() != payload:
            result.add("generated-artifact-drift", "generated artifact is stale", path)
            return
        result.details["artifact"] = str(path)
        result.details["mode"] = "check"
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_bytes(payload)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    result.details["artifact"] = str(path)
    result.details["mode"] = "write"


def render_result(result: CheckResult, json_output: bool = False) -> int:
    if json_output:
        print(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True, indent=2))
    else:
        status = "PASS" if result.ok else "FAIL"
        print(f"{status} {result.check} (observed={str(result.observed).lower()})")
        for finding in result.findings:
            location = ""
            if finding.path:
                location = f" {finding.path}"
                if finding.line is not None:
                    location += f":{finding.line}"
            print(f"  [{finding.code}]{location} {finding.message}")
        for key, value in sorted(result.details.items()):
            if not isinstance(value, (dict, list)):
                print(f"  {key}: {value}")
    return EXIT_OK if result.ok else EXIT_VALIDATION_FAILED


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--json", action="store_true", help="emit machine-readable result")


Runner = Callable[..., subprocess.CompletedProcess[str]]


def run_command(
    command: Sequence[str],
    *,
    cwd: Path,
    timeout: int = 300,
    env: Mapping[str, str] | None = None,
    runner: Runner = subprocess.run,
) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return runner(
        list(command),
        cwd=cwd,
        env=merged_env,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def add_command_failure(
    result: CheckResult,
    command: Sequence[str],
    completed: subprocess.CompletedProcess[str],
    *,
    code: str = "command-failed",
) -> None:
    output = (completed.stderr or completed.stdout or "").strip()
    if len(output) > 1000:
        output = output[-1000:]
    result.add(code, f"{' '.join(command)} exited {completed.returncode}: {output}")


def safe_relative(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    try:
        return resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"path escapes repository root: {path}") from exc


def flatten_json(value: JsonValue, prefix: str = "") -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise ValueError("catalog root must be a JSON object")
    flat: dict[str, JsonValue] = {}
    for key, item in value.items():
        if not key:
            raise ValueError("catalog keys must be non-empty strings")
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(item, dict):
            flat.update(flatten_json(item, path))
        else:
            flat[path] = item
    return flat


ID_PATTERN = re.compile(r"\b([A-Z][A-Z0-9_-]+-[0-9]{3})\b")


def stable_ids(text: str) -> set[str]:
    return set(ID_PATTERN.findall(text))


def main_guard(run: Callable[[], int]) -> None:
    try:
        raise SystemExit(run())
    except BrokenPipeError:
        sys.stderr.close()
        raise SystemExit(EXIT_USAGE) from None
