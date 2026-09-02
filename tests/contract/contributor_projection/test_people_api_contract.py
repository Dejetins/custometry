import json
from pathlib import Path

from custometry_api.config import Settings
from custometry_api.main import create_app
from custometry_api.people.router import create_people_app
from packages.contracts.people import PEOPLE_API_VERSION


def test_people_openapi_provider_matches_committed_contract() -> None:
    root = Path(__file__).resolve().parents[3]
    committed = json.loads(
        (root / "packages/contracts/openapi/people.openapi.json").read_text(encoding="utf-8")
    )
    generated = create_people_app(Settings(version="0.1.0-dev.0")).openapi()

    assert generated == committed
    assert generated["info"]["version"] == PEOPLE_API_VERSION


def test_people_provider_is_independently_versioned_and_mounted() -> None:
    parent = create_app(settings=Settings(version="0.1.0-dev.0"))

    assert "/people/contributors" not in parent.openapi()["paths"]
    assert any(getattr(route, "path", None) == "/people" for route in parent.routes)


def test_people_contract_has_no_surveillance_or_hidden_count_surface() -> None:
    schema = create_people_app(Settings(version="0.1.0-dev.0")).openapi()
    profile = schema["components"]["schemas"]["ContributorProfileResponse"]
    listing = schema["components"]["schemas"]["ContributorListResponse"]
    serialized = json.dumps(schema, sort_keys=True).casefold()

    assert schema["paths"]["/contributors"]["get"]["operationId"] == (
        "list_people_contributors"
    )
    assert schema["paths"]["/contributors/{principal_id}"]["get"]["operationId"] == (
        "get_people_contributor"
    )
    assert "visible_count" in listing["required"]
    assert "total_count" not in listing["properties"]
    assert "visible_resource_count" in profile["required"]
    assert not {
        "email",
        "raw_audit",
        "audit_events",
        "ranking",
        "productivity_score",
        "peer_percentile",
        "login_history",
    }.intersection(profile["properties"])
    assert "password" not in serialized
    assert "recipient_email" not in serialized
