/** Isolate shared-browser animation-frame scheduling from API and report code. */
import {chromium} from '@playwright/test';
import {writeFileSync} from 'node:fs';
const browser=await chromium.launch({headless:true});
const records=[];
try{
 const pages=await Promise.all(Array.from({length:50},async()=>{
  const context=await browser.newContext({viewport:{width:1440,height:900}});
  const page=await context.newPage();
  await page.setContent('<body style="margin:0;background:#191a1f"><iframe style="width:100vw;height:100vh;border:0" srcdoc="<body style=background:#191a1f><svg width=800 height=400><path d=\'M0,400L800,0\' stroke=white /></svg></body>"></iframe></body>');
  return page;
 }));
 await pages[0].waitForTimeout(500);
 for(let round=0;round<4;round++){
  const batch=await Promise.all(pages.map((page,user)=>page.evaluate(()=>new Promise(resolve=>{
   const start=performance.now();let first=null;requestAnimationFrame(()=>{first=performance.now()-start;requestAnimationFrame(()=>resolve({first,second:performance.now()-start}));});
  })).then(t=>({round,user,...t}))));records.push(...batch);
 }
 writeFileSync('.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/browser-frame-floor.json',JSON.stringify({browser:browser.version(),headless:true,pages:50,viewport:{width:1440,height:900},purpose:'Static same-size iframe/SVG only, no application or API; scheduling diagnostic, not report acceptance.',records},null,2));
}finally{await browser.close();}
