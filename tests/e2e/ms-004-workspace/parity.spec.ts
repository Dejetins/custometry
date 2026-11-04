import {test,expect,openInspector,closeInspector} from './observed-test';
import type {Page} from '@playwright/test';
import type {configuredReports as W} from '@custometry/contracts';
import {writeFile} from 'node:fs/promises';
async function login(page:Page,workspace:string,who='reader'){
 await page.addInitScript(()=>localStorage.setItem('custometry-language','en'));await page.goto('/auth/sign-in');
 await page.getByLabel(/Workspace/).fill(workspace);await page.getByLabel('Email',{exact:true}).fill(`${who}@example.test`);await page.getByLabel('Password',{exact:true}).fill(who==='author'?'synthetic-author-password':'synthetic-reader-password');await page.getByRole('button',{name:'Sign in',exact:true}).click();await page.waitForURL(/\/reports$/);
}
test('S05 reader pair persists server comparison reasons after reopen',async({page,request},info)=>{
 await page.addInitScript(()=>{const native=window.fetch;window.fetch=async(...args)=>{const response=await native(...args);if(String(args[0]).endsWith('/apply'))(window as unknown as {capturedApply:Promise<unknown>}).capturedApply=response.clone().json();return response;};});
 const s=await(await request.get('/fixture/scenario')).json() as {workspace:string;report:string};await login(page,s.workspace);await page.goto(`/w/${s.workspace}/reports/${s.report}/edit`);const f=page.frameLocator('iframe');await closeInspector(f);
 await f.locator('.mw-cards .kpi-card').nth(0).getByLabel('Select',{exact:true}).check();await f.locator('.mw-cards .kpi-card').nth(1).getByLabel('Select',{exact:true}).check();
 await f.getByRole('button',{name:'Chart / comparison settings'}).click();await f.getByRole('button',{name:'Compare two cards',exact:true}).click();await closeInspector(f);
 const applied=page.waitForResponse(r=>r.url().endsWith(`/v2/${s.report}/apply`)&&r.request().method()==='POST');await f.getByRole('button',{name:'Apply',exact:true}).click();expect((await applied).status()).toBe(200);const payload=await page.evaluate(()=>(window as unknown as {capturedApply:Promise<W.WorkspaceApplyResponse>}).capturedApply);expect(payload.comparison).not.toBeNull();
 await expect(f.locator('.mw')).toHaveAttribute('aria-busy','false');await f.getByRole('button',{name:'Table',exact:true}).last().click();await expect(f.locator('.mw-table tbody tr')).toHaveCount(payload.comparison!.buckets.length);await expect(f.locator('.mw-table tbody tr').first()).toContainText('Different measurement units');const before=await f.locator('.mw-table tbody').innerText();
 const saved=page.waitForResponse(r=>r.url().endsWith('/saved-views')&&r.request().method()==='POST');await f.getByRole('button',{name:'Save personal view',exact:true}).click();const view=await(await saved).json() as W.SavedViewV1;await expect(f.getByRole('status').filter({hasText:'Saved'})).toBeVisible();await expect(f.locator('.mw')).toHaveAttribute('aria-busy','false',{timeout:60000});
 await request.post(`/fixture/reader-view-only/${s.report}`);await page.reload();await closeInspector(f);await f.getByRole('combobox',{name:'My saved views',exact:true}).selectOption(view.saved_view_id);await expect(f.locator('.mw-table tbody tr')).toHaveCount(payload.comparison!.buckets.length);await page.screenshot({path:info.outputPath('reader-pair.png')});
 await writeFile(info.outputPath('parity.json'),JSON.stringify({comparison:payload.comparison,view,table_before:before,table_after:await f.locator('.mw-table tbody').innerText()},null,2));
 await expect(f.locator('.mw-table tbody')).toHaveText(before,{useInnerText:true});
});

