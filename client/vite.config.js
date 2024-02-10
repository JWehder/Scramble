import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
/// <reference types="vitest" />
/// <reference types="vite/client" />

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    css: true,
    setupFiles: './src/test/setup.js'
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5555',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      }
    }
  },
})
