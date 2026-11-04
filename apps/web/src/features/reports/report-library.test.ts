import {describe,it,expect} from 'vitest';
import {filterReports} from './ReportLibrary';
const report=(report_id:string,title:string,saved_at:string)=>({report_id,title,saved_at,revision:1,lifecycle:'owned_draft_preview' as const,snapshot_id:'s',version_id:'v'});
const rows=[report('1','Revenue','2026-09-01T10:00:00Z'),report('2','Receipts','2026-09-29T10:00:00Z')];
describe('report library',()=>{
 it('combines search, favorites and date filters without modifying source order',()=>{
  expect(filterReports(rows,'  RECE  ','7',['2'],true,'newest',new Date('2026-09-30T12:00:00Z').getTime()).map(r=>r.report_id)).toEqual(['2']);
  expect(filterReports(rows,'Revenue','7',[],false,'newest',new Date('2026-09-30T12:00:00Z').getTime())).toEqual([]);
  expect(filterReports(rows,'','0',[],false,'newest').map(r=>r.report_id)).toEqual(['2','1']);
  expect(rows.map(r=>r.report_id)).toEqual(['1','2']);
 });
 it('uses local calendar-day boundaries for today',()=>{
  const now=new Date(2026,8,30,12);const midnight=new Date(2026,8,30);const before=new Date(midnight.getTime()-1);
  expect(filterReports([report('a','A',midnight.toISOString()),report('b','B',before.toISOString())],'','1',[],false,'newest',now.getTime()).map(r=>r.report_id)).toEqual(['a']);
 });
});
