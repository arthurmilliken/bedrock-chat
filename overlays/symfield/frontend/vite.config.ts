// @ts-nocheck
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

// https://vitejs.dev/config/
export default defineConfig({
  resolve: { alias: { './runtimeConfig': './runtimeConfig.browser' } },
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      devOptions: {
        enabled: true,
      },
      injectRegister: 'auto',
      workbox: {
        maximumFileSizeToCacheInBytes: 3 * 1024 * 1024,
      },
      manifest: {
        name: 'Symfield Chat',
        short_name: 'Symfield Chat',
        description: 'AWS-native chatbot using Bedrock',
        start_url: '/index.html',
        display: 'standalone',
        theme_color: '#232F3E',
        icons: [
          {
            src: '/images/symfield_icon_72.png',
            sizes: '72x72',
            type: 'image/png',
          },
          {
            src: '/images/symfield_icon_96.png',
            sizes: '96x96',
            type: 'image/png',
          },
          {
            src: '/images/symfield_icon_128.png',
            sizes: '128x128',
            type: 'image/png',
          },
          {
            src: '/images/symfield_icon_144.png',
            sizes: '144x144',
            type: 'image/png',
          },
          {
            src: '/images/symfield_icon_152.png',
            sizes: '152x152',
            type: 'image/png',
          },
          {
            src: '/images/symfield_icon_192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: '/images/symfield_icon_384.png',
            sizes: '384x384',
            type: 'image/png',
          },
          {
            src: '/images/symfield_icon_512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable',
          },
          {
            src: '/images/symfield_icon_512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any',
          },
        ],
      },
    }),
  ],
  server: { host: true },
});
