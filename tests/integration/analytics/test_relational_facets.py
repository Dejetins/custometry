"""Facet grain/ceilings before aggregation over real admitted Parquet and DuckDB."""

from dataclasses import replace
from uuid import uuid4
import pytest
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.retail_relational import RelationalFacetQuery
from tests.integration.analytics.test_relational_filters import (
    RelationalSetup,
    setup as setup,
    request,
    predicate,
)


def test_facets_root_membership_child_ceiling_search_and_pagination(setup: RelationalSetup):
    engine, access, _, actor, _, _ = setup
    q = request(setup)
    root = engine.facets(
        q, RelationalFacetQuery(entity="Receipt", field_id="Receipt.id"), actor_id=actor
    )
    assert [(v.value, v.count) for v in root.values] == [("b", 1)]
    assert root.count_grain == "matching_receipts"
    # Root universe is authorized a,b,c,n; secret root is excluded. The hidden
    # item at c is also excluded by its independent mandatory child ceiling.
    q = q.model_copy(
        update={"expression": predicate(access.grant, q.root_scope_id, "Receipt.allowed", True)}
    )
    query = RelationalFacetQuery(entity="ReceiptItem", field_id="ReceiptItem.color", limit=2)
    first = engine.facets(q, query, actor_id=actor)
    assert [(v.value, v.count) for v in first.values] == [("blue", 1), ("red", 2)]
    assert first.has_more and first.count_grain == "observed_items_in_matching_receipts"
    last = engine.facets(q, query.model_copy(update={"offset": 2}), actor_id=actor)
    assert [(v.value, v.count) for v in last.values] == [(None, 1)] and not last.has_more
    for search in ("' OR true --", "%", "secret"):
        assert (
            engine.facets(q, query.model_copy(update={"search": search}), actor_id=actor).values
            == []
        )
    assert (
        engine.facets(q, query.model_copy(update={"search": "RED"}), actor_id=actor).values[0].count
        == 2
    )


def test_facets_current_grant_and_binding_limits(setup: RelationalSetup):
    engine, access, _, actor, _, _ = setup
    q = request(setup)
    facet = RelationalFacetQuery(entity="ReceiptItem", field_id="ReceiptItem.color")
    with pytest.raises(AnalyticsFailure, match="FILTER_FIELD_FORBIDDEN"):
        engine.facets(q, facet.model_copy(update={"field_id": "Receipt.id"}), actor_id=actor)
    with pytest.raises(AnalyticsFailure, match="FILTER_COMPATIBILITY_REGISTRY_BINDING"):
        engine.execute(
            q.model_copy(update={"compatibility_registry_version_id": uuid4()}), actor_id=actor
        )
    access.calls = 0
    access.changed = True
    with pytest.raises(AnalyticsFailure, match="FILTER_POLICY_CHANGED"):
        engine.facets(q, facet, actor_id=actor)
    access.changed = False
    access.grant = replace(
        access.grant,
        resource_policy=access.grant.resource_policy.model_copy(update={"max_estimated_work": 1}),
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_WORK_LIMIT"):
        engine.facets(q, facet, actor_id=actor)
