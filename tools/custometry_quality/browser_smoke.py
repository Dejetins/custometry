from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Callable, Sequence

from .core import (
    CheckResult,
    JsonObject,
    add_common_arguments,
    add_command_failure,
    json_list,
    json_object,
    json_string,
    load_json,
    main_guard,
    render_result,
    require_file,
    run_command,
    string_list,
)


LIFECYCLE = "self-contained-disposable"


def _manifest(
    root: Path, data: JsonObject
) -> tuple[list[str], dict[str, str], list[dict[str, str]]]:
    if data.get("schema_version") != 1:
        raise ValueError("browser manifest requires schema_version=1")
    runtime = json_object(data.get("runtime"), "runtime")
    if runtime.get("lifecycle") != LIFECYCLE:
        raise ValueError(f"runtime.lifecycle must be {LIFECYCLE!r}")
    command = string_list(runtime.get("command"), "runtime.command", non_empty=True)
    if command[0] not in {"bash", "sh"} or len(command) < 2:
        raise ValueError("runtime.command must invoke a repository-owned shell lifecycle script")
    script = Path(command[1])
    if script.is_absolute() or ".." in script.parts or not (root / script).is_file():
        raise ValueError("runtime.command lifecycle script must be a repository-relative file")
    if any(token in {"npx", "--yes"} or "://" in token for token in command):
        raise ValueError("runtime.command cannot download tooling or target an external URL")
    environment_raw = json_object(runtime.get("environment"), "runtime.environment")
    environment: dict[str, str] = {}
    for key, value in environment_raw.items():
        if key != "CUSTOMETRY_RUN_BROWSER" or value != "1":
            raise ValueError("runtime.environment must contain only CUSTOMETRY_RUN_BROWSER=1")
        environment[key] = "1"
    if environment != {"CUSTOMETRY_RUN_BROWSER": "1"}:
        raise ValueError("runtime.environment requires CUSTOMETRY_RUN_BROWSER=1")
    journey_values = json_list(data.get("journeys"), "journeys")
    if not journey_values:
        raise ValueError("journeys must be a non-empty list")
    required = ("name", "path", "assert_text")
    journeys: list[dict[str, str]] = []
    names: set[str] = set()
    for index, value in enumerate(journey_values):
        journey = json_object(value, f"journeys[{index}]")
        normalized = {
            key: json_string(journey.get(key), f"journeys[{index}].{key}") for key in required
        }
        if not normalized["path"].startswith("/") or ".." in normalized["path"].split("/"):
            raise ValueError(f"journeys[{index}].path must be a safe local absolute path")
        if normalized["name"] in names:
            raise ValueError(f"duplicate journey name: {normalized['name']}")
        names.add(normalized["name"])
        journeys.append(normalized)
    return command, environment, journeys


def check(
    root: Path,
    *,
    mode: str,
    manifest: Path,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> CheckResult:
    result = CheckResult("browser_smoke")
    if mode not in {"static", "runtime"}:
        result.add("browser-mode-invalid", f"unsupported mode {mode}")
        return result
    manifest_path = root / manifest
    if not require_file(manifest_path, result):
        return result
    try:
        command, environment, journeys = _manifest(root, load_json(manifest_path))
    except ValueError as exc:
        result.add("browser-manifest-invalid", str(exc), manifest_path)
        return result
    result.details.update(
        mode=mode,
        lifecycle=LIFECYCLE,
        journeys=len(journeys),
        command=" ".join(command),
    )
    if mode == "static":
        return result
    completed = run_command(
        command,
        cwd=root,
        runner=runner,
        timeout=1800,
        env=environment,
    )
    if completed.returncode != 0:
        add_command_failure(result, command, completed, code="browser-smoke-failed")
    result.details["runtime_observed"] = result.ok
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate or execute a self-contained disposable real-browser smoke lifecycle"
    )
    add_common_arguments(parser)
    parser.add_argument("--mode", choices=("static", "runtime"), default="static")
    parser.add_argument("--manifest", type=Path, default=Path("tests/e2e/browser-smoke.json"))
    args = parser.parse_args(argv)
    return render_result(
        check(args.root.resolve(), mode=args.mode, manifest=args.manifest), args.json
    )


if __name__ == "__main__":
    main_guard(cli)
