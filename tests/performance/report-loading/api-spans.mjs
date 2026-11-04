// Diagnostic direct HTTP decomposition; not report-paint acceptance evidence.
import {readFileSync,writeFileSync} from 'node:fs';
import {spawn,execFileSync} from 'node:child_process';
import {resolve} from 'node:path';
const startedAt=new Date().toISOString();
const workers=8,version='candidate',threads=process.env.W39_THREAD_LIMIT??'40';
const fixtures=JSON.parse(readFileSync('.runtime/w39/load-fixtures.json'));
const server=spawn(resolve('.venv/bin/python'),['scripts/w39-serve.py','--version',version,'--port','58143','--workers',String(workers)],{env:{...process.env,W39_INSTRUMENT:'1',W39_THREAD_LIMIT:threads},stdio:['ignore','ignore','inherit']});
const resources=[];
const sampler=setInterval(()=>{try{const children=execFileSync('pgrep',['-P',String(server.pid)],{encoding:'utf8'}).trim().split(/\s+/).filter(Boolean);resources.push({at:new Date().toISOString(),processes:execFileSync('ps',['-p',[server.pid,...children].join(','),'-o','pid=,ppid=,rss=,time='],{encoding:'utf8'})});}catch{}},1000);
try {
 for(let n=0;n<240;n++){try{if((await fetch('http://127.0.0.1:58143/health/live')).ok)break;}catch{}await new Promise(r=>setTimeout(r,250));}
 execFileSync(resolve('.venv/bin/python'),['tests/performance/report-loading/sessions.py','candidate',`direct-http-${threads}`],{stdio:'ignore'});
 const cookies=JSON.parse(readFileSync('.runtime/w39/candidate/sessions.json'));
 async function read(i){const start=performance.now();const response=await fetch(`http://127.0.0.1:58143/reports/v2/${fixtures[i].report}`,{headers:{...(process.env.W39_PROFILE==='1'&&i===0?{'X-W39-Profile':'1'}:{}),Cookie:cookies[i].map(c=>`${c.name}=${c.value}`).join('; ')}});const headersMs=performance.now()-start;const body=await response.text();const bodyMs=performance.now()-start;return {user:i,status:response.status,headersMs,bodyMs,bytes:Buffer.byteLength(body),worker:response.headers.get('x-w39-worker'),serverTiming:response.headers.get('server-timing')};}
 // Prime imports and worker-local pools outside measurement.
 for(let n=0;n<16;n++)await read(n);
 const rounds=[];for(let round=0;round<3;round++)rounds.push(await Promise.all(fixtures.map((_,i)=>read(i))));
 writeFileSync(`.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/api-spans-${threads}threads.json`,JSON.stringify({startedAt,finishedAt:new Date().toISOString(),workers,threads,gcThreshold:process.env.W39_GC_THRESHOLD??'runtime default',resources,concurrency:50,rounds,scope:'HTTP report metadata only; no browser paint or result follow-up'},null,2));
}finally{clearInterval(sampler);if(server.exitCode===null){server.kill('SIGTERM');await new Promise(r=>server.once('exit',r));}}
