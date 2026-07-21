import { expect, test, type Page } from "@playwright/test";

interface BrowserEvidence {
  readonly consoleErrors: string[];
  readonly pageErrors: string[];
  readonly failedRequests: string[];
  readonly expectedAborts: string[];
}

function observeBrowser(page: Page): BrowserEvidence {
  const evidence: BrowserEvidence = {
    consoleErrors: [],
    pageErrors: [],
    failedRequests: [],
    expectedAborts: [],
  };
  page.on("console", (message) => {
    if (message.type() === "error") evidence.consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => evidence.pageErrors.push(error.message));
  page.on("requestfailed", (request) => {
    const knownAbortBoundary = /\/api\/(health\/ready|spike\/(workspace-summary|cancellable-summary|events))/.test(
      request.url(),
    );
    const aborted = /aborted|cancelled/i.test(request.failure()?.errorText ?? "");
    if (knownAbortBoundary && aborted) {
      evidence.expectedAborts.push(`${request.method()} ${new URL(request.url()).pathname}`);
    } else {
      evidence.failedRequests.push(
        `${request.method()} ${request.url()}: ${request.failure()?.errorText ?? "unknown"}`,
      );
    }
  });
  return evidence;
}

function expectCleanBrowser(evidence: BrowserEvidence): void {
  expect(evidence.consoleErrors).toEqual([]);
  expect(evidence.pageErrors).toEqual([]);
  expect(evidence.failedRequests).toEqual([]);
}

async function installMockBoundary(page: Page): Promise<void> {
  let revision = 1;
  await page.route("**/api/health/ready", async (route) => {
    await route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({ status: "ready", service: "api", version: "w20-spike" }),
    });
  });
  await page.route("**/api/spike/workspace-summary", async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 15));
    await route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({
        workspace_id: "northwind-retail",
        revision: revision++,
        result_count: 12,
        freshness: "authoritative",
      }),
    });
  });
  await page.route("**/api/spike/cancellable-summary", async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 800));
    try {
      await route.fulfill({
        contentType: "application/json",
        body: JSON.stringify({
          workspace_id: "northwind-retail",
          revision: 999,
          result_count: 12,
          freshness: "authoritative",
        }),
      });
    } catch {
      // The browser aborted this deterministic mock as the assertion requires.
    }
  });
  await page.route("**/api/spike/events", async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 1200));
    await route.fulfill({
      status: 200,
      headers: {
        "cache-control": "no-cache",
        "content-type": "text/event-stream",
      },
      body: [
        "retry: 10",
        "id: 50",
        "event: workspace-snapshot",
        `data: ${JSON.stringify({
          workspace_id: "northwind-retail",
          revision: 50,
          result_count: 13,
          freshness: "authoritative",
        })}`,
        "",
        "",
      ].join("\n"),
    });
  });
}

test.beforeEach(async ({ page }) => {
  await installMockBoundary(page);
});

test("reversible route mount keeps the canonical legacy fallback and browser history", async ({ page }) => {
  const evidence = observeBrowser(page);
  await page.goto("/w/northwind-retail/analytics/sales");
  await expect(page.getByText("Planned surface")).toBeVisible();
  await page.getByTestId("open-architecture-spike").click();
  await expect(page).toHaveURL(/view=linear-spike/);
  await expect(page.getByRole("heading", { name: "Frontend architecture spike" })).toBeVisible();
  await expect(page.getByTestId("server-transport")).toHaveText("rest");
  await expect(page.getByTestId("server-revision")).toHaveText("50");
  await expect(page.getByTestId("server-transport")).toHaveText("sse");

  await page.reload();
  await expect(page.getByRole("heading", { name: "Frontend architecture spike" })).toBeVisible();
  await page.getByTestId("rollback-link").click();
  await expect(page).not.toHaveURL(/view=linear-spike/);
  await expect(page.getByText("Planned surface")).toBeVisible();
  await page.goBack();
  await expect(page).toHaveURL(/view=linear-spike/);
  await expect(page.getByRole("heading", { name: "Frontend architecture spike" })).toBeVisible();
  await page.goForward();
  await expect(page.getByText("Planned surface")).toBeVisible();
  expectCleanBrowser(evidence);
});

test("MobX theme and panel state remain local while Query REST cancellation is observable", async ({ page }) => {
  const evidence = observeBrowser(page);
  await page.goto("/w/northwind-retail/analytics/sales?view=linear-spike");
  await expect(page.getByTestId("server-transport")).toHaveText("rest");
  const navigationCount = await page.evaluate(() => performance.getEntriesByType("navigation").length);

  for (const themeId of ["abyss", "graphite", "frost", "paper"] as const) {
    await page.getByRole("button", { name: themeId }).click();
    await expect(page.getByTestId("theme-id")).toHaveText(themeId);
    await expect(page.locator(`[data-theme="${themeId}"]`)).toBeVisible();
  }
  expect(await page.evaluate(() => performance.getEntriesByType("navigation").length)).toBe(navigationCount);

  const separator = page.getByRole("separator", { name: "Resize spike sidebar" });
  await separator.focus();
  await page.keyboard.press("ArrowRight");
  await expect(page.getByTestId("sidebar-width")).toHaveText("248px");
  await page.keyboard.press("Home");
  await expect(page.getByTestId("sidebar-width")).toHaveText("240px");

  const box = await separator.boundingBox();
  expect(box).not.toBeNull();
  if (box) {
    await page.mouse.move(box.x + box.width / 2, box.y + 40);
    await page.mouse.down();
    await page.mouse.move(box.x + 55, box.y + 40, { steps: 4 });
    await page.mouse.up();
  }
  const resizedWidth = Number((await page.getByTestId("sidebar-width").textContent())?.replace("px", ""));
  expect(resizedWidth).toBeGreaterThanOrEqual(208);
  expect(resizedWidth).toBeLessThanOrEqual(320);
  await page.reload();
  await expect(page.getByTestId("sidebar-width")).toHaveText(`${resizedWidth}px`);
  await expect(page.getByTestId("theme-id")).toHaveText("paper");

  await page.getByRole("button", { name: "Prove REST cancellation" }).click();
  await expect(page.getByTestId("cancel-state")).toHaveText("observed");
  await expect(page.getByTestId("server-revision")).not.toHaveText("999");

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  expect(overflow).toBeLessThanOrEqual(1);
  expectCleanBrowser(evidence);
});

test("refresh preserves the reserved server-state region and SSE replaces only the authoritative snapshot", async ({ page }) => {
  const evidence = observeBrowser(page);
  await page.goto("/w/northwind-retail/analytics/sales?view=linear-spike");
  await expect(page.getByTestId("server-transport")).toHaveText("rest");
  const initialRevision = Number(await page.getByTestId("server-revision").textContent());
  const panel = page.getByRole("region", { name: "TanStack Query server state" });
  const before = await panel.boundingBox();
  const response = page.waitForResponse((candidate) => candidate.url().includes("/api/spike/workspace-summary"));
  await page.getByRole("button", { name: "Refresh authoritative snapshot" }).click();
  await response;
  await expect.poll(async () => Number(await page.getByTestId("server-revision").textContent())).toBeGreaterThan(initialRevision);
  const after = await panel.boundingBox();
  expect(after?.width).toBe(before?.width);
  await expect(page.getByTestId("server-revision")).toHaveText("50");
  await expect(page.getByTestId("server-transport")).toHaveText("sse");
  expectCleanBrowser(evidence);
});
