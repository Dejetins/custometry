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
    parse_frontmatter,
    render_result,
    require_file,
    stable_ids,
)


STATUSES = {"planned", "foundation", "implemented"}
ROLE_HINTS = {"IA", "WA", "DS", "AN", "ML", "OP", "VW", "all", "invited", "allowed", "owners"}
FAMILIES = {"public_auth", "global_user", "installation", "workspace"}
SHELL_BY_FAMILY = {
    "public_auth": "auth",
    "global_user": "global",
    "installation": "installation",
    "workspace": "workspace",
}
AUTHORIZATION_MODES = {
    "public",
    "authenticated",
    "global_permission",
    "workspace_membership",
    "workspace_permission",
    "workspace_object_access",
    "workspace_permission_or_object_access",
}
OBJECT_AUTHORIZATION_MODES = {
    "workspace_object_access",
    "workspace_permission_or_object_access",
}
PERMISSION_PATTERN = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$")
TITLE_KEY = re.compile(r"^(UI-[A-Z]+-[0-9]{3}|FOUNDATION-[A-Z][A-Z-]*)$")
ROUTE_ID = re.compile(r"^UI-(?!OVR-|SYS-)[A-Z]+-[0-9]{3}$")
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
CANONICAL_PENPOT_FILE_ID = "7cd71457-8d32-8044-8008-549f83bb4645"
OVERLAY_ID = re.compile(r"^UI-OVR-[0-9]{3}$")
SYSTEM_SURFACE_ID = re.compile(r"^UI-SYS-[0-9]{3}$")
CROSS_SURFACE_CAPABILITY_ID = re.compile(r"^UI-CAP-[0-9]{3}$")
USE_CASE_ID = re.compile(r"^UC-[0-9]{3}$")
REQUIREMENT_RANGE = re.compile(r"^([A-Z][A-Z0-9-]*-)([0-9]{3})…([0-9]{3})$")
CONTRACT_ROOT_KEYS = {
    "schema_version",
    "product_spec_version",
    "ui_spec_version",
    "identity_registry_schema_version",
    "source_files",
    "role_catalog",
    "permission_catalog",
    "profiles",
    "routes",
}
ROUTE_CONTRACT_KEYS = {
    "id",
    "path",
    "title_key",
    "family",
    "shell_profile",
    "navigation_group",
    "surface_kind",
    "release",
    "status",
    "role_hints",
    "authorization",
    "guard_profile",
    "state_profile",
    "navigation_profile",
    "query_profile",
    "focus_explore",
    "source",
    "design",
}
AUTHORIZATION_KEYS = {"mode", "entry_permissions_any", "action_permissions", "object_scoped"}
SOURCE_KEYS = {"ui_blueprint_id", "requirement_ids"}
DESIGN_KEYS = {"penpot_status", "frame_key", "baseline_version"}
PROFILE_CATEGORIES = {"guards", "states", "navigation", "queries"}
SURFACE_KINDS = {
    "overview",
    "list",
    "detail",
    "editor",
    "wizard",
    "workspace",
    "operator",
    "reader",
    "settings",
}
FOCUS_MODES = {"not_applicable", "reportable_blocks", "primary_surface"}
STATE_VALUES = {
    "first_loading",
    "ready",
    "refreshing",
    "empty",
    "partial",
    "forbidden",
    "failed",
    "stale",
    "dependency_unavailable",
    "validation_error",
    "conflict",
    "saving",
    "preflight",
    "queued",
    "running",
    "cancelling",
    "succeeded",
    "blocked",
    "maintenance",
    "upgrade_required",
    "session_expired",
}
QUERY_KEYS = {"view", "tab", "focus", "sort", "page", "saved_view", "step"}
GUARD_PROFILE_KEYS = {
    "authenticated",
    "workspace_resolution",
    "membership",
    "permission",
    "object_access",
    "deny_before_fetch",
}
STATE_PROFILE_KEYS = {"required_states", "preserve_previous_data_on_refresh"}
NAVIGATION_PROFILE_KEYS = {
    "history_entry",
    "shell_persistent",
    "restore_focus",
    "restore_scroll",
    "dirty_guard",
}
QUERY_PROFILE_KEYS = {"allowed_keys", "sensitive_values_forbidden", "complex_state"}
SURFACE_CONTRACT_ROOT_KEYS = {
    "schema_version",
    "product_spec_version",
    "ui_spec_version",
    "route_contract_schema_version",
    "source_files",
    "route_decision_policy",
    "penpot_baseline",
    "overlays",
    "system_surfaces",
    "cross_surface_capabilities",
    "use_case_bindings",
}
OVERLAY_KEYS = {"id", "name", "kind", "route_backed", "history_semantics", "requirement_ids"}
SYSTEM_SURFACE_KEYS = {"id", "name", "requirement_ids"}
CAPABILITY_KEYS = {"id", "name", "delivery_form", "requirement_ids"}
USE_CASE_BINDING_KEYS = {"use_case_id", "surface_ids", "coverage_types", "rationale"}


def _canonical_path(route: str) -> str:
    is_global = any(route == prefix or route.startswith(f"{prefix}/") for prefix in GLOBAL_PREFIXES)
    return route if is_global else f"/w/:workspaceKey{route}"


