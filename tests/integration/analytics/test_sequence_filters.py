"""Real native UTC Parquet/DuckDB sequence proof with trusted synthetic admission."""

from dataclasses import replace
from datetime import datetime, UTC, timedelta
from uuid import UUID, uuid4
from typing import Any, TypeVar, cast
import hashlib
import pytest
import pyarrow as _pa  # pyright: ignore[reportMissingTypeStubs]
import pyarrow.parquet as _pq  # pyright: ignore[reportMissingTypeStubs]
from pydantic import ValidationError
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.sequence_filters import (
    SequenceFilterRequest,
    SequenceExpression,
    SequenceInputGrant,
    EventInput,
    BehavioralSequence,
    PositiveStep,
    NegativeStep,
    SequenceGap,
    FixedSequenceWindow,
    RelativeSequenceWindow,
    SequencePropertyBinding,
    SequenceNot,
    SequenceBoolean,
    canonical_sequence_expression,
)
from packages.contracts.analytics.aggregate_filters import AggregateFilterRequest
from packages.contracts.analytics.relational_filters import (
    RelationalFilterRequest,
    RelationalFilterResult,
)
from packages.contracts.semantic.filter_events import (
    EventTimeFieldVersion,
    FilterEventVersion,
    EventObservation,
)
from packages.contracts.semantic.filter_aggregates import AggregateFieldRef
from tests.integration.analytics.test_relational_filters import FilterSetup, predicate
from tests.integration.analytics.test_relational_filters import setup as relational_setup  # pyright: ignore[reportUnusedImport]  # noqa: F401

pa: Any = _pa
pq: Any = _pq
SequenceSetup = FilterSetup[SequenceInputGrant]
SequenceGrantT = TypeVar("SequenceGrantT", bound=SequenceInputGrant)

T = datetime(2025, 1, 1, tzinfo=UTC)


def at(seconds: int) -> datetime:
    return T + timedelta(seconds=seconds)


@pytest.fixture
def setup(request: pytest.FixtureRequest) -> SequenceSetup:
    base = cast(SequenceSetup, request.getfixturevalue("relational_setup"))
    _, access, _, _, _, root = base
    child = access.grant.entities[1]
    path = root / child.binding.relative_uri
    table = pq.read_table(path)
    table = table.append_column(
        "time", pa.array([at(1), at(2), at(1), at(1), at(1), at(1)], pa.timestamp("us", tz="UTC"))
    )
    table = table.append_column("time_known", pa.array([True] * 6))
    pq.write_table(table, path)
    child = replace(
        child,
        binding=replace(child.binding, content_hash=hashlib.sha256(path.read_bytes()).hexdigest()),
    )
    relation = access.grant.relationships[0]
    definition = FilterEventVersion(
        event_id="item.observed",
        version_id=uuid4(),
        entity="ReceiptItem",
        relationship_version_id=relation.relationship.version_id,
        time_field=EventTimeFieldVersion(
            field_id="ReceiptItem.event_time",
            version_id=uuid4(),
            entity="ReceiptItem",
            column="time",
            known_column="time_known",
        ),
    )
    event = EventInput(
        definition,
        EventObservation(
            starts_at=at(0), ends_at=at(10), observation_as_of=at(10), knowledge_as_of=at(11)
        ),
        True,
        "e" * 64,
    )
    access.grant = SequenceInputGrant(
        entities=(access.grant.entities[0], child),
        relationships=access.grant.relationships,
        resource_policy=access.grant.resource_policy,
        events=(event,),
    )
    return base


def step(
    setup: FilterSetup[SequenceGrantT],
    scope: UUID,
    color: str = "red",
    gap: SequenceGap | None = None,
) -> PositiveStep:
    grant = setup[1].grant
    child = uuid4()
    return PositiveStep(
        step_id=uuid4(),
        child_scope_id=child,
        event=grant.events[0].definition,
        predicate=predicate(grant, child, "ReceiptItem.color", color),
        gap=gap,
    )


