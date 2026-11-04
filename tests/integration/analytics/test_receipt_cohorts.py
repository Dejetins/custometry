"""Actual Parquet/DuckDB receipt membership and global compiler boundary proof."""

from contextlib import contextmanager
from dataclasses import replace
import hashlib
import json
from uuid import UUID, uuid4
from typing import Any, Generator, TypeVar, cast
import pyarrow as _pa  # pyright: ignore[reportMissingTypeStubs]
import pyarrow.parquet as _pq  # pyright: ignore[reportMissingTypeStubs]
import pytest
from pydantic import BaseModel, ValidationError
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.receipt_cohorts import (
    ReceiptCohortGrant,
    CohortExpression,
    CohortFilterRequest,
    CustomerEventMembership,
    CohortBoolean,
    CohortNot,
)
from packages.contracts.analytics.customer_events import ObservedChildRootRestriction
from packages.contracts.analytics.sequence_filters import (
    BehavioralSequence,
    PositiveStep,
    NegativeStep,
    FixedSequenceWindow,
    SequenceGap,
)
from packages.contracts.analytics.relational_filters import (
    RelationalFilterRequest,
    RelationalFilterResult,
    RelationalResourcePolicy,
)
from packages.contracts.analytics.columnar_filters import MaterializedFilterBinding
from packages.contracts.analytics.aggregate_filters import AggregateFilterRequest
from packages.contracts.analytics.retail_relational import RelationalFacetQuery
from packages.contracts.semantic.nullable_relationships import NullableFilterRelationshipVersion
from packages.analytics_core.infrastructure import relational_filters as runtime
from tests.integration.analytics.test_sequence_filters import (
    setup as sequence_setup,  # pyright: ignore[reportUnusedImport]  # noqa: F401 -- fixture registration
    at,
    change_column,
)  # noqa: F401
from tests.integration.analytics.test_relational_filters import FilterSetup, predicate
from tests.integration.analytics.test_relational_filters import setup as relational_setup  # pyright: ignore[reportUnusedImport]  # noqa: F401


pa: Any = _pa
pq: Any = _pq
CohortSetup = FilterSetup[ReceiptCohortGrant]
ModelT = TypeVar("ModelT", bound=BaseModel)


def renamed(model: ModelT) -> ModelT:
    raw = (
        model.model_dump_json()
        .replace("ReceiptItem", "TEMP")
        .replace("Receipt", "Customer")
        .replace("TEMP", "Receipt")
    )
    return type(model).model_validate_json(raw)


@pytest.fixture
def setup(request: pytest.FixtureRequest) -> CohortSetup:
    base = cast(CohortSetup, request.getfixturevalue("sequence_setup"))
    access = base[1]
    old = access.grant
    entities = tuple(
        replace(
            e,
            registry=renamed(e.registry),
            row_ceiling=renamed(e.row_ceiling),
            binding=replace(
                cast(MaterializedFilterBinding, e.binding),
                entity="Customer" if i == 0 else "Receipt",
            ),
        )
        for i, e in enumerate(old.entities)
    )
    edge = renamed(old.relationships[0].relationship)
    edge = NullableFilterRelationshipVersion.model_validate(
        edge.model_dump() | {"nullable_child_fields": ["Receipt.parent"]}
    )
    access.grant = ReceiptCohortGrant(
        entities=entities,
        relationships=(replace(old.relationships[0], relationship=edge),),
        resource_policy=old.resource_policy,
        events=(replace(old.events[0], definition=renamed(old.events[0].definition)),),
        receipt_registry_versions=(("Receipt", uuid4()),),
        facet_fields=tuple(
            ("Receipt", f.field_id) for f in entities[1].registry.fields if f.column != "parent"
        ),
        root_restrictions=(
            ObservedChildRootRestriction(
                version_id=uuid4(),
                root_entity="Customer",
                relationship_id=edge.relationship_id,
                relationship_version_id=edge.version_id,
            ),
        ),
    )
    return base


