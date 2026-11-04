import {useEffect,useRef,useState} from 'react';
import type {composerReports as C} from '@custometry/contracts';
import {composerApi} from './composer-api';
import {csrf} from './report-api';
import {queryKey,type Definition} from './composer-state';
import {signed} from './workspace-presentation';
import {workspaceReason,workspaceUnit} from './workspace-copy';
export type PairResult={key:string;value:C.CardComparisonV1};
export function pairKey(d:Definition,results:readonly C.ComposerResultRef[]):string {
 return JSON.stringify(d.pair?[d.pair,...[d.pair.left_block_id,d.pair.right_block_id].map(id=>{const block=d.blocks.find(b=>b.block_id===id);return [block?queryKey(d,block):null,results.find(r=>r.block_id===id)?.result_id];})]:null);
}
export function ComposerPair({definition:d,results,value,locale,readOnly,busy,commit,onCompared,onRunning}:{definition:Definition;results:readonly C.ComposerResultRef[];value?:C.CardComparisonV1;locale:'ru'|'en';readOnly:boolean;busy:boolean;commit:(d:Definition)=>void;onCompared:(r:PairResult)=>void;onRunning:(running:boolean)=>void}){
 const ru=locale==='ru',key=pairKey(d,results),current=useRef(key);current.current=key;
 const [running,setRunning]=useState(false),[error,setError]=useState(false);const request=useRef<AbortController|null>(null);
 useEffect(()=>{request.current?.abort();setRunning(false);setError(false);return()=>request.current?.abort();},[key]);
 useEffect(()=>{onRunning(running);return()=>onRunning(false);},[running,onRunning]);
 const compare=async()=>{const call=new AbortController();request.current?.abort();request.current=call;setRunning(true);setError(false);
  try{const value=await composerApi.compare({contract_version:'analytical-authoring/v1',definition:d,results},csrf(),call.signal);if(!call.signal.aborted&&current.current===key)onCompared({key,value});}
  catch{if(!call.signal.aborted&&current.current===key)setError(true);}finally{if(request.current===call)setRunning(false);}
 };
 const ready=Boolean(d.pair&&[d.pair.left_block_id,d.pair.right_block_id].every(id=>results.some(r=>r.block_id===id)));
 const labels=[ru?'Первый блок':'First block',ru?'Второй блок':'Second block'];
 const select=(side:'left_block_id'|'right_block_id',id:string)=>{const other=side==='left_block_id'?'right_block_id':'left_block_id';const otherId=d.pair?.[other]??d.blocks.find(b=>b.source&&b.block_id!==id)?.block_id;if(id&&otherId&&id!==otherId)commit({...d,pair:side==='left_block_id'?{left_block_id:id,right_block_id:otherId}:{left_block_id:otherId,right_block_id:id}});};
 const format=new Intl.NumberFormat(locale,{maximumFractionDigits:2});
 return <section className="composer-pair" aria-label={ru?'Сравнение блоков':'Block comparison'}><h2>{ru?'Сравнение двух блоков':'Compare two blocks'}</h2>
 {!readOnly&&<div className="composer-toolbar">{(['left_block_id','right_block_id'] as const).map((side,i)=><label key={side}>{labels[i]}<select aria-label={labels[i]} disabled={busy||d.blocks.filter(b=>b.source).length<2} value={d.pair?.[side]??''} onChange={e=>select(side,e.target.value)}><option value="">{ru?'Выберите блок':'Choose block'}</option>{d.blocks.filter(b=>b.source).map(b=><option key={b.block_id} value={b.block_id} disabled={d.pair?.[i===0?'right_block_id':'left_block_id']===b.block_id}>{b.presentation.title}</option>)}</select></label>)}<button disabled={!ready||busy||running} onClick={()=>void compare()}>{running?(ru?'Сравниваем…':'Comparing…'):(ru?'Сравнить блоки':'Compare blocks')}</button>{d.pair&&<button disabled={busy} onClick={()=>commit({...d,pair:null})}>{ru?'Убрать сравнение':'Remove comparison'}</button>}</div>}
 {error&&<p role="alert">{ru?'Сравнение не получено. Повторите попытку.':'Comparison failed. Try again.'}</p>}
 {d.pair&&!value&&<p role="status">{ru?'Примените оба блока и нажмите «Сравнить блоки».':'Apply both blocks, then choose Compare blocks.'}</p>}
 {value&&<><p role="status">{value.comparability_status==='comparable'?(ru?'Сопоставимые данные':'Comparable data'):value.comparability_status==='descriptive'?(ru?'Описательное сравнение':'Descriptive comparison'):(ru?'Сравнение недоступно':'Comparison unavailable')}</p><div className="mw-table" tabIndex={0} role="region" aria-label={ru?'Результат сравнения':'Comparison result'}><table><caption>{[value.left,value.right].map(s=>d.blocks.find(b=>b.block_id===s.card_id)?.presentation.title).join(' / ')}</caption><thead><tr><th scope="col">{ru?'Период':'Period'}</th>{[value.left,value.right].map((s,i)=><th scope="col" key={i}>{labels[i]} · {workspaceUnit(locale,s.unit)}</th>)}<th scope="col">Δ</th><th scope="col">Δ %</th><th scope="col">{ru?'Причины':'Reasons'}</th></tr></thead><tbody>{[{...value.totals,bucket_id:ru?'Итого':'Total'},...value.buckets].map(row=><tr key={row.bucket_id}><th scope="row">{row.bucket_id}</th>{[row.left,row.right].map((n,i)=><td key={i} data-value={n??''}>{n==null?'—':format.format(Number(n))}</td>)}<td data-value={row.absolute_delta??''}>{signed(row.absolute_delta,locale)}</td><td data-value={row.relative_delta_percent??''}>{signed(row.relative_delta_percent,locale,1)}</td><td>{row.reason_codes.map(code=>workspaceReason(locale,code)).join(', ')}</td></tr>)}</tbody></table></div></>}
 </section>;
}
