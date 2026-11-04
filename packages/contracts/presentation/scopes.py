"""Versioned provider-backed scopes with unchanged v1 Store semantics.

V2 adds published Receipt expressions, not the general relational filter language.
"""

from __future__ import annotations

from typing import Annotated, Literal, Any
from uuid import UUID
from pydantic import Field, model_validator, model_serializer, SerializerFunctionWrapHandler
from packages.contracts.semantic import Strict, CalendarRef, Hash
from packages.contracts.analytics.workspace import (
    Period,
    Grain,
    CalendarBasis,
    WorkspaceRunRequest,
)

from packages.contracts.semantic.store_filters import StoreFilterV1
from packages.contracts.analytics.receipt_selection import ReceiptSelection
from packages.contracts.analytics.temporal import TemporalSettingsV2


class ScopeTarget(Strict):
    kind: Literal["document", "chapter", "page", "section", "block"]
    id: UUID


ContextField = Literal["period", "grain", "calendar_ref", "calendar_basis", "alignment", "time_comparison"]


class ContextOverride(Strict):
    time_comparison: TemporalSettingsV2 | None = None

    @model_serializer(mode="wrap")
    def preserve_old_comparison(self, handler: SerializerFunctionWrapHandler):
        value: dict[str, Any] = handler(self)
        if "time_comparison" not in self.model_fields_set:
            value.pop("time_comparison", None)
        return value

    period: Period | None = None
    grain: Grain | None = None
    calendar_ref: CalendarRef | None = None
    calendar_basis: CalendarBasis | None = None
    alignment: Literal["none", "previous_year_same_dates"] | None = None

    @model_validator(mode="after")
    def nonempty(self) -> ContextOverride:
        if self.time_comparison is not None and self.alignment not in (None, "none"):
            raise ValueError("COMPARISON_CONTRACT_CONFLICT")
        if not any(getattr(self, key) is not None for key in type(self).model_fields):
            raise ValueError("COMPOSER_EMPTY_CONTEXT_OVERRIDE")
        return self


class ContextScopeBinding(Strict):
    binding_id: UUID
    target: ScopeTarget
    context: ContextOverride
    locked_fields: list[ContextField] = Field(default_factory=lambda: list[ContextField]())

    @model_validator(mode="after")
    def locks_have_values(self) -> ContextScopeBinding:
        if len(set(self.locked_fields)) != len(self.locked_fields) or any(
            getattr(self.context, key) is None for key in self.locked_fields
        ):
            raise ValueError("COMPOSER_INVALID_CONTEXT_LOCK")
        return self


class FilterScopeBinding(Strict):
    binding_id: UUID
    target: ScopeTarget
    order: Annotated[int, Field(strict=True, ge=0)]
    filter: StoreFilterV1
    combine_mode: Literal["intersect", "replace_allowed_parent_field"] = "intersect"
    replaces: list[UUID] = Field(default_factory=lambda: list[UUID]())
    replaceable: bool = Field(default=False, strict=True)
    locked: bool = Field(default=False, strict=True)
    linked_target_block_ids: list[UUID] = Field(default_factory=lambda: list[UUID]())

    @model_validator(mode="after")
    def explicit_replacement(self) -> FilterScopeBinding:
        if bool(self.replaces) != (self.combine_mode == "replace_allowed_parent_field"):
            raise ValueError("COMPOSER_INVALID_SCOPE_REPLACEMENT")
        if self.locked and self.replaceable:
            raise ValueError("COMPOSER_LOCKED_SCOPE_NOT_REPLACEABLE")
        if len(set(self.replaces)) != len(self.replaces) or len(
            set(self.linked_target_block_ids)
        ) != len(self.linked_target_block_ids):
            raise ValueError("COMPOSER_DUPLICATE_SCOPE_REFERENCE")
        if self.replaces and self.linked_target_block_ids:
            raise ValueError("COMPOSER_LINKED_REPLACEMENT_UNSUPPORTED")
        return self


