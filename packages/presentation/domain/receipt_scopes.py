"""Deterministic scope composition; no provider lookup or predicate evaluation."""

from __future__ import annotations
import json
from typing import Any, Literal
from uuid import NAMESPACE_URL, UUID, uuid5
from packages.contracts.analytics.columnar_filters import (
    FlatBoolean,
    canonical_flat_expression,
    flat_expression_fields,
)
from packages.contracts.analytics.retail_filter import ReceiptFilterInput
from packages.contracts.analytics.retail_relational import RelationalReceiptFilterInput
from packages.contracts.analytics.receipt_selection import ReceiptSelection
from packages.contracts.analytics.receipt_cohorts import CohortReceiptFilterInput, CohortBoolean
from packages.contracts.analytics.sequence_filters import canonical_sequence_expression
from packages.contracts.analytics.retail_aggregate import AggregateReceiptFilterInput
from packages.contracts.analytics.aggregate_filters import (
    AggregateBoolean,
    canonical_aggregate_expression,
)
from packages.contracts.analytics.relational_filters import (
    ScopedBoolean,
    canonical_scoped_expression,
)


def canonical_filter(value: ReceiptSelection) -> dict[str, Any]:
    raw = value.model_dump(mode="json")
    raw["expression"] = (
        canonical_flat_expression(value.expression)
        if isinstance(value, ReceiptFilterInput)
        else canonical_sequence_expression(value.expression)
        if isinstance(value, CohortReceiptFilterInput)
        else canonical_aggregate_expression(value.expression)
        if isinstance(value, AggregateReceiptFilterInput)
        else canonical_scoped_expression(value.expression)
    )
    return raw


def replacement_field(value: ReceiptSelection) -> set[str]:
    if isinstance(value, ReceiptFilterInput):
        return set(flat_expression_fields(value.expression))

    def fields(node: dict[str, Any]) -> set[str]:
        if node["kind"] in (
            "exists",
            "not_exists",
            "aggregate_compare",
            "customer_event_membership",
        ) or node["scope_id"] != str(value.root_scope_id):
            return set()
        if node["kind"] == "predicate":
            return {node["field_id"]}
        children = [node["child"]] if node["kind"] == "not" else node["children"]
        parts = [fields(c) for c in children]
        return {field for part in parts for field in part} if all(parts) else set()

    return fields(value.expression.model_dump(mode="json"))


def compatible(left: ReceiptSelection, right: ReceiptSelection) -> bool:
    if isinstance(left, CohortReceiptFilterInput) or isinstance(right, CohortReceiptFilterInput):
        cohort = left if isinstance(left, CohortReceiptFilterInput) else right
        other = right if isinstance(left, CohortReceiptFilterInput) else left
        assert isinstance(cohort, CohortReceiptFilterInput)
        if any(
            origin != cohort.receipt_registry_versions for origin in cohort.promoted_registry_sets
        ):
            return False
        if isinstance(other, ReceiptFilterInput):
            return (
                cohort.legacy_registry_version_id is None
                or cohort.legacy_registry_version_id == other.registry_version_id
            )
        if (
            cohort.legacy_registry_version_id is not None
            and other.legacy_registry_version_id is not None
            and cohort.legacy_registry_version_id != other.legacy_registry_version_id
        ):
            return False
        if isinstance(other, CohortReceiptFilterInput):
            return (
                cohort.registry_versions == other.registry_versions
                and cohort.receipt_registry_versions == other.receipt_registry_versions
                and all(
                    origin == other.receipt_registry_versions
                    for origin in other.promoted_registry_sets
                )
            )
        return cohort.receipt_registry_versions == other.registry_versions
    if isinstance(left, ReceiptFilterInput) and isinstance(right, ReceiptFilterInput):
        return left.registry_version_id == right.registry_version_id
    if not isinstance(left, ReceiptFilterInput) and not isinstance(right, ReceiptFilterInput):
        return (
            left.registry_versions == right.registry_versions
            and left.legacy_registry_version_id == right.legacy_registry_version_id
        )
    old = left if isinstance(left, ReceiptFilterInput) else right
    new = right if not isinstance(right, ReceiptFilterInput) else left
    assert isinstance(old, ReceiptFilterInput) and isinstance(
        new, (RelationalReceiptFilterInput, AggregateReceiptFilterInput)
    )
    return new.legacy_registry_version_id == old.registry_version_id


def compatible_replacement(child: ReceiptSelection, parent: ReceiptSelection) -> bool:
    """Replacement must retain pins of an ancestor removed from the effective query."""
    if not compatible(child, parent):
        return False
    parent_pin = (parent.registry_version_id if isinstance(parent, ReceiptFilterInput)
                  else parent.legacy_registry_version_id)
    child_pin = (child.registry_version_id if isinstance(child, ReceiptFilterInput)
                 else child.legacy_registry_version_id)
    return parent_pin is None or child_pin == parent_pin


