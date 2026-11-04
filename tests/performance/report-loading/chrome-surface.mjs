import {chromium} from '@playwright/test';
import {readFileSync,writeFileSync} from 'node:fs';
const root='.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY';
const fixture=JSON.parse(readFileSync('.runtime/w39/load-fixtures.json'))[49];
const browser=await chromium.launch({headless:true});
try{
 const context=await browser.newContext({baseURL:'http://127.0.0.1:41740',viewport:{width:1440,height:900}});
 const login=await context.request.post('/api/identity/login',{data:{workspace_id:fixture.workspace,email:fixture.email,password:'synthetic-w39-password',device_label:'W39 surface comparison'}});
 if(login.status()!==200)throw Error('LOGIN_FAILED');
 const page=await context.newPage();await page.goto(`/w/${fixture.workspace}/reports/${fixture.report}/edit`);
 await page.frameLocator('iframe').locator('.mw-plot svg').waitFor();await page.waitForTimeout(250);
 const before=await page.evaluate(()=>{const w=document.querySelector('iframe').contentWindow;const e=w.document.querySelector('.workspace-chrome');const s=w.getComputedStyle(e);return {backdrop:s.backdropFilter,background:s.backgroundColor,bounds:e.getBoundingClientRect().toJSON()};});
 await page.screenshot({path:root+'/chrome-blur-before.png'});
 await page.frameLocator('iframe').locator('body').evaluate(body=>{const s=body.ownerDocument.createElement('style');s.textContent='body[data-workspace-v2] .workspace-chrome{backdrop-filter:none}';body.append(s);});
 await page.waitForTimeout(250);await page.screenshot({path:root+'/chrome-blur-none.png'});
 writeFileSync(root+'/chrome-surface-comparison.json',JSON.stringify({browser:browser.version(),viewport:{width:1440,height:900},before,mutation:'Temporary browser-only backdrop-filter:none on workspace chrome; no product source change.'},null,2));
}finally{await browser.close();}
