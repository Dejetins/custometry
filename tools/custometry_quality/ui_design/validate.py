from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, cast

from tools.custometry_quality.core import (
    CheckResult,
    add_common_arguments,
    json_list,
    json_object,
    json_string,
    load_json,
    render_result,
    repo_root,
)


TOKEN_SCHEMA_VERSION = "custometry.ui-design.tokens/v1"
COMPONENT_SCHEMA_VERSION = "custometry.ui-design.components/v1"
ICON_SCHEMA_VERSION = "custometry.ui-design.icons/v1"
MANIFEST_SCHEMA_VERSION = "custometry.ui-design.screen-manifest/v1"
SUPPORTED_VERSION = "1.0.0"
THEMES = ["abyss", "graphite", "frost", "paper"]
ALLOWED_ACTIONS = {
    "analysis.run",
    "analysis.manage",
    "export.create",
    "share.link",
    "report.email",
}
REQUIRED_REGIONS = {
    "shell",
    "sidebar",
    "page-header",
    "context-bar",
    "kpi-strip",
    "chart-frame",
    "channel-table",
    "context-inspector",
    "result-trust",
}
EXPECTED_TARGET = {
    "library_file_key": "hX3nQOtcSdCc97uv26m9eG",
    "library_page_id": "0:1",
    "product_file_key": "MXfxuhSFpIczbUtFmOSyPp",
    "product_page_id": "0:1",
}
FORBIDDEN_MANIFEST_KEYS = {
    "raw_node",
    "raw_nodes",
    "figma_node",
    "figma_nodes",
    "raw_color",
    "raw_typography",
    "detach",
    "detached",
    "rectangle",
    "ellipse",
    "vector",
    "line",
}


def _items(value: object, label: str) -> list[dict[str, Any]]:
    return [cast(dict[str, Any], json_object(item, f"{label}[]")) for item in json_list(value, label)]


def _duplicates(values: list[str]) -> set[str]:
    return {value for value in values if values.count(value) > 1}


