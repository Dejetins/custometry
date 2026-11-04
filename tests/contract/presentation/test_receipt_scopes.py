"""Receipt hierarchy, preserved reader behavior and structural lock regressions."""

import importlib.util
import sys
from pathlib import Path
from uuid import uuid4

import pytest
from pydantic import ValidationError
from packages.contracts.presentation.composer import ComposerDefinitionV1, duplicate_block
from packages.contracts.presentation.scopes import ComposerScopesV1, ComposerScopesV2
from packages.presentation.domain.scopes import (
    resolve_scope,
    preserve_scope_locks,
    validate_scope_graph,
)
from tests.contract.presentation.test_composer_scopes import document, binding, DATASET

REGISTRY = uuid4()
FIELD = uuid4()


def receipt(kind, identifier, value="completed", **kwargs):
    return {
        "binding_id": str(uuid4()),
        "target": {"kind": kind, "id": str(identifier)},
        "semantic_dataset_version_id": str(DATASET),
        "order": 0,
        "filter": {
            "registry_version_id": str(REGISTRY),
            "expression": {
                "kind": "predicate",
                "field_id": "Receipt.status",
                "field_version_id": str(FIELD),
                "operator": "eq",
                "values": [{"data_type": "string", "value": value}],
            },
        },
        **kwargs,
    }


def scopes(d, *receipts, stores=()):
    s = ComposerScopesV2(receipt_filters=list(receipts), filters=list(stores))
    return ComposerDefinitionV1.model_validate(
        {**d.model_dump(mode="json"), "scopes": s.model_dump(mode="json")}
    )


def resolved(d):
    return resolve_scope(d, d.scopes, d.blocks[0].block_id)


def test_all_ancestors_intersect_and_preserve_block_local_input():
    d = document()
    bindings = [
        receipt(kind, identifier, value=str(i))
        for i, (kind, identifier) in enumerate(
            [
                ("document", d.document_id),
                ("chapter", d.chapters[0].chapter_id),
                ("page", d.pages[0].page_id),
                ("section", d.sections[0].section_id),
                ("section", d.sections[1].section_id),
                ("block", d.blocks[0].block_id),
            ]
        )
    ]
    raw = d.model_dump(mode="json")
    raw["definitions"][0]["query"]["receipt_filter"] = receipt("document", d.document_id, "local")[
        "filter"
    ]
    d = scopes(ComposerDefinitionV1.model_validate(raw), *bindings)
    result = resolved(d)
    assert [c.values[0].value for c in result.query.receipt_filter.expression.children] == [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "local",
    ]
    assert len(result.origins) == 6 and all(o.field == "Receipt" for o in result.origins)
    moved = d.model_copy(update={"title": "Presentation only"})
    assert resolved(moved).dependency_hash == result.dependency_hash


def test_allowed_single_field_replacement_and_rejected_mixed_field_dataset_registry():
    d = document()
    parent = receipt("document", d.document_id, replaceable=True)
    child = receipt(
        "block",
        d.blocks[0].block_id,
        "other",
        combine_mode="replace_allowed_parent_field",
        replaces=[parent["binding_id"]],
    )
    result = resolved(scopes(d, parent, child))
    assert result.query.receipt_filter.expression.values[0].value == "other"
    assert [o.state for o in result.origins] == ["overridden", "applied"]
    for mutation in ["dataset", "registry", "field", "multi"]:
        import copy

        changed = copy.deepcopy(child)
        if mutation == "dataset":
            changed["semantic_dataset_version_id"] = str(uuid4())
        elif mutation == "registry":
            changed["filter"]["registry_version_id"] = str(uuid4())
        elif mutation == "field":
            changed["filter"]["expression"]["field_id"] = "Receipt.currency"
        else:
            other = copy.deepcopy(changed["filter"]["expression"])
            other["field_id"] = "Receipt.currency"
            changed["filter"]["expression"] = {
                "kind": "and",
                "children": [changed["filter"]["expression"], other],
            }
        with pytest.raises(ValueError, match="REPLACEMENT_FIELD_MISMATCH"):
            resolved(scopes(d, parent, changed))
    with pytest.raises(ValueError, match="SCOPE_LOCKED"):
        resolved(scopes(d, {**parent, "replaceable": False, "locked": True}, child))
    with pytest.raises(ValueError, match="REPLACEMENT_FIELD_MISMATCH"):
        resolved(
            scopes(
                d,
                child,
                stores=[
                    binding(
                        "document",
                        d.document_id,
                        ["a"],
                        binding_id=parent["binding_id"],
                        replaceable=True,
                    )
                ],
            )
        )


