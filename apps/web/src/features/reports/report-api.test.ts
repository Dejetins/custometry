import {afterEach,describe,expect,it,vi} from 'vitest';
import {clearReportAccess,reportQueries,protectedFetch,accessStore} from './report-api';
import {reportCopy} from './copy';
afterEach(()=>{vi.unstubAllGlobals();clearReportAccess(false);});
describe('protected report state',()=>{
  it('clears cached results and rejects older in-flight replies after denial',async()=>{
    clearReportAccess(false);let resolve!:(value:Response)=>void;
    vi.stubGlobal('fetch',vi.fn().mockImplementationOnce(()=>new Promise<Response>((r)=>{resolve=r;})).mockResolvedValueOnce(new Response('{}',{status:403})));
    reportQueries.setQueryData(['report','owned'],{title:'Protected'});
    const old=protectedFetch('/api/reports/owned');
    await expect(protectedFetch('/api/identity/me')).rejects.toThrow('ACCESS_DENIED');
    expect(accessStore.get()).toBe(true);expect(reportQueries.getQueryData(['report','owned'])).toBeUndefined();
    resolve(new Response('{}',{status:200}));await expect(old).rejects.toThrow('ACCESS_DENIED');
  });
  it('keeps RU and EN report copy keys identical',()=>{expect(Object.keys(reportCopy.ru).sort()).toEqual(Object.keys(reportCopy.en).sort());});
});
