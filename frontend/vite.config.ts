import path from "node:path";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
      // Ejemplos JSON del contrato de API, usados por los mocks (MSW)
      "@contracts": path.resolve(__dirname, "../contracts"),
    },
  },
  server: {
    port: 5173,
    fs: { allow: [".."] },
    // El backend corre en :8000 (Django). Evita CORS en desarrollo.
    proxy: { "/api": "http://localhost:8000" },
  },
});
