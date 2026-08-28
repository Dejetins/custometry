"""Deterministic OpenAPI, event schema, and consumer manifest generation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from custometry_api.config import Settings
from custometry_api.notifications.router import create_notifications_app


def render_openapi() -> bytes:
    schema = create_notifications_app(Settings(version="0.1.0-dev.0")).openapi()
    return (json.dumps(schema, indent=2, sort_keys=True) + "\n").encode()


def render_event_schema() -> bytes:
    scalar = {"type": ["string", "integer", "boolean"]}
    document: dict[str, Any] = {
        "$id": "https://contracts.custometry.local/notifications/event-v1.schema.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "additionalProperties": False,
        "properties": {
            "category": {
                "enum": [
                    "run",
                    "data_quality",
                    "data_freshness",
                    "forecast",
                    "schedule",
                    "system",
                    "security",
                    "admin",
                ]
            },
            "deep_link": {
                "oneOf": [
                    {"type": "null"},
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "parameters": {
                                "type": "object",
                                "additionalProperties": {"type": "string", "maxLength": 128},
                            },
                            "route_id": {"type": "string", "maxLength": 64},
                        },
                        "required": ["route_id", "parameters"],
                    },
                ]
            },
            "event_id": {"type": "string", "format": "uuid"},
            "group_key": {"type": "string", "maxLength": 128},
            "message_code": {"type": "string", "pattern": "^[A-Z][A-Z0-9_]{2,79}$"},
            "message_parameters": {
                "type": "object",
                "additionalProperties": scalar,
                "maxProperties": 16,
            },
            "occurred_at": {"type": "string", "format": "date-time"},
            "resolved": {"type": "boolean"},
            "resource_id": {"type": "string", "maxLength": 128},
            "resource_type": {"type": "string", "maxLength": 128},
            "severity": {"enum": ["info", "warning", "critical"]},
            "source_owner": {"type": "string", "maxLength": 128},
            "source_type": {"type": "string", "maxLength": 128},
            "source_version": {"type": "integer", "minimum": 1},
            "trace_id": {"type": ["string", "null"], "maxLength": 128},
            "workspace_id": {"type": "string", "format": "uuid"},
        },
        "required": [
            "event_id",
            "source_owner",
            "source_type",
            "source_version",
            "workspace_id",
            "resource_type",
            "resource_id",
            "severity",
            "category",
            "occurred_at",
            "message_code",
            "message_parameters",
            "group_key",
            "deep_link",
            "trace_id",
            "resolved",
        ],
        "title": "NotificationEventV1",
        "type": "object",
    }
    return (json.dumps(document, indent=2, sort_keys=True) + "\n").encode()


def render_consumer(openapi: bytes, event_schema: bytes) -> bytes:
    document: dict[str, Any] = json.loads(openapi)
    operations: list[tuple[str, str, str]] = []
    for path, path_item in sorted(document["paths"].items()):
        for method in ("get", "post", "put", "patch", "delete"):
            operation = path_item.get(method)
            if operation is not None:
                operations.append((str(operation["operationId"]), method.upper(), path))
    lines = [
        "// Generated from Notifications OpenAPI and event schema. Do not edit.",
        f'export const notificationsApiDigest = "{hashlib.sha256(openapi).hexdigest()}" as const;',
        f'export const notificationEventDigest = "{hashlib.sha256(event_schema).hexdigest()}" as const;',
        "export const notificationOperations = {",
    ]
    for operation_id, method, path in sorted(operations):
        lines.append(
            f"  {json.dumps(operation_id)}: {{ method: {json.dumps(method)}, "
            f"path: {json.dumps(path)} }},"
        )
    schemas = sorted(document.get("components", {}).get("schemas", {}))
    lines.extend(
        (
            "} as const;",
            "export const notificationSchemaNames = "
            + json.dumps(schemas, separators=(",", ":"))
            + " as const;",
            "",
        )
    )
    return "\n".join(lines).encode()


def generate(root: Path) -> None:
    openapi = render_openapi()
    event_schema = render_event_schema()
    (root / "packages/contracts/openapi/notifications.openapi.json").write_bytes(openapi)
    (root / "packages/contracts/schemas/notification-event.schema.json").write_bytes(event_schema)
    (root / "packages/contracts/src/notifications.ts").write_bytes(
        render_consumer(openapi, event_schema)
    )


if __name__ == "__main__":
    generate(Path(__file__).resolve().parents[3])
