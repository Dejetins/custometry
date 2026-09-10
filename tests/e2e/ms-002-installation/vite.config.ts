import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
export default defineConfig({
  plugins: [react()],
  server: { proxy: {
    "/api": { target: "http://127.0.0.1:8000", changeOrigin: false, rewrite: path => path.replace(/^\/api/, "") },
    "/docs": { target: "http://127.0.0.1:8835", changeOrigin: false, rewrite: path => path.replace(/^\/docs/, "") },
  } },
});
