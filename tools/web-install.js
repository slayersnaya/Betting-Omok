// 웹으로 열었을 때 '앱 설치' 카드 (설치된 앱으로 열면 안 보임)
(()=>{
 const ua=navigator.userAgent||'',standalone=matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
 if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js').catch(()=>{});
 if(standalone)return;
 const isIOS=/iPhone|iPad|iPod/i.test(ua)||(/Macintosh/.test(ua)&&navigator.maxTouchPoints>1),isAnd=/Android/i.test(ua);
 const isKakao=/KAKAOTALK/i.test(ua),inApp=isKakao||/NAVER\(inapp|Instagram|FBAN|FBAV|Line\/|DaumApps|everytimeApp|; wv\)/i.test(ua);
 const K='bo-inst-x';let ev=null;
 const hidden=()=>{try{return Date.now()-(+localStorage.getItem(K)||0)<3*864e5}catch(e){return false}};
 const css=document.createElement('style');css.textContent=`
 .instcard{display:flex;align-items:center;gap:12px;margin-bottom:12px;padding:12px 10px 12px 14px}
 .instcard img{width:44px;height:44px;border-radius:12px;flex:none}
 .instcard .it{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
 .instcard .it b{font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
 .instcard .it span{font-size:12.5px;color:var(--mute);text-wrap:pretty;word-break:keep-all}
 .instcard .btn{flex:none}
 .instcard .ibtn{width:44px;height:44px;margin-left:-6px;margin-right:-4px}
 .instcard .ibtn svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round}`;
 document.head.appendChild(css);
 function card(sub,btn,fn){
  if(hidden())return;let c=document.getElementById('instCard');const home=document.getElementById('tab-home');if(!home)return;
  if(!c){c=document.createElement('div');c.className='card instcard';c.id='instCard';home.insertBefore(c,home.firstChild)}
  c.innerHTML=`<img src="icons/icon-192.png" alt=""><div class="it"><b>앱 설치</b><span>${sub}</span></div>${btn?`<button class="btn small" id="instBtn" type="button">${btn}</button>`:''}<button class="ibtn" id="instX" type="button" aria-label="닫기"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button>`;
  if(btn)c.querySelector('#instBtn').onclick=fn;
  c.querySelector('#instX').onclick=()=>{try{localStorage.setItem(K,String(Date.now()))}catch(e){}c.remove()};
 }
 const hide=()=>{const c=document.getElementById('instCard');if(c)c.remove()};
 window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();ev=e;card('홈 화면에서 바로 열기','설치',async()=>{if(!ev)return;ev.prompt();try{const r=await ev.userChoice;if(r&&r.outcome==='accepted')hide()}catch(x){}ev=null})});
 window.addEventListener('appinstalled',hide);
 const ready=f=>document.readyState==='loading'?document.addEventListener('DOMContentLoaded',f):f();
 ready(()=>{
  if(inApp&&isAnd){const u=location.href;card('크롬에서 열어 설치','크롬으로',()=>{location.href=isKakao?'kakaotalk://web/openExternal?url='+encodeURIComponent(u):'intent://'+u.replace(/^https?:\/\//,'')+'#Intent;scheme=https;package=com.android.chrome;end'})}
  else if(inApp&&isIOS)card('Safari에서 열어 설치');
  else if(isIOS)card('공유 버튼 → 홈 화면에 추가');
 });
})();
