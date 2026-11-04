import {useEffect,useState,type DragEvent} from 'react';
import type {Definition} from './composer-state';
import {structure,node,nodes,identity,parent,ancestors,isLocked,isHidden,orderedPages,type Target,type Kind,type Command} from './composer-structure';

export function ComposerStructure({definition:d,activePage,activate,commit,locale,readOnly,busy,snapshot,undo,redo,canUndo,canRedo}:{definition:Definition;activePage:string;activate:(id:string)=>void;commit:(d:Definition)=>void;locale:'ru'|'en';readOnly:boolean;busy:boolean;snapshot?:string;undo:()=>void;redo:()=>void;canUndo:boolean;canRedo:boolean}){
 const t=(en:string,ru:string)=>locale==='ru'?ru:en;
 const kindLabel=(kind:Kind)=>({chapter:t('chapter','глава'),page:t('page','страница'),section:t('section','секция'),block:t('block','блок')})[kind];
 const [search,setSearch]=useState(''),[selected,setSelected]=useState<Target>({kind:'page',id:activePage});
 const [name,setName]=useState(''),[newName,setNewName]=useState(''),[kind,setKind]=useState<'chapter'|'page'|'section'>('page'),[destination,setDestination]=useState('');
 const [position,setPosition]=useState({column:1,span:6,row:1,row_span:1});
 const [drag,setDrag]=useState<Target|null>(null),[drop,setDrop]=useState<{id:string;valid:boolean}|null>(null),[error,setError]=useState('');
 const exists=nodes(d,selected.kind).some(n=>identity(n)===selected.id);const target:Target=exists?selected:{kind:'page',id:activePage};const current=node(d,target);
 useEffect(()=>{setSelected({kind:'page',id:activePage});},[activePage]);
 useEffect(()=>{setName('block_id'in current?current.presentation.title:current.title);setDestination('');if('block_id'in current){const p=current.placement;setPosition({column:(p?.column??0)+1,span:p?.span??6,row:(p?.row??0)+1,row_span:p?.row_span??1});}},[current]);
 const locked=isLocked(d,target),ancestorLocked=isLocked(d,target,false);
 const run=(command:Command)=>{if(readOnly||busy)return;try{const next=structure(d,command);commit(next);setError('');if(!next.pages.some(p=>p.page_id===activePage))activate(next.default_page_id);}catch{setError(t('This change is unavailable. Check locks, destination and grid overlap.','Изменение недоступно. Проверьте блокировки, размещение и пересечение блоков.'));}};
 const pages=orderedPages(d).filter(p=>!readOnly||!isHidden(d,{kind:'page',id:p.page_id}));
 const filtered=pages.filter(p=>p.title.toLocaleLowerCase(locale).includes(search.toLocaleLowerCase(locale)));
 const all=(['chapter','page','section','block'] as const).flatMap(k=>nodes(d,k).map(n=>({target:{kind:k,id:identity(n)},value:n})));
 const label=(value:typeof current)=>'block_id'in value?value.presentation.title:value.title;
 const destinationKinds:Kind[]=target.kind==='page'?['chapter']:target.kind==='section'?['page','section']:target.kind==='block'?['section']:[];
 const destinations=all.filter(v=>destinationKinds.includes(v.target.kind)&&v.target.id!==target.id&&!ancestors(d,v.target).some(a=>a.id===target.id)&&!isLocked(d,v.target));
 const dropCommand=(at:Target):Command|null=>{
  if(!drag||drag.id===at.id)return null;
  if(drag.kind===at.kind)return {type:'move',target:drag,parent:parent(d,at),before:at.id};
  if(drag.kind==='page'&&at.kind==='chapter'||drag.kind==='section'&&['page','section'].includes(at.kind)||drag.kind==='block'&&at.kind==='section')return {type:'move',target:drag,parent:at};
  return null;
 };
 const dragProps=(at:Target)=>({
  draggable:!readOnly&&!busy&&!isLocked(d,at),
  onDragStart:(e:DragEvent)=>{e.stopPropagation();if(readOnly||busy||isLocked(d,at)){e.preventDefault();return;}setDrag(at);e.dataTransfer.effectAllowed='move';e.dataTransfer.setData('text/plain',at.id);},
  onDragEnd:()=>{setDrag(null);setDrop(null);},
  onDragOver:(e:DragEvent)=>{if(readOnly||busy)return;const command=dropCommand(at);let valid=false;if(command)try{structure(d,command);valid=true;}catch{/* Invalid destinations remain unavailable. */}e.preventDefault();e.stopPropagation();e.dataTransfer.dropEffect=valid?'move':'none';setDrop(old=>old?.id===at.id&&old.valid===valid?old:{id:at.id,valid});},
  onDrop:(e:DragEvent)=>{e.preventDefault();e.stopPropagation();const command=dropCommand(at);if(command)run(command);setDrag(null);setDrop(null);},
  'data-drop-state':drop?.id===at.id?(drop.valid?'valid':'invalid'):undefined,
 });
 return <div className="composer-structure">
 <nav aria-label={t('Document pages','Страницы документа')}>
 {pages.length>1&&<label>{t('Find page','Найти страницу')}<input type="search" value={search} onChange={e=>setSearch(e.target.value)}/></label>}
 <div className="composer-pages" role="tablist" aria-label={t('Pages','Страницы')}>
 {filtered.map(p=><button key={p.page_id} className="report-tab" role="tab" id={`page-tab-${p.page_id}`} aria-controls={`page-panel-${p.page_id}`} aria-selected={activePage===p.page_id} tabIndex={activePage===p.page_id||!filtered.some(page=>page.page_id===activePage)&&filtered[0]?.page_id===p.page_id?0:-1} {...dragProps({kind:'page',id:p.page_id})} onClick={()=>activate(p.page_id)} onKeyDown={e=>{const at=filtered.findIndex(x=>x.page_id===p.page_id);const to=e.key==='ArrowRight'?(at+1)%filtered.length:e.key==='ArrowLeft'?(at+filtered.length-1)%filtered.length:e.key==='Home'?0:e.key==='End'?filtered.length-1:-1;if(to>=0){e.preventDefault();activate(filtered[to].page_id);const document=e.currentTarget.ownerDocument;requestAnimationFrame(()=>document.getElementById(`page-tab-${filtered[to].page_id}`)?.focus());}}}>
 {p.chapter_id?<small>{d.chapters?.find(c=>c.chapter_id===p.chapter_id)?.title} · </small>:null}{p.title}{isHidden(d,{kind:'page',id:p.page_id})?t(' (hidden)',' (скрыта)'):''}{isLocked(d,{kind:'page',id:p.page_id})?' 🔒':''}</button>)}
 </div>{pages.length>1&&<label>{t('All pages','Все страницы')}<select aria-label={t('All pages','Все страницы')} value={activePage} onChange={e=>activate(e.target.value)}>{pages.map(p=><option key={p.page_id} value={p.page_id}>{p.chapter_id?`${d.chapters?.find(c=>c.chapter_id===p.chapter_id)?.title} · `:''}{p.title}</option>)}</select></label>}
 {!filtered.length&&<p>{t('No matching pages','Страницы не найдены')}</p>}
 </nav>
 {!readOnly&&<details className="composer-outline"><summary>{t('Document structure','Структура документа')}</summary>
 <div className="composer-toolbar"><button disabled={busy||!canUndo} onClick={undo}>{t('Undo','Отменить')}</button><button disabled={busy||!canRedo} onClick={redo}>{t('Redo','Повторить')}</button><small>{t('Undo keeps the last 50 authoring changes until Save.','До сохранения доступны последние 50 изменений.')}</small></div>
 <label>{t('Presentation profile','Профиль представления')}<select aria-label={t('Presentation profile','Профиль представления')} disabled={busy} value={d.profile} onChange={e=>run({type:'profile',profile:e.target.value as Definition['profile']})}><option value="dashboard">{t('Dashboard','Дашборд')}</option><option value="workbook_report">{t('Workbook report','Многостраничный отчёт')}</option><option value="narrative_research">{t('Research outline','Исследование: структура')}</option></select></label>
 <label>{t('Selected item','Выбранный элемент')}<select aria-label={t('Selected item','Выбранный элемент')} value={`${target.kind}:${target.id}`} onChange={e=>{const [kind,id]=e.target.value.split(':');setSelected({kind:kind as Kind,id});}}>{all.map(({target:t,value})=><option key={t.id} value={`${t.kind}:${t.id}`}>{'— '.repeat(ancestors(d,t).length)}{kindLabel(t.kind)}: {label(value)}</option>)}</select></label>
 <div className="composer-outline-list" aria-label={t('Outline drag targets','Элементы структуры для переноса')}>{all.filter(v=>v.target.kind==='chapter'||v.target.kind==='page'||ancestors(d,v.target).some(a=>a.kind==='page'&&a.id===activePage)).map(v=><button key={v.target.id} {...dragProps(v.target)} disabled={busy} aria-pressed={target.id===v.target.id} onClick={()=>setSelected(v.target)} style={{marginInlineStart:ancestors(d,v.target).length*12}}>{label(v.value)}</button>)}</div>
 <p role="status">{drop?t(drop.valid?'Drop to move here':'This destination is unavailable',drop.valid?'Отпустите для перемещения':'Размещение недоступно'):''}</p>
 <div className="composer-structure-fields">
 <label>{t('Item title','Название элемента')}<input disabled={busy||locked} maxLength={200} value={name} onChange={e=>setName(e.target.value)}/></label><button disabled={busy||locked||!name.trim()} onClick={()=>run({type:'rename',target,title:name})}>{t('Rename','Переименовать')}</button>
 <button disabled={busy||locked} onClick={()=>run({type:'reorder',target,direction:-1})}>{t('Move up','Выше')}</button><button disabled={busy||locked} onClick={()=>run({type:'reorder',target,direction:1})}>{t('Move down','Ниже')}</button>
 <button disabled={busy||locked} onClick={()=>run({type:'duplicate',target,snapshot})}>{t('Duplicate item','Дублировать элемент')}</button><button disabled={busy||locked} onClick={()=>run({type:'delete',target})}>{t('Delete item','Удалить элемент')}</button>
 <button disabled={busy||locked} onClick={()=>run({type:'flag',target,flag:'hidden',value:!current.hidden})}>{current.hidden?t('Show item','Показать элемент'):t('Hide item','Скрыть элемент')}</button>
 <button disabled={busy||ancestorLocked} onClick={()=>run({type:'flag',target,flag:'locked',value:!current.locked})}>{current.locked?t('Unlock item','Разблокировать элемент'):t('Lock item','Заблокировать элемент')}</button>
 {target.kind!=='chapter'&&<><label>{t('Move to / group','Переместить / сгруппировать')}<select aria-label={t('Move to / group','Переместить / сгруппировать')} disabled={busy||locked} value={destination} onChange={e=>setDestination(e.target.value)}><option value="">{t('Choose destination','Выберите размещение')}</option>{target.kind==='page'&&<option value="none">{t('No chapter','Без главы')}</option>}{destinations.map(v=><option key={v.target.id} value={`${v.target.kind}:${v.target.id}`}>{kindLabel(v.target.kind)}: {label(v.value)}</option>)}</select></label><button disabled={busy||locked||!destination} onClick={()=>{const [kind,id]=destination.split(':');run({type:'move',target,parent:destination==='none'?null:{kind:kind as Kind,id}});}}>{t('Move item','Переместить элемент')}</button></>}
 {target.kind==='page'&&'layout'in current&&<label>{t('Page layout','Раскладка страницы')}<select aria-label={t('Page layout','Раскладка страницы')} disabled={busy||locked} value={current.layout} onChange={e=>run({type:'layout',page:target.id,layout:e.target.value as 'flow'|'dashboard_grid'|'narrative'})}><option value="dashboard_grid">{t('Dashboard grid','Сетка дашборда')}</option><option value="flow">{t('Table-first flow','Поток с таблицами')}</option><option value="narrative">{t('Narrative','Повествование')}</option></select></label>}
 {'block_id'in current&&<><label>{t('Density','Плотность')}<select aria-label={t('Density','Плотность')} disabled={busy||locked} value={current.presentation.density??'comfortable'} onChange={e=>run({type:'density',block:target.id,density:e.target.value as 'compact'|'comfortable'|'spacious'})}><option value="compact">{t('Compact','Компактно')}</option><option value="comfortable">{t('Comfortable','Обычно')}</option><option value="spacious">{t('Spacious','Просторно')}</option></select></label>{current.placement&&<fieldset disabled={busy||locked}><legend>{t('Grid position and size','Позиция и размер в сетке')}</legend>{(['column','row','span','row_span'] as const).map((key,index)=><label key={key}>{[t('Column','Колонка'),t('Row','Строка'),t('Column span','Ширина в колонках'),t('Row span','Высота в строках')][index]}<input type="number" min={1} max={key==='column'||key==='span'?(d.grid_columns??12):undefined} value={position[key]} onChange={e=>setPosition(old=>({...old,[key]:Number(e.target.value)}))}/></label>)}<button onClick={()=>run({type:'placement',block:target.id,placement:{...position,column:position.column-1,row:position.row-1}})}>{t('Update layout','Изменить раскладку')}</button></fieldset>}</>}
 </div>
 <form className="composer-structure-fields" onSubmit={e=>{e.preventDefault();const p=kind==='page'?(target.kind==='chapter'?target:undefined):kind==='section'?(target.kind==='section'||target.kind==='page'?target:{kind:'page' as const,id:activePage}):undefined;run({type:'add',kind,title:newName,parent:p});setNewName('');}}><label>{t('New item type','Тип нового элемента')}<select aria-label={t('New item type','Тип нового элемента')} disabled={busy} value={kind} onChange={e=>setKind(e.target.value as typeof kind)}><option value="chapter">{t('Chapter','Глава')}</option><option value="page">{t('Page','Страница')}</option><option value="section">{t('Section','Секция')}</option></select></label><label>{t('New item title','Название нового элемента')}<input disabled={busy} required maxLength={200} value={newName} onChange={e=>setNewName(e.target.value)}/></label><button disabled={busy||!newName.trim()}>{t('Add item','Добавить элемент')}</button></form>
 </details>}
 {error&&<p role="alert">{error}</p>}
 </div>;
}
