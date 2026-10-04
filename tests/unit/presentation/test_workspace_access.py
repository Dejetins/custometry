"""Current Identity projection preserves deny-wins and unsupported scope ceilings."""

from typing import Any
from uuid import uuid4
import pytest
from packages.identity_access.application.resource_access import ResourceAccessService
from packages.identity_access.domain.policy import Actor


class Projection:
    def __init__(self, layers: dict[str, bool], detail: dict[str, Any]):
        self.layers, self.detail = layers, detail

    def resource_context(self, *args: Any) -> dict[str, Any]:
        return {"layers": self.layers, "detail": self.detail}


@pytest.mark.parametrize(
    "denial",
    [
        "functional_permission",
        "active_membership",
        "department_policy",
        "object_policy",
        "row_policy",
        "column_policy",
        "pii_policy",
        "policy_fresh",
    ],
)
def test_explicit_grant_never_cancels_a_denial(denial: str) -> None:
    actor = Actor(uuid4(), uuid4(), "unit@example.test", frozenset({"analysis.read"}))
    layers = {
        key: True
        for key in (
            "functional_permission",
            "active_membership",
            "organization_scope",
            "department_policy",
            "cross_department_grant",
            "object_policy",
            "row_policy",
            "column_policy",
            "export_policy",
            "pii_policy",
            "policy_fresh",
        )
    }
    layers[denial] = False
    service = ResourceAccessService(Projection(layers, {}), lambda: actor)
    assert not service.resolve_resource(
        workspace_id=actor.workspace_id,
        principal_id=actor.principal_id,
        resource_type="analysis",
        resource_id=uuid4(),
        action="view_snapshot",
    ).allowed


@pytest.mark.parametrize(
    "rows,columns,allowed,stores",
    [
        ([[], []], [[], []], True, None),
        ([["store:1", "store:2"], ["store:2"]], [[], []], True, ("2",)),
        ([["store:1"], ["store:2"]], [[], []], True, ()),
        ([["unsupported:row"]], [[]], False, None),
        ([[]], [["unsupported:column"]], False, None),
    ],
)
def test_scope_is_intersected_or_rejected(
    rows: list[list[str]], columns: list[list[str]], allowed: bool, stores: tuple[str, ...] | None
) -> None:
    actor = Actor(uuid4(), uuid4(), "unit@example.test", frozenset({"analysis.read"}))
    layers = {
        key: True
        for key in (
            "functional_permission",
            "active_membership",
            "organization_scope",
            "department_policy",
            "cross_department_grant",
            "object_policy",
            "row_policy",
            "column_policy",
            "export_policy",
            "pii_policy",
            "policy_fresh",
        )
    }
    service = ResourceAccessService(
        Projection(layers, {"row_scopes": rows, "column_scopes": columns}), lambda: actor
    )
    decision = service.resolve_resource(
        workspace_id=actor.workspace_id,
        principal_id=actor.principal_id,
        resource_type="analysis",
        resource_id=uuid4(),
        action="view_snapshot",
    )
    assert (decision.allowed, decision.store_ids) == (allowed, stores)
