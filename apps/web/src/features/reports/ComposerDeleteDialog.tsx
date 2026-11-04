import {useEffect,useRef} from 'react';

export function ComposerDeleteDialog({name,locale,cancel,confirm}:{name:string;locale:'ru'|'en';cancel:()=>void;confirm:()=>void}){
 const dialog=useRef<HTMLDialogElement>(null);const ru=locale==='ru';
 useEffect(()=>{const el=dialog.current!;el.showModal();return()=>el.close();},[]);
 return <dialog ref={dialog} className="composer-delete-dialog" aria-labelledby="composer-delete-title" aria-describedby="composer-delete-description" onCancel={event=>{event.preventDefault();cancel();}}>
  <h2 id="composer-delete-title">{ru?'Удалить блок?':'Delete block?'}</h2>
  <p id="composer-delete-description">{ru?`Блок «${name}» будет удалён из отчёта. Действие можно отменить.`:`Block “${name}” will be removed from the report. You can undo this action.`}</p>
  <div><button autoFocus onClick={cancel}>{ru?'Отмена':'Cancel'}</button><button className="composer-delete-confirm" onClick={confirm}>{ru?'Удалить блок':'Delete block'}</button></div>
 </dialog>;
}
