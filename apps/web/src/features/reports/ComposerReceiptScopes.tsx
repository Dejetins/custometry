import {useEffect,useRef,useState} from 'react';
import type {composerReports as C} from '@custometry/contracts';
import type {FilterInput} from './receipt-filter-tree';
import {composerApi} from './composer-api';
import {csrf} from './report-api';
import {ReceiptFilterEditor,describeFilter} from './ReceiptFilterEditor';
import {receiptScopes} from './composer-scope-state';

type Props={definition:C.ComposerDefinitionV1;target:C.ScopeTarget;dataset:string;locale:'ru'|'en';busy:boolean;onValidating:(token:string,active:boolean)=>void;commit:(d:C.ComposerDefinitionV1)=>void;label:(t:C.ScopeTarget)=>string|undefined};
export function ComposerReceiptScopes(props:Props){
 const {definition:d,target,locale,busy,commit}=props;
 const t=(en:string,ru:string)=>locale==='ru'?ru:en;
 const local=receiptScopes(d).filter(f=>f.target.id===target.id);
 const [selected,setSelected]=useState(local[0]?.binding_id??''),[message,setMessage]=useState(''),[formBusy,setFormBusy]=useState(false);
 const binding=local.find(f=>f.binding_id===selected);
 return <section className="composer-receipt-scopes" aria-label={t('Receipt scope','Область чеков')}>
 <h3>{t('Receipt conditions at this scope','Условия чеков в этой области')}</h3>
 <label>{t('Receipt constraint','Условие чеков')}<select aria-label={t('Receipt constraint','Условие чеков')} disabled={busy||formBusy} value={selected} onChange={e=>{setSelected(e.target.value);setMessage('');}}><option value="">{t('New constraint','Новое условие')}</option>{local.map(f=><option key={f.binding_id} value={f.binding_id}>{describeFilter(f.filter.expression,[],locale)}{f.locked?' 🔒':''}</option>)}</select></label>
 <ReceiptScopeForm key={JSON.stringify(binding??null)} {...props} binding={binding} onBusy={setFormBusy} setMessage={setMessage} onCommit={(next,id)=>{commit(next);setSelected(id);setMessage(t('Receipt scope updated. Apply affected blocks to calculate.','Область чеков обновлена. Для расчёта примените затронутые блоки.'));}}/>
 <p role="status">{message}</p></section>;
}

function ReceiptScopeForm({definition:d,target,dataset,locale,busy,onValidating,label,binding,onBusy,setMessage,onCommit}:Props&{binding?:C.ReceiptScopeBinding;onBusy:(busy:boolean)=>void;setMessage:(message:string)=>void;onCommit:(d:C.ComposerDefinitionV1,id:string)=>void}){
 const t=(en:string,ru:string)=>locale==='ru'?ru:en;
 const receipts=receiptScopes(d);
 const [value,setValue]=useState<FilterInput|null>(binding?.filter??null);
 const [locked,setLocked]=useState(binding?.locked??false),[replaceable,setReplaceable]=useState(binding?.replaceable??false),[replaces,setReplaces]=useState(binding?.replaces?.[0]??''),[links,setLinks]=useState<readonly string[]>(binding?.linked_target_block_ids??[]);
 const [previewing,setPreviewing]=useState(false),[pending,setPending]=useState(false);
 const controller=useRef<AbortController|null>(null),current=useRef(d);current.current=d;
 const [token]=useState(()=>crypto.randomUUID());
 useEffect(()=>()=>{controller.current?.abort();onValidating(token,false);},[onValidating,token]);
 useEffect(()=>{onBusy(pending||previewing);return()=>onBusy(false);},[pending,previewing,onBusy]);
 const readonly=busy||pending||Boolean(binding?.locked);
 async function apply(){
  if(readonly||previewing||!dataset)return;
  const nextBinding:C.ReceiptScopeBinding|undefined=value?{binding_id:binding?.binding_id??crypto.randomUUID(),target,semantic_dataset_version_id:dataset,filter:value,
   order:binding?.order??1+Math.max(-1,...[...(d.scopes?.filters??[]),...receipts].filter(f=>f.target.id===target.id).map(f=>f.order)),
   locked,replaceable:locked?false:replaceable,combine_mode:replaces?'replace_allowed_parent_field':'intersect',replaces:replaces?[replaces]:[],linked_target_block_ids:links}:undefined;
  const next:C.ComposerDefinitionV1={...d,scopes:{...d.scopes,schema_version:'composer-scopes/v2',filters:d.scopes?.filters??[],contexts:d.scopes?.contexts??[],receipt_filters:[...receipts.filter(f=>f.binding_id!==binding?.binding_id),...(nextBinding?[nextBinding]:[])]}};
  controller.current?.abort();const call=new AbortController();controller.current=call;setPending(true);onValidating(token,true);setMessage('');
  try{await composerApi.validate(next,csrf(),call.signal);if(!call.signal.aborted&&current.current===d){onCommit(next,nextBinding?.binding_id??'');}}
  catch{if(!call.signal.aborted)setMessage(t('Scope validation failed. Check source, field replacement, locks and links.','Область не прошла проверку. Проверьте источник, заменяемое поле, блокировки и связи.'));}
  finally{if(controller.current===call){setPending(false);onValidating(token,false);}}
 }
 return <>
 <fieldset disabled={readonly}><legend>{t('Draft scope settings','Черновик настроек области')}</legend>
 <ReceiptFilterEditor dataset={dataset} value={value} locale={locale} onChange={setValue} onPending={setPreviewing} disabled={readonly} target="scope"/>
 <label><input type="checkbox" checked={locked} onChange={e=>setLocked(e.target.checked)}/>{t('Lock receipt constraint after Save','Заблокировать условие чеков после сохранения')}</label>
 <label><input type="checkbox" checked={replaceable&&!locked} disabled={locked} onChange={e=>setReplaceable(e.target.checked)}/>{t('Allow child replacement of the same Receipt field','Разрешить дочернюю замену того же поля чека')}</label>
 <label>{t('Replace parent Receipt constraint','Заменить родительское условие чеков')}<select aria-label={t('Replace parent Receipt constraint','Заменить родительское условие чеков')} value={replaces} onChange={e=>{setReplaces(e.target.value);setLinks([]);}}><option value="">{t('Intersect parents','Пересечение с родительскими условиями')}</option>{receipts.filter(f=>f.replaceable&&!f.locked&&f.target.id!==target.id).map(f=><option key={f.binding_id} value={f.binding_id}>{label(f.target)}: {describeFilter(f.filter.expression,[],locale)}</option>)}</select></label>
 <fieldset disabled={Boolean(replaces)}><legend>{t('Also apply Receipt condition to blocks','Также применить условие чеков к блокам')}</legend>{d.blocks.filter(b=>b.block_id!==target.id).map(b=><label key={b.block_id}><input type="checkbox" checked={links.includes(b.block_id)} onChange={e=>setLinks(old=>e.target.checked?[...old,b.block_id]:old.filter(id=>id!==b.block_id))}/>{b.presentation.title}</label>)}</fieldset>
 <button type="button" disabled={readonly||previewing||!dataset} onClick={()=>void apply()}>{t('Update Receipt scope','Обновить область чеков')}</button>
 </fieldset>{binding?.locked&&<p>{t('Saved locked constraint; it cannot be removed or weakened.','Сохранённое заблокированное условие нельзя удалить или ослабить.')}</p>}
 </>;
}
