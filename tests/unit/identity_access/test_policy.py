from uuid import uuid4

from hypothesis import given, strategies as st
import pytest

from packages.identity_access.domain.policy import (
    ANALYST,
    ROLE_PERMISSIONS,
    VIEWER,
    WORKSPACE_ADMIN,
    WORKSPACE_OWNER,
    Actor,
    PolicyViolation,
    permissions_for_roles,
    require_grant_ceiling,
    require_workspace,
)


def actor(role: str) -> Actor:
    return Actor(
        principal_id=uuid4(),
        workspace_id=uuid4(),
        email="actor@example.test",
        permissions=permissions_for_roles([role]),
    )


def test_default_role_bundles_preserve_functional_ceiling() -> None:
    assert "workspace.members.manage" in ROLE_PERMISSIONS[WORKSPACE_ADMIN]
    assert "analysis.manage" not in ROLE_PERMISSIONS[WORKSPACE_ADMIN]
    assert "analysis.manage" in ROLE_PERMISSIONS[ANALYST]
    assert "workspace.members.manage" not in ROLE_PERMISSIONS[ANALYST]
    assert "report.read" in ROLE_PERMISSIONS[VIEWER]
    assert "pii.preview" not in ROLE_PERMISSIONS[VIEWER]
    assert ROLE_PERMISSIONS[WORKSPACE_ADMIN] <= ROLE_PERMISSIONS[WORKSPACE_OWNER]
    assert ROLE_PERMISSIONS[ANALYST] <= ROLE_PERMISSIONS[WORKSPACE_OWNER]


@given(st.lists(st.sampled_from(sorted(ROLE_PERMISSIONS)), min_size=1, max_size=8))
def test_grants_never_exceed_issuer_permission_ceiling(requested_roles: list[str]) -> None:
    owner = actor(WORKSPACE_OWNER)
    normalized = require_grant_ceiling(owner, requested_roles)

    assert permissions_for_roles(normalized) <= owner.permissions


def test_workspace_scope_fails_closed() -> None:
    resolved = actor(WORKSPACE_OWNER)

    with pytest.raises(PolicyViolation, match="workspace scope denied"):
        require_workspace(resolved, uuid4())


def test_admin_cannot_assign_analyst_role_above_own_ceiling() -> None:
    admin = actor(WORKSPACE_ADMIN)

    with pytest.raises(PolicyViolation, match="permission ceiling"):
        require_grant_ceiling(admin, [ANALYST])
