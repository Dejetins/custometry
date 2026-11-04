import {test,expect,openInspector,closeInspector} from './observed-test';
test('reader private view, EN, administrative separation and session revocation',async({page,request},info)=>{
 const scenario=await(await request.get('/fixture/scenario')).json() as {workspace:string;report:string};
 await page.addInitScript(()=>localStorage.setItem('custometry-language','en'));await page.goto('/auth/sign-in');
 await page.getByLabel(/Workspace/).fill(scenario.workspace);await page.getByLabel('Email',{exact:true}).fill('reader@example.test');await page.getByLabel('Password',{exact:true}).fill('synthetic-reader-password');await page.getByRole('button',{name:'Sign in',exact:true}).click();await page.waitForURL(/\/reports$/);
 await page.goto(`/w/${scenario.workspace}/reports/${scenario.report}/edit`);const f=page.frameLocator('iframe');await openInspector(f);
 await expect(f.getByLabel('Report title',{exact:true})).toBeDisabled();await expect(f.getByRole('button',{name:'Add workset',exact:true})).toHaveCount(0);await closeInspector(f);
 await f.getByRole('button',{name:/2025-01-01.*Report context/}).click();await f.getByLabel('From',{exact:true}).fill('2025-01-02');await closeInspector(f);
 await f.getByRole('button',{name:'Apply',exact:true}).click();await expect(f.locator('.mw')).toHaveAttribute('aria-busy','false',{timeout:60000});
 await expect(f.locator('.mw-cards .kpi-value').first()).not.toHaveText('—',{timeout:60000});await f.getByRole('button',{name:'Save personal view',exact:true}).click();await expect(f.getByRole('status').filter({hasText:'Saved'})).toBeVisible({timeout:60000});

 // Reopen after withdrawing effective report run authorization; data-read policy remains.
 const selectedView=await f.getByRole('combobox',{name:'My saved views',exact:true}).inputValue();
 await request.post(`/fixture/reader-view-only/${scenario.report}`);await page.reload();
 await openInspector(f);await closeInspector(f);
 await expect(f.getByRole('button',{name:'Apply',exact:true})).toBeDisabled();
 const calculations:string[]=[];page.on('request',r=>{if(r.method()==='POST'&&/\/(apply|results)$/.test(new URL(r.url()).pathname))calculations.push(r.url());});
 await f.getByRole('combobox',{name:'My saved views',exact:true}).selectOption(selectedView);
 await f.getByRole('button',{name:'Table',exact:true}).last().click();await expect(f.locator('.mw-table tbody tr')).toHaveCount(30);
 const priorRows=await f.locator('.mw-table tbody').innerText();
 await expect(f.getByRole('button',{name:'Save personal view',exact:true})).toBeEnabled();await f.getByRole('button',{name:'Save personal view',exact:true}).click();await expect(f.getByRole('status').filter({hasText:'Saved'})).toBeVisible({timeout:60000});
 await page.reload();await openInspector(f);await closeInspector(f);await f.getByRole('combobox',{name:'My saved views',exact:true}).selectOption(selectedView);await expect(f.locator('.mw-table tbody')).toHaveText(priorRows,{useInnerText:true});expect(calculations).toEqual([]);
 await expect(f.locator('#workspace-calendar-settings')).toHaveCount(0);await expect(f.getByRole('button',{name:'Adopt company calendar'})).toHaveCount(0);
 await page.screenshot({path:info.outputPath('reader-en.png')});
 // The production logout endpoint invalidates the actual browser session; no intercepted response.
 await page.evaluate(async()=>{const token=decodeURIComponent(document.cookie.split('; ').find(p=>p.startsWith('custometry_csrf='))?.split('=')[1]??'');await fetch('/api/identity/logout',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':token},body:'{}'});});
 await expect(f.locator('.mw-pending')).toBeVisible({timeout:30000});await expect(f.locator('.title-row h1')).toHaveText('');await expect(f.getByRole('alert')).toBeVisible();
});
