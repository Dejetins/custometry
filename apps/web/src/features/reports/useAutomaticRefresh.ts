import {useEffect,useRef,useState} from 'react';
export function useAutomaticRefresh(key:string,enabled:boolean,pending:boolean,run:()=>void){
 const latest=useRef(run);latest.current=run;const attempted=useRef<string|null>(null);
 useEffect(()=>{if(!enabled){attempted.current=null;return;}if(pending||attempted.current===key)return;const timer=setTimeout(()=>{attempted.current=key;latest.current();},150);return()=>clearTimeout(timer);},[key,enabled,pending]);
}
export function useDelayedBusy(busy:boolean,delay=400){
 const [visible,setVisible]=useState(false);
 useEffect(()=>{if(!busy){setVisible(false);return;}const timer=setTimeout(()=>setVisible(true),delay);return()=>clearTimeout(timer);},[busy,delay]);
 return busy&&visible;
}
