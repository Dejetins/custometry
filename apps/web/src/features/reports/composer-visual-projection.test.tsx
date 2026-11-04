import {afterEach,expect,it} from 'vitest';
import {render,screen,cleanup} from '@testing-library/react';
import type {configuredReports as W} from '@custometry/contracts';
import {WorkspaceTable,projection} from './WorkspaceProjection';
import {ComposerVisualTable} from './ComposerVisualTable';
afterEach(cleanup);
const definition={selection:{mode:'single',card_id:'a',temporal:'previous_year_same_dates'}} as W.ConfiguredReportV2;
const bindings=[{card_id:'a',bucket_projection:'net_revenue',unit:'EUR',result:{result_id:'r'}},{card_id:'b',bucket_projection:'receipt_count',unit:'receipt',result:{result_id:'r'}}] as W.CardResultBinding[];
const change=(left:string,right:string)=>({left,right,absolute_delta:'1',relative_delta_percent:'2',reason_codes:[]});
const result={result_id:'r',buckets:[{bucket_id:'jan',label:'Jan',effective_starts_on:'2025-01-01',effective_ends_on:'2025-01-31',state:'ready',is_partial_bucket:false,values:{net_revenue:'10',receipt_count:'3'},coverage:{reason_codes:[]}}],temporal:{buckets:[{bucket_id:'jan',baseline_dates:['2024-01-01'],changes:{net_revenue:change('10','9'),receipt_count:change('3','2')}}]}} as unknown as W.WorkspaceResultV2;
it('keeps the primary metric when the source result includes other metrics',()=>{
 const data=projection({definition,bindings,results:new Map([['r',result]]),comparison:null,locale:'en'});expect(data.rows[0].values).toEqual(['10','9']);
});
it('keeps the previous period for each metric in an explicit combo',()=>{
 const data=projection({definition,bindings,results:new Map([['r',result]]),comparison:null,locale:'en',multiSeries:true});expect(data.rows[0].values).toEqual(['10','9','3','2']);expect(data.units).toEqual(['EUR','EUR','receipt','receipt']);
});
it('preserves partial-period evidence after customizing a table',()=>{
 render(<ComposerVisualTable presentation={{title:'Table',visual:{decimals:1}}} locale="en" data={{comparisonLabel:null,comparisonMissing:false,names:['net_revenue'],units:['EUR'],rows:[{id:'jan',label:'Jan',values:['10'],baseline:'',absolute:null,relative:null,reasons:[],partial:true,state:'ready'}]}}/>);expect(screen.getByText(/Partial bucket/)).toBeTruthy();
});
it('retains all metric pairs and incomplete coverage with temporal v2',()=>{
 const pair=(left:string,right:string,state='complete')=>({...change(left,right),left_coverage:{state},right_coverage:{state:'complete'}});
 const modern={...result,temporal:null,temporal_v2:{spec:{settings:{mode:'previous_year'}},buckets:[{current_bucket_id:'jan',current_dates:['2025-01-01'],comparison_dates:['2024-01-01'],changes:{net_revenue:pair('10','9'),receipt_count:pair('3','2','incomplete')}}]}} as unknown as W.WorkspaceResultV2;
 const data=projection({definition,bindings,results:new Map([['r',modern]]),comparison:null,locale:'en',multiSeries:true});expect(data.rows[0].values).toEqual(['10','9','3','2']);expect(data.rows[0].partial).toBe(true);
});

it('keeps comparison values and deltas without calendar mapping columns on the canvas',()=>{
 const {container}=render(<WorkspaceTable definition={definition} bindings={bindings} results={new Map([['r',result]])} comparison={null} locale="en" compact/>);
 expect(container.textContent).not.toContain('same dates');expect(container.textContent).not.toContain('2024-01');
 expect(screen.getByRole('columnheader',{name:/Prior year/})).toBeTruthy();
 expect(screen.getByRole('cell',{name:'9'})).toBeTruthy();expect(screen.getByRole('columnheader',{name:'Δ'})).toBeTruthy();
});
it('keeps configured comparison tables free of calendar mapping columns',()=>{
 const data=projection({definition,bindings,results:new Map([['r',result]]),comparison:null,locale:'en'});
 const {container}=render(<ComposerVisualTable presentation={{title:'Table',visual:{decimals:1}}} locale="en" data={data}/>);
 expect(container.textContent).not.toContain('Comparison period');expect(container.textContent).not.toContain('2024-01');
 expect(screen.getByRole('cell',{name:'9'})).toBeTruthy();
});
