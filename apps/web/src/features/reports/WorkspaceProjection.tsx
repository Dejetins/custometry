import {chartCatalog} from './composer-visual';
import {ComposerVisualTable} from './ComposerVisualTable';
import {comparisonModeLabel} from './TemporalComparisonDetails';
import {lineAxisRange,signed,adjacentChange} from './workspace-presentation';
import {metricNames,workspaceReason,workspaceUnit} from './workspace-copy';
import {useEffect,useLayoutEffect,useMemo,useRef,useState} from 'react';
import * as echarts from 'echarts/core';
import {applyChartVisual} from './composer-chart-options';
import type {EChartsOption} from 'echarts';
import type {composerReports as C} from '@custometry/contracts';
import {LineChart,BarChart,PieChart,GaugeChart,PictorialBarChart} from 'echarts/charts';
import {GridComponent,TooltipComponent,LegendComponent,AriaComponent,MarkLineComponent,DataZoomComponent} from 'echarts/components';
import {SVGRenderer} from 'echarts/renderers';
import type {configuredReports as W} from '@custometry/contracts';
echarts.use([LineChart,BarChart,PieChart,GaugeChart,PictorialBarChart,DataZoomComponent,GridComponent,TooltipComponent,LegendComponent,AriaComponent,MarkLineComponent,SVGRenderer]);
interface Props {presentation?:C.BlockPresentation;multiSeries?:boolean;totals?:readonly (string|null)[];reveal?:boolean;chartType?:C.BlockPresentation['chart_type'];compact?:boolean;showDifferences?:boolean;legacy?:W.SalesResponse;definition:W.ConfiguredReportV2;bindings:readonly W.CardResultBinding[];results:ReadonlyMap<string,W.WorkspaceResultV2>;comparison:W.CardComparisonV1|null;locale:'ru'|'en'}
function indexBuckets<T extends {bucket_id:string}>(values:readonly T[]=[]):Map<string,T>{const index=new Map<string,T>();for(const value of values){if(!index.has(value.bucket_id))index.set(value.bucket_id,value);}return index;}
export function projection({definition,bindings,results,comparison:provided,legacy,locale,multiSeries}:Props){
 const selection=definition.selection;const ids=selection?.mode==='pair'?[selection.left_card_id,selection.right_card_id]:selection?[selection.card_id]:[];
 const comparison=provided&&provided.left.card_id===ids[0]&&(selection?.mode==='pair'?provided.right.card_id===ids[1]:selection?.mode==='single'&&selection.temporal!=='none')?provided:null;
 const selected=multiSeries?[...bindings]:ids.map(id=>bindings.find(b=>b.card_id===id)).filter((b):b is W.CardResultBinding=>Boolean(b));
 if(selected.length===0&&legacy){const cards=ids.map(id=>definition.worksets.flatMap(s=>s.cards).find(c=>c.card_id===id)).filter((c):c is W.Card=>Boolean(c));const temporal=selection?.mode==='single'&&selection.temporal!=='none'&&legacy.comparison;const units=cards.map(c=>c.metric_ref.metric_id==='receipt_count'?'receipt':c.metric_ref.metric_id==='average_receipt'?'EUR/receipt':'EUR');if(temporal)units.push(units[0]);return {comparisonLabel:null as string|null,comparisonMissing:false,units,names:cards.map(c=>c.metric_ref.metric_id),rows:legacy.daily.map(b=>({id:b.date,label:b.date,dates:b.date,baseline:temporal?(legacy.comparison?.daily.find(p=>p.date.slice(5)===b.date.slice(5))?.date??''):'',state:b.state,partial:false,values:[...cards.map(c=>b[c.metric_ref.metric_id]),...(temporal?[legacy.comparison?.daily.find(p=>p.date.slice(5)===b.date.slice(5))?.[cards[0].metric_ref.metric_id]??null]:[])],absolute:null,relative:null,reasons:[]}))};}
 const first=selected[0]?results.get(selected[0].result.result_id):undefined;
 const modern=first?.temporal_v2;
 if(multiSeries&&first&&(modern||first.temporal)){
  const span=(dates:readonly string[])=>dates.length?dates[0]+(dates.length>1?' — '+dates.at(-1):''):'';
  const entries=modern?modern.buckets.map((b,i)=>({id:b.current_bucket_id??'comparison-'+i,label:first.buckets?.find(bucket=>bucket.bucket_id===b.current_bucket_id)?.label??span(b.current_dates),dates:span(b.current_dates),baseline:span(b.comparison_dates),pairs:selected.map(s=>b.changes[s.bucket_projection]),state:b.changes[selected[0].bucket_projection].left_coverage.state,partial:selected.some(s=>b.changes[s.bucket_projection].left_coverage.state!=='complete'||b.changes[s.bucket_projection].right_coverage.state!=='complete')})):first.buckets.map(b=>({id:b.bucket_id,label:b.label,dates:b.effective_starts_on+' — '+b.effective_ends_on,baseline:span(first.temporal!.buckets.find(t=>t.bucket_id===b.bucket_id)?.baseline_dates??[]),pairs:selected.map(s=>first.temporal!.buckets.find(t=>t.bucket_id===b.bucket_id)?.changes[s.bucket_projection] as W.ComparisonValues|undefined),state:b.state,partial:b.is_partial_bucket}));
  return {comparisonLabel:modern?comparisonModeLabel(locale,modern.spec.settings.mode):(locale==='ru'?'Год к году':'Year over year'),comparisonMissing:false,names:selected.flatMap(s=>[s.bucket_projection,s.bucket_projection]),units:selected.flatMap(s=>[s.unit,s.unit]),rows:entries.map(b=>({id:b.id,label:b.label,dates:b.dates,baseline:b.baseline,state:b.state,partial:b.partial,values:b.pairs.flatMap(c=>[c?.left??null,c?.right??null]),absolute:b.pairs[0]?.absolute_delta??null,relative:b.pairs[0]?.relative_delta_percent??null,reasons:[...new Set(b.pairs.flatMap(c=>c?.reason_codes??[]))],comparisonPairs:b.pairs}))};
 }

 if(modern&&selected.length===1&&selection?.mode==='single'){
  const metric=selected[0].bucket_projection;
  const span=(ds:readonly string[])=>ds.length?ds[0]+(ds.length>1?' — '+ds[ds.length-1]:''):'';
  return {comparisonLabel:comparisonModeLabel(locale,modern.spec.settings.mode),comparisonMissing:false,names:[metric],units:[selected[0].unit,selected[0].unit],rows:modern.buckets.map((b,i)=>{
   const c=b.changes[metric];return {id:b.current_bucket_id??'comparison-'+i,label:first.buckets?.find(bucket=>bucket.bucket_id===b.current_bucket_id)?.label??(span(b.current_dates)||'—'),dates:span(b.current_dates),baseline:span(b.comparison_dates),state:c.left_coverage.state,partial:c.left_coverage.state!=='complete'||c.right_coverage.state!=='complete',values:[c.left,c.right],absolute:c.absolute_delta,relative:c.relative_delta_percent,reasons:c.reason_codes};
  })};
 }
 const buckets=first?.buckets??[];
 const temporal=!multiSeries&&selection?.mode==='single'&&selection.temporal!=='none'?first?.temporal:null;
 const delta=selection?.mode==='single'&&selection.display==='delta_trend';
 const comparisonMissing=selection?.mode==='pair'&&!comparison;
 const baselineRange=(dates:readonly string[])=>dates.length<2?(dates[0]??''):dates[0]+' — '+dates[dates.length-1]+' ('+dates.length+(locale==='ru'?' сопоставленных дат)':' mapped dates)');
 const comparisonBuckets=indexBuckets(comparison?.buckets);
 const temporalBuckets=indexBuckets(temporal?.buckets);
 const baselineBuckets=indexBuckets(first?.temporal?.buckets);
 const valuesByResult=new Map(selected.map(binding=>[binding.result.result_id,indexBuckets(results.get(binding.result.result_id)?.buckets)] as const));
 const rows=buckets.map(b=>{const c=comparisonBuckets.get(b.bucket_id)??(selected[0]?temporalBuckets.get(b.bucket_id)?.changes[selected[0].bucket_projection] as W.ComparisonValues|undefined:undefined);return {id:b.bucket_id,label:b.label,dates:b.effective_starts_on===b.effective_ends_on?b.effective_starts_on:`${b.effective_starts_on} — ${b.effective_ends_on}`,baseline:baselineRange(baselineBuckets.get(b.bucket_id)?.baseline_dates??[]),state:b.state,partial:b.is_partial_bucket,values:(comparison||temporal)?(delta?[c?.relative_delta_percent??null]:[c?.left??null,c?.right??null]):selected.map(binding=>valuesByResult.get(binding.result.result_id)?.get(b.bucket_id)?.values[binding.bucket_projection]??null),absolute:c?.absolute_delta??null,relative:c?.relative_delta_percent??null,reasons:c?.reason_codes??b.coverage.reason_codes};});
 const names=selected.map(b=>b.bucket_projection);
 const units=comparison?(delta?['percent']:[comparison.left.unit,comparison.right.unit]):temporal?(delta?['percent']:[selected[0].unit,selected[0].unit]):selected.map(b=>b.unit);
 return {rows,units,names,comparisonMissing,comparisonLabel:null as string|null};
}
export function WorkspacePlot(props:Props){
 const unavailable=chartCatalog.find(item=>item[0]===props.chartType)?.[3];
 const projected=useMemo(()=>projection(props),[props.definition,props.bindings,props.results,props.comparison,props.locale,props.legacy,props.multiSeries]);
 const [reducedMotion,setReducedMotion]=useState(()=>window.matchMedia('(prefers-reduced-motion: reduce)').matches);
 useEffect(()=>{const media=window.matchMedia('(prefers-reduced-motion: reduce)');const changed=()=>setReducedMotion(media.matches);media.addEventListener('change',changed);return()=>media.removeEventListener('change',changed);},[]);
 const [chartWidth,setChartWidth]=useState(600);
 const node=useRef<HTMLDivElement>(null);const instance=useRef<ReturnType<typeof echarts.init>|null>(null);
 useLayoutEffect(()=>{
  const element=node.current;if(!element)return;
  const chart=echarts.init(element,undefined,{renderer:'svg'});instance.current=chart;chart.getZr().setSleepAfterStill(1);
  const fit=()=>{
   const scroll=element.closest('.report-scroll') as HTMLElement|null;
   const focus=element.closest('.mw-focus');
   const top=element.getBoundingClientRect().top+(focus?(focus as HTMLElement).scrollTop:scroll?.scrollTop??0);
   const bottom=focus?focus.getBoundingClientRect().bottom-parseFloat(getComputedStyle(focus).paddingBottom):scroll?.getBoundingClientRect().bottom??element.ownerDocument.defaultView!.innerHeight;
   const height=props.compact?element.clientHeight:focus?Math.max(320,Math.floor(bottom-top)):Math.max(320,Math.min(520,Math.round(element.ownerDocument.defaultView!.innerHeight*.44)));
   if(!props.compact&&element.style.height!==height+'px')element.style.height=height+'px';
   setChartWidth(element.clientWidth);
   if(element.clientWidth!==chart.getWidth()||element.clientHeight!==chart.getHeight())chart.resize({animation:{duration:0}});
  };
  fit();const observer=new ResizeObserver(fit);observer.observe(element);
  const layout=element.closest('.mw-focus')??element.closest('.mw');if(layout)observer.observe(layout);
  const scroll=element.closest('.report-scroll');if(scroll)observer.observe(scroll);
  return()=>{observer.disconnect();chart.dispose();instance.current=null;};
 },[]);
 useLayoutEffect(()=>{
  const chart=instance.current;if(!chart)return;if(unavailable){chart.clear();return;}const started=performance.now();
  const {rows,units,names,comparisonMissing}=projected;const axes=units.length?[...new Set(units)]:[''];
  const theme=getComputedStyle(node.current!);const labels=metricNames[props.locale];const format=new Intl.NumberFormat(props.locale,{maximumFractionDigits:props.presentation?.visual?.decimals??2,notation:props.presentation?.visual?.compact?'compact':'standard'});const percentFormat=new Intl.NumberFormat(props.locale,{maximumFractionDigits:1});
  const temporal=Boolean(projected.comparisonLabel)||(props.definition.selection?.mode==='single'&&props.definition.selection.temporal!=='none');
  const name=(index:number)=>[labels[names[index]??names[0]],temporal?((props.multiSeries?index%2===1:index===1)?(projected.comparisonLabel??(props.locale==='ru'?'Год назад':'Prior year')):(props.locale==='ru'?'Текущий период':'Current period')):units.length>1?String(index+1):'',workspaceUnit(props.locale,units[index])].filter(Boolean).join(' · ');
  const option={animation:!reducedMotion,animationDuration:0,animationDurationUpdate:reducedMotion?0:200,animationEasingUpdate:'cubicOut',aria:{enabled:true},backgroundColor:'transparent',textStyle:{color:'#b7b8be'},legend:{show:!props.reveal,textStyle:{color:'#b7b8be'},...(props.compact?{top:'auto',bottom:0}: {})},tooltip:{trigger:'axis',renderMode:'html',confine:true,backgroundColor:'#46525b',borderWidth:0,borderRadius:8,padding:[9,12],extraCssText:'max-width:calc(100% - 16px);box-sizing:border-box;white-space:normal;box-shadow:0 8px 24px #0003;',textStyle:{color:'#f4f6f8',fontSize:13},formatter:(params:{dataIndex?:number}|{dataIndex?:number}[])=>{
   const index=(Array.isArray(params)?params[0]:params)?.dataIndex??0;const row=rows[index];if(!row)return '';
   const doc=node.current!.ownerDocument;const content=doc.createElement('div');content.className='mw-tooltip';content.style.cssText='max-width:300px;font-size:12px;line-height:1.4';
   const line=(label:string,value:string,delta?:string|null)=>{const item=doc.createElement('div');item.className='mw-tooltip-row';item.style.cssText='display:grid;grid-template-columns:auto auto;gap:12px;align-items:baseline;margin:3px 0';const caption=doc.createElement('span');caption.className='mw-tooltip-label';caption.style.cssText='text-align:left;color:#cbd1d5;overflow-wrap:anywhere';caption.textContent=label+':';const data=doc.createElement('strong');data.style.cssText='color:#f4f6f8;font-weight:600;font-variant-numeric:tabular-nums;overflow-wrap:anywhere';if(delta!=null&&Number(delta)!==0)data.style.color=Number(delta)>0?'#9ed7bd':'#f0a6a6';data.textContent=value;item.append(caption,data);content.append(item);};
   const divider=()=>{const rule=doc.createElement('hr');rule.style.cssText='border:0;border-top:1px solid #ffffff80;margin:6px 0';content.append(rule);};
   const fmt=(v:string|null|undefined,percent=false)=>v==null?'—':(percent?percentFormat:format).format(Number(v));
   line(props.locale==='ru'?'Период':'Period',row.label);
   const ru=props.locale==='ru';
   const currentIndices=row.values.map((_,i)=>i).filter(i=>!temporal||(props.multiSeries?i%2===0:i===0));const currentValues=currentIndices.map(i=>row.values[i]);
   currentValues.forEach((v,j)=>{const i=currentIndices[j];line(labels[names[i]??names[0]]??name(i),fmt(v,units[i]==='percent')+(units[i]==='percent'&&v!=null?'%':''));});
   const section=(label:string)=>{divider();const heading=doc.createElement('div');heading.textContent=label;heading.style.cssText='font-size:11px;color:#cbd1d5;margin-bottom:5px';content.append(heading);};
   const changeText=(absolute:string|null,relative:string|null)=>signed(absolute,props.locale,2)+(relative==null?' · '+(ru?'% недоступен':'% unavailable'):' ('+signed(relative,props.locale,1)+'%)');
   const previous=rows[index-1];
   if(props.presentation?.visual?.tooltip_previous!==false){section(ru?'К предыдущей точке':'Previous point');
   if(previous){
    currentValues.forEach((v,j)=>{const i=currentIndices[j];const change=adjacentChange(v,previous.values[i]);line(currentValues.length>1?(labels[names[i]??names[0]]??name(i)):previous.label,change?changeText(change.absolute,change.relative):'—',change?.absolute);});
   }else line(ru?'Изменение':'Change',ru?'Первая точка':'First point');
   }
   if(props.presentation?.visual?.tooltip_comparison!==false&&'comparisonPairs' in row&&row.comparisonPairs){section(projected.comparisonLabel??(ru?'Сравнение периодов':'Period comparison'));row.comparisonPairs.forEach((pair,i)=>{line(labels[names[i*2]??names[0]]??name(i*2),pair?changeText(pair.absolute_delta,pair.relative_delta_percent):'—',pair?.absolute_delta);});}
   else if(props.presentation?.visual?.tooltip_comparison!==false&&temporal&&(row.values[1]!=null||row.absolute!=null||row.relative!=null)){
    section(projected.comparisonLabel??(ru?'Год к году':'Year over year'));
    line(ru?'Изменение':'Change',changeText(row.absolute,row.relative),row.absolute);
   }
   if(row.reasons.length){divider();row.reasons.forEach(code=>line(props.locale==='ru'?'Состояние':'Status',workspaceReason(props.locale,code)));}return content;
  }},grid:props.compact?{left:8,right:8,bottom:32,top:28,containLabel:true}:{left:75,right:75,bottom:65,top:45},xAxis:{type:'category',data:rows.map(r=>r.label)},yAxis:axes.map((unit,i)=>({id:'axis-'+unit,axisLabel:{formatter:(value:number)=>(unit==='percent'?percentFormat:format).format(value)},...lineAxisRange(rows.flatMap(r=>r.values.filter((_,index)=>units[index]===unit)),unit==='receipt'),type:'value',scale:true,name:props.reveal?'':unit==='percent'?'Δ %':labels[names[units.findIndex(value=>value===unit)]??names[0]]??'',position:i===0?'left':'right',nameLocation:'end',nameTextStyle:{align:i===0?'left':'right'},splitLine:{lineStyle:{color:'#34353a'}}})),series:(comparisonMissing?[]:units).map((unit,i)=>({id:'metric-series-'+i+(props.reveal?JSON.stringify([props.chartType,rows.map(r=>r.values)]):''),name:name(i),type:props.chartType??'line',animationDuration:props.reveal?(props.chartType==='bar'?400:850):undefined,animationEasing:props.chartType==='bar'?'cubicOut':'linear',animationDelay:props.reveal&&props.chartType==='bar'?(index:number)=>Math.min(index*110,600):0,barMaxWidth:32,areaStyle:props.reveal?{opacity:.055}:undefined,yAxisIndex:axes.indexOf(unit),data:rows.map(r=>r.values[i]??null),connectNulls:false,markLine:i===0&&props.showDifferences&&temporal&&units.length===2&&units[0]===units[1]?{silent:true,animation:false,symbol:['circle','circle'],symbolSize:4,lineStyle:{type:'dashed',width:1.5,color:'#8f9ca4'},label:{show:true,position:'middle',rotate:0,formatter:'{b}',color:theme.getPropertyValue('--text').trim(),backgroundColor:theme.getPropertyValue('--surface').trim(),borderRadius:4,borderWidth:1,borderColor:theme.getPropertyValue('--border').trim(),padding:[4,6],fontSize:11},data:rows.filter(r=>r.values[0]!=null&&r.values[1]!=null&&r.relative!=null).map((r,index)=>[{name:signed(r.relative,props.locale,1)+'%',label:{show:index%Math.max(1,Math.ceil(rows.length/Math.max(1,Math.floor((chart.getWidth()-150)/90))))===0},coord:[r.label,Number(r.values[1])]},{coord:[r.label,Number(r.values[0])]}])}:undefined,lineStyle:{color:i===0?'#66b9d3':'#d2ac72'},itemStyle:{color:i===0?'#66b9d3':'#d2ac72'}}))} as EChartsOption;
  chart.setOption(applyChartVisual(option,props.presentation,units.map((_,i)=>(names[i]??names[0])+(temporal&&(props.multiSeries?i%2===1:i===1)?':baseline':'')),units,props.totals,props.locale,chartWidth),{replaceMerge:['series','yAxis','xAxis','dataZoom']});
  chart.getZr().flush();performance.clearMeasures('custometry.report.plot');performance.measure('custometry.report.plot',{start:started,end:performance.now()});
 },[projected,props.definition,props.locale,props.showDifferences,props.compact,props.reveal,props.chartType,props.presentation,props.totals,unavailable,reducedMotion,chartWidth]);
 return <>{unavailable&&<p role="status">{props.locale==='ru'?'Для этого типа нужны: ':'This type requires: '}{unavailable.split(' / ')[props.locale==='ru'?0:1]??unavailable}</p>}{projected.comparisonMissing&&<p role="status">{props.locale==='ru'?'Сравнение не сохранено. Примените или сохраните представление.':'Comparison is not saved. Apply or save the view.'}</p>}<div ref={node} className="mw-plot" role="img" aria-label={props.locale==='ru'?'График серверных значений. Полные данные доступны в таблице.':'Server value chart. Complete data is available in the table.'}/></>;
}
export function WorkspaceTable(props:Props){const {rows,units,names,comparisonMissing,comparisonLabel}=useMemo(()=>projection(props),[props.definition,props.bindings,props.results,props.comparison,props.locale,props.legacy,props.multiSeries]);const formatters=[new Intl.NumberFormat(props.locale,{maximumFractionDigits:0}),new Intl.NumberFormat(props.locale,{maximumFractionDigits:2}),new Intl.NumberFormat(props.locale,{maximumFractionDigits:1})];const ru=props.locale==='ru';const showDates=!props.compact&&props.definition.grain!=='day';const showState=!props.compact||rows.some(r=>r.reasons.length||r.partial||!['ready','complete'].includes(r.state));const temporal=Boolean(comparisonLabel)||(props.definition.selection?.mode==='single'&&props.definition.selection.temporal!=='none');if(props.presentation?.visual)return <ComposerVisualTable data={{rows,units,names,comparisonMissing,comparisonLabel}} presentation={props.presentation} locale={props.locale}/>;return <div className="mw-table" tabIndex={0} role="region" aria-label={ru?'Таблица результатов':'Result table'}>{comparisonMissing&&<p role="status">{ru?'Сравнение не сохранено. Примените или сохраните представление для получения проверенных значений.':'Comparison is not saved. Apply or save the view to obtain verified comparison values.'}</p>}<table aria-label={ru?'Таблица результатов':'Result table'}><thead><tr><th scope="col">{ru?'Период':'Period'}</th>{showDates&&<th scope="col">{ru?'Точные даты':'Exact dates'}</th>}{temporal&&!props.compact&&<th scope="col">{comparisonLabel??(ru?'Год назад · те же даты':'Prior year · same dates')}</th>}{units.map((u,i)=><th key={i} scope="col">{[metricNames[props.locale][names[i]??names[0]],temporal?(i===0?(ru?'Сейчас':'Current'):(comparisonLabel??(ru?'Год назад':'Prior year'))):String(i+1),workspaceUnit(props.locale,u)].filter(Boolean).join(' · ')}</th>)}{(!props.compact||temporal)&&<><th scope="col">Δ</th><th scope="col">Δ %</th></>}{showState&&<th scope="col">{ru?'Состояние / причины':'State / reasons'}</th>}</tr></thead><tbody>{rows.map(r=><tr key={r.id}><th scope="row">{r.label}</th>{showDates&&<td>{r.dates}</td>}{temporal&&!props.compact&&<td>{r.baseline||'—'}</td>}{r.values.map((v,i)=><td key={i} data-value={v??''}>{v==null?'—':formatters[units[i]==='receipt'?0:units[i]==='percent'?2:1].format(Number(v))}</td>)}{(!props.compact||temporal)&&<><td data-value={r.absolute??''}>{r.absolute==null?'—':formatters[1].format(Number(r.absolute))}</td><td data-value={r.relative??''}>{r.relative==null?'—':formatters[2].format(Number(r.relative))}</td></>}{showState&&<td>{workspaceReason(props.locale,r.state)} {r.partial?(ru?'Часть периода':'Partial bucket'):''} {r.reasons.map(code=>workspaceReason(props.locale,code)).join(', ')}</td>}</tr>)}</tbody></table>{rows.length===0&&<p>{ru?'Нет применённых данных':'No applied data'}</p>}</div>;}
