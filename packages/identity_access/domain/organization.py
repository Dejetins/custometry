"""Organization hierarchy invariants and deny-wins access composition."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Final
from uuid import UUID


ORG_UNIT_KINDS: Final = frozenset({"company", "division", "department", "team"})
ORG_UNIT_STATUSES: Final = frozenset({"active", "inactive", "merged"})
LEADERSHIP_SCOPES: Final = frozenset({"unit", "subtree", "workspace"})
OWNER_TYPES: Final = frozenset({"principal", "org_unit", "workspace_legacy"})
RESOURCE_ACTION_PERMISSIONS: Final = {
    ("report", "view_snapshot"): "report.read",
    ("report", "search"): "report.read",
    ("report", "run"): "analysis.run",
    ("report", "export"): "report.export_xlsx",
    ("report", "edit"): "report.manage",
    ("report", "manage_access"): "report_access.manage",
    ("dashboard", "view_snapshot"): "report.read",
    ("dashboard", "search"): "report.read",
    ("dashboard", "edit"): "dashboard.manage",
    ("dashboard", "manage_access"): "dashboard_access.manage",
    ("analysis", "view_snapshot"): "analysis.read",
    ("analysis", "run"): "analysis.run",
    ("analysis", "edit"): "analysis.manage",
    ("research", "view_snapshot"): "research.read",
    ("research", "edit"): "research.manage",
    ("segment", "view_snapshot"): "segment.read",
    ("segment", "edit"): "segment.manage",
    ("segment", "export"): "segment.export",
}


class OrganizationInvariant(ValueError):
    """Raised before persistence when a domain command is structurally invalid."""


@dataclass(frozen=True, slots=True)
class OrgUnitVersion:
    org_unit_id: UUID
    workspace_id: UUID
    key: str
    version: int
    kind: str
    parent_org_unit_id: UUID | None
    display_name: str
    status: str
    effective_from: datetime
    effective_to: datetime | None
    successor_org_unit_id: UUID | None


@dataclass(frozen=True, slots=True)
class AccessInputs:
    functional_permission: bool
    active_membership: bool
    organization_scope: bool
    department_policy: bool
    cross_department_grant: bool
    object_policy: bool
    row_policy: bool
    column_policy: bool
    export_policy: bool
    pii_policy: bool
    policy_fresh: bool
    explicit_denies: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class EffectiveAccessDecision:
    allowed: bool
    denied_by: tuple[str, ...]
    layers: tuple[tuple[str, bool], ...]


def validate_unit_shape(
    *,
    key: str,
    kind: str,
    display_name: str,
    parent_org_unit_id: UUID | None,
) -> tuple[str, str, str]:
    """Normalize a unit without assigning policy meaning to its name."""

    normalized_key = key.strip().casefold()
    normalized_name = display_name.strip()
    normalized_kind = kind.strip().casefold()
    if normalized_kind not in ORG_UNIT_KINDS:
        raise OrganizationInvariant("invalid org unit kind")
    if not (2 <= len(normalized_key) <= 80) or not normalized_key[0].isalnum():
        raise OrganizationInvariant("invalid org unit key")
    if not all(character.isalnum() or character in {"-", "_"} for character in normalized_key):
        raise OrganizationInvariant("invalid org unit key")
    if not (1 <= len(normalized_name) <= 160):
        raise OrganizationInvariant("invalid org unit display name")
    if normalized_kind == "company" and parent_org_unit_id is not None:
        raise OrganizationInvariant("company unit cannot have a parent")
    if normalized_kind != "company" and parent_org_unit_id is None:
        raise OrganizationInvariant("non-company unit requires a parent")
    return normalized_key, normalized_kind, normalized_name


def required_functional_permission(resource_type: str, action: str) -> str:
    """Resolve the functional ceiling from a server-owned action registry."""

    try:
        return RESOURCE_ACTION_PERMISSIONS[(resource_type, action)]
    except KeyError as exc:
        raise OrganizationInvariant("unsupported resource action") from exc


def effective_access(inputs: AccessInputs) -> EffectiveAccessDecision:
    """Intersect every access layer; an allow-only grant never cancels a deny."""

    organization_allowed = inputs.organization_scope or inputs.cross_department_grant
    layers = (
        ("functional_permission", inputs.functional_permission),
        ("active_workspace_membership", inputs.active_membership),
        ("organization_scope", organization_allowed),
        ("department_data_policy", inputs.department_policy),
        ("object_version_policy", inputs.object_policy),
        ("row_policy", inputs.row_policy),
        ("column_policy", inputs.column_policy),
        ("export_policy", inputs.export_policy),
        ("pii_policy", inputs.pii_policy),
        ("policy_fresh", inputs.policy_fresh),
    )
    denied = [name for name, allowed in layers if not allowed]
    denied.extend(f"explicit_deny:{reason}" for reason in inputs.explicit_denies)
    return EffectiveAccessDecision(
        allowed=not denied,
        denied_by=tuple(denied),
        layers=layers,
    )
