window.echarts=echarts;
let innerWidth=window.innerWidth,innerHeight=window.innerHeight;window.addEventListener('resize',()=>{innerWidth=window.innerWidth;innerHeight=window.innerHeight;});
// Browser globals belong to the isolated source document, never the application shell.
const requestAnimationFrame=window.requestAnimationFrame.bind(window);
const cancelAnimationFrame=window.cancelAnimationFrame.bind(window);
const setTimeout=window.setTimeout.bind(window);
const clearTimeout=window.clearTimeout.bind(window);
const addEventListener=window.addEventListener.bind(window);
const navigator=window.navigator;
const Element=window.Element;
const HTMLElement=window.HTMLElement;
const location=new URL(bridge.url());
const history={state:null,pushState(state,_,href){this.state=state;location.href=new URL(href,location).href;bridge.urlChanged(location.href);},replaceState(state,_,href){this.state=state;location.href=new URL(href,location).href;bridge.urlChanged(location.href);},back(){location.searchParams.delete('focus');location.searchParams.delete('focus-section');bridge.urlChanged(location.href);showFocusSurface();}};
// Pilot preferences are presentation only and deliberately disappear on unmount.
const preferences=new Map();
const localStorage={getItem:key=>preferences.get(key)??null,setItem:(key,value)=>preferences.set(key,value),removeItem:key=>preferences.delete(key)};
const unavailable=()=>locale==='ru'?'Данные недоступны для этого источника':'Data unavailable for this source';
const escapeText=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const emptyOption=()=>({animation:false,title:{text:unavailable(),textStyle:{fontSize:11,color:'#999a9e'},left:'center',top:'center'},series:[]});
const unavailableTable=id=>{const node=document.getElementById(id);if(node)node.innerHTML=`<caption>${unavailable()}</caption>`;};
const realTable=()=>bridge.table(locale);
