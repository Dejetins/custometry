"""Generate sales DTOs with the existing schema renderer and bounded HTTP methods."""

from pathlib import Path
import hashlib
import json
from tools.custometry_quality.check_contract_drift import render_typescript


def render(root: Path) -> bytes:
    raw = (root / "packages/contracts/openapi/analytics.openapi.json").read_bytes()
    schema = json.loads(raw)
    # The shared renderer supports DTOs; its Foundation HTTP generator has no inputs.
    types = (
        render_typescript(
            {**schema, "paths": {}}, source_digest=hashlib.sha256(raw).hexdigest(), schema_ids=[]
        )
        .decode()
        .split("export class FoundationApiClient")[0]
    )
    return (
        types
        + """export class SalesReportClient {
  public constructor(private readonly baseUrl: string, private readonly fetcher: typeof fetch = globalThis.fetch.bind(globalThis)) {}
  public async run(input: SalesRunRequest, csrfToken: string): Promise<SalesResponse> {
    const response = await this.fetcher(`${this.baseUrl}/sales-reports/v1`, {
      method: "POST", credentials: "same-origin",
      headers: {"Content-Type": "application/json", "X-CSRF-Token": csrfToken},
      body: JSON.stringify(input),
    });
    if (!response.ok) throw new Error(`SALES_REPORT_HTTP_${response.status}`);
    return response.json() as Promise<SalesResponse>;
  }
  public async get(resultId: string): Promise<SalesResponse> {
    const response = await this.fetcher(`${this.baseUrl}/sales-reports/v1/${encodeURIComponent(resultId)}`, {credentials: "same-origin"});
    if (!response.ok) throw new Error(`SALES_REPORT_HTTP_${response.status}`);
    return response.json() as Promise<SalesResponse>;
  }
}
"""
    ).encode()


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    (root / "packages/contracts/src/analytics-client.ts").write_bytes(render(root))
