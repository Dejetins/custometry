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

function assertCleanDiagnostics(evidence: Diagnostics): void {
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
    surfaceRight: document.querySelector(".connections")?.getBoundingClientRect().right ?? 0,
  }));
  expect(geometry.scrollWidth, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
  expect(geometry.bodyScrollWidth, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
  expect(geometry.surfaceRight, JSON.stringify(geometry)).toBeLessThanOrEqual(geometry.clientWidth + 1);
}

async function useActor(page: Page, token: "owner" | "no-permission"): Promise<void> {
  await page.setExtraHTTPHeaders({ Authorization: `Bearer ${token}` });
}

async function capture(page: Page, testInfo: TestInfo, name: string): Promise<void> {
  await page.screenshot({ path: testInfo.outputPath(`${name}.png`), fullPage: true });
}

test.describe.configure({ mode: "serial" });
test.beforeEach(async ({ page }) => {
  await useActor(page, "owner");
});

test("real W14 adapter persists, authorizes, redacts, tests, and discovers PostgreSQL", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await page.goto("/w/northwind-retail/connections");
  await expect(page.getByRole("heading", { level: 1, name: "Connections" })).toBeVisible();
  await expect(page.getByText("Connection listing is not available in W14")).toBeVisible();
  await expect(page.getByText("CONNECTION_LIST_UNAVAILABLE")).toBeVisible();
  await page.getByRole("link", { name: "Add connection" }).first().click();
  await expect(page.getByRole("heading", { level: 1, name: "New connection" })).toBeVisible();

  await page.getByRole("button", { name: "Save and test" }).click();
  const errorSummary = page.getByRole("alert");
  await expect(errorSummary).toContainText("Review the highlighted fields");
  await expect(errorSummary).toBeFocused();
  await page.getByLabel("Display name").fill(`Retail PostgreSQL ${testInfo.project.name}`);
  await page.getByLabel("Network profile reference").fill("retail_demo");
  await page.getByLabel("Credential reference").fill("retail_demo_reader");
  await page.getByRole("button", { name: "Save draft" }).click();
  await expect(page.getByText("Draft saved in this tab only; the credential reference was not stored. W14 has no persisted draft lifecycle.")).toBeVisible();
  expect(await page.evaluate(() => window.sessionStorage.getItem("custometry:w33:connection-draft:northwind-retail"))).not.toContain("retail_demo_reader");
  await page.reload();
  await expect(page.getByLabel("Display name")).toHaveValue(`Retail PostgreSQL ${testInfo.project.name}`);
  await expect(page.getByLabel("Network profile reference")).toHaveValue("retail_demo");
  await expect(page.getByLabel("Credential reference")).toHaveValue("");
  await page.getByLabel("Credential reference").fill("retail_demo_reader");

  const createdResponse = page.waitForResponse((response) => response.request().method() === "POST" && response.url().endsWith("/api/connections/"));
  await page.getByRole("button", { name: "Save and test" }).click();
  const created = await (await createdResponse).json() as { connection_id: string; profile_ref?: string; secret_ref?: string };
  expect(created.profile_ref).toBeUndefined();
  expect(created.secret_ref).toBeUndefined();
  const result = page.getByRole("region", { name: "Connection persisted and read-only test passed" });
  await expect(result).toContainText("Read-only enforced");
  await expect(result).toContainText("2 catalog objects discovered");
  await expect(page.getByLabel("Credential reference")).toHaveValue("");
  await expect(page.locator("body")).not.toContainText("retail_demo_reader");

  const proofResponse = await page.request.get(`http://127.0.0.1:8033/__fixture__/proof/${created.connection_id}`);
  expect(proofResponse.ok()).toBe(true);
  expect(await proofResponse.json()).toEqual(expect.objectContaining({
    status: "active",
    connector_id: "postgresql",
    profile_reference_persisted: true,
    secret_reference_persisted: true,
    audit_count: 1,
    raw_references_exposed: false,
  }));
  await assertNoOverflow(page);
  await capture(page, testInfo, "real-w14-save-test-redacted");
  assertCleanDiagnostics(diagnostics);
});

