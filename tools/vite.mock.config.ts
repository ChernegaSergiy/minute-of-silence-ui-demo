import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
export default defineConfig({
  plugins: [react()],
  base: "./",
  build: { outDir: "dist-mock", emptyOutDir: true, rollupOptions: { input: "index.mock.html", output: { inlineDynamicImports: true } } },
});
