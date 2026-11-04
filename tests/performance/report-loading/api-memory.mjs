/** Sustained real result reads with independent API RSS; never retains bodies. */
import {readFileSync,writeFileSync} from 'node:fs';
import {spawn,execFileSync} from 'node:child_process';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
const startedAt=new Date().toISOString(),rounds=[];
const fixtures=JSON.parse(readFileSync('.runtime/w39/load-fixtures.json'));
const paths=['apps/api/src/custometry_api/main.py','apps/api/src/custometry_api/runtime_policy.py','apps/api/src/custometry_api/config.py','apps/api/src/custometry_api/database.py','apps/api/src/custometry_api/reports/prepared.py','apps/api/src/custometry_api/reports/workspace_composition.py','apps/api/src/custometry_api/reports/encoding.py','scripts/w39_instrumented.py','scripts/w39-container.py','tests/performance/report-loading/api-memory.mjs'];
const sourceFiles=paths.map(path=>({path,sha256:createHash('sha256').update(readFileSync(path)).digest('hex')}));
const server=spawn(resolve('.venv/bin/python'),['scripts/w39-container.py','--version','candidate','--port','58160','--workers','8'],{detached:true,stdio:['ignore','ignore','inherit'],env:{...process.env,W39_BALANCED:'1'}});
let runtime;
try{
 let ready=false;for(let n=0;n<240;n++){try{if((await Promise.all(Array.from({length:8},(_,i)=>fetch(`http://127.0.0.1:${58160+i}/health/live`).then(r=>r.ok)))).every(Boolean)){ready=true;break;}}catch{}await new Promise(r=>setTimeout(r,250));}if(!ready)throw Error('START_FAILED');
 runtime=JSON.parse(readFileSync('.runtime/w39/container-run.json'));
 execFileSync(resolve('.venv/bin/python'),['tests/performance/report-loading/sessions.py','candidate','sustained-read-memory'],{stdio:'ignore'});
 const cookies=JSON.parse(readFileSync('.runtime/w39/candidate/sessions.json'));
 for(let round=0;round<Number(process.env.W39_MEMORY_ROUNDS??40);round++){
  const requests=await Promise.all(fixtures.map(async(f,i)=>{const start=performance.now();const response=await fetch(`http://127.0.0.1:41746/api/reports/v2/${f.report}`,{headers:{Cookie:cookies[i].map(c=>`${c.name}=${c.value}`).join('; ')}});const bytes=(await response.arrayBuffer()).byteLength;return {user:i,status:response.status,elapsedMs:performance.now()-start,decodedBytes:bytes,serverTiming:response.headers.get('server-timing')};}));
  const processes=execFileSync('docker',['top',runtime.name,'-eo','pid,ppid,rss,time'],{encoding:'utf8'});
  const rssKiB=processes.split('\n').map(s=>s.trim().split(/\s+/)).filter(r=>/^\d+$/.test(r[0])&&r.length>=3).reduce((sum,r)=>sum+Number(r[2]),0);
  rounds.push({round,at:new Date().toISOString(),rssKiB,processes,requests});
  writeFileSync('.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/api-sustained-memory.json',JSON.stringify({startedAt,observedAt:new Date().toISOString(),runtime,sourceFiles,gcThreshold:process.env.W39_GC_THRESHOLD??'default',threadLimit:process.env.W39_THREAD_LIMIT??'default',concurrency:50,forcedCollections:false,scope:'Repeated authorized report reads, no browser; RSS includes all API container processes.',rounds},null,2));
  if(round%10===9)console.log(`${(round+1)*50} reads; API RSS ${(rssKiB/1024).toFixed(1)} MiB`);
 }
}finally{
 if(server.exitCode===null){const exited=new Promise(r=>server.once('exit',r));server.kill('SIGTERM');await exited;}
}
