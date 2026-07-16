from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .core import (
    CheckResult,
    add_common_arguments,
    json_object,
    json_string,
    main_guard,
    parse_frontmatter,
    render_result,
    require_file,
    stable_ids,
)


def check(root: Path, machine: Path, human: Path) -> CheckResult:
    result = CheckResult("validate_blueprints")
    machine_path = root / machine
    human_path = root / human
    if not require_file(machine_path, result) or not require_file(human_path, result):
        return result
    try:
        machine_meta, _ = parse_frontmatter(machine_path)
        human_meta, _ = parse_frontmatter(human_path)
    except ValueError as exc:
        result.add("frontmatter-invalid", str(exc))
        return result
    for key in ("document_family_id", "spec_version"):
        if machine_meta.get(key) != human_meta.get(key):
            result.add(
                "blueprint-metadata-drift",
                f"{key} differs: machine={machine_meta.get(key)!r}, human={human_meta.get(key)!r}",
            )
    if machine_meta.get("representation") != "machine" or machine_meta.get("normative") is not True:
        result.add("machine-authority-invalid", "machine blueprint must be representation=machine and normative=true")
    if human_meta.get("representation") != "human" or human_meta.get("normative") is not False:
        result.add("human-authority-invalid", "human blueprint must be representation=human and normative=false")
    try:
        alternate = json_object(machine_meta.get("alternate_document"), "alternate_document")
        source = json_object(human_meta.get("source_of_truth"), "source_of_truth")
    except ValueError as exc:
        result.add("blueprint-link-invalid", str(exc))
        return result
    alternate_path = Path(json_string(alternate.get("path"), "alternate_document.path"))
    source_path = Path(json_string(source.get("path"), "source_of_truth.path"))
    if (
        alternate_path.is_absolute()
        or ".." in alternate_path.parts
        or (machine_path.parent / alternate_path).resolve() != human_path.resolve()
    ):
        result.add("machine-link-invalid", "machine alternate_document does not point to human mirror")
    if (
        source_path.is_absolute()
        or ".." in source_path.parts
        or (human_path.parent / source_path).resolve() != machine_path.resolve()
    ):
        result.add("human-link-invalid", "human source_of_truth does not point to machine blueprint")
    if alternate.get("expected_spec_version") != machine_meta.get("spec_version"):
        result.add("machine-expected-version-drift", "alternate expected_spec_version is stale")
    if source.get("expected_spec_version") != human_meta.get("spec_version"):
        result.add("human-expected-version-drift", "source expected_spec_version is stale")
    machine_ids = stable_ids(machine_path.read_text(encoding="utf-8"))
    human_ids = stable_ids(human_path.read_text(encoding="utf-8"))
    missing = sorted(machine_ids - human_ids)
    extra = sorted(human_ids - machine_ids)
    if missing:
        result.add("human-mirror-missing-ids", f"missing IDs: {', '.join(missing[:30])}", human_path)
    if extra:
        result.add("human-mirror-extra-ids", f"extra IDs: {', '.join(extra[:30])}", human_path)
    result.details.update(
        spec_version=machine_meta.get("spec_version"), requirement_ids=len(machine_ids)
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate machine/human blueprint synchronization")
    add_common_arguments(parser)
    parser.add_argument("--machine", type=Path, default=Path("custometry-technical-blueprint-ru.md"))
    parser.add_argument(
        "--human", type=Path, default=Path("custometry-technical-blueprint-human-ru.md")
    )
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve(), args.machine, args.human), args.json)


if __name__ == "__main__":
    main_guard(cli)
