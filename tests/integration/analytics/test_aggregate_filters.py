"""Actual admitted Parquet/DuckDB aggregate math; synthetic trusted capabilities."""

from dataclasses import replace
from datetime import date, datetime, UTC
from uuid import uuid4
import hashlib
import pytest
import pyarrow as pa
import pyarrow.parquet as pq
from pydantic import ValidationError
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.aggregate_filters import (
    AggregateFilterRequest,
    AggregateInputGrant,
    CountInput,
    AggregateWindow,
    ScopedCount,
    CountRatio,
    AggregateCompare,
    AggregateScalar,
    AggregateBoolean,
    AggregateNot,
    AggregateExists,
    canonical_aggregate_expression,
)
from packages.contracts.analytics.relational_filters import RelationalFilterRequest
from packages.contracts.analytics.retail_relational import RelationalReceiptFilterInput
from packages.contracts.semantic.filter_aggregates import (
    FilterCountVersion,
    AggregateFieldRef,
    AggregateObservation,
)
from packages.contracts.semantic.filter_fields import FilterFieldVersion
from tests.integration.analytics.test_relational_filters import (
    setup as relational_setup,  # noqa: F401 -- pytest fixture registration
    predicate,
    run,
)


def at(day):
    return datetime(2025, 1, day, tzinfo=UTC)


@pytest.fixture
def setup(request):
    relational = request.getfixturevalue("relational_setup")
    engine, access, w, a, d, root = relational
    entities = []
    for e in access.grant.entities:
        path = root / e.binding.relative_uri
        table = pq.read_table(path)
        dates = [date(2025, 1, 1)] * table.num_rows
        if e.registry.entity == "ReceiptItem":
            dates[1] = date(2025, 1, 2)
        table = table.append_column("day", pa.array(dates, pa.date32()))
        table = table.append_column("day_known", pa.array([True] * table.num_rows))
        field = FilterFieldVersion(
            field_id=f"{e.registry.entity}.day",
            version_id=uuid4(),
            entity=e.registry.entity,
            column="day",
            data_type="date",
            operators=("eq", "ge"),
            null_policy="unknown",
            known_column="day_known",
        )
        pq.write_table(table, path)
        entities.append(
            replace(
                e,
                binding=replace(
                    e.binding, content_hash=hashlib.sha256(path.read_bytes()).hexdigest()
                ),
                registry=e.registry.model_copy(update={"fields": (*e.registry.fields, field)}),
            )
        )
    original = access.grant
    access.grant = AggregateInputGrant(
        entities=tuple(entities),
        relationships=original.relationships,
        resource_policy=original.resource_policy,
    )
    return relational


def count(
    setup,
    scope,
    *,
    distinct=False,
    start=1,
    end=3,
    parent_time=False,
    null_policy="unknown",
    red=False,
):
    access = setup[1]
    r = access.grant.relationships[0].relationship
    fields = {f.field_id: f for e in access.grant.entities for f in e.registry.fields}

    def ref(name):
        return AggregateFieldRef(field_id=name, version_id=fields[name].version_id)

    definition = FilterCountVersion(
        count_id="items.colors" if distinct else "items.rows",
        version_id=uuid4(),
        relationship_version_id=r.version_id,
        child_entity="ReceiptItem",
        kind="count_distinct" if distinct else "count",
        grain_fields=(ref("ReceiptItem.color" if distinct else "ReceiptItem.id"),),
        unit="colors" if distinct else "items",
        null_policy=null_policy,
        time_entity="parent" if parent_time else "child",
        time_field=ref("Receipt.day" if parent_time else "ReceiptItem.day"),
    )
    observation = AggregateObservation(
        starts_at=at(1), ends_at=at(4), observation_as_of=at(4), knowledge_as_of=at(5)
    )
    access.grant = replace(
        access.grant, counts=(*access.grant.counts, CountInput(definition, observation, "b" * 64))
    )
    child = uuid4()
    return ScopedCount(
        parent_scope_id=scope,
        child_scope_id=child,
        child_entity="ReceiptItem",
        relationship_id=r.relationship_id,
        relationship_version_id=r.version_id,
        definition=definition,
        window=AggregateWindow(
            starts_at=at(start), ends_at=at(end), observation_as_of=at(4), knowledge_as_of=at(5)
        ),
        predicate=predicate(
            access.grant,
            child,
            "ReceiptItem.color" if red else "ReceiptItem.quantity",
            "red" if red else 0,
            "eq" if red else "ge",
        ),
    )


