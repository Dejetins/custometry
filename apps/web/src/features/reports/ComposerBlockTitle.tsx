import {useId,useRef,useState} from 'react';
import {createPortal} from 'react-dom';
import {Info} from 'lucide-react';
import type {composerReports as C} from '@custometry/contracts';
export function ComposerBlockTitle({presentation:p}:{presentation:C.BlockPresentation}){
 const id=useId(),button=useRef<HTMLButtonElement>(null);
 const [open,setOpen]=useState(false),[position,setPosition]=useState({left:0,top:0});
 const show=()=>{const el=button.current;if(!el)return;const r=el.getBoundingClientRect();setPosition({left:Math.max(8,Math.min(r.left,(el.ownerDocument.defaultView?.innerWidth??1000)-276)),top:r.bottom+6});setOpen(true);};
 return <span className="composer-block-title">{p.show_title!==false&&<span title={p.title}>{p.title}</span>}{p.description?.trim()&&<><button ref={button} className="composer-info composer-no-drag" aria-label={p.description} aria-describedby={open?id:undefined} aria-expanded={open} onMouseEnter={show} onMouseLeave={()=>{if(button.current?.ownerDocument.activeElement!==button.current)setOpen(false);}} onFocus={show} onBlur={()=>setOpen(false)} onClick={e=>{e.stopPropagation();show();}} onKeyDown={e=>{if(e.key==='Escape'){e.stopPropagation();setOpen(false);}}}><Info size={14}/></button>{open&&button.current&&createPortal(<span id={id} role="tooltip" className="composer-description-tooltip" style={{position:'fixed',...position,zIndex:10000,maxWidth:260,padding:10,background:'#46525b',color:'#f4f6f8',borderRadius:8,fontSize:12,lineHeight:1.5,whiteSpace:'normal',overflowWrap:'anywhere'}}>{p.description}</span>,button.current.ownerDocument.body)}</>}</span>;
}