def combine_filters(
    inputs: list[tuple[UUID | Literal["block-base"], ReceiptSelection]],
) -> ReceiptSelection:
    values = [v for _, v in inputs]
    if all(isinstance(v, ReceiptFilterInput) for v in values):
        old = [v for v in values if isinstance(v, ReceiptFilterInput)]
        if len({v.registry_version_id for v in old}) != 1:
            raise ValueError("COMPOSER_FILTER_REGISTRY_MISMATCH")
        return ReceiptFilterInput(
            registry_version_id=old[0].registry_version_id,
            expression=old[0].expression
            if len(old) == 1
            else FlatBoolean(kind="and", children=tuple(v.expression for v in old)),
        )
    new = next(
        (v for v in values if isinstance(v, CohortReceiptFilterInput)),
        next(v for v in values if not isinstance(v, ReceiptFilterInput)),
    )
    if any(not compatible(new, v) for v in values):
        raise ValueError("COMPOSER_FILTER_REGISTRY_MISMATCH")
    # These IDs are local to one effective request. Presentation source/block IDs
    # must not change query identity when a title changes or a block is copied.
    seed = uuid5(NAMESPACE_URL, "custometry/receipt-scope-composition/v2")
    root = uuid5(seed, "combined-receipt-root/v2")
    nodes: list[dict[str, Any]] = []
    for binding, value in inputs:
        namespace = uuid5(seed, f"binding/{binding}" if isinstance(binding, UUID) else binding)

        def rebase(raw: dict[str, Any], path: str) -> dict[str, Any]:
            node = dict(raw)
            if isinstance(value, ReceiptFilterInput):
                node.update(node_id=str(uuid5(namespace, path)), scope_id=str(root))
            else:
                for key in (
                    "node_id",
                    "scope_id",
                    "parent_scope_id",
                    "child_scope_id",
                    "customer_scope_id",
                    "step_id",
                    "after_step_id",
                    "left_step_id",
                    "right_step_id",
                ):
                    if key in node:
                        node[key] = str(
                            root
                            if key.endswith("scope_id") and node[key] == str(value.root_scope_id)
                            else uuid5(namespace, node[key])
                        )
            if node["kind"] in ("and", "or"):
                node["children"] = [
                    rebase(c, f"{path}/{i}") for i, c in enumerate(node["children"])
                ]
            elif node["kind"] == "not":
                node["child"] = rebase(node["child"], path + "/not")
            elif node["kind"] in (
                "exists",
                "not_exists",
                "customer_event_membership",
                "positive",
                "negative",
            ):
                node["predicate"] = rebase(node["predicate"], path + "/child")
            elif node["kind"] == "aggregate_compare":
                node["left"] = rebase(node["left"], path + "/left")
                node["right"] = rebase(node["right"], path + "/right")
            elif node["kind"] == "count_ratio":
                node["numerator"] = rebase(node["numerator"], path + "/numerator")
                node["denominator"] = rebase(node["denominator"], path + "/denominator")
            elif node["kind"] == "scoped_count":
                node["predicate"] = rebase(node["predicate"], path + "/rows")
            elif node["kind"] == "sequence":
                node["steps"] = [
                    rebase(step, f"{path}/step/{i}") for i, step in enumerate(node["steps"])
                ]
                node["bindings"] = [
                    {
                        **binding,
                        **{
                            key: str(uuid5(namespace, binding[key]))
                            for key in ("left_step_id", "right_step_id")
                        },
                    }
                    for binding in node["bindings"]
                ]
            return node

        # Canonical ordering makes v1 promotion IDs independent of Boolean order.
        raw = canonical_filter(value)["expression"]
        nodes.append(rebase(raw, "root"))
    if isinstance(new, CohortReceiptFilterInput):
        legacy_pins = {
            v.registry_version_id
            if isinstance(v, ReceiptFilterInput)
            else v.legacy_registry_version_id
            for v in values
        } - {None}
        if len(legacy_pins) > 1:
            raise ValueError("COMPOSER_FILTER_REGISTRY_MISMATCH")
        origins = [
            origin
            for value in values
            if isinstance(value, CohortReceiptFilterInput)
            for origin in value.promoted_registry_sets
        ]
        origins.extend(
            value.registry_versions
            for value in values
            if isinstance(value, (RelationalReceiptFilterInput, AggregateReceiptFilterInput))
        )
        unique = {
            json.dumps({k: str(v) for k, v in origin.items()}, sort_keys=True): origin
            for origin in origins
        }
        return CohortReceiptFilterInput(
            root_scope_id=root,
            registry_versions=new.registry_versions,
            receipt_registry_versions=new.receipt_registry_versions,
            promoted_registry_sets=tuple(unique[key] for key in sorted(unique)),
            legacy_registry_version_id=next(iter(legacy_pins), None),
            expression=CohortBoolean.model_validate(
                dict(kind="and", node_id=uuid5(root, "combined-and"), scope_id=root, children=nodes)
            ),
        )
    aggregate = any(isinstance(v, AggregateReceiptFilterInput) for v in values)
    expression = (AggregateBoolean if aggregate else ScopedBoolean).model_validate(
        dict(kind="and", node_id=uuid5(root, "combined-and"), scope_id=root, children=nodes)
    )
    output = AggregateReceiptFilterInput if aggregate else RelationalReceiptFilterInput
    return output.model_validate(
        dict(
            root_scope_id=root,
            registry_versions=new.registry_versions,
            expression=expression.model_dump(mode="json"),
            legacy_registry_version_id=new.legacy_registry_version_id,
        )
    )
