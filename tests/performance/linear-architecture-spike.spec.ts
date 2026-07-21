import { readdirSync, readFileSync, statSync } from "node:fs";
import { cpus, platform, release, totalmem } from "node:os";
import { join } from "node:path";
import { gzipSync } from "node:zlib";

import { expect, test, type Page } from "@playwright/test";

type MetricName = "clientDispatch" | "responseToPaint" | "sseToPaint" | "inp" | "longTask";
type BrowserMetrics = Readonly<Record<MetricName, readonly number[]>>;

interface Distribution {
  readonly count: number;
  readonly p50: number;
  readonly p75: number;
  readonly p95: number;
  readonly max: number;
}

function round(value: number): number {
  return Math.round(value * 100) / 100;
}

function distribution(values: readonly number[]): Distribution {
  if (values.length === 0) return { count: 0, p50: 0, p75: 0, p95: 0, max: 0 };
  const sorted = [...values].sort((left, right) => left - right);
  const percentile = (value: number): number => {
    const index = Math.max(0, Math.ceil(value * sorted.length) - 1);
    return round(sorted[index] ?? 0);
  };
  return {
    count: sorted.length,
    p50: percentile(0.5),
    p75: percentile(0.75),
    p95: percentile(0.95),
    max: round(sorted[sorted.length - 1] ?? 0),
  };
}

function bundleCost(): { readonly rawBytes: number; readonly gzipBytes: number; readonly files: readonly string[] } {
  const assetsRoot = join(process.cwd(), "apps/web/dist/assets");
  const files = readdirSync(assetsRoot).filter((name) => /\.(css|js)$/.test(name)).sort();
  let rawBytes = 0;
  let gzipBytes = 0;
  for (const file of files) {
    const path = join(assetsRoot, file);
    rawBytes += statSync(path).size;
    gzipBytes += gzipSync(readFileSync(path)).byteLength;
  }
  return { rawBytes, gzipBytes, files };
}

interface DeterministicTransportControl {
  readonly startSse: () => void;
}

async function installDeterministicTransport(page: Page): Promise<DeterministicTransportControl> {
  let restRevision = 1;
  let sseRevision = 100;
  let releaseSse: (() => void) | undefined;
  const sseGate = new Promise<void>((resolve) => {
    releaseSse = resolve;
  });
  await page.route("**/api/health/ready", (route) => route.fulfill({
    contentType: "application/json",
    body: JSON.stringify({ status: "ready", service: "api", version: "w20-benchmark" }),
  }));
  await page.route("**/api/spike/workspace-summary", async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 15));
    await route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({
        workspace_id: "northwind-retail",
        revision: restRevision++,
        result_count: 12,
        freshness: "authoritative",
      }),
    });
  });
  await page.route("**/api/spike/events", async (route) => {
    await sseGate;
    await new Promise((resolve) => setTimeout(resolve, 12));
    await route.fulfill({
      status: 200,
      headers: { "cache-control": "no-cache", "content-type": "text/event-stream" },
      body: [
        "retry: 10",
        `id: ${sseRevision}`,
        "event: workspace-snapshot",
        `data: ${JSON.stringify({
          workspace_id: "northwind-retail",
          revision: sseRevision++,
          result_count: 13,
          freshness: "authoritative",
        })}`,
        "",
        "",
      ].join("\n"),
    });
  });
  return {
    startSse: () => releaseSse?.(),
  };
}

async function readMetrics(page: Page): Promise<BrowserMetrics> {
  return page.evaluate(() => {
    const bridge = window.__CUSTOMETRY_SPIKE_METRICS__;
    if (!bridge) throw new Error("W20 metric bridge unavailable");
    return bridge.read();
  });
}

test("repeatable W20 client-overhead benchmark", async ({ browserName, page }) => {
  const transport = await installDeterministicTransport(page);
  await page.goto("/w/northwind-retail/analytics/sales?view=linear-spike");
  await expect(page.getByTestId("query-status")).toHaveText("success");
  await page.evaluate(() => window.__CUSTOMETRY_SPIKE_METRICS__?.reset());

  const sampleCount = 30;
  for (let index = 1; index <= sampleCount; index += 1) {
    await page.getByRole("button", { name: "Refresh authoritative snapshot" }).click();
    await page.waitForFunction(
      (expected) => (window.__CUSTOMETRY_SPIKE_METRICS__?.read().responseToPaint.length ?? 0) >= expected,
      index,
    );
  }
  transport.startSse();
  await page.waitForFunction(
    (expected) => (window.__CUSTOMETRY_SPIKE_METRICS__?.read().sseToPaint.length ?? 0) >= expected,
    sampleCount,
  );
  await page.waitForTimeout(250);

  const metrics = await readMetrics(page);
  const summary = {
    schemaVersion: 1,
    revision: process.env.GIT_COMMIT ?? "working-tree-w20",
    workload: {
      dataRows: 12,
      samples: sampleCount,
      state: "warm_after_one_cold_mount",
      cache: "TanStack Query warm cache with explicit refetch",
      network: "same-process Playwright route with deterministic 15ms REST and 12ms SSE mock delay",
    },
    runtime: {
      browserName,
      browserVersion: page.context().browser()?.version() ?? "unknown",
      userAgent: await page.evaluate(() => navigator.userAgent),
      viewport: page.viewportSize(),
      clientHardwareConcurrency: await page.evaluate(() => navigator.hardwareConcurrency),
      hostPlatform: `${platform()} ${release()}`,
      hostCpu: cpus()[0]?.model ?? "unknown",
      hostLogicalCpus: cpus().length,
      hostRamBytes: totalmem(),
    },
    distributionsMs: {
      clientDispatch: distribution(metrics.clientDispatch),
      responseToPaint: distribution(metrics.responseToPaint.slice(0, sampleCount)),
      sseToPaint: distribution(metrics.sseToPaint.slice(0, sampleCount)),
      inp: distribution(metrics.inp),
      longTask: distribution(metrics.longTask),
    },
    bundle: bundleCost(),
  };

  console.log(`W20_PERFORMANCE_RESULT ${JSON.stringify(summary)}`);

  expect(summary.distributionsMs.clientDispatch.count).toBeGreaterThanOrEqual(sampleCount);
  expect(summary.distributionsMs.clientDispatch.p75).toBeLessThanOrEqual(20);
  expect(summary.distributionsMs.clientDispatch.p95).toBeLessThanOrEqual(50);
  expect(summary.distributionsMs.responseToPaint.count).toBe(sampleCount);
  expect(summary.distributionsMs.responseToPaint.p75).toBeLessThanOrEqual(100);
  expect(summary.distributionsMs.responseToPaint.p95).toBeLessThanOrEqual(200);
  expect(summary.distributionsMs.sseToPaint.count).toBe(sampleCount);
  expect(summary.distributionsMs.sseToPaint.p75).toBeLessThanOrEqual(100);
  expect(summary.distributionsMs.sseToPaint.p95).toBeLessThanOrEqual(200);
  expect(summary.distributionsMs.inp.count).toBeGreaterThanOrEqual(sampleCount);
  expect(summary.distributionsMs.inp.p75).toBeLessThanOrEqual(100);
  expect(summary.distributionsMs.inp.max).toBeLessThanOrEqual(200);
  expect(metrics.longTask.filter((duration) => duration > 50)).toEqual([]);
});
