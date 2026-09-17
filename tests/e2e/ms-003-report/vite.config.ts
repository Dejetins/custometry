import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({plugins:[react()],server:{host:'127.0.0.1',port:41734,strictPort:true,proxy:{'/api':{target:'http://127.0.0.1:58104',changeOrigin:false,rewrite:(path)=>path.replace(/^\/api/,'')}}}});
