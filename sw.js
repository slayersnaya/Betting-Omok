// 베팅 오목 서비스 워커 (버전 261126.2339)
const C='bo-261126.2339';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>c.addAll(['./','index.html','manifest.json','icons/icon-192.png']).catch(()=>{})))});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);
 if(e.request.method!=='GET'||u.origin!==location.origin||u.pathname.endsWith('version.json'))return;
 e.respondWith(fetch(e.request).then(r=>{if(r.ok&&(e.request.mode==='navigate'||/\.(png|jpg|json|html)$/.test(u.pathname))){const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp))}return r})
  .catch(()=>caches.match(e.request,{ignoreSearch:true}).then(r=>r||(e.request.mode==='navigate'&&!/privacy\.html$/.test(u.pathname)?caches.match('index.html'):null)).then(r=>r||new Response('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><body style="margin:0;height:100vh;display:grid;place-items:center;background:#0f1716;color:#e9f0ee;font-family:sans-serif"><div style="text-align:center">인터넷에 연결되면 다시 열어 주세요<br><br><button onclick="location.reload()" style="font:inherit;padding:10px 18px;border-radius:12px;border:0;background:#009999;color:#fff">다시 시도</button></div></body>',{headers:{'Content-Type':'text/html; charset=utf-8'}}))))});
