// Cache the app shell and local icons. News and articles come from the server.
const CACHE = 'nhl365-shell-v2';
const ASSETS = ['/manifest.webmanifest', '/static/icons/nhl365-180.png', '/static/icons/nhl365-192.png', '/static/icons/nhl365-512.png'];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await cache.add('/');
    await Promise.allSettled(ASSETS.map(path => cache.add(path)));
    await self.skipWaiting();
  })());
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(
    keys.filter(key => key.startsWith('nhl365-shell-') && key !== CACHE).map(key => caches.delete(key))
  )).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin || url.pathname.startsWith('/api/')) return;
  if (event.request.mode === 'navigate' && ['/', '/index.html'].includes(url.pathname)) {
    event.respondWith(fetch(event.request).catch(() => caches.match('/')));
    return;
  }
  if (ASSETS.includes(url.pathname + url.search)) {
    event.respondWith(caches.match(event.request).then(response => response || fetch(event.request)));
  }
});