def query(setup, left, right="1", operator="ge"):
    scope = left.numerator.parent_scope_id if isinstance(left, CountRatio) else left.parent_scope_id
    if isinstance(right, str):
        unit = "ratio" if isinstance(left, CountRatio) else left.definition.unit
        right = AggregateScalar(value=right, unit=unit)
    return AggregateFilterRequest(
        workspace_id=setup[2],
        dataset_version_id=setup[4],
        root_entity="Receipt",
        root_scope_id=scope,
        registry_versions={
            e.registry.entity: e.registry.version_id for e in setup[1].grant.entities
        },
        expression=AggregateCompare(
            node_id=uuid4(), scope_id=scope, left=left, operator=operator, right=right
        ),
    )


def rewrite(setup, entity, column, values, dtype):
    access = setup[1]
    entities = []
    for e in access.grant.entities:
        if e.registry.entity == entity:
            path = setup[5] / e.binding.relative_uri
            table = pq.read_table(path)
            table = table.set_column(
                table.column_names.index(column), column, pa.array(values, type=dtype)
            )
            pq.write_table(table, path)
            e = replace(
                e,
                binding=replace(
                    e.binding, content_hash=hashlib.sha256(path.read_bytes()).hexdigest()
                ),
            )
        entities.append(e)
    access.grant = replace(access.grant, entities=tuple(entities))


def test_count_empty_complete_and_half_open_windows(setup):
    c = count(setup, uuid4())
    assert run(setup, query(setup, c, "2")).matched_ids == ("a",)
    result = run(setup, query(setup, c, "0", "eq"))
    assert (
        result.matched_ids == ("c",) and result.unknown_count == 0 and result.authorized_count == 4
    )
    first = count(setup, uuid4(), end=2)
    assert run(setup, query(setup, first, "1", "eq")).matched_ids == ("a", "b", "n")
    parent = count(setup, uuid4(), start=2, end=3, parent_time=True)
    assert run(setup, query(setup, parent, "0", "eq")).matched_ids == ("a", "b", "c", "n")


def test_distinct_null_exclusion_and_unknown_property(setup):
    c = count(setup, uuid4(), distinct=True)
    result = run(setup, query(setup, c, "1"))
    assert result.matched_ids == ("a", "b") and result.unknown_count == 1
    c = count(setup, uuid4(), distinct=True, null_policy="exclude")
    result = run(setup, query(setup, c, "0", "eq"))
    assert result.matched_ids == ("c", "n") and result.unknown_count == 0


def test_unknown_window_and_predicate_never_zero_or_negated_true(setup):
    rewrite(setup, "ReceiptItem", "day_known", [True, True, False, True, True, True], pa.bool_())
    c = count(setup, uuid4(), red=True)
    q = query(setup, c, "0", "eq")
    result = run(setup, q)
    assert result.matched_ids == ("c",) and result.unknown_count == 2
    q = q.model_copy(
        update={
            "expression": AggregateNot(
                node_id=uuid4(), scope_id=q.root_scope_id, child=q.expression
            )
        }
    )
    result = run(setup, q)
    assert result.matched_ids == ("a",) and result.unknown_count == 2


def test_incomplete_relationship_or_coverage_is_unknown(setup):
    c = count(setup, uuid4())
    access = setup[1]
    access.grant = replace(
        access.grant, relationships=(replace(access.grant.relationships[0], complete=False),)
    )
    result = run(setup, query(setup, c, "0", "eq"))
    assert result.matched_ids == () and result.unknown_count == 4
    access.grant = replace(
        access.grant, relationships=(replace(access.grant.relationships[0], complete=True),)
    )
    given = access.grant.counts[0]
    access.grant = replace(
        access.grant,
        counts=(
            replace(given, observation=given.observation.model_copy(update={"starts_at": at(2)})),
        ),
    )
    assert run(setup, query(setup, c)).unknown_count == 4