def sequence(setup: FilterSetup[SequenceGrantT], *, single: bool = False) -> BehavioralSequence:
    grant = setup[1].grant
    scope = uuid4()
    first = step(setup, scope)
    steps = (
        (first,) if single else (first, step(setup, scope, "blue", SequenceGap(maximum_us=2000000)))
    )
    r = grant.relationships[0].relationship
    return BehavioralSequence(
        node_id=uuid4(),
        scope_id=scope,
        parent_scope_id=scope,
        relationship_id=r.relationship_id,
        relationship_version_id=r.version_id,
        child_entity="ReceiptItem",
        window=FixedSequenceWindow(
            starts_at=at(0), ends_at=at(10), observation_as_of=at(10), knowledge_as_of=at(11)
        ),
        steps=steps,
    )


def run(setup: FilterSetup[SequenceGrantT], node: SequenceExpression) -> RelationalFilterResult:
    engine, access, w, a, d, _ = setup
    return engine.execute(
        SequenceFilterRequest(
            workspace_id=w,
            dataset_version_id=d,
            root_entity="Receipt",
            root_scope_id=node.scope_id,
            registry_versions={
                e.registry.entity: e.registry.version_id for e in access.grant.entities
            },
            expression=node,
        ),
        actor_id=a,
    )


def change_column(
    setup: FilterSetup[SequenceGrantT], column: str, values: list[Any], dtype: Any = None
) -> None:
    access = setup[1]
    e = access.grant.entities[1]
    p = setup[-1] / e.binding.relative_uri
    t = pq.read_table(p)
    i = t.schema.get_field_index(column)
    t = t.set_column(i, column, pa.array(values, type=dtype or t.schema.field(i).type))
    pq.write_table(t, p)
    access.grant = replace(
        access.grant,
        entities=(
            access.grant.entities[0],
            replace(
                e,
                binding=replace(e.binding, content_hash=hashlib.sha256(p.read_bytes()).hexdigest()),
            ),
        ),
    )


def negative(
    setup: FilterSetup[SequenceGrantT],
    node: BehavioralSequence,
    color: str = "blue",
    end: int = 2000000,
) -> NegativeStep:
    p = step(setup, node.scope_id, color)
    return NegativeStep(
        step_id=p.step_id,
        child_scope_id=p.child_scope_id,
        event=p.event,
        predicate=p.predicate,
        after_step_id=node.steps[0].step_id,
        ends_after_us=end,
    )


def test_positive_order_and_hidden_roots(setup: SequenceSetup):
    result = run(setup, sequence(setup))
    assert result.matched_ids == ("a",)
    assert result.authorized_count == 4
    assert result.unknown_count == 0


@pytest.mark.parametrize("second", [at(1), at(0), at(4)])
def test_equal_reverse_or_beyond_gap_never_order(setup: SequenceSetup, second: datetime):
    change_column(setup, "time", [at(1), second, at(1), at(1), at(1), at(1)])
    assert run(setup, sequence(setup)).matched_ids == ()


def test_exact_microsecond_gap(setup: SequenceSetup):
    change_column(
        setup, "time", [at(1), at(1) + timedelta(microseconds=1), at(1), at(1), at(1), at(1)]
    )
    node = sequence(setup)
    second = node.steps[1].model_copy(update={"gap": SequenceGap(minimum_us=1, maximum_us=1)})
    assert run(setup, node.model_copy(update={"steps": (node.steps[0], second)})).matched_ids == (
        "a",
    )


def test_negative_complete_and_incomplete(setup: SequenceSetup):
    node = sequence(setup, single=True)
    node = node.model_copy(update={"steps": (*node.steps, negative(setup, node))})
    result = run(setup, node)
    assert result.matched_ids == ("b",)
    assert result.unknown_count == 1
    access = setup[1]
    access.grant = replace(access.grant, events=(replace(access.grant.events[0], complete=False),))
    result = run(setup, node)
    assert result.matched_ids == ()
    assert result.unknown_count >= 2


def test_negative_interval_boundary_and_next_step(setup: SequenceSetup):
    node = sequence(setup)
    neg = negative(setup, node, end=1000000)
    result = run(setup, node.model_copy(update={"steps": (node.steps[0], neg, node.steps[1])}))
    assert result.matched_ids == ("a",)  # blue at exclusive negative end and next-step start
    neg = neg.model_copy(update={"ends_after_us": 1000001})
    assert (
        run(
            setup, node.model_copy(update={"steps": (node.steps[0], neg, node.steps[1])})
        ).matched_ids
        == ()
    )


