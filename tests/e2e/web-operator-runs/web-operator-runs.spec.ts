import { expect, test, type Page, type TestInfo } from "@playwright/test";

interface Diagnostics {
  readonly consoleErrors: string[];
  readonly pageErrors: string[];
  readonly failedRequests: string[];
  readonly errorResponses: string[];
}

function collectDiagnostics(page: Page): Diagnostics {
  const evidence: Diagnostics = { consoleErrors: [], pageErrors: [], failedRequests: [], errorResponses: [] };
  page.on("console", (message) => { if (message.type() === "error") evidence.consoleErrors.push(message.text()); });
  page.on("pageerror", (error) => evidence.pageErrors.push(error.message));
  page.on("requestfailed", (request) => {
    const abortedHealth = request.url().endsWith("/api/health/ready") && request.failure()?.errorText === "net::ERR_ABORTED";
    if (!abortedHealth) evidence.failedRequests.push(`${request.method()} ${request.url()} ${request.failure()?.errorText ?? "unknown"}`);
  });
  page.on("response", (response) => { if (response.status() >= 400) evidence.errorResponses.push(`${response.status()} ${response.url()}`); });
  return evidence;
}

async function assertCleanDiagnostics(evidence: Diagnostics): Promise<void> {
  expect(evidence.consoleErrors, "console errors").toEqual([]);
  expect(evidence.pageErrors, "page errors").toEqual([]);
  expect(evidence.failedRequests, "failed requests").toEqual([]);
  expect(evidence.errorResponses, "HTTP error responses").toEqual([]);
}

async function assertNoOverflow(page: Page): Promise<void> {
  const geometry = await page.evaluate(() => ({
    clientWidth: document.documentElement.clientWidth,
    scrollWidth: document.documentElement.scrollWidth,
    bodyScrollWidth: document.body.scrollWidth,
    surfaceRight: document.querySelector(".operator-runs")?.getBoundingClientRect().right ?? 0,
  }));
  expect(geometry.scrollWidth, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
  expect(geometry.bodyScrollWidth, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
  expect(geometry.surfaceRight, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
}

async function useActor(page: Page, token: "operator" | "owner" | "no-permission"): Promise<void> {
  await page.setExtraHTTPHeaders({ Authorization: `Bearer ${token}` });
}

async function reset(page: Page): Promise<Record<string, string>> {
  const response = await page.request.post("http://127.0.0.1:8000/__fixture__/reset");
  expect(response.ok()).toBe(true);
  return response.json() as Promise<Record<string, string>>;
}

async function capture(page: Page, testInfo: TestInfo, name: string): Promise<void> {
  await page.screenshot({ path: testInfo.outputPath(`${name}.png`), fullPage: true });
}

test.describe.configure({ mode: "serial" });

test.beforeEach(async ({ page }) => {
  await reset(page);
  await useActor(page, "operator");
  await page.addInitScript(() => window.localStorage.clear());
});

test("real W36 boundary loads, filters, refreshes, persists cancel/retry, and exposes fencing ancestry", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await page.goto("/w/northwind-retail/runs");
  await expect(page.getByRole("heading", { level: 1, name: "Operator Center" })).toBeVisible();
  await expect(page.locator(".operator-run")).toHaveCount(6);
  await expect(page.getByText("trace-failed-safe")).toBeVisible();
  await expect(page.getByText("bulk")).toHaveCount(2);

  await page.getByLabel("State").selectOption("FAILED");
  await expect(page.locator(".operator-run")).toHaveCount(1);
  await expect(page.getByText("Margin analysis")).toBeVisible();
  await page.getByLabel("State").selectOption("all");
  await page.getByLabel("Execution kind").selectOption("forecast");
  await expect(page.locator(".operator-run")).toHaveCount(1);
  await expect(page.getByText("Cancelable forecast")).toBeVisible();
  await page.getByLabel("Execution kind").selectOption("");
  await page.getByLabel("Trace identity").fill("trace-failed-safe");
  await expect(page.locator(".operator-run")).toHaveCount(1);
  await page.getByRole("button", { name: "Clear filters" }).click();
  await expect(page.locator(".operator-run")).toHaveCount(6);

  const failed = page.locator(".operator-run").filter({ hasText: "Margin analysis" });
  await failed.getByRole("button", { name: "Inspect run" }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await expect(page.getByText("RESOURCE_LIMIT_EXCEEDED")).toBeVisible();
  await expect(page.getByText("Reduce the bounded input range and retry failed nodes.")).toBeVisible();
  await page.getByLabel("Audit reason").fill("retry after bounded operator review");
  await page.getByRole("button", { name: "Retry run" }).click();
  await expect(page.getByText("Retry created a new run with ancestry.")).toBeAttached();
  await expect(page.getByRole("dialog").getByText("Retry of run").locator("..")).toContainText(/[0-9a-f-]{36}/i);
  await page.getByRole("button", { name: "Close run details" }).click();

  const running = page.locator(".operator-run").filter({ hasText: "Daily retail ingestion" });
  await running.getByRole("button", { name: "Inspect run" }).click();
  await page.getByLabel("Audit reason").fill("cancel during bounded maintenance");
  await page.getByRole("button", { name: "Cancel run" }).click();
  await expect(page.getByText("Cancellation requested; state is CANCELLING until cleanup completes.")).toBeAttached();
  await expect(page.getByRole("dialog")).toContainText("Cancelling");
  await page.getByRole("button", { name: "Close run details" }).click();

  const drain = await page.request.post("http://127.0.0.1:8000/__fixture__/drain");
  expect(drain.ok()).toBe(true);
  await expect.poll(async () => {
    const card = page.locator(".operator-run").filter({ hasText: "Daily retail ingestion" });
    return card.textContent();
  }, { timeout: 8_000 }).toContain("Cancelled");

  const reconciled = page.locator(".operator-run").filter({ hasText: "Reconciled lease" });
  await reconciled.getByRole("button", { name: "Inspect run" }).click();
  await expect(page.locator(".operator-attempts > li")).toHaveCount(2);
  await expect(page.getByText("Retry of attempt").nth(1).locator("..")).not.toContainText("Original run");
  await expect(page.getByText("Fencing token").first().locator("..")).toContainText("2");
  await page.getByRole("button", { name: "Close run details" }).click();

  await assertNoOverflow(page);
  await capture(page, testInfo, "real-w36-operator-runs");
  await assertCleanDiagnostics(diagnostics);
});

test("real W36 authorization filters actions and fails closed before list presentation", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await useActor(page, "owner");
  await page.goto("/w/northwind-retail/runs");
  await expect(page.locator(".operator-run")).toHaveCount(6);
  await page.locator(".operator-run").filter({ hasText: "Margin analysis" }).getByRole("button", { name: "Inspect run" }).click();
  await expect(page.getByText("The current policy does not grant run.retry.")).toBeVisible();
  await expect(page.getByRole("button", { name: "Retry run" })).toHaveCount(0);
  await page.getByRole("button", { name: "Close run details" }).click();

  await useActor(page, "no-permission");
  await page.reload();
  await expect(page.getByRole("alert")).toContainText("Operator Center is unavailable");
  await capture(page, testInfo, "real-w36-forbidden");
  expect(diagnostics.errorResponses.some((entry) => entry.startsWith("403 "))).toBe(true);
  expect(diagnostics.pageErrors).toEqual([]);
  expect(diagnostics.failedRequests).toEqual([]);
});

test("RU keyboard flow restores focus and 200-percent reflow honors reduced motion", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.addInitScript(() => window.localStorage.setItem("custometry-language", "ru"));
  await page.goto("/w/northwind-retail/runs");
  await expect(page.getByRole("heading", { level: 1, name: "Центр оператора" })).toBeVisible();

  const skipLink = page.getByRole("link", { name: "Перейти к содержимому" });
  await skipLink.focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("main")).toBeFocused();

  let detailReached = false;
  for (let index = 0; index < 24; index += 1) {
    await page.keyboard.press("Tab");
    detailReached = await page.evaluate(() => document.activeElement?.textContent?.includes("Открыть запуск") ?? false);
    if (detailReached) break;
  }
  expect(detailReached).toBe(true);
  await page.keyboard.press("Enter");
  await expect(page.getByRole("dialog", { name: "Связи запуска и попыток" })).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("button", { name: "Открыть запуск" }).first()).toBeFocused();

  for (const label of ["Состояние", "Тип выполнения", "Идентификатор трассировки", "Автообновление каждые 5 секунд"]) {
    await expect(page.getByLabel(label)).toBeVisible();
  }
  const viewport = testInfo.project.use.viewport;
  if (!viewport) throw new Error("W34 project must declare a viewport");
  await page.setViewportSize({ width: Math.floor(viewport.width / 2), height: Math.floor(viewport.height / 2) });
  await assertNoOverflow(page);
  const motion = await page.evaluate(() => {
    const card = getComputedStyle(document.querySelector(".operator-run") as Element);
    const spinner = getComputedStyle(document.querySelector(".operator-spinner") ?? document.body);
    return { transition: card.transitionDuration, animation: spinner.animationDuration };
  });
  expect(motion).toEqual({ transition: "0s", animation: "0s" });
  await capture(page, testInfo, "ru-keyboard-reflow-reduced-motion");
  await assertCleanDiagnostics(diagnostics);
});

