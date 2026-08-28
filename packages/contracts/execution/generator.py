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


def generate(root: Path) -> None:
    openapi = render_openapi()
    (root / "packages/contracts/openapi/execution-control.openapi.json").write_bytes(openapi)
    (root / "packages/contracts/src/execution-control.ts").write_bytes(
        render_consumer(openapi)
    )


if __name__ == "__main__":
    generate(Path(__file__).resolve().parents[3])
