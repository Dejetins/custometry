"""Native report creation keeps author, access and persistence boundaries explicit."""

from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock
from uuid import UUID, uuid4

import pytest
from packages.contracts.presentation import PresentationFailure
from packages.contracts.presentation.workspace import (
    NewWorkspaceRequest,
    CreatorApplyRequest,
    WorkspaceSaveRequest,
)
from packages.presentation.application.workspace import WorkspaceReportService


def setup_service() -> tuple[WorkspaceReportService, Any, Any, Any, Any]:
    workspace, actor = uuid4(), uuid4()
    repository, results, access, artifacts, calendars = (Mock() for _ in range(5))
    repository.metadata.side_effect = PresentationFailure("NOT_FOUND")

    def put_reference(workspace: UUID, actor: UUID, value: dict[str, Any]) -> dict[str, Any]:
        return value

    repository.put_reference.side_effect = put_reference
    access.resolve_resource.return_value = SimpleNamespace(
        allowed=True, permissions={"report.read", "report.manage", "analysis.read", "analysis.run"}
    )
    results.context.return_value = {
        "metrics": [
            dict(metric_id=m, version_id=str(uuid4()), content_hash="a" * 64)
            for m in ("net_revenue", "receipt_count", "average_receipt")
        ]
    }
    calendars.get_default.return_value = SimpleNamespace(
        calendar=SimpleNamespace(version_id=uuid4(), content_hash="b" * 64)
    )
    service = WorkspaceReportService(repository, results, access, artifacts, calendars)
    return service, workspace, actor, repository, access


def request(template: str = "sales") -> NewWorkspaceRequest:
    return NewWorkspaceRequest.model_validate(
        dict(
            report_id=uuid4(),
            semantic_dataset_version_id=uuid4(),
            common_context=dict(starts_on="2025-01-01", ends_on="2025-01-31", store_ids=None),
            template=template,
            locale="ru",
        )
    )


@pytest.mark.parametrize("template,count", [("blank", 0), ("sales", 3)])
def test_preparation_has_no_document_or_calculation_side_effect(template: str, count: int) -> None:
    service, workspace, actor, repository, _ = setup_service()
    definition = service.new_definition(workspace, actor, request(template), {"name": "system"})
    assert definition.creator_principal_id == actor
    assert definition.base_snapshot_ref is None
    assert len(definition.worksets[0].cards) == count
    assert (definition.selection is None) == (count == 0)
    repository.save_workspace.assert_not_called()
    service.results.apply.assert_not_called()  # type: ignore[attr-defined]


@pytest.mark.parametrize("permission", ["report.manage", "report.read", "analysis.read"])
def test_new_report_requires_current_functional_permissions(permission: str) -> None:
    service, workspace, actor, _, access = setup_service()
    access.resolve_resource.return_value.permissions.remove(permission)
    with pytest.raises(PresentationFailure, match="FORBIDDEN"):
        service.new_definition(workspace, actor, request(), {})


def test_native_apply_rejects_forged_creator_and_existing_report() -> None:
    service, workspace, actor, repository, _ = setup_service()
    definition = service.new_definition(workspace, actor, request(), {})
    body = CreatorApplyRequest(
        contract_version="configured-report/v2",
        mode="creator",
        base_revision=0,
        definition=definition,
    )
    with pytest.raises(PresentationFailure, match="INVALID_DEFINITION_BINDING"):
        service.apply_new(workspace, uuid4(), body)
    repository.metadata.side_effect = None
    repository.metadata.return_value = {"creator": actor}
    with pytest.raises(PresentationFailure, match="REVISION_CONFLICT"):
        service.apply_new(workspace, actor, body)
    repository.metadata.return_value = {"creator": uuid4()}
    with pytest.raises(PresentationFailure, match="FORBIDDEN"):
        service.apply_new(workspace, actor, body)


def test_first_save_retry_reaches_locked_replay_after_concurrent_commit() -> None:
    service, workspace, actor, repository, _ = setup_service()
    definition = service.new_definition(workspace, actor, request("blank"), {})
    body = WorkspaceSaveRequest(
        contract_version="configured-report/v2",
        definition=definition,
        expected_revision=0,
        expected_saved_view_revision=0,
        idempotency_key=uuid4(),
        configuration_hash="a" * 64,
        result_ids=[],
        chart_specs=[],
    )
    repository.metadata.side_effect = [PresentationFailure("NOT_FOUND"), {"creator": actor}]
    repository.replay.return_value = None
    # Stop at materialization: the important interleaving is replay miss -> creator's commit.
    service._materialize = Mock(side_effect=RuntimeError("reached materialization"))  # type: ignore[method-assign]
    with pytest.raises(RuntimeError, match="reached materialization"):
        service.save(workspace, actor, definition.report_id, body)


def test_first_save_never_targets_another_authors_document() -> None:
    service, workspace, actor, repository, _ = setup_service()
    definition = service.new_definition(workspace, actor, request("blank"), {})
    body = WorkspaceSaveRequest(
        contract_version="configured-report/v2",
        definition=definition,
        expected_revision=0,
        expected_saved_view_revision=0,
        idempotency_key=uuid4(),
        configuration_hash="a" * 64,
        result_ids=[],
        chart_specs=[],
    )
    repository.metadata.side_effect = None
    repository.metadata.return_value = {"creator": uuid4()}
    with pytest.raises(PresentationFailure, match="FORBIDDEN"):
        service.save(workspace, actor, definition.report_id, body)
    repository.replay.assert_not_called()
    repository.save_workspace.assert_not_called()
