import { recordPendingDispatch } from "./metrics";

export interface WorkspaceSnapshot {
  readonly workspaceId: string;
  readonly revision: number;
  readonly resultCount: number;
  readonly freshness: "authoritative" | "refreshing";
  readonly transport: "rest" | "sse";
  readonly receivedAt: number;
}

interface WorkspaceSnapshotPayload {
  readonly workspace_id: string;
  readonly revision: number;
  readonly result_count: number;
  readonly freshness: "authoritative" | "refreshing";
}

function isWorkspaceSnapshotPayload(value: unknown): value is WorkspaceSnapshotPayload {
  if (typeof value !== "object" || value === null) return false;
  const payload = value as Partial<WorkspaceSnapshotPayload>;
  return (
    typeof payload.workspace_id === "string" &&
    Number.isInteger(payload.revision) &&
    typeof payload.result_count === "number" &&
    (payload.freshness === "authoritative" || payload.freshness === "refreshing")
  );
}

function toSnapshot(
  payload: WorkspaceSnapshotPayload,
  transport: WorkspaceSnapshot["transport"],
): WorkspaceSnapshot {
  return {
    workspaceId: payload.workspace_id,
    revision: payload.revision,
    resultCount: payload.result_count,
    freshness: payload.freshness,
    transport,
    receivedAt: performance.now(),
  };
}

export async function fetchWorkspaceSnapshot(signal: AbortSignal): Promise<WorkspaceSnapshot> {
  recordPendingDispatch();
  const response = await fetch("/api/spike/workspace-summary", {
    headers: { Accept: "application/json" },
    signal,
  });
  if (!response.ok) throw new Error(`workspace snapshot failed with ${response.status}`);
  const payload: unknown = await response.json();
  if (!isWorkspaceSnapshotPayload(payload)) throw new Error("workspace snapshot contract mismatch");
  return toSnapshot(payload, "rest");
}

export async function fetchCancellableSnapshot(signal: AbortSignal): Promise<WorkspaceSnapshot> {
  const response = await fetch("/api/spike/cancellable-summary", {
    headers: { Accept: "application/json" },
    signal,
  });
  if (!response.ok) throw new Error(`cancellable snapshot failed with ${response.status}`);
  const payload: unknown = await response.json();
  if (!isWorkspaceSnapshotPayload(payload)) throw new Error("cancellable snapshot contract mismatch");
  return toSnapshot(payload, "rest");
}

export function subscribeToWorkspaceEvents(
  onSnapshot: (snapshot: WorkspaceSnapshot) => void,
): () => void {
  const events = new EventSource("/api/spike/events");
  events.addEventListener("workspace-snapshot", (event) => {
    const payload: unknown = JSON.parse((event as MessageEvent<string>).data);
    if (isWorkspaceSnapshotPayload(payload)) onSnapshot(toSnapshot(payload, "sse"));
  });
  return () => events.close();
}
