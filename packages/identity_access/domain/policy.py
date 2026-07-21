"""Functional permission bundles and fail-closed policy composition."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final
from uuid import UUID


WORKSPACE_OWNER: Final = "workspace_owner"
WORKSPACE_ADMIN: Final = "workspace_admin"
ANALYST: Final = "analyst"
VIEWER: Final = "viewer"

ADMIN_PERMISSIONS: Final = frozenset(
    {
        "workspace.read",
        "workspace.manage",
        "workspace.members.read",
        "workspace.members.manage",
        "workspace.roles.assign",
        "workspace.sessions.manage",
        "workspace.password_reset.manage",
        "connection.read_metadata",
        "connection.manage",
        "connection.secret.rotate",
        "report_access.manage",
        "dashboard_access.manage",
        "report_email_policy.manage",
        "brand.read",
        "brand.assign",
        "audit.read",
        "organization.read",
        "organization.manage",
        "organization.members.assign",
        "organization.leadership.assign",
        "organization.data_policy.manage",
        "organization.access.delegate",
        "organization.ownership.manage",
        "api_token.manage_own",
        "session.manage_own",
        "password.change_own",
    }
)

ANALYST_PERMISSIONS: Final = frozenset(
    {
        "workspace.read",
        "metric.read",
        "metric.manage",
        "metric.publish",
        "methodology.read",
        "methodology.manage",
        "methodology.publish",
        "analysis.read",
        "analysis.run",
        "analysis.manage",
        "research.read",
        "research.manage",
        "segment.read",
        "segment.manage",
        "segment.export",
        "dashboard.manage",
        "dashboard.publish",
        "report.read",
        "report.manage",
        "report.send",
        "report.export_xlsx",
        "comment.read",
        "comment.create",
        "comment.resolve",
        "organization.read",
        "api_token.manage_own",
        "session.manage_own",
        "password.change_own",
    }
)

VIEWER_PERMISSIONS: Final = frozenset(
    {
        "workspace.read",
        "report.read",
        "comment.read",
        "comment.create",
        "organization.read",
        "api_token.manage_own",
        "session.manage_own",
        "password.change_own",
    }
)

ROLE_PERMISSIONS: Final[dict[str, frozenset[str]]] = {
    WORKSPACE_OWNER: ADMIN_PERMISSIONS | ANALYST_PERMISSIONS,
    WORKSPACE_ADMIN: ADMIN_PERMISSIONS,
    ANALYST: ANALYST_PERMISSIONS,
    VIEWER: VIEWER_PERMISSIONS,
}


class PolicyViolation(ValueError):
    """Raised when a requested grant exceeds a functional ceiling."""


@dataclass(frozen=True, slots=True)
class Actor:
    """Resolved principal and workspace policy for one authenticated request."""

    principal_id: UUID
    workspace_id: UUID
    email: str
    permissions: frozenset[str]
    installation_admin: bool = False
    session_id: UUID | None = None
    csrf_token_hash: str | None = None
    token_kind: str = "session"

    def allows(self, permission: str) -> bool:
        return permission in self.permissions


def normalized_roles(roles: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    """Return a stable role set and reject unknown or empty grants."""

    normalized = tuple(sorted(set(roles)))
    if not normalized:
        raise PolicyViolation("at least one functional role is required")
    unknown = set(normalized) - ROLE_PERMISSIONS.keys()
    if unknown:
        raise PolicyViolation("unknown functional role")
    return normalized


def permissions_for_roles(roles: list[str] | tuple[str, ...]) -> frozenset[str]:
    """Compose role grants without introducing implicit permissions."""

    normalized = normalized_roles(roles)
    combined: set[str] = set()
    for role in normalized:
        combined.update(ROLE_PERMISSIONS[role])
    return frozenset(combined)


def require_permission(actor: Actor, permission: str) -> None:
    """Fail closed when the resolved actor lacks a functional permission."""

    if not actor.allows(permission):
        raise PolicyViolation("permission denied")


def require_workspace(actor: Actor, workspace_id: UUID) -> None:
    """Reject cross-workspace use before any resource fetch."""

    if actor.workspace_id != workspace_id:
        raise PolicyViolation("workspace scope denied")


def require_grant_ceiling(actor: Actor, roles: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    """Ensure an invitation or assignment cannot exceed the issuer's grants."""

    normalized = normalized_roles(roles)
    requested = permissions_for_roles(normalized)
    if not requested.issubset(actor.permissions):
        raise PolicyViolation("requested role exceeds issuer permission ceiling")
    return normalized
