"""Negative profile and current-access contracts complement real provider proof."""

from dataclasses import replace
from uuid import uuid4

import pytest

from custometry_api.analytics.filter_access import PublishedRetailFilterAccess
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import (
    FilterResourcePolicy,
    MaterializedFilterBinding,
)
from packages.contracts.identity.access import ResourceAccess
from packages.semantic_model.application.retail_filters import retail_filter_projection


def source():
    return {
        "summary": {"profile": "retail-report/v1", "namespace": "northwind-retail"},
        "capabilities": {"receipts": "available"},
        "publication_hash": "a" * 64,
        "bindings": [
            {
                "entity": "Receipt",
                "primary_key": ["source_system_id", "receipt_id"],
                "artifact_id": str(uuid4()),
                "content_hash": "b" * 64,
            }
        ],
    }


@pytest.mark.parametrize(
    "part,key,value",
    [
        ("summary", "profile", "unpublished-profile"),
        ("summary", "namespace", "multiple-sources"),
        ("capabilities", "receipts", "unavailable"),
    ],
)
def test_profile_cannot_infer_capabilities(part, key, value):
    payload = source()
    payload[part][key] = value
    with pytest.raises(AnalyticsFailure, match="FILTER_PROFILE_UNAVAILABLE"):
        retail_filter_projection(uuid4(), payload)


def test_binding_grain_and_publication_version():
    payload = source()
    dataset = uuid4()
    baseline = retail_filter_projection(dataset, payload)
    assert baseline == retail_filter_projection(dataset, payload)
    payload["publication_hash"] = "c" * 64
    assert (
        retail_filter_projection(dataset, payload).registry.version_id
        != baseline.registry.version_id
    )
    payload["bindings"][0]["primary_key"] = ["receipt_id"]
    with pytest.raises(AnalyticsFailure, match="FILTER_PROFILE_BINDING"):
        retail_filter_projection(dataset, payload)


def test_empty_current_row_universe_and_denial_before_catalog():
    workspace, actor, dataset = uuid4(), uuid4(), uuid4()
    published = retail_filter_projection(dataset, source())
    calls = []

    class Identity:
        decision = ResourceAccess(True, "a" * 64, (), frozenset({"analysis.read", "analysis.run"}))

        def resolve_resource(self, **kwargs):
            return self.decision

    class Semantic:
        def retail_filter_projection(self, **kwargs):
            calls.append("semantic")
            return published

    class Artifacts:
        def admit_filter_input(self, **kwargs):
            return MaterializedFilterBinding(**kwargs, relative_uri="objects/test.parquet")

    identity = Identity()
    policy = FilterResourcePolicy(
        version_id=uuid4(),
        max_rows=100,
        max_input_bytes=10000,
        max_nodes=20,
        max_depth=10,
        max_values=100,
        memory_mb=64,
        threads=1,
        timeout_ms=1000,
    )
    access = PublishedRetailFilterAccess(
        identity=identity, semantics=Semantic(), artifacts=Artifacts(), resource_policy=policy
    )
    grant = access.authorize(workspace_id=workspace, actor_id=actor, dataset_version_id=dataset)
    assert [child.operator for child in grant.row_ceiling.children] == [
        "eq",
        "is_null",
        "is_not_null",
    ]
    calls.clear()
    identity.decision = replace(identity.decision, permissions=frozenset({"analysis.read"}))
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        access.authorize(workspace_id=workspace, actor_id=actor, dataset_version_id=dataset)
    assert calls == []
