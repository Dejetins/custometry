"""V3 composition preserves aggregate policies while rebasing only local scopes."""

from uuid import uuid4
import pytest
from pydantic import ValidationError
from packages.contracts.analytics.retail_aggregate import AggregateReceiptFilterInput
from packages.contracts.analytics.retail_relational import RelationalReceiptFilterInput
from packages.contracts.analytics.aggregate_filters import (
    AggregateCompare,
    ScopedCount,
    AggregateWindow,
    AggregateScalar,
)
from packages.contracts.semantic.filter_aggregates import FilterCountVersion, AggregateFieldRef
from packages.contracts.presentation.composer import ComposerDefinitionV1, duplicate_block
from packages.presentation.domain.receipt_scopes import replacement_field
from packages.presentation.domain.scopes import resolve_scope, preserve_scope_locks
from tests.contract.presentation.test_relational_receipt_scopes import related
from tests.contract.presentation.test_receipt_scopes import document, receipt, scopes, resolved


def aggregate():
    v2 = related()
    node = v2.expression
    definition = FilterCountVersion(
        count_id="items.rows",
        version_id=uuid4(),
        relationship_version_id=node.relationship_version_id,
        child_entity="ReceiptItem",
        kind="count",
        grain_fields=(AggregateFieldRef(field_id="ReceiptItem.line_id", version_id=uuid4()),),
        unit="items",
        null_policy="unknown",
        time_entity="parent",
        time_field=AggregateFieldRef(field_id="Receipt.receipt_date", version_id=uuid4()),
    )
    left = ScopedCount(
        parent_scope_id=v2.root_scope_id,
        child_scope_id=node.child_scope_id,
        child_entity=node.child_entity,
        relationship_id=node.relationship_id,
        relationship_version_id=node.relationship_version_id,
        definition=definition,
        window=AggregateWindow(
            starts_at="2025-01-01T00:00:00Z",
            ends_at="2025-02-01T00:00:00Z",
            observation_as_of="2026-01-01T12:00:00Z",
            knowledge_as_of="2026-01-01T12:00:00Z",
        ),
        predicate=node.predicate,
    )
    v3 = AggregateReceiptFilterInput(
        root_scope_id=v2.root_scope_id,
        registry_versions=v2.registry_versions,
        legacy_registry_version_id=v2.legacy_registry_version_id,
        expression=AggregateCompare(
            node_id=uuid4(),
            scope_id=v2.root_scope_id,
            left=left,
            operator="ge",
            right=AggregateScalar(value="1", unit="items"),
        ),
    )
    return v2, v3


def test_mixed_v1_v2_v3_preserves_policies_and_independent_correlation():
    d = document()
    v2, v3 = aggregate()
    old = receipt("document", d.document_id)
    correlated = receipt("page", d.pages[0].page_id)
    correlated["filter"] = v2.model_dump(mode="json")
    counted = receipt("block", d.blocks[0].block_id, locked=True)
    counted["filter"] = v3.model_dump(mode="json")
    d = scopes(d, old, correlated, counted)
    result = resolved(d).query.receipt_filter
    assert isinstance(result, AggregateReceiptFilterInput)
    count = result.expression.children[-1]
    assert count.left.definition == v3.expression.left.definition
    assert count.left.window == v3.expression.left.window
    assert count.left.child_scope_id == count.left.predicate.scope_id
    assert count.left.parent_scope_id == count.scope_id == result.root_scope_id
    assert count.left.child_scope_id != result.expression.children[1].child_scope_id
    assert replacement_field(v3) == set()
    with pytest.raises(ValueError, match="SCOPE_LOCKED"):
        preserve_scope_locks(d, scopes(d, old, correlated))
    with pytest.raises(ValidationError):
        RelationalReceiptFilterInput.model_validate(
            {**result.model_dump(mode="json"), "schema_version": "receipt-filter/v2"}
        )


def test_base_source_replacement_and_duplicate_preserve_v3_identity():
    d = document()
    _, v3 = aggregate()
    parent = receipt("document", d.document_id)
    parent["filter"] = v3.model_dump(mode="json")
    raw = d.model_dump(mode="json")
    raw["definitions"][0]["query"]["receipt_filter"] = v3.model_dump(mode="json")
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
    replacement = str(uuid4())
    raw["definitions"].append({**raw["definitions"][0], "definition_id": replacement})
    raw["blocks"][0]["source"]["definition_id"] = replacement
    raw["blocks"][0]["presentation"]["title"] = "Only presentation"
    assert resolved(ComposerDefinitionV1.model_validate(raw)).query == before.query
