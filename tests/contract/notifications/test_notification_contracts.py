import json
from pathlib import Path

from custometry_api.config import Settings
from custometry_api.main import create_app
from custometry_api.notifications.router import create_notifications_app
from packages.contracts.notifications import NOTIFICATIONS_API_VERSION
from packages.contracts.notifications.generator import (
    render_consumer,
    render_event_schema,
    render_openapi,
)


def test_generated_openapi_event_and_consumer_contracts_have_no_drift() -> None:
    root = Path(__file__).resolve().parents[3]
    openapi = render_openapi()
    event = render_event_schema()

    assert openapi == (root / "packages/contracts/openapi/notifications.openapi.json").read_bytes()
    assert (
        event == (root / "packages/contracts/schemas/notification-event.schema.json").read_bytes()
    )
    assert (
        render_consumer(openapi, event)
        == (root / "packages/contracts/src/notifications.ts").read_bytes()
    )

    schema = create_notifications_app(Settings(version="0.1.0-dev.0")).openapi()
    assert schema["info"]["version"] == NOTIFICATIONS_API_VERSION
    assert set(schema["paths"]) == {
        "/items",
        "/items/{notification_id}",
        "/items/{notification_id}/acknowledge",
        "/items/{notification_id}/dismiss",
        "/items/{notification_id}/read",
        "/unread-count",
    }


def test_event_and_api_contracts_are_locale_neutral_and_redacted() -> None:
    event = json.loads(render_event_schema())
    properties = event["properties"]
    assert {"message_code", "message_parameters", "deep_link"}.issubset(properties)
    assert not {
        "rendered_text",
        "locale",
        "email",
        "secret",
        "provider_payload",
        "source_value",
    }.intersection(properties)

    api = json.loads(render_openapi())
    item = api["components"]["schemas"]["NotificationResponse"]
    assert {"message_code", "message_parameters", "deep_link", "revision"}.issubset(
        item["properties"]
    )
    assert not {"recipient_id", "resource_id", "rendered_text", "raw_payload"}.intersection(
        item["properties"]
    )


def test_provider_is_independently_versioned_and_mounted() -> None:
    parent = create_app(settings=Settings(version="0.1.0-dev.0"))

    assert "/notifications/items" not in parent.openapi()["paths"]
    assert any(getattr(route, "path", None) == "/notifications" for route in parent.routes)
