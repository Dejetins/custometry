import { defineConfig } from "@playwright/test";
import { resolve } from "node:path";

const repositoryRoot = resolve(process.cwd(), "../..");
const webPort = 41734;
const baseURL = `http://127.0.0.1:${webPort}`;

export default defineConfig({
  testDir: ".",
  testMatch: "web-operator-runs.spec.ts",
  fullyParallel: false,
  forbidOnly: true,
  retries: 0,
  workers: 1,
  outputDir: "test-results",
  reporter: "list",
  use: { baseURL, screenshot: "only-on-failure", trace: "retain-on-failure" },
  webServer: [
    {
      command: "bash -lc 'source scripts/activate-toolchain.sh && exec uv run --locked --package custometry-api python tests/e2e/web-operator-runs/real_execution_fixture.py --port 8000'",
      cwd: repositoryRoot,
      url: "http://127.0.0.1:8000/health/ready",
      reuseExistingServer: false,
      timeout: 180_000,
      stdout: "pipe",
      stderr: "pipe",
    },
    {
      command: `pnpm --filter @custometry/web exec vite --host 127.0.0.1 --port ${webPort} --strictPort`,
      cwd: repositoryRoot,
      url: baseURL,
      reuseExistingServer: false,
      timeout: 120_000,
      stdout: "pipe",
      stderr: "pipe",
    },
  ],
  projects: [
    { name: "web-768", use: { browserName: "chromium", viewport: { width: 768, height: 1024 } } },
    { name: "web-1920", use: { browserName: "chromium", viewport: { width: 1920, height: 1080 } } },
  ],
});
