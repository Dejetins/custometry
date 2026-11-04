"""Real immutable Parquet proof for mandatory roots and nullable child references."""

from dataclasses import replace, fields
from uuid import uuid4
from typing import Any, cast
import pytest
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import FlatInputGrant
from packages.contracts.analytics.customer_events import (
    RootRestrictedSequenceGrant,
    ObservedChildRootRestriction,
)
from packages.contracts.semantic.nullable_relationships import NullableFilterRelationshipVersion
from packages.contracts.analytics.sequence_filters import SequenceNot
from tests.integration.analytics.test_sequence_filters import (
    setup as sequence_setup,  # pyright: ignore[reportUnusedImport]  # noqa: F401 -- fixture registration
    run,
    sequence,
    change_column,
)  # noqa: F401
from tests.integration.analytics.test_relational_filters import FilterSetup, predicate
from tests.integration.analytics.test_relational_filters import setup as relational_setup  # pyright: ignore[reportUnusedImport]  # noqa: F401


CustomerSetup = FilterSetup[RootRestrictedSequenceGrant]


@pytest.fixture
def setup(request: pytest.FixtureRequest) -> CustomerSetup:
    result = cast(CustomerSetup, request.getfixturevalue("sequence_setup"))
    access = result[1]
    old = access.grant
    edge = old.relationships[0].relationship
    edge = NullableFilterRelationshipVersion.model_validate(
        edge.model_dump() | {"nullable_child_fields": ["ReceiptItem.parent"]}
    )
    restriction = ObservedChildRootRestriction(
        version_id=uuid4(),
        root_entity="Receipt",
        relationship_id=edge.relationship_id,
        relationship_version_id=edge.version_id,
    )
    attributes: dict[str, Any] = {f.name: getattr(old, f.name) for f in fields(old)}
    attributes.update(
        relationships=(replace(old.relationships[0], relationship=edge),),
        root_restrictions=(restriction,),
    )
    access.grant = RootRestrictedSequenceGrant(**attributes)
    return result


def everything(setup: CustomerSetup) -> SequenceNot:
    scope = uuid4()
    return SequenceNot(
        node_id=uuid4(),
        scope_id=scope,
        child=predicate(setup[1].grant, scope, "Receipt.id", "never"),
    )


def test_root_requires_observed_authorized_child_independently_of_filter(setup: CustomerSetup):
    result = run(setup, everything(setup))
    assert result.matched_ids == ("a", "b", "n")
    assert result.authorized_count == 3
    change_column(setup, "allowed", [False] * 6)
    assert run(setup, everything(setup)).authorized_count == 0


def test_null_child_reference_is_unlinked_not_invented_root(setup: CustomerSetup):
    change_column(setup, "parent", ["a", "a", "b", None, "secret", "c"])
    result = run(setup, everything(setup))
    assert result.matched_ids == ("a", "b")
    assert result.authorized_count == 2
    assert run(setup, sequence(setup)).matched_ids == ("a",)


def test_nonnull_orphan_still_rejected(setup: CustomerSetup):
    change_column(setup, "parent", ["a", "a", "b", "missing", "secret", "c"])
    with pytest.raises(AnalyticsFailure, match="FILTER_RELATIONSHIP_KEYS"):
        run(setup, everything(setup))


def test_wrong_root_or_relation_policy_denied(setup: CustomerSetup):
    access = setup[1]
    restriction = access.grant.root_restrictions[0]
    access.grant = replace(
        access.grant,
        root_restrictions=(restriction.model_copy(update={"root_entity": "ReceiptItem"}),),
    )
    with pytest.raises(AnalyticsFailure, match="FILTER_ROOT_POLICY_BINDING"):
        run(setup, everything(setup))
    access.grant = replace(access.grant, root_restrictions=())
    with pytest.raises(AnalyticsFailure, match="FILTER_ROOT_POLICY_BINDING"):
        run(setup, everything(setup))


