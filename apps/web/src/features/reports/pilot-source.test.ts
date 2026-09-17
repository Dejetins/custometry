import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {expect,it} from 'vitest';
import {reportPilotCopy} from '@custometry/localization';
it('retains the pinned pilot cascade with only selector isolation',()=>{
 const source=readFileSync(resolve(process.cwd(),'../../docs/architecture/ui/target-pilot/ru/source.html'),'utf8');
 expect(createHash('sha256').update(source).digest('hex')).toBe('b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700');
 let css=source.split('<style>')[1].split('</style>')[0].replaceAll(':root','&').replace(/(?<![\w-])\b(?:html|body)\b/g,'&');
 for(const name of ['app-shell','brand','nav-item','sidebar','sidebar-footer','skip-link','sr-only'])css=css.replace(new RegExp('\\.'+name+'(?![\\w-])','g'),'.pilot-'+name);
 const actual=readFileSync(resolve(process.cwd(),'src/features/reports/pilot.css'),'utf8').split('.report-pilot {')[1].replace(/}\s*$/,'');
 expect(actual.trim()).toBe(css.trim());
 expect(Object.keys(reportPilotCopy.ru)).toEqual(Object.keys(reportPilotCopy.en));
});