def test_scoped_operands_ratio_exact_comparison_and_zero_denominator(setup):
    scope = uuid4()
    left = count(setup, scope, end=2)
    right = count(setup, scope, start=2, end=3)
    result = run(setup, query(setup, left, right, "eq"))
    assert result.matched_ids == ("a", "c")
    scope = uuid4()
    ratio = CountRatio(numerator=count(setup, scope, red=True), denominator=count(setup, scope))
    q = query(setup, ratio, "0.5", "eq")
    result = run(setup, q)
    assert result.matched_ids == ("a",) and result.unknown_count == 2
    assert run(setup, query(setup, ratio, "0.500001", "lt")).matched_ids == ("a",)
    other = CountRatio(numerator=count(setup, scope, red=True), denominator=count(setup, scope))
    assert run(setup, query(setup, ratio, other, "eq")).matched_ids == ("a", "b")


def test_current_authorization_and_pre_aggregation_child_ceiling(setup):
    c = count(setup, uuid4())
    q = query(setup, c, "0", "eq")
    # c has one hidden child: it stays empty within the current authorized scope.
    assert run(setup, q).matched_ids == ("c",)
    setup[1].changed = True
    setup[1].calls = 0
    with pytest.raises(AnalyticsFailure, match="FILTER_POLICY_CHANGED"):
        run(setup, q)


def test_old_readers_reject_aggregate_and_unchanged_canonical_boolean_order(setup):
    scope = uuid4()
    q = query(setup, count(setup, scope))
    old = {**q.model_dump(mode="json"), "schema_version": "relational-filter-execution/v2"}
    with pytest.raises(ValidationError):
        RelationalFilterRequest.model_validate(old)
    with pytest.raises(ValidationError):
        RelationalReceiptFilterInput.model_validate(
            dict(
                root_scope_id=scope,
                registry_versions=q.registry_versions,
                expression=q.expression.model_dump(mode="json"),
            )
        )
    second = query(setup, count(setup, scope, distinct=True)).expression
    tree = AggregateBoolean(
        kind="and", node_id=uuid4(), scope_id=scope, children=(q.expression, second)
    )
    reversed_tree = tree.model_copy(update={"children": tuple(reversed(tree.children))})
    assert canonical_aggregate_expression(tree) == canonical_aggregate_expression(reversed_tree)
    q = q.model_copy(update={"expression": tree})
    other = q.model_copy(update={"expression": reversed_tree})
    assert setup[0].fingerprint(q, actor_id=setup[3]) == setup[0].fingerprint(
        other, actor_id=setup[3]
    )
    assert run(setup, q).matched_ids == ("a", "b")


@pytest.mark.parametrize(
    "change,code",
    [
        ("definition", "BINDING"),
        ("asof", "AS_OF"),
        ("unit", "UNIT"),
        ("scope", "SCOPE_INVALID"),
        ("version", "BINDING"),
        ("window_field", "TIME_FIELD"),
        ("row_grain", "GRAIN"),
        ("capability", "CAPABILITY"),
    ],
)
def test_invalid_bindings_fail_closed(setup, change, code):
    c = count(setup, uuid4())
    q = query(setup, c)
    if change == "definition":
        c = c.model_copy(
            update={"definition": c.definition.model_copy(update={"version_id": uuid4()})}
        )
    elif change == "asof":
        c = c.model_copy(update={"window": c.window.model_copy(update={"knowledge_as_of": at(6)})})
    elif change == "unit":
        q = q.model_copy(
            update={
                "expression": q.expression.model_copy(
                    update={"right": AggregateScalar(value="1", unit="other")}
                )
            }
        )
    elif change == "scope":
        c = c.model_copy(update={"child_scope_id": q.root_scope_id})
    elif change == "version":
        c = c.model_copy(update={"relationship_version_id": uuid4()})
    elif change in ("window_field", "row_grain"):
        field = next(
            f
            for f in setup[1].grant.entities[1].registry.fields
            if f.field_id == "ReceiptItem.color"
        )
        ref = AggregateFieldRef(field_id=field.field_id, version_id=field.version_id)
        definition = c.definition.model_copy(
            update={"time_field": ref} if change == "window_field" else {"grain_fields": (ref,)}
        )
        c = c.model_copy(update={"definition": definition})
        supplied = setup[1].grant.counts[0]
        setup[1].grant = replace(setup[1].grant, counts=(replace(supplied, definition=definition),))
    elif change == "capability":
        from packages.contracts.analytics.relational_filters import RelationalInputGrant

        old = setup[1].grant
        setup[1].grant = RelationalInputGrant(
            entities=old.entities,
            relationships=old.relationships,
            resource_policy=old.resource_policy,
        )
    q = q.model_copy(update={"expression": q.expression.model_copy(update={"left": c})})
    with pytest.raises(AnalyticsFailure, match=code):
        run(setup, q)


