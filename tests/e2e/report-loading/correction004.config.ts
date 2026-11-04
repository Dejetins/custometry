import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'.',testMatch:'owner-correction004.spec.ts',workers:1,retries:0,timeout:120000,expect:{timeout:15000},reporter:'list',use:{baseURL:'http://127.0.0.1:41746',viewport:{width:1480,height:969}},outputDir:'../../../test-results/w39-correction004'});
