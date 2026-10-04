import {test as base,expect} from '@playwright/test';
import {writeFile} from 'node:fs/promises';
type Event={method:string;path:string;status:number;classification:string};
export const test=base.extend<{observation:void}>({observation:[async({context},use,info)=>{
 const network:Event[]=[];const errors:string[]=[];const consoleEntries:{type:string;text:string}[]=[];
 context.on('page',page=>{page.on('pageerror',error=>errors.push(error.message));page.on('console',message=>{if(message.type()==='error'||message.type()==='warning')consoleEntries.push({type:message.type(),text:message.text()});});page.on('response',response=>{const url=new URL(response.url());if(!url.pathname.startsWith('/api/'))return;const status=response.status();const expected=status===401&&url.pathname==='/api/identity/me'||status===409&&/\/api\/reports\/v2\/[^/]+\/(apply|versions)$/.test(url.pathname);network.push({method:response.request().method(),path:url.pathname,status,classification:status<400?'success':expected?'expected-denial-or-conflict':'unexpected-error'});});});
 await use();
 const unexpected=network.filter(e=>e.classification==='unexpected-error');
 const consoleErrors=consoleEntries.filter(e=>e.type==='error'&&!(/status of (401|409)/.test(e.text)&&network.some(n=>n.classification==='expected-denial-or-conflict')));
 await writeFile(info.outputPath('browser-observations.json'),JSON.stringify({schema:'ms004-browser-observation/v1',test:info.title,project:info.project.name,network,console:consoleEntries,pageErrors:errors},null,2));
 expect(errors,'browser exceptions').toEqual([]);expect(unexpected,'unexpected API failures').toEqual([]);expect(consoleErrors,'unexpected console errors').toEqual([]);
 },{auto:true}]});
export {expect} from '@playwright/test';
