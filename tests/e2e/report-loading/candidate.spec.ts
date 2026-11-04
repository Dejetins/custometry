import {test,expect} from '@playwright/test';
import {readFileSync,writeFileSync} from 'node:fs';
import {spawn} from 'node:child_process';
import {resolve} from 'node:path';
const base=process.env.W39_URL??'http://127.0.0.1:41740';
test('native pending frame, recovery, two tabs and logout invalidation',async({browser})=>{
 const context=await browser.newContext({baseURL:base,viewport:{width:1440,height:900}});
 const fixture=process.env.W39_USE_SCENARIO?await(await context.request.get('/fixture/scenario')).json():JSON.parse(readFileSync('.runtime/w39/load-fixtures.json','utf8'))[49];
 const report=`/w/${fixture.workspace}/reports/${fixture.report}/edit`;
 const login=await context.request.post('/api/identity/login',{data:{workspace_id:fixture.workspace,email:fixture.email??'author@example.test',password:fixture.email?'synthetic-w39-password':'synthetic-author-password',device_label:'W39 browser lifecycle'}});expect(login.status()).toBe(200);
 const page=await context.newPage();const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 let release!:()=>void;const gate=new Promise<void>(r=>release=r);
 await page.route('**/api/reports/v2/*',async route=>{await gate;await route.continue();});
 await page.goto(report);const frame=page.frameLocator('iframe');
 await expect(frame.locator('.mw-pending')).toBeVisible();
 await expect(frame.locator('.title-row h1')).toHaveText('');
 await expect(frame.locator('.kpi-value:visible')).toHaveCount(0);
 await page.screenshot({path:'.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/delayed-native-frame.png'});
 release();await expect(frame.locator('.mw-plot svg').first()).toBeVisible();await page.unroute('**/api/reports/v2/*');
 expect(await frame.locator('#report-unit-context').count()).toBe(0);
 const tab=await context.newPage();await tab.goto(report);await expect(tab.frameLocator('iframe').locator('.mw-plot svg').first()).toBeVisible();
 const unsavedName='W39 unsaved reconnect draft';
 await frame.getByRole('textbox',{name:'Workset name',exact:true}).fill(unsavedName);
 await context.setOffline(true);await expect(frame.locator('.mw-pending')).toBeVisible();await expect(frame.locator('.title-row h1')).toHaveText('');
 await context.setOffline(false);await expect(frame.locator('.mw-plot svg').first()).toBeVisible();
 await expect(frame.getByRole('textbox',{name:'Workset name',exact:true})).toHaveValue(unsavedName);
 const csrf=(await context.cookies()).find(c=>c.name==='custometry_csrf')!.value;
 const started=Date.now();const logout=await context.request.post('/api/identity/logout',{headers:{'X-CSRF-Token':decodeURIComponent(csrf),Origin:base}});expect(logout.status()).toBe(204);
 await expect(frame.locator('.mw-pending')).toBeVisible();await expect(tab.frameLocator('iframe').locator('.mw-pending')).toBeVisible();
 const hiddenMs=Date.now()-started;await expect(frame.locator('.title-row h1')).toHaveText('');
 await page.waitForTimeout(1000);await expect(frame.locator('.mw-plot svg')).toHaveCount(0);
 expect(errors).toEqual([]);writeFileSync('.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/browser-lifecycle.json',JSON.stringify({hiddenMs,tabs:2,errors,delayedFrame:true,offlineRecovery:true},null,2));
 await context.close();
});


