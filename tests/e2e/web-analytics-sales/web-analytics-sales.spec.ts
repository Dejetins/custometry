import { expect, test, type Page, type TestInfo } from "@playwright/test";

import { assertSalesAccessibility } from "../../accessibility/web-analytics-sales/accessibility-smoke";

interface Diagnostics {
  consoleErrors: string[];
  pageErrors: string[];
  failedRequests: string[];
  errorResponses: string[];
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

function expectCleanDiagnostics(evidence: Diagnostics): void {
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
    surfaceRight: document.querySelector(".sales-overview")?.getBoundingClientRect().right ?? 0,
  }));
  expect(geometry.scrollWidth, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
  expect(geometry.bodyScrollWidth, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
  expect(geometry.surfaceRight, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
}

async function useActor(page: Page, token: "owner" | "viewer" | "no-permission"): Promise<void> {
  await page.setExtraHTTPHeaders({ Authorization: `Bearer ${token}` });
}

async function capture(page: Page, testInfo: TestInfo, name: string): Promise<void> {
  await page.screenshot({ path: testInfo.outputPath(`${name}.png`), fullPage: true });
}

test.describe.configure({ mode: "serial" });

test.beforeEach(async ({ page }) => {
  const reset = await page.request.post("http://127.0.0.1:8000/__fixture__/reset");
  expect(reset.ok()).toBe(true);
  await useActor(page, "owner");
  await page.addInitScript(() => window.localStorage.clear());
});

test("real W16 PostgreSQL/API boundary renders metrics, filters, comparison, and Result Trust", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  const responses: string[] = [];
  page.on("response", (response) => {
    if (response.url().includes("/api/analytics/results")) responses.push(`${response.request().method()} ${response.status()}`);
  });
  await page.goto("/w/northwind-retail/analytics/sales");
  await expect(page.getByRole("heading", { level: 1, name: "Sales Overview" })).toBeVisible();
  const kpis = page.locator(".sales-kpi-strip");
  await expect(kpis).toContainText("425");
  await expect(kpis).toContainText("2");
  await expect(kpis).toContainText("212.5");
  await expect(kpis).toContainText("Margin is not exposed by the W16 sales projection.");
  await expect(page.getByText("W16 exposes governed period aggregates, not a time-series trend.")).toBeVisible();
  const breakdowns = page.getByLabel("Breakdowns");
  for (const label of ["Product", "Store", "Channel"]) await expect(breakdowns.getByText(label, { exact: true })).toBeVisible();

  const trustTrigger = page.getByRole("button", { name: "Open Result Trust" });
  await trustTrigger.click();
  const dialog = page.getByRole("dialog", { name: "Result Trust" });
  await expect(dialog).toContainText("receipt_header");
  await expect(dialog).toContainText("passed");
  await expect(dialog).toContainText("PVM decomposition is not part of W16");
  await expect(dialog).toContainText("aggregate recorded discount only");
  await page.keyboard.press("Escape");
  await expect(trustTrigger).toBeFocused();

  await page.getByLabel("Store").fill("store-1");
  await page.getByLabel("Channel").fill("web");
  await page.getByRole("button", { name: "Apply governed view" }).click();
  await expect(kpis).toContainText("145");
  await expect(kpis).toContainText("1");
  await expect.poll(() => responses.filter((entry) => entry === "POST 200").length).toBeGreaterThan(0);
  await assertSalesAccessibility(page);
  await assertNoOverflow(page);
  await capture(page, testInfo, "real-w16-sales-overview");
  expectCleanDiagnostics(diagnostics);
});

test("real W16 policy boundary keeps read-only visible and forbidden fail-closed", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await useActor(page, "viewer");
  await page.goto("/w/northwind-retail/analytics/sales");
  await expect(page.getByText(/analysis\.read/)).toBeVisible();
  await expect(page.getByRole("button", { name: "Apply governed view" })).toBeDisabled();

  await useActor(page, "no-permission");
  await page.reload();
  await expect(page.getByText("Sales Overview is unavailable")).toBeVisible();
  await capture(page, testInfo, "real-w16-forbidden");
  expect(diagnostics.errorResponses.some((entry) => entry.startsWith("403 "))).toBe(true);
  expect(diagnostics.consoleErrors).not.toEqual([]);
  expect(diagnostics.consoleErrors.every((entry) => entry.includes("403 (Forbidden)"))).toBe(true);
  expect(diagnostics.pageErrors).toEqual([]);
  expect(diagnostics.failedRequests).toEqual([]);
});

