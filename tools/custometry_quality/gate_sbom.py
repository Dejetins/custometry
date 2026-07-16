from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Sequence

from .core import (
    CheckResult,
    JsonObject,
    add_common_arguments,
    json_list,
    json_object,
    json_string,
    load_json,
    main_guard,
    render_result,
    require_file,
)


SUBJECT_PROPERTY = "custometry:subject-digest"
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")


def _components(data: JsonObject) -> tuple[str, list[dict[str, Any]]]:
    if data.get("bomFormat") == "CycloneDX":
        json_string(data.get("specVersion"), "specVersion")
        values = json_list(data.get("components"), "components")
        return "cyclonedx", [json_object(value, f"components[{index}]") for index, value in enumerate(values)]
    if str(data.get("spdxVersion", "")).startswith("SPDX-"):
        values = json_list(data.get("packages"), "packages")
        return "spdx", [json_object(value, f"packages[{index}]") for index, value in enumerate(values)]
    raise ValueError("unsupported SBOM format; CycloneDX or SPDX JSON required")


def _subjects(data: JsonObject) -> set[str]:
    metadata_raw = data.get("metadata")
    if metadata_raw is None:
        return set()
    metadata = json_object(metadata_raw, "metadata")
    properties_raw = metadata.get("properties")
    if properties_raw is None:
        return set()
    properties = json_list(properties_raw, "metadata.properties")
    result: set[str] = set()
    for index, value in enumerate(properties):
        item = json_object(value, f"metadata.properties[{index}]")
        if item.get("name") == SUBJECT_PROPERTY:
            result.add(json_string(item.get("value"), f"metadata.properties[{index}].value"))
    return result


def check(
    root: Path,
    sbom: Path,
    *,
    expected_subjects: Sequence[str] = (),
    require_subjects: bool = False,
) -> CheckResult:
    result = CheckResult("gate_sbom")
    path = root / sbom
    if not require_file(path, result, "sbom-missing"):
        return result
    try:
        document = load_json(path)
        format_name, components = _components(document)
        actual_subjects = _subjects(document)
    except ValueError as exc:
        result.add("sbom-invalid", str(exc), path)
        return result
    if not components:
        result.add("sbom-empty", "SBOM contains no packages/components", path)
    for index, item in enumerate(components):
        if not (item.get("name") or item.get("PackageName")):
            result.add("sbom-component-invalid", f"component {index} has no name", path)
    expected = set(expected_subjects)
    invalid = sorted(subject for subject in {*actual_subjects, *expected} if not DIGEST.fullmatch(subject))
    if invalid:
        result.add("sbom-subject-invalid", f"invalid subject digest(s): {invalid}", path)
    if require_subjects and not expected:
        result.observed = False
        result.add(
            "sbom-expected-subjects-unobserved",
            "release gate requires expected candidate image digests",
        )
    elif expected and actual_subjects != expected:
        result.add(
            "sbom-subject-drift",
            f"SBOM subjects {sorted(actual_subjects)} do not match candidates {sorted(expected)}",
            path,
        )
    result.details.update(
        format=format_name,
        components=len(components),
        artifact=str(path),
        subject_digests=sorted(actual_subjects),
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail-closed SBOM artifact gate")
    add_common_arguments(parser)
    parser.add_argument("--sbom", type=Path, required=True)
    parser.add_argument("--subject-digest", action="append", default=[])
    parser.add_argument("--require-subjects", action="store_true")
    args = parser.parse_args(argv)
    return render_result(
        check(
            args.root.resolve(),
            args.sbom,
            expected_subjects=args.subject_digest,
            require_subjects=args.require_subjects,
        ),
        args.json,
    )


if __name__ == "__main__":
    main_guard(cli)
