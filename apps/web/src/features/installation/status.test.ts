import { describe, expect, it, vi } from "vitest";
import { isInstallationStatus, readInstallationStatus } from "./status";
const ready = { schema_version: "custometry-installation-status/v1", next_action: "bootstrap_not_available", version: "1.0", components: { database: "ready", schema: "ready", storage: "ready" }, state: "ready_for_bootstrap" };
describe("operational status trust boundary", () => {
  it("rejects malformed and contradictory readiness without inventing success", () => {
    expect(isInstallationStatus(ready, 200)).toBe(true);
    expect(isInstallationStatus(ready, 503)).toBe(false);
    expect(isInstallationStatus({ ...ready, components: { ...ready.components, storage: "not_ready" } }, 200)).toBe(false);
    expect(isInstallationStatus({ ...ready, schema_version: "other" }, 200)).toBe(false);
    expect(isInstallationStatus(null, 200)).toBe(false);
    expect(isInstallationStatus({ ...ready, version: "" }, 200)).toBe(false);
  });
  it("times out a non-responsive transport", async () => {
    vi.useFakeTimers();
    vi.stubGlobal("fetch", vi.fn((_url, init) => new Promise((_resolve, reject) => init.signal.addEventListener("abort", () => reject(new Error("aborted"))))));
    try {
      const result = expect(readInstallationStatus(new AbortController().signal)).rejects.toThrow("aborted");
      await vi.advanceTimersByTimeAsync(5000);
      await result;
    } finally { vi.unstubAllGlobals(); vi.useRealTimers(); }
  });
});
