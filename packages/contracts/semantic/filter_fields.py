"""Published flat filter field projection; not the complete relational registry."""

from __future__ import annotations

from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, model_validator

from packages.contracts.semantic import Strict

Name = Annotated[str, Field(min_length=1, max_length=128)]
Operator = Literal["eq", "ne", "lt", "le", "gt", "ge", "in", "is_null", "is_not_null"]
DataType = Literal["string", "integer", "decimal", "boolean", "date"]


class FilterFieldVersion(Strict):
    field_id: Name
    version_id: UUID
    entity: Name
    column: Name
    data_type: DataType
    operators: tuple[Operator, ...] = Field(min_length=1)
    null_policy: Literal["not_matched", "unknown"]
    # A provider-owned Boolean observation column; NULL/false means unavailable.
    known_column: Name | None = None
    decimal_precision: Annotated[int, Field(strict=True, ge=1, le=38)] = 18
    decimal_scale: Annotated[int, Field(strict=True, ge=0, le=38)] = 2

    @model_validator(mode="after")
    def consistent_decimal(self) -> FilterFieldVersion:
        if self.decimal_scale > self.decimal_precision:
            raise ValueError("FILTER_FIELD_DECIMAL_SCALE")
        if len(set(self.operators)) != len(self.operators):
            raise ValueError("FILTER_FIELD_DUPLICATE_OPERATOR")
        return self


class FlatFilterRegistry(Strict):
    schema_version: Literal["flat-filter-registry/v1"] = "flat-filter-registry/v1"
    version_id: UUID
    dataset_version_id: UUID
    entity: Name
    fields: tuple[FilterFieldVersion, ...] = Field(min_length=1, max_length=256)

    @model_validator(mode="after")
    def unique_fields(self) -> FlatFilterRegistry:
        if len({f.field_id for f in self.fields}) != len(self.fields):
            raise ValueError("FILTER_REGISTRY_DUPLICATE_FIELD")
        if any(f.entity != self.entity for f in self.fields):
            raise ValueError("FILTER_REGISTRY_SCOPE_MISMATCH")
        return self
