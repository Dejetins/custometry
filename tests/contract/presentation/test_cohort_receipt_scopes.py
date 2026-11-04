"""Mixed receipt schemas preserve locks, source pins and sequence-local references."""

from uuid import uuid4
import pytest
from pydantic import ValidationError
from packages.contracts.analytics.receipt_cohorts import (
    CohortReceiptFilterInput,
    CustomerEventMembership,
    CohortBoolean,
)
from packages.contracts.analytics.sequence_filters import (
    BehavioralSequence,
    PositiveStep,
    NegativeStep,
    SequenceGap,
    FixedSequenceWindow,
    SequencePropertyBinding,
)
from packages.contracts.analytics.relational_filters import ScopedPredicate
from packages.contracts.analytics.columnar_filters import FilterValue
from packages.contracts.analytics.retail_aggregate import AggregateReceiptFilterInput
from packages.contracts.semantic.filter_events import FilterEventVersion, EventTimeFieldVersion
from packages.contracts.semantic.filter_aggregates import AggregateFieldRef
from packages.contracts.presentation.composer import ComposerDefinitionV1, duplicate_block
from packages.presentation.domain.receipt_scopes import (
    replacement_field,
    compatible,
    combine_filters,
)
from packages.presentation.domain.scopes import preserve_scope_locks, resolve_scope
from tests.contract.presentation.test_aggregate_receipt_scopes import aggregate
from tests.contract.presentation.test_receipt_scopes import document, receipt, scopes, resolved


def cohort():
    v2, v3 = aggregate()
    root, customer, edge = uuid4(), uuid4(), uuid4()
    event = FilterEventVersion(
        event_id="receipt.observed",
        version_id=uuid4(),
        entity="Receipt",
        relationship_version_id=edge,
        time_field=EventTimeFieldVersion(
            field_id="Receipt.event_time",
            version_id=uuid4(),
            entity="Receipt",
            column="receipt_datetime",
        ),
    )
    prop = AggregateFieldRef(field_id="Receipt.store_id", version_id=uuid4())

    def positive(gap=None):
        child = uuid4()
        return PositiveStep(
            step_id=uuid4(),
            child_scope_id=child,
            event=event,
            gap=gap,
            predicate=ScopedPredicate(
                node_id=uuid4(),
                scope_id=child,
                field_id=prop.field_id,
                field_version_id=prop.version_id,
                operator="eq",
                values=(FilterValue(data_type="string", value="1"),),
            ),
        )

    first = positive()
    middle = positive()
    last = positive(SequenceGap(maximum_us=20000000))
    negative = NegativeStep(
        step_id=middle.step_id,
        child_scope_id=middle.child_scope_id,
        event=event,
        predicate=middle.predicate,
        after_step_id=first.step_id,
        ends_after_us=1000000,
    )
    sequence = BehavioralSequence(
        node_id=uuid4(),
        scope_id=customer,
        parent_scope_id=customer,
        relationship_id="customer.receipts",
        relationship_version_id=edge,
        child_entity="Receipt",
        window=FixedSequenceWindow(
            starts_at="2025-01-01T00:00:00Z",
            ends_at="2025-02-01T00:00:00Z",
            observation_as_of="2025-02-01T12:34:56.123456Z",
            knowledge_as_of="2025-02-01T12:34:56.123456Z",
        ),
        steps=(first, negative, last),
        bindings=(
            SequencePropertyBinding(
                left_step_id=first.step_id,
                left_field=prop,
                right_step_id=last.step_id,
                right_field=prop,
            ),
        ),
    )
    value = CohortReceiptFilterInput(
        root_scope_id=root,
        registry_versions={**v3.registry_versions, "Receipt": uuid4(), "Customer": uuid4()},
        receipt_registry_versions=v3.registry_versions,
        legacy_registry_version_id=v3.legacy_registry_version_id,
        expression=CustomerEventMembership(
            node_id=uuid4(),
            scope_id=root,
            customer_scope_id=customer,
            relationship_id="customer.receipts",
            relationship_version_id=edge,
            predicate=sequence,
        ),
    )
    return v2, v3, value


