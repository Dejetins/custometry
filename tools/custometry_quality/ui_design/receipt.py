from __future__ import annotations

import hashlib
from typing import Any, cast

from tools.custometry_quality.core import CheckResult, canonical_json, json_list, json_object


RECEIPT_SCHEMA_VERSION = "custometry.ui-design.render-receipt/v1"
IGNORED_TARGET_KEYS = {"candidate_id", "candidate_node_id", "rendered_at"}


def normalized_semantic_structure(receipt: dict[str, Any]) -> dict[str, Any]:
    target = cast(dict[str, Any], json_object(receipt.get("target", {}), "receipt.target"))
    normalized_target = {
        key: value for key, value in target.items() if key not in IGNORED_TARGET_KEYS
    }
    instances: list[dict[str, Any]] = []
    for raw_item in json_list(receipt.get("instances", []), "receipt.instances"):
        item = cast(dict[str, Any], json_object(raw_item, "receipt.instances[]"))
        instances.append(
            {
                key: value
                for key, value in item.items()
                if key not in {"figma_instance_id", "absolute_x", "absolute_y"}
            }
        )
    return {
        "schema_version": receipt.get("schema_version"),
        "manifest_digest": receipt.get("manifest_digest"),
        "renderer_version": receipt.get("renderer_version"),
        "target": normalized_target,
        "wrappers": receipt.get("wrappers"),
        "instances": instances,
        "detached_instance_count": receipt.get("detached_instance_count"),
        "binding_audit": receipt.get("binding_audit"),
    }


def semantic_structure_digest(receipt: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(normalized_semantic_structure(receipt))).hexdigest()


def audit_receipt_data(receipt: dict[str, Any], plan: dict[str, Any]) -> CheckResult:
    result = CheckResult(check="ui-design-render-receipt")
    if receipt.get("schema_version") != RECEIPT_SCHEMA_VERSION:
        result.add("unknown-contract-version", "receipt schema_version is unsupported")
    for key in ("manifest_digest", "renderer_version"):
        if receipt.get(key) != plan.get(key):
            result.add("receipt-contract-drift", f"receipt {key} does not match render plan")

    receipt_target = cast(
        dict[str, Any], json_object(receipt.get("target", {}), "receipt.target")
    )
    plan_target = cast(dict[str, Any], json_object(plan.get("target", {}), "plan.target"))
    for key in ("library_file_key", "library_page_id", "product_file_key", "product_page_id"):
        if receipt_target.get(key) != plan_target.get(key):
            result.add("target-drift", f"receipt target {key} does not match render plan")

    detached = receipt.get("detached_instance_count")
    if detached != 0:
        result.add("detached-instance", f"expected zero detached instances; observed {detached!r}")

    wrappers = receipt.get("wrappers")
    if wrappers != plan.get("allowed_structural_wrappers"):
        result.add("wrapper-drift", "receipt structural wrappers do not match renderer allowlist")

    planned_instances = [
        cast(dict[str, Any], json_object(value, "plan.instances[]"))
        for value in json_list(plan.get("instances", []), "plan.instances")
    ]
    observed_instances = [
        cast(dict[str, Any], json_object(value, "receipt.instances[]"))
        for value in json_list(receipt.get("instances", []), "receipt.instances")
    ]
    planned_identity = [
        (item.get("region_id"), item.get("instance_id"), item.get("component_id"), item.get("variant"))
        for item in planned_instances
    ]
    observed_identity = [
        (item.get("region_id"), item.get("instance_id"), item.get("component_id"), item.get("variant"))
        for item in observed_instances
    ]
    if observed_identity != planned_identity:
        result.add("instance-structure-drift", "receipt instances differ from deterministic plan")
    for item in observed_instances:
        if item.get("node_type") != "INSTANCE":
            result.add(
                "raw-visible-node",
                f"visible item {item.get('instance_id')!r} is not a Figma INSTANCE",
            )
        component_key = item.get("component_key")
        if not isinstance(component_key, str) or not component_key:
            result.add(
                "component-key-missing",
                f"instance {item.get('instance_id')!r} has no cross-file component key",
            )

    binding_audit = cast(
        dict[str, Any], json_object(receipt.get("binding_audit", {}), "receipt.binding_audit")
    )
    for key in ("unbound_paint_count", "unbound_text_style_count", "raw_icon_count"):
        if binding_audit.get(key) != 0:
            result.add("binding-audit-failed", f"{key} must be zero")
    if binding_audit.get("semantic_variable_mode") not in {
        "abyss",
        "graphite",
        "frost",
        "paper",
    }:
        result.add("binding-audit-failed", "semantic_variable_mode is missing or invalid")

    result.details.update(
        {
            "candidate_id": receipt.get("candidate_id"),
            "instance_count": len(observed_instances),
            "semantic_structure_digest": semantic_structure_digest(receipt),
        }
    )
    return result
