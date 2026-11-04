import {test,expect,type Page,type BrowserContext} from '@playwright/test';
import {readFileSync,writeFileSync} from 'node:fs';
const root='.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/owner-correction-002';
const fixtures=JSON.parse(readFileSync('.runtime/w39/load-fixtures.json','utf8'));
async function login(context:BrowserContext,index=3){const f=fixtures[index];expect((await context.request.post('/api/identity/login',{data:{workspace_id:f.workspace,email:f.email,password:'synthetic-w39-password',device_label:'W39 isolated correction002'}})).status()).toBe(200);return f;}
async function geometry(page:Page){return page.evaluate(()=>{const d=document.querySelector('iframe')!.contentDocument!;const rect=(s:string)=>{const n=d.querySelector<HTMLElement>(s);if(!n||getComputedStyle(n).visibility==='hidden'||!n.getClientRects().length)return null;const r=n.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom};};return {rail:rect('.sidebar'),workspace:rect('.workspace'),header:rect('.page-header'),title:rect('.title-row'),tabs:rect('.report-tabs'),chrome:rect('.workspace-chrome'),toggle:rect('#context-open'),left:rect('#nav-context-panel'),right:rect('.mw-inspector')??rect('#context-drawer'),headerParent:d.querySelector('.page-header')!.parentElement!.id};});}
for(const viewport of [{width:2688,height:1575},{width:1480,height:969},{width:768,height:1024},{width:400,height:900}])for(const kind of ['configured','legacy'])test(`${kind} independent docks ${viewport.width}`,async({page,context})=>{
 await page.setViewportSize(viewport);const fixture=await login(context);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(`/w/${fixture.workspace}/reports/${kind==='legacy'?'new':fixture.report}/edit`);const f=page.frameLocator('iframe');const toggle=f.locator('#context-open');await expect(toggle).toBeVisible();
 if(await toggle.getAttribute('aria-expanded')==='true')await toggle.click();await expect(toggle).toHaveAttribute('aria-expanded','false');await page.waitForTimeout(250);
 const closed=await geometry(page);expect(closed.headerParent).toBe('workspace');
 await toggle.click();await expect(toggle).toHaveAttribute('aria-expanded','true');await page.waitForTimeout(250);const right=await geometry(page);expect(right.toggle).toEqual(closed.toggle);expect(right.right!.y).toBeGreaterThanOrEqual(right.header!.bottom);expect(right.rail).toEqual(closed.rail);
 if(viewport.width>1100)expect(right.right!.x).toBeGreaterThanOrEqual(right.chrome!.right);
 await toggle.click();await expect(toggle).toHaveAttribute('aria-expanded','false');
 const data=f.locator('[data-nav-root="system"]');await data.click();await expect(data).toHaveAttribute('aria-expanded','true');await page.waitForTimeout(250);const left=await geometry(page);
 expect(left.rail).toEqual(closed.rail);expect(left.left!.height).toBeLessThan(viewport.height*.8);
 if(viewport.width>640){expect(left.left!.y).toBeCloseTo(left.workspace!.y,0);expect(left.workspace!.x).toBeGreaterThanOrEqual(left.left!.right);}else expect(left.workspace!.y).toBeGreaterThanOrEqual(left.left!.bottom);
 await toggle.click();await expect(toggle).toHaveAttribute('aria-expanded','true');await page.waitForTimeout(250);const both=await geometry(page);expect(both.toggle).toEqual(left.toggle);expect(both.left).toEqual(left.left);expect(both.right!.y).toBeGreaterThanOrEqual(both.header!.bottom);
 if(viewport.width>1100)expect(both.right!.x).toBeGreaterThanOrEqual(both.chrome!.right);
 for(const state of [closed,right,left,both]){expect(state.tabs!.y).toBeGreaterThanOrEqual(state.header!.bottom);expect(state.tabs!.y).toBeGreaterThanOrEqual(state.title!.bottom);expect(state.tabs!.bottom).toBeLessThanOrEqual(state.chrome!.bottom);}
 await page.screenshot({path:`${root}/${kind}-${viewport.width}-both.png`});
 await f.locator('#nav-context-close').focus();await page.keyboard.press('Shift+Tab');expect(await f.locator('#nav-context-panel').evaluate(n=>n.contains(n.ownerDocument.activeElement))).toBe(false);
 await f.locator('[data-nav-root="analytics"]').click();await page.waitForTimeout(200);const switched=await geometry(page);if(viewport.width>640)expect(switched.workspace).toEqual(both.workspace);else {expect(switched.workspace!.x).toBe(both.workspace!.x);expect(switched.workspace!.width).toBe(both.workspace!.width);expect(switched.workspace!.y).toBeGreaterThanOrEqual(switched.left!.bottom);}await expect(f.locator('#nav-context-panel')).toHaveCount(1);
 await f.locator('#nav-context-close').focus();await page.keyboard.press('Escape');await expect(f.locator('[data-nav-root="analytics"]')).toBeFocused();await expect(f.locator('.app-shell')).toHaveAttribute('data-nav-context','closed');
 await toggle.focus();await page.keyboard.press('Enter');await expect(toggle).toHaveAttribute('aria-expanded','false');await expect(toggle).toBeFocused();
 writeFileSync(`${root}/${kind}-${viewport.width}.json`,JSON.stringify({viewport,closed,right,left,both,errors},null,2));expect(errors).toEqual([]);
});

