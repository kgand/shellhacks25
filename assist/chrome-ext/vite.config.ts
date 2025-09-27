import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        sidepanel: path.resolve(__dirname, 'ui/sidepanel.html'),
        offscreen: path.resolve(__dirname, 'offscreen.html')
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]'
      }
    },
    copyPublicDir: false
  },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.')
      }
    },
    define: {
      'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development')
    }
});