async function chartState(page:Page,showTip=false){
 return page.evaluate(async show=>{
  const doc=document.querySelector('iframe')!.contentDocument!;
  const echarts=(doc.defaultView as unknown as {echarts:typeof import('echarts/core')}).echarts;
  const node=doc.querySelector('.mw-focus .mw-plot')??doc.querySelector('.mw-plot');
  const chart=echarts.getInstanceByDom(node);
  if(show)chart.dispatchAction({type:'showTip',seriesIndex:0,dataIndex:0});
  const o=chart.getOption();
  return {series:o.series.map((s:{name:string;data:(string|null)[];yAxisIndex:number})=>({name:s.name,data:s.data,axis:s.yAxisIndex})),axes:o.yAxis.map((a:{name:string})=>a.name),dates:o.xAxis[0].data};
 },showTip) as Promise<{series:{name:string;data:(string|null)[];axis:number}[];axes:string[];dates:string[]}>;
}
async function tableValues(page:Page){return page.frameLocator('iframe').locator('.mw-table tbody tr').evaluateAll(rows=>rows.map(row=>Array.from(row.querySelectorAll('td[data-value]')).map(td=>td.getAttribute('data-value'))));}
test('S05 reader temporal artifact parity, delta trend and modal keyboard',async({page,request},info)=>{
 // Observe the actual streamed response in the browser; Chromium may discard its CDP body buffer.
 await page.addInitScript(()=>{const native=window.fetch;window.fetch=async(...args)=>{const response=await native(...args);if(String(args[0]).endsWith('/apply'))(window as unknown as {capturedApply:Promise<unknown>}).capturedApply=response.clone().json();return response;};});
 const s=await(await request.get('/fixture/scenario')).json() as {workspace:string;report:string};await login(page,s.workspace);await page.goto(`/w/${s.workspace}/reports/${s.report}/edit`);const f=page.frameLocator('iframe');
 // Narrow inspector opens explicitly; its dock leaves the header usable.
 if(info.project.name==='768'){
  await openInspector(f);await expect(f.getByRole('heading',{name:'Report inspector'})).toBeFocused();
  await page.keyboard.press('Escape');await expect(f.locator('#context-open')).toBeFocused();
 }
 await closeInspector(f);
 const applied=page.waitForResponse(r=>r.url().endsWith(`/v2/${s.report}/apply`)&&r.request().method()==='POST');await f.getByRole('button',{name:'Apply',exact:true}).click();expect((await applied).status()).toBe(200);const payload=await page.evaluate(()=>(window as unknown as {capturedApply:Promise<W.WorkspaceApplyResponse>}).capturedApply);expect(payload.comparison?.mode).toBe('temporal');
 await expect(f.locator('.mw-cards .kpi-value').first()).not.toHaveText('—');await f.getByRole('button',{name:'Table',exact:true}).last().click();await expect(f.locator('.mw-table tbody tr')).toHaveCount(payload.comparison!.buckets.length);
 const expected=payload.comparison!.buckets.map(b=>[b.left??'',b.right??'',b.absolute_delta??'',b.relative_delta_percent??'']);await expect.poll(()=>tableValues(page)).toEqual(expected);
 await f.getByRole('button',{name:'Save personal view',exact:true}).click();await expect(f.getByRole('status').filter({hasText:'Saved'})).toBeVisible();await expect(f.locator('.mw')).toHaveAttribute('aria-busy','false',{timeout:60000});const id=await f.getByRole('combobox',{name:'My saved views',exact:true}).inputValue();
 await request.post(`/fixture/reader-view-only/${s.report}`);await page.reload();await closeInspector(f);await f.getByRole('combobox',{name:'My saved views',exact:true}).selectOption(id);await expect(f.locator('.mw-table tbody tr')).toHaveCount(expected.length);await expect.poll(()=>tableValues(page)).toEqual(expected);
 const computations:string[]=[];page.on('request',r=>{if(r.method()==='POST'&&/\/(apply|results|comparisons)$/.test(new URL(r.url()).pathname))computations.push(r.url());});
 await f.getByRole('button',{name:'Chart',exact:true}).last().click();await expect(f.locator('.mw-plot svg')).toBeVisible();const chart=await chartState(page,true);expect(chart.series.map(s=>s.data)).toEqual([payload.comparison!.buckets.map(b=>b.left),payload.comparison!.buckets.map(b=>b.right)]);expect(chart.series[1].name).toContain('Prior year');expect(chart.axes).toHaveLength(1);
 await expect(f.locator('.mw-plot')).toContainText('Prior year · same dates: 2024-01-01');await expect(f.locator('.mw-plot')).toContainText('Δ '+new Intl.NumberFormat('en',{maximumFractionDigits:2}).format(Number(payload.comparison!.buckets[0].absolute_delta)));await page.screenshot({path:info.outputPath('temporal-tooltip.png')});
 await f.getByRole('button',{name:'Focus',exact:true}).click();const dialog=f.getByRole('dialog',{name:'Focus'});await expect(dialog).toBeFocused();
 const close=dialog.getByRole('button',{name:'Close Focus',exact:true});await expect(close).toBeInViewport({ratio:1});expect(await close.evaluate(el=>{const r=el.getBoundingClientRect();return el.contains(el.ownerDocument.elementFromPoint(r.left+2,r.top+r.height/2));})).toBe(true);expect(await dialog.locator('th,td').evaluateAll(cells=>cells.every(cell=>cell.scrollWidth<=cell.clientWidth+1))).toBe(true);
 for(const key of ['Shift+Tab','Tab','Tab','Shift+Tab']){await page.keyboard.press(key);expect(await dialog.evaluate(el=>el.contains(el.ownerDocument.activeElement))).toBe(true);}
 expect((await chartState(page)).series).toEqual(chart.series);expect(await dialog.locator('tbody tr').evaluateAll(rows=>rows.map(row=>Array.from(row.querySelectorAll('td[data-value]')).map(td=>td.getAttribute('data-value'))))).toEqual(expected);
 await page.screenshot({path:info.outputPath('focus.png')});await page.keyboard.press('Escape');await expect(f.getByRole('button',{name:'Focus',exact:true})).toBeFocused();
 await f.getByRole('button',{name:'Chart / comparison settings'}).click();await f.getByRole('combobox',{name:'Display',exact:true}).selectOption('delta_trend');await closeInspector(f);
 const delta=await chartState(page);expect(delta.series).toHaveLength(1);expect(delta.series[0].data).toEqual(payload.comparison!.buckets.map(b=>b.relative_delta_percent));expect(delta.axes).toEqual(['Δ %']);
 await f.getByRole('button',{name:'Save personal view',exact:true}).click();await expect(f.getByRole('status').filter({hasText:'Saved'})).toBeVisible();await expect(f.locator('.mw')).toHaveAttribute('aria-busy','false',{timeout:60000});expect(computations).toEqual([]);
 await writeFile(info.outputPath('temporal-parity.json'),JSON.stringify({comparison:payload.comparison,expected,chart,delta,no_calculation_requests:computations},null,2));
});

