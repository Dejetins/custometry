"""Pure C04 scope proof; no provider, API or runtime authorization claim."""

from copy import deepcopy
from uuid import UUID, uuid4
import pytest
from pydantic import ValidationError
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.presentation.composer import ComposerDefinitionV1
from packages.contracts.presentation.scopes import ComposerScopesV1
from packages.contracts.semantic.store_filters import StoreFilterV1
from packages.presentation.domain.scopes import resolve_scope, validate_scope_graph
from packages.analytics_core.application.store_scopes import resolve_store_filters
from tests.contract.presentation.test_composer import fixture


DATASET = UUID("fddadad4-1234-4000-9000-123456789012")


def document():
    raw = fixture()
    raw["definitions"][0]["query"]["semantic_dataset_version_id"] = str(DATASET)
    chapter, inner = str(uuid4()), str(uuid4())
    raw["chapters"] = [{"chapter_id": chapter, "order": 0, "title": "Chapter"}]
    raw["pages"][0]["chapter_id"] = chapter
    raw["sections"].append(
        {
            "section_id": inner,
            "page_id": raw["pages"][0]["page_id"],
            "parent_section_id": raw["sections"][0]["section_id"],
            "order": 0,
            "title": "Nested",
        }
    )
    raw["blocks"][0]["section_id"] = inner
    return ComposerDefinitionV1.model_validate(raw)


def select(values):
    return {"kind": "store_in", "values": values}


def binding(kind, identifier, values, **kwargs):
    return {
        "binding_id": str(uuid4()),
        "target": {"kind": kind, "id": str(identifier)},
        "order": 0,
        "filter": {"semantic_dataset_version_id": str(DATASET), "expression": select(values)},
        **kwargs,
    }


def context(kind, identifier, **fields):
    return {
        "binding_id": str(uuid4()),
        "target": {"kind": kind, "id": str(identifier)},
        "context": fields,
    }


def effective(d, raw, block=0, allowed=("a", "b", "c"), mandatory=()):
    resolved = resolve_scope(d, ComposerScopesV1.model_validate(raw), d.blocks[block].block_id)
    return resolved, resolve_store_filters(
        resolved.filters, allowed=frozenset(allowed), dataset_id=DATASET, mandatory=mandatory
    )


def test_five_scope_intersection_nested_order_and_locked_provenance():
    d = document()
    bindings = [
        binding("document", d.document_id, ["a", "b", "c"]),
        binding("chapter", d.chapters[0].chapter_id, ["a", "b"]),
        binding("page", d.pages[0].page_id, ["a", "b"]),
        binding("section", d.sections[0].section_id, ["a", "b"]),
        binding("section", d.sections[1].section_id, ["b"], locked=True),
        binding("block", d.blocks[0].block_id, ["a", "b"]),
    ]
    before = d.model_dump_json()
    r, stores = effective(d, {"filters": list(reversed(bindings))})
    assert stores == ["b"]
    assert [str(o.binding_id) for o in r.origins] == [b["binding_id"] for b in bindings]
    assert r.origins[4].state == "locked"
    assert d.model_dump_json() == before
    assert r.query == d.definitions[0].query


def test_defaults_per_field_override_and_context_locks():
    d = document()
    root = context("document", d.document_id, grain="month", alignment="previous_year_same_dates")
    local = context(
        "block",
        d.blocks[0].block_id,
        grain="day",
        period={"starts_on": "2025-02-01", "ends_on": "2025-02-28"},
    )
    r, _ = effective(d, {"contexts": [local, root]})
    assert r.query.grain == "day" and r.query.alignment == "previous_year_same_dates"
    assert str(r.query.common.starts_on) == "2025-02-01"
    assert r.origins[0].state == "overridden"
    root["locked_fields"] = ["grain"]
    with pytest.raises(ValueError, match="COMPOSER_CONTEXT_LOCKED"):
        effective(d, {"contexts": [root, local]})


def test_replace_only_explicit_unlocked_ancestor_keeps_source_constraint():
    d = document()
    root = binding("document", d.document_id, ["a"], replaceable=True)
    local = binding(
        "block",
        d.blocks[0].block_id,
        ["b", "c"],
        combine_mode="replace_allowed_parent_field",
        replaces=[root["binding_id"]],
    )
    r, stores = effective(d, {"filters": [local, root]}, mandatory=[["b"]])
    assert stores == ["b"] and r.origins[0].state == "overridden"
    root["replaceable"] = False
    with pytest.raises(ValueError, match="COMPOSER_SCOPE_LOCKED"):
        effective(d, {"filters": [root, local]})
    root["locked"] = True
    with pytest.raises(ValueError, match="COMPOSER_SCOPE_LOCKED"):
        effective(d, {"filters": [root, local]})


