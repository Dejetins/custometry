import { test, expect } from "@playwright/test";
import { resolve } from "node:path";
// Repeat runs must never overwrite receipt-bound stage evidence.
const evidence = resolve(process.cwd(), "../../tests/e2e/ms-002-installation/test-results/screenshots");

test("real status, recovery, locales, keyboard and pilot comparison", async ({ page, request }, info) => {
  const errors: string[] = [];
  const consoleErrors: string[] = [];
  const httpStatuses: number[] = [];
  let expectedFailure = false;
  page.on("console", message => { if (message.type() === "error" && !expectedFailure) consoleErrors.push(message.text()); });
  page.on("response", response => { if (response.url().endsWith("/api/installation/status")) httpStatuses.push(response.status()); });
  page.on("pageerror", error => errors.push(error.message));
  await page.goto("/");
  await expect(page.getByRole("status")).toHaveText("Installation is ready");
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
      await request.post(`http://127.0.0.1:8001/fault/${mode}-stop`);
      if (mode !== "storage") await retry.click();
      await expect(page.getByRole("status")).toHaveText(mode === "api" ? "Unable to check installation" : "Installation needs attention", { timeout: 15000 });
      await expect(page.getByText("Installation is ready", { exact: true })).toHaveCount(0);
      if (mode !== "api") expect((await request.get("/api/installation/status")).status()).toBe(503);
      if (info.project.name === "web-1440") await page.screenshot({ path: `${evidence}/${mode}-failure.png`, fullPage: true });
    } finally { await request.post(`http://127.0.0.1:8001/fault/${mode}-start`); }
    await expect.poll(async () => (await request.get("/api/installation/status")).status(), { timeout: 15000 }).toBe(200);
    await retry.click();
    await expect(page.getByRole("status")).toHaveText("Installation is ready");
    expectedFailure = false;
  }
  expect(errors).toEqual([]);
  expect(consoleErrors).toEqual([]);
  expect(httpStatuses).toEqual(expect.arrayContaining([200, 503, 500]));
  await page.getByRole("link", { name: "Open installation help" }).click();
  await expect(page.getByRole("heading", { name: "First-run status", exact: false })).toBeVisible();
  await page.goBack();
  await expect(page.getByRole("status")).toHaveText("Installation is ready");
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.evaluate(async () => {
    const path = "/src/i18n.ts";
    const { default: i18n } = await import(path);
    const original = i18n.getResourceBundle("en", "foundation").installation;
    const expand = (value: unknown): unknown => typeof value === "string" ? `[ ${value} — ${value} ]` : Object.fromEntries(Object.entries(value as object).map(([key, item]) => [key, expand(item)]));
    const expanded = expand(original) as Record<string, unknown>;
    expanded.helpHref = original.helpHref;
    i18n.addResourceBundle("en-XA", "foundation", { installation: expanded });
    await i18n.changeLanguage("en-XA");
  });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  await page.screenshot({ path: `${evidence}/${info.project.name}-pseudo.png`, fullPage: true });
  await page.goto("http://127.0.0.1:8834/ru/source.html");
  await page.screenshot({ path: `${evidence}/${info.project.name}-pilot-ru.png`, fullPage: true });
});
