import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import { supplyInventory } from "./supply-inventory";

export default defineConfig({
  plugins: [react(), supplyInventory()],
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: false,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: "./tests/setup.ts",
  },
});
