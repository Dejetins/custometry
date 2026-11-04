import {useEffect,useRef,type ReactNode} from 'react';

function positionMenu(el:HTMLDetailsElement){
 if(!el.open)return;
 const menu=el.querySelector<HTMLElement>(':scope > div')!;const view=el.ownerDocument.defaultView!;
 const rect=el.querySelector('summary')!.getBoundingClientRect();
 menu.style.left=`${Math.max(8,Math.min(rect.left,view.innerWidth-menu.offsetWidth-8))}px`;
 menu.style.top=`${Math.max(8,Math.min(rect.bottom+6,view.innerHeight-menu.offsetHeight-8))}px`;
}

/** One contextual disclosure at a time, scoped to the mounted report document. */
export function ComposerBlockMenu({className,label,children,accessibleLabel}:{className:string;label:string;children:ReactNode;accessibleLabel?:string}){
 const ref=useRef<HTMLDetailsElement>(null);
 useEffect(()=>{
  const el=ref.current!;const doc=el.ownerDocument;const view=doc.defaultView!;
  const close=(restore=false)=>{if(!el.open)return;el.open=false;if(restore)el.querySelector('summary')?.focus();};
  const outside=(e:Event)=>{if(!el.contains(e.target as Node))close();};
  const escape=(e:KeyboardEvent)=>{if(el.open&&e.key==='Escape'){e.preventDefault();close(true);}};
  const scroll=(e:Event)=>{if(!el.querySelector(':scope > div')?.contains(e.target as Node))positionMenu(el);};
  const resize=()=>positionMenu(el);
  doc.addEventListener('pointerdown',outside,true);doc.addEventListener('focusin',outside,true);
  doc.addEventListener('keydown',escape);doc.addEventListener('scroll',scroll,true);view.addEventListener('resize',resize);
  return()=>{doc.removeEventListener('pointerdown',outside,true);doc.removeEventListener('focusin',outside,true);doc.removeEventListener('keydown',escape);doc.removeEventListener('scroll',scroll,true);view.removeEventListener('resize',resize);};
 },[]);
 return <details ref={ref} className={`composer-layout-menu ${className}`} onClick={e=>{
  const el=e.currentTarget;const target=e.target as HTMLElement;
  if(target.closest('summary')){
   const scope=el.closest('.composer')??el.ownerDocument;
   scope.querySelectorAll<HTMLDetailsElement>('.composer-layout-menu[open]').forEach(other=>{if(other!==el)other.open=false;});
  }else if(target.closest('button')&&!target.closest('[data-menu-keep-open]')){
   const restore=el.contains(el.ownerDocument.activeElement);el.open=false;
   if(restore)el.querySelector('summary')?.focus();
  }
 }} onToggle={e=>positionMenu(e.currentTarget)}><summary aria-label={accessibleLabel}>{label}</summary><div>{children}</div></details>;
}
