import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// base './' so the built dist works when served from any sub-path.
export default defineConfig({
  base: './',
  plugins: [react()],
  build: { chunkSizeWarningLimit: 2500, outDir: 'dist' },
  server: { port: 5174 },
});