test('transactional invalidation reaches a second API process',async({browser})=>{
 test.skip(!process.env.W39_USE_SCENARIO,'requires the task-owned fixture database');
 const worker=spawn(resolve('.venv/bin/python'),['scripts/w39-serve.py','--version','candidate','--runtime','.runtime/w39/qa','--port','58145'],{stdio:['ignore','ignore','pipe']});
 const web=spawn(process.execPath,[resolve('apps/web/node_modules/vite/bin/vite.js'),'--config',resolve('tests/e2e/report-loading/vite.config.ts')],{cwd:resolve('apps/web'),env:{...process.env,W39_WEB_PORT:'41745',W39_API_PORT:'58145'},stdio:'ignore'});
 const observations:number[]=[];
 try{
  await expect.poll(async()=>{try{return(await fetch('http://127.0.0.1:58145/health/live')).status;}catch{return 0;}}).toBe(200);
  await expect.poll(async()=>{try{return(await fetch('http://127.0.0.1:41745')).status;}catch{return 0;}}).toBe(200);
  for(let iteration=0;iteration<10;iteration++){
   const context=await browser.newContext({baseURL:base,viewport:{width:1440,height:900}});
   const fixture=await(await context.request.get('/fixture/scenario')).json();
   const login=await context.request.post('/api/identity/login',{data:{workspace_id:fixture.workspace,email:'author@example.test',password:'synthetic-author-password',device_label:'W39 cross worker'}});expect(login.status()).toBe(200);
   const pages=await Promise.all([0,1].map(async index=>{
    const page=await context.newPage();
    await page.goto(`${index===1?'http://127.0.0.1:41745':base}/w/${fixture.workspace}/reports/${fixture.report}/edit`);
    await expect(page.frameLocator('iframe').locator('.title-row h1')).not.toHaveText('');
    return page;
   }));
   const csrf=(await context.cookies()).find(c=>c.name==='custometry_csrf')!.value;
   const start=Date.now();const response=await context.request.post('/api/identity/logout-all',{headers:{Origin:base,'X-CSRF-Token':decodeURIComponent(csrf)}});expect(response.ok()).toBe(true);
   await Promise.all(pages.map(async p=>{await expect(p.frameLocator('iframe').locator('.title-row h1')).toHaveText('');observations.push(Date.now()-start);}));
   await context.close();
  }
  const sorted=[...observations].sort((a,b)=>a-b);const p95=sorted[Math.ceil(sorted.length*.95)-1];
  writeFileSync('.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/cross-worker-revoke.json',JSON.stringify({apiProcesses:2,sessionCycles:10,tabObservations:20,observations,p95},null,2));
  expect(p95).toBeLessThanOrEqual(1000);
 }finally{web.kill('SIGTERM');worker.kill('SIGTERM');await Promise.all([web,worker].map(child=>new Promise<void>(resolve=>{if(child.exitCode!==null)resolve();else child.once('exit',()=>resolve());})));}
});

