from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, Sequence

from .core import (
    CheckResult,
    JsonObject,
    add_common_arguments,
    json_list,
    json_object,
    load_json,
    main_guard,
    render_result,
    require_file,
    string_list,
)


UNKNOWN = {"", "NOASSERTION", "NONE", "UNKNOWN"}
NON_PACKAGE_COMPONENT_TYPES = {"file"}


def _licenses(item: JsonObject) -> Iterable[str]:
    concluded = item.get("licenseConcluded")
    if isinstance(concluded, str):
        yield concluded
        return
    licenses = item.get("licenses")
    if isinstance(licenses, list):
        for index, value in enumerate(licenses):
            entry = json_object(value, f"licenses[{index}]")
            nested = entry.get("license")
            license_value = json_object(nested, f"licenses[{index}].license") if nested is not None else entry
            identifier = license_value.get("id") or license_value.get("name")
            yield identifier if isinstance(identifier, str) else ""


def check(root: Path, sbom: Path, policy: Path) -> CheckResult:
    result = CheckResult("gate_licenses")
    sbom_path, policy_path = root / sbom, root / policy
    if not require_file(sbom_path, result, "sbom-missing") or not require_file(policy_path, result, "license-policy-missing"):
        return result
    try:
        document, config = load_json(sbom_path), load_json(policy_path)
        if config.get("schema_version") != 1:
            raise ValueError("license policy requires schema_version=1")
        allowed = set(string_list(config.get("allowed"), "allowed", non_empty=True))
        denied = set(string_list(config.get("denied"), "denied"))
        review_required = set(
            string_list(config.get("review_required", []), "review_required")
        )
        overlap = (allowed & denied) | (allowed & review_required) | (denied & review_required)
        if overlap:
            raise ValueError(f"license policy categories overlap: {sorted(overlap)}")
        values = (
            json_list(document.get("components"), "components")
            if document.get("bomFormat") == "CycloneDX"
            else json_list(document.get("packages"), "packages")
        )
        if not values:
            raise ValueError("SBOM contains no components/packages")
        components = [json_object(value, f"components[{index}]") for index, value in enumerate(values)]
        evaluated = [
            item
            for item in components
            if item.get("type") not in NON_PACKAGE_COMPONENT_TYPES
        ]
        if not evaluated:
            raise ValueError("SBOM contains no package-level components")
    except ValueError as exc:
        result.add("license-input-invalid", str(exc))
        return result
    observed = 0
    seen: set[tuple[str, str, str]] = set()
    for item in evaluated:
        raw_name = item.get("name") or item.get("PackageName")
        name = raw_name if isinstance(raw_name, str) else "<unnamed>"
        raw_version = item.get("version") or item.get("PackageVersion")
        version = raw_version if isinstance(raw_version, str) else ""
        values = list(_licenses(item))
        if not values:
            finding = (name, version, "<missing>")
            if finding not in seen:
                seen.add(finding)
                result.add("license-unknown", f"{name}: no license declaration", sbom_path)
            continue
        for value in values:
            finding = (name, version, value)
            if finding in seen:
                continue
            seen.add(finding)
            observed += 1
            if value.upper() in UNKNOWN:
                result.add("license-unknown", f"{name}: {value or '<empty>'}", sbom_path)
            elif value in denied:
                result.add("license-denied", f"{name}: {value}", sbom_path)
            elif value in review_required:
                result.add("license-review-required", f"{name}: {value}", sbom_path)
            elif value not in allowed:
                result.add("license-not-allowed", f"{name}: {value}", sbom_path)
    result.details.update(
        components_total=len(components),
        components_evaluated=len(evaluated),
        components_ignored=len(components) - len(evaluated),
        license_declarations=observed,
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate SBOM licenses against explicit policy")
    add_common_arguments(parser)
    parser.add_argument("--sbom", type=Path, required=True)
    parser.add_argument("--policy", type=Path, default=Path("deploy/license-policy.json"))
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve(), args.sbom, args.policy), args.json)


if __name__ == "__main__":
    main_guard(cli)
