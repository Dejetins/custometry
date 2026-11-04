import {useEffect,useState} from 'react';
import {clearReportAccess,csrf} from './report-api';

/** Invalidation hints carry no authority. Every reconnect mounts fresh queries. */
export function useReportSession() {
 const [state,setState]=useState({trusted:false,epoch:0,unavailable:false});
 const [retries,setRetries]=useState(0);
 useEffect(()=>{
  let stopped=false;let source:EventSource|null=null;let timer:ReturnType<typeof setTimeout>|undefined;
  let attempt=0;let reconnecting=false;let renewed=false;
  const suspend=()=>{clearReportAccess(false,true);setState(s=>({trusted:false,epoch:s.epoch+1,unavailable:true}));};
  const connect=()=>{
   if(stopped)return;
   source=new EventSource('/api/identity/events');
   source.addEventListener('connected',()=>{attempt=0;reconnecting=false;renewed=false;setState(s=>({...s,trusted:true,unavailable:false}));});
   source.addEventListener('invalidate',()=>restart(false));
   source.addEventListener('disconnect',()=>restart(false));
   source.addEventListener('renew',()=>restart(true));
   source.onerror=()=>restart(true);
  };
  const restart=(renew:boolean)=>{
   if(stopped||reconnecting)return;reconnecting=true;
   source?.close();suspend();
   const delay=Math.min(30000,250*2**Math.min(attempt++,7));
   timer=setTimeout(()=>{void (async()=>{
    if(renew&&!renewed){try{
     const before=csrf();
     await navigator.locks.request('custometry-session-renewal',async()=>{
      if(csrf()!==before)return; // Another tab already rotated this token family.
      const response=await fetch('/api/identity/refresh',{method:'POST',credentials:'same-origin',headers:{'X-CSRF-Token':csrf()}});
      if(response.status===401||response.status===403){clearReportAccess();stopped=true;return;}
      if(!response.ok)throw Error('RENEW_UNAVAILABLE');
     });renewed=true;
    }catch{reconnecting=false;restart(true);return;}}
    if(!stopped){reconnecting=false;connect();}
   })();},delay);
  };
  const offline=()=>restart(false);window.addEventListener('offline',offline);
  connect();
  return()=>{stopped=true;source?.close();clearTimeout(timer);window.removeEventListener('offline',offline);};
 },[retries]);
 return {...state,retry:()=>setRetries(n=>n+1)};
}