def test_link_intersects_once_after_ancestry_and_does_not_copy_implicit_context():
    d = document()
    root = binding(
        "document", d.document_id, ["a", "b"], linked_target_block_ids=[str(d.blocks[1].block_id)]
    )
    donor = binding(
        "block",
        d.blocks[0].block_id,
        ["b", "c"],
        linked_target_block_ids=[str(d.blocks[1].block_id)],
    )
    contexts = [context("block", d.blocks[0].block_id, grain="day")]
    r, stores = effective(d, {"filters": [donor, root], "contexts": contexts}, block=1)
    assert stores == ["b"] and len(r.filters) == 2
    assert r.origins[-1].state == "linked"
    assert r.query.grain == d.definitions[0].query.grain


@pytest.mark.parametrize(
    "case",
    [
        "cycle",
        "self",
        "dangling",
        "wrong_kind",
        "id_collision",
        "nonancestor",
        "duplicate_order",
        "duplicate_id",
    ],
)
def test_graph_rejects_invalid_targets_before_evaluation(case):
    d = document()
    left = binding(
        "block", d.blocks[0].block_id, ["a"], linked_target_block_ids=[str(d.blocks[1].block_id)]
    )
    right = binding("block", d.blocks[1].block_id, ["a"])
    if case == "cycle":
        right["linked_target_block_ids"] = [str(d.blocks[0].block_id)]
    elif case == "self":
        left["linked_target_block_ids"] = [str(d.blocks[0].block_id)]
    elif case == "dangling":
        left["linked_target_block_ids"] = [str(uuid4())]
    elif case == "wrong_kind":
        left["target"]["kind"] = "page"
    elif case == "id_collision":
        left["binding_id"] = str(d.document_id)
    elif case == "nonancestor":
        left.update(
            linked_target_block_ids=[],
            combine_mode="replace_allowed_parent_field",
            replaces=[right["binding_id"]],
        )
        right["replaceable"] = True
    elif case == "duplicate_order":
        right["target"] = left["target"]
    elif case == "duplicate_id":
        right["binding_id"] = left["binding_id"]
    with pytest.raises((ValueError, ValidationError)):
        validate_scope_graph(d, ComposerScopesV1.model_validate({"filters": [left, right]}))


def test_boolean_complement_empty_set_and_no_short_circuit_permission_bypass():
    def run(expression, mandatory=()):
        return resolve_store_filters(
            [
                StoreFilterV1.model_validate(
                    {"semantic_dataset_version_id": str(DATASET), "expression": expression}
                )
            ],
            allowed=frozenset(["a", "b", "c"]),
            dataset_id=DATASET,
            mandatory=mandatory,
        )

    assert run({"kind": "not", "child": select(["a"])}, [["a", "b"]]) == ["b"]
    assert run({"kind": "and", "children": [select(["a"]), select(["b"])]}) == []
    assert run({"kind": "or", "children": [select([]), select(["b", "a", "a"])]}) == ["a", "b"]
    assert run({"kind": "not", "child": select([])}) == ["a", "b", "c"]
    assert run(select(["a"]), [[]]) == []
    for expr in (
        {"kind": "and", "children": [select([]), select(["forbidden"])]},
        {"kind": "or", "children": [select(["a", "b", "c"]), select(["forbidden"])]},
        {"kind": "not", "child": select(["forbidden"])},
    ):
        with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
            run(expr)
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        run(select([]), [["forbidden"]])


@pytest.mark.parametrize(
    "expression",
    [
        {"kind": "store_in", "field": "channel_id", "values": ["a"]},
        {"kind": "sql", "value": "1=1"},
        {"kind": "exists", "entity": "Receipt"},
        {"kind": "and", "children": []},
        {"kind": "store_in", "values": [True]},
    ],
)
def test_unsupported_expressions_are_rejected_not_downgraded(expression):
    with pytest.raises(ValidationError):
        StoreFilterV1.model_validate(
            {"semantic_dataset_version_id": str(DATASET), "expression": expression}
        )


