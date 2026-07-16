from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Sequence

from .core import (
    CheckResult,
    add_common_arguments,
    canonical_json,
    main_guard,
    parse_frontmatter,
    render_result,
    require_file,
    stable_ids,
    write_or_check,
)


DEFINITION_PATTERN = re.compile(r"^\s*-\s+id:\s+([A-Z][A-Z0-9_-]+-[0-9]{3})\s*$")


def build_index(machine_path: Path, human_path: Path) -> dict[str, Any]:
    machine_meta, _ = parse_frontmatter(machine_path)
    machine_text = machine_path.read_text(encoding="utf-8")
    human_text = human_path.read_text(encoding="utf-8")
    all_ids = sorted(stable_ids(machine_text))
    lines_by_id: dict[str, list[int]] = {identifier: [] for identifier in all_ids}
    definition_lines: dict[str, int] = {}
    for number, line in enumerate(machine_text.splitlines(), 1):
        for identifier in stable_ids(line):
            lines_by_id.setdefault(identifier, []).append(number)
        match = DEFINITION_PATTERN.match(line)
        if match:
            definition_lines[match.group(1)] = number
    human_ids = stable_ids(human_text)
    records: list[dict[str, Any]] = []
    for identifier in all_ids:
        records.append(
            {
                "id": identifier,
                "family": identifier.rsplit("-", 1)[0],
                "definition_line": definition_lines.get(identifier),
                "machine_occurrences": lines_by_id[identifier],
                "present_in_human": identifier in human_ids,
            }
        )
    return {
        "schema_version": 1,
        "document_family_id": machine_meta.get("document_family_id"),
        "spec_version": machine_meta.get("spec_version"),
        "source": machine_path.name,
        "human_mirror": human_path.name,
        "requirement_count": len(records),
        "requirements": records,
    }


def check(
    root: Path,
    *,
    machine: Path,
    human: Path,
    output: Path,
    check_mode: bool,
) -> CheckResult:
    result = CheckResult("generate_requirement_index")
    machine_path = root / machine
    human_path = root / human
    output_path = root / output
    if not require_file(machine_path, result) or not require_file(human_path, result):
        return result
    try:
        index = build_index(machine_path, human_path)
    except ValueError as exc:
        result.add("invalid-blueprint", str(exc))
        return result
    missing = [item["id"] for item in index["requirements"] if not item["present_in_human"]]
    if missing:
        result.add("human-mirror-missing-ids", f"missing IDs: {', '.join(missing[:20])}", human_path)
    write_or_check(output_path, canonical_json(index), check_mode, result)
    result.details["requirements"] = index["requirement_count"]
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate deterministic requirement index")
    add_common_arguments(parser)
    parser.add_argument("--machine", type=Path, default=Path("custometry-technical-blueprint-ru.md"))
    parser.add_argument(
        "--human", type=Path, default=Path("custometry-technical-blueprint-human-ru.md")
    )
    parser.add_argument(
        "--output", type=Path, default=Path("docs/generated/requirement-index.json")
    )
    parser.add_argument("--check", action="store_true", help="fail when output is absent or stale")
    return parser


def cli(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = check(
        args.root.resolve(),
        machine=args.machine,
        human=args.human,
        output=args.output,
        check_mode=args.check,
    )
    return render_result(result, args.json)


if __name__ == "__main__":
    main_guard(cli)
