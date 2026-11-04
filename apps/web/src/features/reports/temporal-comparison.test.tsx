import {afterEach,describe,it,expect,vi} from 'vitest';
import {render,cleanup,fireEvent,screen} from '@testing-library/react';
import type {composerReports as C,configuredReports as W} from '@custometry/contracts';
import {TemporalSettingsEditor} from './TemporalSettingsEditor';
import {TemporalComparisonDetails} from './TemporalComparisonDetails';
import {projection} from './WorkspaceProjection';

afterEach(cleanup);
const change={left:'120',right:'0',absolute_delta:'120',relative_delta_percent:null,reason_codes:['ZERO_BASELINE'],left_coverage:{state:'complete'},right_coverage:{state:'complete'}};
const artifact={spec:{settings:{mode:'custom_period',incomplete_period_policy:'explicit_partial'},timezone:'UTC',current_period:{starts_on:'2025-01-01',ends_on:'2025-01-03',local_date_count:3},comparison_period:{starts_on:'2024-01-01',ends_on:'2024-01-03',local_date_count:3},overlap_local_dates:0,duration_difference_local_dates:0},evaluated_current_dates:['2025-01-01'],evaluated_comparison_dates:['2024-01-01'],comparability_status:'descriptive',limitation_codes:['ZERO_BASELINE'],changes:{net_revenue:change},buckets:[{current_bucket_id:'current',current_dates:['2025-01-01'],comparison_dates:['2024-01-01'],changes:{net_revenue:change}}]} as unknown as C.TemporalArtifactV2;
describe('explicit temporal presentation',()=>{
 it('keeps unavailable relative delta distinct from zero and labels actual custom period',()=>{
  const {container}=render(<TemporalComparisonDetails value={artifact} metric="net_revenue" locale="en"/>);
  expect(screen.getByRole('heading').textContent).toBe('Custom comparison period · UTC');
  expect(Array.from(container.querySelectorAll('td')).map(td=>td.dataset.value)).toEqual(['120','0','120','']);
  expect(container.textContent).toContain('No duration normalization.');expect(container.textContent).not.toContain('Prior year');expect(container.textContent).not.toContain('Infinity');
 });
 it('projects backend paired dates/values without recalculating or labeling previous year',()=>{
  const result={result_id:'result',temporal_v2:artifact} as unknown as W.WorkspaceResultV2;
  const projected=projection({definition:{selection:{mode:'single',card_id:'card',temporal:'none'}} as W.ConfiguredReportV2,bindings:[{card_id:'card',result:{result_id:'result'},bucket_projection:'net_revenue',unit:'EUR'} as W.CardResultBinding],results:new Map([['result',result]]),comparison:null,locale:'en'});
  expect(projected.comparisonLabel).toBe('Custom comparison period');expect(projected.rows[0]).toMatchObject({dates:'2025-01-01',baseline:'2024-01-01',values:['120','0'],absolute:'120',relative:null,reasons:['ZERO_BASELINE']});
 });
 it('emits explicit inherited none, and clears new settings when selecting legacy mode',()=>{
  const callback=vi.fn();render(<TemporalSettingsEditor settings={null} alignment={null} change={callback} locale="en" label="Scope comparison" inherit/>);
  fireEvent.change(screen.getByLabelText('Scope comparison'),{target:{value:'none'}});expect(callback.mock.lastCall?.[0]).toMatchObject({mode:'none',incomplete_period_policy:'exclude'});
  fireEvent.change(screen.getByLabelText('Scope comparison'),{target:{value:'previous_year_same_dates'}});expect(callback.mock.lastCall).toEqual([null,'previous_year_same_dates']);
  fireEvent.change(screen.getByLabelText('Scope comparison'),{target:{value:'inherit'}});expect(callback.mock.lastCall).toEqual([null,null]);
 });
});

it('keeps explicit year policies separate from legacy mode and constrains elapsed mode',()=>{
 const callback=vi.fn();const view=render(<TemporalSettingsEditor settings={null} alignment="none" change={callback} locale="en" label="Temporal comparison"/>);
 fireEvent.change(screen.getByLabelText('Temporal comparison'),{target:{value:'explicit_previous_year_same_dates'}});expect(callback.mock.lastCall?.[0]).toMatchObject({mode:'previous_year_same_dates',leap_day_policy:'exclude'});expect(callback.mock.lastCall?.[1]).toBeNull();
 fireEvent.change(screen.getByLabelText('Temporal comparison'),{target:{value:'previous_year_iso_week_aligned'}});expect(callback.mock.lastCall?.[0]).toMatchObject({iso_week_53_policy:'exclude'});expect(callback.mock.lastCall?.[0].leap_day_policy).toBeUndefined();
 fireEvent.change(screen.getByLabelText('Temporal comparison'),{target:{value:'previous_year_comparable_elapsed_days'}});const settings=callback.mock.lastCall?.[0];expect(settings.incomplete_period_policy).toBe('comparable_elapsed_days');view.rerender(<TemporalSettingsEditor settings={settings} alignment={null} change={callback} locale="en" label="Temporal comparison"/>);expect((screen.getByLabelText('Incomplete period policy') as HTMLSelectElement).disabled).toBe(true);
});

it('discloses all-unmapped periods and exact excluded dates without a fabricated range',()=>{
 const value={...artifact,spec:{...artifact.spec,settings:{mode:'previous_year_same_dates',leap_day_policy:'exclude',incomplete_period_policy:'exclude'},comparison_period:null,date_mapping:[{current_date:'2024-02-29',comparison_date:null,excluded:true,reason:'LEAP_DAY_EXCLUDED'}]},comparability_status:'unavailable',evaluated_comparison_dates:[],evaluated_current_dates:[],limitation_codes:['COMPARISON_NO_MAPPED_DATES']} as C.TemporalArtifactV2;
 const {container}=render(<TemporalComparisonDetails value={value} metric="net_revenue" locale="en"/>);expect(container.textContent).toContain('No mapped comparison dates.');expect(container.textContent).toContain('2024-02-29 → — Excluded');expect(container.textContent).not.toContain('undefined');
});

it.each(['ru','en'] as const)('does not promise UTC for an effective pinned calendar in %s',locale=>{
 const {container}=render(<TemporalSettingsEditor settings={{mode:'previous_period',previous_period_basis:'local_date_duration',incomplete_period_policy:'exclude'}} alignment={null} change={vi.fn()} locale={locale} label="Comparison"/>);
 expect(container.textContent).not.toContain('UTC');expect(container.textContent).toContain(locale==='ru'?'действующий закреплённый календарь':'effective pinned calendar');
});
