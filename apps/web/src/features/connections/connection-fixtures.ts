import {
  ConnectionsApiError,
  type CatalogResponse,
  type ConnectionCatalogPort,
  type ConnectionCatalogResult,
  type ConnectionResponse,
  type ConnectionTestResponse,
  type CreateConnectionInput,
} from "./connections-api";

const observedAt = "2026-08-30T09:30:00Z";
const populated: ConnectionCatalogResult = {
  support: "available",
  observedAt,
  connections: [
    { connectionId: "fixture-pg", displayName: "Retail PostgreSQL", connectorId: "postgresql", status: "ready", ownerLabel: "Data platform", updatedAt: "2026-08-30T09:22:00Z", secretReferencePresent: true },
    { connectionId: "fixture-xlsx", displayName: "Weekly assortment template", connectorId: "xlsx_template", status: "stale", ownerLabel: "Merchandising", updatedAt: "2026-08-29T15:10:00Z", secretReferencePresent: false },
    { connectionId: "fixture-ch", displayName: "Store events", connectorId: "clickhouse", status: "degraded", ownerLabel: "Operations", updatedAt: "2026-08-30T08:50:00Z", secretReferencePresent: true },
    { connectionId: "fixture-csv", displayName: "Returns intake", connectorId: "csv_template", status: "draft", ownerLabel: "Data stewardship", updatedAt: "2026-08-28T12:00:00Z", secretReferencePresent: false },
  ],
};

export class ConnectionPresentationFixture implements ConnectionCatalogPort {
  public constructor(private readonly state = "w33-fixture") {}

  public async capabilities() {
    if (this.state === "w33-forbidden") throw new ConnectionsApiError(403, "FORBIDDEN");
    return {
      principalId: "fixture-principal",
      workspaceId: "fixture-workspace",
      permissions: new Set(["connection.read_metadata", "connection.manage", "connection.secret.rotate"]),
    };
  }

  public async list(): Promise<ConnectionCatalogResult> {
    if (this.state === "w33-failed") throw new ConnectionsApiError(503, "SOURCE_INTAKE_UNAVAILABLE");
    if (this.state === "w33-empty") return { ...populated, connections: [] };
    if (this.state === "w33-stale") return { ...populated, connections: populated.connections.map((item) => ({ ...item, status: "stale" as const })) };
    if (this.state === "w33-refreshing") return { ...populated, connections: populated.connections.map((item, index) => index === 0 ? { ...item, status: "refreshing" as const } : item) };
    if (this.state === "w33-degraded") return { ...populated, connections: populated.connections.map((item, index) => index === 0 ? { ...item, status: "degraded" as const } : item) };
    return populated;
  }

  public async create(input: CreateConnectionInput): Promise<ConnectionResponse> {
    return { connection_id: "fixture-created", source_system_id: "fixture-source", connector_id: "postgresql", display_name: input.display_name, status: "active" };
  }

  public async test(connectionId: string): Promise<ConnectionTestResponse> {
    return {
      status: "ready",
      connection: { connection_id: connectionId, source_system_id: "fixture-source", connector_id: "postgresql", display_name: "Fixture PostgreSQL", status: "active" },
      capabilities: { driver: "psycopg", driver_version: "3.fixture", supported_source_versions: ["17"], consistency_modes: ["repeatable_read"], pushdown: ["projection"], read_only_enforced: true },
    };
  }

  public async discover(): Promise<CatalogResponse> {
    return { objects: [{ schema_name: "retail", object_name: "receipts", object_type: "table", columns: ["receipt_id"] }] };
  }
}