def member(
    setup: CohortSetup, scope: UUID | None = None, negative: bool = False
) -> CustomerEventMembership:
    grant = setup[1].grant
    scope, customer = scope or uuid4(), uuid4()
    edge = grant.relationships[0].relationship

    def step(color: str, gap: SequenceGap | None = None) -> PositiveStep:
        child = uuid4()
        return PositiveStep(
            step_id=uuid4(),
            child_scope_id=child,
            event=grant.events[0].definition,
            predicate=predicate(grant, child, "Receipt.color", color),
            gap=gap,
        )

    first = step("red")
    second: PositiveStep | NegativeStep = step("blue", SequenceGap(maximum_us=2000000))
    if negative:
        second = NegativeStep(
            step_id=second.step_id,
            child_scope_id=second.child_scope_id,
            event=second.event,
            predicate=second.predicate,
            after_step_id=first.step_id,
            ends_after_us=2000000,
        )
    sequence = BehavioralSequence(
        node_id=uuid4(),
        scope_id=customer,
        parent_scope_id=customer,
        relationship_id=edge.relationship_id,
        relationship_version_id=edge.version_id,
        child_entity="Receipt",
        window=FixedSequenceWindow(
            starts_at=at(0), ends_at=at(10), observation_as_of=at(10), knowledge_as_of=at(11)
        ),
        steps=(first, second),
    )
    return CustomerEventMembership(
        node_id=uuid4(),
        scope_id=scope,
        customer_scope_id=customer,
        relationship_id=edge.relationship_id,
        relationship_version_id=edge.version_id,
        predicate=sequence,
    )


def query(setup: CohortSetup, node: CohortExpression) -> CohortFilterRequest:
    _, access, workspace, _, dataset, _ = setup
    return CohortFilterRequest(
        workspace_id=workspace,
        dataset_version_id=dataset,
        root_scope_id=node.scope_id,
        registry_versions={e.registry.entity: e.registry.version_id for e in access.grant.entities},
        receipt_registry_versions=dict(access.grant.receipt_registry_versions),
        expression=node,
    )


def run(setup: CohortSetup, node: CohortExpression) -> RelationalFilterResult:
    return setup[0].execute(query(setup, node), actor_id=setup[3])


def test_receipts_share_customer_membership_without_multiplication(setup: CohortSetup):
    result = run(setup, member(setup))
    assert result.matched_ids == ("a1", "a2")
    assert result.authorized_count == 5
    assert result.not_matched_count == 2
    assert result.unknown_count == 1  # forbidden customer; a lone event cannot form two steps


def test_receipt_outside_history_window_is_still_selected(setup: CohortSetup):
    child = setup[1].grant.entities[1]
    path = setup[-1] / child.binding.relative_uri
    table = pq.read_table(path)
    extra = pa.Table.from_pylist(
        [dict(table.slice(0, 1).to_pylist()[0], id="a3", time=at(20))], schema=table.schema
    )
    pq.write_table(pa.concat_tables([table, extra]), path)
    setup[1].grant = replace(
        setup[1].grant,
        entities=(
            setup[1].grant.entities[0],
            replace(
                child,
                binding=replace(
                    child.binding, content_hash=hashlib.sha256(path.read_bytes()).hexdigest()
                ),
            ),
        ),
    )
    assert run(setup, member(setup)).matched_ids == ("a1", "a2", "a3")


def test_anonymous_not_is_unknown_and_orphan_is_failure(setup: CohortSetup):
    change_column(setup, "parent", ["a", "a", "b", None, "secret", "c"])
    node = member(setup)
    result = run(setup, CohortNot(node_id=uuid4(), scope_id=node.scope_id, child=node))
    assert result.matched_ids == ("b1",)
    assert result.unknown_count == 2
    change_column(setup, "parent", ["a", "a", "b", "orphan", "secret", "c"])
    with pytest.raises(AnalyticsFailure, match="FILTER_RELATIONSHIP_KEYS"):
        run(setup, node)


