import { executionControlOperations } from "../../../../../packages/contracts/src/execution-control";

export const EXECUTION_CONTROL_CONTRACT_VERSION = "1.0.0" as const;

export type RunState =
  | "CREATED"
  | "VALIDATING"
  | "QUEUED"
  | "RUNNING"
  | "CANCELLING"
  | "SUCCEEDED"
  | "FAILED"
  | "CANCELLED"
  | "PARTIAL";
export type AttemptState =
  | "PENDING"
  | "READY"
  | "RUNNING"
  | "RETRY_WAIT"
  | "SUCCEEDED"
  | "FAILED"
  | "CANCELLED";
export type RetryMode = "failed_nodes" | "full_rerun";
export type QueueFreshness = "fresh" | "stale" | "degraded";

export interface OperatorRun {
  readonly run_id: string;
  readonly owner_principal_id: string;
  readonly execution_kind: string;
  readonly lane: string;
  readonly safe_title: string;
  readonly safe_trace_id: string | null;
  readonly state: RunState;
  readonly revision: number;
  readonly retry_of_id: string | null;
  readonly retry_mode: RetryMode | null;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface OperatorAttempt {
  readonly attempt_id: string;
  readonly state: AttemptState;
  readonly attempt_number: number;
  readonly fencing_token: number;
  readonly retry_of_id: string | null;
  readonly lease_expires_at: string | null;
  readonly failure_code: "RESOURCE_LIMIT_EXCEEDED" | null;
  readonly observed_limit?: number | null;
  readonly configured_limit?: number | null;
  readonly safe_remediation: string | null;
}

export interface OperatorRunDetail extends OperatorRun {
  readonly attempts: readonly OperatorAttempt[];
}

export interface RunListResponse {
  readonly runs: readonly OperatorRun[];
  readonly visible_count: number;
}

export interface QueueSummary {
  readonly counts: Readonly<Record<string, number>>;
  readonly lane_counts: Readonly<Record<string, number>>;
  readonly oldest_queued_age_seconds: number | null;
  readonly observed_at: string;
  readonly freshness: QueueFreshness;
}

export interface RunCapabilities {
  readonly workspaceId: string;
  readonly permissions: ReadonlySet<string>;
}

export interface RunFilters {
  readonly states?: readonly RunState[];
  readonly executionKind?: string;
  readonly safeTraceId?: string;
}

interface IdentityMeResponse {
  readonly workspace_id: string;
  readonly permissions: readonly string[];
}

interface ErrorResponse {
  readonly code?: string;
  readonly current_state?: string;
}

export class OperatorRunsApiError extends Error {
  public constructor(
    public readonly status: number,
    public readonly code: string,
    public readonly currentState?: string,
  ) {
    super(code);
    this.name = "OperatorRunsApiError";
  }
}

function requestIdentity(prefix: string): string {
  const generated = globalThis.crypto?.randomUUID?.();
  return generated ? `${prefix}-${generated}` : `${prefix}-${Date.now().toString(36)}`;
}

async function errorFrom(response: Response): Promise<OperatorRunsApiError> {
  let payload: ErrorResponse = {};
  try {
    payload = (await response.json()) as ErrorResponse;
  } catch {
    // A non-JSON gateway response still receives a stable presentation code.
  }
  return new OperatorRunsApiError(
    response.status,
    payload.code ?? `HTTP_${response.status}`,
    payload.current_state,
  );
}

function queryFor(filters: RunFilters): string {
  const query = new URLSearchParams({ limit: "100" });
  for (const state of filters.states ?? []) query.append("states", state);
  if (filters.executionKind?.trim()) query.set("execution_kind", filters.executionKind.trim());
  if (filters.safeTraceId?.trim()) query.set("safe_trace_id", filters.safeTraceId.trim());
  return query.toString();
}

export class OperatorRunsApiClient {
  public constructor(
    private readonly executionBase = "/api/execution",
    private readonly identityBase = "/api/identity",
    private readonly fetcher: typeof fetch = globalThis.fetch.bind(globalThis),
  ) {}

  private async request<T>(path: string, init: RequestInit = {}): Promise<T> {
    const headers = new Headers(init.headers);
    headers.set("Accept", "application/json");
    headers.set("X-Contract-Version", EXECUTION_CONTROL_CONTRACT_VERSION);
    headers.set("X-Request-ID", requestIdentity("w34"));
    const response = await this.fetcher(`${this.executionBase}${path}`, {
      ...init,
      credentials: "same-origin",
      headers,
    });
    if (!response.ok) throw await errorFrom(response);
    return (await response.json()) as T;
  }

  public async capabilities(): Promise<RunCapabilities> {
    const response = await this.fetcher(`${this.identityBase}/me`, {
      method: "GET",
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    });
    if (!response.ok) throw await errorFrom(response);
    const payload = (await response.json()) as IdentityMeResponse;
    return { workspaceId: payload.workspace_id, permissions: new Set(payload.permissions) };
  }

  public list(filters: RunFilters): Promise<RunListResponse> {
    return this.request(
      `${executionControlOperations.list_operator_runs.path}?${queryFor(filters)}`,
      { method: executionControlOperations.list_operator_runs.method },
    );
  }

  public summary(): Promise<QueueSummary> {
    return this.request(executionControlOperations.get_operator_queue_summary.path, {
      method: executionControlOperations.get_operator_queue_summary.method,
    });
  }

  public detail(runId: string): Promise<OperatorRunDetail> {
    const path = executionControlOperations.get_operator_run.path.replace(
      "{run_id}", encodeURIComponent(runId),
    );
    return this.request(path, { method: executionControlOperations.get_operator_run.method });
  }

  public mutate(
    run: OperatorRun,
    action: "cancel" | "retry",
    reason: string,
    mode: RetryMode = "failed_nodes",
  ): Promise<OperatorRun> {
    const operation = action === "cancel"
      ? executionControlOperations.cancel_operator_run
      : executionControlOperations.retry_operator_run;
    const path = operation.path.replace("{run_id}", encodeURIComponent(run.run_id));
    const body = action === "cancel"
      ? { expected_revision: run.revision, reason }
      : { expected_revision: run.revision, reason, mode };
    return this.request(path, {
      method: operation.method,
      headers: {
        "Content-Type": "application/json",
        "Idempotency-Key": requestIdentity(`w34-${action}`),
      },
      body: JSON.stringify(body),
    });
  }
}

export const operatorRunsApi = new OperatorRunsApiClient();