test("RU keyboard, 200-percent reflow equivalent, reduced motion, and accessibility semantics", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.addInitScript(() => window.localStorage.setItem("custometry-language", "ru"));
  await page.goto("/w/northwind-retail/analytics/sales");
  await expect(page.getByRole("heading", { level: 1, name: "Обзор продаж" })).toBeVisible();
  const skipLink = page.getByRole("link", { name: "Перейти к содержимому" });
  await skipLink.focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("main")).toBeFocused();
  const trustTrigger = page.getByRole("button", { name: "Открыть доверие к результату" });
  await trustTrigger.focus();
  await expect(trustTrigger).toBeFocused();
  const focusStyle = await trustTrigger.evaluate((element) => {
    const style = getComputedStyle(element);
    return { outlineStyle: style.outlineStyle, outlineWidth: style.outlineWidth };
  });
  expect(focusStyle.outlineStyle).not.toBe("none");
  expect(focusStyle.outlineWidth).not.toBe("0px");
  await page.keyboard.press("Enter");
  await expect(page.getByRole("dialog", { name: "Доверие к результату" })).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(trustTrigger).toBeFocused();
  const viewport = testInfo.project.use.viewport;
  if (!viewport) throw new Error("W32 project must declare a viewport");
  await page.setViewportSize({ width: Math.floor(viewport.width / 2), height: Math.floor(viewport.height / 2) });
  await assertNoOverflow(page);
  await assertSalesAccessibility(page);
  const motion = await page.evaluate(() => {
    const button = getComputedStyle(document.querySelector(".sales-button") as Element);
    const spinner = getComputedStyle(document.querySelector(".sales-spinner") ?? document.body);
    return { transition: button.transitionDuration, animation: spinner.animationDuration };
  });
  expect(motion).toEqual({ transition: "0s", animation: "0s" });
  await capture(page, testInfo, "ru-keyboard-reflow-reduced-motion");
  expectCleanDiagnostics(diagnostics);
});

test("presentation-only interceptions keep loading, empty, stale/degraded, refreshing, and failed distinct", async ({ page }, testInfo) => {
  let releaseLoading: (() => void) | undefined;
  const loadingGate = new Promise<void>((resolve) => { releaseLoading = resolve; });
  await page.route("**/api/analytics/results?*", async (route) => { await loadingGate; await route.continue(); });
  await page.goto("/w/northwind-retail/analytics/sales", { waitUntil: "commit" });
  await expect(page.getByText("Loading policy-visible sales result")).toBeVisible();
  releaseLoading?.();
  await expect(page.getByRole("heading", { level: 1, name: "Sales Overview" })).toBeVisible();
  await page.unroute("**/api/analytics/results?*");

  await page.route("**/api/analytics/results?*", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ results: [], visible_count: 0 }) }));
  await page.reload();
  await expect(page.getByText("No visible sales result")).toBeVisible();
  await page.unroute("**/api/analytics/results?*");

  const resultResponse = await page.request.get("http://127.0.0.1:8000/analytics/results?offset=0&limit=50", { headers: { Authorization: "Bearer owner" } });
  const payload = await resultResponse.json() as { results: Array<Record<string, unknown>>; visible_count: number };
  for (const state of ["stale", "degraded"] as const) {
    const result = { ...payload.results[0], freshness: { ...(payload.results[0].freshness as object), status: state } };
    await page.route("**/api/analytics/results?*", (route) => route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ results: [result], visible_count: 1 }) }));
    await page.reload();
    await expect(page.getByText(state === "stale" ? "Result freshness is stale" : "Result is degraded").first()).toBeVisible();
    await page.unroute("**/api/analytics/results?*");
  }

  await page.reload();
  await expect(page.locator(".sales-kpi-strip")).toContainText("425");
  await page.route("**/api/analytics/results?*", async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 250));
    await route.fulfill({ status: 503, contentType: "application/json", body: JSON.stringify({ code: "DEPENDENCY_UNAVAILABLE" }) });
  });
  await page.getByRole("button", { name: "Refresh" }).click();
  await expect(page.getByRole("button", { name: "Refreshing" })).toBeVisible();
  await expect(page.getByText("Refresh failed; the last authorized result remains visible.")).toBeVisible();
  await expect(page.locator(".sales-kpi-strip")).toContainText("425");
  await page.unroute("**/api/analytics/results?*");

  await page.route("**/api/analytics/results?*", (route) => route.fulfill({ status: 503, contentType: "application/json", body: JSON.stringify({ code: "DEPENDENCY_UNAVAILABLE" }) }));
  await page.reload();
  await expect(page.getByText("Sales result could not be loaded")).toBeVisible();
  await capture(page, testInfo, "presentation-only-states");
});
