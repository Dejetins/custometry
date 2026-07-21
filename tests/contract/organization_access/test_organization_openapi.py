import json
from pathlib import Path

from custometry_api.config import Settings
from custometry_api.main import create_app
from custometry_api.organization.router import create_organization_app


def test_organization_openapi_provider_matches_committed_contract() -> None:
    root = Path(__file__).resolve().parents[3]
    committed = json.loads(
        (root / "packages/contracts/openapi/organization.openapi.json").read_text(
            encoding="utf-8"
        )
    )

    generated = create_organization_app(Settings(version="0.1.0-dev.0")).openapi()

    assert generated == committed


def test_organization_is_independently_versioned_and_mounted() -> None:
    parent = create_app(settings=Settings(version="0.1.0-dev.0"))
    foundation = parent.openapi()

    assert "/organization/units" not in foundation["paths"]
    assert any(getattr(route, "path", None) == "/organization" for route in parent.routes)


def test_contract_exposes_versioned_mutations_and_explainable_access() -> None:
    schema = create_organization_app(Settings(version="0.1.0-dev.0")).openapi()

    assert schema["paths"]["/units/{org_unit_id}/versions"]["post"]["operationId"] == (
        "version_organization_unit"
    )
    assert schema["paths"]["/access/decide"]["post"]["operationId"] == (
        "explain_effective_organization_access"
    )
    assert "expected_version" in schema["components"]["schemas"]["PolicyPublishRequest"][
        "required"
    ]
    decision_properties = schema["components"]["schemas"]["AccessDecisionRequest"][
        "properties"
    ]
    assert not {
        "functional_permission",
        "object_policy",
        "row_policy",
        "column_policy",
        "export_policy",
        "pii_policy",
        "requires_pii",
        "explicit_denies",
    }.intersection(decision_properties)
    ownership_properties = schema["components"]["schemas"]["OwnershipRequest"][
        "properties"
    ]
    assert {
        "allowed_actions",
        "required_row_scope_refs",
        "required_column_policy_refs",
        "requires_pii",
    }.issubset(ownership_properties)