def test_identity_pins_coverage_definition_and_evidence(setup):
    c = count(setup, uuid4())
    q = query(setup, c)
    access = setup[1]
    baseline = setup[0].fingerprint(q, actor_id=setup[3])
    given = access.grant.counts[0]
    for modified in [
        replace(given, evidence_hash="c" * 64),
        replace(given, observation=given.observation.model_copy(update={"starts_at": at(2)})),
    ]:
        access.grant = replace(access.grant, counts=(modified,))
        assert setup[0].fingerprint(q, actor_id=setup[3]) != baseline


def test_limits_and_cancellation(setup):
    from threading import Event

    scope = uuid4()
    ratio = CountRatio(numerator=count(setup, scope), denominator=count(setup, scope))
    q = query(setup, ratio)
    access = setup[1]
    policy = access.grant.resource_policy
    for patch, code in [
        ({"max_correlations": 1}, "PLAN_LIMIT"),
        ({"max_estimated_work": 1}, "WORK_LIMIT"),
        ({"max_values": 1}, "PLAN_LIMIT"),
        ({"max_fan_out": 1}, "FAN_OUT_LIMIT"),
    ]:
        access.grant = replace(access.grant, resource_policy=policy.model_copy(update=patch))
        with pytest.raises(AnalyticsFailure, match=code):
            run(setup, q)
    access.grant = replace(access.grant, resource_policy=policy)
    cancelled = Event()
    cancelled.set()
    with pytest.raises(AnalyticsFailure, match="CANCELLED"):
        setup[0].execute(q, actor_id=setup[3], cancel=cancelled)


@pytest.mark.parametrize("value", ["NaN", "1e2", "-1", "1000000000", "0.1234567", "01"])
def test_scalar_numeric_bound(value):
    with pytest.raises(ValidationError):
        AggregateScalar(value=value, unit="ratio")


def test_window_rejects_unresolved_non_utc_intraday_or_reversed():
    valid = dict(starts_at=at(1), ends_at=at(2), observation_as_of=at(4), knowledge_as_of=at(5))
    for patch in [
        dict(starts_at=at(3)),
        dict(starts_at=at(1).replace(hour=1)),
        dict(ends_at=at(6)),
        dict(timezone="Europe/Moscow"),
        dict(starts_at=at(1).replace(tzinfo=None)),
    ]:
        with pytest.raises(ValidationError):
            AggregateWindow(**{**valid, **patch})


def test_boolean_mixed_exists_aggregate_and_distinct_composite_grain(setup):
    scope = uuid4()
    c = count(setup, scope, distinct=True)
    f = next(
        f
        for f in setup[1].grant.entities[1].registry.fields
        if f.field_id == "ReceiptItem.quantity"
    )
    definition = c.definition.model_copy(
        update={
            "grain_fields": (
                *c.definition.grain_fields,
                AggregateFieldRef(field_id=f.field_id, version_id=f.version_id),
            )
        }
    )
    c = c.model_copy(update={"definition": definition})
    given = setup[1].grant.counts[0]
    setup[1].grant = replace(setup[1].grant, counts=(replace(given, definition=definition),))
    q = query(setup, c, "2")
    relation = setup[1].grant.relationships[0].relationship
    child = uuid4()
    exists = AggregateExists(
        kind="exists",
        node_id=uuid4(),
        scope_id=scope,
        parent_scope_id=scope,
        child_scope_id=child,
        child_entity="ReceiptItem",
        relationship_id=relation.relationship_id,
        relationship_version_id=relation.version_id,
        predicate=predicate(setup[1].grant, child, "ReceiptItem.color", "red"),
    )
    q = q.model_copy(
        update={
            "expression": AggregateBoolean(
                kind="and", node_id=uuid4(), scope_id=scope, children=(q.expression, exists)
            )
        }
    )
    assert run(setup, q).matched_ids == ("a",)


