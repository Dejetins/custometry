export const SOURCE_INTAKE_CONTRACT_VERSION = "1.0.0" as const;

export type ConnectionStatus = "ready" | "refreshing" | "degraded" | "stale" | "failed" | "draft";
export type ConnectorId =
  | "postgresql"
  | "mssql"
  | "mysql"
  | "clickhouse"
  | "csv_template"
  | "xlsx_template"
  | "yandex_metrica";

export interface ConnectionListItem {
  readonly connectionId: string;
  readonly displayName: string;
  readonly connectorId: ConnectorId;
  readonly status: ConnectionStatus;
  readonly ownerLabel: string;
  readonly updatedAt: string;
  readonly secretReferencePresent: boolean;
}

export interface ConnectionCatalogResult {
  readonly support: "available" | "unavailable";
  readonly connections: readonly ConnectionListItem[];
  readonly observedAt: string;
  readonly stableCode?: "CONNECTION_LIST_UNAVAILABLE";
}

export interface ConnectionCapabilities {
  readonly principalId: string;
  readonly workspaceId: string;
  readonly permissions: ReadonlySet<string>;
}

export interface CreateConnectionInput {
  readonly connector_id: "postgresql";
  readonly profile_ref: string;
  readonly secret_ref: string;
  readonly display_name: string;
}

export interface ConnectionResponse {
  readonly connection_id: string;
  readonly source_system_id: string;
  readonly connector_id: "postgresql";
  readonly display_name: string;
  readonly status: "active" | "disabled" | "archived";
}

export interface ConnectionTestResponse {
  readonly status: "ready";
  readonly connection: ConnectionResponse;
  readonly capabilities: {
    readonly driver: string;
    readonly driver_version: string;
    readonly supported_source_versions: readonly string[];
    readonly consistency_modes: readonly string[];
    readonly pushdown: readonly string[];
    readonly read_only_enforced: boolean;
  };
}

export interface CatalogResponse {
  readonly objects: readonly {
    readonly schema_name: string;
    readonly object_name: string;
    readonly object_type: "table" | "view";
    readonly columns: readonly string[];
  }[];
}

export interface ConnectionCatalogPort {
  capabilities(): Promise<ConnectionCapabilities>;
  list(): Promise<ConnectionCatalogResult>;
  create(input: CreateConnectionInput): Promise<ConnectionResponse>;
  test(connectionId: string): Promise<ConnectionTestResponse>;
  discover(connectionId: string): Promise<CatalogResponse>;
}

export class ConnectionsApiError extends Error {
  public constructor(
    public readonly status: number,
    public readonly code: string,
  ) {
    super(code);
  }
}

interface IdentityMeResponse {
  readonly principal_id: string;
  readonly workspace_id: string;
  readonly permissions: readonly string[];
}

async function apiError(response: Response): Promise<ConnectionsApiError> {
  let code = "SOURCE_INTAKE_UNAVAILABLE";
  try {
    const payload = (await response.json()) as { readonly code?: unknown };
    if (typeof payload.code === "string") code = payload.code;
  } catch {
    // Preserve a stable, non-sensitive fallback without retaining response bodies.
  }
  return new ConnectionsApiError(response.status, code);
}

function requestIdentity(scope: string): string {
  return `${scope}-${crypto.randomUUID()}`;
}

function assertRedacted(payload: unknown): void {
  if (!payload || typeof payload !== "object") return;
  if ("secret_ref" in payload || "profile_ref" in payload) {
    throw new ConnectionsApiError(502, "SOURCE_INTAKE_REDACTION_BREACH");
  }
}

export class W14SourceIntakeClient implements ConnectionCatalogPort {
  public constructor(
    private readonly connectionsBase = "/api/connections",
    private readonly identityBase = "/api/identity",
    private readonly fetcher: typeof fetch = globalThis.fetch.bind(globalThis),
  ) {}

  private async request<T>(path: string, init: RequestInit): Promise<T> {
    const headers = new Headers(init.headers);
    headers.set("Accept", "application/json");
    headers.set("X-Contract-Version", SOURCE_INTAKE_CONTRACT_VERSION);
    headers.set("X-Request-ID", requestIdentity("w33"));
    const response = await this.fetcher(`${this.connectionsBase}${path}`, {
      ...init,
      credentials: "same-origin",
      headers,
    });
    if (!response.ok) throw await apiError(response);
    return (await response.json()) as T;
  }

  public async capabilities(): Promise<ConnectionCapabilities> {
    const response = await this.fetcher(`${this.identityBase}/me`, {
      method: "GET",
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    });
    if (!response.ok) throw await apiError(response);
    const payload = (await response.json()) as IdentityMeResponse;
    return {
      principalId: payload.principal_id,
      workspaceId: payload.workspace_id,
      permissions: new Set(payload.permissions),
    };
  }

  public async list(): Promise<ConnectionCatalogResult> {
    // W14 intentionally exposes create/get-by-command boundaries but no list query.
    // Returning an explicit capability gap prevents the UI from inventing a GET contract.
    return {
      support: "unavailable",
      connections: [],
      observedAt: new Date().toISOString(),
      stableCode: "CONNECTION_LIST_UNAVAILABLE",
    };
  }

  public async create(input: CreateConnectionInput): Promise<ConnectionResponse> {
    const payload = await this.request<ConnectionResponse>("/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input),
    });
    assertRedacted(payload);
    return payload;
  }

  public async test(connectionId: string): Promise<ConnectionTestResponse> {
    const payload = await this.request<ConnectionTestResponse>(
      `/${encodeURIComponent(connectionId)}/test`,
      { method: "POST" },
    );
    assertRedacted(payload.connection);
    return payload;
  }

  public discover(connectionId: string): Promise<CatalogResponse> {
    return this.request(`/${encodeURIComponent(connectionId)}/catalog`, { method: "GET" });
  }
}

export const w14SourceIntakeApi = new W14SourceIntakeClient();
