"""Explicit nullable-child relationship capability; the old DTO stays strict."""

from typing import Literal
from pydantic import Field, model_validator
from packages.contracts.semantic.filter_fields import Name
from packages.contracts.semantic.relationships import FilterRelationshipVersion


class NullableFilterRelationshipVersion(FilterRelationshipVersion):
    schema_version: Literal["nullable-filter-relationship/v1"] = "nullable-filter-relationship/v1"
    nullable_child_fields: tuple[Name, ...] = Field(min_length=1, max_length=4)
    null_policy: Literal["unlinked_all_nullable_keys_null/v1"] = (
        "unlinked_all_nullable_keys_null/v1"
    )

    @model_validator(mode="after")
    def nullable_keys(self):
        if len(set(self.nullable_child_fields)) != len(self.nullable_child_fields) or not set(
            self.nullable_child_fields
        ) <= set(self.child_fields):
            raise ValueError("FILTER_NULLABLE_RELATIONSHIP_KEYS")
        return self
