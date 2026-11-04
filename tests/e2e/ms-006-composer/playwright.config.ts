import {defineConfig} from '@playwright/test';
import {resolve} from 'node:path';
const root=resolve(__dirname,'../../..');
export default defineConfig({testDir:'.',testMatch:'*.spec.ts',workers:1,retries:0,forbidOnly:true,timeout:180000,expect:{timeout:20000},reporter:'list',outputDir:root+'/test-results/ms006-composer',use:{actionTimeout:10000,baseURL:'http://127.0.0.1:41747',screenshot:'off',trace:'off'},webServer:[
 {command:"bash -lc 'source scripts/activate-toolchain.sh && exec uv run --locked --no-sync python tests/e2e/ms-006-composer/real_api_fixture.py'",cwd:root,url:'http://127.0.0.1:58147/health/live',reuseExistingServer:false,timeout:240000,gracefulShutdown:{signal:'SIGTERM',timeout:15000}},
 {command:"bash -lc 'source scripts/activate-toolchain.sh && exec pnpm --filter @custometry/web exec vite --config ../../tests/e2e/ms-006-composer/vite.config.ts'",cwd:root,url:'http://127.0.0.1:41747',reuseExistingServer:false,timeout:60000,gracefulShutdown:{signal:'SIGTERM',timeout:10000}}
],projects:[{name:'desktop',use:{viewport:{width:1440,height:1000}}}]});
