import {defineConfig} from '@playwright/test';
import {resolve} from 'node:path';
const root=resolve(__dirname, '../../..')+'/';
export default defineConfig({testDir:'.',testMatch:'report.spec.ts',workers:1,retries:0,forbidOnly:true,timeout:120000,reporter:'list',outputDir:root+'test-results/ms003-pilot-native',use:{actionTimeout:10000,baseURL:'http://127.0.0.1:41734',screenshot:'off',trace:'off'},webServer:[
{command:"bash -lc 'source scripts/activate-toolchain.sh && exec uv run --locked --package custometry-api python tests/e2e/ms-003-report/real_api_fixture.py'",cwd:root,url:'http://127.0.0.1:58105/health',reuseExistingServer:false,gracefulShutdown:{signal:'SIGTERM',timeout:10000},timeout:240000},
{command:"bash -lc 'source scripts/activate-toolchain.sh && exec corepack pnpm --filter @custometry/web exec vite --config ../../tests/e2e/ms-003-report/vite.config.ts'",cwd:root,url:'http://127.0.0.1:41734',reuseExistingServer:false,gracefulShutdown:{signal:'SIGTERM',timeout:10000},timeout:60000},
{command:'python3 -m http.server 8834 --bind 127.0.0.1 --directory docs/architecture/ui/target-pilot',cwd:root,url:'http://127.0.0.1:8834/ru/source.html',reuseExistingServer:false,gracefulShutdown:{signal:'SIGTERM',timeout:10000}}],projects:[{name:'1920',use:{viewport:{width:1920,height:1080}}},{name:'768',use:{viewport:{width:768,height:1024}}}]});
