from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Sequence

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


ROUTE_ROW = re.compile(
    r"^\|\s*(UI-(?!OVR-|SYS-)[A-Z]+-[0-9]{3})\s*\|\s*`(/[^`]*)`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
    re.MULTILINE,
)
STATUSES = {"planned", "foundation", "implemented"}
TITLE_KEY = re.compile(r"^(UI-[A-Z]+-[0-9]{3}|FOUNDATION-[A-Z][A-Z-]*)$")
GLOBAL_PREFIXES = (
    "/admin",
    "/audit",
    "/auth",
    "/bootstrap",
    "/help",
    "/invites",
    "/notifications",
    "/onboarding",
    "/profile",
)


def blueprint_routes(path: Path) -> dict[str, dict[str, str]]:
    routes: dict[str, dict[str, str]] = {}
    for match in ROUTE_ROW.finditer(path.read_text(encoding="utf-8")):
        identifier, route, title, release = (item.strip() for item in match.groups())
        if identifier in routes:
            raise ValueError(f"duplicate route ID in UI blueprint: {identifier}")
        is_global = any(route == prefix or route.startswith(f"{prefix}/") for prefix in GLOBAL_PREFIXES)
        canonical = route if is_global else f"/w/:workspaceKey{route}"
        routes[identifier] = {"path": canonical, "title": title, "release": release}
    if not routes:
        raise ValueError("no route-level UI rows found")
    return routes


def _route_records(data: JsonObject, field: str) -> list[dict[str, str]]:
    values = data.get(field, [])
    routes = json_list(values, field)
    normalized: list[dict[str, str]] = []
    for index, value in enumerate(routes):
        item = json_object(value, f"{field}[{index}]")
        required = ("id", "path", "title_key", "release", "status")
        unexpected = sorted(item.keys() - set(required))
        if unexpected:
            raise ValueError(f"{field}[{index}] has unexpected fields: {unexpected}")
        normalized.append(
            {
                key: json_string(item.get(key), f"{field}[{index}].{key}").strip()
                for key in required
            }
        )
    return normalized


def _registry(data: JsonObject) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    if data.get("schema_version") != "2.0.0":
        raise ValueError("route registry requires schema_version=2.0.0")
    return _route_records(data, "routes"), _route_records(data, "foundation_utility_routes")


def _title_catalog(data: JsonObject, label: str) -> dict[str, str]:
    return {
        key: json_string(value, f"{label}.{key}").strip()
        for key, value in data.items()
    }


def check(
    root: Path,
    ui_blueprint: Path = Path("custometry-ui-blueprint-ru.md"),
    registry: Path = Path("packages/contracts/routes/ui-routes.json"),
    english_titles: Path = Path("packages/localization/locales/en/route-titles.json"),
    russian_titles: Path = Path("packages/localization/locales/ru/route-titles.json"),
) -> CheckResult:
    result = CheckResult("validate_route_registry")
    blueprint_path = root / ui_blueprint
    registry_path = root / registry
    english_path = root / english_titles
    russian_path = root / russian_titles
    required_paths = (blueprint_path, registry_path, english_path, russian_path)
    if not all(require_file(path, result) for path in required_paths):
        return result
    try:
        expected = blueprint_routes(blueprint_path)
        records, utility_records = _registry(json_object(load_json(registry_path), "registry"))
        english = _title_catalog(json_object(load_json(english_path), "english titles"), "en")
        russian = _title_catalog(json_object(load_json(russian_path), "russian titles"), "ru")
    except ValueError as exc:
        result.add("route-contract-invalid", str(exc))
        return result
    actual: dict[str, dict[str, str]] = {}
    paths: dict[str, str] = {}
    all_records = [*records, *utility_records]
    title_keys: dict[str, str] = {}
    all_ids: set[str] = set()
    for record in all_records:
        identifier = record["id"]
        if identifier in all_ids:
            result.add("route-id-duplicate", f"duplicate ID {identifier}", registry_path)
        all_ids.add(identifier)
        title_key = record["title_key"]
        if not TITLE_KEY.fullmatch(title_key):
            result.add(
                "route-title-key-invalid",
                f"{identifier} has invalid locale-neutral title key {title_key!r}",
                registry_path,
            )
        if title_key in title_keys:
            result.add(
                "route-title-key-duplicate",
                f"{title_key} is used by {title_keys[title_key]} and {identifier}",
                registry_path,
            )
        title_keys[title_key] = identifier
        if record["status"] not in STATUSES:
            result.add("route-status-invalid", f"{identifier} has status {record['status']}", registry_path)

    for record in records:
        identifier = record["id"]
        if identifier in actual:
            continue
        if record["path"] in paths:
            result.add(
                "route-path-duplicate",
                f"{record['path']} is used by {paths[record['path']]} and {identifier}",
                registry_path,
            )
        paths[record["path"]] = identifier
        actual[identifier] = record
    for identifier in sorted(expected.keys() - actual.keys()):
        result.add("route-missing", f"UI blueprint route is absent: {identifier}", registry_path)
    for identifier in sorted(actual.keys() - expected.keys()):
        result.add("route-extra", f"registry route is not in UI blueprint: {identifier}", registry_path)
    for identifier in sorted(expected.keys() & actual.keys()):
        for key in ("path", "release"):
            if actual[identifier][key] != expected[identifier][key]:
                result.add(
                    "route-metadata-drift",
                    f"{identifier}.{key}: registry={actual[identifier][key]!r}, blueprint={expected[identifier][key]!r}",
                    registry_path,
                )
        title_key = actual[identifier]["title_key"]
        if english.get(title_key) != expected[identifier]["title"]:
            result.add(
                "route-title-source-drift",
                f"{identifier} resolves to {english.get(title_key)!r}; UI blueprint title is {expected[identifier]['title']!r}",
                english_path,
            )

    used_title_keys = set(title_keys)
    for key in sorted(used_title_keys - english.keys()):
        result.add("english-route-title-missing", f"{key} is required by {title_keys[key]}", english_path)
    for key in sorted(used_title_keys - russian.keys()):
        result.add("russian-route-title-missing", f"{key} is required by {title_keys[key]}", russian_path)
    for key in sorted(english.keys() - used_title_keys):
        result.add("english-route-title-unused", key, english_path)
    for key in sorted(russian.keys() - used_title_keys):
        result.add("russian-route-title-unused", key, russian_path)
    result.details.update(
        routes=len(actual),
        utility_routes=len(utility_records),
        title_keys=len(used_title_keys),
        planned=sum(item["status"] == "planned" for item in actual.values()),
        foundation=sum(item["status"] == "foundation" for item in actual.values()),
        implemented=sum(item["status"] == "implemented" for item in actual.values()),
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate route registry against the UI blueprint")
    add_common_arguments(parser)
    parser.add_argument("--ui-blueprint", type=Path, default=Path("custometry-ui-blueprint-ru.md"))
    parser.add_argument(
        "--registry", type=Path, default=Path("packages/contracts/routes/ui-routes.json")
    )
    parser.add_argument(
        "--english-titles",
        type=Path,
        default=Path("packages/localization/locales/en/route-titles.json"),
    )
    parser.add_argument(
        "--russian-titles",
        type=Path,
        default=Path("packages/localization/locales/ru/route-titles.json"),
    )
    args = parser.parse_args(argv)
    return render_result(
        check(
            args.root.resolve(),
            args.ui_blueprint,
            args.registry,
            args.english_titles,
            args.russian_titles,
        ),
        args.json,
    )


if __name__ == "__main__":
    main_guard(cli)
