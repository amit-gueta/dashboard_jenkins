import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000, // Client-side port
    proxy: {
      '/api': { // Proxy API requests
        target: 'http://localhost:8000', // Your backend server
        changeOrigin: true,
      },
    },
  },
})