async function api<T>(page:Page,path:string,body?:unknown):Promise<T>{
 return page.evaluate(async({path,body})=>{const headers:Record<string,string>={'Content-Type':'application/json'};if(body!==undefined)headers['X-CSRF-Token']=decodeURIComponent(document.cookie.split('; ').find(p=>p.startsWith('custometry_csrf='))?.split('=')[1]??'');const r=await fetch('/api'+path,{method:body===undefined?'GET':'POST',headers,body:body===undefined?undefined:JSON.stringify(body)});if(!r.ok)throw Error(`API ${r.status} ${path}`);return r.json();},{path,body}) as Promise<T>;
}
test('S05 fiscal multi-workset same/different stores, exact snapshots and owner demonstration',async({page,request},info)=>{
 const s=await(await request.get('/fixture/scenario')).json() as {workspace:string;report:string};await login(page,s.workspace,'author');await page.goto(`/w/${s.workspace}/reports/${s.report}/edit`);const f=page.frameLocator('iframe');await closeInspector(f);
 const base=`/reports/v2/${s.report}`;const original=await api<W.WorkspaceEditorResponse>(page,base);const d=structuredClone((original.definition??original.base_definition)!) as {-readonly [K in keyof W.ConfiguredReportV2]: W.ConfiguredReportV2[K]};const context=await api<{stores:{id:string}[]}>(page,`/analytics/metric-workspace/v2/datasets/${d.semantic_dataset_version_id}/context`);expect(context.stores.length).toBeGreaterThan(1);
 const legacy=await api<unknown>(page,`/reports/${s.report}/snapshots/${original.report.snapshot_id}`);
 // Synthetic company setup is a fixture precondition, never a report action.
 const calendar=await api<{revision:number}>(page,'/semantic/workspace-calendar/v1');
 const configured=await api<{calendar:W.ConfiguredReportV2['calendar_ref']}>(page,'/semantic/workspace-calendar/v1/versions',{expected_revision:calendar.revision,idempotency_key:crypto.randomUUID(),profile:{schema_version:'business-calendar/v1',kind:'month_based',fiscal_year_start_month:4,fiscal_year_start_day:1,year_label:'end_year',timezone:'UTC',week_start:'monday'}});
 d.calendar_ref={version_id:configured.calendar.version_id,content_hash:configured.calendar.content_hash};d.calendar_basis='fiscal';
 const reportCalendarRequests:string[]=[];page.on('request',r=>{if(r.url().includes('/semantic/workspace-calendar/'))reportCalendarRequests.push(r.url());});
 const first=d.worksets[0].cards[0];const repeated={...first,card_id:crypto.randomUUID(),local_store_ids:[context.stores[0].id]};const different={...first,card_id:crypto.randomUUID(),local_store_ids:[context.stores[1].id]};
 const one={...d.worksets[0],name:{ru:'Сравнение магазинов',en:'Store comparison'},cards:[{...first,local_store_ids:[context.stores[0].id]},repeated,different]};
 const two={...one,workset_id:crypto.randomUUID(),name:{ru:'Обзор продаж',en:'Sales overview'},cards:d.worksets[0].cards.map(c=>({...c,card_id:crypto.randomUUID()}))};
 d.worksets=[one,two];d.default_workset_id=one.workset_id;d.title='MS-004 · Store comparison';d.common_context={...d.common_context,ends_on:'2025-11-30'};d.grain='quarter';d.selection={mode:'pair',left_card_id:first.card_id,right_card_id:different.card_id,display:'series'};
 let prepared=await api<W.WorkspaceApplyResponse>(page,base+'/apply',{contract_version:'configured-report/v2',mode:'creator',base_revision:original.report.revision,definition:d,reuse_result_ids:null});
 const ids=prepared.bindings_by_card;expect(ids[0].result).toEqual(ids[1].result);expect(ids[0].result.result_id).not.toEqual(ids[2].result.result_id);expect(new Set(ids.map(b=>b.card_id)).size).toBe(6);
 const saved=await api<W.WorkspaceReportResponse>(page,base+'/versions',{contract_version:'configured-report/v2',definition:d,expected_revision:original.report.revision,expected_saved_view_revision:original.saved_view_revision,idempotency_key:crypto.randomUUID(),configuration_hash:prepared.configuration_hash,result_ids:ids.map(b=>b.result.result_id),chart_specs:prepared.chart_specs});
 await page.reload();await closeInspector(f);await f.getByRole('button',{name:'Table',exact:true}).last().click();await expect(f.locator('.mw-table tbody tr')).toHaveCount(4);expect(await tableValues(page)).toEqual(prepared.comparison!.buckets.map(b=>[b.left??'',b.right??'',b.absolute_delta??'',b.relative_delta_percent??'']));
 await expect(f.locator('#workspace-calendar-settings')).toHaveCount(0);await expect(f.getByRole('button',{name:'Adopt company calendar'})).toHaveCount(0);await expect(f.getByText('Current company calendar',{exact:false})).toHaveCount(0);
 await expect(f.locator('.mw-table tbody tr')).toHaveCount(4);expect(await tableValues(page)).toEqual(prepared.comparison!.buckets.map(b=>[b.left??'',b.right??'',b.absolute_delta??'',b.relative_delta_percent??'']));await expect(f.locator('.mw-table')).toContainText('FY2026');
 const table=await f.locator('.mw-table tbody').innerText();await page.screenshot({path:info.outputPath('fiscal-table.png')});await f.getByRole('button',{name:'Chart',exact:true}).last().click();const chart=await chartState(page,true);expect(chart.axes).toEqual(['Net revenue']);expect(chart.series.map(s=>s.data)).toEqual([prepared.comparison!.buckets.map(b=>b.left),prepared.comparison!.buckets.map(b=>b.right)]);await page.screenshot({path:info.outputPath('fiscal-chart.png')});
 const exact=await api<W.WorkspaceEditorResponse>(page,base);expect(await api<unknown>(page,`/reports/${s.report}/snapshots/${original.report.snapshot_id}`)).toEqual(legacy);expect((await api<W.WorkspaceEditorResponse>(page,base+`/snapshots/${saved.snapshot_id}`)).report).toEqual(saved);
 const compute:string[]=[];page.on('request',r=>{if(r.method()==='POST'&&/\/(apply|results|comparisons)$/.test(new URL(r.url()).pathname))compute.push(r.url());});
 await page.reload();await closeInspector(f);await f.getByRole('button',{name:'Table',exact:true}).last().click();await expect(f.locator('.mw-table tbody')).toHaveText(table,{useInnerText:true});expect((await api<W.WorkspaceEditorResponse>(page,base)).report).toEqual(exact.report);expect(compute).toEqual([]);expect(reportCalendarRequests).toEqual([]);
 await page.setViewportSize({width:400,height:900});await page.screenshot({path:info.outputPath('fiscal-400.png')});await expect(f.getByRole('button',{name:'Apply',exact:true})).toBeInViewport();
 await writeFile(info.outputPath('fiscal-parity.json'),JSON.stringify({comparison:prepared.comparison,chart,card_bindings:ids,old_snapshot_id:original.report.snapshot_id,calendar_before:saved.composition.definition.calendar_ref,calendar_after:prepared.definition!.calendar_ref,table},null,2));
});

