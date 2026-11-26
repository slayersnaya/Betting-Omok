# 아티팩트용 index.html에서 웹(Firebase) 버전 index.html을 만든다
import json,re,os,time
VER=time.strftime('%y%m%d.%H%M',time.gmtime(time.time()+9*3600))
src=open('/home/claude/betting-omok/index.html').read()
cfg={"apiKey":"AIzaSyDvsab_8P_Bf_Sr4OZrvFQDF7TPfKoTQck","authDomain":"betting-omok-5e0c2.firebaseapp.com","projectId":"betting-omok-5e0c2","storageBucket":"betting-omok-5e0c2.firebasestorage.app","messagingSenderId":"1058641815494","appId":"1:1058641815494:web:c32dccf8188df54b69b4c7"}
adapter=open('/home/claude/firebase/fb-adapter.js').read()
boot=("<script>window.BO_VER='"+VER+"';window.BO_FIREBASE_CONFIG="+json.dumps(cfg)+";"
 "(()=>{let res;const p=new Promise(r=>res=r);window.__BO_FB={resolve:res};window.claude={use:n=>p.then(x=>x[n]||null)}})();</script>\n"
 "<script>"+adapter+"</script>\n")
# 글꼴: 아티팩트 전용 /_blob 주소 대신 공개 CDN의 나눔스퀘어
src=re.sub(r',url\(/_blob/[0-9a-f]+\) format\("truetype"\)','',src)
# @font-face 이름(NS)은 그대로 두고, 글자 스택에만 CDN 글꼴 이름을 끼움(전에는 @font-face 이름까지 바꿔 무효가 됐음)
src=src.replace('NS,"Apple SD','NS,"NanumSquare","Apple SD')

BASE='https://slayersnaya.github.io/Betting-Omok/'
head=(# 글꼴은 한 곳에서, 화면 그리기를 막지 않게(먼저 기본 글꼴로 보이고 받아지면 바뀜)
 '<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>\n'
 '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" media="print" onload="this.media=\'all\'">\n'
 '<meta name="description" content="베팅 승자가 착수하는 2인 전략 오목. 일반 게임, 랭크전, AI 대국.">\n'
 '<meta property="og:site_name" content="베팅 오목">\n<meta property="og:locale" content="ko_KR">\n'
 '<meta property="og:title" content="베팅 오목">\n<meta property="og:description" content="베팅 승자가 착수하는 2인 전략 오목">\n'
 '<meta property="og:type" content="website">\n<meta property="og:url" content="'+BASE+'">\n'
 '<meta property="og:image" content="'+BASE+'thumb.jpg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
 '<meta property="og:image:alt" content="베팅 오목 대국 화면">\n<meta name="twitter:card" content="summary_large_image">\n'
 '<link rel="icon" href="icons/icon-192.png">\n<link rel="apple-touch-icon" href="icons/apple-180.png">\n'
 '<link rel="manifest" href="manifest.json">\n<meta name="theme-color" content="#0f1716">\n')
j=src.index('</head>');src=src[:j]+head+src[j:]
i=src.index("<script>")
out=src[:i]+boot+src[i:]
inst=open('/home/claude/firebase/web-install.js').read()
k=out.rindex('</body>');out=out[:k]+'<script>'+inst+'</script>\n'+out[k:]
os.makedirs('/home/claude/web',exist_ok=True)
open('/home/claude/web/index.html','w').write(out)
man={"id":"./","name":"베팅 오목","short_name":"베팅 오목","description":"베팅 승자가 착수하는 2인 전략 오목","lang":"ko","start_url":"./","scope":"./","display":"standalone","background_color":"#0f1716","theme_color":"#0f1716",
 "screenshots":[{"src":"shots/s1.png","sizes":"1080x1920","type":"image/png","form_factor":"narrow","label":"홈"},{"src":"shots/s2.png","sizes":"1080x1920","type":"image/png","form_factor":"narrow","label":"베팅"},{"src":"shots/s3.png","sizes":"1080x1920","type":"image/png","form_factor":"narrow","label":"개봉"},{"src":"shots/s4.png","sizes":"1080x1920","type":"image/png","form_factor":"narrow","label":"결과"}],
 "categories":["games"],"icons":[{"src":"icons/icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},{"src":"icons/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},{"src":"icons/maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]}
open('/home/claude/web/manifest.json','w').write(json.dumps(man,ensure_ascii=False,indent=1))
json.dump({'v':VER},open('/home/claude/web/version.json','w'))
# 서비스 워커: 화면 파일은 '인터넷 먼저, 안 되면 저장해 둔 것' → 업데이트는 바로, 오프라인에서도 열림
sw='''// 베팅 오목 서비스 워커 (버전 '''+VER+''')
const C='bo-'''+VER+'''';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>c.addAll(['./','index.html','manifest.json','icons/icon-192.png']).catch(()=>{})))});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);
 if(e.request.method!=='GET'||u.origin!==location.origin||u.pathname.endsWith('version.json'))return;
 e.respondWith(fetch(e.request).then(r=>{if(r.ok&&(e.request.mode==='navigate'||/\\.(png|jpg|json|html)$/.test(u.pathname))){const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp))}return r})
  .catch(()=>caches.match(e.request,{ignoreSearch:true}).then(r=>r||(e.request.mode==='navigate'&&!/privacy\\.html$/.test(u.pathname)?caches.match('index.html'):null)).then(r=>r||new Response('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><body style="margin:0;height:100vh;display:grid;place-items:center;background:#0f1716;color:#e9f0ee;font-family:sans-serif"><div style="text-align:center">인터넷에 연결되면 다시 열어 주세요<br><br><button onclick="location.reload()" style="font:inherit;padding:10px 18px;border-radius:12px;border:0;background:#009999;color:#fff">다시 시도</button></div></body>',{headers:{'Content-Type':'text/html; charset=utf-8'}}))))});
'''
open('/home/claude/web/sw.js','w').write(sw)
print('built',len(out),'ver',VER)