def _walk_forbidden(value: object, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        mapping = cast(dict[object, object], value)
        for raw_key, child in mapping.items():
            key = str(raw_key)
            child_path = f"{path}.{key}"
            if key.lower() in FORBIDDEN_MANIFEST_KEYS:
                findings.append(child_path)
            findings.extend(_walk_forbidden(child, child_path))
    elif isinstance(value, list):
        sequence = cast(list[object], value)
        for index, child in enumerate(sequence):
            findings.extend(_walk_forbidden(child, f"{path}[{index}]"))
    return findings


def validate_contracts(
    tokens: dict[str, Any],
    components: dict[str, Any],
    icons: dict[str, Any],
    manifest: dict[str, Any],
) -> CheckResult:
    result = CheckResult(check="ui-design-contracts")

    versions = {
        "tokens": tokens.get("schema_version"),
        "components": components.get("schema_version"),
        "icons": icons.get("schema_version"),
        "manifest": manifest.get("schema_version"),
    }
    expected_versions = {
        "tokens": TOKEN_SCHEMA_VERSION,
        "components": COMPONENT_SCHEMA_VERSION,
        "icons": ICON_SCHEMA_VERSION,
        "manifest": MANIFEST_SCHEMA_VERSION,
    }
    for name, expected in expected_versions.items():
        if versions[name] != expected:
            result.add(
                "unknown-contract-version",
                f"{name} schema_version must be {expected!r}; observed {versions[name]!r}",
            )

    semantic_versions = {
        "token_version": tokens.get("token_version"),
        "registry_version": components.get("registry_version"),
        "icon_version": icons.get("icon_version"),
        "manifest_version": manifest.get("manifest_version"),
    }
    for name, version in semantic_versions.items():
        if version != SUPPORTED_VERSION:
            result.add(
                "unknown-contract-version",
                f"{name} must be {SUPPORTED_VERSION!r}; observed {version!r}",
            )

    observed_themes = tokens.get("themes")
    if observed_themes != THEMES:
        result.add("theme-contract-invalid", f"themes must be ordered exactly as {THEMES!r}")

    token_items = _items(tokens.get("tokens", []), "tokens.tokens")
    token_names = [json_string(item.get("name"), "token.name") for item in token_items]
    for duplicate in sorted(_duplicates(token_names)):
        result.add("duplicate-token", f"token {duplicate!r} is declared more than once")
    token_name_set = set(token_names)
    for item in token_items:
        name = json_string(item.get("name"), "token.name")
        values = json_object(item.get("values"), f"token {name}.values")
        if item.get("type") == "color" and list(values) != THEMES:
            result.add(
                "theme-token-incomplete",
                f"color token {name!r} must define the four ordered theme modes",
            )

    component_items = _items(components.get("components", []), "components.components")
    component_ids = [json_string(item.get("id"), "component.id") for item in component_items]
    for duplicate in sorted(_duplicates(component_ids)):
        result.add("duplicate-component", f"component {duplicate!r} is declared more than once")
    component_map = {json_string(item.get("id"), "component.id"): item for item in component_items}
    if components.get("token_version") != tokens.get("token_version"):
        result.add("contract-version-drift", "component registry token_version does not match tokens")
    for component_id, item in component_map.items():
        required_tokens = [
            json_string(value, f"component {component_id}.required_tokens[]")
            for value in json_list(item.get("required_tokens", []), "required_tokens")
        ]
        for token_name in required_tokens:
            if token_name not in token_name_set:
                result.add(
                    "unknown-token",
                    f"component {component_id!r} references unknown token {token_name!r}",
                )
        actions = {
            json_string(value, f"component {component_id}.actions[]")
            for value in json_list(item.get("actions", []), "actions")
        }
        for action in sorted(actions - ALLOWED_ACTIONS):
            result.add(
                "forbidden-action",
                f"component {component_id!r} declares forbidden action {action!r}",
            )

    icon_items = [
        json_string(value, "icons.icons[]")
        for value in json_list(icons.get("icons", []), "icons.icons")
    ]
    for duplicate in sorted(_duplicates(icon_items)):
        result.add("duplicate-icon", f"icon {duplicate!r} is declared more than once")

    for forbidden_path in _walk_forbidden(manifest):
        result.add(
            "raw-node-forbidden",
            f"restricted screen manifest contains forbidden construction key at {forbidden_path}",
        )

    if manifest.get("surface_id") != "UI-AN-003":
        result.add("surface-drift", "surface_id must remain UI-AN-003")
    if manifest.get("route") != "/w/:workspaceKey/analytics/sales":
        result.add("route-drift", "route must remain /w/:workspaceKey/analytics/sales")
    if manifest.get("product_state") != "success":
        result.add("state-drift", "pilot manifest must remain in success state")
    if manifest.get("viewport") != {"width": 1440, "height": 900}:
        result.add("viewport-drift", "pilot viewport must remain exactly 1440 by 900")
    if manifest.get("theme") not in THEMES:
        result.add("theme-contract-invalid", "manifest theme is not a registered theme")
    if manifest.get("locale") not in {"en", "ru"}:
        result.add("locale-contract-invalid", "manifest locale must be en or ru")

    target = json_object(manifest.get("target"), "manifest.target")
    for key, expected in EXPECTED_TARGET.items():
        if target.get(key) != expected:
            result.add(
                "target-drift",
                f"manifest target {key} must be {expected!r}; observed {target.get(key)!r}",
            )

    contract_refs = json_object(manifest.get("contracts"), "manifest.contracts")
    expected_contract_refs = {
        "token_version": tokens.get("token_version"),
        "component_registry_version": components.get("registry_version"),
        "icon_version": icons.get("icon_version"),
        "renderer_version": SUPPORTED_VERSION,
    }
    for key, expected in expected_contract_refs.items():
        if contract_refs.get(key) != expected:
            result.add(
                "contract-version-drift",
                f"manifest contracts.{key} must be {expected!r}",
            )

    allowed_actions = {
        json_string(value, "manifest.allowed_actions[]")
        for value in json_list(manifest.get("allowed_actions", []), "allowed_actions")
    }
    for action in sorted(allowed_actions - ALLOWED_ACTIONS):
        result.add("forbidden-action", f"manifest permits forbidden action {action!r}")
    if allowed_actions != ALLOWED_ACTIONS:
        result.add(
            "action-contract-incomplete",
            f"manifest actions must match the route contract: {sorted(ALLOWED_ACTIONS)!r}",
        )

    required_regions = {
        json_string(value, "manifest.required_regions[]")
        for value in json_list(manifest.get("required_regions", []), "required_regions")
    }
    region_items = _items(manifest.get("regions", []), "manifest.regions")
    region_ids = [json_string(item.get("region_id"), "region.region_id") for item in region_items]
    for duplicate in sorted(_duplicates(region_ids)):
        result.add("duplicate-region", f"region {duplicate!r} is declared more than once")
    missing_regions = REQUIRED_REGIONS - set(region_ids)
    missing_required_declarations = REQUIRED_REGIONS - required_regions
    for region_id in sorted(missing_regions | missing_required_declarations):
        result.add("missing-region", f"required region {region_id!r} is absent")

    instance_ids = [json_string(item.get("instance_id"), "region.instance_id") for item in region_items]
    for duplicate in sorted(_duplicates(instance_ids)):
        result.add("duplicate-instance", f"instance {duplicate!r} is declared more than once")

    for region in region_items:
        component_id = json_string(region.get("component_id"), "region.component_id")
        component = component_map.get(component_id)
        if component is None:
            result.add(
                "unknown-component",
                f"region {region.get('region_id')!r} references unknown component {component_id!r}",
            )
            continue
        variant = json_string(region.get("variant"), "region.variant")
        variants = {
            json_string(value, f"component {component_id}.variants[]")
            for value in json_list(component.get("variants", []), "variants")
        }
        if variant not in variants:
            result.add(
                "unknown-variant",
                f"component {component_id!r} does not register variant {variant!r}",
            )
        action = region.get("action_id")
        if action is not None:
            action_id = json_string(action, "region.action_id")
            component_actions = {
                json_string(value, f"component {component_id}.actions[]")
                for value in json_list(component.get("actions", []), "actions")
            }
            if action_id not in allowed_actions or action_id not in component_actions:
                result.add(
                    "forbidden-action",
                    f"region {region.get('region_id')!r} uses unregistered action {action_id!r}",
                )

    result.details.update(
        {
            "token_count": len(token_items),
            "component_count": len(component_items),
            "icon_count": len(icon_items),
            "region_count": len(region_items),
            "surface_id": manifest.get("surface_id"),
            "candidate_id": target.get("candidate_id"),
        }
    )
    return result


def check(root: Path) -> CheckResult:
    contract_root = root / "packages/contracts/ui-design"
    try:
        tokens = cast(dict[str, Any], load_json(contract_root / "tokens.v1.json"))
        components = cast(
            dict[str, Any], load_json(contract_root / "components.ui-an-003.v1.json")
        )
        icons = cast(dict[str, Any], load_json(contract_root / "icons.ui-an-003.v1.json"))
        manifest = cast(
            dict[str, Any], load_json(contract_root / "ui-an-003.manifest.v1.json")
        )
    except (OSError, ValueError) as exc:
        result = CheckResult(check="ui-design-contracts", observed=False)
        result.add("contract-load-failed", str(exc))
        return result
    return validate_contracts(tokens, components, icons, manifest)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Custometry UI design contracts")
    add_common_arguments(parser)
    return parser


def cli(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root(args.root)
    return render_result(check(root), json_output=args.json)


if __name__ == "__main__":
    raise SystemExit(cli())