def test_unknown_grain_observation_not_excluded_as_known_null(setup):
    access = setup[1]
    child = access.grant.entities[1]
    fields = tuple(
        f.model_copy(update={"known_column": "day_known"})
        if f.field_id == "ReceiptItem.color"
        else f
        for f in child.registry.fields
    )
    child = replace(child, registry=child.registry.model_copy(update={"fields": fields}))
    access.grant = replace(access.grant, entities=(access.grant.entities[0], child))
    rewrite(setup, "ReceiptItem", "day_known", [True, True, False, True, True, True], pa.bool_())
    c = count(setup, uuid4(), distinct=True, null_policy="exclude", parent_time=True)
    result = run(setup, query(setup, c, "0", "eq"))
    assert result.matched_ids == ("c", "n") and result.unknown_count == 1


def test_ratio_incompatible_units_and_reused_child_scope_reject(setup):
    scope = uuid4()
    numerator = count(setup, scope)
    denominator = count(setup, scope, distinct=True)
    ratio = CountRatio(numerator=numerator, denominator=denominator)
    with pytest.raises(AnalyticsFailure, match="AGGREGATE_UNIT"):
        run(setup, query(setup, ratio))
    with pytest.raises(AnalyticsFailure, match="SCOPE_INVALID"):
        run(setup, query(setup, CountRatio(numerator=numerator, denominator=numerator)))


def test_aggregate_unknown_obeys_boolean_three_valued_logic(setup):
    scope = uuid4()
    q = query(setup, count(setup, scope))
    access = setup[1]
    access.grant = replace(
        access.grant, relationships=(replace(access.grant.relationships[0], complete=False),)
    )
    true = predicate(access.grant, scope, "Receipt.allowed", True)
    false = predicate(access.grant, scope, "Receipt.allowed", False)
    for kind, node, matched, unknown in [
        ("and", false, (), 0),
        ("or", true, ("a", "b", "c", "n"), 0),
        ("and", true, (), 4),
        ("or", false, (), 4),
    ]:
        expression = AggregateBoolean(
            kind=kind, node_id=uuid4(), scope_id=scope, children=(q.expression, node)
        )
        result = run(setup, q.model_copy(update={"expression": expression}))
        assert result.matched_ids == matched and result.unknown_count == unknown


def test_count_distinct_counts_values_not_rows_and_observation_change_rejects(setup):
    rewrite(setup, "ReceiptItem", "color", ["red", "red", "red", None, "red", "red"], pa.string())
    c = count(setup, uuid4(), distinct=True, null_policy="exclude")
    q = query(setup, c, "1", "eq")
    assert run(setup, q).matched_ids == ("a", "b")
    access = setup[1]
    original = access.authorize
    calls = 0

    def changing(**kwargs):
        nonlocal calls
        calls += 1
        grant = original(**kwargs)
        return (
            replace(grant, counts=(replace(grant.counts[0], evidence_hash="d" * 64),))
            if calls > 1
            else grant
        )

    access.authorize = changing
    with pytest.raises(AnalyticsFailure, match="FILTER_POLICY_CHANGED"):
        run(setup, q)


def test_as_of_keeps_exact_publication_time_without_rounding(setup):
    c = count(setup, uuid4())
    observation_as_of = at(4).replace(hour=13, minute=2, second=3, microsecond=456)
    knowledge_as_of = at(5).replace(hour=14, minute=10)
    given = setup[1].grant.counts[0]
    observation = AggregateObservation(
        starts_at=at(1),
        ends_at=at(4),
        observation_as_of=observation_as_of,
        knowledge_as_of=knowledge_as_of,
    )
    setup[1].grant = replace(setup[1].grant, counts=(replace(given, observation=observation),))
    window = AggregateWindow(
        starts_at=at(1),
        ends_at=at(3),
        observation_as_of=observation_as_of,
        knowledge_as_of=knowledge_as_of,
    )
    c = c.model_copy(update={"window": window})
    assert run(setup, query(setup, c, "2")).matched_ids == ("a",)
    wrong = c.model_copy(
        update={
            "window": window.model_copy(
                update={"knowledge_as_of": knowledge_as_of.replace(microsecond=1)}
            )
        }
    )
    with pytest.raises(AnalyticsFailure, match="AGGREGATE_AS_OF"):
        run(setup, query(setup, wrong))