def _family_for_path(path: str) -> str:
    if path.startswith("/w/:workspaceKey"):
        return "workspace"
    if path == "/audit" or path.startswith("/admin"):
        return "installation"
    if path.startswith("/auth/") or path == "/bootstrap" or path.startswith("/invites/"):
        return "public_auth"
    return "global_user"


def blueprint_routes(path: Path) -> dict[str, dict[str, object]]:
    routes: dict[str, dict[str, object]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 5 or ROUTE_ID.fullmatch(cells[0]) is None:
            continue
        identifier, route_cell, title, release, roles_cell = cells[:5]
        if not (route_cell.startswith("`") and route_cell.endswith("`")):
            raise ValueError(f"{identifier} route must be wrapped in backticks")
        if identifier in routes:
            raise ValueError(f"duplicate route ID in UI blueprint: {identifier}")
        role_hints = tuple(item.strip() for item in roles_cell.split(",") if item.strip())
        if not role_hints:
            raise ValueError(f"{identifier} has no role hints")
        route = route_cell[1:-1]
        routes[identifier] = {
            "path": _canonical_path(route),
            "title": title,
            "release": release,
            "role_hints": role_hints,
        }
    if not routes:
        raise ValueError("no route-level UI rows found")
    return routes


def _expand_requirement_refs(value: str) -> tuple[str, ...]:
    requirement_ids: list[str] = []
    for raw_item in value.replace("`", "").split(","):
        item = raw_item.strip()
        if not item:
            continue
        match = REQUIREMENT_RANGE.fullmatch(item)
        if match is None:
            requirement_ids.append(item)
            continue
        prefix, start_text, end_text = match.groups()
        start = int(start_text)
        end = int(end_text)
        if end < start:
            raise ValueError(f"descending requirement range in UI blueprint: {item}")
        requirement_ids.extend(f"{prefix}{index:03d}" for index in range(start, end + 1))
    if not requirement_ids:
        raise ValueError("empty requirement reference cell in UI blueprint")
    if len(requirement_ids) != len(set(requirement_ids)):
        raise ValueError(f"duplicate requirement IDs in UI blueprint cell: {value}")
    return tuple(requirement_ids)


def blueprint_requirement_surfaces(
    path: Path, identifier_pattern: re.Pattern[str]
) -> dict[str, dict[str, object]]:
    surfaces: dict[str, dict[str, object]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4 or identifier_pattern.fullmatch(cells[0]) is None:
            continue
        identifier, name, _, requirement_cell = cells[:4]
        if identifier in surfaces:
            raise ValueError(f"duplicate UI surface ID in UI blueprint: {identifier}")
        if not name:
            raise ValueError(f"{identifier} has no surface name")
        surfaces[identifier] = {
            "name": name,
            "requirement_ids": _expand_requirement_refs(requirement_cell),
        }
    return surfaces


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
            {key: json_string(item.get(key), f"{field}[{index}].{key}").strip() for key in required}
        )
    return normalized


def _registry(data: JsonObject) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    if data.get("schema_version") != "2.0.0":
        raise ValueError("route registry requires schema_version=2.0.0")
    return _route_records(data, "routes"), _route_records(data, "foundation_utility_routes")


def _title_catalog(data: JsonObject, label: str) -> dict[str, str]:
    return {key: json_string(value, f"{label}.{key}").strip() for key, value in data.items()}


def _string_list(value: object, label: str, *, non_empty: bool = False) -> tuple[str, ...]:
    items = json_list(value, label)
    normalized = tuple(
        json_string(item, f"{label}[{index}]").strip() for index, item in enumerate(items)
    )
    if non_empty and not normalized:
        raise ValueError(f"{label} must not be empty")
    if any(not item for item in normalized):
        raise ValueError(f"{label} contains an empty string")
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{label} contains duplicates")
    return normalized


def _permission_catalog(product_text: str) -> tuple[str, ...]:
    match = re.search(
        r"^permissions:\n(?P<body>(?:  - [a-z0-9_.]+\n)+)", product_text, re.MULTILINE
    )
    if match is None:
        raise ValueError("normative product permission catalog is missing")
    permissions = tuple(line.strip()[2:] for line in match.group("body").splitlines())
    if len(permissions) != len(set(permissions)):
        raise ValueError("normative product permission catalog contains duplicates")
    return permissions


def _add(result: CheckResult, code: str, message: str, path: Path) -> None:
    result.add(code, message, path)


def _check_exact_keys(
    value: JsonObject,
    expected: set[str],
    *,
    label: str,
    path: Path,
    result: CheckResult,
) -> bool:
    missing = sorted(expected - value.keys())
    unexpected = sorted(value.keys() - expected)
    if missing or unexpected:
        _add(
            result,
            "route-contract-shape-invalid",
            f"{label} keys drift: missing={missing}, unexpected={unexpected}",
            path,
        )
        return False
    return True


def _check_schema(schema: JsonObject, path: Path, result: CheckResult) -> None:
    try:
        properties = json_object(schema.get("properties"), "schema.properties")
        schema_version = json_object(
            properties.get("schema_version"), "schema.properties.schema_version"
        )
        definitions = json_object(schema.get("$defs"), "schema.$defs")
        route_definition = json_object(
            definitions.get("routeContract"), "schema.$defs.routeContract"
        )
        required = set(
            _string_list(route_definition.get("required"), "schema route required", non_empty=True)
        )
    except ValueError as exc:
        _add(result, "route-contract-schema-invalid", str(exc), path)
        return
    if (
        schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
        or schema_version.get("const") != "1.0.0"
        or schema.get("additionalProperties") is not False
        or route_definition.get("additionalProperties") is not False
        or required != ROUTE_CONTRACT_KEYS
    ):
        _add(
            result,
            "route-contract-schema-invalid",
            "schema must be draft 2020-12, closed, version 1.0.0, and require the canonical route fields",
            path,
        )


def _check_profiles(data: JsonObject, path: Path, result: CheckResult) -> dict[str, set[str]]:
    try:
        profiles = json_object(data.get("profiles"), "profiles")
    except ValueError as exc:
        _add(result, "route-contract-profiles-invalid", str(exc), path)
        return {key: set() for key in PROFILE_CATEGORIES}
    if set(profiles) != PROFILE_CATEGORIES:
        _add(
            result,
            "route-contract-profiles-invalid",
            f"profile categories must be {sorted(PROFILE_CATEGORIES)}",
            path,
        )
    names: dict[str, set[str]] = {}
    for category in PROFILE_CATEGORIES:
        try:
            values = json_object(profiles.get(category), f"profiles.{category}")
        except ValueError as exc:
            _add(result, "route-contract-profiles-invalid", str(exc), path)
            names[category] = set()
            continue
        if not values:
            _add(result, "route-contract-profiles-invalid", f"profiles.{category} is empty", path)
        names[category] = set(values)
        for name, raw_profile in values.items():
            try:
                profile = json_object(raw_profile, f"profiles.{category}.{name}")
            except ValueError as exc:
                _add(result, "route-contract-profiles-invalid", str(exc), path)
                continue
            if category == "guards":
                if not _check_exact_keys(
                    profile,
                    GUARD_PROFILE_KEYS,
                    label=f"guard profile {name}",
                    path=path,
                    result=result,
                ):
                    continue
                if not all(isinstance(profile[key], bool) for key in GUARD_PROFILE_KEYS):
                    _add(
                        result,
                        "route-contract-profiles-invalid",
                        f"guard profile {name} values must be booleans",
                        path,
                    )
            elif category == "states":
                if not _check_exact_keys(
                    profile,
                    STATE_PROFILE_KEYS,
                    label=f"state profile {name}",
                    path=path,
                    result=result,
                ):
                    continue
                try:
                    states = set(
                        _string_list(
                            profile.get("required_states"),
                            f"state profile {name}.required_states",
                            non_empty=True,
                        )
                    )
                except ValueError as exc:
                    _add(result, "route-contract-profiles-invalid", str(exc), path)
                    states = set()
                if not states <= STATE_VALUES or not isinstance(
                    profile.get("preserve_previous_data_on_refresh"), bool
                ):
                    _add(
                        result,
                        "route-contract-profiles-invalid",
                        f"state profile {name} contains invalid values",
                        path,
                    )
            elif category == "navigation":
                if not _check_exact_keys(
                    profile,
                    NAVIGATION_PROFILE_KEYS,
                    label=f"navigation profile {name}",
                    path=path,
                    result=result,
                ):
                    continue
                bool_keys = NAVIGATION_PROFILE_KEYS - {"history_entry"}
                if profile.get("history_entry") not in {
                    "push",
                    "replace_for_presentation_only",
                } or not all(isinstance(profile[key], bool) for key in bool_keys):
                    _add(
                        result,
                        "route-contract-profiles-invalid",
                        f"navigation profile {name} contains invalid values",
                        path,
                    )
            else:
                if not _check_exact_keys(
                    profile,
                    QUERY_PROFILE_KEYS,
                    label=f"query profile {name}",
                    path=path,
                    result=result,
                ):
                    continue
                try:
                    allowed_keys = set(
                        _string_list(
                            profile.get("allowed_keys"), f"query profile {name}.allowed_keys"
                        )
                    )
                except ValueError as exc:
                    _add(result, "route-contract-profiles-invalid", str(exc), path)
                    allowed_keys = set()
                if (
                    not allowed_keys <= QUERY_KEYS
                    or profile.get("sensitive_values_forbidden") is not True
                    or profile.get("complex_state")
                    not in {"forbidden", "saved_view_or_opaque_reference"}
                ):
                    _add(
                        result,
                        "route-contract-profiles-invalid",
                        f"query profile {name} contains invalid values",
                        path,
                    )
    return names


def _check_executable_contract(
    data: JsonObject,
    *,
    path: Path,
    expected: dict[str, dict[str, object]],
    actual: dict[str, dict[str, str]],
    product_spec_version: str,
    ui_spec_version: str,
    product_permissions: tuple[str, ...],
    product_requirement_ids: set[str],
    result: CheckResult,
) -> None:
    if not _check_exact_keys(
        data, CONTRACT_ROOT_KEYS, label="contract root", path=path, result=result
    ):
        return
    if (
        data.get("schema_version") != "1.0.0"
        or data.get("identity_registry_schema_version") != "2.0.0"
    ):
        _add(
            result,
            "route-contract-version-invalid",
            "route contract must be 1.0.0 over identity registry 2.0.0",
            path,
        )
    if (
        data.get("product_spec_version") != product_spec_version
        or data.get("ui_spec_version") != ui_spec_version
    ):
        _add(
            result,
            "route-contract-version-drift",
            f"contract product/UI versions must be {product_spec_version}/{ui_spec_version}",
            path,
        )
    try:
        role_catalog = set(_string_list(data.get("role_catalog"), "role_catalog", non_empty=True))
        permission_catalog = _string_list(
            data.get("permission_catalog"), "permission_catalog", non_empty=True
        )
        source_files = _string_list(data.get("source_files"), "source_files", non_empty=True)
        contract_values = json_list(data.get("routes"), "routes")
    except ValueError as exc:
        _add(result, "route-contract-root-invalid", str(exc), path)
        return
    if role_catalog != ROLE_HINTS:
        _add(
            result,
            "route-contract-role-catalog-drift",
            f"role catalog must be {sorted(ROLE_HINTS)}",
            path,
        )
    if permission_catalog != product_permissions:
        _add(
            result,
            "route-contract-permission-catalog-drift",
            "permission catalog differs from the normative product blueprint",
            path,
        )
    required_sources = {
        "custometry-technical-blueprint-ru.md",
        "custometry-ui-blueprint-ru.md",
        "packages/contracts/routes/ui-routes.json",
    }
    if not required_sources <= set(source_files):
        _add(
            result,
            "route-contract-source-list-invalid",
            f"source_files must include {sorted(required_sources)}",
            path,
        )

    profiles = _check_profiles(data, path, result)
    contracts: dict[str, JsonObject] = {}
    penpot_backlog: set[str] = set()
    for index, value in enumerate(contract_values):
        label = f"routes[{index}]"
        try:
            item = json_object(value, label)
        except ValueError as exc:
            _add(result, "route-contract-record-invalid", str(exc), path)
            continue
        if not _check_exact_keys(item, ROUTE_CONTRACT_KEYS, label=label, path=path, result=result):
            continue
        try:
            identifier = json_string(item.get("id"), f"{label}.id")
        except ValueError as exc:
            _add(result, "route-contract-record-invalid", str(exc), path)
            continue
        if identifier in contracts:
            _add(result, "route-contract-id-duplicate", identifier, path)
            continue
        contracts[identifier] = item
        identity = actual.get(identifier)
        source_row = expected.get(identifier)
        if identity is None or source_row is None:
            _add(result, "route-contract-route-extra", identifier, path)
            continue
        for field in ("path", "title_key", "release", "status"):
            if item.get(field) != identity[field]:
                _add(
                    result,
                    "route-contract-identity-drift",
                    f"{identifier}.{field}: contract={item.get(field)!r}, registry={identity[field]!r}",
                    path,
                )
        family = item.get("family")
        canonical_family = _family_for_path(identity["path"])
        if family not in FAMILIES or family != canonical_family:
            _add(
                result,
                "route-contract-family-drift",
                f"{identifier} must use family {canonical_family}",
                path,
            )
        if item.get("shell_profile") != SHELL_BY_FAMILY.get(canonical_family):
            _add(
                result,
                "route-contract-shell-drift",
                f"{identifier} shell does not match {canonical_family}",
                path,
            )
        if item.get("surface_kind") not in SURFACE_KINDS:
            _add(
                result,
                "route-contract-surface-invalid",
                f"{identifier} has invalid surface kind {item.get('surface_kind')!r}",
                path,
            )
        navigation_group = item.get("navigation_group")
        if (
            not isinstance(navigation_group, str)
            or re.fullmatch(r"[a-z][a-z0-9_]*", navigation_group) is None
        ):
            _add(
                result,
                "route-contract-navigation-group-invalid",
                f"{identifier} has invalid navigation group",
                path,
            )
        if item.get("focus_explore") not in FOCUS_MODES:
            _add(
                result, "route-contract-focus-invalid", f"{identifier} has invalid Focus mode", path
            )
        try:
            role_hints = _string_list(item.get("role_hints"), f"{label}.role_hints", non_empty=True)
        except ValueError as exc:
            _add(result, "route-contract-role-hints-invalid", str(exc), path)
            role_hints = ()
        if role_hints != source_row["role_hints"]:
            _add(
                result,
                "route-contract-role-hints-drift",
                f"{identifier} roles={role_hints!r}; UI blueprint={source_row['role_hints']!r}",
                path,
            )
        if not set(role_hints) <= ROLE_HINTS:
            _add(
                result,
                "route-contract-role-hints-invalid",
                f"{identifier} contains unknown role hints",
                path,
            )

        try:
            authorization = json_object(item.get("authorization"), f"{label}.authorization")
            source = json_object(item.get("source"), f"{label}.source")
            design = json_object(item.get("design"), f"{label}.design")
        except ValueError as exc:
            _add(result, "route-contract-record-invalid", str(exc), path)
            continue
        _check_exact_keys(
            authorization,
            AUTHORIZATION_KEYS,
            label=f"{label}.authorization",
            path=path,
            result=result,
        )
        _check_exact_keys(source, SOURCE_KEYS, label=f"{label}.source", path=path, result=result)
        _check_exact_keys(design, DESIGN_KEYS, label=f"{label}.design", path=path, result=result)
        mode = authorization.get("mode")
        if mode not in AUTHORIZATION_MODES:
            _add(
                result,
                "route-contract-authorization-invalid",
                f"{identifier} has unknown mode {mode!r}",
                path,
            )
        expected_mode_family = {
            "public": "public_auth",
            "authenticated": "global_user",
            "global_permission": "installation",
        }.get(str(mode))
        if expected_mode_family and family != expected_mode_family:
            _add(
                result,
                "route-contract-authorization-invalid",
                f"{identifier} mode {mode} conflicts with family {family}",
                path,
            )
        if isinstance(mode, str) and mode.startswith("workspace_") and family != "workspace":
            _add(
                result,
                "route-contract-authorization-invalid",
                f"{identifier} workspace mode requires workspace family",
                path,
            )
        expected_guard = {
            "public": "public",
            "authenticated": "authenticated_global",
            "global_permission": "global_permission",
            "workspace_membership": "workspace_member",
            "workspace_permission": "workspace_permission",
            "workspace_object_access": "workspace_object",
            "workspace_permission_or_object_access": "workspace_object",
        }.get(str(mode))
        if expected_guard and item.get("guard_profile") != expected_guard:
            _add(
                result,
                "route-contract-guard-drift",
                f"{identifier} mode {mode} requires guard {expected_guard}",
                path,
            )
        try:
            entry_permissions = _string_list(
                authorization.get("entry_permissions_any"), f"{label}.entry_permissions_any"
            )
            action_permissions = _string_list(
                authorization.get("action_permissions"), f"{label}.action_permissions"
            )
        except ValueError as exc:
            _add(result, "route-contract-permission-invalid", str(exc), path)
            entry_permissions = action_permissions = ()
        unknown_permissions = sorted(
            (set(entry_permissions) | set(action_permissions)) - set(product_permissions)
        )
        if unknown_permissions or any(
            PERMISSION_PATTERN.fullmatch(item) is None
            for item in (*entry_permissions, *action_permissions)
        ):
            _add(
                result,
                "route-contract-permission-invalid",
                f"{identifier} unknown/invalid permissions: {unknown_permissions}",
                path,
            )
        if (
            mode
            in {
                "global_permission",
                "workspace_permission",
                "workspace_object_access",
                "workspace_permission_or_object_access",
            }
            and not entry_permissions
        ):
            _add(
                result,
                "route-contract-permission-invalid",
                f"{identifier} mode {mode} requires entry permissions",
                path,
            )
        object_scoped = authorization.get("object_scoped")
        if not isinstance(object_scoped, bool) or object_scoped != (
            mode in OBJECT_AUTHORIZATION_MODES
        ):
            _add(
                result,
                "route-contract-object-scope-drift",
                f"{identifier} object_scoped conflicts with authorization mode",
                path,
            )

        profile_refs = {
            "guard_profile": "guards",
            "state_profile": "states",
            "navigation_profile": "navigation",
            "query_profile": "queries",
        }
        for field, category in profile_refs.items():
            value_ref = item.get(field)
            if not isinstance(value_ref, str) or value_ref not in profiles[category]:
                _add(
                    result,
                    "route-contract-profile-reference-invalid",
                    f"{identifier}.{field}={value_ref!r}",
                    path,
                )
        if source.get("ui_blueprint_id") != identifier:
            _add(result, "route-contract-source-drift", f"{identifier} source UI ID differs", path)
        try:
            requirement_ids = _string_list(
                source.get("requirement_ids"), f"{label}.requirement_ids", non_empty=True
            )
        except ValueError as exc:
            _add(result, "route-contract-requirements-invalid", str(exc), path)
            requirement_ids = ()
        unknown_requirements = sorted(set(requirement_ids) - product_requirement_ids)
        if unknown_requirements:
            _add(
                result,
                "route-contract-requirements-invalid",
                f"{identifier} unknown IDs: {unknown_requirements}",
                path,
            )
        if (
            design.get("frame_key") != identifier
            or not isinstance(design.get("baseline_version"), str)
            or not design.get("baseline_version")
        ):
            _add(
                result,
                "route-contract-design-invalid",
                f"{identifier} design identity/version is invalid",
                path,
            )
        penpot_status = design.get("penpot_status")
        if penpot_status == "backlog":
            penpot_backlog.add(identifier)
        elif penpot_status != "baseline_verified":
            _add(
                result,
                "route-contract-design-invalid",
                f"{identifier} has invalid Penpot status {penpot_status!r}",
                path,
            )

    for identifier in sorted(expected.keys() - contracts.keys()):
        _add(result, "route-contract-route-missing", identifier, path)
    result.details.update(
        route_contract_schema="1.0.0",
        route_contracts=len(contracts),
        route_contract_profiles=sum(len(values) for values in profiles.values()),
        penpot_baseline=len(contracts) - len(penpot_backlog),
        penpot_backlog=len(penpot_backlog),
    )


def _check_surface_schema(schema: JsonObject, path: Path, result: CheckResult) -> None:
    try:
        properties = json_object(schema.get("properties"), "surface schema.properties")
        schema_version = json_object(
            properties.get("schema_version"), "surface schema.properties.schema_version"
        )
    except ValueError as exc:
        _add(result, "ui-surface-schema-invalid", str(exc), path)
        return
    if (
        schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema"
        or schema_version.get("const") != "1.0.0"
        or schema.get("additionalProperties") is not False
    ):
        _add(
            result,
            "ui-surface-schema-invalid",
            "surface schema must be closed draft 2020-12 version 1.0.0",
            path,
        )


def _check_surface_contract(
    data: JsonObject,
    *,
    schema: JsonObject,
    path: Path,
    schema_path: Path,
    route_contract: JsonObject,
    route_ids: set[str],
    blueprint_overlays: dict[str, dict[str, object]],
    blueprint_system_surfaces: dict[str, dict[str, object]],
    blueprint_capabilities: dict[str, dict[str, object]],
    product_spec_version: str,
    ui_spec_version: str,
    product_requirement_ids: set[str],
    result: CheckResult,
) -> None:
    _check_surface_schema(schema, schema_path, result)
    if not _check_exact_keys(
        data,
        SURFACE_CONTRACT_ROOT_KEYS,
        label="UI surface contract root",
        path=path,
        result=result,
    ):
        return
    if (
        data.get("schema_version") != "1.0.0"
        or data.get("route_contract_schema_version") != "1.0.0"
        or data.get("product_spec_version") != product_spec_version
        or data.get("ui_spec_version") != ui_spec_version
    ):
        _add(
            result,
            "ui-surface-version-drift",
            "surface contract versions must match product, UI, and route contracts",
            path,
        )
    try:
        source_files = set(_string_list(data.get("source_files"), "surface source_files", non_empty=True))
        decision_policy = json_object(data.get("route_decision_policy"), "route_decision_policy")
        penpot = json_object(data.get("penpot_baseline"), "penpot_baseline")
    except ValueError as exc:
        _add(result, "ui-surface-root-invalid", str(exc), path)
        return
    required_sources = {
        "custometry-technical-blueprint-ru.md",
        "custometry-technical-blueprint-human-ru.md",
        "custometry-ui-blueprint-ru.md",
        "packages/contracts/routes/ui-routes.json",
        "packages/contracts/routes/ui-route-contracts.json",
    }
    if not required_sources <= source_files:
        _add(
            result,
            "ui-surface-source-list-invalid",
            f"surface source_files must include {sorted(required_sources)}",
            path,
        )
    if decision_policy.get("route_count_is_ceiling") is not False:
        _add(
            result,
            "ui-surface-route-ceiling-invalid",
            "route_count_is_ceiling must remain false",
            path,
        )

    try:
        route_values = json_list(route_contract.get("routes"), "route contract routes")
        penpot_statuses = [
            json_object(json_object(item, "route").get("design"), "route.design").get(
                "penpot_status"
            )
            for item in route_values
        ]
    except ValueError as exc:
        _add(result, "ui-surface-penpot-invalid", str(exc), path)
        penpot_statuses = []
    verified_count = sum(status == "baseline_verified" for status in penpot_statuses)
    backlog_count = sum(status == "backlog" for status in penpot_statuses)
    if (
        penpot.get("file_id") != CANONICAL_PENPOT_FILE_ID
        or penpot.get("verified_route_count") != verified_count
        or penpot.get("target_route_count") != len(route_ids)
        or verified_count + backlog_count != len(route_ids)
    ):
        _add(
            result,
            "ui-surface-penpot-invalid",
            "Penpot identity and verified/backlog/target route counts must match route contracts",
            path,
        )

    catalog_specs = (
        ("overlays", OVERLAY_KEYS, OVERLAY_ID, blueprint_overlays),
        ("system_surfaces", SYSTEM_SURFACE_KEYS, SYSTEM_SURFACE_ID, blueprint_system_surfaces),
        (
            "cross_surface_capabilities",
            CAPABILITY_KEYS,
            CROSS_SURFACE_CAPABILITY_ID,
            blueprint_capabilities,
        ),
    )
    surface_ids = set(route_ids)
    for field, keys, identifier_pattern, expected_catalog in catalog_specs:
        expected_ids = set(expected_catalog)
        try:
            values = json_list(data.get(field), field)
        except ValueError as exc:
            _add(result, "ui-surface-catalog-invalid", str(exc), path)
            continue
        actual_ids: set[str] = set()
        for index, raw_item in enumerate(values):
            label = f"{field}[{index}]"
            try:
                item = json_object(raw_item, label)
                identifier = json_string(item.get("id"), f"{label}.id")
                requirement_ids = _string_list(
                    item.get("requirement_ids"), f"{label}.requirement_ids", non_empty=True
                )
            except ValueError as exc:
                _add(result, "ui-surface-catalog-invalid", str(exc), path)
                continue
            _check_exact_keys(item, keys, label=label, path=path, result=result)
            if identifier_pattern.fullmatch(identifier) is None or identifier in actual_ids:
                _add(
                    result,
                    "ui-surface-id-invalid",
                    f"invalid or duplicate surface ID {identifier}",
                    path,
                )
            actual_ids.add(identifier)
            unknown = sorted(set(requirement_ids) - product_requirement_ids)
            if unknown:
                _add(
                    result,
                    "ui-surface-requirements-invalid",
                    f"{identifier} unknown requirement IDs: {unknown}",
                    path,
                )
            if identifier in expected_catalog:
                blueprint_surface = expected_catalog[identifier]
                if item.get("name") != blueprint_surface["name"]:
                    _add(
                        result,
                        "ui-surface-blueprint-name-drift",
                        f"{identifier} name differs from the UI blueprint",
                        path,
                    )
                expected_requirements = set(blueprint_surface["requirement_ids"])
                if set(requirement_ids) != expected_requirements:
                    _add(
                        result,
                        "ui-surface-blueprint-requirements-drift",
                        f"{identifier} requirements={sorted(requirement_ids)}, blueprint={sorted(expected_requirements)}",
                        path,
                    )
        if actual_ids != expected_ids:
            _add(
                result,
                "ui-surface-blueprint-drift",
                f"{field} IDs differ: contract={sorted(actual_ids)}, blueprint={sorted(expected_ids)}",
                path,
            )
        surface_ids.update(actual_ids)

    product_use_cases = {item for item in product_requirement_ids if USE_CASE_ID.fullmatch(item)}
    try:
        bindings = json_list(data.get("use_case_bindings"), "use_case_bindings")
    except ValueError as exc:
        _add(result, "ui-surface-use-case-invalid", str(exc), path)
        return
    bound_use_cases: set[str] = set()
    for index, raw_item in enumerate(bindings):
        label = f"use_case_bindings[{index}]"
        try:
            item = json_object(raw_item, label)
            use_case_id = json_string(item.get("use_case_id"), f"{label}.use_case_id")
            bound_surfaces = _string_list(
                item.get("surface_ids"), f"{label}.surface_ids", non_empty=True
            )
            coverage_types = set(
                _string_list(item.get("coverage_types"), f"{label}.coverage_types", non_empty=True)
            )
        except ValueError as exc:
            _add(result, "ui-surface-use-case-invalid", str(exc), path)
            continue
        _check_exact_keys(
            item, USE_CASE_BINDING_KEYS, label=label, path=path, result=result
        )
        if use_case_id in bound_use_cases or use_case_id not in product_use_cases:
            _add(
                result,
                "ui-surface-use-case-invalid",
                f"invalid or duplicate use case binding {use_case_id}",
                path,
            )
        bound_use_cases.add(use_case_id)
        unknown_surfaces = sorted(set(bound_surfaces) - surface_ids)
        if unknown_surfaces:
            _add(
                result,
                "ui-surface-reference-invalid",
                f"{use_case_id} unknown surfaces: {unknown_surfaces}",
                path,
            )
        derived_types: set[str] = set()
        for surface_id in bound_surfaces:
            if surface_id in route_ids:
                derived_types.add("route")
            elif OVERLAY_ID.fullmatch(surface_id):
                derived_types.add("overlay")
            elif SYSTEM_SURFACE_ID.fullmatch(surface_id):
                derived_types.add("system")
            elif CROSS_SURFACE_CAPABILITY_ID.fullmatch(surface_id):
                derived_types.add("cross_surface_capability")
        if coverage_types != derived_types:
            _add(
                result,
                "ui-surface-coverage-type-drift",
                f"{use_case_id} coverage_types={sorted(coverage_types)}, derived={sorted(derived_types)}",
                path,
            )
        if not isinstance(item.get("rationale"), str) or not item.get("rationale", "").strip():
            _add(
                result,
                "ui-surface-use-case-invalid",
                f"{use_case_id} requires a route-decision rationale",
                path,
            )
    if bound_use_cases != product_use_cases:
        _add(
            result,
            "ui-surface-use-case-gap",
            f"bindings={sorted(bound_use_cases)}, product={sorted(product_use_cases)}",
            path,
        )
    result.details.update(
        ui_surface_schema="1.0.0",
        ui_overlays=len(blueprint_overlays),
        ui_system_surfaces=len(blueprint_system_surfaces),
        ui_cross_surface_capabilities=len(blueprint_capabilities),
        ui_use_case_bindings=len(bound_use_cases),
    )


def check(
    root: Path,
    ui_blueprint: Path = Path("custometry-ui-blueprint-ru.md"),
    registry: Path = Path("packages/contracts/routes/ui-routes.json"),
    english_titles: Path = Path("packages/localization/locales/en/route-titles.json"),
    russian_titles: Path = Path("packages/localization/locales/ru/route-titles.json"),
    executable_contract: Path = Path("packages/contracts/routes/ui-route-contracts.json"),
    executable_schema: Path = Path("packages/contracts/routes/ui-route-contracts.schema.json"),
    product_blueprint: Path = Path("custometry-technical-blueprint-ru.md"),
    surface_contract: Path = Path("packages/contracts/routes/ui-surface-contracts.json"),
    surface_schema: Path = Path("packages/contracts/routes/ui-surface-contracts.schema.json"),
) -> CheckResult:
    result = CheckResult("validate_route_registry")
    blueprint_path = root / ui_blueprint
    registry_path = root / registry
    english_path = root / english_titles
    russian_path = root / russian_titles
    contract_path = root / executable_contract
    schema_path = root / executable_schema
    product_path = root / product_blueprint
    surface_contract_path = root / surface_contract
    surface_schema_path = root / surface_schema
    required_paths = (
        blueprint_path,
        registry_path,
        english_path,
        russian_path,
        contract_path,
        schema_path,
        product_path,
        surface_contract_path,
        surface_schema_path,
    )
    if not all(require_file(path, result) for path in required_paths):
        return result
    try:
        expected = blueprint_routes(blueprint_path)
        records, utility_records = _registry(json_object(load_json(registry_path), "registry"))
        english = _title_catalog(json_object(load_json(english_path), "english titles"), "en")
        russian = _title_catalog(json_object(load_json(russian_path), "russian titles"), "ru")
        contract = json_object(load_json(contract_path), "executable route contract")
        schema = json_object(load_json(schema_path), "executable route schema")
        ui_surface_contract = json_object(
            load_json(surface_contract_path), "UI surface coverage contract"
        )
        ui_surface_schema = json_object(load_json(surface_schema_path), "UI surface schema")
        blueprint_overlays = blueprint_requirement_surfaces(blueprint_path, OVERLAY_ID)
        blueprint_system_surfaces = blueprint_requirement_surfaces(
            blueprint_path, SYSTEM_SURFACE_ID
        )
        blueprint_capabilities = blueprint_requirement_surfaces(
            blueprint_path, CROSS_SURFACE_CAPABILITY_ID
        )
        ui_meta, _ = parse_frontmatter(blueprint_path)
        product_meta, product_body = parse_frontmatter(product_path)
        product_text = product_path.read_text(encoding="utf-8")
        product_permissions = _permission_catalog(product_body)
        product_requirement_ids = stable_ids(product_text)
        product_spec_version = json_string(product_meta.get("spec_version"), "product spec_version")
        ui_spec_version = json_string(ui_meta.get("ui_spec_version"), "UI spec_version")
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
        if TITLE_KEY.fullmatch(title_key) is None:
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
            result.add(
                "route-status-invalid", f"{identifier} has status {record['status']}", registry_path
            )

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
        result.add(
            "route-extra", f"registry route is not in UI blueprint: {identifier}", registry_path
        )
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
        result.add(
            "english-route-title-missing", f"{key} is required by {title_keys[key]}", english_path
        )
    for key in sorted(used_title_keys - russian.keys()):
        result.add(
            "russian-route-title-missing", f"{key} is required by {title_keys[key]}", russian_path
        )
    for key in sorted(english.keys() - used_title_keys):
        result.add("english-route-title-unused", key, english_path)
    for key in sorted(russian.keys() - used_title_keys):
        result.add("russian-route-title-unused", key, russian_path)

    _check_schema(schema, schema_path, result)
    _check_executable_contract(
        contract,
        path=contract_path,
        expected=expected,
        actual=actual,
        product_spec_version=product_spec_version,
        ui_spec_version=ui_spec_version,
        product_permissions=product_permissions,
        product_requirement_ids=product_requirement_ids,
        result=result,
    )
    _check_surface_contract(
        ui_surface_contract,
        schema=ui_surface_schema,
        path=surface_contract_path,
        schema_path=surface_schema_path,
        route_contract=contract,
        route_ids=set(actual),
        blueprint_overlays=blueprint_overlays,
        blueprint_system_surfaces=blueprint_system_surfaces,
        blueprint_capabilities=blueprint_capabilities,
        product_spec_version=product_spec_version,
        ui_spec_version=ui_spec_version,
        product_requirement_ids=product_requirement_ids,
        result=result,
    )
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
    parser = argparse.ArgumentParser(
        description="Validate UI route identity and execution contracts"
    )
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
    parser.add_argument(
        "--executable-contract",
        type=Path,
        default=Path("packages/contracts/routes/ui-route-contracts.json"),
    )
    parser.add_argument(
        "--executable-schema",
        type=Path,
        default=Path("packages/contracts/routes/ui-route-contracts.schema.json"),
    )
    parser.add_argument(
        "--product-blueprint", type=Path, default=Path("custometry-technical-blueprint-ru.md")
    )
    parser.add_argument(
        "--surface-contract",
        type=Path,
        default=Path("packages/contracts/routes/ui-surface-contracts.json"),
    )
    parser.add_argument(
        "--surface-schema",
        type=Path,
        default=Path("packages/contracts/routes/ui-surface-contracts.schema.json"),
    )
    args = parser.parse_args(argv)
    return render_result(
        check(
            args.root.resolve(),
            args.ui_blueprint,
            args.registry,
            args.english_titles,
            args.russian_titles,
            args.executable_contract,
            args.executable_schema,
            args.product_blueprint,
            args.surface_contract,
            args.surface_schema,
        ),
        args.json,
    )


if __name__ == "__main__":
    main_guard(cli)
