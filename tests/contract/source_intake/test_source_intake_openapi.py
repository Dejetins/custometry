import json
from pathlib import Path

from custometry_api.config import Settings
from custometry_api.connections.router import create_connection_app
from custometry_api.imports.router import create_import_app
from custometry_api.main import create_app


def test_source_intake_openapi_providers_match_committed_contracts() -> None:
    root = Path(__file__).resolve().parents[3]
    committed_connections = json.loads(
        (root / "packages/contracts/openapi/source-connections.openapi.json").read_text(
            encoding="utf-8"
        )
    )
    committed_imports = json.loads(
        (root / "packages/contracts/openapi/source-imports.openapi.json").read_text(
            encoding="utf-8"
        )
    )

    assert create_connection_app(Settings()).openapi() == committed_connections
    assert create_import_app(Settings()).openapi() == committed_imports


def test_source_intake_is_independently_versioned_and_mounted() -> None:
    parent = create_app(settings=Settings())
    foundation = parent.openapi()

    assert not any(path.startswith("/connections") for path in foundation["paths"])
    assert not any(path.startswith("/imports") for path in foundation["paths"])
    mounted = {getattr(route, "path", None) for route in parent.routes}
    assert {"/connections", "/imports"} <= mounted


def test_public_contracts_do_not_expose_source_network_or_secret_details() -> None:
    connections = create_connection_app(Settings()).openapi()
    imports = create_import_app(Settings()).openapi()
    rendered = json.dumps({"connections": connections, "imports": imports}, sort_keys=True)

    for forbidden in ("database_host", "password", "dsn", "secret_ref", "profile_ref"):
        if forbidden in {"secret_ref", "profile_ref"}:
            assert forbidden in rendered
        else:
            assert forbidden not in rendered.casefold()
    response_properties = connections["components"]["schemas"]["ConnectionResponse"]["properties"]
    assert "secret_ref" not in response_properties
    assert "profile_ref" not in response_properties
