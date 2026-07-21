export type SpikeMetricName =
  | "clientDispatch"
  | "responseToPaint"
  | "sseToPaint"
  | "inp"
  | "longTask";

export type SpikeMetrics = Readonly<Record<SpikeMetricName, readonly number[]>>;

const samples: Record<SpikeMetricName, number[]> = {
  clientDispatch: [],
  responseToPaint: [],
  sseToPaint: [],
  inp: [],
  longTask: [],
};

let pendingDispatchStartedAt: number | null = null;
let observersStarted = false;

function now(): number {
  return typeof performance === "undefined" ? Date.now() : performance.now();
}

export function recordSpikeMetric(name: SpikeMetricName, durationMs: number): void {
  if (Number.isFinite(durationMs) && durationMs >= 0) samples[name].push(durationMs);
}

export function beginDispatchMeasurement(): void {
  pendingDispatchStartedAt = now();
}

export function recordPendingDispatch(): void {
  if (pendingDispatchStartedAt === null) return;
  recordSpikeMetric("clientDispatch", now() - pendingDispatchStartedAt);
  pendingDispatchStartedAt = null;
}

export function recordNextPaint(name: "responseToPaint" | "sseToPaint", startedAt: number): void {
  const schedule = typeof requestAnimationFrame === "function"
    ? requestAnimationFrame
    : (callback: FrameRequestCallback): number => window.setTimeout(() => callback(now()), 0);
  schedule(() => schedule(() => recordSpikeMetric(name, now() - startedAt)));
}

export function resetSpikeMetrics(): void {
  for (const values of Object.values(samples)) values.length = 0;
  pendingDispatchStartedAt = null;
}

export function readSpikeMetrics(): SpikeMetrics {
  return {
    clientDispatch: [...samples.clientDispatch],
    responseToPaint: [...samples.responseToPaint],
    sseToPaint: [...samples.sseToPaint],
    inp: [...samples.inp],
    longTask: [...samples.longTask],
  };
}

function startPerformanceObservers(): void {
  if (observersStarted || typeof PerformanceObserver === "undefined") return;
  observersStarted = true;

  try {
    const eventObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        const eventEntry = entry as PerformanceEntry & { readonly interactionId?: number };
        if ((eventEntry.interactionId ?? 0) > 0) recordSpikeMetric("inp", entry.duration);
      }
    });
    eventObserver.observe({ type: "event", buffered: true, durationThreshold: 16 } as PerformanceObserverInit);
  } catch {
    // Event Timing is optional in unit-test DOMs; the browser harness records availability.
  }

  try {
    const longTaskObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) recordSpikeMetric("longTask", entry.duration);
    });
    longTaskObserver.observe({ type: "longtask", buffered: true } as PerformanceObserverInit);
  } catch {
    // Long Tasks is optional in unit-test DOMs; the browser harness records availability.
  }
}

declare global {
  interface Window {
    readonly __CUSTOMETRY_SPIKE_METRICS__?: {
      readonly read: typeof readSpikeMetrics;
      readonly reset: typeof resetSpikeMetrics;
    };
  }
}

if (typeof window !== "undefined") {
  Object.defineProperty(window, "__CUSTOMETRY_SPIKE_METRICS__", {
    configurable: true,
    value: { read: readSpikeMetrics, reset: resetSpikeMetrics },
  });
  startPerformanceObservers();
}
