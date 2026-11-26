// 웹으로 열었을 때 앱 설치를 최대한 쉽게 (설치된 앱으로 열면 아무것도 안 함)
// 1) 카카오톡·네이버 등 앱 안 브라우저 → 알아서 크롬(아이폰은 사파리)으로 열어 줌(세션마다 한 번)
// 2) 크롬·삼성 인터넷 → 설치 창(버튼 한 번)을 홈 화면에 띄움. 브라우저 규칙상 마지막 '설치' 한 번은 사람이 눌러야 함
// 3) 아이폰 사파리 → 공유 버튼 위치를 가리키는 안내(자동 설치는 아이폰이 허용하지 않음)
(()=>{
 const ua=navigator.userAgent||'',standalone=matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
 if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js').catch(()=>{});
 if(standalone)return;
 const isIOS=/iPhone|iPad|iPod/i.test(ua)||(/Macintosh/.test(ua)&&navigator.maxTouchPoints>1),isAnd=/Android/i.test(ua),isPad=/iPad/i.test(ua)||(/Macintosh/.test(ua)&&navigator.maxTouchPoints>1);
 const isKakao=/KAKAOTALK/i.test(ua),inApp=isKakao||/NAVER\(inapp|Instagram|FBAN|FBAV|Line\/|DaumApps|everytimeApp|; wv\)/i.test(ua);
 const isSafari=isIOS&&!inApp&&/Safari/i.test(ua)&&!/CriOS|FxiOS|EdgiOS|OPiOS|Whale/i.test(ua);
 const K='bo-inst-x',KS='bo-inst-s';let ev=null;
 const ls=(k,v)=>{try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}};
 const hidden=()=>Date.now()-(+ls(K)||0)<3*864e5,sheetSeen=()=>Date.now()-(+ls(KS)||0)<3*864e5;
 // 앱 안 브라우저에서 넘어온 경우(inst=1)는 설치하려는 흐름으로 보고 바로 설치 창을 띄움
 let want=false;try{const u=new URL(location.href);want=u.searchParams.get('inst')==='1';if(want){u.searchParams.delete('inst');history.replaceState(history.state,'',u.pathname+u.search+u.hash)}}catch(e){}
 const target=()=>{try{const u=new URL(location.href);u.searchParams.set('inst','1');return u.toString()}catch(e){return location.href}};
 const toOut=()=>{const t=target();location.href=isKakao?'kakaotalk://web/openExternal?url='+encodeURIComponent(t):'intent://'+t.replace(/^https?:\/\//,'')+'#Intent;scheme=https;package=com.android.chrome;S.browser_fallback_url='+encodeURIComponent(t)+';end'};
 const css=document.createElement('style');css.textContent=`
 .instcard{display:flex;align-items:center;gap:12px;margin-bottom:12px;padding:12px 10px 12px 14px}
 .instcard img{width:44px;height:44px;border-radius:12px;flex:none}
 .instcard .it{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
 .instcard .it b{font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
 .instcard .it span{font-size:12.5px;color:var(--mute);text-wrap:pretty;word-break:keep-all}
 .instcard .btn{flex:none}
 @media (max-width:340px){.instcard img{display:none}.instcard .it span{white-space:nowrap}}
 .instcard .ibtn{width:44px;height:44px;margin-left:-6px;margin-right:-4px}
 .instcard .ibtn svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round}
 #instSheet{position:fixed;inset:0;z-index:60;display:flex;align-items:flex-end;justify-content:center;background:rgba(0,0,0,.5);animation:isFade .2s ease-out}
 #instSheet .box{width:min(440px,100%);margin:0 10px calc(10px + env(safe-area-inset-bottom));background:var(--card);color:var(--ink);border-radius:22px;padding:20px 18px 16px;box-shadow:0 12px 40px rgba(0,0,0,.35);animation:isUp .28s cubic-bezier(.2,.8,.2,1)}
 #instSheet .hd{display:flex;align-items:center;gap:14px;margin-bottom:12px}
 #instSheet .hd img{width:56px;height:56px;border-radius:14px;flex:none}
 #instSheet h2{margin:0;font-size:18px}#instSheet .hd p{margin:3px 0 0;font-size:13px;color:var(--mute);font-weight:700}
 #instSheet ul{margin:0 0 14px;padding:0;list-style:none;display:grid;gap:6px;font-size:14px;font-weight:700}
 #instSheet li{display:flex;align-items:center;gap:8px;white-space:nowrap}#instSheet li i{width:6px;height:6px;border-radius:50%;background:var(--jade);flex:none}
 #instSheet .row{display:grid;grid-template-columns:1fr 2fr;gap:8px}#instSheet .btn{min-height:50px;font-size:16px}
 #instSheet .ios{display:grid;gap:8px;margin:0 0 14px;font-size:14px;font-weight:700}
 #instSheet .ios div{display:flex;align-items:center;gap:10px;white-space:nowrap}#instSheet .ios b{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:50%;background:var(--jade);color:#fff;font-size:13px;flex:none}
 #instSheet .ios svg{width:22px;height:22px;fill:none;stroke:#2f7df6;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
 #instArrow{position:fixed;left:50%;bottom:calc(6px + env(safe-area-inset-bottom));z-index:61;transform:translateX(-50%);width:36px;height:36px;color:#fff;animation:isBob 1s ease-in-out infinite;pointer-events:none}
 #instArrow.pad{left:auto;right:84px;bottom:auto;top:6px;transform:rotate(180deg)}
 #instSheet.iosw .box{margin-bottom:calc(54px + env(safe-area-inset-bottom))}#instSheet.iosw.pad .box{margin-bottom:calc(10px + env(safe-area-inset-bottom))}
 @keyframes isFade{from{opacity:0}}@keyframes isUp{from{transform:translateY(40px);opacity:0}}@keyframes isBob{50%{translate:0 6px}}
 @media (prefers-reduced-motion:reduce){#instSheet,#instSheet .box,#instArrow{animation:none}}`;
 document.head.appendChild(css);
 function card(sub,btn,fn){
  if(hidden())return;let c=document.getElementById('instCard');const home=document.getElementById('tab-home');if(!home)return;
  if(!c){c=document.createElement('div');c.className='card instcard';c.id='instCard';home.insertBefore(c,home.firstChild)}
  c.innerHTML=`<img src="icons/icon-192.png" alt=""><div class="it"><b>앱 설치</b><span>${sub}</span></div>${btn?`<button class="btn small" id="instBtn" type="button">${btn}</button>`:''}<button class="ibtn" id="instX" type="button" aria-label="닫기"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button>`;
  if(btn)c.querySelector('#instBtn').onclick=fn;
  c.querySelector('#instX').onclick=()=>{ls(K,String(Date.now()));c.remove()};
 }
 const hide=()=>{['instCard','instSheet','instArrow'].forEach(id=>{const c=document.getElementById(id);if(c)c.remove()})};
 // 설치 창: 첫 화면(로비)에서 안내 창·튜토리얼이 없을 때만 띄움
 const free=()=>{const q=id=>document.getElementById(id),w=q('welcome'),d=q('dlg'),lb=q('lobby');return !!lb&&!lb.classList.contains('hide')&&(!w||w.classList.contains('hide'))&&(!d||d.classList.contains('hide'))&&!document.body.classList.contains('shopen')};
 function whenFree(f,n){if(free())f();else if((n||0)<60)setTimeout(()=>whenFree(f,(n||0)+1),1500)}
 let prevFocus=null;
 function sheet(html,onOk,cls){if(document.getElementById('instSheet'))return;ls(KS,String(Date.now()));prevFocus=document.activeElement;
  const s=document.createElement('div');s.id='instSheet';if(cls)s.className=cls;s.setAttribute('role','dialog');s.setAttribute('aria-modal','true');s.setAttribute('aria-labelledby','instT');
  s.innerHTML=`<div class="box"><div class="hd"><img src="icons/icon-192.png" alt=""><div><h2 id="instT">베팅 오목 앱으로 설치</h2><p>홈 화면에서 바로 열려요</p></div></div>${html}<div class="row"><button class="btn ghost" type="button" data-later>나중에</button>${onOk?'<button class="btn" type="button" data-ok>설치</button>':'<button class="btn" type="button" data-done>확인</button>'}</div></div>`;
  const close=later=>{if(later)ls(K,String(Date.now()));s.remove();const a=document.getElementById('instArrow');if(a)a.remove();try{prevFocus&&prevFocus.focus&&prevFocus.focus()}catch(e){}};
  s.addEventListener('click',e=>{if(e.target===s)close(true)});s.querySelector('[data-later]').onclick=()=>close(true);{const d=s.querySelector('[data-done]');if(d)d.onclick=()=>close(false)}
  if(onOk)s.querySelector('[data-ok]').onclick=async()=>{close(false);await onOk()};
  s.addEventListener('keydown',e=>{if(e.key==='Escape')close(true)});
  document.body.appendChild(s);setTimeout(()=>{const b=s.querySelector('[data-ok]')||s.querySelector('[data-done]');if(b)b.focus()},50)}
 async function doPrompt(){if(!ev)return;const e=ev;ev=null;try{e.prompt();const r=await e.userChoice;if(r&&r.outcome==='accepted')hide()}catch(x){}}
 window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();ev=e;card('홈 화면에서 바로 열기','설치',doPrompt);
  if(want||(!hidden()&&!sheetSeen()))whenFree(()=>{if(ev)sheet('<ul><li><i></i>주소창 없이 전체 화면으로</li><li><i></i>설치는 몇 초 · 용량 거의 없음</li></ul>',doPrompt)})});
 window.addEventListener('appinstalled',hide);
 const ready=f=>document.readyState==='loading'?document.addEventListener('DOMContentLoaded',f):f();
 ready(()=>{
  if(inApp&&(isKakao||isAnd)){
   // 앱 안 브라우저는 설치가 안 되므로 바깥 브라우저로 자동 이동(세션마다 한 번, 실패해도 카드로 다시 시도 가능)
   let tried=false;try{tried=!!sessionStorage.getItem('bo-ext');if(!tried)sessionStorage.setItem('bo-ext','1')}catch(e){}
   if(!tried)setTimeout(toOut,400);
   card(isIOS?'사파리에서 열어 설치':'크롬에서 열어 설치',isIOS?'사파리로':'크롬으로',toOut)}
  else if(inApp&&isIOS)card('··· 메뉴 → Safari로 열기 후 설치');
  else if(isSafari){card('공유 버튼 → 홈 화면에 추가');
   if(want||(!hidden()&&!sheetSeen()))whenFree(()=>{
    sheet(`<div class="ios"><div><b>1</b>아래 공유 버튼 <svg viewBox="0 0 24 24" aria-label="공유"><path d="M12 15V3M8 7l4-4 4 4"/><path d="M6 11v9h12v-9"/></svg> 누르기</div><div><b>2</b>'홈 화면에 추가' 누르기</div></div>`,null,'iosw'+(isPad?' pad':''));
    const a=document.createElementNS('http://www.w3.org/2000/svg','svg');a.id='instArrow';a.setAttribute('viewBox','0 0 24 24');a.setAttribute('aria-hidden','true');if(isPad)a.classList.add('pad');
    a.innerHTML='<path d="M12 3v15M6 12l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>';document.body.appendChild(a);
    if(isPad){const ios=document.querySelector('#instSheet .ios div');if(ios)ios.firstChild.nextSibling.textContent='위쪽 공유 버튼 '}})}
  else if(isIOS)card('Safari로 열면 설치할 수 있어요');
 });
})();
