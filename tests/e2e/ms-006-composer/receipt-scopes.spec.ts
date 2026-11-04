import {test,expect} from '@playwright/test';

test('Receipt hierarchy replaces only allowed field, preserves unaffected result and saved lock',async({page,request},testInfo)=>{
 const scenario=await(await request.get('/fixture/scenario')).json() as {workspace:string};
 const bodies:Record<string,any>={};
 for(const path of ['/composer/v1/apply','/composer/v1/versions'])await page.route(`**${path}`,async route=>{const upstream=await route.fetch();bodies[path]=await upstream.json();await route.fulfill({response:upstream});});
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>localStorage.setItem('custometry-language','en'));
 await page.goto('/auth/sign-in');await page.getByLabel(/Workspace/).fill(scenario.workspace);await page.getByLabel('Email',{exact:true}).fill('author@example.test');await page.getByLabel('Password',{exact:true}).fill('synthetic-author-password');await page.getByRole('button',{name:'Sign in',exact:true}).click();await page.waitForURL(/\/reports$/);
 await page.goto(`/w/${scenario.workspace}/reports/new/edit?view=composer`);const frame=page.frameLocator('iframe');
 for(const name of ['Local receipt','Unaffected receipt']){await frame.getByRole('button',{name:'Add block',exact:true}).last().click();await frame.getByRole('button',{name:'Continue',exact:true}).click();await frame.getByRole('button',{name:'Continue',exact:true}).click();await frame.getByLabel('Block type',{exact:true}).selectOption('table');await frame.getByLabel('Block title',{exact:true}).fill(name);await frame.getByRole('button',{name:'Add to document',exact:true}).click();await expect(frame.getByRole('article',{name,exact:true})).toBeVisible();}
 const first=frame.getByRole('article',{name:'Local receipt',exact:true}),second=frame.getByRole('article',{name:'Unaffected receipt',exact:true});
 const firstId=(await first.getAttribute('data-block-id'))!;
 await frame.locator('summary').filter({hasText:'Filters and analytical context'}).click();
 const scope=frame.getByRole('region',{name:'Receipt scope',exact:true});
 async function editCondition(operator:'eq'|'ne'){
  const editor=scope.locator('.receipt-filter-editor');await editor.locator(':scope > summary').click();
  await editor.getByLabel('Search fields',{exact:true}).fill('status');await editor.getByRole('button',{name:'Receipt status +',exact:true}).click();
  await editor.locator('.receipt-filter-condition').getByLabel('Operator',{exact:true}).selectOption(operator);
  await editor.locator('.receipt-filter-condition').getByLabel('Value',{exact:true}).fill('never-a-receipt-status');
  await editor.getByRole('button',{name:'Apply to scope settings',exact:true}).click();
  await expect(editor.getByText(/Applied to scope settings:.*never-a-receipt-status/)).toBeVisible();
 }
 async function update(){await scope.getByRole('button',{name:'Update Receipt scope',exact:true}).click();await expect(scope.getByText('Receipt scope updated. Apply affected blocks to calculate.',{exact:true})).toBeVisible();}
 async function apply(article:typeof first){const response=page.waitForResponse(r=>r.url().endsWith('/composer/v1/apply')&&r.request().method()==='POST');await article.getByRole('button',{name:'Apply',exact:true}).click();expect((await response).status()).toBe(200);await expect(article.getByRole('table')).toBeVisible();return bodies['/composer/v1/apply'];}
 await editCondition('ne');await scope.getByLabel('Allow child replacement of the same Receipt field',{exact:true}).check();await update();
 const before=await apply(first),unaffected=await apply(second);expect(Number(before.result.totals.net_revenue)).toBeGreaterThan(0);
 await frame.getByLabel('Scope target',{exact:true}).selectOption(firstId);await editCondition('eq');
 const replacement=scope.getByLabel('Replace parent Receipt constraint',{exact:true});await expect(replacement.locator('option')).toHaveCount(2);await replacement.selectOption({index:1});
 await scope.getByLabel('Lock receipt constraint after Save',{exact:true}).check();await update();
 await expect(first.getByRole('table')).toHaveCount(0);await expect(second.getByRole('table')).toBeVisible();
 await frame.getByLabel('Inspect effective block context',{exact:true}).selectOption(firstId);await expect(frame.locator('.composer-effective')).toContainText('Overridden');await expect(frame.locator('.composer-effective')).toContainText('Locked');
 const after=await apply(first);expect(after.result.totals.net_revenue).toBeNull();expect(after.result.request_hash).not.toBe(before.result.request_hash);
 const saving=page.waitForResponse(r=>r.url().endsWith('/composer/v1/versions')&&r.request().method()==='POST');await frame.getByRole('button',{name:'Save report',exact:true}).click();expect((await saving).status()).toBe(200);
 const saved=bodies['/composer/v1/versions'];expect(saved.definition.scopes.schema_version).toBe('composer-scopes/v2');expect(saved.definition.scopes.receipt_filters).toHaveLength(2);expect(saved.results.find((r:any)=>r.block_id!==firstId).result_id).toBe(unaffected.result.result_id);
 await page.waitForURL(/reports\/[0-9a-f-]+\/edit/);await page.reload();await expect(first.getByRole('table')).toBeVisible();await expect(second.getByRole('table')).toBeVisible();
 await frame.locator('summary').filter({hasText:'Filters and analytical context'}).click();await frame.getByLabel('Scope target',{exact:true}).selectOption(firstId);
 await expect(scope.getByRole('button',{name:'Update Receipt scope',exact:true})).toBeDisabled();await expect(scope.getByText('Saved locked constraint; it cannot be removed or weakened.',{exact:true})).toBeVisible();
 const tampered=structuredClone(saved.definition);tampered.scopes.receipt_filters=tampered.scopes.receipt_filters.filter((f:any)=>!f.locked);
 const denial=await page.evaluate(async definition=>{const token=decodeURIComponent(document.cookie.split('; ').find(p=>p.startsWith('custometry_csrf='))?.split('=')[1]??'');const response=await fetch('/api/reports/composer/v1/validate',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':token},body:JSON.stringify(definition)});return {status:response.status,body:await response.json()};},tampered);
 expect(denial.status).toBeGreaterThanOrEqual(400);expect(JSON.stringify(denial.body)).toContain('COMPOSER_SCOPE_LOCKED');
 await page.setViewportSize({width:768,height:1000});await scope.screenshot({path:testInfo.outputPath('receipt-scope-locked.png')});expect(errors).toEqual([]);
});
