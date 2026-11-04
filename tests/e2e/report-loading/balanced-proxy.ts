import {request} from 'node:http';
import type {Plugin} from 'vite';

/** Diagnostic local proxy: least outstanding RPCs, independently spread SSE. */
export function balancedProxy():Plugin {
 const workers=Number(process.env.W39_BALANCED_WORKERS??8);
 if(![8,16].includes(workers))throw Error('W39_BALANCED_WORKERS_REQUIRED');
 const active=Array(workers).fill(0) as number[];let events=0;let requests=0;
 return {name:'w39-diagnostic-balanced-proxy',configurePreviewServer(server){
  server.middlewares.use((req,res,next)=>{
   if(!req.url?.startsWith('/api/'))return next();
   const event=req.url.startsWith('/api/identity/events');
   const first=requests++%workers;
   const index=event?events++%workers:Array.from({length:workers},(_,n)=>(first+n)%workers).find(n=>active[n]===Math.min(...active))!;
   if(!event)active[index]++;
   let released=false;
   const release=()=>{if(!released){released=true;if(!event)active[index]--;}};
   res.once('finish',release);res.once('close',release);
   const upstream=request({host:'127.0.0.1',port:58160+index,path:req.url.slice(4),method:req.method,headers:req.headers},incoming=>{
    res.writeHead(incoming.statusCode??502,incoming.headers);incoming.pipe(res);
   });
   upstream.on('error',()=>{if(!res.headersSent){res.statusCode=503;res.end('Diagnostic upstream unavailable');}else res.destroy();});
   req.once('aborted',()=>upstream.destroy());res.once('close',()=>upstream.destroy());
   req.pipe(upstream);
  });
 }};
}
