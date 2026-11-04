import {useEffect,useId,useRef,useState,type ReactNode} from 'react';

/** A disclosure of secondary actions; native buttons retain standard Tab navigation. */
export function ReportActionsMenu({label,children}:{label:string;children:ReactNode}){
 const id=useId();
 const [open,setOpen]=useState(false);
 const root=useRef<HTMLDivElement>(null);
 const trigger=useRef<HTMLButtonElement>(null);
 useEffect(()=>{
  if(!open)return;
  const doc=root.current!.ownerDocument;
  const outside=(event:PointerEvent)=>{if(!root.current?.contains(event.target as Node))setOpen(false);};
  doc.addEventListener('pointerdown',outside);
  return()=>doc.removeEventListener('pointerdown',outside);
 },[open]);
 return <div className="mw-report-menu" ref={root} onKeyDown={event=>{if(event.key==='Escape'&&open){event.preventDefault();setOpen(false);trigger.current?.focus();}}} onBlur={event=>{if(!event.currentTarget.contains(event.relatedTarget as Node))setOpen(false);}}>
  <button ref={trigger} title={label} aria-label={label} aria-expanded={open} aria-controls={open?id:undefined} onClick={()=>setOpen(!open)}><svg className="icon" aria-hidden="true" viewBox="0 0 24 24"><circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/></svg></button>
  {open&&<div id={id} className="mw-report-menu-items" role="group" aria-label={label} onClick={event=>{if((event.target as HTMLElement).closest('button:not(:disabled)')){setOpen(false);trigger.current?.focus();}}}>{children}</div>}
 </div>;
}
