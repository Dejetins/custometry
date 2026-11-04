import {test,expect} from '@playwright/test';

test('C04 inherited scopes, local override, immutable pair and saved inspector',async({page,request},testInfo)=>{
 const scenario=await(await request.get('/fixture/scenario')).json() as {workspace:string};
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));let applies=0,compares=0;
 page.on('request',r=>{if(r.url().endsWith('/composer/v1/apply'))applies++;if(r.url().endsWith('/composer/v1/compare'))compares++;});
 await page.addInitScript(()=>{if(!localStorage.getItem('custometry-language'))localStorage.setItem('custometry-language','en');});
 await page.goto('/auth/sign-in');await page.getByLabel(/Workspace/).fill(scenario.workspace);await page.getByLabel('Email',{exact:true}).fill('author@example.test');await page.getByLabel('Password',{exact:true}).fill('synthetic-author-password');await page.getByRole('button',{name:'Sign in',exact:true}).click();await page.waitForURL(/\/reports$/);
 await page.goto(`/w/${scenario.workspace}/reports/new/edit?view=composer`);
 const frame=page.frameLocator('iframe');
 for(const name of ['First scope','Second scope']){await frame.getByRole('button',{name:'Add block',exact:true}).last().click();await frame.getByRole('button',{name:'Continue',exact:true}).click();await frame.getByRole('button',{name:'Continue',exact:true}).click();await frame.getByLabel('Block type',{exact:true}).selectOption('table');await frame.getByLabel('Block title',{exact:true}).fill(name);await frame.getByRole('button',{name:'Add to document',exact:true}).click();await expect(frame.getByRole('article',{name,exact:true})).toBeVisible();}
 const first=frame.getByRole('article',{name:'First scope',exact:true}),second=frame.getByRole('article',{name:'Second scope',exact:true});
 const left=(await first.getAttribute('data-block-id'))!,right=(await second.getAttribute('data-block-id'))!;
 await frame.locator('summary').filter({hasText:'Filters and analytical context'}).click();
 await frame.getByLabel('Scope grain',{exact:true}).selectOption('month');
 const stores=frame.getByRole('group',{name:'Scope stores',exact:true});await stores.getByLabel('All permitted stores',{exact:true}).uncheck();
 const options=stores.locator('.mw-store-list input');await expect(options).not.toHaveCount(0);for(let i=1;i<await options.count();i++)await options.nth(i).uncheck();
 const update=async()=>{const response=page.waitForResponse(r=>r.url().endsWith('/composer/v1/validate'));await frame.getByRole('button',{name:'Update scope',exact:true}).click();expect((await response).status()).toBe(200);await expect(frame.getByText('Scope updated. Apply affected blocks to calculate.',{exact:true})).toBeVisible();};
 let releaseValidation!:()=>void,validationArrived!:()=>void;
 const validationGate=new Promise<void>(resolve=>{releaseValidation=resolve;}),arrived=new Promise<void>(resolve=>{validationArrived=resolve;});
 await page.route('**/composer/v1/validate',async route=>{const response=await route.fetch();validationArrived();await validationGate;await route.fulfill({response});});
 await frame.getByRole('button',{name:'Update scope',exact:true}).click();await arrived;await expect(frame.getByRole('button',{name:'Save report',exact:true})).toBeDisabled();
 releaseValidation();await expect(frame.getByText('Scope updated. Apply affected blocks to calculate.',{exact:true})).toBeVisible();await page.unroute('**/composer/v1/validate');
 await expect(frame.getByRole('button',{name:'Save report',exact:true})).toBeEnabled();await expect(frame.locator('.composer-effective')).toContainText('month');expect(applies).toBe(0);
 for(const article of [first,second]){await article.getByRole('button',{name:'Apply',exact:true}).click();await expect(article.getByRole('table')).toBeVisible({timeout:60000});}
 await frame.getByLabel('First block',{exact:true}).selectOption(left);await expect(frame.getByLabel('Second block',{exact:true})).toHaveValue(right);
 const pair=frame.getByRole('region',{name:'Block comparison',exact:true});
 await pair.getByRole('button',{name:'Compare blocks',exact:true}).click();await expect(pair.getByText('Comparable data',{exact:true})).toBeVisible();expect(applies).toBe(2);expect(compares).toBe(1);
 // Local context invalidates only the affected block and the pair artifact.
 await frame.getByLabel('Scope target',{exact:true}).selectOption(right);await frame.getByLabel('Scope grain',{exact:true}).selectOption('week');await update();
 await expect(first.getByRole('table')).toBeVisible();await expect(second.getByRole('table')).toHaveCount(0);await expect(pair.getByRole('table')).toHaveCount(0);
 await second.getByRole('button',{name:'Apply',exact:true}).click();await expect(second.getByRole('table')).toBeVisible({timeout:60000});await pair.getByRole('button',{name:'Compare blocks',exact:true}).click();await expect(pair.getByText('Comparison unavailable',{exact:true})).toBeVisible();
 const saving=page.waitForResponse(r=>r.url().endsWith('/composer/v1/versions'));await frame.getByRole('button',{name:'Save report',exact:true}).click();const response=await saving;expect(response.status()).toBe(200);const saved=await response.json();expect(saved.comparison.totals.reason_codes).toContain('GRAIN_MISMATCH');expect(saved.results).toHaveLength(2);
 await page.waitForURL(/reports\/[0-9a-f-]+\/edit/);await page.reload();await expect(pair.getByText('Comparison unavailable',{exact:true})).toBeVisible();expect(applies).toBe(3);expect(compares).toBe(2);
 await frame.getByRole('button',{name:'Exact saved preview',exact:true}).click();await page.waitForURL(/snapshots\//);await expect(frame.locator('.composer')).toBeVisible({timeout:60000});await frame.locator('summary').filter({hasText:'Filters and analytical context'}).click();await frame.getByLabel('Inspect effective block context',{exact:true}).selectOption(right);await expect(frame.locator('.composer-effective')).toContainText('week');await expect(pair.getByRole('table')).toBeVisible();await expect(pair.getByRole('button',{name:'Compare blocks',exact:true})).toHaveCount(0);
 await page.screenshot({path:testInfo.outputPath('c04-saved-pair-scopes.png'),fullPage:true});expect(errors).toEqual([]);expect(applies).toBe(3);expect(compares).toBe(2);
});

