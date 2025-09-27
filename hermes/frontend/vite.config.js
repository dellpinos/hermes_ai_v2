import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
    root: resolve(__dirname, 'static/src'),
    base: process.env.STATIC_URL || '/static/',
    
    build: {
        outDir: resolve(__dirname, 'static/dist'),
        manifest: true,
        emptyOutDir: true,
        assetsDir: '',
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'static/src/js/main.js'),
                styles: resolve(__dirname, 'static/src/styles/app.css')
            },
            output: {
                // To keep a clear structure
                entryFileNames: 'js/[name]-[hash].js',
                chunkFileNames: 'js/[name]-[hash].js',
                assetFileNames: (assetInfo) => {
                    if (assetInfo.name.endsWith('.css')) {
                        return 'css/[name]-[hash][extname]';
                    }
                    return 'assets/[name]-[hash][extname]';
                }
            }
        },
    },
    
    server: {
        host: 'localhost',
        port: 3000,
    },
    
    plugins: [
        // Plugin to copy static files
        {
            name: 'django-static-copy',
            apply: 'build',
            generateBundle() {
                // This is to copy files rightly
            }
        }
    ],
    
    resolve: {
        alias: {
            '@': resolve(__dirname, 'static/src'),
            '@js': resolve(__dirname, 'static/src/js'),
            '@styles': resolve(__dirname, 'static/src/styles'),
            '@img': resolve(__dirname, 'static/src/img'),
        }
    }
});