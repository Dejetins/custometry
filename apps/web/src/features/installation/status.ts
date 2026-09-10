import type { InstallationStatus } from "@custometry/contracts";

/** Typed operational port; 503 is a valid failure projection, never cached success. */
export async function readInstallationStatus(signal: AbortSignal): Promise<InstallationStatus> {
  const controller = new AbortController();
  const abort = () => controller.abort();
  signal.addEventListener("abort", abort, { once: true });
  if (signal.aborted) controller.abort();
  const timeout = setTimeout(abort, 5000);
  try {
    const response = await fetch("/api/installation/status", {
      signal: controller.signal, cache: "no-store", headers: { Accept: "application/json" },
    });
    if (response.status !== 200 && response.status !== 503) throw new Error("STATUS_UNAVAILABLE");
    const value: unknown = await response.json();
    if (!isInstallationStatus(value, response.status)) throw new Error("STATUS_INVALID");
    return value;
  } finally {
    clearTimeout(timeout);
    signal.removeEventListener("abort", abort);
  }
}

export function isInstallationStatus(value: unknown, status: number): value is InstallationStatus {
  if (!value || typeof value !== "object") return false;
  const item = value as Partial<InstallationStatus>;
  if (item.schema_version !== "custometry-installation-status/v1" ||
      item.next_action !== "bootstrap_not_available" || typeof item.version !== "string" ||
      !item.version.trim() || !item.components) return false;
  const states = [item.components.database, item.components.schema, item.components.storage];
  if (!states.every(state => state === "ready" || state === "not_ready")) return false;
  if (status === 200) return item.state === "ready_for_bootstrap" && states.every(state => state === "ready") && item.code == null;
  return status === 503 && item.state === "not_ready" && states.includes("not_ready") &&
    ["DATABASE_UNAVAILABLE", "SCHEMA_INCOMPATIBLE", "STORAGE_UNAVAILABLE"].includes(item.code ?? "");
}