def test_forbidden_events_do_not_confirm_customer(setup: CohortSetup):
    change_column(setup, "allowed", [True, False, True, True, True, False])
    assert run(setup, member(setup)).matched_ids == ()


def test_negative_and_multiple_materialized_cohorts(setup: CohortSetup):
    node = member(setup, negative=True)
    assert run(setup, node).matched_ids == ("b1",)
    other = member(setup, node.scope_id)
    combined = CohortBoolean(
        kind="or", node_id=uuid4(), scope_id=node.scope_id, children=(node, other)
    )
    assert run(setup, combined).matched_ids == ("a1", "a2", "b1")


def test_main_parameters_before_cohort_in_tree_and_facets(setup: CohortSetup):
    node = member(setup)
    pred = predicate(setup[1].grant, node.scope_id, "Receipt.color", "red")
    combined = CohortBoolean(
        kind="and", node_id=uuid4(), scope_id=node.scope_id, children=(pred, node)
    )
    assert run(setup, combined).matched_ids == ("a1",)
    result = setup[0].facets(
        query(setup, combined),
        RelationalFacetQuery(
            entity="Receipt", field_id="Receipt.color", search="re", limit=1, offset=0
        ),
        actor_id=setup[3],
    )
    assert [(v.value, v.count) for v in result.values] == [("red", 1)]


def test_actual_duckdb_plan_materializes_each_customer_leaf(
    setup: CohortSetup, monkeypatch: pytest.MonkeyPatch
):
    original = runtime.isolated_connection
    plans: list[Any] = []

    @contextmanager
    def capture(policy: RelationalResourcePolicy) -> Generator[Any, None, None]:
        with original(policy) as connection:

            class Connection:
                def __getattr__(self, name: str) -> Any:
                    return getattr(connection, name)

                def execute(self, sql: str, parameters: Any = None) -> Any:
                    if sql.startswith("WITH cohort_"):
                        row = connection.execute(
                            "EXPLAIN (FORMAT JSON) " + sql, parameters
                        ).fetchone()
                        assert row is not None
                        plans.append(json.loads(row[1]))
                    return (
                        connection.execute(sql, parameters)
                        if parameters is not None
                        else connection.execute(sql)
                    )

            yield Connection()

    monkeypatch.setattr(runtime, "isolated_connection", capture)
    node = member(setup)
    second = member(setup, node.scope_id, negative=True)
    run(
        setup,
        CohortBoolean(kind="or", node_id=uuid4(), scope_id=node.scope_id, children=(node, second)),
    )

    def walk(nodes: Any) -> Generator[Any, None, None]:
        for n in nodes:
            yield n
            yield from walk(n.get("children", []))

    ctes = [
        n
        for n in walk(plans[0])
        if n["name"] == "CTE" and n["extra_info"].get("CTE Name", "").startswith("cohort_")
    ]
    assert sorted(n["extra_info"]["CTE Name"] for n in ctes) == ["cohort_0", "cohort_1"]
    assert sum(n["name"] == "CTE_SCAN" for n in walk(plans[0])) >= 2


@pytest.mark.parametrize("collision", ["node", "scope", "step"])
def test_cross_leaf_identifiers_cannot_collide(setup: CohortSetup, collision: str):
    node = member(setup)
    other = member(setup, node.scope_id)
    if collision == "node":
        other = other.model_copy(
            update={
                "predicate": other.predicate.model_copy(update={"node_id": node.predicate.node_id})
            }
        )
    elif collision == "scope":
        other = other.model_copy(update={"customer_scope_id": node.customer_scope_id})
    else:
        steps = (
            cast(BehavioralSequence, other.predicate)
            .steps[0]
            .model_copy(
                update={"step_id": cast(BehavioralSequence, node.predicate).steps[0].step_id}
            ),
            cast(BehavioralSequence, other.predicate).steps[1],
        )
        other = other.model_copy(
            update={"predicate": other.predicate.model_copy(update={"steps": steps})}
        )
    with pytest.raises(AnalyticsFailure, match="FILTER_SCOPE_INVALID"):
        run(
            setup,
            CohortBoolean(
                kind="or", node_id=uuid4(), scope_id=node.scope_id, children=(node, other)
            ),
        )


