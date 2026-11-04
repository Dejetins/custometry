import {useRef,type ReactNode} from 'react';
// Native buttons handle keyboard activation; dragging the rail never selects a card.
export function CardRail({children}:{children:ReactNode}){
 const gesture=useRef<{x:number;y:number;scroll:number;dragged:boolean;pointer:number}|null>(null);
 return <div className="kpi-strip mw-cards" onPointerDown={e=>{
  if(e.button!==0||(e.target as Element).closest('label,input,button:not(.mw-card-select)'))return;
  if(e.pointerType==='mouse'){e.preventDefault();(e.target as HTMLElement).closest<HTMLButtonElement>('.mw-card-select')?.focus({preventScroll:true});}
  gesture.current={x:e.clientX,y:e.clientY,scroll:e.currentTarget.scrollLeft,dragged:false,pointer:e.pointerId};
 }} onPointerMove={e=>{
  const g=gesture.current;if(!g||g.pointer!==e.pointerId||!e.buttons)return;
  if(Math.abs(e.clientX-g.x)>6||Math.abs(e.clientY-g.y)>6)g.dragged=true;
  if(g.dragged&&e.pointerType==='mouse'){e.currentTarget.setPointerCapture(e.pointerId);e.currentTarget.scrollLeft=g.scroll+g.x-e.clientX;e.preventDefault();}
 }} onPointerCancel={()=>{gesture.current=null;}} onClickCapture={e=>{
  const g=gesture.current;gesture.current=null;
  if(e.detail>0&&g&&g.dragged){e.preventDefault();e.stopPropagation();}
 }}>{children}</div>;
}
