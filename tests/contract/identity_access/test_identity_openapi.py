import json
from pathlib import Path

from custometry_api.config import Settings
from custometry_api.identity.router import create_identity_app
from custometry_api.main import create_app


def test_identity_openapi_provider_matches_committed_contract() -> None:
    root = Path(__file__).resolve().parents[3]
    committed = json.loads(
        (root / "packages/contracts/openapi/identity.openapi.json").read_text(encoding="utf-8")
    )

    generated = create_identity_app(Settings(version="0.1.0-dev.0")).openapi()

    assert generated == committed


def test_identity_is_independently_versioned_without_foundation_contract_drift() -> None:
    parent = create_app(settings=Settings(version="0.1.0-dev.0"))
    foundation = parent.openapi()

    assert "/identity/login" not in foundation["paths"]
    assert any(getattr(route, "path", None) == "/identity" for route in parent.routes)


def test_identity_contract_declares_cookie_csrf_and_scoped_token_boundaries() -> None:
    schema = create_identity_app(Settings(version="0.1.0-dev.0")).openapi()

    refresh_parameters = schema["paths"]["/refresh"]["post"]["parameters"]
    assert {item["name"] for item in refresh_parameters} == {
        "X-CSRF-Token",
        "custometry_refresh",
    }
    token_schema = schema["components"]["schemas"]["ApiTokenCreateRequest"]
    assert "scopes" in token_schema["required"]
    assert schema["paths"]["/bootstrap"]["post"]["operationId"] == "bootstrap_identity"
