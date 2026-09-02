import { describe, expect, it, vi } from "vitest";

import {
  ConnectionsApiError,
  W14SourceIntakeClient,
} from "../../src/features/connections/connections-api";

describe("W33 typed W14 source-intake adapter", () => {
  it("uses exact W14 create/test/catalog operations and required contract headers", async () => {
    const responses = [
      new Response(JSON.stringify({ connection_id: "connection-1", source_system_id: "source-1", connector_id: "postgresql", display_name: "Retail", status: "active" }), { status: 200 }),
      new Response(JSON.stringify({ status: "ready", connection: { connection_id: "connection-1", source_system_id: "source-1", connector_id: "postgresql", display_name: "Retail", status: "active" }, capabilities: { driver: "psycopg", driver_version: "3.2", supported_source_versions: ["17"], consistency_modes: ["repeatable_read"], pushdown: ["projection"], read_only_enforced: true } }), { status: 200 }),
      new Response(JSON.stringify({ objects: [] }), { status: 200 }),
    ];
    const fetcher = vi.fn().mockImplementation(async () => responses.shift());
    const client = new W14SourceIntakeClient("/api/connections", "/api/identity", fetcher);
    await client.create({ connector_id: "postgresql", display_name: "Retail", profile_ref: "retail_demo", secret_ref: "retail_reader" });
    await client.test("connection-1");
    await client.discover("connection-1");

    expect(fetcher.mock.calls.map(([url]) => url)).toEqual(["/api/connections/", "/api/connections/connection-1/test", "/api/connections/connection-1/catalog"]);
    for (const [, init] of fetcher.mock.calls as [string, RequestInit][]) {
      const headers = new Headers(init.headers);
      expect(headers.get("X-Contract-Version")).toBe("1.0.0");
      expect(headers.get("X-Request-ID")).toMatch(/^w33-/);
    }
  });

  it("rejects any W14 response that echoes credential or network references", async () => {
    const fetcher = vi.fn().mockResolvedValue(new Response(JSON.stringify({ connection_id: "connection-1", source_system_id: "source-1", connector_id: "postgresql", display_name: "Retail", status: "active", secret_ref: "must-not-escape" }), { status: 200 }));
    const client = new W14SourceIntakeClient("/api/connections", "/api/identity", fetcher);
    await expect(client.create({ connector_id: "postgresql", display_name: "Retail", profile_ref: "retail_demo", secret_ref: "retail_reader" })).rejects.toEqual(expect.objectContaining<Partial<ConnectionsApiError>>({ code: "SOURCE_INTAKE_REDACTION_BREACH" }));
  });

  it("declares the missing W14 list boundary without issuing an invented request", async () => {
    const fetcher = vi.fn();
    const client = new W14SourceIntakeClient("/api/connections", "/api/identity", fetcher);
    await expect(client.list()).resolves.toEqual(expect.objectContaining({ support: "unavailable", stableCode: "CONNECTION_LIST_UNAVAILABLE" }));
    expect(fetcher).not.toHaveBeenCalled();
  });
});
