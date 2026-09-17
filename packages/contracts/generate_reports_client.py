"""Generate the bounded draft client from the versioned Presentation OpenAPI."""

from pathlib import Path
import hashlib
import json
from tools.custometry_quality.check_contract_drift import render_typescript


def render(root: Path) -> bytes:
    raw = (root / "packages/contracts/openapi/reports.openapi.json").read_bytes()
    schema = json.loads(raw)
    types = (
        render_typescript(
            {**schema, "paths": {}}, source_digest=hashlib.sha256(raw).hexdigest(), schema_ids=[]
        )
        .decode()
        .split("export class FoundationApiClient")[0]
    )
    return (
        types
        + """export class DraftReportClient {
  public constructor(private readonly baseUrl: string, private readonly fetcher: typeof fetch = globalThis.fetch.bind(globalThis)) {}
  private async request<T>(path: string, input?: unknown, csrfToken?: string): Promise<T> {
    const response = await this.fetcher(`${this.baseUrl}${path}`, {
      method: input === undefined ? "GET" : "POST", credentials: "same-origin", cache: "no-store",
      headers: input === undefined ? {} : {"Content-Type": "application/json", "X-CSRF-Token": csrfToken ?? ""},
      ...(input === undefined ? {} : {body: JSON.stringify(input)}),
    });
    if (!response.ok) {
      const error = await response.json() as {code?: string};
      throw new Error(error.code ?? `DRAFT_REPORT_HTTP_${response.status}`);
    }
    return response.json() as Promise<T>;
  }
  public prepare(input: PrepareRequest, csrf: string): Promise<PreparedResponse> { return this.request("/prepare", input, csrf); }
  public create(input: SaveRequest, csrf: string): Promise<DraftResponse> { return this.request("/", input, csrf); }
  public save(id: string, input: SaveRequest, csrf: string): Promise<DraftResponse> { return this.request(`/${encodeURIComponent(id)}/versions`, input, csrf); }
  public get(id: string): Promise<DraftResponse> { return this.request(`/${encodeURIComponent(id)}`); }
  public preview(id: string, snapshot: string, locator: Record<string, string> = {}): Promise<DraftResponse> { const query = new URLSearchParams(locator); return this.request(`/${encodeURIComponent(id)}/snapshots/${encodeURIComponent(snapshot)}${query.size ? "?" + query.toString() : ""}`); }
  public list(offset = 0, limit = 50): Promise<ReportList> { return this.request(`/?offset=${offset}&limit=${limit}`); }
}
"""
    ).encode()


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    (root / "packages/contracts/src/reports-client.ts").write_bytes(render(root))
