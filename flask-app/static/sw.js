const CACHE = 'bc-v2';
const ASSETS = [
  'index.html','breaches.html','breach.html','stats.html',
  'assets/css/style.css',
  'assets/js/api.js','assets/js/ui.js','assets/js/hash.js','assets/js/theme.js','assets/js/i18n.js',
  'assets/js/main.js','assets/js/breaches.js','assets/js/breach.js','assets/js/stats.js',
  'assets/img/logo.svg','assets/img/hero.svg','manifest.webmanifest'
];
self.addEventListener('install', e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)));
});
self.addEventListener('activate', e=>{
  e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))));
});
self.addEventListener('fetch', e=>{
  const {request} = e; if(request.method!=='GET') return;
  e.respondWith(
    caches.match(request).then(cached=>{
      const fetcher = fetch(request).then(res=>{
        caches.open(CACHE).then(c=>c.put(request, res.clone()));
        return res;
      }).catch(()=>cached);
      return cached || fetcher;
    })
  );
});
