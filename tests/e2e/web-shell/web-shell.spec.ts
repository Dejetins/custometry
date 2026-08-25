import { expect, test, type Page, type TestInfo } from "@playwright/test";

interface BrowserDiagnostics {
  readonly consoleErrors: string[];
  readonly pageErrors: string[];
  readonly failedRequests: string[];
  readonly expectedCancellations: string[];
  readonly errorResponses: string[];
}

function collectDiagnostics(page: Page): BrowserDiagnostics {
  const evidence: BrowserDiagnostics = {
    consoleErrors: [],
    pageErrors: [],
    failedRequests: [],
    expectedCancellations: [],
    errorResponses: [],
  };
  page.on("console", (message) => {
    if (message.type() === "error") evidence.consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => evidence.pageErrors.push(error.message));
  page.on("requestfailed", (request) => {
    const diagnostic = `${request.method()} ${request.url()} ${request.failure()?.errorText ?? "unknown"}`;
    if (request.url().endsWith("/api/health/ready") && request.failure()?.errorText === "net::ERR_ABORTED") {
      evidence.expectedCancellations.push(diagnostic);
    } else {
      evidence.failedRequests.push(diagnostic);
    }
  });
  page.on("response", (response) => {
    if (response.status() >= 400) evidence.errorResponses.push(`${response.status()} ${response.url()}`);
  });
  return evidence;
}

async function installContractFixtures(page: Page): Promise<void> {
  await page.route("**/api/health/ready", async (route) => {
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ status: "ready", version: "w31-contract-fixture" }) });
  });
  await page.route("**/help-index.json", async (route) => {
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ documents: [] }) });
  });
}

async function assertCleanDiagnostics(diagnostics: BrowserDiagnostics): Promise<void> {
  expect(diagnostics.consoleErrors, "console errors").toEqual([]);
  expect(diagnostics.pageErrors, "page errors").toEqual([]);
  expect(diagnostics.failedRequests, "failed same-origin requests").toEqual([]);
  expect(diagnostics.errorResponses, "HTTP error responses").toEqual([]);
}

async function assertNoWholePageOverflow(page: Page): Promise<void> {
  const geometry = await page.evaluate(() => ({
    clientWidth: document.documentElement.clientWidth,
    scrollWidth: document.documentElement.scrollWidth,
    bodyScrollWidth: document.body.scrollWidth,
  }));
  expect(geometry.scrollWidth, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
  expect(geometry.bodyScrollWidth, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
}

async function capture(page: Page, testInfo: TestInfo, name: string): Promise<void> {
  await page.screenshot({ path: testInfo.outputPath(`${name}.png`), fullPage: true });
}

test.beforeEach(async ({ page }) => {
  await installContractFixtures(page);
  await page.addInitScript(() => window.localStorage.clear());
});

test("route identity, history, refresh, RU/EN, current navigation and focus are preserved", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await page.goto("/w/northwind-retail/overview");

  await expect(page.locator("[data-shell-profile]")) .toHaveAttribute("data-shell-profile", "workspace");
  await expect(page.getByRole("heading", { level: 1, name: "Workspace Overview" })).toBeVisible();
  await expect(page.getByRole("link", { name: "Overview" })).toHaveAttribute("aria-current", "page");
  await assertNoWholePageOverflow(page);

  await page.getByRole("link", { name: "Analytics" }).click();
  await expect(page).toHaveURL(/\/w\/northwind-retail\/analytics\/sales$/);
  await expect(page.getByRole("heading", { level: 1, name: "Sales Overview" })).toBeFocused();

  await page.goBack();
  await expect(page).toHaveURL(/\/w\/northwind-retail\/overview$/);
  await expect(page.locator('[data-focus-key="nav-analytics/sales"]')).toBeFocused();
  await page.reload();
  await expect(page.getByRole("heading", { level: 1, name: "Workspace Overview" })).toBeVisible();

  await page.getByRole("button", { name: "Switch language" }).click();
  await expect(page.getByRole("heading", { level: 1, name: "Обзор рабочего пространства" })).toBeVisible();
  await expect(page).toHaveURL(/\/w\/northwind-retail\/overview$/);
  await expect(page).toHaveTitle(/Обзор рабочего пространства · Custometry/);
  await capture(page, testInfo, "shell-ru-history");
  await assertCleanDiagnostics(diagnostics);
});

test("keyboard-only traversal reaches skip link and preserves logical route focus", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await page.goto("/w/northwind-retail/overview");

  await page.keyboard.press("Tab");
  await expect(page.getByRole("link", { name: "Skip to content" })).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("main")).toBeFocused();

  let reachedAnalytics = false;
  for (let index = 0; index < 14; index += 1) {
    await page.keyboard.press("Tab");
    reachedAnalytics = await page.evaluate(() => (document.activeElement as HTMLElement | null)?.dataset.focusKey === "nav-analytics/sales");
    if (reachedAnalytics) break;
  }
  expect(reachedAnalytics).toBe(true);
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { level: 1, name: "Sales Overview" })).toBeFocused();
  await expect(page.getByRole("link", { name: "Analytics" })).toHaveAttribute("aria-current", "page");
  await capture(page, testInfo, "keyboard-route-focus");
  await assertCleanDiagnostics(diagnostics);
});

test("system surfaces are safe, localized and explicitly fixture-backed", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  const states = [
    ["w31-forbidden", "UI-SYS-001", "This surface is not available"],
    ["w31-session-expired", "UI-SYS-003", "Your session has expired"],
    ["w31-maintenance", "UI-SYS-004", "Part of Custometry is under maintenance"],
    ["w31-upgrade-required", "UI-SYS-005", "A client upgrade is required"],
  ] as const;

  for (const [view, surfaceId, title] of states) {
    await page.goto(`/w/northwind-retail/overview?view=${view}`);
    await expect(page.locator(`[data-system-surface="${surfaceId}"]`)).toBeVisible();
    await expect(page.getByRole("heading", { level: 1, name: title })).toBeVisible();
    await expect(page.getByRole("note")).toContainText("No backend authorization");
    await assertNoWholePageOverflow(page);
  }

  await page.goto("/resource-that-is-not-registered");
  await expect(page.locator('[data-system-surface="UI-SYS-002"]')).toBeVisible();
  await expect(page.getByText("SYS-404-PATH")).toBeVisible();
  await page.getByRole("button", { name: "Switch language" }).click();
  await expect(page.getByRole("heading", { level: 1, name: "Страница не найдена" })).toBeVisible();
  await capture(page, testInfo, "system-404-ru");
  await assertCleanDiagnostics(diagnostics);
});

test("200 percent reflow equivalent and reduced motion keep the shell usable", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/w/northwind-retail/overview?view=w31-maintenance");

  const viewport = testInfo.project.use.viewport;
  if (!viewport) throw new Error("W31 project must declare a viewport");
  await page.setViewportSize({ width: Math.floor(viewport.width / 2), height: Math.floor(viewport.height / 2) });
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.getByRole("button", { name: "Switch language" })).toBeVisible();
  await assertNoWholePageOverflow(page);

  const motion = await page.evaluate(() => {
    const shell = getComputedStyle(document.querySelector(".app-shell") as Element);
    const nav = getComputedStyle(document.querySelector(".nav-item") as Element);
    return { shellTransition: shell.transitionDuration, navTransition: nav.transitionDuration, shellAnimation: shell.animationDuration };
  });
  expect(motion).toEqual({ shellTransition: "0s", navTransition: "0s", shellAnimation: "0s" });
  await capture(page, testInfo, "zoom-200-reduced-motion");
  await assertCleanDiagnostics(diagnostics);
});
