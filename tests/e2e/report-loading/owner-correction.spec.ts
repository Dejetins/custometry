import {test,expect} from '@playwright/test';
import {readFileSync,writeFileSync} from 'node:fs';
const root='.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-001';
const phase=process.env.W39_CORRECTION_PHASE??'before';
test('owner correction geometry and retained chart identity',async({page,context})=>{
 const fixture=JSON.parse(readFileSync('.runtime/w39/load-fixtures.json','utf8'))[0];
 const login=await context.request.post('/api/identity/login',{data:{workspace_id:fixture.workspace,email:fixture.email,password:'synthetic-w39-password',device_label:'W39 isolated correction QA'}});expect(login.status()).toBe(200);
 await page.goto(`/w/${fixture.workspace}/reports/${fixture.report}/edit`);const frame=page.frameLocator('iframe');await expect(frame.locator('.mw-plot svg')).toBeVisible();
 const probe=()=>page.evaluate(()=>{const d=document.querySelector('iframe')!.contentDocument!;const rect=(s:string)=>{const n=d.querySelector(s) as HTMLElement;if(!n)return null;const r=n.getBoundingClientRect(),c=getComputedStyle(n);return {x:r.x,y:r.y,width:r.width,height:r.height,radius:c.borderRadius,font:c.fontSize};};return {chrome:rect('.workspace-chrome'),inspector:rect('.mw-inspector'),cards:rect('.mw-cards'),plot:rect('.mw-plot'),sample:rect('#period-menu-open'),action:rect('.mw-toolbar>button'),gear:rect('.mw-cards .kpi-card>button:last-of-type'),scroll:d.querySelector('.report-scroll')!.scrollTop};});
 const open=await probe();await page.screenshot({path:`${root}/${phase}-2688-open.png`});
 await frame.getByRole('button',{name:'Close inspector',exact:true}).click();
 await page.waitForTimeout(250);const before=await probe();
 await page.evaluate(()=>{const d=document.querySelector('iframe')!.contentDocument!;(window as any).__w39svg=d.querySelector('.mw-plot svg');});
 await frame.locator('.mw-cards .kpi-card>button:first-child').nth(1).click();
 await expect(frame.locator('#workspace-v2 > .mw')).toHaveAttribute('aria-busy','false');await page.waitForTimeout(250);
 const after=await probe();const sameSvg=await page.evaluate(()=>(window as any).__w39svg===document.querySelector('iframe')!.contentDocument!.querySelector('.mw-plot svg'));
 writeFileSync(`${root}/${phase}-geometry.json`,JSON.stringify({open,before,after,sameSvg},null,2));
 if(phase==='after'){expect(after.cards!.y).toBeCloseTo(before.cards!.y,0);expect(after.plot!.y).toBeCloseTo(before.plot!.y,0);expect(after.scroll).toBe(before.scroll);expect(sameSvg).toBe(true);}
 await context.clearCookies();
});

