"""Real DuckDB facet authorization and vectorized membership selection."""
from dataclasses import replace
from uuid import uuid4

import pytest

from packages.analytics_core.infrastructure.retail_filter import PublishedReceiptFilter
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import FlatBoolean
from packages.contracts.analytics.retail_filter import FilterFacetQuery, ReceiptFilterInput
from tests.integration.analytics.test_columnar_filters import FlatSetup, setup as setup


def test_facets_apply_ceiling_before_counts_search_and_pagination(setup: FlatSetup) -> None:
    engine, access, request, _ = setup
    request = request.model_copy(update={"expression": access.grant.row_ceiling})
    first = engine.facets(request, FilterFacetQuery(field_id="label", limit=2), actor_id=access.grant.actor_id)
    assert [(v.value, v.count) for v in first.values] == [("first", 1), ("fourth", 1)]
    assert first.has_more
    second = engine.facets(request, FilterFacetQuery(field_id="label", limit=2, offset=2), actor_id=access.grant.actor_id)
    assert [(v.value, v.count) for v in second.values] == [("second", 1), (None, 1)]
    assert not second.has_more
    for search in ("hidden", "' OR true --", "%"):
        result = engine.facets(request, FilterFacetQuery(field_id="label", search=search), actor_id=access.grant.actor_id)
        assert result.values == []
    assert engine.facets(request, FilterFacetQuery(field_id="label", search="IRST"), actor_id=access.grant.actor_id).values[0].value == "first"


def test_facets_and_fingerprint_reject_versions_fields_and_revoke(setup: FlatSetup) -> None:
    engine, access, request, _ = setup
    with pytest.raises(AnalyticsFailure, match="FILTER_INPUT_BINDING"):
        engine.fingerprint(request.model_copy(update={"registry_version_id": uuid4()}), actor_id=access.grant.actor_id)
    with pytest.raises(AnalyticsFailure, match="FILTER_FIELD_FORBIDDEN"):
        engine.facets(request, FilterFacetQuery(field_id="secret"), actor_id=access.grant.actor_id)
    access.calls = 0
    access.revoke = True
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        engine.facets(request, FilterFacetQuery(field_id="label"), actor_id=access.grant.actor_id)


def test_receipt_projection_uses_real_engine_and_does_not_mutate_input(setup: FlatSetup) -> None:
    engine, access, request, _ = setup
    provider = PublishedReceiptFilter(engine)
    value = ReceiptFilterInput(registry_version_id=request.registry_version_id, expression=request.expression)
    inputs = {"Receipt": [{"receipt_id": name, "amount": amount} for name, amount in [("a", "1.01"), ("b", "1.02"), ("secret", "1.01")]], "Store": []}
    projected = provider.project(request.workspace_id, access.grant.actor_id, request.dataset_version_id, value, inputs)
    assert projected.inputs["Receipt"] == [{"receipt_id": "a", "amount": "1.01"}]
    assert len(inputs["Receipt"]) == 3
    assert projected.inputs["Store"] is inputs["Store"]


def test_filter_identity_pins_policy_and_canonical_boolean_order(setup: FlatSetup) -> None:
    engine, access, request, _ = setup
    children = (request.expression, access.grant.row_ceiling)
    left = request.model_copy(update={"expression": FlatBoolean(kind="and", children=children)})
    right = request.model_copy(update={"expression": FlatBoolean(kind="and", children=tuple(reversed(children)))})
    identity = engine.fingerprint(left, actor_id=access.grant.actor_id)
    assert identity == engine.fingerprint(right, actor_id=access.grant.actor_id)
    access.grant = replace(access.grant, policy_revision="changed")
    assert identity != engine.fingerprint(left, actor_id=access.grant.actor_id)
