"""Stable public identifiers for the Organization API provider contract."""

from typing import Final


ORGANIZATION_API_VERSION: Final = "1.0.0"

ORG_UNIT_KINDS: Final = ("company", "division", "department", "team")
ORG_UNIT_STATUSES: Final = ("active", "inactive", "merged")
LEADERSHIP_SCOPE_MODES: Final = ("unit", "subtree", "workspace")
RESOURCE_OWNER_TYPES: Final = ("principal", "org_unit", "workspace_legacy")
POLICY_STATUSES: Final = ("draft", "published", "deprecated")


__all__ = [
    "LEADERSHIP_SCOPE_MODES",
    "ORGANIZATION_API_VERSION",
    "ORG_UNIT_KINDS",
    "ORG_UNIT_STATUSES",
    "POLICY_STATUSES",
    "RESOURCE_OWNER_TYPES",
]