for(const viewport of [{width:2688,height:1575},{width:1480,height:969},{width:768,height:1024},{width:400,height:900}])test(`responsive controls, focus and labels ${viewport.width}`,async({page,context})=>{
 test.skip(phase==='before');await page.setViewportSize(viewport);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 const fixture=JSON.parse(readFileSync('.runtime/w39/load-fixtures.json','utf8'))[1];
 expect((await context.request.post('/api/identity/login',{data:{workspace_id:fixture.workspace,email:fixture.email,password:'synthetic-w39-password',device_label:'W39 correction responsive'}})).status()).toBe(200);
 await page.goto(`/w/${fixture.workspace}/reports/${fixture.report}/edit`);const f=page.frameLocator('iframe');await expect(f.locator('.mw-plot svg')).toBeVisible();
 if(await f.getByRole('button',{name:'Close inspector',exact:true}).isVisible())await f.getByRole('button',{name:'Close inspector',exact:true}).click();
 const audit=()=>page.evaluate(()=>{const d=document.querySelector('iframe')!.contentDocument!;const elements=[...d.querySelectorAll<HTMLElement>('*')].filter(n=>n.getClientRects().length&&getComputedStyle(n).visibility!=='hidden');const text=d.body.innerText+' '+elements.flatMap(n=>['aria-label','title'].map(a=>n.getAttribute(a)??'')).join(' ');const rect=(s:string)=>{const n=d.querySelector(s) as HTMLElement;if(!n)return null;const r=n.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom};};const reference=d.querySelector('#period-menu-open')!;const sample=getComputedStyle(reference);return {tokens:text.match(/\b(?:EUR|UTC)\b/g)??[],chrome:rect('.workspace-chrome'),rail:rect('.sidebar'),plot:rect('.mw-plot'),scroll:d.querySelector('.report-scroll')!.scrollTop,reference:{height:reference.getBoundingClientRect().height,radius:sample.borderRadius,font:sample.fontSize},controls:elements.filter(n=>n.matches('.mw-toolbar button,.mw-inspector button')).map(n=>{const s=getComputedStyle(n);return {label:n.getAttribute('aria-label')??n.innerText,height:n.getBoundingClientRect().height,radius:s.borderRadius,font:s.fontSize};}),inspector:d.querySelector('.mw-inspector')?rect('.mw-inspector'):null};});
 await page.waitForTimeout(250);const closed=await audit();expect(closed.tokens).toEqual([]);for(const b of closed.controls){expect(b.height).toBe(28);expect(b.radius).toBe(closed.reference.radius);expect(b.font).toBe(closed.reference.font);}
 const gear=f.getByRole('button',{name:'Configure card',exact:true}).first();expect(await gear.locator('svg use').getAttribute('href')).toBe('#i-settings');
 await gear.click();await expect(f.locator('.mw-inspector')).toBeVisible();await page.waitForTimeout(250);const open=await audit();expect(open.tokens).toEqual([]);expect(open.rail).toEqual(closed.rail);
 if(viewport.width>1100)expect(open.inspector!.x).toBeGreaterThanOrEqual(open.chrome.right);else expect(open.inspector!.y).toBeGreaterThanOrEqual(open.chrome.bottom);
 for(const b of open.controls){expect(b.height).toBe(28);expect(b.radius).toBe(open.reference.radius);expect(b.font).toBe(open.reference.font);}
 await page.screenshot({path:`${root}/responsive-${viewport.width}-inspector.png`});
 await page.keyboard.press('Escape');await expect(gear).toBeFocused();await expect(f.locator('.mw-inspector')).toHaveCount(0);
 await f.getByRole('button',{name:'Table',exact:true}).last().click();expect((await audit()).tokens).toEqual([]);await f.getByRole('button',{name:'Chart',exact:true}).last().click();
 const focus=f.getByRole('button',{name:'Focus',exact:true});await focus.click();await expect(f.getByRole('dialog',{name:'Focus'})).toBeVisible();expect((await audit()).tokens).toEqual([]);
 expect((await f.locator('.mw-focus .mw-plot').boundingBox())!.height).toBeGreaterThanOrEqual(viewport.height-140);
 await page.screenshot({path:`${root}/responsive-${viewport.width}-focus.png`});
 const focusHeight=(await f.locator('.mw-focus .mw-plot').boundingBox())!.height;await page.setViewportSize({...viewport,height:viewport.height+100});
 await expect.poll(async()=>(await f.locator('.mw-focus .mw-plot').boundingBox())!.height).toBe(focusHeight+100);await page.setViewportSize(viewport);
 await page.keyboard.press('Escape');await expect(focus).toBeFocused();
 await page.evaluate(()=>{document.querySelector('iframe')!.contentDocument!.querySelector('.report-scroll')!.scrollTop=0;});
 await page.screenshot({path:`${root}/responsive-${viewport.width}-report.png`});
 writeFileSync(`${root}/responsive-${viewport.width}.json`,JSON.stringify({viewport,closed,open,errors},null,2));expect(errors).toEqual([]);
});

test('legacy new report no-data surface omits presentation currency/timezone',async({page,context})=>{
 test.skip(phase==='before');const fixture=JSON.parse(readFileSync('.runtime/w39/load-fixtures.json','utf8'))[2];const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 expect((await context.request.post('/api/identity/login',{data:{workspace_id:fixture.workspace,email:fixture.email,password:'synthetic-w39-password',device_label:'W39 correction legacy'}})).status()).toBe(200);
 await page.goto(`/w/${fixture.workspace}/reports/new/edit`);const f=page.frameLocator('iframe');await expect(f.locator('#context-open')).toBeVisible();
 const audit=()=>page.evaluate(()=>{const d=document.querySelector('iframe')!.contentDocument!;return (d.body.innerText+' '+[...d.querySelectorAll<HTMLElement>('[aria-label],[title]')].filter(n=>n.getClientRects().length).map(n=>(n.getAttribute('aria-label')??'')+' '+(n.title??'')).join(' ')).match(/\b(?:EUR|UTC)\b/g)??[];});
 expect(await audit()).toEqual([]);await f.locator('#context-open').click();
 const computed=page.waitForResponse(r=>r.request().method()==='POST'&&r.url().includes('/analytics/sales-reports/v1'));
 await f.locator('#context-apply').click();const response=await computed;
 await page.waitForTimeout(250);expect(await audit()).toEqual([]);
 const state=await f.locator('body').innerText();expect(response.status()).toBe(200);expect(state).toContain('Data unavailable for this source');
 await page.screenshot({path:`${root}/legacy-new.png`});
 writeFileSync(`${root}/legacy.json`,JSON.stringify({url:page.url(),status:response.status(),errors,renderedTokens:await audit(),state},null,2));
 expect(errors).toEqual([]);
});
