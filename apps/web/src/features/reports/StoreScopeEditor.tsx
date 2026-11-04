import {useEffect,useState,type ComponentProps} from 'react';
import {StoreScopePicker} from './StoreScopePicker';
export function StoreScopeEditor(props:ComponentProps<typeof StoreScopePicker>){
 const [draft,setDraft]=useState(props.value);useEffect(()=>setDraft(props.value),[props.value]);const changed=JSON.stringify(draft)!==JSON.stringify(props.value);const ru=props.locale==='ru';
 return <div><StoreScopePicker {...props} value={draft} onChange={setDraft}/>{changed&&<div className="mw-toolbar"><button disabled={props.disabled} onClick={()=>props.onChange(draft===null?null:[...draft])}>{ru?'Показать результат':'Show results'}</button><button onClick={()=>setDraft(props.value)}>{ru?'Отмена':'Cancel'}</button></div>}</div>;
}
