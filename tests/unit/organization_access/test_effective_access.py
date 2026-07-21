from datetime import UTC, datetime
from uuid import uuid4

import pytest

from packages.identity_access.domain.organization import (
    AccessInputs,
    OrganizationInvariant,
    effective_access,
    required_functional_permission,
    validate_unit_shape,
)


def test_effective_access_requires_every_layer() -> None:
    allowed = effective_access(
        AccessInputs(
            functional_permission=True,
            active_membership=True,
            organization_scope=True,
            department_policy=True,
            cross_department_grant=False,
            object_policy=True,
            row_policy=True,
            column_policy=True,
            export_policy=True,
            pii_policy=True,
            policy_fresh=True,
        )
    )

    assert allowed.allowed is True
    assert allowed.denied_by == ()


@pytest.mark.parametrize(
    "overrides, expected",
    [
        ({"functional_permission": False, "cross_department_grant": True}, "functional_permission"),
        ({"object_policy": False, "cross_department_grant": True}, "object_version_policy"),
        ({"pii_policy": False, "cross_department_grant": True}, "pii_policy"),
        ({"policy_fresh": False, "cross_department_grant": True}, "policy_fresh"),
    ],
)
def test_allow_only_grant_cannot_raise_other_ceilings(
    overrides: dict[str, bool], expected: str
) -> None:
    values: dict[str, object] = {
        "functional_permission": True,
        "active_membership": True,
        "organization_scope": False,
        "department_policy": True,
        "cross_department_grant": True,
        "object_policy": True,
        "row_policy": True,
        "column_policy": True,
        "export_policy": True,
        "pii_policy": True,
        "policy_fresh": True,
    }
    values.update(overrides)

    decision = effective_access(AccessInputs(**values))  # type: ignore[arg-type]

    assert decision.allowed is False
    assert expected in decision.denied_by


def test_explicit_deny_wins_over_complete_allow() -> None:
    decision = effective_access(
        AccessInputs(
            functional_permission=True,
            active_membership=True,
            organization_scope=False,
            department_policy=True,
            cross_department_grant=True,
            object_policy=True,
            row_policy=True,
            column_policy=True,
            export_policy=True,
            pii_policy=True,
            policy_fresh=True,
            explicit_denies=("legal_hold",),
        )
    )

    assert decision.allowed is False
    assert decision.denied_by == ("explicit_deny:legal_hold",)


def test_unit_shape_has_stable_key_and_structural_parent_rules() -> None:
    key, kind, name = validate_unit_shape(
        key=" Sales_Core ",
        kind="Department",
        display_name=" Sales Core ",
        parent_org_unit_id=uuid4(),
    )
    assert (key, kind, name) == ("sales_core", "department", "Sales Core")

    with pytest.raises(OrganizationInvariant):
        validate_unit_shape(
            key="root",
            kind="company",
            display_name="Root",
            parent_org_unit_id=uuid4(),
        )

    assert datetime.now(UTC).tzinfo is UTC


def test_resource_action_registry_owns_the_functional_ceiling() -> None:
    assert required_functional_permission("report", "view_snapshot") == "report.read"
    assert required_functional_permission("report", "run") == "analysis.run"
    assert required_functional_permission("report", "export") == "report.export_xlsx"

    with pytest.raises(OrganizationInvariant):
        required_functional_permission("report", "unknown")