def test_negative_extending_past_observation_unknown(setup: SequenceSetup):
    node = sequence(setup, single=True)
    neg = negative(setup, node, "missing", end=10000000)
    result = run(setup, node.model_copy(update={"steps": (*node.steps, neg)}))
    assert result.matched_ids == ()
    assert result.unknown_count == 3


def test_unknown_native_time_and_property_not_false_absence(setup: SequenceSetup):
    change_column(setup, "time_known", [True, False, True, True, True, True])
    result = run(setup, sequence(setup))
    assert result.matched_ids == ()
    assert result.unknown_count == 1
    node = sequence(setup, single=True)
    result = run(setup, node)
    assert result.unknown_count == 1  # unknown color for n


def test_relative_exact_resolution_identity_and_half_open(setup: SequenceSetup):
    node = sequence(setup)
    window = RelativeSequenceWindow(
        anchor=at(10),
        start_offset_us=-9000000,
        end_offset_us=-8000000,
        starts_at=at(1),
        ends_at=at(2),
        observation_as_of=at(10),
        knowledge_as_of=at(11),
    )
    relative = node.model_copy(update={"window": window})
    assert run(setup, relative).matched_ids == ()
    assert run(setup, relative).request_hash != run(setup, node).request_hash
    with pytest.raises(ValidationError):
        RelativeSequenceWindow.model_validate(window.model_dump() | {"starts_at": at(0)})


def test_property_binding_and_unknown(setup: SequenceSetup):
    node = sequence(setup)
    f = next(
        f
        for f in setup[1].grant.entities[1].registry.fields
        if f.field_id == "ReceiptItem.quantity"
    )
    ref = AggregateFieldRef(field_id=f.field_id, version_id=f.version_id)
    binding = SequencePropertyBinding(
        left_step_id=node.steps[0].step_id,
        left_field=ref,
        right_step_id=node.steps[1].step_id,
        right_field=ref,
    )
    node = node.model_copy(update={"bindings": (binding,)})
    assert run(setup, node).matched_ids == ()
    change_column(setup, "quantity", [5, 5, 10, 10, 10, 10])
    assert run(setup, node).matched_ids == ("a",)
    change_column(setup, "quantity", [5, None, 10, 10, 10, 10])
    assert run(setup, node).unknown_count == 1


def test_unknown_boolean_and_canonical_order(setup: SequenceSetup):
    node = sequence(setup, single=True)
    result = run(setup, SequenceNot(node_id=uuid4(), scope_id=node.scope_id, child=node))
    assert result.matched_ids == ("c",)
    assert result.unknown_count == 1
    root = predicate(setup[1].grant, node.scope_id, "Receipt.id", "n")
    a = SequenceBoolean(node_id=uuid4(), scope_id=node.scope_id, kind="or", children=(node, root))
    b = a.model_copy(update={"children": (root, node)})
    assert canonical_sequence_expression(a) == canonical_sequence_expression(b)
    assert run(setup, a).matched_ids == ("a", "b", "n")


@pytest.mark.parametrize("dtype", [pa.timestamp("ms", tz="UTC"), pa.timestamp("us"), pa.int64()])
def test_native_time_wrong_schema_rejected(setup: SequenceSetup, dtype: Any):
    change_column(setup, "time", [1] * 6, dtype)
    with pytest.raises(AnalyticsFailure, match="FILTER_INPUT_SCHEMA"):
        run(setup, sequence(setup))


