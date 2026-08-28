import { expect, test, type Page, type TestInfo } from "@playwright/test";

interface BrowserDiagnostics {
  readonly consoleErrors: string[];
  readonly pageErrors: string[];
  readonly failedRequests: string[];
  readonly errorResponses: string[];
}

function collectDiagnostics(page: Page): BrowserDiagnostics {
  const evidence: BrowserDiagnostics = {
    consoleErrors: [], pageErrors: [], failedRequests: [], errorResponses: [],
  };
  page.on("console", (message) => {
    if (message.type() === "error") evidence.consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => evidence.pageErrors.push(error.message));
  page.on("requestfailed", (request) => {
    const abortedHealth = request.url().endsWith("/api/health/ready")
      && request.failure()?.errorText === "net::ERR_ABORTED";
    if (!abortedHealth) {
      evidence.failedRequests.push(
        `${request.method()} ${request.url()} ${request.failure()?.errorText ?? "unknown"}`,
      );
    }
  });
  page.on("response", (response) => {
    if (response.status() >= 400) {
      evidence.errorResponses.push(`${response.status()} ${response.url()}`);
    }
  });
  return evidence;
}

async function assertCleanDiagnostics(diagnostics: BrowserDiagnostics): Promise<void> {
  expect(diagnostics.consoleErrors, "console errors").toEqual([]);
  expect(diagnostics.pageErrors, "page errors").toEqual([]);
  expect(diagnostics.failedRequests, "failed requests").toEqual([]);
  expect(diagnostics.errorResponses, "HTTP error responses").toEqual([]);
}

async function assertNoWholePageOverflow(page: Page): Promise<void> {
  const geometry = await page.evaluate(() => ({
    clientWidth: document.documentElement.clientWidth,
    scrollWidth: document.documentElement.scrollWidth,
    bodyScrollWidth: document.body.scrollWidth,
    inboxRight: document.querySelector(".notification-inbox")?.getBoundingClientRect().right ?? 0,
  }));
  expect(geometry.scrollWidth, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
  expect(geometry.bodyScrollWidth, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
  expect(geometry.inboxRight, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
}

async function resetRealBoundary(page: Page): Promise<void> {
  const response = await page.request.post("http://127.0.0.1:8000/__fixture__/reset");
  expect(response.ok()).toBe(true);
}

async function useActor(page: Page, token: "acknowledger" | "reader" | "no-permission"): Promise<void> {
  await page.setExtraHTTPHeaders({ Authorization: `Bearer ${token}` });
}

async function capture(page: Page, testInfo: TestInfo, name: string): Promise<void> {
  await page.screenshot({ path: testInfo.outputPath(`${name}.png`), fullPage: true });
}

test.describe.configure({ mode: "serial" });

test.beforeEach(async ({ page }) => {
  await resetRealBoundary(page);
  await useActor(page, "acknowledger");
  await page.addInitScript(() => window.localStorage.clear());
});

test("real W37 adapter loads, filters, persists acknowledgement, groups duplicates, and navigates safely", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await page.goto("/notifications");

  await expect(page.getByRole("heading", { level: 1, name: "Notification Inbox" })).toBeVisible();
  await expect(page.locator(".notification-card")).toHaveCount(3);
  await expect(page.getByText("2 events in group")).toBeVisible();
  await expect(page.getByText("Some notification data may be delayed")).toBeVisible();

  await page.getByLabel("Severity").selectOption("warning");
  await expect(page.locator(".notification-card")).toHaveCount(1);
  await expect(page.locator(".notification-card--warning")).toBeVisible();
  await page.getByLabel("Severity").selectOption("all");
  await expect(page.locator(".notification-card")).toHaveCount(3);

  await page.getByLabel("Category").selectOption("system");
  await expect(page.locator(".notification-card")).toHaveCount(0);
  await page.getByLabel("Category").selectOption("all");
  await expect(page.locator(".notification-card")).toHaveCount(3);

  await page.getByLabel("Read state").selectOption("true");
  await expect(page.locator(".notification-card")).toHaveCount(0);
  await page.getByLabel("Read state").selectOption("false");
  await expect(page.locator(".notification-card")).toHaveCount(3);
  await page.getByLabel("Read state").selectOption("all");

  await page.getByLabel("Acknowledgement").selectOption("true");
  await expect(page.locator(".notification-card")).toHaveCount(0);
  await page.getByLabel("Acknowledgement").selectOption("false");
  await expect(page.locator(".notification-card")).toHaveCount(3);
  await page.getByLabel("Acknowledgement").selectOption("all");

  await page.getByLabel("Resolution").selectOption("true");
  await expect(page.locator(".notification-card")).toHaveCount(1);
  await page.getByLabel("Resolution").selectOption("false");
  await expect(page.locator(".notification-card")).toHaveCount(2);
  await page.getByLabel("Resolution").selectOption("all");
  await expect(page.locator(".notification-card")).toHaveCount(3);

  const critical = page.locator(".notification-card--critical");
  await critical.getByRole("button", { name: "View details" }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.getByRole("button", { name: "Acknowledge" }).click();
  await expect(page.getByText("Acknowledged", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Close details" }).click();

  await page.reload();
  await expect(page.locator(".notification-card--critical")).toContainText("Acknowledged");
  await page.locator(".notification-card--critical").getByRole("button", { name: "View details" }).click();
  await page.getByRole("link", { name: "Open related run" }).click();
  await expect(page).toHaveURL(/\/w\/northwind-retail\/runs\/run-critical$/);
  await expect(page.getByRole("heading", { level: 1, name: "Run Detail" })).toBeVisible();

  await page.goBack();
  await expect(page).toHaveURL(/\/notifications$/);
  await assertNoWholePageOverflow(page);
  await capture(page, testInfo, "real-w37-acknowledged-inbox");
  await assertCleanDiagnostics(diagnostics);
});

test("real W37 permission denial and access revocation fail closed", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await useActor(page, "no-permission");
  await page.goto("/notifications");
  await expect(page.getByRole("alert")).toContainText("Notification inbox is unavailable");
  expect(diagnostics.errorResponses.some((entry) => entry.startsWith("403 "))).toBe(true);

  await useActor(page, "reader");
  await page.reload();
  await expect(page.locator(".notification-card")).toHaveCount(3);
  await expect(page.locator(".notification-card--critical").getByRole("button", { name: "View details" })).toBeVisible();
  await page.locator(".notification-card--critical").getByRole("button", { name: "View details" }).click();
  await expect(page.getByText("Acknowledgement requires notification.acknowledge.")).toBeVisible();
  await page.getByRole("button", { name: "Close details" }).click();

  const revoke = await page.request.post("http://127.0.0.1:8000/__fixture__/revoke");
  expect(revoke.ok()).toBe(true);
  await page.getByRole("button", { name: "Refresh" }).click();
  await expect(page.getByText("No notifications match this view")).toBeVisible();
  await capture(page, testInfo, "real-w37-revoked-empty");
  expect(diagnostics.consoleErrors).toHaveLength(4);
  expect(diagnostics.consoleErrors.every((entry) => entry.includes("403 (Forbidden)"))).toBe(true);
  expect(diagnostics.errorResponses.every((entry) => entry.startsWith("403 "))).toBe(true);
  expect(diagnostics.pageErrors).toEqual([]);
  expect(diagnostics.failedRequests).toEqual([]);
});

test("RU keyboard-only drawer flow restores focus and exposes accessible names", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await page.addInitScript(() => window.localStorage.setItem("custometry-language", "ru"));
  await page.goto("/notifications");
  await expect(page.getByRole("heading", { level: 1, name: "Центр уведомлений" })).toBeVisible();

  const skipLink = page.getByRole("link", { name: "Перейти к содержимому" });
  await skipLink.focus();
  await expect(skipLink).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("main")).toBeFocused();

  let detailReached = false;
  for (let index = 0; index < 32; index += 1) {
    await page.keyboard.press("Tab");
    detailReached = await page.evaluate(() =>
      document.activeElement?.textContent?.includes("Открыть подробности") ?? false,
    );
    if (detailReached) break;
  }
  expect(detailReached).toBe(true);
  await page.keyboard.press("Enter");
  await expect(page.getByRole("dialog", { name: "Подробности уведомления" })).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("button", { name: "Открыть подробности" }).first()).toBeFocused();

  for (const label of ["Важность", "Категория", "Прочитано", "Подтверждено", "Разрешено"]) {
    await expect(page.getByLabel(label)).toBeVisible();
  }
  await capture(page, testInfo, "ru-keyboard-focus-restored");
  await assertNoWholePageOverflow(page);
  await assertCleanDiagnostics(diagnostics);
});

test("loading, empty, degraded, failed, 200-percent reflow, and reduced motion remain truthful", async ({ page }, testInfo) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  let releaseLoading: (() => void) | undefined;
  const loadingGate = new Promise<void>((resolve) => { releaseLoading = resolve; });
  await page.route("**/api/notifications/items?*", async (route) => {
    await loadingGate;
    await route.continue();
  });
  await page.goto("/notifications");
  await expect(page.getByText("Loading notifications")).toBeVisible();
  releaseLoading?.();
  await expect(page.locator(".notification-card")).toHaveCount(3);
  await page.unroute("**/api/notifications/items?*");

  await page.route("**/api/notifications/items?*", async (route) => {
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ items: [], visible_count: 0 }) });
  });
  await page.route("**/api/notifications/unread-count", async (route) => {
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ unread_count: 0, capped: false }) });
  });
  await page.reload();
  await expect(page.getByText("No notifications match this view")).toBeVisible();
  await page.unroute("**/api/notifications/items?*");
  await page.unroute("**/api/notifications/unread-count");

  await page.reload();
  await expect(page.getByText("Some notification data may be delayed")).toBeVisible();
  await page.route("**/api/notifications/items?*", async (route) => {
    await route.fulfill({ status: 503, contentType: "application/json", body: JSON.stringify({ code: "DEPENDENCY_UNAVAILABLE" }) });
  });
  await page.reload();
  await expect(page.getByRole("alert")).toContainText("Notifications could not be loaded");
  await page.unroute("**/api/notifications/items?*");
  await page.reload();
  await expect(page.locator(".notification-card")).toHaveCount(3);

  const viewport = testInfo.project.use.viewport;
  if (!viewport) throw new Error("W35 project must declare a viewport");
  await page.setViewportSize({ width: Math.floor(viewport.width / 2), height: Math.floor(viewport.height / 2) });
  await assertNoWholePageOverflow(page);
  const motion = await page.evaluate(() => {
    const card = getComputedStyle(document.querySelector(".notification-card") as Element);
    const spinner = getComputedStyle(document.querySelector(".notification-spinner") ?? document.body);
    return { transition: card.transitionDuration, animation: spinner.animationDuration };
  });
  expect(motion).toEqual({ transition: "0s", animation: "0s" });
  await capture(page, testInfo, "reflow-200-reduced-motion");
});
