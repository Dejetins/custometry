import {chromium} from '@playwright/test';
import {readFileSync,writeFileSync,readdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {spawn,execFileSync} from 'node:child_process';
import {resolve} from 'node:path';
const version=process.env.W39_VERSION??'candidate';
const mode=process.env.W39_MODE??'warm';
const workers=Number(process.env.W39_WORKERS??1);
const browserCount=Number(process.env.W39_BROWSER_PROCESSES??1);
if(![1,50].includes(browserCount)||(browserCount!==1&&process.env.W39_TRACE==='1'))throw Error('BROWSER_PROFILE_REQUIRED');
const balanced=process.env.W39_BALANCED==='1';
const container=process.env.W39_CONTAINER==='1';
if(balanced&&![8,16].includes(workers))throw Error('BALANCED_WORKER_COUNT_REQUIRED');
const port=balanced?58160:version==='candidate'?58143:58142;
const base=process.env.W39_URL??`http://127.0.0.1:${version==='candidate'?41743:41742}`;
const runtime=`.runtime/w39/${version==='candidate'?'candidate/':''}`;
const fixtures=JSON.parse(readFileSync('.runtime/w39/load-fixtures.json'));
const buildRoot=version==='baseline'?'.runtime/w39/baseline/apps/web/dist':'apps/web/dist';
function files(dir){return readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(`${dir}/${e.name}`):[`${dir}/${e.name}`]);}
const buildFiles=files(buildRoot).sort().map(path=>({path:path.slice(buildRoot.length+1),sha256:createHash('sha256').update(readFileSync(path)).digest('hex')}));
const sourceRoot=version==='baseline'?'.runtime/w39/baseline':'.';
const sourceFiles=['apps/api/src','apps/web/src','packages/identity_access','packages/presentation','packages/contracts','packages/analytics_core','packages/artifacts','packages/semantic_model'].flatMap(dir=>files(`${sourceRoot}/${dir}`)).filter(path=>/\.(py|ts|tsx|json)$/.test(path)).sort().map(path=>({path:path.slice(sourceRoot.length+1),sha256:createHash('sha256').update(readFileSync(path)).digest('hex')}));

const harnessFiles=[...files('tests/performance/report-loading'),...files('tests/e2e/report-loading').filter(p=>p.endsWith('.ts')),...readdirSync('scripts').filter(p=>p.startsWith('w39')).map(p=>'scripts/'+p)].filter(p=>!p.includes('__pycache__')&&!p.endsWith('.pyc')).sort().map(path=>({path,sha256:createHash('sha256').update(readFileSync(path)).digest('hex')}));

const records=[];const resources=[];const shutdowns=[];let api=null;let browser=null;let browsers=[];const clientResources=[];
const sampler=setInterval(()=>{if(!api)return;try{let processes;if(container){const run=JSON.parse(readFileSync('.runtime/w39/container-run.json'));processes=execFileSync('docker',['top',run.name,'-eo','pid,ppid,rss,time'],{encoding:'utf8'});}else{const children=execFileSync('pgrep',['-P',String(api.pid)],{encoding:'utf8'}).trim().split(/\s+/).filter(Boolean);processes=execFileSync('ps',['-p',[api.pid,...children].join(','),'-o','pid=,ppid=,rss=,time='],{encoding:'utf8'});}resources.push({at:new Date().toISOString(),runtime:container?'container':'host',processes});if(resources.length>256)resources.shift();}catch{}},5000);
const pause=ms=>new Promise(r=>setTimeout(r,ms));
async function start(){
 api=spawn(resolve('.venv/bin/python'),balanced&&!container?['scripts/w39-balanced.py','--version',version,'--workers',String(workers)]:[container?'scripts/w39-container.py':'scripts/w39-serve.py','--version',version,'--port',String(port),'--workers',String(workers)],{detached:true,stdio:['ignore','ignore','inherit']});
 for(let i=0;i<240;i++){try{if((await Promise.all(Array.from({length:balanced?workers:1},(_,n)=>fetch(`http://127.0.0.1:${port+n}/health/live`).then(r=>r.ok)))).every(Boolean))return;}catch{}await pause(250);}
 throw Error('API_START_FAILED');
}
async function closeBrowsers(){await Promise.all(browsers.map(b=>b.close()));browsers=[];browser=null;}
async function stop(){
 if(browsers.length)await closeBrowsers();
 if(api){const child=api;api=null;if(child.exitCode===null){
  let timer;const exited=new Promise(resolve=>child.once('exit',()=>resolve(true)));
  child.kill('SIGTERM');const graceful=await Promise.race([exited,new Promise(resolve=>{timer=setTimeout(()=>resolve(false),5000);})]);clearTimeout(timer);
  if(!graceful){try{process.kill(-child.pid,'SIGKILL');}catch{}await exited;}
  shutdowns.push({at:new Date().toISOString(),graceful,budgetMs:5000});
 }}
}