def test_mixed_scopes_preserve_pins_and_rebase_step_references():
    d = document()
    v2, v3, v4 = cohort()
    old = receipt("document", d.document_id)
    bindings = [old]
    for level, identifier, value in [
        ("page", d.pages[0].page_id, v2),
        ("section", d.blocks[0].section_id, v3),
        ("block", d.blocks[0].block_id, v4),
    ]:
        item = receipt(level, identifier, locked=True)
        item["filter"] = value.model_dump(mode="json")
        bindings.append(item)
    d = scopes(d, *bindings)
    result = resolved(d).query.receipt_filter
    assert isinstance(result, CohortReceiptFilterInput)
    assert result.receipt_registry_versions == v2.registry_versions
    assert result.promoted_registry_sets == (v2.registry_versions,)
    leaf = result.expression.children[-1]
    seq = leaf.predicate
    before = v4.expression.predicate
    assert (
        leaf.scope_id == result.root_scope_id
        and seq.scope_id == leaf.customer_scope_id == seq.parent_scope_id
    )
    assert (
        seq.window == before.window
        and seq.relationship_version_id == before.relationship_version_id
    )
    for new, previous in zip(seq.steps, before.steps, strict=True):
        assert new.step_id != previous.step_id and new.child_scope_id == new.predicate.scope_id
        assert new.event == previous.event
    assert seq.steps[1].after_step_id == seq.steps[0].step_id
    assert seq.bindings[0].left_step_id == seq.steps[0].step_id
    assert seq.bindings[0].right_step_id == seq.steps[-1].step_id
    assert seq.bindings[0].left_field == before.bindings[0].left_field
    assert replacement_field(v4) == set()
    wrapped = v4.model_copy(
        update={
            "expression": CohortBoolean(
                kind="and", node_id=uuid4(), scope_id=v4.root_scope_id, children=(v4.expression,)
            )
        }
    )
    assert replacement_field(wrapped) == set()
    with pytest.raises(ValueError, match="SCOPE_LOCKED"):
        preserve_scope_locks(d, scopes(d, *bindings[:-1]))
    with pytest.raises(ValidationError):
        AggregateReceiptFilterInput.model_validate(
            result.model_dump(mode="json") | {"schema_version": "receipt-filter/v3"}
        )


def test_v4_copy_title_and_save_roundtrip_identity():
    d = document()
    _, _, v4 = cohort()
    parent = receipt("document", d.document_id)
    parent["filter"] = v4.model_dump(mode="json")
    raw = d.model_dump(mode="json")
    raw["definitions"][0]["query"]["receipt_filter"] = v4.model_dump(mode="json")
    d = scopes(ComposerDefinitionV1.model_validate(raw), parent)
    before = resolved(d)
    copied = duplicate_block(
        d,
        d.blocks[0].block_id,
        section_id=d.blocks[0].section_id,
        order=1,
        placement=d.blocks[0].placement.model_copy(update={"row": 1}),
    )
    after = resolve_scope(copied, copied.scopes, copied.blocks[-1].block_id)
    assert after.query == before.query and after.dependency_hash == before.dependency_hash
    raw = d.model_dump(mode="json")
    raw["blocks"][0]["presentation"]["title"] = "Presentation only"
    reopened = ComposerDefinitionV1.model_validate_json(
        ComposerDefinitionV1.model_validate(raw).model_dump_json()
    )
    assert resolved(reopened).query == before.query


def test_bridge_and_origin_mismatch_fail_composition():
    v2, _, v4 = cohort()
    assert compatible(v2, v4) and compatible(v4, v2)
    for bad in (
        v4.model_copy(update={"receipt_registry_versions": {"Receipt": uuid4()}}),
        v4.model_copy(update={"promoted_registry_sets": ({"Receipt": uuid4()},)}),
    ):
        assert not compatible(bad, v2)
        with pytest.raises(ValueError, match="COMPOSER_FILTER_REGISTRY_MISMATCH"):
            combine_filters([(uuid4(), v2), (uuid4(), bad)])


@pytest.mark.parametrize("old_kind", [0, 1])
def test_optional_absent_legacy_pin_does_not_prevent_v4_bridge(old_kind):
    v2, v3, v4 = cohort()
    old = (v2, v3)[old_kind].model_copy(update={"legacy_registry_version_id": None})
    assert compatible(old, v4)
    result = combine_filters([(uuid4(), old), (uuid4(), v4)])
    assert isinstance(result, CohortReceiptFilterInput)
    assert result.legacy_registry_version_id == v4.legacy_registry_version_id
    assert result.promoted_registry_sets == (old.registry_versions,)


def test_conflicting_present_legacy_pins_are_not_lost_in_v4_composition():
    v2, _, v4 = cohort()
    old = v2.model_copy(update={"legacy_registry_version_id": uuid4()})
    assert not compatible(old, v4)
    with pytest.raises(ValueError, match="COMPOSER_FILTER_REGISTRY_MISMATCH"):
        combine_filters([(uuid4(), old), (uuid4(), v4)])


def test_v4_replacement_cannot_erase_ancestor_legacy_registry_pin():
    d = document()
    parent = receipt("document", d.document_id, replaceable=True)
    child = receipt("block", d.blocks[0].block_id, "other",
                    combine_mode="replace_allowed_parent_field",
                    replaces=[parent["binding_id"]])
    _, _, v4 = cohort()
    raw = dict(child["filter"]["expression"])
    raw.update(node_id=str(uuid4()), scope_id=str(v4.root_scope_id))
    value = v4.model_dump(mode="json")
    value.update(expression=raw, legacy_registry_version_id=None)
    child["filter"] = value
    with pytest.raises(ValueError, match="REPLACEMENT_FIELD_MISMATCH"):
        resolved(scopes(d, parent, child))
    value["legacy_registry_version_id"] = parent["filter"]["registry_version_id"]
    result = resolved(scopes(d, parent, child))
    assert result.query.receipt_filter.legacy_registry_version_id == v4.legacy_registry_version_id
