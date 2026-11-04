import {test,expect} from '@playwright/test';
// Functional provider checks allow 60s for real Save/read work. The capture proxy
// must not impose the 10s UI-action deadline; latency acceptance remains C10.

test('published filters affect real values and survive save/reopen; draft undo and reset',async({page,request})=>{
 const scenario=await(await request.get('/fixture/scenario')).json() as {workspace:string};
 // Capture actual upstream bytes before forwarding them unchanged. Chromium CDP
 // intermittently loses Network.getResponseBody for these iframe-hosted requests.
 const bodies:Record<string,any>={};let delayPreview=false,pendingApply=false;
 for(const path of ['/composer/v1/apply','/filters/preview','/composer/v1/versions'])await page.route(`**${path}`,async route=>{
  if(path==='/filters/preview'&&delayPreview){pendingApply=true;await new Promise(resolve=>setTimeout(resolve,300));}
  const upstream=await route.fetch({timeout:60000});bodies[path]=await upstream.json();await route.fulfill({response:upstream});
 });
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>localStorage.setItem('custometry-language','en'));
 await page.goto('/auth/sign-in');await page.getByLabel(/Workspace/).fill(scenario.workspace);await page.getByLabel('Email',{exact:true}).fill('author@example.test');await page.getByLabel('Password',{exact:true}).fill('synthetic-author-password');await page.getByRole('button',{name:'Sign in',exact:true}).click();await page.waitForURL(/\/reports$/);
 let releaseContext!:()=>void;const contextGate=new Promise<void>(resolve=>{releaseContext=resolve;});
 await page.route('**/metric-workspace/v2/datasets/*/context',async route=>{const upstream=await route.fetch({timeout:60000});await contextGate;await route.fulfill({response:upstream});});
 await page.goto(`/w/${scenario.workspace}/reports/new/edit?view=composer`);const frame=page.frameLocator('iframe');
 async function builder(name:string){await frame.getByRole('button',{name:'Add block',exact:true}).last().click();await frame.getByRole('button',{name:'Continue',exact:true}).click();if(name==='Unfiltered'){await expect(frame.getByRole('button',{name:'Continue',exact:true})).toBeDisabled();releaseContext();}await frame.getByRole('button',{name:'Continue',exact:true}).click();await frame.getByLabel('Block type',{exact:true}).selectOption('table');await frame.getByLabel('Block title',{exact:true}).fill(name);}
 await builder('Unfiltered');await frame.getByRole('button',{name:'Add to document',exact:true}).click();
 const unfiltered=frame.getByRole('article',{name:'Unfiltered',exact:true});
 let response=page.waitForResponse(r=>r.url().endsWith('/composer/v1/apply')&&r.request().method()==='POST',{timeout:60000});await unfiltered.getByRole('button',{name:'Apply',exact:true}).click();expect((await response).status()).toBe(200);const before=bodies['/composer/v1/apply'];expect(Number(before.result.totals.net_revenue)).toBeGreaterThan(0);
 await builder('Filtered empty');await frame.locator('.composer-builder .receipt-filter-editor > summary').click();const editor=frame.locator('.composer-builder .receipt-filter-editor');
 await expect(editor.getByText('Mandatory access restrictions:',{exact:false})).toBeVisible();
 await editor.getByLabel('Search fields',{exact:true}).fill('status');await expect(editor.getByRole('button',{name:'Receipt status +',exact:true})).toBeVisible();await editor.getByRole('button',{name:'Receipt status +',exact:true}).click();
 await editor.locator('.receipt-filter-condition').getByLabel('Value',{exact:true}).fill('not-a-real-status');
 response=page.waitForResponse(r=>r.url().endsWith('/filters/preview')&&r.request().method()==='POST',{timeout:60000});await editor.getByRole('button',{name:'Check draft',exact:true}).click();const preview=await response;expect(preview.status()).toBe(200);const counts=bodies['/filters/preview'];expect(counts.matched_count).toBe(0);expect(counts.authorized_count).toBeGreaterThan(0);expect(counts).not.toHaveProperty('matched_ids');
 await editor.getByRole('button',{name:'Clear draft',exact:true}).click();await expect(editor.locator('.receipt-filter-condition').getByLabel('Value',{exact:true})).toHaveCount(0);await editor.getByRole('button',{name:'Undo change',exact:true}).click();await expect(editor.locator('.receipt-filter-condition').getByLabel('Value',{exact:true})).toHaveValue('not-a-real-status');
 await editor.getByRole('button',{name:'Reset to initial',exact:true}).click();await expect(editor.locator('.receipt-filter-condition').getByLabel('Value',{exact:true})).toHaveCount(0);await editor.getByRole('button',{name:'Undo change',exact:true}).click();
 delayPreview=true;
 await editor.getByRole('button',{name:'Apply filter to block',exact:true}).click();
 await expect.poll(()=>pendingApply).toBe(true);await expect(frame.getByRole('button',{name:'Add to document',exact:true})).toBeDisabled();
 await expect(editor.getByText(/Applied to block settings:.*not-a-real-status/)).toBeVisible();delayPreview=false;
 await editor.getByRole('button',{name:'Apply filter to block',exact:true}).focus();await page.keyboard.press('Enter');await expect(editor.getByText(/Applied to block settings:.*not-a-real-status/)).toBeVisible();
 await frame.getByRole('button',{name:'Add to document',exact:true}).click();const filtered=frame.getByRole('article',{name:'Filtered empty',exact:true});
 response=page.waitForResponse(r=>r.url().endsWith('/composer/v1/apply')&&r.request().method()==='POST',{timeout:60000});await filtered.getByRole('button',{name:'Apply',exact:true}).click();const afterResponse=await response;expect(afterResponse.status()).toBe(200);const after=bodies['/composer/v1/apply'];expect(after.result.totals.net_revenue).toBeNull();expect(after.result.request_hash).not.toBe(before.result.request_hash);
 response=page.waitForResponse(r=>r.url().endsWith('/composer/v1/versions')&&r.request().method()==='POST',{timeout:60000});await frame.getByRole('button',{name:'Save report',exact:true}).click();const savedResponse=await response;expect(savedResponse.status()).toBe(200);const saved=bodies['/composer/v1/versions'];expect(saved.definition.definitions.some((d:any)=>d.query.receipt_filter?.expression.values[0].value==='not-a-real-status')).toBe(true);
 await page.waitForURL(/reports\/[0-9a-f-]+\/edit\?view=composer/);await page.reload();await expect(filtered.getByRole('table')).toBeVisible({timeout:60000});await expect(unfiltered.getByRole('table')).toBeVisible({timeout:60000});
 await filtered.getByRole('button',{name:'Edit block',exact:true}).click();await frame.getByRole('button',{name:'Continue',exact:true}).click();await frame.getByRole('button',{name:'Continue',exact:true}).click();await frame.locator('.composer-builder .receipt-filter-editor > summary').click();await expect(editor.getByText(/Applied to block settings:.*not-a-real-status/)).toBeVisible();
 await page.setViewportSize({width:390,height:844});await expect(editor.getByRole('button',{name:'Apply filter to block',exact:true})).toBeVisible();expect(errors).toEqual([]);
});
