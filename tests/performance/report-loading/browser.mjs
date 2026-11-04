import {chromium} from '@playwright/test';
import {readFileSync,writeFileSync} from 'node:fs';
import {performance} from 'node:perf_hooks';
const version=process.env.W39_VERSION??'baseline';
const base=process.env.W39_URL??'http://127.0.0.1:41739';
const fixtures=JSON.parse(readFileSync('.runtime/w39/load-fixtures.json','utf8'));
if(fixtures.length!==50)throw Error('FIFTY_DISTINCT_USERS_REQUIRED');
const browser=await chromium.launch({headless:true});
const records=[];const contexts=[];const pages=[];
const out=`.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/${version}-timings.json`;
const pause=ms=>new Promise(r=>setTimeout(r,ms));
try{
 for(const [i,f] of fixtures.entries()){
  const context=await browser.newContext({baseURL:base,viewport:{width:1440,height:900}});
  const login=await context.request.post('/api/identity/login',{data:{workspace_id:f.workspace,email:f.email,password:'synthetic-w39-password',device_label:`W39 ${version} load ${i}`}});
  if(!login.ok())throw Error(`Login ${i}: ${login.status()}`);
  contexts.push(context);const page=await context.newPage();pages.push(page);
  await page.goto('/auth/sign-in');
  await pause(3100); // Honor production rate limits; login is outside open timings.
 }
 console.log('50 authenticated browser contexts ready');
 for(let round=0;round<4;round++){
  await Promise.all(pages.map(async(page,i)=>{
   const f=fixtures[i];await page.evaluate(()=>{history.pushState({},'','/auth/sign-in');dispatchEvent(new PopStateEvent('popstate'));});
   await page.locator('iframe').waitFor({state:'detached'});
   await page.evaluate(()=>performance.clearResourceTimings());
   const start=performance.now();let status='passed';let frameMs=null;let firstGraphMs=null;let allCardsMs=null;
   try{
    await page.evaluate(url=>{history.pushState({},'',url);dispatchEvent(new PopStateEvent('popstate'));},`/w/${f.workspace}/reports/${f.report}/edit`);
    await page.locator('iframe').waitFor({state:'visible',timeout:180000});frameMs=performance.now()-start;
    const frame=page.frameLocator('iframe');
    await frame.locator('.mw-plot svg').first().waitFor({state:'visible',timeout:180000});
    await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));firstGraphMs=performance.now()-start;
    await frame.locator('.mw-cards .kpi-value').filter({hasText:/\d/}).nth(5).waitFor({state:'visible',timeout:180000});allCardsMs=performance.now()-start;
   }catch(error){status=String(error).split('\n')[0];}
   const resources=await page.evaluate(()=>performance.getEntriesByType('resource').filter(r=>r.name.includes('/api/')).map(r=>({path:new URL(r.name).pathname,start:r.startTime,end:r.responseEnd,duration:r.duration,bytes:r.transferSize})));
   records.push({mode:'warm-internal',round,user:i,status,frameMs,firstGraphMs,allCardsMs,resources});
  }));
  writeFileSync(out,JSON.stringify({version,browser:browser.version(),viewport:{width:1440,height:900},concurrency:50,records},null,2));
  console.log(`Warm round ${round+1}/4 complete; failures ${records.filter(r=>r.status!=='passed').length}`);
 }
 if(process.env.W39_SOAK==='1'){
  console.log('Idle soak start');writeFileSync(`.runtime/w39/${version}-soak-start`,new Date().toISOString());
  // The baseline has no automatic renewal. Keep that observed product behavior;
  // do not inject synthetic renewal or conceal failed expiry during idle.
  await pause(30*60*1000);
  const views=await Promise.all(pages.map(p=>p.locator('iframe').count()));
  writeFileSync(`.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/${version}-idle.json`,JSON.stringify({minutes:30,users:50,visibleReportFrames:views.filter(Boolean).length,finishedAt:new Date().toISOString()},null,2));
  console.log('Idle soak complete');
 }
}finally{await browser.close();}
