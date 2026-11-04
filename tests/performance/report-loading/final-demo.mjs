/** UI login and ready report proof on the isolated localhost origin. */
import {chromium} from '@playwright/test';
import {writeFileSync} from 'node:fs';
const root='.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY';
const base='http://localhost:41746';
const workspace='70568e58-2a23-4de1-9cf7-17bb44e8ae8d';
const report='9285c38c-574d-5ce3-a8d1-028e809cc1ff';
const browser=await chromium.launch({headless:true});
try {
 const context=await browser.newContext({viewport:{width:1440,height:900}});
 const page=await context.newPage();const errors=[];const compute=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('request',r=>{if(r.method()==='POST'&&/\/(apply|results)$/.test(new URL(r.url()).pathname))compute.push(new URL(r.url()).pathname);});
 await page.addInitScript(()=>localStorage.setItem('custometry-language','ru'));
 await page.goto(base+'/auth/sign-in');
 await page.getByLabel('Идентификатор рабочего пространства').fill(workspace);
 await page.getByLabel('Электронная почта').fill('author@example.test');
 await page.getByLabel('Пароль',{exact:true}).fill('synthetic-author-password');
 await page.getByRole('button',{name:'Войти',exact:true}).click();
 await page.waitForURL(/\/reports$/);
 await page.goto(`${base}/w/${workspace}/reports/${report}/edit`);
 const frame=page.frameLocator('iframe');
 await frame.locator('.mw-plot svg').first().waitFor({state:'visible',timeout:30000});
 const snapshot=await page.evaluate(()=>{const d=document.querySelector('iframe')?.contentDocument;return {title:d?.querySelector('.title-row h1')?.textContent,cards:d?.querySelectorAll('.mw-cards .kpi-card').length,values:[...(d?.querySelectorAll('.mw-cards .kpi-value')??[])].map(n=>n.textContent),contextCount:d?.querySelectorAll('#report-unit-context').length,pending:Boolean(d?.querySelector('.mw-pending'))};});
 if(errors.length||compute.length||snapshot.pending||snapshot.contextCount!==1||!snapshot.values.every(v=>/\d/.test(v)))throw Error('FINAL_STAND_PROOF_FAILED');
 await page.screenshot({path:root+'/final-demo.png'});
 writeFileSync(root+'/final-stand.json',JSON.stringify({url:page.url(),browser:browser.version(),snapshot,errors,computeRequests:compute,originIsolation:'localhost, separate from owner demonstration on 127.0.0.1',instrumentation:false},null,2));
 console.log('Final normal-runtime UI login and saved graph passed; no compute requests.');
} finally {await browser.close();}
