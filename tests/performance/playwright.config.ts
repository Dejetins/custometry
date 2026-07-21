import { defineConfig } from "@playwright/test";

const baseURL = process.env.CUSTOMETRY_SPIKE_BASE_URL ?? "http://127.0.0.1:4175";

export default defineConfig({
  testDir: ".",
  testMatch: "linear-architecture-spike.spec.ts",
  fullyParallel: false,
  forbidOnly: true,
  retries: 0,
  timeout: 120_000,
  outputDir: "test-results/w20-performance",
  reporter: "line",
  use: {
    baseURL,
    browserName: "chromium",
    viewport: { width: 1440, height: 900 },
    screenshot: "off",
    trace: "off",
  },
  webServer: process.env.CUSTOMETRY_SPIKE_BASE_URL
    ? undefined
    : {
        command: "pnpm --filter @custometry/web exec vite --host 127.0.0.1 --port 4175",
        url: baseURL,
        reuseExistingServer: false,
        timeout: 120_000,
      },
});
