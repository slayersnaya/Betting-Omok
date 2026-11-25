// 베팅 오목: 설치용 최소 서비스 워커 (저장해 두지 않음 → 업데이트는 항상 바로 반영)
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
 if(e.request.mode!=='navigate')return;
 e.respondWith(fetch(e.request).catch(()=>new Response('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><body style="margin:0;height:100vh;display:grid;place-items:center;background:#0f1716;color:#e9f0ee;font-family:sans-serif">인터넷에 연결되면 다시 열어 주세요</body>',{headers:{'Content-Type':'text/html; charset=utf-8'}})));
});
