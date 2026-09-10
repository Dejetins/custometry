import { defineConfig } from "@playwright/test";
import { resolve } from "node:path";
const root = resolve(process.cwd(), "../..");
export default defineConfig({
  testDir: ".", testMatch: "installation.spec.ts", fullyParallel: false, workers: 1,
  retries: 0, forbidOnly: true, timeout: 60000, reporter: "list",
  outputDir: "test-results/ms-002-installation",
  use: { baseURL: "http://127.0.0.1:41736", screenshot: "only-on-failure" },
  webServer: [
    { command: "bash -lc 'source scripts/activate-toolchain.sh && uv run --locked --package custometry-docs mkdocs build --strict && exec python3 -m http.server 8835 --bind 127.0.0.1 --directory site'", cwd: root, url: "http://127.0.0.1:8835", timeout: 120000, reuseExistingServer: false },
    { command: "bash -lc 'source scripts/activate-toolchain.sh && exec uv run --locked --package custometry-api python tests/e2e/ms-002-installation/real_api_fixture.py'", cwd: root, url: "http://127.0.0.1:8001/health", timeout: 180000, reuseExistingServer: false },
    { command: "pnpm --filter @custometry/web exec vite --config ../../tests/e2e/ms-002-installation/vite.config.ts --host 127.0.0.1 --port 41736 --strictPort", cwd: root, url: "http://127.0.0.1:41736", reuseExistingServer: false },
    { command: "python3 -m http.server 8834 --bind 127.0.0.1 --directory docs/architecture/ui/target-pilot", cwd: root, url: "http://127.0.0.1:8834/ru/source.html", reuseExistingServer: false },
  ],
  projects: [
    { name: "web-768", use: { viewport: { width: 768, height: 1024 } } },
    { name: "web-1024", use: { viewport: { width: 1024, height: 768 } } },
    { name: "web-1440", use: { viewport: { width: 1440, height: 900 } } },
    { name: "web-1920", use: { viewport: { width: 1920, height: 1080 } } },
  ],
});
