import { expect, test, type Page } from "@playwright/test";

interface BrowserEvidence {
  readonly consoleErrors: string[];
  readonly pageErrors: string[];
  readonly failedSameOriginRequests: string[];
  readonly sameOriginErrorResponses: string[];
}

function observeBrowser(page: Page): BrowserEvidence {
  const evidence: BrowserEvidence = {
    consoleErrors: [],
    pageErrors: [],
    failedSameOriginRequests: [],
    sameOriginErrorResponses: [],
  };
  const origin = new URL(process.env.CUSTOMETRY_BASE_URL ?? "http://invalid.local").origin;
  page.on("console", (message) => {
    if (message.type() === "error") evidence.consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => evidence.pageErrors.push(error.message));
  page.on("requestfailed", (request) => {
    if (request.url().startsWith(origin)) {
      evidence.failedSameOriginRequests.push(
        `${request.method()} ${request.url()}: ${request.failure()?.errorText ?? "unknown"}`,
      );
    }
  });
  page.on("response", (response) => {
    if (response.url().startsWith(origin) && response.status() >= 400) {
      const url = new URL(response.url());
      evidence.sameOriginErrorResponses.push(
        `${response.request().method()} ${response.status()} ${url.pathname}${url.search}`,
      );
    }
  });
  return evidence;
}

function expectCleanBrowser(evidence: BrowserEvidence): void {
  expect(evidence.consoleErrors).toEqual([]);
  expect(evidence.pageErrors).toEqual([]);
  expect(evidence.failedSameOriginRequests).toEqual([]);
  expect(evidence.sameOriginErrorResponses).toEqual([]);
}

async function expectUnauthenticatedSalesBoundary(evidence: BrowserEvidence): Promise<void> {
  await expect.poll(() => [...evidence.sameOriginErrorResponses].sort()).toEqual([
    "GET 401 /api/analytics/results?offset=0&limit=50",
    "GET 401 /api/identity/me",
  ]);
  expect(evidence.consoleErrors).toEqual([
    "Failed to load resource: the server responded with a status of 401 (Unauthorized)",
    "Failed to load resource: the server responded with a status of 401 (Unauthorized)",
  ]);
  expect(evidence.pageErrors).toEqual([]);
  expect(evidence.failedSameOriginRequests).toEqual([]);
  evidence.consoleErrors.splice(0);
  evidence.sameOriginErrorResponses.splice(0);
}

async function expectDocsReady(page: Page): Promise<void> {
  await expect(page.getByRole("heading", { level: 1 })).toContainText(
    "Custometry documentation",
  );
  await page.waitForLoadState("networkidle");
}

test("Foundation shell, API, language round-trip and local docs CSP/search", async ({
  page,
  request,
}) => {
  const evidence = observeBrowser(page);

  await page.goto("/help");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.getByText(/API readiness: ready/i)).toBeVisible();
  const languageButton = page.getByRole("button", { name: "Switch language" });
  await expect(languageButton).toHaveText("RU");
  await languageButton.click();
  await expect(page.getByText("Локальная работа")).toBeVisible();
  await expect(page.getByRole("link", { name: "Аналитика" })).toBeVisible();
  const russianLanguageButton = page.getByRole("button", { name: "Переключить язык" });
  await expect(russianLanguageButton).toHaveText("EN");
  await russianLanguageButton.click();
  await expect(page.getByText("Local first")).toBeVisible();

  const readiness = await request.get("/api/health/ready");
  expect(readiness.ok()).toBeTruthy();
  expect(await readiness.json()).toMatchObject({ status: "ready", service: "api" });

  const docsResponse = await page.goto("/docs/");
  expect(docsResponse?.ok()).toBeTruthy();
  const docsCsp = (await docsResponse?.allHeaders())?.["content-security-policy"] ?? "";
  expect(docsCsp).toContain("script-src 'self' 'sha256-");
  expect(docsCsp.match(/script-src[^;]*/)?.[0]).not.toContain("'unsafe-inline'");
  await expectDocsReady(page);
  const docsSearch = page.locator("input.md-search__input");
  if (!(await docsSearch.isVisible())) {
    await page.locator("label.md-header__button[for='__search']").click();
  }
  await docsSearch.pressSequentially("Foundation");
  await expect(page.locator(".md-search-result__link").first()).toBeVisible();
  expectCleanBrowser(evidence);
});

