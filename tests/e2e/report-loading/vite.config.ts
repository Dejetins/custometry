import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import {balancedProxy} from './balanced-proxy';
const port=Number(process.env.W39_WEB_PORT??41739);
const target=`http://127.0.0.1:${process.env.W39_API_PORT??58139}`;
const proxy={'/api':{target,changeOrigin:false,rewrite:(path:string)=>path.replace(/^\/api/,'')},'/fixture':{target}};
export default defineConfig({plugins:[react(),...(process.env.W39_BALANCED==='1'?[balancedProxy()]:[])],preview:{host:'127.0.0.1',port,strictPort:true,proxy:process.env.W39_BALANCED==='1'?undefined:proxy},server:{host:'127.0.0.1',port,strictPort:true,proxy}});