@pytest.mark.parametrize(
    "key,value",
    [
        ("max_nodes", 10),
        ("max_correlations", 7),
        ("max_values", 25),
        ("max_depth", 3),
        ("max_estimated_work", 50),
    ],
)
def test_multiple_leaves_obey_global_limits(setup: CohortSetup, key: str, value: int):
    node = member(setup)
    other = member(setup, node.scope_id)
    setup[1].grant = replace(
        setup[1].grant,
        resource_policy=setup[1].grant.resource_policy.model_copy(update={key: value}),
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_(PLAN|WORK|SEQUENCE_WORK)_LIMIT"):
        run(
            setup,
            CohortBoolean(
                kind="or", node_id=uuid4(), scope_id=node.scope_id, children=(node, other)
            ),
        )


def test_promoted_registry_pins_validated_and_in_identity(setup: CohortSetup):
    node = member(setup)
    q = query(setup, node)
    before = setup[0].fingerprint(q, actor_id=setup[3])
    promoted = q.model_copy(update={"promoted_registry_sets": (q.receipt_registry_versions,)})
    assert setup[0].fingerprint(promoted, actor_id=setup[3]) != before
    for update in (
        {"receipt_registry_versions": {"Receipt": uuid4()}},
        {"promoted_registry_sets": ({"Receipt": uuid4()},)},
    ):
        with pytest.raises(AnalyticsFailure, match="FILTER_COHORT_REGISTRY_BRIDGE"):
            setup[0].fingerprint(q.model_copy(update=update), actor_id=setup[3])


def test_current_authorization_rechecked(setup: CohortSetup):
    setup[1].changed = True
    with pytest.raises(AnalyticsFailure, match="FILTER_POLICY_CHANGED"):
        run(setup, member(setup))


@pytest.mark.parametrize("reader", [RelationalFilterRequest, AggregateFilterRequest])
def test_old_execution_readers_reject_cohort_node(
    setup: CohortSetup, reader: type[RelationalFilterRequest] | type[AggregateFilterRequest]
):
    q = query(setup, member(setup)).model_dump(
        exclude={"receipt_registry_versions", "promoted_registry_sets", "schema_version"}
    )
    with pytest.raises(ValidationError):
        reader.model_validate(q)


def test_sequence_and_materialization_work_are_charged_together(setup: CohortSetup):
    node = member(setup)
    other = member(setup, node.scope_id)
    setup[1].grant = replace(
        setup[1].grant,
        resource_policy=setup[1].grant.resource_policy.model_copy(
            update={"max_estimated_work": 100}
        ),
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_SEQUENCE_WORK_LIMIT"):
        run(
            setup,
            CohortBoolean(
                kind="or", node_id=uuid4(), scope_id=node.scope_id, children=(node, other)
            ),
        )


def test_facet_parameters_share_the_query_budget(setup: CohortSetup):
    node = member(setup)
    q = query(setup, node)
    compiled = runtime.Compiler(q, setup[3], setup[1].grant)
    cap = len(compiled.parameters) + len(compiled.prelude_parameters)
    setup[1].grant = replace(
        setup[1].grant,
        resource_policy=setup[1].grant.resource_policy.model_copy(update={"max_values": cap}),
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_PLAN_LIMIT"):
        setup[0].facets(
            q,
            RelationalFacetQuery(
                entity="Receipt", field_id="Receipt.color", search="x", limit=1, offset=0
            ),
            actor_id=setup[3],
        )


def test_customer_reference_is_not_a_receipt_facet(setup: CohortSetup):
    with pytest.raises(AnalyticsFailure, match="FILTER_FIELD_FORBIDDEN"):
        setup[0].facets(
            query(setup, member(setup)),
            RelationalFacetQuery(entity="Receipt", field_id="Receipt.parent", limit=10),
            actor_id=setup[3],
        )