def test_root_policy_is_part_of_identity(setup: CustomerSetup):
    node = everything(setup)
    before = run(setup, node)
    access = setup[1]
    restriction = access.grant.root_restrictions[0]
    access.grant = replace(
        access.grant, root_restrictions=(restriction.model_copy(update={"version_id": uuid4()}),)
    )
    assert run(setup, node).request_hash != before.request_hash


def test_unlinked_rows_do_not_form_a_customer_fanout(setup: CustomerSetup):
    import hashlib
    import pyarrow as _pa  # pyright: ignore[reportMissingTypeStubs]
    import pyarrow.parquet as _pq  # pyright: ignore[reportMissingTypeStubs]

    pa: Any = _pa
    pq: Any = _pq

    access = setup[1]
    child = access.grant.entities[1]
    path = setup[-1] / child.binding.relative_uri
    table = pq.read_table(path)
    extra = pa.Table.from_pylist(
        [
            dict(table.slice(0, 1).to_pylist()[0], id=f"unlinked{i}", parent=None)
            for i in range(100)
        ],
        schema=table.schema,
    )
    pq.write_table(pa.concat_tables([table, extra]), path)
    policy = access.grant.resource_policy.model_copy(update={"max_rows": 1000})
    access.grant = replace(
        access.grant,
        resource_policy=policy,
        entities=(
            replace(access.grant.entities[0], resource_policy=policy),
            replace(
                child,
                resource_policy=policy,
                binding=replace(
                    child.binding, content_hash=hashlib.sha256(path.read_bytes()).hexdigest()
                ),
            ),
        ),
    )
    result = run(setup, sequence(setup))
    assert result.matched_ids == ("a",)
    assert result.authorized_count == 3


@pytest.mark.parametrize("missing_namespace", [False, True])
def test_nullable_foreign_key_does_not_null_required_namespace(
    setup: CustomerSetup, missing_namespace: bool
):
    import hashlib
    import pyarrow as _pa  # pyright: ignore[reportMissingTypeStubs]
    import pyarrow.parquet as _pq  # pyright: ignore[reportMissingTypeStubs]

    pa: Any = _pa
    pq: Any = _pq
    from packages.contracts.semantic.filter_fields import FilterFieldVersion

    access = setup[1]
    entities: list[FlatInputGrant] = []
    for entity in access.grant.entities:
        path = setup[-1] / entity.binding.relative_uri
        table = pq.read_table(path)
        values: list[str | None] = ["source"] * table.num_rows
        if entity.registry.entity == "ReceiptItem" and missing_namespace:
            values[3] = None
        table = table.append_column("namespace", pa.array(values, pa.string()))
        pq.write_table(table, path)
        field = FilterFieldVersion(
            field_id=f"{entity.registry.entity}.namespace",
            version_id=uuid4(),
            entity=entity.registry.entity,
            column="namespace",
            data_type="string",
            operators=("eq",),
            null_policy="unknown",
        )
        entities.append(
            replace(
                entity,
                binding=replace(
                    entity.binding, content_hash=hashlib.sha256(path.read_bytes()).hexdigest()
                ),
                registry=entity.registry.model_copy(
                    update={"fields": (*entity.registry.fields, field)}
                ),
            )
        )
    relation = access.grant.relationships[0]
    edge = relation.relationship.model_copy(
        update={
            "parent_fields": ("Receipt.namespace", "Receipt.id"),
            "child_fields": ("ReceiptItem.namespace", "ReceiptItem.parent"),
        }
    )
    access.grant = replace(
        access.grant,
        entities=tuple(entities),
        relationships=(replace(relation, relationship=edge),),
    )
    change_column(setup, "parent", ["a", "a", "b", None, "secret", "c"])
    if missing_namespace:
        with pytest.raises(AnalyticsFailure, match="FILTER_RELATIONSHIP_KEYS"):
            run(setup, everything(setup))
    else:
        assert run(setup, everything(setup)).matched_ids == ("a", "b")


def test_old_relationship_reader_rejects_new_nullable_capability(setup: CustomerSetup):
    from packages.contracts.semantic.relationships import FilterRelationshipVersion
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        FilterRelationshipVersion.model_validate(
            setup[1].grant.relationships[0].relationship.model_dump()
        )
