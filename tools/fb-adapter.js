// 베팅 오목 — Firebase 연결 어댑터(웹·어플 버전 전용, claude.ai 아티팩트에는 넣지 않음)
// window.claude.use('db'|'user'|'room')를 같은 모양으로 Firebase(익명 로그인 + Firestore)에 연결한다.
(async()=>{
const V='https://www.gstatic.com/firebasejs/10.12.2/';
const cfg=window.BO_FIREBASE_CONFIG,FB=window.__BO_FB;
try{
 const [{initializeApp},{getAuth,signInAnonymously,onAuthStateChanged,GoogleAuthProvider,linkWithPopup,signInWithCredential,reauthenticateWithPopup},{initializeFirestore,doc,collection,getDoc,getDocs,setDoc,deleteDoc,onSnapshot,query,orderBy,limit,where,serverTimestamp}]=
  await Promise.all([import(V+'firebase-app.js'),import(V+'firebase-auth.js'),import(V+'firebase-firestore.js')]);
 const app=initializeApp(cfg),auth=getAuth(app),fs=initializeFirestore(app,{experimentalForceLongPolling:true,ignoreUndefinedProperties:true});
 // 로그인: 처음이면 익명(게스트)으로 바로 시작
 const uid=await new Promise((res,rej)=>{const off=onAuthStateChanged(auth,u=>{if(u){off();res(u.uid)}else signInAnonymously(auth).catch(rej)})});

 // 오류 코드를 게임 코드가 아는 이름으로
 const MAP={'permission-denied':'invalid_argument','resource-exhausted':'quota_exceeded','unauthenticated':'invalid_argument'};
 const wrapErr=p=>p.catch(e=>{const x=new Error(e&&e.message||'error');x.code=MAP[e&&e.code]||(e&&e.code)||'unknown';throw x});
 const MD={includeMetadataChanges:true};
 // Firestore는 '배열 안의 배열'을 저장하지 못함 → 저장할 때 안쪽 배열을 {__a:[...]}로 감싸고, 읽을 때 되돌림
 const plain=v=>v&&typeof v==='object'&&!Array.isArray(v)&&Object.getPrototypeOf(v)===Object.prototype;
 const isST=v=>plain(v)&&v.__st===1&&Object.keys(v).length===1;
 const enc=v=>Array.isArray(v)?v.map(x=>Array.isArray(x)?{__a:enc(x)}:x===undefined?null:enc(x)):isST(v)?serverTimestamp():plain(v)?Object.fromEntries(Object.entries(v).filter(([,x])=>x!==undefined).map(([k,x])=>[k,enc(x)])):v;
 const dec=v=>Array.isArray(v)?v.map(dec):v&&typeof v==='object'?(typeof v.toMillis==='function'?v.toMillis():Array.isArray(v.__a)&&Object.keys(v).length===1?dec(v.__a):Object.fromEntries(Object.entries(v).map(([k,x])=>[k,dec(x)]))):v;
 // 대국 기록 문서(g/*/p/*): 턴 기록 t:{n:{k:v}}를 맨 위 키 't_n_k'로 펼쳐 저장 → 서버 규칙이 '추가만 허용(지난 기록 수정 금지)'을 검사할 수 있음.
 // 모든 쓰기에 서버 시각 at을 붙임(부재승 판정용)
 const isP=path=>/^g\/[^/]+\/p\/[^/]+$/.test(path);
 const flat=(o,pre,out)=>{for(const [k,v] of Object.entries(o)){if(v===undefined)continue;const key=pre+'_'+k;if(plain(v))flat(v,key,out);else out[key]=v}return out};
 const pEnc=d=>{const o={};for(const [k,v] of Object.entries(d)){if(k==='t'&&plain(v))flat(v,'t',o);else o[k]=v}o.at=serverTimestamp();return o};
 const pDec=d=>{const o={},t={};for(const [k,v] of Object.entries(d)){const m=/^t_(\d+)_(.+)$/.exec(k);if(!m){o[k]=v;continue}let cur=(t[m[1]]=t[m[1]]||{});const ps=m[2].split('_');ps.slice(0,-1).forEach(p=>{cur=(cur[p]=cur[p]&&typeof cur[p]==='object'?cur[p]:{})});cur[ps[ps.length-1]]=v}if(Object.keys(t).length){const T=o.t&&typeof o.t==='object'?o.t:{};for(const n in t)T[n]=Object.assign(T[n]&&typeof T[n]==='object'?T[n]:{},t[n]);o.t=T}return o};
 const wEnc=(path,d)=>enc(isP(path)?pEnc(d):d);
 const safe=f=>{try{return f()}catch(e){return Promise.reject(e)}};
 const snapDoc=s=>({id:s.id,exists:s.exists(),data:()=>{const d=s.data({serverTimestamps:'estimate'});if(d==null)return d;const x=dec(d);return isP(s.ref.path)?pDec(x):x},metadata:{fromCache:s.metadata.fromCache,hasPendingWrites:s.metadata.hasPendingWrites}});
 const D=path=>{const ref=doc(fs,path);return{
  get:()=>wrapErr(getDoc(ref)).then(snapDoc),
  set:d=>wrapErr(safe(()=>setDoc(ref,wEnc(path,d)))),
  // 게임 코드는 update로 중첩 객체를 깊게 합치므로 merge 저장으로 맞춤
  update:d=>wrapErr(safe(()=>setDoc(ref,wEnc(path,d),{merge:true}))),
  delete:()=>wrapErr(deleteDoc(ref)),
  // 메타데이터 변화(캐시 → 서버 확인)도 받아야 '서버에서 확인됨' 신호를 놓치지 않음
  onSnapshot:(cb,err)=>onSnapshot(ref,MD,s=>cb(snapDoc(s)),e=>err&&err(e))}};
 const C=(path,cons=[])=>{const q=()=>query(collection(fs,path),...cons);return{
  orderBy:(f,dir)=>C(path,[...cons,orderBy(f,dir||'asc')]),
  limit:n=>C(path,[...cons,limit(n)]),
  where:(a,o,b)=>C(path,[...cons,where(a,o,b)]),
  doc:id=>D(path+'/'+id),
  get:()=>wrapErr(getDocs(q())).then(qs=>({docs:qs.docs.map(snapDoc),metadata:{fromCache:qs.metadata.fromCache}})),
  onSnapshot:(cb,err)=>onSnapshot(q(),MD,qs=>cb({docs:qs.docs.map(snapDoc),metadata:{fromCache:qs.metadata.fromCache}}),e=>err&&err(e))}};
 const db={doc:D,collection:C};

 // 접속 표시(presence): rt/{방}/p/{uid}에 20초마다 '살아 있음'을 쓰고, 60초 안에 쓴 사람만 접속 중으로 봄
 const rooms=new Set();
 const Room=name=>{let pres={},hb=null,un=null,tick=null,last=[];const ref=doc(fs,`rt/${name}/p/${uid}`);
  const beat=()=>setDoc(ref,{presence:pres,at:serverTimestamp()}).catch(()=>{});
  const r={
   presence(p){pres=Object.assign({},pres,p);for(const k in pres)if(pres[k]==null)delete pres[k];
    // 표시할 것이 없으면 '살아 있음' 쓰기를 멈추고 문서도 지움(매칭 취소 후 20초마다 쓰던 문제)
    if(!Object.keys(pres).length){clearInterval(hb);hb=null;rooms.delete(r);return deleteDoc(ref).catch(()=>{})}
    beat();if(!hb)hb=setInterval(beat,20000);rooms.add(r);return Promise.resolve()},
   // 접속 판정은 '내 폰이 그 사람의 갱신을 받은 시각' 기준(폰마다 시계가 달라도 됨)
   onPeers(cb){const seen={};const emit=()=>{const now=Date.now();cb({peers:last.filter(p=>p.you||now-(seen[p.id]?seen[p.id].t:0)<60000)})};
    un=onSnapshot(collection(fs,`rt/${name}/p`),qs=>{const now=Date.now();last=qs.docs.map(d=>{const v=d.data()||{},at=+v.at||0,o=seen[d.id];
      if(!o)seen[d.id]={at,t:Math.abs(now-at)<120000?now:now-3600e3};else if(o.at!==at)seen[d.id]={at,t:now};
      return{id:d.id,presence:v.presence||{},at,you:d.id===uid}});emit()},()=>{});
    tick=setInterval(emit,15000);return()=>{un&&un();clearInterval(tick)}},
   leave(){clearInterval(hb);hb=null;clearInterval(tick);un&&un();rooms.delete(r);return deleteDoc(ref).catch(()=>{})}};
  return r};
 const lobby=Room('lobby');
 const room=Object.assign(lobby,{join:n=>Promise.resolve(Room(String(n).replace(/[^A-Za-z0-9_-]/g,'').slice(0,40)))});
 addEventListener('pagehide',()=>{for(const r of [...rooms])r.leave()});

 // 사용자: 게스트(익명) → 구글 계정 연결(같은 uid 유지). 이미 다른 기록이 있는 구글 계정이면 그 기록으로 전환
 const prov=new GoogleAuthProvider();
 const user={firebase:true,
  id:()=>Promise.resolve(auth.currentUser?auth.currentUser.uid:uid),
  can:()=>Promise.resolve(true),
  me:()=>Promise.resolve({name:''}),
  google:()=>{const u=auth.currentUser;if(!u||u.isAnonymous)return null;const g=u.providerData.find(p=>p.providerId==='google.com');return g?(g.email||'연결됨'):null},
  linkGoogle:()=>linkWithPopup(auth.currentUser,prov).then(()=> 'linked').catch(e=>{
   if(e&&e.code==='auth/credential-already-in-use'){const cred=GoogleAuthProvider.credentialFromError(e);return signInWithCredential(auth,cred).then(()=>'switched')}
   if(e&&e.code==='auth/popup-blocked'){const x=new Error('popup');x.code='popup-blocked';throw x}
   throw e}),
  // 계정 삭제(구글 계정은 최근 로그인이 필요하면 한 번 더 확인 창)
  deleteAccount:async()=>{const u=auth.currentUser;if(!u)return;try{await u.delete()}catch(e){if(e&&e.code==='auth/requires-recent-login'&&!u.isAnonymous){await reauthenticateWithPopup(u,prov);await u.delete()}else throw e}}};
 FB.resolve({db,user,room});
}catch(e){console.warn('firebase init failed',e);FB.resolve({})}

})();
