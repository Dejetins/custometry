from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, cast

import pytest

from tools.custometry_quality.core import canonical_json
from tools.custometry_quality.ui_design.compile_render_plan import compile_plan_data
from tools.custometry_quality.ui_design.receipt import (
    audit_receipt_data,
    semantic_structure_digest,
)
from tools.custometry_quality.ui_design.validate import validate_contracts


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_ROOT = ROOT / "packages/contracts/ui-design"
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures"


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return cast(dict[str, Any], value)


def contracts() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    return (
        load(CONTRACT_ROOT / "tokens.v1.json"),
        load(CONTRACT_ROOT / "components.ui-an-003.v1.json"),
        load(CONTRACT_ROOT / "icons.ui-an-003.v1.json"),
        load(CONTRACT_ROOT / "ui-an-003.manifest.v1.json"),
    )


def apply_mutation(document: dict[str, Any], fixture: dict[str, Any]) -> None:
    mutation = cast(dict[str, Any], fixture["mutation"])
    path = cast(list[str | int], mutation["path"])
    parent: Any = document
    for segment in path[:-1]:
        parent = parent[segment]
    final = path[-1]
    if mutation["op"] == "set":
        parent[final] = copy.deepcopy(mutation["value"])
    elif mutation["op"] == "delete":
        del parent[final]
    else:
        raise AssertionError(f"unsupported fixture operation: {mutation['op']}")


def receipt_for(plan: dict[str, Any], candidate_id: str = "candidate-a") -> dict[str, Any]:
    instances: list[dict[str, Any]] = []
    for index, planned in enumerate(cast(list[dict[str, Any]], plan["instances"])):
        instances.append(
            {
                "region_id": planned["region_id"],
                "instance_id": planned["instance_id"],
                "component_id": planned["component_id"],
                "variant": planned["variant"],
                "node_type": "INSTANCE",
                "component_key": f"published-key-{planned['component_id']}",
                "figma_instance_id": f"100:{index}",
            }
        )
    target = copy.deepcopy(cast(dict[str, Any], plan["target"]))
    target["candidate_id"] = candidate_id
    target["candidate_node_id"] = "200:1"
    return {
        "schema_version": "custometry.ui-design.render-receipt/v1",
        "candidate_id": candidate_id,
        "manifest_digest": plan["manifest_digest"],
        "renderer_version": plan["renderer_version"],
        "target": target,
        "wrappers": plan["allowed_structural_wrappers"],
        "instances": instances,
        "detached_instance_count": 0,
        "binding_audit": {
            "unbound_paint_count": 0,
            "unbound_text_style_count": 0,
            "raw_icon_count": 0,
            "semantic_variable_mode": "graphite",
        },
    }


def test_canonical_contracts_validate_and_compile_deterministically() -> None:
    tokens, components, icons, manifest = contracts()
    assert validate_contracts(tokens, components, icons, manifest).ok

    first = compile_plan_data(tokens, components, icons, manifest)
    second = compile_plan_data(tokens, components, icons, manifest)
    assert canonical_json(first) == canonical_json(second)
    assert first["manifest_digest"] == second["manifest_digest"]
    assert len(cast(list[object], first["instances"])) == 9


def test_receipts_audit_and_normalize_platform_generated_identities() -> None:
    tokens, components, icons, manifest = contracts()
    plan = compile_plan_data(tokens, components, icons, manifest)
    first = receipt_for(plan, "candidate-a")
    second = receipt_for(plan, "candidate-b")
    second["target"]["candidate_node_id"] = "900:20"
    for index, item in enumerate(second["instances"]):
        item["figma_instance_id"] = f"900:{index + 30}"

    assert audit_receipt_data(first, plan).ok
    assert audit_receipt_data(second, plan).ok
    assert semantic_structure_digest(first) == semantic_structure_digest(second)


MANIFEST_NEGATIVE_FIXTURES = [
    "raw-node.json",
    "unknown-component.json",
    "forbidden-action.json",
    "missing-region.json",
    "target-drift.json",
    "unknown-version.json",
]


@pytest.mark.parametrize("fixture_name", MANIFEST_NEGATIVE_FIXTURES)
def test_manifest_negative_fixtures_fail_closed(fixture_name: str) -> None:
    tokens, components, icons, manifest = contracts()
    fixture = load(FIXTURE_ROOT / fixture_name)
    apply_mutation(manifest, fixture)
    result = validate_contracts(tokens, components, icons, manifest)
    assert not result.ok
    assert fixture["expected_code"] in {finding.code for finding in result.findings}


def test_detached_instance_fixture_fails_closed() -> None:
    tokens, components, icons, manifest = contracts()
    plan = compile_plan_data(tokens, components, icons, manifest)
    receipt = receipt_for(plan)
    fixture = load(FIXTURE_ROOT / "detached-instance.json")
    apply_mutation(receipt, fixture)
    result = audit_receipt_data(receipt, plan)
    assert not result.ok
    assert fixture["expected_code"] in {finding.code for finding in result.findings}
