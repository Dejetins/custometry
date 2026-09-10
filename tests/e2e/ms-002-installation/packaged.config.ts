import { defineConfig } from "@playwright/test";
if (!process.env.CUSTOMETRY_PACKAGED_URL?.startsWith("https://") || !process.env.CUSTOMETRY_PACKAGED_ROOT || !process.env.CUSTOMETRY_PYTHON312) throw new Error("Explicit S04 installed HTTPS and disposable target required");
export default defineConfig({
  testDir: ".", testMatch: "packaged.spec.ts", fullyParallel: false, workers: 1,
  retries: 0, forbidOnly: true, timeout: 180000, reporter: "list",
  outputDir: "test-results/ms-002-packaged",
  use: { baseURL: process.env.CUSTOMETRY_PACKAGED_URL, ignoreHTTPSErrors: false, screenshot: "only-on-failure" },
  projects: [
    { name: "web-768", use: { viewport: { width: 768, height: 1024 } } },
    { name: "web-1024", use: { viewport: { width: 1024, height: 768 } } },
    { name: "web-1440", use: { viewport: { width: 1440, height: 900 } } },
    { name: "web-1920", use: { viewport: { width: 1920, height: 1080 } } },
  ],
});
