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
  it('rejects a body decoded after logout and a new login generation',async()=>{
    clearReportAccess(false);let release!:()=>void;
    const response=new Response(new ReadableStream({start(controller){release=()=>{controller.enqueue(new TextEncoder().encode('{"title":"Previous principal"}'));controller.close();};}}));
    vi.stubGlobal('fetch',vi.fn().mockResolvedValue(response));
    const received=await protectedFetch('/api/reports/old');const body=received.json();
    clearReportAccess();clearReportAccess(false);release();
    await expect(body).rejects.toThrow('ACCESS_DENIED');
  });
  it('keeps RU and EN report copy keys identical',()=>{expect(Object.keys(reportCopy.ru).sort()).toEqual(Object.keys(reportCopy.en).sort());});
});

it('cancels oversized result bodies before cache admission',async()=>{
 clearReportAccess(false);const cancel=vi.fn();let count=0;
 vi.stubGlobal('fetch',vi.fn().mockResolvedValue(new Response(new ReadableStream({pull(controller){controller.enqueue(new Uint8Array(1024*1024));count++;},cancel}))));
 const response=await protectedFetch('/api/analytics/datasets/test/results/large');
 await expect(response.json()).rejects.toThrow('RESPONSE_PAYLOAD_LIMIT');
 expect(cancel).toHaveBeenCalledOnce();expect(count).toBeLessThanOrEqual(4);
 expect(reportQueries.getQueryCache().getAll()).toHaveLength(0);
});
