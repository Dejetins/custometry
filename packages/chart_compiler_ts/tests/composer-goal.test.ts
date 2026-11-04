import {describe,it,expect} from 'vitest';
import * as echarts from 'echarts';
import type {composerReports as C} from '@custometry/contracts';
import {applyChartVisual} from '../src/composer';
const base:echarts.EChartsOption={xAxis:{type:'category',data:['Jan','Feb']},yAxis:{type:'value'},series:[{type:'line',data:[30000,44000]}]};
function option(visual:C.BlockVisual={}){return applyChartVisual(base,{chart_type:'line',visual} as C.BlockPresentation,['revenue'],['EUR']);}
describe('composer goal scale',()=>{
 it.each([60000,-10000,0])('includes goal %s in automatic bounds',goal=>{
  const chart=echarts.init(null,undefined,{renderer:'svg',ssr:true,width:600,height:400});
  chart.setOption(option({goal,goal_label:'Sales target',animation:false}));
  const point=chart.convertToPixel({seriesIndex:0},['Jan',goal]) as number[];
  expect(point[1]).toBeGreaterThan(20);expect(point[1]).toBeLessThan(375);
  expect(chart.renderToSVGString()).toContain('Sales target:');chart.dispose();
 });
 it('preserves explicit limits and restores auto scale when removed',()=>{
  const axes=option({goal:60000,y_min:0,y_max:50000}).yAxis as any[];
  expect(axes[0].min).toBe(0);expect(axes[0].max).toBe(50000);
  expect((option({goal:null}).yAxis as any[])[0].max).toBeUndefined();
 });
 it('places horizontal bar goals on their value axis',()=>{
  const chart=echarts.init(null,undefined,{renderer:'svg',ssr:true,width:600,height:400});
  const result=applyChartVisual(base,{chart_type:'bar',visual:{horizontal:true,goal:60000,animation:false}} as C.BlockPresentation,['revenue'],['EUR']);
  chart.setOption(result);const point=chart.convertToPixel({seriesIndex:0},[60000,'Jan']) as number[];
  expect(point[0]).toBeGreaterThan(30);expect(point[0]).toBeLessThan(590);
  expect(chart.renderToSVGString()).toContain('Goal: 60,000');chart.dispose();
 });
});
