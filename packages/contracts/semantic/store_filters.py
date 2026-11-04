"""Versioned bounded Store expression semantics; no general registry claim."""

from __future__ import annotations
from typing import Annotated, Literal, Any
import json
from uuid import UUID
from pydantic import Field, field_validator, ConfigDict
from packages.contracts.semantic import Strict


class StoreSelection(Strict):
    kind: Literal["store_in"] = "store_in"
    field: Literal["Store.store_id"] = "Store.store_id"
    values: list[Annotated[str, Field(min_length=1, max_length=128, pattern=r"\S")]] = Field(
        max_length=1000
    )

    @field_validator("values", mode="after")
    @classmethod
    def canonical_values(cls, values: list[str]) -> list[str]:
        return sorted(set(values))


class StoreBoolean(Strict):
    model_config = ConfigDict(extra="forbid", frozen=True, json_schema_mode_override="validation")
    kind: Literal["and", "or"]
    children: list[StoreExpression] = Field(min_length=1)


class StoreNot(Strict):
    model_config = ConfigDict(extra="forbid", frozen=True, json_schema_mode_override="validation")
    kind: Literal["not"] = "not"
    child: StoreExpression


StoreExpression = Annotated[StoreSelection | StoreBoolean | StoreNot, Field(discriminator="kind")]
StoreBoolean.model_rebuild()
StoreNot.model_rebuild()


class StoreFilterV1(Strict):
    semantic_dataset_version_id: UUID
    schema_version: Literal["store-filter/v1"] = "store-filter/v1"
    semantic_rule: Literal["authorized-store-set/v1"] = "authorized-store-set/v1"
    expression: StoreExpression


def semantic_expression(value: StoreExpression) -> dict[str, Any]:
    if value.kind == "store_in":
        return {"kind": value.kind, "field": value.field, "values": sorted(set(value.values))}
    if value.kind == "not":
        return {"kind": value.kind, "child": semantic_expression(value.child)}
    children = [semantic_expression(child) for child in value.children]
    return {
        "kind": value.kind,
        "children": sorted(children, key=lambda c: json.dumps(c, sort_keys=True)),
    }
