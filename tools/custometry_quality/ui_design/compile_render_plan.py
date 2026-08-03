from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any, cast

from tools.custometry_quality.core import (
    CheckResult,
    canonical_json,
    json_list,
    json_object,
    json_string,
    load_json,
    render_result,
    repo_root,
    sha256_file,
    write_or_check,
)
from tools.custometry_quality.ui_design.validate import SUPPORTED_VERSION, validate_contracts


ALLOWED_STRUCTURAL_WRAPPERS = [
    "candidate-root",
    "application-grid",
    "primary-content-stack",
]


def compile_plan_data(
    tokens: dict[str, Any],
    components: dict[str, Any],
    icons: dict[str, Any],
    manifest: dict[str, Any],
) -> dict[str, Any]:
    validation = validate_contracts(tokens, components, icons, manifest)
    if not validation.ok:
        codes = ", ".join(item.code for item in validation.findings)
        raise ValueError(f"cannot compile invalid UI design contracts: {codes}")

    component_items = [
        cast(dict[str, Any], json_object(value, "components[]"))
        for value in json_list(components.get("components", []), "components")
    ]
    component_map = {
        json_string(item.get("id"), "component.id"): item for item in component_items
    }
    regions = [
        cast(dict[str, Any], json_object(value, "regions[]"))
        for value in json_list(manifest.get("regions", []), "regions")
    ]
    instances: list[dict[str, Any]] = []
    for order, region in enumerate(regions):
        component_id = json_string(region.get("component_id"), "region.component_id")
        component = component_map[component_id]
        instances.append(
            {
                "order": order,
                "region_id": region["region_id"],
                "instance_id": region["instance_id"],
                "component_id": component_id,
                "figma_component_name": component["figma_name"],
                "variant": region["variant"],
                "props": region["props"],
                "action_id": region.get("action_id"),
                "bindings": region.get("bindings", {}),
            }
        )

    manifest_digest = hashlib.sha256(canonical_json(manifest)).hexdigest()
    return {
        "schema_version": "custometry.ui-design.render-plan/v1",
        "renderer_version": SUPPORTED_VERSION,
        "dedupe_key": (
            f"{manifest['target']['candidate_id']}:{manifest_digest}:{SUPPORTED_VERSION}"
        ),
        "manifest_digest": manifest_digest,
        "surface_id": manifest["surface_id"],
        "product_state": manifest["product_state"],
        "theme": manifest["theme"],
        "locale": manifest["locale"],
        "viewport": manifest["viewport"],
        "target": manifest["target"],
        "contract_versions": manifest["contracts"],
        "allowed_structural_wrappers": ALLOWED_STRUCTURAL_WRAPPERS,
        "instances": instances,
    }


def check(root: Path, output: Path, check_mode: bool) -> CheckResult:
    contract_root = root / "packages/contracts/ui-design"
    result = CheckResult(check="ui-design-render-plan")
    inputs = {
        "tokens": contract_root / "tokens.v1.json",
        "components": contract_root / "components.ui-an-003.v1.json",
        "icons": contract_root / "icons.ui-an-003.v1.json",
        "manifest": contract_root / "ui-an-003.manifest.v1.json",
    }
    try:
        loaded = {
            name: cast(dict[str, Any], load_json(path)) for name, path in inputs.items()
        }
        plan = compile_plan_data(
            loaded["tokens"], loaded["components"], loaded["icons"], loaded["manifest"]
        )
    except (OSError, ValueError, KeyError) as exc:
        result.observed = False
        result.add("render-plan-compile-failed", str(exc))
        return result

    plan["input_digests"] = {name: sha256_file(path) for name, path in inputs.items()}
    output_path = output if output.is_absolute() else root / output
    write_or_check(output_path, canonical_json(plan), check_mode, result)
    result.details.update(
        {
            "manifest_digest": plan["manifest_digest"],
            "instance_count": len(cast(list[object], plan["instances"])),
            "renderer_version": SUPPORTED_VERSION,
        }
    )
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile a deterministic UI render plan")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            ".codex/delivery/evidence/assets/W21-CONTRACT-COMPILED-UI-PILOT/"
            "ui-an-003.render-plan.v1.json"
        ),
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def cli(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root(args.root)
    return render_result(check(root, args.output, args.check), json_output=args.json)


if __name__ == "__main__":
    raise SystemExit(cli())
