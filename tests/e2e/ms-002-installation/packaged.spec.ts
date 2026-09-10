import { test, expect } from "@playwright/test";
import { resolve } from "node:path";
import { execFileSync } from "node:child_process";
const fault = (mode: string, action: string) => execFileSync(process.env.CUSTOMETRY_PYTHON312!, [resolve(process.cwd(), "../../tests/e2e/ms-002-installation/packaged_fault.py"), mode, action], { env: process.env, stdio: "pipe" });
// Repeat runs must never overwrite receipt-bound stage evidence.
const evidence = resolve(process.cwd(), "../../tests/e2e/ms-002-installation/test-results/packaged-screenshots");

test("packaged trusted HTTPS, real failures, recovery, locales and keyboard", async ({ page, request }, info) => {
  const errors: string[] = [];
  const consoleErrors: string[] = [];
  const httpStatuses: number[] = [];
  let expectedFailure = false;
  page.on("console", message => { if (message.type() === "error" && !expectedFailure) consoleErrors.push(message.text()); });
  page.on("response", response => { if (response.url().endsWith("/api/installation/status")) httpStatuses.push(response.status()); });
  page.on("pageerror", error => errors.push(error.message));
  await page.goto("/");
  await expect(page.getByRole("status")).toHaveText("Installation is ready");
  const first = await request.get("/");
  const second = await request.get("/");
  const policy = first.headers()["content-security-policy"];
  expect(policy).not.toContain("unsafe-inline");
  const nonce = policy.match(/style-src 'self' 'nonce-([a-f0-9]{32})'/)?.[1];
  expect(nonce).toBeTruthy();
  expect(await first.text()).toContain(`window.__webpack_nonce__="${nonce}"`);
  expect(second.headers()["content-security-policy"]).not.toBe(policy);
  const styles = await page.locator("style[data-styled]").evaluateAll(nodes => nodes.map(node => ({ nonce: (node as HTMLStyleElement).nonce, rules: (node as HTMLStyleElement).sheet?.cssRules.length })));
  expect(styles.length).toBeGreaterThan(0);
  expect(styles.every(style => /^[a-f0-9]{32}$/.test(style.nonce) && (style.rules ?? 0) > 0)).toBe(true);

  const response = await request.get("/api/installation/status");
  expect(response.status()).toBe(200);
  expect(response.headers()["cache-control"]).toBe("no-store");
  const dto = await response.json();
  await expect(page.getByText(dto.version, { exact: true })).toBeVisible();
  expect(await page.locator("nav").count()).toBe(0);
  await page.keyboard.press("Tab");
  await expect(page.getByRole("link", { name: "Skip to installation status" })).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("main")).toBeFocused();
  await page.keyboard.press("Tab");
  const retry = page.getByRole("button", { name: "Check again" });
  await expect(retry).toBeFocused();
  expect(await retry.evaluate(el => getComputedStyle(el).outlineStyle)).toBe("solid");
  await page.keyboard.press("Enter");
  await expect(page.getByRole("status")).toHaveText("Installation is ready");
  await expect(retry).toBeFocused();
  await page.screenshot({ path: `${evidence}/${info.project.name}-entry-en.png`, fullPage: true });
  await page.getByLabel("Language").selectOption("ru");
  await expect(page.getByRole("status")).toHaveText("Установка готова");
  await expect(page.locator("html")).toHaveAttribute("lang", "ru");
  await page.screenshot({ path: `${evidence}/${info.project.name}-entry-ru.png`, fullPage: true });
  await page.reload();
  await expect(page.getByRole("status")).toHaveText("Установка готова");
  // CSS zoom exercises doubled layout size and reflow, not device scale/pinch zoom.
  await page.evaluate(() => { document.documentElement.style.zoom = "2"; });
  await expect(page.getByRole("button", { name: "Проверить снова" })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({ path: `${evidence}/${info.project.name}-zoom-ru.png`, fullPage: true });
  await page.evaluate(() => { document.documentElement.style.zoom = ""; });
  await page.getByLabel("Язык").selectOption("en");
  for (const mode of ["database", "schema", "storage", "api"]) {
    try {
      expectedFailure = true;
      fault(mode, "stop");
      if (mode === "storage") await expect.poll(async () => (await request.get("/api/health/live")).status(), { timeout: 20000 }).toBe(200);
      if (mode !== "storage") await retry.click();
      await expect(page.getByRole("status")).toHaveText(mode === "api" ? "Unable to check installation" : "Installation needs attention", { timeout: 15000 });
      await expect(page.getByText("Installation is ready", { exact: true })).toHaveCount(0);
      if (mode !== "api") expect((await request.get("/api/installation/status")).status()).toBe(503);
      if (info.project.name === "web-1440") await page.screenshot({ path: `${evidence}/${mode}-failure.png`, fullPage: true });
    } finally { fault(mode, "start"); }
    await expect.poll(async () => (await request.get("/api/installation/status")).status(), { timeout: 15000 }).toBe(200);
    await retry.click();
    await expect(page.getByRole("status")).toHaveText("Installation is ready");
    expectedFailure = false;
  }
  expect(errors).toEqual([]);
  expect(consoleErrors).toEqual([]);
  expect(httpStatuses).toEqual(expect.arrayContaining([200, 503]));
  expect(httpStatuses.some(status => status === 502 || status === 504)).toBe(true);
  await page.getByRole("link", { name: "Open installation help" }).click();
  await expect(page.getByRole("heading", { name: "First-run status", exact: false })).toBeVisible();
  await page.goBack();
  await expect(page.getByRole("status")).toHaveText("Installation is ready");
});