test('S05 late production JSON body cannot restore revoked protected state',async({page,request},info)=>{
 const s=await(await request.get('/fixture/scenario')).json() as {workspace:string;report:string};await login(page,s.workspace,'author');await page.goto(`/w/${s.workspace}/reports/${s.report}/edit`);const f=page.frameLocator('iframe');await closeInspector(f);await f.getByRole('button',{name:'Apply',exact:true}).click();await expect(f.getByRole('button',{name:'Save report',exact:true})).toBeEnabled({timeout:60000});
 const saving=page.waitForResponse(r=>r.url().endsWith(`/v2/${s.report}/versions`)&&r.request().method()==='POST');await f.getByRole('button',{name:'Save report',exact:true}).click();expect((await saving).status()).toBe(200);await expect(f.locator('.mw')).toHaveAttribute('aria-busy','false',{timeout:60000});
 await request.post('/fixture/delay-result-body');await page.reload();await expect.poll(async()=> (await(await request.get('/fixture/result-body-state')).json() as {held:boolean}).held,{timeout:60000}).toBe(true);
 const isResult=(r:import('@playwright/test').Request)=>r.method()==='GET'&&(/\/datasets\/[^/]+\/results\//.test(r.url())||r.url().endsWith(`/v2/${s.report}`));const finished=Promise.race([page.waitForEvent('requestfinished',{predicate:isResult,timeout:60000}),page.waitForEvent('requestfailed',{predicate:isResult,timeout:60000})]);
 await page.evaluate(async()=>{const token=decodeURIComponent(document.cookie.split('; ').find(p=>p.startsWith('custometry_csrf='))?.split('=')[1]??'');await fetch('/api/identity/logout',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':token},body:'{}'});});
 await expect(f.locator('.mw-pending')).toBeVisible({timeout:30000});await expect(f.locator('.title-row h1')).toHaveText('');await request.post('/fixture/release-result-body');await finished;await page.evaluate(()=>new Promise<void>(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve()))));await expect(f.locator('.mw-plot svg')).toHaveCount(0);await expect(f.getByRole('alert')).toBeVisible();
 const state=await(await request.get('/fixture/result-body-state')).json() as {held:boolean;timed_out:boolean};expect(state).toMatchObject({held:false,timed_out:false});await page.screenshot({path:info.outputPath('revoked-late-body.png')});await writeFile(info.outputPath('late-body.json'),JSON.stringify({body_was_held:true,logout_cleared_protected_content:true,finished_body_did_not_restore_protected_content:true,state},null,2));
});

test('S05 Reload saved rejects an obsolete actual Apply response',async({page,request},info)=>{
 const s=await(await request.get('/fixture/scenario')).json() as {workspace:string;report:string};await login(page,s.workspace,'author');await page.goto(`/w/${s.workspace}/reports/${s.report}/edit`);const f=page.frameLocator('iframe');await closeInspector(f);
 await f.getByRole('button',{name:'Table',exact:true}).last().click();const original=await f.locator('.mw-table tbody').innerText();
 await f.getByRole('button',{name:/2025-01-01.*Report context/}).click();await f.getByLabel('From',{exact:true}).fill('2025-01-02');await closeInspector(f);
 await request.post('/fixture/delay-apply-body');await f.getByRole('button',{name:'Apply',exact:true}).click();await expect.poll(async()=> (await(await request.get('/fixture/result-body-state')).json() as {held:boolean}).held,{timeout:60000}).toBe(true);
 await f.getByRole('button',{name:'Reload saved',exact:true}).click();await expect(f.getByRole('button',{name:/2025-01-01.*Report context/})).toBeVisible();await expect(f.locator('.mw-table tbody')).toHaveText(original,{useInnerText:true});
 const isApply=(r:import('@playwright/test').Request)=>r.method()==='POST'&&r.url().endsWith(`/v2/${s.report}/apply`);const finished=Promise.race([page.waitForEvent('requestfinished',{predicate:isApply,timeout:60000}),page.waitForEvent('requestfailed',{predicate:isApply,timeout:60000})]);await request.post('/fixture/release-result-body');await finished;
 await expect(f.locator('.mw')).toHaveAttribute('aria-busy','false');await page.evaluate(()=>new Promise<void>(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve()))));
 await expect(f.locator('.mw-table tbody')).toHaveText(original,{useInnerText:true});await expect(f.getByRole('button',{name:/2025-01-01.*Report context/})).toBeVisible();
 const state=await(await request.get('/fixture/result-body-state')).json();expect(state).toMatchObject({held:false,timed_out:false});await page.screenshot({path:info.outputPath('reload-late-body.png')});await writeFile(info.outputPath('reload-late-body.json'),JSON.stringify({actual_apply_body_held:true,reloaded_saved_context_preserved:true,state},null,2));
});
