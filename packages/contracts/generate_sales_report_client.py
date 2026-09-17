"""Generate the bounded sales report projections from production response models."""

import hashlib
import json
from pathlib import Path
from pydantic.json_schema import models_json_schema
from custometry_api.analytics.sales_models import SalesContext, SalesResponse, SalesRunRequest
from tools.custometry_quality.check_contract_drift import render_typescript


def render() -> bytes:
    _, schema = models_json_schema(
        [(m, "validation") for m in (SalesContext, SalesResponse, SalesRunRequest)]
    )
    schema = json.loads(json.dumps(schema).replace("#/$defs/", "#/components/schemas/"))
    document = {"openapi": "3.1.0", "components": {"schemas": schema["$defs"]}, "paths": {}}
    raw = json.dumps(document, sort_keys=True).encode()
    return (
        render_typescript(json.loads(raw), source_digest=hashlib.sha256(raw).hexdigest(), schema_ids=[])
        .decode()
        .split("export class FoundationApiClient")[0]
        .rstrip()
        .encode()
        + b"\n"
    )


if __name__ == "__main__":
    (Path(__file__).resolve().parent / "src/sales-report-client.ts").write_bytes(render())
