import type {ReactNode} from 'react';
import type {composerReports as C} from '@custometry/contracts';
import {makeCount,type CountCatalog} from './receipt-filter-tree';
type Operand=C.ScopedCount|C.CountRatio;
type Expr=C.AggregateReceiptFilterInput['expression'];
export const countLabel=(c:C.ScopedCount,locale:'ru'|'en')=>c.definition.kind==='count'?(locale==='ru'?'Наблюдаемые позиции':'Observed items'):(locale==='ru'?'Разные наблюдаемые товары':'Distinct observed products');
export const operandUnit=(v:Operand)=>'numerator' in v?'ratio':v.definition.unit;
export function describeOperand(value:Operand,locale:'ru'|'en',describe:(n:Expr)=>string):string {
 if('numerator' in value)return `${describeOperand(value.numerator,locale,describe)} / ${describeOperand(value.denominator,locale,describe)}`;
 return `${countLabel(value,locale)} [${value.window.starts_at.slice(0,10)}, ${value.window.ends_at.slice(0,10)}) UTC (${describe(value.predicate)})`;
}
export function AggregateFilterEditor({node,catalog,locale,change,remove,renderRows}:{node:C.AggregateCompare;catalog:CountCatalog;locale:'ru'|'en';change:(v:C.AggregateCompare)=>void;remove:()=>void;renderRows:(count:C.ScopedCount,change:(v:Expr)=>void)=>ReactNode}){
 const ru=locale==='ru';
 function fresh(){const target='numerator' in node.left?node.left.numerator.definition:node.left.definition;return makeCount(catalog,node.scope_id,catalog.counts.find(c=>c.definition.version_id===target.version_id));}
 function ratio(base?:C.ScopedCount):C.CountRatio {const numerator=base??fresh();const selected=catalog.counts.find(c=>c.definition.version_id===numerator.definition.version_id);return {kind:'count_ratio',numerator,denominator:makeCount(catalog,node.scope_id,selected),unit:'ratio',zero_denominator_policy:'unknown'};}
 function left(v:Operand){change({...node,left:v,right:'value' in node.right?{...node.right,unit:operandUnit(v)}:node.right});}
 function Count({value,onChange,label}:{value:C.ScopedCount;onChange:(v:C.ScopedCount)=>void;label:string}){
  return <fieldset className="receipt-filter-count"><legend>{label}</legend><label>{ru?'Счётчик':'Count definition'}<select aria-label={`${label} ${ru?'счётчик':'count definition'}`} value={value.definition.version_id} onChange={e=>{const selected=catalog.counts.find(c=>c.definition.version_id===e.target.value);if(selected)onChange({...value,definition:selected.definition,window:{...value.window,observation_as_of:selected.observation.observation_as_of,knowledge_as_of:selected.observation.knowledge_as_of}});}}>{catalog.counts.map(c=><option key={c.definition.version_id} value={c.definition.version_id}>{c.label[locale]}</option>)}</select></label>
   <label>{ru?'Начало окна включительно':'Observation start (inclusive)'}<input aria-label={`${label} ${ru?'начало окна':'observation start'}`} type="date" value={value.window.starts_at.slice(0,10)} onChange={e=>onChange({...value,window:{...value.window,starts_at:`${e.target.value}T00:00:00Z`}})}/></label>
   <label>{ru?'Конец окна не включается':'Observation end (exclusive)'}<input aria-label={`${label} ${ru?'конец окна':'observation end'}`} type="date" value={value.window.ends_at.slice(0,10)} onChange={e=>onChange({...value,window:{...value.window,ends_at:`${e.target.value}T00:00:00Z`}})}/></label>
   <p>{ru?'Дата родительского чека · UTC. Учитываются все наблюдаемые строки, подходящие под условия ниже. Неизвестные свойства сохраняют неизвестный результат. Ноль допустим только для полного пустого набора.':'Parent receipt date · UTC. Counts all observed rows matching the conditions below. Unavailable properties remain unknown. Zero requires a complete empty set.'}</p>
   <p>{ru?'Снимок данных':'Data snapshot'}: {value.window.knowledge_as_of}</p>
   {renderRows(value,predicate=>onChange({...value,predicate}))}
  </fieldset>;
 }
 function OperandEditor({value,onChange,label}:{value:Operand;onChange:(v:Operand)=>void;label:string}){
  const isRatio='numerator' in value;
  return <fieldset><legend>{label}</legend><label>{ru?'Способ расчёта':'Calculation'}<select aria-label={`${label} ${ru?'способ расчёта':'calculation'}`} value={isRatio?'ratio':'count'} onChange={e=>onChange(e.target.value==='ratio'?ratio(isRatio?value.numerator:value):isRatio?value.numerator:value)}><option value="count">{ru?'Количество':'Count'}</option><option value="ratio">{ru?'Отношение двух счётчиков':'Ratio of two counts'}</option></select></label>
   {isRatio?<>{Count({value:value.numerator,label:`${label} ${ru?'числитель':'numerator'}`,onChange:numerator=>onChange({...value,numerator})})}{Count({value:value.denominator,label:`${label} ${ru?'знаменатель':'denominator'}`,onChange:denominator=>onChange({...value,denominator})})}<p>{ru?'Нулевой или неизвестный знаменатель даёт неизвестный результат. Единицы двух счётчиков должны совпадать.':'Zero or unknown denominator gives an unknown result. Both counts must use the same unit.'}</p></>:Count({value,label,onChange})}
  </fieldset>;
 }
 return <fieldset className="receipt-filter-aggregate"><legend>{ru?'Условие по количеству':'Count condition'}</legend><p>{ru?'История позиций неполная. Точное количество и соответствие этому условию могут остаться неизвестными.':'Item history is incomplete. The exact count and membership may remain unknown.'}</p>
  {OperandEditor({value:node.left,label:ru?'Слева':'Left',onChange:left})}
  <label>{ru?'Сравнение счётчиков':'Count comparison'}<select aria-label={ru?'Сравнение счётчиков':'Count comparison'} value={node.operator} onChange={e=>change({...node,operator:e.target.value as C.AggregateCompare['operator']})}>{(['eq','ne','lt','le','gt','ge'] as const).map((op,i)=><option key={op} value={op}>{(ru?['равно','не равно','меньше','не больше','больше','не меньше']:['equals','does not equal','less than','at most','greater than','at least'])[i]}</option>)}</select></label>
  <label>{ru?'Сравнить с':'Compare with'}<select aria-label={ru?'Сравнить с':'Compare with'} value={'value' in node.right?'scalar':'scoped'} onChange={e=>change({...node,right:e.target.value==='scalar'?{kind:'scalar',value:'1',unit:operandUnit(node.left)}:operandUnit(node.left)==='ratio'?ratio():fresh()})}><option value="scalar">{ru?'Значением':'A value'}</option><option value="scoped">{ru?'Другим окном или счётчиком':'Another window or count'}</option></select></label>
  {'value' in node.right?<label>{ru?'Порог':'Threshold'}<input aria-label={ru?'Порог':'Threshold'} inputMode="decimal" value={node.right.value} onChange={e=>change({...node,right:{kind:'scalar',unit:operandUnit(node.left),value:e.target.value}})}/><span>{operandUnit(node.left)==='ratio'?(ru?'Доля':'Ratio'):countLabel(node.left as C.ScopedCount,locale)}</span></label>:OperandEditor({value:node.right,label:ru?'Справа':'Right',onChange:right=>change({...node,right})})}
  <button type="button" onClick={remove}>{ru?'Удалить условие по количеству':'Remove count condition'}</button>
 </fieldset>;
}
