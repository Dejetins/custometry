import {useRef,useState,useEffect} from 'react';
import {getInstanceByDom} from 'echarts/core';
import {rowsToCsv,xlsxFor,type Rows} from './result-export';
function download(doc:Document,blob:Blob,name:string){const url=URL.createObjectURL(blob);const a=doc.createElement('a');a.href=url;a.download=name;doc.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);}
export function ResultExportMenu({table,locale,disabled}:{table:boolean;locale:'ru'|'en';disabled:boolean}){
 const ru=locale==='ru';const root=useRef<HTMLDivElement>(null);const [open,setOpen]=useState(false);const [working,setWorking]=useState(false);const [error,setError]=useState(false);const label=table?(ru?'Скачать таблицу':'Download table'):(ru?'Скачать график':'Download chart');
 useEffect(()=>{if(!open)return;const doc=root.current!.ownerDocument;const handler=(e:PointerEvent)=>{if(!root.current?.contains(e.target as Node))setOpen(false);};doc.addEventListener('pointerdown',handler);return()=>doc.removeEventListener('pointerdown',handler);},[open]);
 const allowed=useRef(!disabled);allowed.current=!disabled;
 const run=async(format:'png'|'svg'|'csv'|'xlsx')=>{if(disabled||working)return;setOpen(false);setWorking(true);setError(false);try{
  const doc=root.current!.ownerDocument;const scope=root.current!.closest('.mw-focus,.mw-result-panel')!;
  let blob:Blob;
  if(format==='csv'||format==='xlsx'){
   const tableNode=scope.querySelector('table');if(!tableNode)throw Error('NO_TABLE');
   const rows:Rows=Array.from(tableNode.rows,row=>Array.from(row.cells,cell=>{const raw=cell.getAttribute('data-value');if(raw===null)return cell.textContent??'';if(raw==='')return '';const num=Number(raw);return Number.isFinite(num)&&raw.replace(/[^0-9]/g,'').length<=15?num:raw;}));
   blob=format==='csv'?new Blob([rowsToCsv(rows)],{type:'text/csv;charset=utf-8'}):xlsxFor(rows);
  }else{
   const node=scope.querySelector<HTMLElement>('.mw-plot');const chart=node?getInstanceByDom(node):undefined;if(!chart)throw Error('NO_CHART');
   const parsed=new DOMParser().parseFromString(chart.renderToSVGString({useViewBox:true}),'image/svg+xml');const background=parsed.createElementNS('http://www.w3.org/2000/svg','rect');background.setAttribute('width','100%');background.setAttribute('height','100%');background.setAttribute('fill',getComputedStyle(node!).getPropertyValue('--surface').trim()||'#111214');parsed.documentElement.prepend(background);const svg=new XMLSerializer().serializeToString(parsed);blob=new Blob([svg],{type:'image/svg+xml;charset=utf-8'});
   if(format==='png'){
    const url=URL.createObjectURL(blob);try{const img=new Image();await new Promise<void>((resolve,reject)=>{img.onload=()=>resolve();img.onerror=()=>reject(Error('IMAGE'));img.src=url;});const canvas=doc.createElement('canvas');canvas.width=chart.getWidth()*2;canvas.height=chart.getHeight()*2;const ctx=canvas.getContext('2d');if(!ctx)throw Error('CANVAS');ctx.scale(2,2);ctx.fillStyle=getComputedStyle(node!).getPropertyValue('--surface').trim()||'#111214';ctx.fillRect(0,0,chart.getWidth(),chart.getHeight());ctx.drawImage(img,0,0,chart.getWidth(),chart.getHeight());blob=await new Promise<Blob>((resolve,reject)=>canvas.toBlob(value=>value?resolve(value):reject(Error('PNG')),'image/png'));}finally{URL.revokeObjectURL(url);}
   }
  }
  if(!allowed.current||!root.current?.isConnected)return;
  download(doc,blob,`custometry-${table?'table':'chart'}.${format}`);
 }catch{setError(true);}finally{setWorking(false);root.current?.querySelector('button')?.focus();}};
 return <div className="mw-export-menu" ref={root} onKeyDown={e=>{if(e.key==='Escape'){e.stopPropagation();setOpen(false);root.current?.querySelector('button')?.focus();}}}><button className="mw-export-trigger" aria-label={label} title={label} aria-expanded={open} disabled={disabled||working} onClick={()=>setOpen(!open)}><svg className="icon" aria-hidden="true"><use href="#i-download"/></svg></button>{open&&<div className="mw-export-options" role="group" aria-label={label}>{(table?['xlsx','csv']:['png','svg']).map(format=><button key={format} onClick={()=>void run(format as 'png'|'svg'|'csv'|'xlsx')}>{format==='xlsx'?'Excel':format==='png'?'PNG · 2×':format.toUpperCase()}</button>)}</div>}{error&&<span role="alert">{ru?'Не удалось скачать файл. Повторите попытку.':'Download failed. Try again.'}</span>}</div>;
}