def test_dependency_hash_boolean_order_canonical_layout_independent_and_semantic_sensitive():
    d = document()
    f = binding("document", d.document_id, ["a"])
    f["filter"]["expression"] = {"kind": "or", "children": [select(["a"]), select(["b"])]}
    scope = {"filters": [f]}
    r, _ = effective(d, scope)
    swapped = deepcopy(scope)
    swapped["filters"][0]["filter"]["expression"]["children"].reverse()
    assert effective(d, swapped)[0].dependency_hash == r.dependency_hash
    raw = d.model_dump(mode="json")
    raw["title"] = "Layout only"
    raw["blocks"][0]["presentation"]["density"] = "compact"
    assert (
        effective(ComposerDefinitionV1.model_validate(raw), scope)[0].dependency_hash
        == r.dependency_hash
    )
    swapped["filters"][0]["filter"]["expression"]["children"] = [select(["c"])]
    assert effective(d, swapped)[0].dependency_hash != r.dependency_hash
    other = deepcopy(scope)
    other["filters"][0]["binding_id"] = str(uuid4())
    assert effective(d, other)[0].dependency_hash != r.dependency_hash


def test_empty_envelope_preserves_exact_legacy_query_and_no_digest():
    d = document()
    before = d.model_dump_json()
    r, _ = effective(d, {})
    assert r.query.model_dump_json() == d.definitions[0].query.model_dump_json()
    assert r.dependency_hash is None and r.filters == [] and r.origins == []
    assert d.model_dump_json() == before
    schema = ComposerScopesV1.model_json_schema()
    assert schema["additionalProperties"] is False
    assert (
        ComposerScopesV1.model_validate_json(ComposerScopesV1().model_dump_json())
        == ComposerScopesV1()
    )


def test_replacement_cannot_resurrect_an_already_overridden_parent():
    d = document()
    a = binding("document", d.document_id, ["a"], replaceable=True)
    b = binding(
        "page",
        d.pages[0].page_id,
        ["b"],
        combine_mode="replace_allowed_parent_field",
        replaces=[a["binding_id"]],
        replaceable=True,
    )
    c = binding(
        "block",
        d.blocks[0].block_id,
        ["c"],
        combine_mode="replace_allowed_parent_field",
        replaces=[a["binding_id"]],
    )
    with pytest.raises(ValueError, match="COMPOSER_REPLACEMENT_NOT_ACTIVE"):
        effective(d, {"filters": [a, b, c]})


def test_store_scope_is_pinned_to_the_semantic_dataset():
    d = document()
    f = binding("document", d.document_id, ["a"])
    f["filter"]["semantic_dataset_version_id"] = str(uuid4())
    with pytest.raises(ValueError, match="COMPOSER_FILTER_DATASET_MISMATCH"):
        effective(d, {"filters": [f]})
    with pytest.raises(AnalyticsFailure, match="COMPOSER_FILTER_DATASET_MISMATCH"):
        resolve_store_filters(
            [StoreFilterV1.model_validate(f["filter"])],
            allowed=frozenset(["a"]),
            dataset_id=DATASET,
            mandatory=[],
        )


def test_duplicate_preserves_local_constraints_with_fresh_binding_identity():
    from packages.contracts.presentation.composer import duplicate_block, GridPlacement
    d = document()
    original = d.blocks[0]
    local = binding("block", original.block_id, ["a"], locked=True)
    d = d.model_copy(update={"scopes": ComposerScopesV1.model_validate({"filters": [local], "contexts": [context("block", original.block_id, grain="month")]})})
    copied = duplicate_block(d, original.block_id, section_id=original.section_id, order=1, placement=GridPlacement(column=0, row=2, span=12))
    assert copied.scopes is not None
    clone = copied.blocks[-1]
    copied_filter = next(f for f in copied.scopes.filters if f.target.id == clone.block_id)
    assert copied_filter.binding_id != copied.scopes.filters[0].binding_id
    assert copied_filter.locked and copied_filter.linked_target_block_ids == []
    resolved = resolve_scope(copied, copied.scopes, clone.block_id)
    assert resolved.query.grain == "month"
    assert resolve_store_filters(resolved.filters, allowed=frozenset({"a", "b"}), dataset_id=DATASET, mandatory=()) == ["a"]


def test_persisted_lock_cannot_be_escaped_by_moving_surviving_block():
    from packages.presentation.domain.scopes import preserve_scope_locks
    d = document()
    section = d.blocks[0].section_id
    scoped = d.model_copy(update={"scopes": ComposerScopesV1.model_validate({"filters": [binding("section", section, ["a"], locked=True)]})})
    moved = scoped.model_copy(update={"blocks": [scoped.blocks[0].model_copy(update={"section_id": scoped.sections[0].section_id})]})
    with pytest.raises(ValueError, match="COMPOSER_SCOPE_LOCKED"):
        preserve_scope_locks(scoped, moved)
