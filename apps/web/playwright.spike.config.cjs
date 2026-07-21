const { resolve } = require("node:path");
const { defineConfig } = require("@playwright/test");

const baseURL = process.env.CUSTOMETRY_SPIKE_BASE_URL ?? "http://127.0.0.1:4174";
const evidenceRoot = process.env.CUSTOMETRY_PLAYWRIGHT_EVIDENCE_ROOT ?? "test-results/w20-browser";

module.exports = defineConfig({
  testDir: resolve(__dirname, "../../tests/e2e"),
  testMatch: "linear-architecture-spike.spec.ts",
  fullyParallel: false,
  forbidOnly: true,
  retries: 0,
  outputDir: resolve(__dirname, evidenceRoot),
  reporter: "line",
  use: {
    baseURL,
    screenshot: "only-on-failure",
    trace: "on",
  },
  webServer: process.env.CUSTOMETRY_SPIKE_BASE_URL
    ? undefined
    : {
        command: "pnpm --filter @custometry/web exec vite --host 127.0.0.1 --port 4174",
        cwd: resolve(__dirname, "../.."),
        url: baseURL,
        reuseExistingServer: false,
        timeout: 120_000,
      },
  projects: [
    { name: "chromium-1440x900", use: { browserName: "chromium", viewport: { width: 1440, height: 900 } } },
    { name: "chromium-1280x800", use: { browserName: "chromium", viewport: { width: 1280, height: 800 } } },
  ],
});
