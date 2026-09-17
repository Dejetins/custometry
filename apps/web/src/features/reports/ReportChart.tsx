import { useEffect, useRef, useState } from 'react';
import { init, use as useECharts } from 'echarts/core';
import { LineChart } from 'echarts/charts';
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components';
import { SVGRenderer } from 'echarts/renderers';
import { compileLineChart } from '@custometry/chart-compiler';
import type { Actor, References, Result } from './report-api';
import type { Copy } from './copy';
useECharts([LineChart, GridComponent, TooltipComponent, LegendComponent, SVGRenderer]);

export function canonicalJson(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(',')}]`;
  if (value !== null && typeof value === 'object') return `{${Object.keys(value).sort().map((k) => `${JSON.stringify(k)}:${canonicalJson((value as Record<string, unknown>)[k])}`).join(',')}}`;
  return JSON.stringify(value);
}
export async function checkReferences(refs: References): Promise<void> {
  for (const obj of [refs.chart_spec, refs.brand_profile, refs.company_pack]) {
    const bytes = new TextEncoder().encode(canonicalJson(obj.payload));
    const hash = [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map((b) => b.toString(16).padStart(2,'0')).join('');
    if (hash !== obj.reference.content_hash) throw new Error('REFERENCE_HASH_MISMATCH');
  }
  if (canonicalJson(refs.company_pack.payload.brand_profile) !== canonicalJson(refs.brand_profile.reference) || refs.brand_profile.payload.remote_assets.length) throw new Error('REFERENCE_MISMATCH');
}
export function ReportChart({result, refs, actor, locale, copy, size}: {result: Result; refs: References; actor: Actor; locale:'ru'|'en'; copy: Copy; size:'small'|'medium'|'large'}) {
  const element = useRef<HTMLDivElement>(null);
  const [error, setError] = useState(false);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    let cancelled = false;
    let chart: ReturnType<typeof init> | undefined;
    let observer: ResizeObserver | undefined;
    setError(false); setReady(false);
    void checkReferences(refs).then(() => {
      if (cancelled || !element.current) return;
      const token = (name: string) => {
        const entry = refs.brand_profile.payload.tokens.find((t) => t.name === name);
        const color = (entry?.values as Record<string,string> | undefined)?.graphite;
        if (!color) throw new Error('MISSING_COLOR_ROLE');
        return color;
      };
      const metric = result.metrics[0];
      if (!refs.company_pack.payload.metric_versions.some((m) => m.version_id === metric.version_id && m.content_hash === metric.content_hash)) throw new Error('METRIC_REFERENCE_MISMATCH');
      const compiled = compileLineChart(refs.chart_spec.payload, {
        workspaceId: actor.workspace_id, ownerPrincipalId: actor.principal_id, policyHash: result.policy_hash,
        artifactId:String(result.manifest.artifact_id), artifactHash:String(result.manifest.content_hash), parameters:result.parameters,
        metricVersionId:String(metric.version_id), metricHash:String(metric.content_hash), daily:result.daily, comparison:result.comparison?.daily ?? null,
      }, {locale,primary:token('color/data/series-primary'),comparison:token('color/data/series-comparison'),text:token('color/text/default'),grid:token('color/border/subtle')});
      // The owner-selected pilot is the Web presentation profile. Persisted
      // result/spec/default references above remain verified and unchanged.
      const pilot = getComputedStyle(element.current.closest('.report-pilot')!);
      const primary = pilot.getPropertyValue('--accent').trim();
      const comparison = '#a8b3ba';
      const muted = pilot.getPropertyValue('--text-muted').trim();
      const axisSize = Math.round(10 * (size==='small'?0.85:size==='large'?1.2:1));
      const option = {
        ...compiled.option,
        textStyle: {fontFamily:'Inter, system-ui, sans-serif',color:muted,fontSize:11},
        grid: {left:46,right:24,top:8,bottom:38,containLabel:true},
        legend: {show:false},
        xAxis: {...compiled.option.xAxis,axisLine:{lineStyle:{color:'#34353a'}},axisTick:{show:false},axisLabel:{color:muted,fontSize:axisSize,margin:8}},
        yAxis: {...compiled.option.yAxis,name:'',axisLine:{show:false},axisTick:{show:false},axisLabel:{color:muted,fontSize:axisSize,margin:8},splitLine:{lineStyle:{color:'#292a2e'}}},
        series: compiled.option.series.map((series,index)=>({...series,lineStyle:{...series.lineStyle,width:2,color:index===0?primary:comparison},itemStyle:{color:index===0?primary:comparison}})),
      };
      chart = init(element.current, undefined, {renderer:'svg'});
      chart.setOption(option);
      observer = new ResizeObserver(() => chart?.resize()); observer.observe(element.current);
      setReady(true);
    }).catch(() => { if (!cancelled) setError(true); });
    return () => {cancelled=true; observer?.disconnect(); chart?.dispose();};
  }, [result, refs, actor, locale, size]);
  const series = [{label:copy.current,value:result.totals.net_revenue,color:'#66b9d3'},...(result.comparison?[{label:copy.prior,value:result.comparison.totals.net_revenue,color:'#a8b3ba'}]:[])];
  return <div className="chart-stage has-series-panel-right report-chart-stage" data-presentation-profile="target-pilot/b54b8b77">
    <div className="report-chart"><h4 className="report-chart-title">{copy.net_revenue} · EUR</h4><div className="report-plot" ref={element} role="img" aria-label={`${copy.net_revenue} · EUR`} data-chart-ready={ready}/>{error&&<p role="alert">{copy.unavailable}</p>}</div>
    <aside className="adaptive-legend-host series-panel" aria-label={locale==='ru'?'Серии':'Series'}><header className="series-panel-header"><strong className="series-panel-title">{locale==='ru'?'Серии':'Series'}</strong><span className="series-panel-count">{series.length}/{series.length}</span></header><div className="series-panel-body"><div className="adaptive-legend"><div className="adaptive-legend-row"><span className="adaptive-legend-row-label">{locale==='ru'?'Серии':'Series'}</span><div className="adaptive-legend-items">{series.map(s=><div className="adaptive-legend-item" key={s.label}><span className="adaptive-legend-swatch" style={{background:s.color}}/><span className="adaptive-legend-item-label">{s.label}</span><span className="adaptive-legend-item-value">{s.value===null?'—':new Intl.NumberFormat(locale,{maximumFractionDigits:2}).format(Number(s.value))}</span></div>)}</div></div></div></div></aside>
  </div>;
}
