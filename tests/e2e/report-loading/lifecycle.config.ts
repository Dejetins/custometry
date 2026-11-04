import {defineConfig} from '@playwright/test';
import regression from './regression.config';
export default defineConfig({...regression,testDir:'.',testMatch:'candidate.spec.ts',projects:[{name:'1440',use:{viewport:{width:1440,height:900}}}],outputDir:'../../../test-results/w39-lifecycle'});