try{
 for(let round=0;round<Number(process.env.W39_ROUNDS??4);round++){
  if(!api)await start();
  execFileSync(resolve('.venv/bin/python'),['tests/performance/report-loading/sessions.py',version,`${version}-${mode}-${workers}w-${round}`],{stdio:['ignore','ignore','inherit']});
  const cookies=JSON.parse(readFileSync(runtime+'sessions.json'));
  for(let n=0;n<browserCount;n+=4)browsers.push(...await Promise.all(Array.from({length:Math.min(4,browserCount-n)},()=>chromium.launch({headless:true,...(process.env.W39_BROWSER_CHANNEL?{channel:process.env.W39_BROWSER_CHANNEL}:{})}))));
  browser=browsers[0];
  const pages=await Promise.all(fixtures.map(async(f,i)=>{
   const context=await browsers[i%browsers.length].newContext({baseURL:base,viewport:{width:1440,height:900}});await context.addCookies(cookies[i]);
   await context.addInitScript(limit=>{window.__w39limit=limit;},Number(process.env.W39_TIMEOUT_MS??240000));
   await context.addInitScript(()=>{
    const parse=JSON.parse;window.__w39parse=[];
    JSON.parse=function(text,reviver){const start=performance.now();try{return parse(text,reviver);}finally{
     if(typeof text==='string'&&text.length>10000){window.__w39parse.push({start,duration:performance.now()-start,characters:text.length});if(window.__w39parse.length>64)window.__w39parse.shift();}
    }};
   });
   const page=await context.newPage();
   return page;
  }));
  if(mode==='warm'){
   // Warm assets/data outside timing at four users, identically for both versions.
   // The measured navigation below still dispatches all 50 users together.
   let nextPrime=0;
   await Promise.all(Array.from({length:4},async()=>{while(nextPrime<pages.length){
    const i=nextPrime++;const page=pages[i];const f=fixtures[i];
    await page.goto(`/w/${f.workspace}/reports/${f.report}/edit`);
    await page.frameLocator('iframe').locator('.mw-plot svg').first().waitFor({timeout:240000});
    await page.evaluate(()=>{history.pushState({},'','/auth/sign-in');dispatchEvent(new PopStateEvent('popstate'));});
    await page.locator('iframe').waitFor({state:'detached'});
   }}));
  }
  // Real rotation gives all users valid tokens immediately before the timed batch.
  let nextRefresh=0;await Promise.all(Array.from({length:4},async()=>{while(nextRefresh<pages.length){const p=pages[nextRefresh++];const token=(await p.context().cookies()).find(c=>c.name==='custometry_csrf').value;const r=await p.context().request.post('/api/identity/refresh',{headers:{Origin:base,'X-CSRF-Token':decodeURIComponent(token)}});if(r.status()!==200)throw Error('PRE_BATCH_REFRESH_FAILED');}}));
  const trace=process.env.W39_TRACE==='1'?await browser.newBrowserCDPSession():null;
  if(trace)await trace.send('Tracing.start',{categories:'devtools.timeline,blink.user_timing,disabled-by-default-devtools.timeline.frame',transferMode:'ReturnAsStream'});
  const measure=(url)=>{
   const start=performance.now();performance.clearResourceTimings();window.__w39parse=[];
   const events=[];const tasks=[];
   try{new PerformanceObserver(list=>events.push(...list.getEntries().map(e=>({name:e.name,duration:e.duration,interactionId:e.interactionId})))).observe({type:'event',durationThreshold:16});new PerformanceObserver(list=>tasks.push(...list.getEntries().map(e=>({start:e.startTime,duration:e.duration})))).observe({type:'longtask'});}catch{}
   let frameMs=null;let graphMs=null;let cardsMs=null;let graphSeen=0;
   window.__w39=new Promise(resolve=>{
    const tick=()=>{
     const doc=document.querySelector('iframe')?.contentDocument;
     if(frameMs===null&&doc?.querySelector('.mw')&&!doc.querySelector('#initial-paint-guard'))frameMs=performance.now()-start;
     if(doc?.querySelector('.mw-plot svg')){if(++graphSeen>=2&&graphMs===null)graphMs=performance.now()-start;}else graphSeen=0;
     const cards=doc?.querySelectorAll('.mw-cards .kpi-value');
     if(cards&&cards.length===6&&[...cards].every(c=>/\d/.test(c.textContent)))cardsMs??=performance.now()-start;
     if((graphMs!==null&&cardsMs!==null)||performance.now()-start>window.__w39limit){resolve({startedAt:new Date(performance.timeOrigin+start).toISOString(),frameMs,firstGraphMs:graphMs,allCardsMs:cardsMs,events,tasks,parse:window.__w39parse,chrome:performance.getEntriesByName('custometry.report.chrome').map(e=>({start:e.startTime-start,duration:e.duration})),plot:performance.getEntriesByName('custometry.report.plot').map(e=>({start:e.startTime-start,duration:e.duration})),resources:performance.getEntriesByType('resource').filter(r=>r.name.includes('/api/')).map(r=>({path:new URL(r.name).pathname,start:r.startTime-start,end:r.responseEnd-start,duration:r.duration,requestStart:r.requestStart-start,responseStart:r.responseStart-start,bytes:r.transferSize,serverTiming:r.serverTiming.map(s=>({name:s.name,duration:s.duration,description:s.description}))})),status:graphMs!==null&&cardsMs!==null?'passed':'timeout'});return;}
     requestAnimationFrame(tick);
    };requestAnimationFrame(tick);
   });
   if(url){history.pushState({},'',url);dispatchEvent(new PopStateEvent('popstate'));}
  };
  await Promise.all(pages.map(async(p,i)=>{
   try{const f=fixtures[i];const url=`/w/${f.workspace}/reports/${f.report}/edit`;
   if(mode==='cold'){await p.addInitScript(measure);await p.goto(url);}else{await p.evaluate(measure,url);}
   const result=await p.evaluate(()=>window.__w39);
   records.push({...result,round,user:i});
   }catch(error){records.push({round,user:i,status:String(error).split('\n')[0]});}
  }));
  if(trace){const completed=new Promise(resolve=>trace.once('Tracing.tracingComplete',resolve));await trace.send('Tracing.end');const {stream}=await completed;let output='';while(true){const chunk=await trace.send('IO.read',{handle:stream});output+=chunk.data;if(chunk.eof)break;}await trace.send('IO.close',{handle:stream});writeFileSync('.runtime/w39/render-trace.json',output);await trace.detach();}
  const clientPids=[];for(const instance of browsers){const session=await instance.newBrowserCDPSession();const info=await session.send('SystemInfo.getProcessInfo');clientPids.push(...info.processInfo.map(p=>p.id));await session.detach();}clientResources.push({round,at:new Date().toISOString(),processes:execFileSync('ps',['-p',[...new Set(clientPids)].join(','),'-o','pid=,ppid=,rss=,time='],{encoding:'utf8'})});
  // Resource observation must not attach CDP/evaluate while peer opens are timed.
  for(let i=0;i<pages.length;i++){const p=pages[i],record=records.find(r=>r.round===round&&r.user===i);if(record?.status!=='passed')continue;const cdp=await p.context().newCDPSession(p);await cdp.send('Performance.enable');const metrics=await cdp.send('Performance.getMetrics');await cdp.detach();record.cache=await p.evaluate(()=>performance.getEntriesByName('custometry.report.cache').map(e=>e.detail));record.heap=metrics.metrics.filter(m=>['JSHeapUsedSize','JSHeapTotalSize','Nodes','Documents'].includes(m.name));}
  await Promise.all(pages.map(async(p,i)=>{const record=records.find(r=>r.round===round&&r.user===i);if(record?.status!=='passed')return;try{
   // Trusted local representation changes exercise real browser event latency.
   await p.evaluate(()=>{const w=document.querySelector('iframe').contentWindow;w.__w39events=[];new w.PerformanceObserver(list=>w.__w39events.push(...list.getEntries().filter(e=>e.interactionId&&e.startTime>=(w.__w39cutoff??0)).map(e=>({name:e.name,duration:e.duration,interactionId:e.interactionId})))).observe({type:'event',durationThreshold:16});});
   const frame=p.frameLocator('iframe');
   await frame.getByRole('button',{name:'Close inspector',exact:true}).click();
   await frame.getByRole('button',{name:'Table',exact:true}).last().click();
   await frame.getByRole('button',{name:'Chart',exact:true}).last().click();
   await p.waitForTimeout(100);
   const interactions=await p.evaluate(()=>document.querySelector('iframe').contentWindow.__w39events);
   record.interactions=interactions;
  }catch(error){record.interactionError=String(error).split('\n')[0];}}));
  // Representative foreground interaction: the other 49 loaded tabs remain
  // idle. Preserve the concurrent stress observations above separately.
  for(let i=0;i<pages.length;i++){
   const p=pages[i],record=records.find(r=>r.round===round&&r.user===i);
   if(record?.status!=='passed')continue;
   try{
    await p.bringToFront();
    await p.evaluate(()=>{const w=document.querySelector('iframe').contentWindow;w.__w39events=[];w.__w39cutoff=w.performance.now();});
    const frame=p.frameLocator('iframe');
    await frame.getByRole('button',{name:'Table',exact:true}).last().click();
    await p.waitForTimeout(100);
    await frame.getByRole('button',{name:'Chart',exact:true}).last().click();
    await p.waitForTimeout(100);
    record.foregroundInteractions=await p.evaluate(()=>document.querySelector('iframe').contentWindow.__w39events);
    record.foregroundEventThresholdMs=16;
   }catch(error){record.foregroundInteractionError=String(error).split('\n')[0];}
  }
  writeFileSync(`.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/${version}-${mode}-${workers}w-controlled.json`,JSON.stringify({version,mode,workers,apiRuntime:container?JSON.parse(readFileSync('.runtime/w39/container-run.json')):{kind:'native'},diagnostics:{browserProcesses:browserCount,browserChannel:process.env.W39_BROWSER_CHANNEL??'default-headless-shell',tracing:process.env.W39_TRACE==='1',balanced,container,enabled:process.env.W39_INSTRUMENT==='1',gcThreshold:process.env.W39_GC_THRESHOLD??'default',threadLimit:process.env.W39_THREAD_LIMIT??'default',threadSwitch:process.env.W39_THREAD_SWITCH_SECONDS??'default',poolSize:process.env.W39_POOL_SIZE??'default'},buildFiles,sourceFiles,harnessFiles,concurrency:50,preconditionConcurrency:4,refreshConcurrency:4,timeoutMs:Number(process.env.W39_TIMEOUT_MS??240000),browser:browser.version(),osFilesystemCache:'not flushed',shutdowns,resources,clientResources,records},null,2));
  console.log(`${version} ${mode} ${workers} workers: ${records.length} measured opens, ${records.filter(r=>r.status!=='passed').length} failures`);
  await closeBrowsers();if(mode==='cold')await stop();
  const output=`.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/${version}-${mode}-${workers}w-controlled.json`;const saved=JSON.parse(readFileSync(output));saved.shutdowns=shutdowns;writeFileSync(output,JSON.stringify(saved,null,2));
 }
}finally{clearInterval(sampler);await stop();if(records.length){const output=`.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/${version}-${mode}-${workers}w-controlled.json`;const saved=JSON.parse(readFileSync(output));saved.shutdowns=shutdowns;writeFileSync(output,JSON.stringify(saved,null,2));}}
