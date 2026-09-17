from copy import deepcopy
from typing import Any
from uuid import uuid4
import pytest
from pydantic import ValidationError
from packages.contracts.presentation import PresentationFailure, SaveRequest
from packages.presentation.domain.reports import composition, validate_result, versioned


def test_explicit_contract_and_closed_save_surface() -> None:
    with pytest.raises(ValidationError):
        SaveRequest.model_validate(
            {"title": "Unsafe", "result_id": str(uuid4()), "option": {"formatter": "<script>"}}
        )
    invalid_values: list[dict[str, Any]] = [
        {},
        {"schema_version": "other"},
        {"schema_version": "sales-report/v1", "lineage": {}},
    ]
    for value in invalid_values:
        with pytest.raises(PresentationFailure, match="INCOMPLETE_RESULT_BINDING"):
            validate_result(value)


def test_content_addressed_defaults_never_mutate_input() -> None:
    original = {"name": "System", "tokens": {"series-primary": "#858BFF"}}
    source = deepcopy(original)
    a = versioned("brand_profile", source)
    assert source == original
    assert a == versioned("brand_profile", original)
    b = versioned("brand_profile", {**source, "name": "Changed"})
    assert a["reference"] != b["reference"]


def test_hierarchy_and_saved_filter_precedence_are_stable() -> None:
    report, workspace, owner = uuid4(), uuid4(), uuid4()
    result: dict[str, Any] = {
        "schema_version": "sales-report/v1",
        "result_id": str(uuid4()),
        "manifest": {},
        "parameters": {"eligibility": {"locked": True}},
        "metrics": [],
        "mart": {"output_grain": ["date"]},
        "daily": [],
        "policy_hash": "policy",
    }
    refs = {
        "chart_spec": {"reference": {"id": str(uuid4()), "content_hash": "a" * 64}},
        "brand_profile": {"reference": {"id": str(uuid4())}},
    }
    first = composition(report, uuid4(), workspace, owner, "One", result, refs)
    second = composition(report, uuid4(), workspace, owner, "Two", result, refs)
    assert first["default_page_id"] == second["default_page_id"]
    assert [b["block_id"] for b in first["blocks"]] == [b["block_id"] for b in second["blocks"]]
    duplicate = composition(uuid4(), uuid4(), workspace, owner, "Copy", result, refs)
    assert duplicate["default_page_id"] != first["default_page_id"]
    assert first["filter_scope_bindings"][0]["combine_mode"] == "intersect"
    assert first["filter_scope_bindings"][0]["precedence"][:2] == ["security", "system_locked"]