def test_saved_locks_cannot_be_removed_changed_or_escaped_by_move():
    d = document()
    lock = receipt("section", d.sections[1].section_id, locked=True)
    before = scopes(d, lock)
    for after in [
        scopes(d),
        scopes(d, {**lock, "locked": False}),
        scopes(d, {**lock, "target": {"kind": "block", "id": str(d.blocks[0].block_id)}}),
        before.model_copy(
            update={
                "blocks": [
                    before.blocks[0].model_copy(update={"section_id": d.sections[0].section_id})
                ]
            }
        ),
    ]:
        with pytest.raises(ValueError, match="SCOPE_LOCKED"):
            preserve_scope_locks(before, after)
    preserve_scope_locks(before, before.model_copy(update={"title": "Changed title"}))


def test_link_is_direct_and_cycles_reject_and_duplication_keeps_constraints():
    d = document()
    d = duplicate_block(
        d,
        d.blocks[0].block_id,
        section_id=d.sections[1].section_id,
        order=1,
        placement=d.blocks[0].placement.model_copy(update={"row": 1}),
    )
    source, target = d.blocks[0], d.blocks[-1]
    donor = receipt("block", source.block_id, linked_target_block_ids=[str(target.block_id)])
    d = scopes(d, donor)
    linked = resolve_scope(d, d.scopes, target.block_id)
    assert linked.origins[0].state == "linked"
    copied = duplicate_block(
        d,
        target.block_id,
        section_id=d.sections[1].section_id,
        order=2,
        placement=d.blocks[0].placement.model_copy(update={"row": 2}),
    )
    local = copied.scopes.receipt_filters[-1]
    assert local.target.id == copied.blocks[-1].block_id and not local.linked_target_block_ids
    assert local.filter == copied.scopes.receipt_filters[0].filter
    reverse = receipt("block", target.block_id, linked_target_block_ids=[str(source.block_id)])
    with pytest.raises(ValueError, match="LINK_CYCLE"):
        validate_scope_graph(scopes(d, donor, reverse), scopes(d, donor, reverse).scopes)


def test_registry_dataset_and_mixed_id_order_reject():
    d = document()
    r = receipt("document", d.document_id)
    with pytest.raises(ValueError, match="DATASET_MISMATCH"):
        resolved(scopes(d, {**r, "semantic_dataset_version_id": str(uuid4())}))
    r2 = receipt("block", d.blocks[0].block_id)
    r2["filter"]["registry_version_id"] = str(uuid4())
    with pytest.raises(ValueError, match="REGISTRY_MISMATCH"):
        resolved(scopes(d, r, r2))
    with pytest.raises(ValidationError, match="DUPLICATE_SCOPE_ORDER"):
        scopes(d, r, stores=[binding("document", d.document_id, ["a"])])


def load(name, filename):
    spec = importlib.util.spec_from_file_location(
        name, Path(".codex/delivery/evidence/MS-012/preparation") / filename
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_actual_v1_reader_resolver_and_unaffected_v2_identity():
    old_reader = load("ms012_old_scopes", "scopes-before.py")
    old_resolver = load("ms012_old_resolver", "scope-resolver-before.py")
    d = document()
    old = ComposerScopesV1(filters=[binding("document", d.document_id, ["a"])])
    assert (
        old_reader.ComposerScopesV1.model_validate_json(old.model_dump_json()).model_dump_json()
        == old.model_dump_json()
    )
    assert old_resolver.resolve_scope(d, old, d.blocks[0].block_id) == resolve_scope(
        d, old, d.blocks[0].block_id
    )
    upgraded = ComposerScopesV2(filters=old.filters)
    assert resolve_scope(d, upgraded, d.blocks[0].block_id) == resolve_scope(
        d, old, d.blocks[0].block_id
    )
    with pytest.raises(ValidationError):
        old_reader.ComposerScopesV1.model_validate_json(upgraded.model_dump_json())
    raw = d.model_dump(mode="json")
    raw["scopes"] = {"filters": [binding("document", d.document_id, ["a"])]}
    assert isinstance(ComposerDefinitionV1.model_validate(raw).scopes, ComposerScopesV1)