def test_forged_event_asof_and_policy_recheck(setup: SequenceSetup):
    node = sequence(setup)
    with pytest.raises(AnalyticsFailure, match="FILTER_EVENT_AS_OF"):
        run(
            setup,
            node.model_copy(
                update={"window": node.window.model_copy(update={"knowledge_as_of": at(12)})}
            ),
        )
    forged = node.steps[0].model_copy(
        update={"event": node.steps[0].event.model_copy(update={"event_id": "forged"})}
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_EVENT_BINDING"):
        run(setup, node.model_copy(update={"steps": (forged, node.steps[1])}))
    setup[1].calls = 0
    setup[1].changed = True
    with pytest.raises(AnalyticsFailure, match="FILTER_POLICY_CHANGED"):
        run(setup, node)


def test_sequence_work_preflight(setup: SequenceSetup):
    access = setup[1]
    access.grant = replace(
        access.grant,
        resource_policy=access.grant.resource_policy.model_copy(update={"max_estimated_work": 35}),
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_SEQUENCE_WORK_LIMIT"):
        run(setup, sequence(setup))


def test_old_request_readers_reject_sequence(setup: SequenceSetup):
    node = sequence(setup)
    _, access, w, _, d, _ = setup
    data = dict(
        workspace_id=w,
        dataset_version_id=d,
        root_entity="Receipt",
        root_scope_id=node.scope_id,
        registry_versions={e.registry.entity: e.registry.version_id for e in access.grant.entities},
        expression=node.model_dump(),
    )
    for cls in (RelationalFilterRequest, AggregateFilterRequest):
        with pytest.raises(ValidationError):
            cls.model_validate(data)


def test_hidden_event_cannot_disprove_absence(setup: SequenceSetup):
    change_column(setup, "parent", ["a", "a", "b", "n", "secret", "a"])
    change_column(setup, "color", ["red", "green", "red", None, "red", "blue"])
    change_column(setup, "time", [at(1), at(2), at(1), at(1), at(1), at(2)])
    node = sequence(setup, single=True)
    result = run(setup, node.model_copy(update={"steps": (*node.steps, negative(setup, node))}))
    assert result.matched_ids == ("a", "b")
    assert run(setup, sequence(setup)).matched_ids == ()


def test_observed_positive_survives_incomplete_history(setup: SequenceSetup):
    access = setup[1]
    access.grant = replace(
        access.grant, relationships=(replace(access.grant.relationships[0], complete=False),)
    )
    result = run(setup, sequence(setup))
    assert result.matched_ids == ("a",)
    assert result.unknown_count == 3


def test_observed_negative_beyond_global_window_not_used(setup: SequenceSetup):
    node = sequence(setup, single=True)
    node = node.model_copy(update={"window": node.window.model_copy(update={"ends_at": at(2)})})
    neg = negative(setup, node, end=3000000)
    result = run(setup, node.model_copy(update={"steps": (*node.steps, neg)}))
    assert result.matched_ids == ()
    assert result.unknown_count == 3  # blue at global exclusive end is not an admitted step


def test_known_time_column_wrong_type_rejected(setup: SequenceSetup):
    change_column(setup, "time_known", [1] * 6, pa.int64())
    with pytest.raises(AnalyticsFailure, match="FILTER_INPUT_SCHEMA"):
        run(setup, sequence(setup))


def test_duplicate_scope_and_event_time_forgery_rejected(setup: SequenceSetup):
    node = sequence(setup)
    second = node.steps[1].model_copy(update={"child_scope_id": node.steps[0].child_scope_id})
    with pytest.raises(AnalyticsFailure, match="FILTER_SCOPE_INVALID"):
        run(setup, node.model_copy(update={"steps": (node.steps[0], second)}))
    first = node.steps[0]
    forged = first.event.model_copy(
        update={"time_field": first.event.time_field.model_copy(update={"column": "unauthorized"})}
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_EVENT_BINDING"):
        run(
            setup,
            node.model_copy(
                update={"steps": (first.model_copy(update={"event": forged}), node.steps[1])}
            ),
        )


def test_negative_first_wrong_anchor_and_limits_rejected(setup: SequenceSetup):
    node = sequence(setup)
    neg = negative(setup, node)
    for steps in [
        (neg,),
        (*node.steps, neg),
        (node.steps[0], node.steps[0]),
        tuple(node.steps[0] for _ in range(9)),
    ]:
        with pytest.raises(ValidationError):
            BehavioralSequence.model_validate(
                node.model_dump() | {"steps": [s.model_dump() for s in steps]}
            )
    with pytest.raises(ValidationError):
        FixedSequenceWindow(
            starts_at=datetime(2025, 1, 1),
            ends_at=at(2),
            observation_as_of=at(10),
            knowledge_as_of=at(11),
        )
    with pytest.raises(ValidationError):
        SequenceGap(minimum_us=2, maximum_us=1)


def test_current_event_evidence_changes_identity(setup: SequenceSetup):
    node = sequence(setup)
    before = run(setup, node)
    access = setup[1]
    access.grant = replace(
        access.grant, events=(replace(access.grant.events[0], evidence_hash="f" * 64),)
    )
    after = run(setup, node)
    assert before.matched_ids == after.matched_ids
    assert before.request_hash != after.request_hash


def test_compound_predicate_parameters_and_multiple_sequences(setup: SequenceSetup):
    node = sequence(setup)
    other = sequence(setup, single=True)
    other = other.model_copy(update={"scope_id": node.scope_id, "parent_scope_id": node.scope_id})
    both = SequenceBoolean(
        node_id=uuid4(), scope_id=node.scope_id, kind="and", children=(node, other)
    )
    result = run(setup, both)
    assert result.matched_ids == ("a",)
    reversed = both.model_copy(update={"children": (other, node)})
    assert run(setup, reversed).request_hash == result.request_hash


def test_cancelled_execution_and_artifact_integrity(setup: SequenceSetup):
    from threading import Event

    node = sequence(setup)
    engine, access, w, a, d, root = setup
    request = SequenceFilterRequest(
        workspace_id=w,
        dataset_version_id=d,
        root_entity="Receipt",
        root_scope_id=node.scope_id,
        registry_versions={e.registry.entity: e.registry.version_id for e in access.grant.entities},
        expression=node,
    )
    cancel = Event()
    cancel.set()
    with pytest.raises(AnalyticsFailure, match="FILTER_CANCELLED"):
        engine.execute(request, actor_id=a, cancel=cancel)
    path = root / access.grant.entities[1].binding.relative_uri
    path.write_bytes(path.read_bytes() + b"corrupted")
    with pytest.raises(AnalyticsFailure, match="FILTER_ARTIFACT_INTEGRITY"):
        engine.execute(request, actor_id=a)


def test_foreign_root_scope_and_oversized_step_work(setup: SequenceSetup):
    node = sequence(setup)
    with pytest.raises(AnalyticsFailure, match="FILTER_SCOPE_INVALID"):
        run(setup, node.model_copy(update={"parent_scope_id": uuid4()}))
    access = setup[1]
    access.grant = replace(
        access.grant,
        resource_policy=access.grant.resource_policy.model_copy(update={"max_correlations": 1}),
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_PLAN_LIMIT"):
        run(setup, node)


def test_negative_probe_fanout_is_part_of_work_budget(setup: SequenceSetup):
    access = setup[1]
    child = access.grant.entities[1]
    p = setup[-1] / child.binding.relative_uri
    table = pa.table(
        {
            "id": [f"event{i}" for i in range(100)],
            "parent": ["a"] * 100,
            "color": ["red" if i % 2 else "blue" for i in range(100)],
            "quantity": pa.array([1] * 100, pa.int64()),
            "allowed": [True] * 100,
            "time": pa.array(
                [at(1) + timedelta(microseconds=i) for i in range(100)],
                pa.timestamp("us", tz="UTC"),
            ),
            "time_known": [True] * 100,
        }
    )
    pq.write_table(table, p)
    policy = access.grant.resource_policy.model_copy(
        update={"max_rows": 1000, "max_fan_out": 100, "max_estimated_work": 1000}
    )
    entities = (
        replace(access.grant.entities[0], resource_policy=policy),
        replace(
            child,
            resource_policy=policy,
            binding=replace(child.binding, content_hash=hashlib.sha256(p.read_bytes()).hexdigest()),
        ),
    )
    access.grant = replace(access.grant, entities=entities, resource_policy=policy)
    node = sequence(setup, single=True)
    node = node.model_copy(update={"steps": (*node.steps, negative(setup, node))})
    with pytest.raises(AnalyticsFailure, match="FILTER_SEQUENCE_WORK_LIMIT"):
        run(setup, node)


def test_property_binding_requires_equality_capability(setup: SequenceSetup):
    access = setup[1]
    child = access.grant.entities[1]
    field = next(f for f in child.registry.fields if f.field_id == "ReceiptItem.quantity")
    ref = AggregateFieldRef(field_id=field.field_id, version_id=field.version_id)
    child = replace(
        child,
        registry=child.registry.model_copy(
            update={
                "fields": tuple(
                    f.model_copy(update={"operators": ("ge",)}) if f == field else f
                    for f in child.registry.fields
                )
            }
        ),
    )
    access.grant = replace(access.grant, entities=(access.grant.entities[0], child))
    node = sequence(setup)
    binding = SequencePropertyBinding(
        left_step_id=node.steps[0].step_id,
        left_field=ref,
        right_step_id=node.steps[1].step_id,
        right_field=ref,
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_SEQUENCE_PROPERTY_OPERATOR"):
        run(setup, node.model_copy(update={"bindings": (binding,)}))
