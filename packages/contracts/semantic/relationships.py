"""Published relationship meaning; no client-selected joins or storage paths."""

from typing import Literal
from uuid import UUID
from pydantic import Field, model_validator
from packages.contracts.semantic import Strict
from packages.contracts.semantic.filter_fields import Name


class FilterRelationshipVersion(Strict):
    relationship_id: Name
    version_id: UUID
    parent_entity: Name
    child_entity: Name
    parent_fields: tuple[Name, ...] = Field(min_length=1, max_length=4)
    child_fields: tuple[Name, ...] = Field(min_length=1, max_length=4)
    cardinality: Literal["one_to_many"] = "one_to_many"
    policy_version_id: UUID
    observation_basis: Literal["published_snapshot"] = "published_snapshot"

    @model_validator(mode="after")
    def keys(self):
        if (
            len(self.parent_fields) != len(self.child_fields)
            or len(set(self.parent_fields)) != len(self.parent_fields)
            or len(set(self.child_fields)) != len(self.child_fields)
        ):
            raise ValueError("FILTER_RELATIONSHIP_KEYS")
        return self
