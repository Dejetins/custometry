import {useState,useSyncExternalStore} from 'react';
import {Plus,Trash2} from 'lucide-react';
type Rule={id:string;field:string;operator:string;value:string};
type Group={id:string;logic:'and'|'or';rules:Rule[]};
type Filter={logic:'and'|'or';groups:Group[]};
const empty:Filter={logic:'and',groups:[]};
// Design-session state only: never included in report DTOs, storage or requests.
const session=new Map<string,Filter>();const listeners=new Set<()=>void>();
const subscribe=(fn:()=>void)=>{listeners.add(fn);return()=>{listeners.delete(fn);};};
const commit=(key:string,value:Filter|null)=>{if(value)session.set(key,value);else session.delete(key);listeners.forEach(fn=>fn());};
const fields=[
 ['channel','Коммуникации','Communications','Канал','Channel','enum','Розница|Онлайн|Маркетплейс','Retail|Online|Marketplace'],
 ['segment','Клиенты','Customers','Сегмент клиента','Customer segment','enum','Новые|Постоянные|Под риском','New|Returning|At risk'],
 ['city','Клиенты','Customers','Город','City','text','',''],
 ['loyalty','Клиенты','Customers','Участник программы лояльности','Loyalty member','boolean','Да|Нет','Yes|No'],
 ['amount','Заказы','Orders','Сумма заказа','Order amount','number','',''],
 ['status','Заказы','Orders','Статус заказа','Order status','enum','Оплачен|Завершён|Возврат','Paid|Completed|Returned'],
 ['date','Заказы','Orders','Дата заказа','Order date','date','',''],
 ['store','Заказы','Orders','Магазин','Store','text','',''],
 ['category','Товары','Products','Категория товара','Product category','enum','Продукты|Дом|Красота','Grocery|Home|Beauty'],
 ['sku','Товары','Products','Артикул','SKU','text','',''],
 ['coverage','Качество данных','Data quality','Покрытие','Coverage','enum','Полное|Частичное','Complete|Partial'],
] as const;
export function FilterPrototype({scopeKey,reportKey,locale,metric=false,targetKeys=[]}:{scopeKey:string;reportKey:string;locale:'ru'|'en';metric?:boolean;targetKeys?:string[]}){
 const ru=locale==='ru';const saved=useSyncExternalStore(subscribe,()=>session.get(scopeKey));const report=useSyncExternalStore(subscribe,()=>session.get(reportKey));
 const [draft,setDraft]=useState<Filter>(saved??empty);const [inherit,setInherit]=useState(metric&&!saved);const [adding,setAdding]=useState<string|null>(null);const [search,setSearch]=useState('');const [notice,setNotice]=useState('');
 const change=(next:Filter)=>{setDraft(next);setNotice('');};const data=inherit?(report??empty):draft;
 const patch=(group:string,rule:string,values:Partial<Rule>)=>change({...draft,groups:draft.groups.map(g=>g.id===group?{...g,rules:g.rules.map(r=>r.id===rule?{...r,...values}:r)}:g)});
 const addRule=(field:typeof fields[number])=>{const rule={id:crypto.randomUUID(),field:field[0],operator:'is',value:field[5]==='enum'||field[5]==='boolean'?'0':''};change({...draft,groups:adding==='new'?[...draft.groups,{id:crypto.randomUUID(),logic:'and',rules:[rule]}]:draft.groups.map(g=>g.id===adding?{...g,rules:[...g.rules,rule]}:g)});setAdding(null);setSearch('');};
 return <section className="mw-filter-prototype" aria-label={ru?'Конструктор фильтров':'Filter builder'}><header><strong>{ru?'Фильтры':'Filters'}</strong><span>{ru?'Прототип':'Prototype'}</span></header><p className="mw-filter-note">{ru?'Примерные поля и значения. Условия не влияют на расчёт, не сохраняются в отчёте и сбрасываются при перезагрузке.':'Sample fields and values. Conditions do not affect calculations or report saves and reset on reload.'}</p>
 {metric&&<label className="mw-filter-inherit"><input type="checkbox" checked={inherit} onChange={e=>{setInherit(e.target.checked);if(!e.target.checked&&!draft.groups.length)setDraft(report??empty);setNotice('');}}/>{ru?'Наследовать фильтры отчёта':'Inherit report filters'}</label>}
 <fieldset disabled={inherit}><label className="mw-filter-logic">{ru?'Между группами':'Between groups'}<select value={data.logic} onChange={e=>change({...draft,logic:e.target.value as 'and'|'or'})}><option value="and">{ru?'И — все группы':'AND — all groups'}</option><option value="or">{ru?'ИЛИ — любая группа':'OR — any group'}</option></select></label>
 {data.groups.map((g,i)=><div className="mw-filter-group" key={g.id}><header><strong>{ru?'Группа':'Group'} {i+1}</strong><select aria-label={ru?'Логика группы':'Group logic'} value={g.logic} onChange={e=>change({...draft,groups:draft.groups.map(x=>x.id===g.id?{...x,logic:e.target.value as 'and'|'or'}:x)})}><option value="and">{ru?'И':'AND'}</option><option value="or">{ru?'ИЛИ':'OR'}</option></select><button aria-label={ru?'Удалить группу':'Remove group'} onClick={()=>change({...draft,groups:draft.groups.filter(x=>x.id!==g.id)})}><Trash2 size={14}/></button></header>
 {g.rules.map(r=>{const f=fields.find(f=>f[0]===r.field)!;return <div className="mw-filter-rule" key={r.id}><div><span>{f[ru?3:4]}</span><button aria-label={ru?'Удалить условие':'Remove condition'} onClick={()=>change({...draft,groups:draft.groups.map(x=>x.id===g.id?{...x,rules:x.rules.filter(v=>v.id!==r.id)}:x).filter(x=>x.rules.length)})}>×</button></div><select aria-label={ru?'Оператор':'Operator'} value={r.operator} onChange={e=>patch(g.id,r.id,{operator:e.target.value})}><option value="is">{ru?'равно':'is'}</option><option value="not">{ru?'не равно':'is not'}</option>{(f[5]==='number'||f[5]==='date')&&<><option value="gte">{ru?'не меньше':'at least'}</option><option value="lte">{ru?'не больше':'at most'}</option></>}{f[5]==='text'&&<option value="contains">{ru?'содержит':'contains'}</option>}</select>{f[5]==='enum'||f[5]==='boolean'?<select aria-label={ru?'Значение':'Value'} value={r.value} onChange={e=>patch(g.id,r.id,{value:e.target.value})}>{f[ru?6:7].split('|').map((v,i)=><option key={i} value={i}>{v}</option>)}</select>:<input aria-label={ru?'Значение':'Value'} type={f[5]} value={r.value} onChange={e=>patch(g.id,r.id,{value:e.target.value})}/>}</div>;})}
 <button onClick={()=>{setAdding(g.id);setSearch('');}}><Plus size={14}/>{ru?'Условие':'Condition'}</button></div>)}
 {!data.groups.length&&<p>{ru?'Условий пока нет':'No conditions yet'}</p>}<button onClick={()=>{setAdding('new');setSearch('');}}><Plus size={14}/>{data.groups.length?(ru?'Добавить группу':'Add group'):(ru?'Добавить фильтр':'Add filter')}</button>
 {adding&&<div className="mw-filter-fields"><label>{ru?'Найти поле':'Find field'}<input autoFocus type="search" value={search} onChange={e=>setSearch(e.target.value)}/></label>{[...new Set(fields.map(f=>f[ru?1:2]))].map(category=><div key={category}><h4>{category}</h4>{fields.filter(f=>f[ru?1:2]===category&&f[ru?3:4].toLowerCase().includes(search.toLowerCase())).map(f=><button key={f[0]} onClick={()=>addRule(f)}>{f[ru?3:4]}</button>)}</div>)}<button onClick={()=>setAdding(null)}>{ru?'Закрыть список':'Close fields'}</button></div>}
 </fieldset><footer><button onClick={()=>{commit(scopeKey,inherit?null:draft);setNotice(ru?'Применено только в прототипе':'Applied in prototype only');}}>{ru?'Применить в прототипе':'Apply in prototype'}</button><button onClick={()=>{setDraft(saved??empty);setInherit(metric&&!saved);setAdding(null);setNotice('');}}>{ru?'Отменить условия':'Cancel conditions'}</button><button onClick={()=>{setInherit(false);change(empty);setAdding(null);}}>{ru?'Сбросить':'Reset'}</button>{targetKeys.length>1&&<button onClick={()=>{targetKeys.forEach(key=>commit(key,inherit?null:draft));setNotice((ru?'Прототип обновлён для метрик: ':'Prototype updated for metrics: ')+targetKeys.length);}}>{ru?'Для всех выбранных':'For all selected'}</button>}</footer>{notice&&<small role="status">{notice}</small>}</section>;
}