class ComposerScopesV1(Strict):
    schema_version: Literal["composer-scopes/v1"] = "composer-scopes/v1"
    filters: list[FilterScopeBinding] = Field(default_factory=lambda: list[FilterScopeBinding]())
    contexts: list[ContextScopeBinding] = Field(default_factory=lambda: list[ContextScopeBinding]())

    @model_validator(mode="after")
    def unique_bindings(self) -> ComposerScopesV1:
        ids = [b.binding_id for b in [*self.filters, *self.contexts]]
        if len(ids) != len(set(ids)):
            raise ValueError("COMPOSER_DUPLICATE_SCOPE_BINDING")
        targets = [(b.target.kind, b.target.id) for b in self.contexts]
        if len(targets) != len(set(targets)):
            raise ValueError("COMPOSER_DUPLICATE_CONTEXT_TARGET")
        positions = [(b.target.kind, b.target.id, b.order) for b in self.filters]
        if len(positions) != len(set(positions)):
            raise ValueError("COMPOSER_DUPLICATE_SCOPE_ORDER")
        return self


class ReceiptScopeBinding(Strict):
    binding_id: UUID
    target: ScopeTarget
    order: Annotated[int, Field(strict=True, ge=0)]
    semantic_dataset_version_id: UUID
    filter: ReceiptSelection
    combine_mode: Literal["intersect", "replace_allowed_parent_field"] = "intersect"
    replaces: list[UUID] = Field(default_factory=lambda: list[UUID]())
    replaceable: bool = Field(default=False, strict=True)
    locked: bool = Field(default=False, strict=True)
    linked_target_block_ids: list[UUID] = Field(default_factory=lambda: list[UUID]())

    @model_validator(mode="after")
    def explicit_replacement(self) -> ReceiptScopeBinding:
        if bool(self.replaces) != (self.combine_mode == "replace_allowed_parent_field"):
            raise ValueError("COMPOSER_INVALID_SCOPE_REPLACEMENT")
        if self.locked and self.replaceable:
            raise ValueError("COMPOSER_LOCKED_SCOPE_NOT_REPLACEABLE")
        if len(set(self.replaces)) != len(self.replaces) or len(
            set(self.linked_target_block_ids)
        ) != len(self.linked_target_block_ids):
            raise ValueError("COMPOSER_DUPLICATE_SCOPE_REFERENCE")
        if self.replaces and self.linked_target_block_ids:
            raise ValueError("COMPOSER_LINKED_REPLACEMENT_UNSUPPORTED")
        return self


class ComposerScopesV2(Strict):
    schema_version: Literal["composer-scopes/v2"] = "composer-scopes/v2"
    filters: list[FilterScopeBinding] = Field(default_factory=lambda: list[FilterScopeBinding]())
    receipt_filters: list[ReceiptScopeBinding] = Field(default_factory=lambda: list[ReceiptScopeBinding](), max_length=1000)
    contexts: list[ContextScopeBinding] = Field(default_factory=lambda: list[ContextScopeBinding]())

    @model_validator(mode="after")
    def unique_bindings(self) -> ComposerScopesV2:
        ids = [b.binding_id for b in [*self.filters, *self.receipt_filters, *self.contexts]]
        if len(ids) != len(set(ids)):
            raise ValueError("COMPOSER_DUPLICATE_SCOPE_BINDING")
        targets = [(b.target.kind, b.target.id) for b in self.contexts]
        if len(targets) != len(set(targets)):
            raise ValueError("COMPOSER_DUPLICATE_CONTEXT_TARGET")
        positions = [
            (b.target.kind, b.target.id, b.order) for b in [*self.filters, *self.receipt_filters]
        ]
        if len(positions) != len(set(positions)):
            raise ValueError("COMPOSER_DUPLICATE_SCOPE_ORDER")
        return self


ComposerScopes = Annotated[
    ComposerScopesV1 | ComposerScopesV2, Field(discriminator="schema_version")
]


def scope_filter_bindings(scopes: ComposerScopes) -> list[FilterScopeBinding | ReceiptScopeBinding]:
    return [
        *scopes.filters,
        *(scopes.receipt_filters if isinstance(scopes, ComposerScopesV2) else []),
    ]


class ScopeOrigin(Strict):
    binding_id: UUID
    target: ScopeTarget
    field: ContextField | Literal["Store.store_id", "Receipt"]
    state: Literal["applied", "overridden", "locked", "linked"]
    overridden_by: UUID | None = None


class ResolvedComposerScope(Strict):
    schema_version: Literal["resolved-composer-scope/v1"] = "resolved-composer-scope/v1"
    block_id: UUID
    query: WorkspaceRunRequest
    filters: list[StoreFilterV1]
    origins: list[ScopeOrigin]
    dependency_hash: Hash | None
