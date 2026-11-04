import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'.',testMatch:'owner-correction002.spec.ts',workers:1,retries:0,timeout:90000,expect:{timeout:15000},reporter:'list',use:{baseURL:'http://127.0.0.1:41746',viewport:{width:2688,height:1575}},outputDir:'../../../test-results/w39-correction002'});
