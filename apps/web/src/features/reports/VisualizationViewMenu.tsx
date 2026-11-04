import {useId,useRef,useState,type ReactNode} from 'react';

/** Native popover keeps controls in the Tab order and above the scroll surface. */
export function VisualizationViewMenu({locale,table,children}:{locale:'ru'|'en';table:boolean;children:ReactNode}){
 const id=useId();const trigger=useRef<HTMLButtonElement>(null);const menu=useRef<HTMLDivElement>(null);const [open,setOpen]=useState(false);
 const label=locale==='ru'?'Вид':'View';
 const close=()=>{menu.current?.hidePopover();trigger.current?.focus();};
 const show=()=>{
  const node=menu.current!;if(open){close();return;}
  const box=trigger.current!.getBoundingClientRect();const win=node.ownerDocument.defaultView!;
  node.showPopover();node.style.left=`${Math.max(8,Math.min(box.left,win.innerWidth-node.offsetWidth-8))}px`;
  node.style.top=`${Math.max(8,Math.min(box.bottom+6,win.innerHeight-node.offsetHeight-8))}px`;
  node.querySelector<HTMLElement>('select:not(:disabled),button:not(:disabled)')?.focus();
 };
 return <div className="mw-view-disclosure"><button ref={trigger} aria-expanded={open} aria-controls={id} onClick={show}><svg className="icon" aria-hidden="true"><use href="#i-chart-tune"/></svg>{label}</button>
  <div ref={menu} id={id} popover="auto" className="menu-popover mw-view-menu" role="group" aria-label={label} data-mode={table?'table':'chart'} onToggle={event=>setOpen(event.newState==='open')} onKeyDown={event=>{if(event.key==='Escape'){event.preventDefault();event.stopPropagation();close();}}}>
   <div className="menu-heading">{locale==='ru'?'Представление':'Presentation'}</div><div className="mw-view-presentation">{children}</div>
  </div>
 </div>;
}
