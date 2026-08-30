import { expect, type Page } from "@playwright/test";

export async function assertSalesAccessibility(page: Page): Promise<void> {
  await expect(page.getByRole("main")).toHaveCount(1);
  await expect(page.getByRole("heading", { level: 1 })).toHaveCount(1);
  await expect(page.getByRole("form")).toHaveCount(1);
  expect(await page.locator('[tabindex]:not([tabindex="0"]):not([tabindex="-1"])').count()).toBe(0);
  const unnamedButtons = await page.getByRole("button").evaluateAll((buttons) =>
    buttons.filter((button) => !(button.getAttribute("aria-label") || button.textContent?.trim())).length,
  );
  expect(unnamedButtons).toBe(0);
  const formControlsWithoutLabel = await page.locator("input, select").evaluateAll((controls) =>
    controls.filter((control) => !control.closest("label") && !control.getAttribute("aria-label")).length,
  );
  expect(formControlsWithoutLabel).toBe(0);
}
