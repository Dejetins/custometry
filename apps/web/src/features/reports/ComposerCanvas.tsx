import {useLayoutEffect,useRef,useState,type CSSProperties,type ReactNode} from 'react';
import GridLayout,{type Layout} from 'react-grid-layout';
import {SlidersHorizontal,Paintbrush,Copy,Trash2} from 'lucide-react';
import type {composerReports as C} from '@custometry/contracts';
import {canvasLayout,canvasGeometry,commitCanvas} from './composer-canvas';
import {isLocked} from './composer-structure';
import type {Definition} from './composer-state';
import gridStyles from 'react-grid-layout/css/styles.css?raw';
import resizeStyles from 'react-resizable/css/styles.css?raw';
export function ComposerCanvas({definition:d,section,blocks,selected,select,readOnly,busy,locale,commit,copy,remove,render}:{definition:Definition;section:string;blocks:readonly C.ComposerBlock[];selected:string|null;select:(id:string,tab?:'data'|'visual')=>void;readOnly:boolean;busy:boolean;locale:'ru'|'en';commit:(d:Definition)=>void;copy:(id:string)=>void;remove:(id:string)=>void;render:(b:C.ComposerBlock)=>ReactNode}){
 const host=useRef<HTMLDivElement>(null);const moved=useRef(false);const releaseSelection=useRef<()=>void>(()=>{});const [width,setWidth]=useState(0),[gesture,setGesture]=useState(false),[error,setError]=useState('');
 useLayoutEffect(()=>{const el=host.current;if(!el)return;const observer=new ResizeObserver(()=>setWidth(el.clientWidth));observer.observe(el);setWidth(el.clientWidth);return()=>observer.disconnect();},[]);
 // Reveal the selected card without moving focus out of its settings or animating the grid.
 useLayoutEffect(()=>{
  if(readOnly||!selected||!width||gesture)return;
  const frame=requestAnimationFrame(()=>{
   const card=Array.from(host.current?.querySelectorAll<HTMLElement>('[data-block-id]')??[]).find(el=>el.dataset.blockId===selected);
   const viewport=host.current?.closest('#report-scroll');if(!card||!viewport)return;
   const bounds=viewport.getBoundingClientRect(),rect=card.getBoundingClientRect();
   const canvas=host.current!,canvasBounds=canvas.getBoundingClientRect();
   const horizontal=rect.left<canvasBounds.left?rect.left-canvasBounds.left:rect.right>canvasBounds.right?rect.right-canvasBounds.right:0;
   if(horizontal)canvas.scrollBy({left:horizontal,behavior:'instant'});
   const delta=rect.top<bounds.top+12?rect.top-bounds.top-12:rect.bottom>bounds.bottom-12?Math.min(rect.top-bounds.top-12,rect.bottom-bounds.bottom+12):0;
   if(delta)viewport.scrollBy({top:delta,behavior:'instant'});
  });return()=>cancelAnimationFrame(frame);
 },[selected,width,readOnly,blocks.find(b=>b.block_id===selected)?.placement?.span]);
 const grid=d.pages.find(p=>p.page_id===d.sections.find(s=>s.section_id===section)?.page_id)?.layout==='dashboard_grid';
 useLayoutEffect(()=>()=>releaseSelection.current(),[]);
 const start=()=>{
  moved.current=false;releaseSelection.current();
  const doc=host.current?.ownerDocument;if(!doc)return;
  const preventSelection=(event:Event)=>event.preventDefault();
  doc.getSelection()?.removeAllRanges();doc.body.classList.add('composer-pointer-active');
  doc.addEventListener('selectstart',preventSelection);
  const release=()=>{
   doc.body.classList.remove('composer-pointer-active');doc.removeEventListener('selectstart',preventSelection);
   for(const event of ['mouseup','touchend','touchcancel','pointercancel'])doc.removeEventListener(event,release);
   doc.defaultView?.removeEventListener('blur',release);
  };
  releaseSelection.current=release;
  for(const event of ['mouseup','touchend','touchcancel','pointercancel'])doc.addEventListener(event,release);
  doc.defaultView?.addEventListener('blur',release);
 };
 const move=()=>{moved.current=true;setGesture(true);};
 const geometry=canvasGeometry(blocks,width);
 const stop=(layout:Layout[])=>{releaseSelection.current();setGesture(false);if(!moved.current)return;moved.current=false;try{commit(commitCanvas(d,section,layout));setError('');}catch{setError(locale==='ru'?'Позиция недоступна: проверьте блокировки.':'Position unavailable: check locks.');}};
 const wrapper=(b:C.ComposerBlock)=><article key={b.block_id} data-block-id={b.block_id} aria-label={b.presentation.title} className={`composer-block composer-canvas-block composer-${b.block_type}`} data-compact-metric={b.block_type==='metric'&&(b.placement?.row_span??3)<=2} data-selected={!readOnly&&selected===b.block_id} data-targeted={!readOnly&&d.blocks.find(v=>v.block_id===selected)?.control?.target_block_ids.includes(b.block_id)} onClick={()=>{if(!readOnly&&!gesture)select(b.block_id);}}>
 {!readOnly&&<div className="composer-block-tools"><button disabled={busy} aria-label={`${locale==='ru'?'Настроить':'Settings'}: ${b.presentation.title}`} onClick={e=>{e.stopPropagation();select(b.block_id,'data');}}><SlidersHorizontal size={15}/></button><button disabled={busy} aria-label={`${locale==='ru'?'Визуализация':'Visualization'}: ${b.presentation.title}`} onClick={e=>{e.stopPropagation();select(b.block_id,'visual');}}><Paintbrush size={15}/></button><button disabled={busy||isLocked(d,{kind:'block',id:b.block_id})} title={locale==='ru'?'Дублировать блок':'Duplicate block'} aria-label={`${locale==='ru'?'Дублировать блок':'Duplicate block'}: ${b.presentation.title}`} onClick={e=>{e.stopPropagation();copy(b.block_id);}}><Copy size={15}/></button><button disabled={busy||isLocked(d,{kind:'block',id:b.block_id})} title={locale==='ru'?'Удалить блок':'Delete block'} aria-label={`${locale==='ru'?'Удалить блок':'Delete block'}: ${b.presentation.title}`} onClick={e=>{e.stopPropagation();remove(b.block_id);}}><Trash2 size={15}/></button></div>}{render(b)}</article>;
 return <div ref={host} className={`composer-canvas ${gesture?'is-dragging':''}`}><style>{gridStyles+resizeStyles}</style>{width>0&&(grid?<GridLayout width={geometry.width} cols={24} rowHeight={geometry.rowHeight} margin={[6,6]} containerPadding={[0,0]} layout={canvasLayout(d,section,geometry.width).filter(l=>blocks.some(b=>b.block_id===l.i))} isDraggable={!readOnly&&!busy&&width>=600} isResizable={!readOnly&&!busy&&width>=600} draggableCancel='input,textarea,select,option,button,a,label,summary,[contenteditable="true"],[role="button"],[role="slider"],[role="combobox"],.composer-no-drag' compactType={null} preventCollision onDragStart={start} onResizeStart={start} onDrag={move} onResize={move} onDragStop={stop} onResizeStop={stop} style={{'--grid-row':`${geometry.rowHeight}px`,'--grid-step':`${geometry.rowHeight+6}px`} as CSSProperties}>{blocks.map(wrapper)}</GridLayout>:<div className="composer-flow">{blocks.map(wrapper)}</div>)}{error&&<p role="alert">{error}</p>}</div>;
}
