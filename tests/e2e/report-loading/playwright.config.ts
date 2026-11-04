import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'.',testMatch:'*.spec.ts',workers:1,retries:0,timeout:240000,expect:{timeout:60000},reporter:'list',outputDir:'../../../test-results/w39',use:{baseURL:'http://127.0.0.1:41739',viewport:{width:1440,height:900},screenshot:'off',trace:'off'}});
