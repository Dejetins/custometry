"""Lossless adapter to the existing authorized Store-set provider.

Set operations are over provider-resolved dimension IDs, never business rows.
NOT complements only the authorized universe; mandatory source/system constraints
are intersected outside the expression. This is not a general filter evaluator.
"""

from __future__ import annotations
from collections.abc import Iterable
from uuid import UUID
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.semantic.store_filters import StoreExpression, StoreFilterV1


def selected_stores(expression: StoreExpression, universe: frozenset[str]) -> frozenset[str]:
    if expression.kind == "store_in":
        values = frozenset(expression.values)
        if not values <= universe:
            raise AnalyticsFailure("FORBIDDEN")
        return values
    if expression.kind == "not":
        return universe - selected_stores(expression.child, universe)
    # Validate every branch, including branches whose result is already determined.
    children = [selected_stores(child, universe) for child in expression.children]
    if expression.kind == "and":
        return universe.intersection(*children)
    return frozenset[str]().union(*children)


def resolve_store_filters(
    filters: Iterable[StoreFilterV1],
    *,
    allowed: frozenset[str],
    dataset_id: UUID,
    mandatory: Iterable[Iterable[str] | None],
) -> list[str]:
    effective = allowed
    for restriction in mandatory:
        if restriction is not None:
            selected = frozenset(restriction)
            if not selected <= allowed:
                raise AnalyticsFailure("FORBIDDEN")
            effective &= selected
    for expression in filters:
        if expression.semantic_dataset_version_id != dataset_id:
            raise AnalyticsFailure("COMPOSER_FILTER_DATASET_MISMATCH")
        effective &= selected_stores(expression.expression, allowed)
    return sorted(effective)
