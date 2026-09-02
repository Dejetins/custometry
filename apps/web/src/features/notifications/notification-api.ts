import { notificationOperations } from "../../../../../packages/contracts/src/notifications";

export const NOTIFICATIONS_CONTRACT_VERSION = "1.0.0" as const;

export type NotificationSeverity = "info" | "warning" | "critical";
export type NotificationCategory =
  | "run"
  | "data_quality"
  | "data_freshness"
  | "forecast"
  | "schedule"
  | "system"
  | "security"
  | "admin";
export type NotificationFreshness = "fresh" | "stale" | "degraded";

export interface NotificationDeepLink {
  readonly status: "available" | "unavailable";
  readonly route_id: string | null;
  readonly parameters: Readonly<Record<string, string>> | null;
}

export interface NotificationItem {
  readonly notification_id: string;
  readonly workspace_id: string;
  readonly latest_event_id: string;
  readonly source_owner: string;
  readonly source_type: string;
  readonly severity: NotificationSeverity;
  readonly category: NotificationCategory;
  readonly occurred_at: string;
  readonly message_code: string;
  readonly message_parameters: Readonly<Record<string, string | number | boolean>>;
  readonly group_key: string;
  readonly source_event_count: number;
  readonly trace_id: string | null;
  readonly resolved: boolean;
  readonly read: boolean;
  readonly dismissed: boolean;
  readonly acknowledged: boolean;
  readonly revision: number;
  readonly freshness: NotificationFreshness;
  readonly deep_link: NotificationDeepLink;
}

export interface NotificationListResponse {
  readonly items: readonly NotificationItem[];
  readonly visible_count: number;
}

export interface NotificationCapabilities {
  readonly workspaceId: string;
  readonly permissions: ReadonlySet<string>;
}

export interface NotificationFilters {
  readonly severity?: NotificationSeverity;
  readonly category?: NotificationCategory;
  readonly read?: boolean;
  readonly acknowledged?: boolean;
  readonly resolved?: boolean;
}

interface IdentityMeResponse {
  readonly workspace_id: string;
  readonly permissions: readonly string[];
}

interface ErrorResponse {
  readonly code?: string;
  readonly current_revision?: number;
}

export class NotificationApiError extends Error {
  public constructor(
    public readonly status: number,
    public readonly code: string,
    public readonly currentRevision?: number,
  ) {
    super(code);
    this.name = "NotificationApiError";
  }
}

function requestIdentity(prefix: string): string {
  const generated = globalThis.crypto?.randomUUID?.();
  return generated ? `${prefix}-${generated}` : `${prefix}-${Date.now().toString(36)}`;
}

async function errorFrom(response: Response): Promise<NotificationApiError> {
  let payload: ErrorResponse = {};
  try {
    payload = (await response.json()) as ErrorResponse;
  } catch {
    // A non-JSON gateway response is still represented by a stable local code.
  }
  return new NotificationApiError(
    response.status,
    payload.code ?? `HTTP_${response.status}`,
    payload.current_revision,
  );
}

function notificationQuery(filters: NotificationFilters): string {
  const query = new URLSearchParams();
  if (filters.severity) query.append("severity", filters.severity);
  if (filters.category) query.append("category", filters.category);
  if (filters.read !== undefined) query.set("read", String(filters.read));
  if (filters.acknowledged !== undefined) {
    query.set("acknowledged", String(filters.acknowledged));
  }
  if (filters.resolved !== undefined) query.set("resolved", String(filters.resolved));
  query.set("limit", "100");
  return query.toString();
}

export class NotificationApiClient {
  public constructor(
    private readonly notificationsBase = "/api/notifications",
    private readonly identityBase = "/api/identity",
    private readonly fetcher: typeof fetch = globalThis.fetch.bind(globalThis),
  ) {}

  private async notificationRequest<T>(
    path: string,
    init: RequestInit = {},
  ): Promise<T> {
    const headers = new Headers(init.headers);
    headers.set("Accept", "application/json");
    headers.set("X-Contract-Version", NOTIFICATIONS_CONTRACT_VERSION);
    headers.set("X-Request-ID", requestIdentity("w35"));
    const response = await this.fetcher(`${this.notificationsBase}${path}`, {
      ...init,
      credentials: "same-origin",
      headers,
    });
    if (!response.ok) throw await errorFrom(response);
    return (await response.json()) as T;
  }

  public async capabilities(): Promise<NotificationCapabilities> {
    const response = await this.fetcher(`${this.identityBase}/me`, {
      method: "GET",
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    });
    if (!response.ok) throw await errorFrom(response);
    const payload = (await response.json()) as IdentityMeResponse;
    return {
      workspaceId: payload.workspace_id,
      permissions: new Set(payload.permissions),
    };
  }

  public list(filters: NotificationFilters): Promise<NotificationListResponse> {
    const query = notificationQuery(filters);
    return this.notificationRequest<NotificationListResponse>(
      `${notificationOperations.list_notifications.path}?${query}`,
      { method: notificationOperations.list_notifications.method },
    );
  }

  public unreadCount(): Promise<{ readonly unread_count: number; readonly capped: boolean }> {
    return this.notificationRequest(notificationOperations.get_unread_count.path, {
      method: notificationOperations.get_unread_count.method,
    });
  }

  public detail(notificationId: string): Promise<NotificationItem> {
    const path = notificationOperations.get_notification.path.replace(
      "{notification_id}",
      encodeURIComponent(notificationId),
    );
    return this.notificationRequest(path, {
      method: notificationOperations.get_notification.method,
    });
  }

  public mutate(
    item: NotificationItem,
    action: "read" | "dismiss" | "acknowledge",
  ): Promise<NotificationItem> {
    const operation = action === "read"
      ? notificationOperations.mark_notification_read
      : action === "dismiss"
        ? notificationOperations.dismiss_notification
        : notificationOperations.acknowledge_notification;
    const path = operation.path.replace(
      "{notification_id}",
      encodeURIComponent(item.notification_id),
    );
    const body = action === "read"
      ? { expected_revision: item.revision }
      : {
          expected_revision: item.revision,
          reason_code: action === "dismiss" ? "USER_DISMISSED" : "OPERATOR_CONFIRMED",
        };
    return this.notificationRequest(path, {
      method: operation.method,
      headers: {
        "Content-Type": "application/json",
        "Idempotency-Key": requestIdentity(`w35-${action}`),
      },
      body: JSON.stringify(body),
    });
  }
}

export const notificationApi = new NotificationApiClient();
