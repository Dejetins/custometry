import {defineConfig} from '@playwright/test';
import {resolve} from 'node:path';
const root=resolve(__dirname,'../../..');
export default defineConfig({testDir:'.',testMatch:'*.spec.ts',workers:1,retries:0,forbidOnly:true,timeout:240000,expect:{timeout:30000},reporter:'list',outputDir:root+'/test-results/ms004-workspace',use:{actionTimeout:10000,baseURL:'http://127.0.0.1:41744',screenshot:'off',trace:'off'},webServer:[
 {command:"bash -lc 'source scripts/activate-toolchain.sh && exec uv run --locked --package custometry-api --all-groups python tests/e2e/ms-004-workspace/real_api_fixture.py'",cwd:root,url:'http://127.0.0.1:58144/health/live',reuseExistingServer:false,timeout:240000,gracefulShutdown:{signal:'SIGTERM',timeout:15000}},
 {command:"bash -lc 'source scripts/activate-toolchain.sh && exec corepack pnpm --filter @custometry/web exec vite --config ../../tests/e2e/ms-004-workspace/vite.config.ts'",cwd:root,url:'http://127.0.0.1:41744',reuseExistingServer:false,timeout:60000,gracefulShutdown:{signal:'SIGTERM',timeout:10000}}
],projects:[{name:'1920',use:{viewport:{width:1920,height:1080}}},{name:'768',use:{viewport:{width:768,height:1024}}}]});