test("generated Help links and browser history preserve return-to-origin", async ({ page }) => {
  const evidence = observeBrowser(page);

  await page.goto("/help");
  await expect(page.getByText(/API readiness: ready/i)).toBeVisible();
  const articles = page.locator(".help-links a");
  await expect(articles).toHaveCount(8);
  await expect(articles.first()).toHaveAttribute("href", "/docs/");
  await articles.first().click();
  await expect(page).toHaveURL(/\/docs\/$/);
  await expectDocsReady(page);
  await page.goBack();
  await expect(page).toHaveURL(/\/help$/);
  await expect(articles).toHaveCount(8);
  await page.goForward();
  await expect(page).toHaveURL(/\/docs\/$/);
  await expectDocsReady(page);
  await page.goBack();
  await expect(page).toHaveURL(/\/help$/);
  expectCleanBrowser(evidence);
});

test("production sales route, 404 and shell return keep honest route state", async ({ page }) => {
  const evidence = observeBrowser(page);

  await page.goto("/w/northwind-retail/analytics/sales");
  await expect(page).toHaveURL(/\/w\/northwind-retail\/analytics\/sales$/);
  await expect(page.getByRole("heading", { level: 1, name: "Sales Overview" })).toBeVisible();
  await expect(page.getByText("Sales Overview is unavailable")).toBeVisible();
  await expect(page.getByText("Planned surface", { exact: true })).toHaveCount(0);
  await expectUnauthenticatedSalesBoundary(evidence);
  // The installed root has its own trusted packaged journey; this smoke owns shell navigation.
  await expect(page.getByRole("link", { name: "Custometry" })).toHaveAttribute("href", "/");
  await page.getByRole("link", { name: "Overview", exact: true }).click();
  await expect(page).toHaveURL(/\/w\/northwind-retail\/overview$/);
  await page.goBack();
  await expect(page).toHaveURL(/\/w\/northwind-retail\/analytics\/sales$/);
  await expect(page.getByRole("heading", { level: 1, name: "Sales Overview" })).toBeVisible();
  await expect(page.getByText("Sales Overview is unavailable")).toBeVisible();
  await expect(page.getByText("Planned surface", { exact: true })).toHaveCount(0);
  await expectUnauthenticatedSalesBoundary(evidence);
  await page.goForward();
  await expect(page).toHaveURL(/\/w\/northwind-retail\/overview$/);

  await page.goto("/not-a-registered-surface");
  await expect(page.getByRole("heading", { name: "Page not found" })).toBeVisible();
  await page.getByRole("link", { name: "Open allowed Overview" }).click();
  await expect(page).toHaveURL(/\/w\/northwind-retail\/overview$/);
  expectCleanBrowser(evidence);
});

test("responsive navigation exposes names and icons in every supported state", async ({
  page,
}, testInfo) => {
  const evidence = observeBrowser(page);
  await page.goto("/help");
  const viewport = page.viewportSize();

  if (viewport && viewport.width > 900) {
    const collapse = page.getByRole("button", { name: "Collapse navigation" });
    await expect(collapse).toBeVisible();
    await collapse.click();
    const expand = page.getByRole("button", { name: "Expand navigation" });
    await expect(expand).toBeVisible();
    const analytics = page.getByRole("link", { name: "Analytics" });
    await expect(analytics).toBeVisible();
    await expect(analytics.locator("svg")).toBeVisible();
    await expand.click();
    await expect(page.getByRole("button", { name: "Collapse navigation" })).toBeVisible();
  } else {
    await expect(page.getByRole("navigation")).toBeVisible();
    const analytics = page.getByRole("link", { name: "Analytics" });
    await expect(analytics).toBeVisible();
    await expect(analytics.locator("svg")).toBeVisible();
    const more = page.getByRole("button", { name: "More sections" });
    await expect(more).toBeVisible();

    await more.click();
    const dialog = page.getByRole("dialog", { name: "All sections" });
    await expect(dialog).toBeVisible();
    await expect(dialog.getByRole("link", { name: "Administration" })).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(dialog).toBeHidden();
    await expect(more).toBeFocused();

    await more.click();
    await dialog.getByRole("link", { name: "Administration" }).click();
    await expect(page).toHaveURL(/\/admin$/);
    await expect(dialog).toBeHidden();
    await expect(page.getByText("UI-ADMIN-001 · MVP")).toBeVisible();

    await more.click();
    const activeAdministration = dialog.getByRole("link", { name: "Administration" });
    await expect(activeAdministration).toHaveClass(/active/);
    await dialog.getByRole("button", { name: "Close menu" }).click();
    await expect(dialog).toBeHidden();
    await expect(more).toBeFocused();

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    expect(overflow, `${testInfo.project.name} has horizontal viewport overflow`).toBeLessThanOrEqual(1);
  }
  expectCleanBrowser(evidence);
});
