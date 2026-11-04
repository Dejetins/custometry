"""The versioned and legacy comparison controls share the same inheritance lock."""

from uuid import uuid4
import pytest
from packages.contracts.presentation.composer import ComposerDefinitionV1
from packages.presentation.domain.scopes import resolve_scope
from tests.contract.presentation.test_composer_scopes import document


def context(kind, identifier, **values):
    return {
        "binding_id": str(uuid4()),
        "target": {"kind": kind, "id": str(identifier)},
        "context": values,
    }


def settings(mode="previous_period"):
    return {
        "mode": mode,
        "incomplete_period_policy": "exclude",
        **({"previous_period_basis": "local_date_duration"} if mode == "previous_period" else {}),
    }


def resolve(d, contexts):
    d = ComposerDefinitionV1.model_validate(
        {
            **d.model_dump(mode="json"),
            "scopes": {"schema_version": "composer-scopes/v2", "contexts": contexts},
        }
    )
    return resolve_scope(d, d.scopes, d.blocks[0].block_id)


def test_new_comparison_inherits_and_explicit_none_masks_parent():
    d = document()
    parent = context("document", d.document_id, time_comparison=settings())
    result = resolve(d, [parent])
    assert (
        result.query.alignment == "none" and result.query.time_comparison.mode == "previous_period"
    )
    child = context("block", d.blocks[0].block_id, time_comparison=settings("none"))
    result = resolve(d, [parent, child])
    assert result.query.time_comparison.mode == "none"
    assert [o.state for o in result.origins] == ["overridden", "applied"]


def test_legacy_override_clears_new_settings_and_new_override_clears_legacy():
    d = document()
    parent = context("document", d.document_id, time_comparison=settings())
    child = context("block", d.blocks[0].block_id, alignment="previous_year_same_dates")
    result = resolve(d, [parent, child])
    assert (
        result.query.time_comparison is None
        and result.query.alignment == "previous_year_same_dates"
    )
    result = resolve(
        d,
        [
            context("document", d.document_id, alignment="previous_year_same_dates"),
            context("block", d.blocks[0].block_id, time_comparison=settings()),
        ],
    )
    assert (
        result.query.alignment == "none" and result.query.time_comparison.mode == "previous_period"
    )


def test_lock_cannot_be_bypassed_by_switching_between_comparison_contracts():
    d = document()
    new = context("document", d.document_id, time_comparison=settings())
    new["locked_fields"] = ["time_comparison"]
    old = context("document", d.document_id, alignment="none")
    old["locked_fields"] = ["alignment"]
    for parent, child in [
        (new, context("block", d.blocks[0].block_id, alignment="none")),
        (old, context("block", d.blocks[0].block_id, time_comparison=settings())),
    ]:
        with pytest.raises(ValueError, match="CONTEXT_LOCKED"):
            resolve(d, [parent, child])


def test_explicit_local_fiscal_basis_beats_parent_unless_locked():
    d = document()
    parent = context("document", d.document_id, calendar_basis="calendar")
    child = context(
        "block",
        d.blocks[0].block_id,
        calendar_basis="fiscal",
        time_comparison={
            "mode": "previous_year_fiscal_period",
            "incomplete_period_policy": "exclude",
        },
    )
    effective = resolve(d, [parent, child])
    assert effective.query.calendar_basis == "fiscal"
    assert effective.query.time_comparison.mode == "previous_year_fiscal_period"
    parent["locked_fields"] = ["calendar_basis"]
    with pytest.raises(ValueError, match="CONTEXT_LOCKED"):
        resolve(d, [parent, child])


def test_explicit_calendar_adoption_obeys_parent_lock():
    d = document()
    original = d.definitions[0].query.calendar_ref.model_dump(mode="json")
    adopted = {"version_id": str(uuid4()), "content_hash": "f" * 64}
    parent = context("document", d.document_id, calendar_ref=original)
    child = context("block", d.blocks[0].block_id, calendar_ref=adopted)
    assert resolve(d, [parent, child]).query.calendar_ref.model_dump(mode="json") == adopted
    parent["locked_fields"] = ["calendar_ref"]
    with pytest.raises(ValueError, match="CONTEXT_LOCKED"):
        resolve(d, [parent, child])
