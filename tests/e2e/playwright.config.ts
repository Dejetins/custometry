import { defineConfig, devices } from "@playwright/test";

const baseURL = process.env.CUSTOMETRY_BASE_URL ?? process.env.BASE_URL;
if (!baseURL) {
  throw new Error("CUSTOMETRY_BASE_URL is required for the Compose browser smoke");
}
const evidenceRoot = process.env.CUSTOMETRY_PLAYWRIGHT_EVIDENCE_ROOT;
const testResults = evidenceRoot ? `${evidenceRoot}/test-results` : "test-results";
const htmlReport = evidenceRoot ? `${evidenceRoot}/playwright-report` : "playwright-report";

export default defineConfig({
  testDir: ".",
  testMatch: "foundation.spec.ts",
  fullyParallel: false,
  forbidOnly: true,
  retries: process.env.CI ? 1 : 0,
  outputDir: testResults,
  reporter: process.env.CI
    ? [["line"], ["html", { outputFolder: htmlReport, open: "never" }]]
    : "list",
  use: {
    baseURL,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "desktop-chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "mobile-chromium", use: { ...devices["Pixel 7"] } },
  ],
});
