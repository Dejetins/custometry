/** Final-build idle qualification. No injected refresh, input events or forced GC. */
import {chromium} from '@playwright/test';
import {readFileSync,writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
const root='.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY';
const label='final-idle-'+Date.now();
const base=process.env.W39_URL??'http://127.0.0.1:41746';
const fixture=JSON.parse(readFileSync('.runtime/w39/load-fixtures.json'));
const reference=JSON.parse(readFileSync(root+'/candidate-warm-8w-controlled.json'));
for(const f of reference.sourceFiles){if(createHash('sha256').update(readFileSync(f.path)).digest('hex')!==f.sha256)throw Error('SOURCE_CHANGED: '+f.path);}
for(const f of reference.buildFiles){const response=await fetch(base+'/'+f.path);if(!response.ok||createHash('sha256').update(Buffer.from(await response.arrayBuffer())).digest('hex')!==f.sha256)throw Error('SERVED_BUILD_CHANGED: '+f.path);}
execFileSync(resolve('.venv/bin/python'),['tests/performance/report-loading/sessions.py','candidate',label],{stdio:'ignore'});
const cookies=JSON.parse(readFileSync('.runtime/w39/candidate/sessions.json'));
const browser=await chromium.launch({headless:true});const pages=[];const samples=[];const requests={};const errors=[];
const runtime=JSON.parse(readFileSync('.runtime/w39/container-run.json'));
const pause=ms=>new Promise(r=>setTimeout(r,ms));
const snapshot=()=>JSON.parse(execFileSync(resolve('.venv/bin/python'),['tests/performance/report-loading/idle_snapshot.py',label],{encoding:'utf8'}));
const visible=()=>Promise.all(pages.map(p=>p.evaluate(()=>{const d=document.querySelector('iframe')?.contentDocument;const cards=d?.querySelectorAll('.mw-cards .kpi-value');return Boolean(d?.querySelector('.mw-plot svg'))&&!d?.querySelector('.mw-pending')&&cards?.length===6&&[...cards].every(n=>/\d/.test(n.textContent));})));
async function heap(){const result=[];for(const p of pages){const c=await p.context().newCDPSession(p);await c.send('Performance.enable');const m=await c.send('Performance.getMetrics');await c.detach();const cache=await p.evaluate(()=>performance.getEntriesByName('custometry.report.cache').map(e=>e.detail).at(-1));result.push({metrics:m.metrics.filter(v=>['JSHeapUsedSize','Documents','Nodes','JSEventListeners'].includes(v.name)),cache});}return result;}
try{
 for(let n=0;n<50;n++){const c=await browser.newContext({baseURL:base,viewport:{width:1440,height:900}});await c.addCookies(cookies[n]);const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message.slice(0,200)));pages.push(p);}
 let index=0;await Promise.all(Array.from({length:4},async()=>{while(index<50){const i=index++,f=fixture[i],p=pages[i];await p.goto(`/w/${f.workspace}/reports/${f.report}/edit`);await p.frameLocator('iframe').locator('.mw-plot svg').waitFor({timeout:30000});}}));
 if(!(await visible()).every(Boolean))throw Error('INITIAL_GRAPH_REQUIRED');
 const heapBefore=await heap();
 for(const p of pages)p.on('request',r=>{if(!r.url().includes('/api/'))return;const path=new URL(r.url()).pathname.replace(/[0-9a-f]{8}-[0-9a-f-]{27,}/g,'[id]');const key=r.method()+' '+path;requests[key]=(requests[key]??0)+1;});
 const started=performance.now(),startedAt=new Date().toISOString(),deadline=started+30*60*1000;
 let result={label,base,startedAt,minutes:30,users:50,browser:browser.version(),runtime,sourceFiles:reference.sourceFiles,buildFiles:reference.buildFiles,forcedGc:false,injectedRenewal:false,heapBefore,samples,requests,errors};
 do{
  const sample=snapshot();sample.readyGraphs=(await visible()).filter(Boolean).length;samples.push(sample);
  result={...result,elapsedMs:performance.now()-started};writeFileSync(root+'/final-profile-idle.json',JSON.stringify(result,null,2));
  console.log(`Idle ${(result.elapsedMs/60000).toFixed(1)}m: ${sample.readyGraphs}/50 graphs, activity changes ${sample.cohort_activity_changed}, rotations ${sample.cohort_history}, API RSS ${(sample.api_rss_kib/1024).toFixed(1)} MiB`);
  if(performance.now()>=deadline)break;await pause(Math.min(30000,deadline-performance.now()));
 }while(true);
 for(let n=0;n<40&&!(await visible()).every(Boolean);n++)await pause(250);
 const final=snapshot();final.readyGraphs=(await visible()).filter(Boolean).length;samples.push(final);
 result={...result,finishedAt:new Date().toISOString(),elapsedMs:performance.now()-started,heapAfter:await heap(),completed:true};writeFileSync(root+'/final-profile-idle.json',JSON.stringify(result,null,2));
 if(final.readyGraphs!==50||samples.some(s=>s.cohort_activity_changed!==0||s.cohort_sessions!==50||s.cohort_principals!==50)||errors.length)throw Error('IDLE_QUALIFICATION_FAILED');
}finally{await browser.close();}
