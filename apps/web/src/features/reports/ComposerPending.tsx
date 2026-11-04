import {workspaceCopy} from './workspace-copy';

/** Loading has no speculative report layout to rearrange when metadata arrives. */
export function ComposerPending({locale,error,retry,showSignIn=true}:{locale:'ru'|'en';error?:string;retry?:()=>void;showSignIn?:boolean}){
 const c=workspaceCopy[locale];
 return <main aria-busy={!error} style={{position:'fixed',inset:0,background:'#101214',color:'#999a9e',display:'grid',placeContent:'center',gap:12,fontSize:13}}>
  <p role={error?'alert':'status'}>{error??c.loadingReport}</p>
  {retry&&<button onClick={retry}>{c.retry}</button>}
  {error&&showSignIn&&<a href="/auth/sign-in">{locale==='ru'?'Войти':'Sign in'}</a>}
 </main>;
}
