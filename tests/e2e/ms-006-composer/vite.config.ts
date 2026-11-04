import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({plugins:[react()],server:{host:'127.0.0.1',port:Number(process.env.COMPOSER_WEB_PORT??41747),strictPort:true,proxy:{'/api':{target:`http://127.0.0.1:${process.env.COMPOSER_API_PORT??58147}`,changeOrigin:false,rewrite:path=>path.replace(/^\/api/,'')},'/fixture':{target:`http://127.0.0.1:${process.env.COMPOSER_API_PORT??58147}`}}}});