test("presentation fixtures cover searchable list, governed states, and EN to RU localization", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await page.goto("/w/northwind-retail/connections?view=w33-fixture");
  await expect(page.getByText("Presentation fixture")).toBeVisible();
  await expect(page.locator(".connection-card")).toHaveCount(4);
  await page.getByRole("searchbox", { name: "Search connections" }).fill("assortment");
  await expect(page.locator(".connection-card")).toHaveCount(1);
  await expect(page.getByText("Weekly assortment template")).toBeVisible();
  await page.getByRole("button", { name: "Clear filters" }).click();
  await page.getByLabel("Status").selectOption("degraded");
  await expect(page.locator(".connection-card")).toHaveCount(1);
  await page.getByRole("button", { name: "Switch language" }).click();
  await expect(page.getByRole("heading", { level: 1, name: "Подключения" })).toBeVisible();
  await expect(page.getByText("Презентационный fixture")).toBeVisible();

  for (const [view, expected] of [
    ["w33-empty", "Подключений пока нет"],
    ["w33-refreshing", "Обновляется"],
    ["w33-stale", "Устарело"],
    ["w33-degraded", "Ограничено"],
    ["w33-forbidden", "Подключения недоступны"],
    ["w33-failed", "Не удалось загрузить подключения"],
  ] as const) {
    await page.goto(`/w/northwind-retail/connections?view=${view}`);
    const state = view === "w33-refreshing" || view === "w33-stale" || view === "w33-degraded"
      ? page.locator(".connection-status", { hasText: expected }).first()
      : page.getByText(expected).first();
    await expect(state).toBeVisible();
  }
  await capture(page, testInfo, "ru-presentation-state-matrix");
  assertCleanDiagnostics(diagnostics);
});

test("permission denial and loading keep protected data fail-closed", async ({ page }, testInfo) => {
  let releaseIdentity: (() => void) | undefined;
  const identityGate = new Promise<void>((resolve) => { releaseIdentity = resolve; });
  await page.route("**/api/identity/me", async (route) => { await identityGate; await route.continue(); });
  const navigation = page.goto("/w/northwind-retail/connections");
  await expect(page.getByText("Loading connections")).toBeVisible();
  releaseIdentity?.();
  await navigation;
  await expect(page.getByText("Connection listing is not available in W14")).toBeVisible();
  await page.unroute("**/api/identity/me");

  await useActor(page, "no-permission");
  await page.goto("/w/northwind-retail/connections/new");
  await expect(page.getByRole("alert")).toContainText("Connections are unavailable");
  await expect(page.locator(".connection-form")).toHaveCount(0);
  await capture(page, testInfo, "permission-denied");
  await assertNoOverflow(page);
});

test("keyboard, semantics, 200-percent reflow, and reduced motion remain usable", async ({ page }, testInfo) => {
  const diagnostics = collectDiagnostics(page);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/w/northwind-retail/connections?view=w33-fixture");
  await page.keyboard.press("Tab");
  await expect(page.getByRole("link", { name: "Skip to content" })).toBeFocused();
  const add = page.getByRole("link", { name: "Add connection" });
  await add.focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { level: 1, name: "New connection" })).toBeVisible();
  const submit = page.getByRole("button", { name: "Save and test" });
  await submit.focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("alert")).toBeFocused();

  const semantics = await page.evaluate(() => ({
    positiveTabIndex: document.querySelectorAll('[tabindex]:not([tabindex="0"]):not([tabindex="-1"])').length,
    unlabeledInputs: [...document.querySelectorAll("input,select")].filter((control) => !(control as HTMLInputElement).labels?.length).length,
    unnamedButtons: [...document.querySelectorAll("button")].filter((button) => !(button.textContent?.trim() || button.getAttribute("aria-label"))).length,
  }));
  expect(semantics).toEqual({ positiveTabIndex: 0, unlabeledInputs: 0, unnamedButtons: 0 });
  await page.evaluate(() => { document.body.style.zoom = "2"; });
  await assertNoOverflow(page);
  const motion = await page.evaluate(() => {
    const button = getComputedStyle(document.querySelector(".connections-button") as Element);
    const spinner = getComputedStyle(document.querySelector(".connections-spinner") ?? document.body);
    return { transition: button.transitionDuration, animation: spinner.animationDuration };
  });
  expect(motion).toEqual({ transition: "0s", animation: "0s" });
  await capture(page, testInfo, "keyboard-reflow-reduced-motion");
  assertCleanDiagnostics(diagnostics);
});
