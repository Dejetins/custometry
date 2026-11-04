"""Optional selection proof survives serialization without changing old result bytes."""

import importlib.util
import sys
from pathlib import Path
from uuid import uuid4
import pytest
from pydantic import ValidationError
from packages.contracts.analytics.workspace import WorkspaceRunRequest, WorkspaceResultV2
from packages.contracts.analytics.retail_filter import ReceiptSelectionEvidence
from packages.analytics_core.application.workspace_calculation import build_workspace
from tests.unit.analytics.test_temporal_projection import configured
from tests.contract.presentation.test_relational_receipt_scopes import related


def test_unknown_selection_and_comparison_disclosure_are_hashed_and_preserved():
    request, source, inputs, access, calendar = configured()
    before = build_workspace(request, source, inputs, access, calendar)
    selection = ReceiptSelectionEvidence(
        request_hash="a" * 64,
        matched_count=2,
        not_matched_count=0,
        unknown_count=1,
        authorized_count=3,
        limitation_codes=("RELATIONSHIP_HISTORY_INCOMPLETE",),
    )
    filtered = request.model_copy(update={"receipt_filter": related()})
    result = build_workspace(
        filtered,
        {
            **source,
            "receipt_filter_hash": "a" * 64,
            "receipt_selection": selection.model_dump(mode="json"),
        },
        inputs,
        access,
        calendar,
    )
    assert result["receipt_selection"]["count_scope"] == "authorized_dataset"
    assert result["receipt_selection"]["unknown_count"] == 1
    assert "RECEIPT_MEMBERSHIP_UNKNOWN" in result["trust"]["reason_codes"]
    assert "RECEIPT_MEMBERSHIP_UNKNOWN" in result["temporal_v2"]["limitation_codes"]
    assert result["temporal_v2"]["comparability_status"] == "descriptive"
    assert result["temporal_v2"]["content_hash"] != before["temporal_v2"]["content_hash"]
    # Manifest commit is an integration concern. Bind a synthetic immutable ref
    # solely to test the exact strict result serializer round trip here.
    result["manifest"] = {"artifact_id": str(uuid4()), "content_hash": "b" * 64}
    parsed = WorkspaceResultV2.model_validate(result)
    assert (
        WorkspaceResultV2.model_validate_json(parsed.model_dump_json()).receipt_selection
        == selection
    )
    before["manifest"] = result["manifest"]
    assert "receipt_selection" not in WorkspaceResultV2.model_validate(before).model_dump(
        mode="json"
    )


def test_actual_pre_ms019_reader_rejects_v2_query_and_selection_result():
    path = Path(".codex/delivery/evidence/MS-019/preparation/workspace-before.py")
    spec = importlib.util.spec_from_file_location("ms019_old_workspace", path)
    old = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = old
    spec.loader.exec_module(old)
    request, source, inputs, access, calendar = configured()
    assert old.WorkspaceRunRequest.model_validate(request.model_dump(mode="json")).model_dump(
        mode="json"
    ) == request.model_dump(mode="json")
    filtered = request.model_copy(update={"receipt_filter": related()})
    with pytest.raises(ValidationError):
        old.WorkspaceRunRequest.model_validate(filtered.model_dump(mode="json"))
    assert (
        WorkspaceRunRequest.model_validate_json(filtered.model_dump_json()).receipt_filter
        == filtered.receipt_filter
    )
    result = build_workspace(request, source, inputs, access, calendar)
    result["manifest"] = {"artifact_id": str(uuid4()), "content_hash": "b" * 64}
    old.WorkspaceResultV2.model_validate(result)
    result["receipt_selection"] = ReceiptSelectionEvidence(
        request_hash="a" * 64,
        matched_count=0,
        not_matched_count=0,
        unknown_count=0,
        authorized_count=0,
        limitation_codes=(),
    ).model_dump(mode="json")
    with pytest.raises(ValidationError):
        old.WorkspaceResultV2.model_validate(result)
