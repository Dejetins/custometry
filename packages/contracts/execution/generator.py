"""Deterministic execution-control OpenAPI and consumer manifest generator."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from custometry_api.config import Settings
from custometry_api.runs.router import create_runs_app


def render_openapi() -> bytes:
    schema = create_runs_app(Settings(version="0.1.0-dev.0")).openapi()
    return (json.dumps(schema, indent=2, sort_keys=True) + "\n").encode()


def render_consumer(openapi_bytes: bytes) -> bytes:
    document: dict[str, Any] = json.loads(openapi_bytes)
    operations: list[tuple[str, str, str]] = []
    for path, path_item in sorted(document["paths"].items()):
        for method in ("get", "post", "put", "patch", "delete"):
            operation = path_item.get(method)
            if operation is not None:
                operations.append((str(operation["operationId"]), method.upper(), path))
    digest = hashlib.sha256(openapi_bytes).hexdigest()
    lines = [
        "// Generated from execution-control OpenAPI. Do not edit.",
        f'export const executionControlContractDigest = "{digest}" as const;',
        "export const executionControlOperations = {",
    ]
    for operation_id, method, path in sorted(operations):
        lines.append(
            f"  {json.dumps(operation_id)}: {{ method: {json.dumps(method)}, "
            f"path: {json.dumps(path)} }},"
        )
    schema_names = sorted(document.get("components", {}).get("schemas", {}))
    lines.extend(
        (
            "} as const;",
            "export const executionControlSchemaNames = "
            + json.dumps(schema_names, separators=(",", ":"))
            + " as const;",
            "",
        )
    )
    return "\n".join(lines).encode()


def render_terminal_event_schema() -> bytes:
    document = {
        "$id": "https://contracts.custometry.local/execution/terminal-event/v1",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "additionalProperties": False,
        "properties": {
            "attempt_id": {"format": "uuid", "type": "string"},
            "category": {"const": "execution"},
            "event_id": {"format": "uuid", "type": "string"},
            "event_type": {
                "enum": [
                    "execution.run.failed",
                    "execution.run.recovered",
                    "execution.run.stuck",
                ]
            },
            "event_version": {"const": "1.0.0"},
            "group_key": {"maxLength": 128, "type": "string"},
            "message_code": {"enum": ["RUN_FAILED", "RUN_RECOVERED", "RUN_STUCK"]},
            "message_parameters": {
                "additionalProperties": {"maxLength": 128, "type": "string"},
                "maxProperties": 8,
                "type": "object",
            },
            "occurred_at": {"format": "date-time", "type": "string"},
            "reason_code": {"maxLength": 80, "pattern": "^[A-Z][A-Z0-9_]{2,79}$", "type": "string"},
            "resource_id": {"format": "uuid", "type": "string"},
            "resource_type": {"const": "run"},
            "retry_of_attempt_id": {
                "anyOf": [{"format": "uuid", "type": "string"}, {"type": "null"}]
            },
            "retry_of_run_id": {"anyOf": [{"format": "uuid", "type": "string"}, {"type": "null"}]},
            "route_id": {"const": "UI-OPS-002"},
            "route_parameters": {
                "additionalProperties": {"maxLength": 128, "type": "string"},
                "maxProperties": 4,
                "type": "object",
            },
            "run_id": {"format": "uuid", "type": "string"},
            "severity": {"enum": ["critical", "info", "warning"]},
            "source_owner": {"const": "execution"},
            "status_code": {"enum": ["FAILED", "RECOVERED", "STUCK"]},
            "trace_id": {"anyOf": [{"maxLength": 128, "type": "string"}, {"type": "null"}]},
            "workspace_id": {"format": "uuid", "type": "string"},
        },
        "required": [
            "event_id",
            "event_type",
            "event_version",
            "source_owner",
            "workspace_id",
            "resource_type",
            "resource_id",
            "run_id",
            "attempt_id",
            "retry_of_run_id",
            "retry_of_attempt_id",
            "status_code",
            "reason_code",
            "severity",
            "category",
            "occurred_at",
            "message_code",
            "message_parameters",
            "group_key",
            "route_id",
            "route_parameters",
            "trace_id",
        ],
        "title": "ExecutionTerminalEventV1",
        "type": "object",
    }
    return (json.dumps(document, indent=2, sort_keys=True) + "\n").encode()


def render_terminal_event_consumer(schema_bytes: bytes) -> bytes:
    digest = hashlib.sha256(schema_bytes).hexdigest()
    lines = [
        "// Generated from execution-terminal-event.schema.json. Do not edit.",
        f'export const executionTerminalEventContractDigest = "{digest}" as const;',
        'export const executionTerminalEventVersion = "1.0.0" as const;',
        "export type ExecutionTerminalEventType =",
        '  | "execution.run.failed"',
        '  | "execution.run.stuck"',
        '  | "execution.run.recovered";',
        "export interface ExecutionTerminalEventV1 {",
        "  event_id: string;",
        "  event_type: ExecutionTerminalEventType;",
        '  event_version: "1.0.0";',
        '  source_owner: "execution";',
        "  workspace_id: string;",
        '  resource_type: "run";',
        "  resource_id: string;",
        "  run_id: string;",
        "  attempt_id: string;",
        "  retry_of_run_id: string | null;",
        "  retry_of_attempt_id: string | null;",
        '  status_code: "FAILED" | "STUCK" | "RECOVERED";',
        "  reason_code: string;",
        '  severity: "info" | "warning" | "critical";',
        '  category: "execution";',
        "  occurred_at: string;",
        '  message_code: "RUN_FAILED" | "RUN_STUCK" | "RUN_RECOVERED";',
        "  message_parameters: Readonly<Record<string, string>>;",
        "  group_key: string;",
        '  route_id: "UI-OPS-002";',
        "  route_parameters: Readonly<Record<string, string>>;",
        "  trace_id: string | null;",
        "}",
        "",
    ]
    return "\n".join(lines).encode()


def generate(root: Path) -> None:
    openapi = render_openapi()
    (root / "packages/contracts/openapi/execution-control.openapi.json").write_bytes(openapi)
    (root / "packages/contracts/src/execution-control.ts").write_bytes(render_consumer(openapi))
    event_schema = render_terminal_event_schema()
    (root / "packages/contracts/schemas/execution-terminal-event.schema.json").write_bytes(
        event_schema
    )
    (root / "packages/contracts/src/execution-terminal-events.ts").write_bytes(
        render_terminal_event_consumer(event_schema)
    )


if __name__ == "__main__":
    generate(Path(__file__).resolve().parents[3])
