from __future__ import annotations

import argparse
import re
import tomllib
from pathlib import Path
from typing import Sequence

from .core import (
    CheckResult,
    add_common_arguments,
    main_guard,
    parse_frontmatter,
    render_result,
    require_dir,
)


RANGE = re.compile(r"([A-Z][A-Z0-9_-]+)-([0-9]{3})(?:\.\.|…)([0-9]{3})")
CYRILLIC = re.compile(r"[\u0400-\u04FF]")
REQUIRED_RESULT_TERMS = ("status", "mode", "contract impact", "next owner")
ENGLISH_AGENT_ARTIFACTS = (
    Path("AGENTS.md"),
    Path("CONTRIBUTING.md"),
    Path("README.md"),
    Path("SECURITY.md"),
    Path(".codex/AGENTS.md"),
    Path(".codex/PLANS.md"),
    Path(".codex/agents/prompt_template.md"),
    Path(".codex/agents/stage_execution_ledger_template.md"),
    Path(".codex/agents/iteration_report_template.md"),
)


def _maxima(blueprint: str) -> dict[str, int]:
    maxima: dict[str, int] = {}
    for prefix, number in re.findall(r"\b([A-Z][A-Z0-9_-]+)-([0-9]{3})\b", blueprint):
        maxima[prefix] = max(maxima.get(prefix, 0), int(number))
    return maxima


def _check_english_artifact(
    root: Path,
    relative_path: Path,
    result: CheckResult,
) -> str:
    path = root / relative_path
    try:
        source = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    if CYRILLIC.search(source):
        result.add(
            "agent-artifact-language-invalid",
            "repository governance, contributor, agent, registry, profile, and template artifacts must be written in English",
            path,
        )
    return source


def check(root: Path, profiles: Path = Path(".codex/agents")) -> CheckResult:
    result = CheckResult("validate_agent_profiles")
    profile_root = root / profiles
    if not require_dir(profile_root, result):
        return result
    machine = root / "custometry-technical-blueprint-ru.md"
    if not machine.is_file():
        result.observed = False
        result.add("blueprint-missing", "machine blueprint is required", machine)
        return result
    maxima = _maxima(machine.read_text(encoding="utf-8"))
    files = sorted(profile_root.glob("*.toml"))
    if not files:
        result.add("profiles-missing", "no agent TOML profiles found", profile_root)
        return result
    seen_names: set[str] = set()
    for path in files:
        source = _check_english_artifact(root, path.relative_to(root), result)
        try:
            data = tomllib.loads(source)
        except tomllib.TOMLDecodeError as exc:
            result.add("profile-toml-invalid", str(exc), path)
            continue
        name = data.get("name")
        description = data.get("description")
        instructions = data.get("developer_instructions")
        if not isinstance(name, str) or name != path.stem:
            result.add("profile-name-invalid", "name must equal filename stem", path)
        elif name in seen_names:
            result.add("profile-name-duplicate", f"duplicate profile name {name}", path)
        else:
            seen_names.add(name)
        if (
            not isinstance(description, str)
            or "Use for " not in description
            or "Do not use for " not in description
        ):
            result.add(
                "profile-description-invalid",
                "description needs `Use for` and `Do not use for`",
                path,
            )
        if not isinstance(instructions, str) or not instructions.strip():
            result.add(
                "profile-instructions-missing", "developer_instructions must be non-empty", path
            )
            continue
        lower = instructions.lower().replace("_", " ")
        for term in REQUIRED_RESULT_TERMS:
            if term not in lower:
                result.add(
                    "profile-result-contract-incomplete", f"missing result term: {term}", path
                )
        if "complete" not in lower or "partial" not in lower or "blocked" not in lower:
            result.add(
                "profile-status-semantics-incomplete",
                "complete/partial/blocked semantics required",
                path,
            )
        for prefix, _start, end in RANGE.findall(instructions):
            if prefix in maxima and int(end) != maxima[prefix]:
                result.add(
                    "stale-requirement-range",
                    f"{prefix} range ends at {end}, blueprint maximum is {maxima[prefix]:03d}",
                    path,
                )
    try:
        spec, _ = parse_frontmatter(root / "custometry-technical-blueprint-ru.md")
    except ValueError as exc:
        result.add("blueprint-frontmatter-invalid", str(exc), machine)
        return result
    expected = spec.get("spec_version")
    for relative_template in ENGLISH_AGENT_ARTIFACTS:
        template = root / relative_template
        _check_english_artifact(root, relative_template, result)
        if template.suffix != ".md" or template.parent != root / ".codex/agents":
            continue
        try:
            meta, _ = parse_frontmatter(template)
        except (ValueError, FileNotFoundError) as exc:
            result.add("agent-template-invalid", str(exc), template)
            continue
        if meta.get("spec_version") != expected:
            result.add(
                "agent-template-version-drift", f"expected spec_version {expected}", template
            )
    result.details["profiles"] = len(files)
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate agent profile schema and blueprint drift"
    )
    add_common_arguments(parser)
    parser.add_argument("--profiles", type=Path, default=Path(".codex/agents"))
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve(), args.profiles), args.json)


if __name__ == "__main__":
    main_guard(cli)
