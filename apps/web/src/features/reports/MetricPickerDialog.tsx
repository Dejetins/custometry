import {useEffect,useRef,type ReactNode} from 'react';
export function MetricPickerDialog({children,title,onClose}:{children:ReactNode;title:string;onClose:()=>void}){
 const ref=useRef<HTMLDialogElement>(null);
 useEffect(()=>{const dialog=ref.current;if(!dialog)return;const previous=dialog.ownerDocument.activeElement as HTMLElement|null;if(dialog.showModal)dialog.showModal();else dialog.setAttribute('open','');return()=>{if(dialog.close)dialog.close();previous?.focus();};},[]);
 return <dialog ref={ref} className="mw-picker-dialog" aria-label={title} onCancel={e=>{e.preventDefault();e.stopPropagation();onClose();}} onKeyDown={e=>{if(e.key==='Escape')e.stopPropagation();}} onClick={e=>{if(e.target===e.currentTarget)onClose();}}><div className="mw-picker-dialog-content"><header><h2>{title}</h2><button aria-label={/[А-Яа-я]/.test(title)?'Закрыть':'Close'} onClick={onClose}>×</button></header>{children}</div></dialog>;
}
