"""V2 hierarchy and explicit v1 registry bridge preserve correlation and locks."""

from uuid import uuid4
import pytest
from packages.contracts.analytics.retail_filter import ReceiptFilterInput
from packages.contracts.analytics.retail_relational import RelationalReceiptFilterInput
from packages.contracts.analytics.columnar_filters import FlatPredicate, FilterValue
from packages.presentation.domain.receipt_scopes import combine_filters, replacement_field
from packages.presentation.domain.scopes import preserve_scope_locks
from tests.contract.presentation.test_receipt_scopes import (
    document,
    receipt,
    scopes,
    resolved,
    REGISTRY,
    FIELD,
)


def related():
    root, child = uuid4(), uuid4()
    return RelationalReceiptFilterInput.model_validate(
        dict(
            root_scope_id=root,
            registry_versions={"Receipt": uuid4(), "ReceiptItem": uuid4()},
            legacy_registry_version_id=REGISTRY,
            expression=dict(
                kind="exists",
                node_id=uuid4(),
                scope_id=root,
                parent_scope_id=root,
                child_scope_id=child,
                child_entity="ReceiptItem",
                relationship_id="receipt.items",
                relationship_version_id=uuid4(),
                predicate=dict(
                    kind="predicate",
                    node_id=uuid4(),
                    scope_id=child,
                    field_id="ReceiptItem.quantity",
                    field_version_id=uuid4(),
                    operator="ge",
                    values=[dict(data_type="decimal", value="2.000")],
                ),
            ),
        )
    )


def test_mixed_hierarchy_composition_stable_ids_and_single_child_scope():
    d = document()
    parent = receipt("document", d.document_id, locked=True)
    child = receipt("block", d.blocks[0].block_id)
    value = related()
    child["filter"] = value.model_dump(mode="json")
    d = scopes(d, parent, child)
    result = resolved(d)
    effective = result.query.receipt_filter
    assert isinstance(effective, RelationalReceiptFilterInput)
    nodes = effective.expression.children
    old, new = nodes
    assert old.scope_id == new.scope_id == new.parent_scope_id == effective.root_scope_id
    assert new.child_scope_id == new.predicate.scope_id != effective.root_scope_id
    assert old.field_version_id == FIELD
    assert (
        nodes
        == resolved(
            d.model_copy(update={"title": "Presentation only"})
        ).query.receipt_filter.expression.children
    )
    assert len({old.node_id, new.node_id, new.predicate.node_id}) == 3
    # The same source expression at two different bindings must stay independent.
    sibling = {**child, "binding_id": str(uuid4()), "order": 1}
    twice = resolved(scopes(d, parent, child, sibling)).query.receipt_filter.expression.children
    assert twice[1].child_scope_id != twice[2].child_scope_id
    with pytest.raises(ValueError, match="COMPOSER_SCOPE_LOCKED"):
        preserve_scope_locks(d, scopes(d, child))


def test_registry_bridge_mismatch_and_correlated_replacement_rejected():
    old = ReceiptFilterInput(
        registry_version_id=REGISTRY,
        expression=FlatPredicate(
            field_id="Receipt.status",
            field_version_id=FIELD,
            operator="eq",
            values=(FilterValue(data_type="string", value="completed"),),
        ),
    )
    new = related()
    for changed in (
        new.model_copy(update={"legacy_registry_version_id": None}),
        new.model_copy(update={"legacy_registry_version_id": uuid4()}),
    ):
        with pytest.raises(ValueError, match="COMPOSER_FILTER_REGISTRY_MISMATCH"):
            combine_filters([(uuid4(), old), (uuid4(), changed)])
    assert replacement_field(new) == set()
    d = document()
    parent = receipt("document", d.document_id, replaceable=True)
    parent["filter"] = new.model_dump(mode="json")
    child = receipt(
        "block",
        d.blocks[0].block_id,
        combine_mode="replace_allowed_parent_field",
        replaces=[parent["binding_id"]],
    )
    child["filter"] = new.model_dump(mode="json")
    with pytest.raises(ValueError, match="COMPOSER_REPLACEMENT_FIELD_MISMATCH"):
        resolved(scopes(d, parent, child))


def test_malformed_original_scope_is_not_repaired_by_composition():
    value = related()
    raw = value.model_dump(mode="json")
    raw["expression"]["predicate"]["scope_id"] = str(uuid4())
    bad = RelationalReceiptFilterInput.model_validate(raw)
    combined = combine_filters([(uuid4(), bad)])
    node = combined.expression.children[0]
    assert node.predicate.scope_id != node.child_scope_id


def test_v1_canonical_order_promotion_does_not_change_identity():
    from packages.contracts.analytics.columnar_filters import FlatBoolean

    old = ReceiptFilterInput(
        registry_version_id=REGISTRY,
        expression=FlatPredicate(
            field_id="Receipt.status",
            field_version_id=FIELD,
            operator="eq",
            values=(FilterValue(data_type="string", value="completed"),),
        ),
    )
    predicates = (old.expression, old.expression.model_copy(update={"operator": "ne"}))
    left = old.model_copy(update={"expression": FlatBoolean(kind="and", children=predicates)})
    right = old.model_copy(
        update={"expression": FlatBoolean(kind="and", children=tuple(reversed(predicates)))}
    )
    a, b = uuid4(), uuid4()
    new = related()
    assert combine_filters([(a, left), (b, new)]) == combine_filters(
        [(a, right), (b, new)]
    )


def test_presentation_only_source_replacement_preserves_effective_v2_identity():
    from packages.contracts.presentation.composer import ComposerDefinitionV1

    d = document()
    inherited = receipt("document", d.document_id)
    value = related()
    inherited["filter"] = value.model_dump(mode="json")
    raw = d.model_dump(mode="json")
    raw["definitions"][0]["query"]["receipt_filter"] = value.model_dump(mode="json")
    d = scopes(ComposerDefinitionV1.model_validate(raw), inherited)
    before = resolved(d)
    raw = d.model_dump(mode="json")
    replacement = str(uuid4())
    raw["definitions"].append({**raw["definitions"][0], "definition_id": replacement})
    raw["blocks"][0]["source"]["definition_id"] = replacement
    raw["blocks"][0]["presentation"]["title"] = "Renamed only"
    after = resolved(ComposerDefinitionV1.model_validate(raw))
    assert after.query == before.query
    assert after.dependency_hash == before.dependency_hash


def test_duplicate_under_inherited_v2_constraint_reuses_effective_identity():
    from packages.contracts.presentation.composer import duplicate_block
    from packages.presentation.domain.scopes import resolve_scope

    d = document()
    inherited = receipt("document", d.document_id)
    inherited["filter"] = related().model_dump(mode="json")
    d = scopes(d, inherited)
    before = resolved(d)
    copied = duplicate_block(
        d, d.blocks[0].block_id, section_id=d.blocks[0].section_id, order=1,
        placement=d.blocks[0].placement.model_copy(update={"row": 1}),
    )
    after = resolve_scope(copied, copied.scopes, copied.blocks[-1].block_id)
    assert after.query == before.query
    assert after.dependency_hash == before.dependency_hash
