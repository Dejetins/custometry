"""Strict provider binding and no invented business-history completeness."""

from dataclasses import replace
from uuid import uuid4
import pytest
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import MaterializedFilterBinding
from packages.contracts.analytics.relational_filters import RelationalResourcePolicy
from packages.contracts.identity.access import ResourceAccess
from packages.semantic_model.application.retail_relational import retail_relational_projection
from custometry_api.analytics.relational_access import PublishedRetailRelationalAccess
from tests.unit.semantic.test_retail_filters import source as flat_source


def source():
    value = flat_source()
    value["summary"].update(
        relationship_policy="retail-report-current-only/v1",
        relationships=[
            dict(
                parent="Receipt",
                child="ReceiptItem",
                cardinality="one_to_many",
                parent_key=["source_system_id", "receipt_id"],
                child_key=["source_system_id", "receipt_id"],
                nullable=False,
                policy="retail-report-current-only/v1",
            )
        ],
        quality_accounting=dict(
            transport_completeness="complete",
            business_history_completeness="unknown",
            quarantined_count=5,
        ),
    )
    value["bindings"].append(
        dict(
            entity="ReceiptItem",
            primary_key=["source_system_id", "receipt_id", "line_id"],
            artifact_id=str(uuid4()),
            content_hash="c" * 64,
        )
    )
    return value


def test_published_versions_and_completeness_never_inferred():
    value, dataset = source(), uuid4()
    baseline = retail_relational_projection(dataset, value)
    assert baseline == retail_relational_projection(dataset, value)
    assert baseline.relationships[0].complete is False
    value["summary"]["quality_accounting"]["business_history_completeness"] = "complete"
    changed = retail_relational_projection(dataset, value)
    assert changed.relationships[0].complete is False
    assert changed.relationships[0].completeness_hash != baseline.relationships[0].completeness_hash
    value["publication_hash"] = "d" * 64
    changed = retail_relational_projection(dataset, value)
    assert all(
        a.registry.version_id != b.registry.version_id
        for a, b in zip(baseline.entities, changed.entities)
    )
    assert (
        changed.relationships[0].relationship.version_id
        != baseline.relationships[0].relationship.version_id
    )
    fields = {f.column: f for f in changed.entities[1].registry.fields}
    assert fields["quantity"].decimal_scale == 3 and fields["unit_price"].decimal_scale == 2
    assert fields["product_id"].null_policy == "unknown"


@pytest.mark.parametrize(
    "mutation", ["missing", "duplicate", "keys", "policy", "nullable", "cardinality", "item_key"]
)
def test_invalid_published_relationship_fails_closed(mutation):
    value = source()
    relation = value["summary"]["relationships"][0]
    if mutation == "missing":
        value["summary"]["relationships"] = []
    elif mutation == "duplicate":
        value["summary"]["relationships"].append(dict(relation))
    elif mutation == "keys":
        relation["child_key"] = ["product_id"]
    elif mutation == "policy":
        relation["policy"] = "inferred"
    elif mutation == "nullable":
        relation["nullable"] = True
    elif mutation == "cardinality":
        relation["cardinality"] = "many_to_many"
    else:
        value["bindings"][1]["primary_key"] = ["line_id"]
    with pytest.raises(AnalyticsFailure, match="FILTER_RELATIONSHIP_BINDING"):
        retail_relational_projection(uuid4(), value)


def test_admission_rejects_mismatches_and_empty_store_universe():
    workspace, actor, dataset = uuid4(), uuid4(), uuid4()
    published = retail_relational_projection(dataset, source())
    calls = []

    class Identity:
        decision = ResourceAccess(True, "a" * 64, (), frozenset({"analysis.read", "analysis.run"}))

        def resolve_resource(self, **kwargs):
            return self.decision

    class Semantics:
        def retail_relational_projection(self, **kwargs):
            calls.append("semantic")
            return published

    class Artifacts:
        wrong = False

        def admit_filter_input(self, **kwargs):
            value = MaterializedFilterBinding(**kwargs, relative_uri="objects/test.parquet")
            return replace(value, workspace_id=uuid4()) if self.wrong else value

    policy = RelationalResourcePolicy(
        version_id=uuid4(),
        max_rows=100,
        max_input_bytes=10000,
        max_nodes=32,
        max_depth=12,
        max_values=100,
        memory_mb=64,
        threads=1,
        timeout_ms=1000,
        max_entities=2,
        max_correlations=4,
        max_fan_out=10,
        max_estimated_work=1000,
    )
    identity, artifacts = Identity(), Artifacts()
    access = PublishedRetailRelationalAccess(
        identity=identity, semantics=Semantics(), artifacts=artifacts, resource_policy=policy
    )

    def authorize():
        return access.authorize(workspace_id=workspace, actor_id=actor, dataset_version_id=dataset)

    grant = authorize()
    assert [c.operator for c in grant.entities[0].row_ceiling.children] == [
        "eq",
        "is_null",
        "is_not_null",
    ]
    artifacts.wrong = True
    with pytest.raises(AnalyticsFailure, match="FILTER_INPUT_BINDING"):
        authorize()
    calls.clear()
    identity.decision = replace(identity.decision, permissions=frozenset({"analysis.read"}))
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        authorize()
    assert calls == []
