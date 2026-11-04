import {expect,it} from 'vitest';
import type {EChartsOption} from 'echarts';
import {applyChartVisual} from './composer-chart-options';
const base:EChartsOption={animation:true,xAxis:{type:'category',data:['Jan','Feb']},yAxis:[{type:'value'},{type:'value'}],series:[{type:'line',name:'Revenue',data:['10',null]},{type:'line',name:'Receipts',data:['2','3']}]};
it('compiles independent combo rows and preserves missing values',()=>{
 const option=applyChartVisual(base,{title:'Combo',chart_type:'combo',visual:{series:[{key:'revenue',kind:'bar',color:'violet',axis:'left'},{key:'receipts',kind:'area',axis:'right',labels:true}]}},['revenue','receipts'],['EUR','receipt']);
 expect(option.series).toMatchObject([{type:'bar',yAxisIndex:0,itemStyle:{color:'#a195d5'},data:['10',null]},{type:'line',yAxisIndex:1,areaStyle:{opacity:.15},label:{show:true}}]);
});
it('uses server totals for gauges without calculating averages from buckets',()=>{
 const option=applyChartVisual(base,{title:'Gauge',chart_type:'gauge',visual:{gauge_max:50}},['revenue'],['EUR'],['17']);
 expect(option.series).toMatchObject([{type:'gauge',max:50,data:[{value:17}]}]);expect(option.xAxis).toEqual([]);
});
it('hides selected rows and respects motion preference',()=>{
 const option=applyChartVisual({...base,animation:false},{title:'Chart',visual:{series:[{key:'receipts',visible:false}],animation:true}},['revenue','receipts'],['EUR','receipt']);
 expect(option.series).toHaveLength(1);expect(option.animation).toBe(false);
});
it('swaps category and value axes for horizontal bars',()=>{
 const option=applyChartVisual(base,{title:'Bars',chart_type:'bar',visual:{horizontal:true}},['revenue','receipts'],['EUR','receipt']);
 expect(option.yAxis).toMatchObject({type:'category',data:['Jan','Feb']});expect(option.series).toMatchObject([{xAxisIndex:0,yAxisIndex:0},{xAxisIndex:1,yAxisIndex:0}]);
});
it('does not retain pre-stack extents or clip negative bars with an automatic minimum',()=>{
 const option=applyChartVisual({...base,yAxis:[{type:'value',min:0,max:10,interval:2}]},{title:'Stack',chart_type:'stacked_bar'},['revenue','receipts'],['EUR','EUR']);
 expect(option.yAxis).toMatchObject([{min:undefined,max:undefined,interval:undefined,scale:false}]);
});
it('rejects unsupported shapes rather than passing invalid types to ECharts',()=>{
 expect(()=>applyChartVisual(base,{title:'Sankey',chart_type:'sankey'},['revenue'],['EUR'])).toThrow('COMPOSER_CHART_DATA_SHAPE_UNAVAILABLE');
});

it.each(['left','right'] as const)('reserves a separate %s legend lane and resets it when hidden',position=>{
 const p={title:'Chart',legend:true,visual:{legend_position:position}};
 const shown=applyChartVisual(base,p,['revenue','receipts'],['EUR','receipt'],[],'en',600);
 expect(shown.grid).toMatchObject({[position]:208});expect(shown.legend).toMatchObject({type:'scroll',width:180});
 const hidden=applyChartVisual(base,{...p,legend:false},['revenue','receipts'],['EUR','receipt']);expect(hidden.grid).toMatchObject({left:8,right:8});
});
it('reserves space for the centered category title in both orientations',()=>{
 const vertical=applyChartVisual(base,{title:'Chart',chart_type:'bar',visual:{x_title:'Month'}},['revenue'],['EUR']);
 expect(vertical.xAxis).toMatchObject({name:'Month',nameLocation:'middle'});expect(vertical.grid).toMatchObject({bottom:54});
 const horizontal=applyChartVisual(base,{title:'Chart',chart_type:'bar',visual:{x_title:'Month',horizontal:true}},['revenue'],['EUR']);
 expect(horizontal.yAxis).toMatchObject({name:'Month',nameGap:65});expect(horizontal.grid).toMatchObject({left:63});
});
it('uses contrasting inside labels and applies category spacing to stacked bars',()=>{
 const option=applyChartVisual(base,{title:'Stack',chart_type:'stacked_bar',visual:{labels:true,label_position:'inside',bar_width:12,bar_gap:70}},['revenue','receipts'],['EUR','EUR']);
 expect(option.series).toMatchObject([{label:{color:'#f4f6f8',backgroundColor:'#121a21',fontWeight:600},barMaxWidth:12,barCategoryGap:'70%'},{barCategoryGap:'70%'}]);
});