test("fixture-only presentation states keep loading, empty, stale, degraded, and failed distinct", async ({ page }, testInfo) => {
  let releaseLoading: (() => void) | undefined;
  const loadingGate = new Promise<void>((resolve) => { releaseLoading = resolve; });
  await page.route("**/api/execution/runs?*", async (route) => { await loadingGate; await route.continue(); });
  const navigation = page.goto("/w/northwind-retail/runs");
  await expect(page.locator(".operator-state").getByText("Loading operator runs")).toBeVisible();
  releaseLoading?.();
  await navigation;
  await expect(page.locator(".operator-run")).toHaveCount(6);
  await page.unroute("**/api/execution/runs?*");

  await page.route("**/api/execution/runs?*", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ runs: [], visible_count: 0 }) }));
  await page.reload();
  await expect(page.getByText("No runs match this view")).toBeVisible();
  await page.unroute("**/api/execution/runs?*");

  for (const freshness of ["stale", "degraded"] as const) {
    await page.route("**/api/execution/queue-summary", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ counts: { QUEUED: 1 }, lane_counts: { default: 1 }, oldest_queued_age_seconds: 30, observed_at: "2026-08-28T10:00:00Z", freshness }) }));
    await page.reload();
    await expect(page.getByText(freshness === "stale" ? "Queue summary is stale" : "Queue summary is degraded")).toBeVisible();
    await page.unroute("**/api/execution/queue-summary");
  }

  await page.route("**/api/execution/runs?*", (route) => route.fulfill({ status: 503, contentType: "application/json", body: JSON.stringify({ code: "DELIVERY_UNAVAILABLE" }) }));
  await page.reload();
  await expect(page.getByRole("alert")).toContainText("Runs could not be loaded");
  await capture(page, testInfo, "fixture-only-presentation-states");
});
