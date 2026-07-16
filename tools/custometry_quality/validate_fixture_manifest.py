from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Sequence

from .core import (
    CheckResult,
    JsonObject,
    add_common_arguments,
    json_integer,
    json_list,
    json_object,
    json_string,
    load_json,
    main_guard,
    render_result,
    require_file,
    sha256_file,
)


def _entries(data: JsonObject) -> list[dict[str, Any]]:
    if data.get("schema_version") != 1:
        raise ValueError("fixture manifest requires schema_version=1")
    values = json_list(data.get("fixtures"), "fixtures")
    if not values:
        raise ValueError("fixtures must be a non-empty list")
    required = ("path", "sha256", "size", "profile", "seed", "data_schema_version")
    entries: list[dict[str, Any]] = []
    for index, value in enumerate(values):
        raw = json_object(value, f"fixtures[{index}]")
        entry: dict[str, Any] = {
            "path": json_string(raw.get("path"), f"fixtures[{index}].path"),
            "sha256": json_string(raw.get("sha256"), f"fixtures[{index}].sha256"),
            "size": json_integer(raw.get("size"), f"fixtures[{index}].size"),
            "profile": json_string(raw.get("profile"), f"fixtures[{index}].profile"),
            "seed": json_integer(raw.get("seed"), f"fixtures[{index}].seed"),
            "data_schema_version": json_string(
                raw.get("data_schema_version"), f"fixtures[{index}].data_schema_version"
            ),
        }
        fixture_path = Path(entry["path"])
        if fixture_path.is_absolute() or ".." in fixture_path.parts:
            raise ValueError(f"fixtures[{index}].path must be safe and repository-relative")
        if not all(character in "0123456789abcdef" for character in entry["sha256"]) or len(
            entry["sha256"]
        ) != 64:
            raise ValueError(f"fixtures[{index}].sha256 is invalid")
        if entry["size"] < 0:
            raise ValueError(f"fixtures[{index}].size is invalid")
        if any(key not in raw for key in required):
            raise ValueError(f"fixtures[{index}] requires {required}")
        entries.append(entry)
    return entries


def _profile(data: JsonObject) -> tuple[str, int, dict[str, int], list[str]]:
    if data.get("schema_version") != "1.0.0":
        raise ValueError("fixture profile manifest requires schema_version=1.0.0")
    profile = json_string(data.get("profile"), "profile")
    seed = json_integer(data.get("seed"), "seed")
    if seed < 0:
        raise ValueError("seed must be non-negative")
    json_string(data.get("timezone"), "timezone")
    currency = json_string(data.get("default_currency"), "default_currency")
    if len(currency) != 3 or currency.upper() != currency:
        raise ValueError("default_currency must be an uppercase ISO-style three-letter code")
    grain = json_object(data.get("grain"), "grain")
    if not grain or not all(isinstance(value, str) and value.strip() for value in grain.values()):
        raise ValueError("grain must map entities to non-empty descriptions")
    primary_keys = json_object(data.get("primary_keys"), "primary_keys")
    if not primary_keys:
        raise ValueError("primary_keys must be a non-empty mapping")
    for entity, value in primary_keys.items():
        columns = json_list(value, f"primary_keys.{entity}")
        if not columns or not all(isinstance(column, str) and column for column in columns):
            raise ValueError(f"primary_keys.{entity} must be a non-empty string list")
    pii_class = json_object(data.get("pii_class"), "pii_class")
    if not all(isinstance(value, str) and value for value in pii_class.values()):
        raise ValueError("pii_class values must be non-empty strings")
    count_values = json_object(data.get("expected_counts"), "expected_counts")
    if not count_values:
        raise ValueError("expected_counts must be a non-empty mapping")
    counts: dict[str, int] = {}
    for entity, value in count_values.items():
        count = json_integer(value, f"expected_counts.{entity}")
        if count < 0:
            raise ValueError(f"expected_counts.{entity} must be non-negative")
        counts[entity] = count
    scenario_values = json_list(data.get("scenarios"), "scenarios")
    if not scenario_values or not all(isinstance(item, str) and item for item in scenario_values):
        raise ValueError("scenarios must be a non-empty string list")
    scenarios = [str(item) for item in scenario_values]
    if len(scenarios) != len(set(scenarios)):
        raise ValueError("scenarios must be unique")
    return profile, seed, counts, scenarios


def check(
    root: Path, manifest: Path = Path("tests/golden/retail-demo-manifest.json")
) -> CheckResult:
    result = CheckResult("validate_fixture_manifest")
    manifest_path = root / manifest
    if not require_file(manifest_path, result):
        return result
    try:
        document = load_json(manifest_path)
    except ValueError as exc:
        result.add("fixture-manifest-invalid", str(exc), manifest_path)
        return result
    if "fixtures" not in document:
        try:
            profile, seed, counts, scenarios = _profile(document)
        except ValueError as exc:
            result.add("fixture-manifest-invalid", str(exc), manifest_path)
            return result
        result.details.update(
            manifest_kind="deterministic-profile",
            profile=profile,
            seed=seed,
            expected_counts=counts,
            scenarios=len(scenarios),
        )
        return result
    try:
        entries = _entries(document)
    except ValueError as exc:
        result.add("fixture-manifest-invalid", str(exc), manifest_path)
        return result
    seen: set[str] = set()
    for entry in entries:
        raw = entry["path"]
        if raw in seen:
            result.add("fixture-duplicate", f"duplicate fixture path {raw}", manifest_path)
            continue
        seen.add(raw)
        path = root / raw
        if not require_file(path, result, "fixture-missing"):
            continue
        actual_size = path.stat().st_size
        actual_hash = sha256_file(path)
        if actual_size != entry["size"]:
            result.add("fixture-size-drift", f"expected {entry['size']}, got {actual_size}", path)
        if actual_hash != entry["sha256"]:
            result.add("fixture-hash-drift", f"expected {entry['sha256']}, got {actual_hash}", path)
    result.details.update(
        manifest_kind="checksummed-files",
        fixtures=len(entries),
        profiles=sorted({entry["profile"] for entry in entries}),
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate deterministic fixture/golden manifest")
    add_common_arguments(parser)
    parser.add_argument(
        "--manifest", type=Path, default=Path("tests/golden/retail-demo-manifest.json")
    )
    args = parser.parse_args(argv)
    return render_result(check(args.root.resolve(), args.manifest), args.json)


if __name__ == "__main__":
    main_guard(cli)
