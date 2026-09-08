from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, Sequence

from .license_reviews import validate_reviews

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


def _bare_distribution_descriptor(item: JsonObject) -> bool:
    """Only Syft's package-free distro descriptor; explicit declarations always count."""
    if (item.get("type") != "operating-system" or item.get("name") not in {"debian", "alpine"}
            or any(key in item for key in ("purl", "licenses", "licenseConcluded", "hashes"))):
        return False
    name, version = item.get("name"), item.get("version")
    if not isinstance(version, str) or item.get("bom-ref") != f"os:{name}@{version}":
        return False
    properties = item.get("properties")
    if not isinstance(properties, list):
        return False
    pairs = [json_object(value, "distribution.properties") for value in properties]
    return (
        {"name": "syft:distro:id", "value": name} in pairs
        and {"name": "syft:distro:versionID", "value": version} in pairs
        and all(str(value.get("name", "")).startswith("syft:distro:") for value in pairs)
    )


def _licenses(item: JsonObject) -> Iterable[str]:
    concluded = item.get("licenseConcluded")
    if isinstance(concluded, str):
        yield concluded
        return
    licenses = item.get("licenses")
    if isinstance(licenses, list):
        for index, value in enumerate(licenses):
            entry = json_object(value, f"licenses[{index}]")
            expression = entry.get("expression")
            if isinstance(expression, str):
                yield expression
                continue
            nested = entry.get("license")
            license_value = json_object(nested, f"licenses[{index}].license") if nested is not None else entry
            identifier = license_value.get("id") or license_value.get("name")
            yield identifier if isinstance(identifier, str) else ""


def _alternatives(value: str) -> list[frozenset[str]]:
    """Bounded SPDX AND/OR/WITH evaluation; unknown atoms still fail policy."""
    tokens = re.findall(r"[()]|[^\s()]+", value)
    if not tokens or len(tokens) > 128:
        raise ValueError("empty or oversized license expression")
    index = 0

    def atom() -> list[frozenset[str]]:
        nonlocal index
        if index >= len(tokens):
            raise ValueError("missing license operand")
        token = tokens[index]
        index += 1
        if token == "(":
            options = expression()
            if index >= len(tokens) or tokens[index] != ")":
                raise ValueError("unclosed license expression")
            index += 1
            return options
        if token in {"AND", "OR", "WITH", ")"}:
            raise ValueError("invalid license operand")
        if index < len(tokens) and tokens[index] == "WITH":
            index += 1
            if index >= len(tokens) or tokens[index] in {"AND", "OR", "WITH", "(", ")"}:
                raise ValueError("missing license exception")
            token += " WITH " + tokens[index]
            index += 1
        return [frozenset({token})]

    def conjunction() -> list[frozenset[str]]:
        nonlocal index
        options = atom()
        while index < len(tokens) and tokens[index] == "AND":
            index += 1
            right = atom()
            if len(options) * len(right) > 64:
                raise ValueError("too many license alternatives")
            options = [left | other for left in options for other in right]
        return options

    def expression() -> list[frozenset[str]]:
        nonlocal index
        options = conjunction()
        while index < len(tokens) and tokens[index] == "OR":
            index += 1
            options += conjunction()
            if len(options) > 64:
                raise ValueError("too many license alternatives")
        return options

    options = expression()
    if index != len(tokens):
        raise ValueError("unexpected license expression token")
    return options


def check(
    root: Path, sbom: Path, policy: Path, *,
    reviews: Path | None = None, expected_subjects: Sequence[str] = (),
) -> CheckResult:
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
            if item.get("type") not in NON_PACKAGE_COMPONENT_TYPES and not _bare_distribution_descriptor(item)
        ]
        if not evaluated:
            raise ValueError("SBOM contains no package-level components")
        reviewed = validate_reviews(
            root / reviews, sbom_path, policy_path, set(expected_subjects), evaluated
        ) if reviews is not None else {}
    except (ValueError, OSError, KeyError, TypeError) as exc:
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
            try:
                options = _alternatives(value) if value else [frozenset({""})]
            except ValueError:
                # Preserve uninterpretable names instead of guessing an SPDX license.
                options = [frozenset({value})]
            if any(option <= allowed for option in options):
                continue
            for identifier in sorted({identifier for option in options for identifier in option} - allowed):
                obligations = reviewed.get((name, version, str(item.get("purl", ""))))
                base_license = identifier.split(" WITH ", 1)[0]
                reviewable = (
                    re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.+-]*(?: WITH [A-Za-z0-9.-]+)?", identifier) is not None
                    and identifier.upper() not in UNKNOWN
                    and not base_license.upper().startswith(("AGPL", "SSPL", "BUSL", "LICENSEREF"))
                    and base_license not in denied
                )
                if obligations is not None and reviewable:
                    required = {"notice"}
                    if "GPL" in base_license:
                        required.add("corresponding-source")
                    if "LGPL" in base_license:
                        required.add("relinking")
                    if required <= obligations:
                        continue
                if identifier.upper() in UNKNOWN:
                    code = "license-unknown"
                elif identifier in denied:
                    code = "license-denied"
                elif identifier in review_required:
                    code = "license-review-required"
                else:
                    code = "license-not-allowed"
                result.add(code, f"{name}: {identifier or '<empty>'} (declared: {value})", sbom_path)
    result.details.update(
        components_total=len(components),
        components_evaluated=len(evaluated),
        components_ignored=len(components) - len(evaluated),
        license_declarations=observed,
        components_with_bound_review=len(reviewed),
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate SBOM licenses against explicit policy")
    add_common_arguments(parser)
    parser.add_argument("--sbom", type=Path, required=True)
    parser.add_argument("--policy", type=Path, default=Path("deploy/license-policy.json"))
    parser.add_argument("--reviews", type=Path)
    parser.add_argument("--subject", action="append", default=[])
    args = parser.parse_args(argv)
    return render_result(check(
        args.root.resolve(), args.sbom, args.policy,
        reviews=args.reviews, expected_subjects=args.subject,
    ), args.json)


if __name__ == "__main__":
    main_guard(cli)