test('Add single repeated rapid, configured sets and explicit copies preserve user data',async({page,context})=>{
 const fixture=await login(context,4);await page.goto(`/w/${fixture.workspace}/reports/${fixture.report}/edit`);const f=page.frameLocator('iframe');await expect(f.locator('.mw-cards .kpi-card')).toHaveCount(6);
 const group=f.getByRole('group',{name:'Worksets',exact:true});const tabs=group.locator('button[aria-pressed]');const original=await tabs.allTextContents();const cards=await f.locator('.mw-cards .kpi-value').allTextContents();const add=f.getByRole('button',{name:'Add workset',exact:true});
 await add.click();await expect(f.locator('.mw-inspector')).toBeVisible();await expect(f.getByLabel('Workset name',{exact:true})).toHaveValue(/New workset/);await expect(tabs).toHaveCount(original.length+1);
 for(let n=0;n<3;n++)await add.click();await add.dblclick();await add.evaluate(button=>{for(let n=0;n<10;n++)(button as HTMLButtonElement).click();});await expect(tabs).toHaveCount(original.length+1);
 await f.getByLabel('Workset name',{exact:true}).fill('Correction002 configured');await add.click();await expect(tabs).toHaveCount(original.length+2);
 await f.getByText('Metric catalog',{exact:true}).click();await f.locator('.mw-inspector details').getByRole('button',{name:'Net revenue',exact:true}).click();await expect(f.locator('.mw-cards .kpi-card')).toHaveCount(1);
 await add.click();await expect(tabs).toHaveCount(original.length+3);await f.getByRole('button',{name:'Copy workset',exact:true}).click();await expect(tabs).toHaveCount(original.length+4);
 const labels=await tabs.allTextContents();expect(new Set(labels).size).toBe(labels.length);expect(labels.slice(0,original.length)).toEqual(original);
 await tabs.first().click();await expect(f.locator('.mw-cards .kpi-card')).toHaveCount(6);expect(await f.locator('.mw-cards .kpi-value').allTextContents()).toEqual(cards);
 const applied=page.waitForResponse(r=>r.url().endsWith(`/v2/${fixture.report}/apply`)&&r.request().method()==='POST');await f.locator('.mw-inspector footer').getByRole('button',{name:'Apply',exact:true}).click();expect((await applied).status()).toBe(200);
 await expect(f.getByRole('button',{name:'Save report',exact:true})).toBeEnabled();await f.getByRole('button',{name:'Save report',exact:true}).click();await expect(f.getByRole('status').filter({hasText:'Saved'})).toBeVisible();await page.reload();await expect(tabs).toHaveCount(labels.length);expect(await tabs.allTextContents()).toEqual(labels);
 writeFileSync(`${root}/workset-invariants.json`,JSON.stringify({fixtureReport:fixture.report,original,labels,repeatedAndRapidAdds:15,duplicatesCreated:0,persistence:'save/reload passed',existingCardsPreserved:true},null,2));
});