test('C04 Russian linked empty store scope, keyboard update and Undo',async({page,request},testInfo)=>{
 const scenario=await(await request.get('/fixture/scenario')).json() as {workspace:string};
 let applies=0;const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(r.url().endsWith('/composer/v1/apply'))applies++;});
 await page.addInitScript(()=>localStorage.setItem('custometry-language','en'));
 await page.goto('/auth/sign-in');await page.getByLabel(/Workspace/).fill(scenario.workspace);await page.getByLabel('Email',{exact:true}).fill('author@example.test');await page.getByLabel('Password',{exact:true}).fill('synthetic-author-password');await page.getByRole('button',{name:'Sign in',exact:true}).click();await page.waitForURL(/\/reports$/);
 await page.goto(`/w/${scenario.workspace}/reports/new/edit?view=composer`);const frame=page.frameLocator('iframe');
 for(const name of ['Источник связи','Получатель связи']){await frame.getByRole('button',{name:'Add block',exact:true}).last().click();await frame.getByRole('button',{name:'Continue',exact:true}).click();await frame.getByRole('button',{name:'Continue',exact:true}).click();await frame.getByLabel('Block type',{exact:true}).selectOption('table');await frame.getByLabel('Block title',{exact:true}).fill(name);await frame.getByRole('button',{name:'Add to document',exact:true}).click();await expect(frame.getByRole('article',{name,exact:true})).toBeVisible();}
 await frame.locator('#view-menu-open').click();await frame.locator('#locale-toggle').click();await page.keyboard.press('Escape');
 const source=frame.getByRole('article',{name:'Источник связи',exact:true}),target=frame.getByRole('article',{name:'Получатель связи',exact:true});
 await frame.locator('summary').filter({hasText:'Фильтры и аналитический контекст'}).click();await frame.getByLabel('Область действия',{exact:true}).selectOption((await source.getAttribute('data-block-id'))!);
 const stores=frame.getByRole('group',{name:'Магазины области',exact:true});await stores.getByLabel('Все доступные магазины',{exact:true}).uncheck();const options=stores.locator('.mw-store-list input');await expect(options).not.toHaveCount(0);for(let i=0;i<await options.count();i++)await options.nth(i).uncheck();
 await frame.getByRole('group',{name:'Также применить это условие к блокам',exact:true}).getByLabel('Получатель связи',{exact:true}).check();
 const updated=page.waitForResponse(r=>r.url().endsWith('/composer/v1/validate'));await frame.getByRole('button',{name:'Обновить область',exact:true}).focus();await page.keyboard.press('Enter');expect((await updated).status()).toBe(200);
 await frame.getByLabel('Проверить контекст блока',{exact:true}).selectOption((await target.getAttribute('data-block-id'))!);await expect(frame.locator('.composer-effective')).toContainText('Пустая выборка');await expect(frame.locator('.composer-effective')).toContainText('Связанное условие');expect(applies).toBe(0);
 for(const block of [source,target]){await block.getByRole('button',{name:'Применить',exact:true}).click();await expect(block.getByRole('table')).toBeVisible({timeout:60000});}
 await frame.locator('summary').filter({hasText:'Структура документа'}).click();await frame.getByRole('button',{name:'Отменить',exact:true}).click();await expect(target.getByRole('table')).toHaveCount(0);await frame.getByRole('button',{name:'Повторить',exact:true}).click();await expect(target.getByRole('table')).toBeVisible();expect(applies).toBe(2);
 await frame.locator('.composer-scopes').screenshot({path:testInfo.outputPath('c04-ru-linked-empty.png')});expect(errors).toEqual([]);
});
