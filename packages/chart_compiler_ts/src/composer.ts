import type {EChartsOption,SeriesOption} from 'echarts';
import type {composerReports as C} from '@custometry/contracts';
import {seriesFor,visualColors} from './visual';
/** Convert typed presentation settings only; values and aggregates come from the server. */
export function applyChartVisual(base:EChartsOption,p:C.BlockPresentation|undefined,keys:readonly string[],units:readonly string[],totals:readonly (string|null)[]=[],locale:'ru'|'en'='en',chartWidth=600):EChartsOption{
 if(!p)return base;
 const v=p.visual??{},kind=p.chart_type??'line';
 if(!['line','bar','area','stacked_bar','combo','pictorial_bar','pie','donut','gauge','progress'].includes(kind))throw new Error('COMPOSER_CHART_DATA_SHAPE_UNAVAILABLE');
 const horizontal=v.horizontal&&['bar','stacked_bar','pictorial_bar'].includes(kind);
 const original=(Array.isArray(base.series)?base.series:[]) as SeriesOption[];
 const settings=seriesFor({presentation:p} as C.ComposerBlock,keys);
 const axes=[...new Set(units)];
 const format=(value:unknown,percent=false)=>value==null?'—':new Intl.NumberFormat(locale,{maximumFractionDigits:percent?1:v.decimals??2,notation:!percent&&v.compact?'compact':'standard'}).format(Number(value));
 const series:SeriesOption[]=original.flatMap((item,index)=>{
  const s=settings[index]??{key:keys[index]??String(index)},visible=s.visible!==false;if(!visible)return [];
  const type=kind==='combo'?(s.kind==='area'?'line':s.kind??'line'):kind==='area'?'line':kind==='stacked_bar'?'bar':kind==='pictorial_bar'?'pictorialBar':kind;
  const color=visualColors[s.color??(index===0?'primary':'secondary')];
  const inside=(s.label_position??v.label_position??'top').startsWith('inside');
  const label={show:s.labels??v.labels??false,position:s.label_position??v.label_position??'top',rotate:v.label_rotate??0,color:'#f4f6f8',backgroundColor:inside?'#121a21':undefined,padding:inside?[2,3]:0,borderRadius:2,fontWeight:600,textBorderColor:inside?undefined:'#121a21',textBorderWidth:inside?0:3,formatter:(params:{value:unknown})=>format(params.value,units[index]==='percent')};
  const common={...item,name:s.name||item.name,itemStyle:{color},label,labelLayout:{hideOverlap:v.hide_overlap!==false}};
  if(kind==='pie'||kind==='donut'){
   if(index>0)return [];
   const x=Array.isArray(base.xAxis)?base.xAxis[0]:base.xAxis;
   const names=x&&'data' in x?x.data as string[]:[];
   const data=('data' in item?item.data??[]:[]) as (string|null)[];
   return [{...common,type:'pie',radius:kind==='donut'?[`${(v.pie_radius??45)*.6}%`,`${v.pie_radius??45}%`]:`${v.pie_radius??45}%`,startAngle:v.start_angle??90,label:{...label,position:v.label_position==='inside'?'inside':'outside'},data:data.map((value,i)=>({name:names[i]??String(i),value:value==null?undefined:Number(value)}))} as SeriesOption];
  }
  if(kind==='gauge'||kind==='progress'){
   if(index>0)return [];
   return [{...common,type:'gauge',min:v.gauge_min??0,max:v.gauge_max??100,startAngle:kind==='progress'?180:225,endAngle:kind==='progress'?0:-45,progress:{show:true},pointer:{show:kind==='gauge'},detail:{formatter:(value:number)=>format(value,units[index]==='percent'),color:'#dce2e8',fontSize:24},data:[{value:totals[index]==null?undefined:Number(totals[index]),name:String(common.name??'')}]} as SeriesOption];
  }
  const axis=s.axis==='left'?0:s.axis==='right'?1:axes.indexOf(units[index]);
  return [{...common,type,yAxisIndex:axis,xAxisIndex:0,stack:kind==='stacked_bar'?'total':undefined,smooth:s.shape==='smooth',step:s.shape==='step'?'end':false,showSymbol:s.points!==false,symbolSize:v.symbol_size??6,lineStyle:{color,width:s.width??2,type:s.stroke??'solid'},areaStyle:kind==='area'||kind==='combo'&&s.kind==='area'?{opacity:s.fill_opacity??.15,color}:undefined,barMaxWidth:v.bar_width??32,barGap:`${v.bar_gap??20}%`,barCategoryGap:`${v.bar_gap??20}%`,symbol:kind==='pictorial_bar'?'rect':undefined,markLine:v.goal!=null?{silent:true,symbol:'none',data:[{[horizontal?'xAxis':'yAxis']:v.goal,name:v.goal_label?.trim()||(locale==='ru'?'Цель':'Goal'),label:{position:'insideEndTop',color:'#dce2e8',backgroundColor:'#121b22',padding:[3,5],formatter:(params:{name:string;value:unknown})=>`${params.name}: ${format(params.value,units[index]==='percent')}`}}]}:('markLine' in item?item.markLine:undefined)} as SeriesOption];
 });
 const existingAxes=Array.isArray(base.yAxis)?base.yAxis:base.yAxis?[base.yAxis]:[];
 const axisCount=Math.max(existingAxes.length,settings.some(s=>s.axis==='right')?2:1);
 // Reference lines do not contribute to ECharts data extents. Expand only automatic bounds.
 const goalBound=(axis:number,side:'min'|'max')=>v.goal!=null&&series.some(s=>'yAxisIndex' in s&&s.yAxisIndex===axis)?(extent:{min:number;max:number})=>{
  const goal=v.goal!;const edge=side==='min'?Math.min(0,extent.min):Math.max(0,extent.max);
  if(side==='min'?goal>edge:goal<edge)return side==='min'?Math.min(edge,goal):Math.max(edge,goal);
  const padding=Math.max(Math.abs(goal),Math.abs(extent.max-extent.min),1)*.05;
  return side==='min'?goal-padding:goal+padding;
 }:undefined;
 const yAxis=Array.from({length:axisCount},(_,i)=>({...existingAxes[i]??existingAxes[0],id:'visual-axis-'+i,show:v.y_visible!==false,name:(i?v.y_right_title:v.y_title)??'',position:i===0?'left' as const:'right' as const,offset:Math.max(0,i-1)*52,min:v.y_min??goalBound(i,'min'),max:v.y_max??goalBound(i,'max'),interval:undefined,scale:false,axisLabel:{formatter:(value:number)=>format(value,axes[i]==='percent')},splitLine:{show:v.grid_lines!==false,lineStyle:{color:'#343b42'}}}));
 const xAxis={...(Array.isArray(base.xAxis)?base.xAxis[0]:base.xAxis),show:v.x_visible!==false,name:v.x_title??'',nameLocation:'middle' as const,nameGap:horizontal?65:32,nameTextStyle:{color:'#cbd3db'},axisLabel:{rotate:v.x_rotate??0}};
 const cartesian=['line','bar','area','stacked_bar','combo','pictorial_bar'].includes(kind);
 const pos=v.legend_position??'bottom';
 const side=Boolean(p.legend&&['left','right'].includes(pos));
 const legendWidth=Math.max(70,Math.min(210,Math.floor(chartWidth*.3)));
 const inset=side?legendWidth+28:8;
 const plotCenter=pos==='left'?`${50+(inset/chartWidth)*50}%`:`${50-(inset/chartWidth)*50}%`;

 return {...base,animation:base.animation!==false&&v.animation!==false,legend:{show:p.legend??false,type:'scroll',width:side?legendWidth:undefined,textStyle:{color:'#dce2e8',...(side?{width:legendWidth-32,overflow:'truncate' as const}: {})},tooltip:{show:true},orient:['left','right'].includes(pos)?'vertical':'horizontal',top:pos==='top'?0:pos==='bottom'?'auto':'middle',bottom:pos==='bottom'?0:'auto',left:pos==='left'?0:pos==='right'?'auto':'center',right:pos==='right'?0:'auto'},tooltip:{...base.tooltip as object,show:v.tooltip!==false,trigger:cartesian?'axis':'item',...(['gauge','progress'].includes(kind)?{formatter:undefined}: {})},grid:{left:(side&&pos==='left'?inset:8)+(horizontal&&v.x_title?55:0),right:side&&pos==='right'?inset:8,bottom:(p.legend&&pos==='bottom'?48:24)+(!horizontal&&v.x_title?30:0),top:p.legend&&pos==='top'?48:28,containLabel:true},xAxis:cartesian?(horizontal?yAxis:xAxis):[],yAxis:cartesian?(horizontal?{...xAxis,position:'left'}:yAxis):[],dataZoom:v.zoom&&cartesian?[{type:'inside',filterMode:'none'}]:[],series:!cartesian&&side?series.map(s=>({...s,center:[plotCenter,'50%'],...(s.type==='pie'?{radius:kind==='donut'?['22%','36%']:'36%'}:{})} as SeriesOption)):horizontal?series.map(s=>({...s,xAxisIndex:('yAxisIndex' in s?s.yAxisIndex:0),yAxisIndex:0} as SeriesOption)):series} as EChartsOption;
}