test('maximum fifty-card workset uses bounded deduplicated reads',async({browser})=>{
 test.skip(!process.env.W39_USE_SCENARIO,'requires the owned fixture database');
 const context=await browser.newContext({baseURL:base,viewport:{width:1440,height:900}});
 const fixture=await(await context.request.get('/fixture/scenario')).json();
 expect((await context.request.post('/api/identity/login',{data:{workspace_id:fixture.workspace,email:'author@example.test',password:'synthetic-author-password',device_label:'W39 maximum workset'}})).status()).toBe(200);
 const csrf=(await context.cookies()).find(c=>c.name==='custometry_csrf')!.value;
 const headers={Origin:base,'X-CSRF-Token':decodeURIComponent(csrf)};
 const path=`/api/reports/v2/${fixture.report}`;
 const editor=await(await context.request.get(path)).json();const definition=structuredClone(editor.definition);
 const original=definition.worksets[0];const cards=Array.from({length:50},(_,i)=>({...original.cards[i%original.cards.length],card_id:i===0?original.cards[0].card_id:crypto.randomUUID()}));
 definition.worksets=[{...original,cards}];definition.common_context.starts_on='2025-01-01';definition.common_context.ends_on='2025-12-31';definition.selection={mode:'single',card_id:cards[0].card_id,temporal:'previous_year_same_dates',display:'series'};
 const applied=await context.request.post(path+'/apply',{headers,data:{contract_version:'configured-report/v2',mode:'creator',base_revision:editor.report.revision,definition,reuse_result_ids:null}});expect(applied.status()).toBe(200);const prepared=await applied.json();
 const saved=await context.request.post(path+'/versions',{headers,data:{contract_version:'configured-report/v2',definition,expected_revision:editor.report.revision,expected_saved_view_revision:editor.saved_view_revision,idempotency_key:crypto.randomUUID(),configuration_hash:prepared.configuration_hash,result_ids:prepared.bindings_by_card.map(b=>b.result.result_id),chart_specs:prepared.chart_specs}});expect(saved.status()).toBe(200);
 const page=await context.newPage();const reads:string[]=[];const computes:string[]=[];
 page.on('request',r=>{if(r.method()==='GET'&&/\/datasets\/[^/]+\/results\//.test(r.url()))reads.push(r.url());if(r.method()==='POST'&&/\/(apply|results)$/.test(r.url()))computes.push(r.url());});
 await page.goto(`/w/${fixture.workspace}/reports/${fixture.report}/edit`);const frame=page.frameLocator('iframe');
 await expect(frame.locator('.mw-cards .kpi-card')).toHaveCount(50);await expect(frame.locator('.mw-plot svg').first()).toBeVisible();
 await expect(frame.locator('.mw-cards .kpi-value').filter({hasText:/\d/})).toHaveCount(50);
 expect(reads.length).toBe(0);expect(computes).toEqual([]);
 const cache=await page.evaluate(()=>performance.getEntriesByName('custometry.report.cache').map(e=>(e as PerformanceMeasure).detail));
 expect(cache.at(-1).bytes).toBeLessThanOrEqual(16*1024*1024);expect(cache.at(-1).entries).toBeLessThanOrEqual(32);
 writeFileSync('.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/maximum-workset.json',JSON.stringify({cards:50,resultReads:reads.length,delivery:'verified active results in editor response',computeRequests:computes.length,cache},null,2));
 // Fault injection expands the real result transport with valid JSON whitespace.
 // It does not change the stored result or participate in performance timings.
 let expandedBytes=0;
 // Explicitly exercise the retained streaming fallback, not the embedded path.
 await page.route('**/api/reports/v2/*',async route=>{const response=await route.fetch();const payload=await response.json();delete payload.ready_results;await route.fulfill({response,json:payload});});
 await page.route('**/api/analytics/metric-workspace/v2/datasets/*/results/*',async route=>{const response=await route.fetch();const body=(await response.text())+' '.repeat(2*1024*1024);expandedBytes=Buffer.byteLength(body);await route.fulfill({response,body});});
 await page.reload();await expect(frame.getByRole('alert')).toContainText('verified');
 await expect(frame.locator('.mw-cards .kpi-value').filter({hasText:/\d/})).toHaveCount(0);
 await page.unroute('**/api/analytics/metric-workspace/v2/datasets/*/results/*');
 await frame.getByRole('button',{name:'Retry',exact:true}).click();await expect(frame.locator('.mw-cards .kpi-value').filter({hasText:/\d/})).toHaveCount(50);
 writeFileSync('.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/oversized-transport.json',JSON.stringify({expandedBytes,limit:2*1024*1024,rejected:true,retryRecovered:true,method:'real editor response without optional ready_results; real result plus injected JSON whitespace'},null,2));
 await context.close();
});


test('navigation and reconnect release inactive report state',async({browser})=>{
 test.setTimeout(600000);
 const cycles=Number(process.env.W39_NAV_CYCLES??30);expect(Number.isInteger(cycles)&&cycles>=30&&cycles<=1000).toBe(true);
 const context=await browser.newContext({baseURL:base,viewport:{width:1440,height:900}});
 const fixture=await(await context.request.get('/fixture/scenario')).json();
 expect((await context.request.post('/api/identity/login',{data:{workspace_id:fixture.workspace,email:'author@example.test',password:'synthetic-author-password',device_label:'W39 retained heap'}})).status()).toBe(200);
 const page=await context.newPage();const report=`/w/${fixture.workspace}/reports/${fixture.report}/edit`;
 const samples:unknown[]=[];const client=await context.newCDPSession(page);await client.send('Performance.enable');
 await page.goto(report);
 for(let cycle=0;cycle<=cycles;cycle++){
  await expect(page.frameLocator('iframe').locator('.mw-plot svg').first()).toBeVisible();
  if(cycle%5===0){
   await context.setOffline(true);await expect(page.frameLocator('iframe').locator('.title-row h1')).toHaveText('');
   await context.setOffline(false);await expect(page.frameLocator('iframe').locator('.mw-plot svg').first()).toBeVisible();
   await client.send('HeapProfiler.collectGarbage');
   const metrics=(await client.send('Performance.getMetrics')).metrics;
   const cache=await page.evaluate(()=>performance.getEntriesByName('custometry.report.cache').map(e=>(e as PerformanceMeasure).detail).at(-1));
   expect(cache.bytes).toBeLessThanOrEqual(16*1024*1024);expect(cache.entries).toBeLessThanOrEqual(32);
   samples.push({cycle,cache,metrics:metrics.filter(m=>['JSHeapUsedSize','Nodes','Documents','JSEventListeners'].includes(m.name))});
  }
  if(cycle<cycles){
   await page.evaluate(()=>{history.pushState({},'','/auth/sign-in');dispatchEvent(new PopStateEvent('popstate'));});
   await expect(page.locator('iframe')).toHaveCount(0);
   await page.evaluate(url=>{history.pushState({},'',url);dispatchEvent(new PopStateEvent('popstate'));},report);
  }
 }
 writeFileSync('.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/navigation-memory.json',JSON.stringify({cycles,reconnects:Math.floor(cycles/5)+1,forcedGc:true,samples,cards:await page.frameLocator('iframe').locator('.mw-cards .kpi-card').count(),scope:'One fixture report repeatedly mounted in one tab; not total browser RSS'},null,2));
 await client.detach();await context.close();
});
