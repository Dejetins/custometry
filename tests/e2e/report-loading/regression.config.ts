import {defineConfig} from '@playwright/test';
import {resolve} from 'node:path';
const root=resolve(__dirname,'../../..');
export default defineConfig({testDir:'../ms-004-workspace',testMatch:['workspace.spec.ts','reader.spec.ts','parity.spec.ts'],workers:1,retries:0,timeout:240000,expect:{timeout:30000},reporter:'list',outputDir:root+'/test-results/w39-regression',use:{baseURL:'http://127.0.0.1:41741',screenshot:'off',trace:'off'},webServer:[
 {command:"bash -c 'source scripts/activate-toolchain.sh && W39_RUNTIME=.runtime/w39/qa W39_API_PORT=58141 W39_WEB_PORT=41741 uv run --locked python tests/e2e/report-loading/stand.py'",cwd:root,url:'http://127.0.0.1:58141/health/live',reuseExistingServer:false,timeout:240000,gracefulShutdown:{signal:'SIGTERM',timeout:15000}},
 {command:"bash -c 'source scripts/activate-toolchain.sh && W39_API_PORT=58141 W39_WEB_PORT=41741 corepack pnpm --filter @custometry/web exec vite preview --config ../../tests/e2e/report-loading/vite.config.ts'",cwd:root,url:'http://127.0.0.1:41741',reuseExistingServer:false,timeout:60000,gracefulShutdown:{signal:'SIGTERM',timeout:10000}}
],projects:[{name:'1920',use:{viewport:{width:1920,height:1080}}},{name:'768',use:{viewport:{width:768,height:1024}}}]});
