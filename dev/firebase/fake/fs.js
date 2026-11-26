// 테스트용 가짜 Firestore: 같은 브라우저의 여러 페이지가 BroadcastChannel로 같은 저장소를 공유. 규칙(rules) 흉내 포함
let store={};let synced;const ready=new Promise(r=>{synced=r;setTimeout(r,800)});const L=new Set();const bc={postMessage:m=>window.__fsSend(JSON.stringify(m))};
const clone=x=>x==null?x:JSON.parse(JSON.stringify(x));
window.__fsRecv=j=>{const m=JSON.parse(j);if(m.t==='sync?'){bc.postMessage({t:'sync',store})}else if(m.t==='sync'){store=Object.assign({},m.store,store);fire();synced()}else if(m.t==='w'){apply(m);fire()}};
bc.postMessage({t:'sync?'});
function deep(t,s){for(const k in s){if(s[k]&&typeof s[k]==='object'&&!Array.isArray(s[k])){if(!t[k]||typeof t[k]!=='object'||Array.isArray(t[k]))t[k]={};deep(t[k],s[k])}else t[k]=s[k]}return t}
function apply(m){if(m.op==='del')delete store[m.p];else if(m.merge)store[m.p]=deep(store[m.p]||{},clone(m.d));else store[m.p]=clone(m.d)}
function fire(){for(const l of [...L])l()}
export const getFirestore=()=>({});export const initializeFirestore=(app,o)=>{window.__fsOpts=o;return{}};
const nested=v=>Array.isArray(v)?v.some(x=>Array.isArray(x)||nested(x)):v&&typeof v==='object'?Object.values(v).some(nested):false;
export const doc=(fs,p)=>({p});export const collection=(fs,p)=>({p,col:1});
export const query=(c,...cons)=>({p:c.p,cons});export const orderBy=(f,d)=>({k:'o',f,d});export const limit=n=>({k:'l',n});export const where=(f,o,v)=>({k:'w',f,o,v});
const ds=(p)=>({id:p.split('/').pop(),ref:{path:p},exists:()=>store[p]!=null,data:()=>clone(store[p]),metadata:{fromCache:false,hasPendingWrites:false}});
function q(Q){const pre=Q.p+'/';let ks=Object.keys(store).filter(k=>k.startsWith(pre)&&!k.slice(pre.length).includes('/'));
 for(const c of Q.cons||[]){if(c.k==='w')ks=ks.filter(k=>{const v=(store[k]||{})[c.f];return c.o==='=='?v===c.v:c.o==='>'?v>c.v:c.o==='>='?v>=c.v:c.o==='<'?v<c.v:c.o==='<='?v<=c.v:true})}
 for(const c of Q.cons||[])if(c.k==='o')ks.sort((a,b)=>{const x=(store[a]||{})[c.f]??0,y=(store[b]||{})[c.f]??0;return(c.d==='desc'?-1:1)*(x<y?-1:x>y?1:0)});
 for(const c of Q.cons||[])if(c.k==='l')ks=ks.slice(0,c.n);
 return{docs:ks.map(ds),metadata:{fromCache:false}}}
// ---- 규칙 흉내(firestore.rules와 같은 내용) ----
function uid(){const s=sessionStorage.getItem('fake-uid');return s}
const google=()=>sessionStorage.getItem('fake-g')==='1';
function deny(){const e=new Error('denied');e.code='permission-denied';window.__denied=(window.__denied||0)+1;(window.__deniedList=window.__deniedList||[]).push(arguments[0]);throw e}
const ST={__fst:1};export const serverTimestamp=()=>ST;
const isST=v=>v===ST||(v&&typeof v==='object'&&v.__fst===1);
// 서버 시각 표시를 실제 시각(밀리초)으로 바꿈
const fillST=(v,now)=>isST(v)?now:Array.isArray(v)?v.map(x=>fillST(x,now)):v&&typeof v==='object'?Object.fromEntries(Object.entries(v).map(([k,x])=>[k,fillST(x,now)])):v;
const nick=v=>typeof v==='string'&&v.length<=12,seatId=v=>typeof v==='string'&&/^[A-Za-z0-9-]{4,40}$/.test(v),int=v=>Number.isInteger(v);
const near=(ms,back,ahead)=>int(ms)&&ms>Date.now()-back&&ms<Date.now()+ahead;
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const diff=(cur,next)=>{const ks=new Set([...Object.keys(cur||{}),...Object.keys(next||{})]),r={removed:[],changed:[],added:[],aff:[]};
 for(const k of ks){const a=cur&&k in cur,b=next&&k in next;if(a&&!b){r.removed.push(k);r.aff.push(k)}else if(!a&&b){r.added.push(k);r.aff.push(k)}else if(!eq(cur[k],next[k])){r.changed.push(k);r.aff.push(k)}}return r};
const only=(arr,allow)=>arr.every(k=>allow.includes(k)),any=(arr,ks)=>arr.some(k=>ks.includes(k));
const rec=m=>m&&typeof m==='object'&&only(Object.keys(m),['w','l','d'])&&['w','l','d'].every(k=>!(k in m)||int(m[k])),recs=a=>a&&typeof a==='object'&&only(Object.keys(a),['beginner','mid','pro','ultimate'])&&Object.values(a).every(rec);
const cellv=(l,i)=>l.length<=i||typeof l[i]==='number'||(l[i]&&typeof l[i]==='object'&&!Array.isArray(l[i])&&only(Object.keys(l[i]),['__a'])&&Array.isArray(l[i].__a)&&l[i].__a.length<=2&&l[i].__a.every(x=>typeof x==='number'));
const small=v=>v==null||typeof v==='boolean'||typeof v==='number'||(typeof v==='string'&&v.length<=128)||(Array.isArray(v)&&v.length<=3&&[0,1,2].every(i=>cellv(v,i)));
const lkOk=(d,changed)=>Array.isArray(d.lk)&&d.lk.length<=6&&only(changed,[...d.lk,'at','lk'])&&d.lk.every(k=>typeof k==='string'&&/^[A-Za-z0-9_]{1,24}$/.test(k)&&k in d&&small(d[k]));
const stale=ts=>typeof ts==='number'&&ts<Date.now()-180000;
function oppAbsent(gid,g,opp){const pd=store[`g/${gid}/p/${opp}`],rt=store[`rt/g-${gid}/p/${opp}`];
 return (pd?(!('at' in pd)||stale(pd.at)):g.created<Date.now()-180000)&&(!rt||stale(rt.at))}
function check(op,p,raw,merge){const me=uid();if(!me)deny(op+' '+p);const seg=p.split('/');const cur=store[p];
 const now=Date.now(),d=raw?fillST(raw,now):raw;const next=op==='del'?null:(merge?deep(clone(cur)||{},clone(d)):clone(d));
 const create=op!=='del'&&!cur,upd=op!=='del'&&!!cur;
 const atOK=()=>isST(raw.at);
 if(seg[0]==='g'&&seg.length===2){const gid=seg[1];
  if(create){const ks=['host','hostNick','guest','guestNick','created','td','tb','status','private','ranked','prev','first','rv','lob'];
   if(!/^g[0-9a-f]{8}$/.test(gid)||!only(Object.keys(next),ks)||next.host!==me||!nick(next.hostNick)||('guestNick' in next&&!nick(next.guestNick))
    ||('guest' in next&&next.guest!=null&&(!seatId(next.guest)||next.guest===me))||!near(next.created,6e5,6e4)
    ||!((next.status==='open'&&next.guest==null)||(next.status==='playing'&&seatId(next.guest)))
    ||('private' in next&&typeof next.private!=='boolean')||('prev' in next&&!/^g[0-9a-f]{8}$/.test(next.prev||''))||('rv' in next&&next.rv!==2)
    ||('lob' in next&&next.lob!==0&&!(next.lob===next.created&&next.status==='open'&&!next.private))
    ||('first' in next&&next.first!==me&&next.first!==next.guest)||('ranked' in next&&typeof next.ranked!=='boolean')
    ||(next.ranked&&!(next.status==='playing'&&next.rv===2&&next.td===20&&next.tb===30&&!('first' in next)))
    ||!int(next.td)||next.td<0||next.td>600||!int(next.tb)||next.tb<0||next.tb>600||!['open','playing'].includes(next.status)
    ||(next.ranked&&!google()))deny('g create '+p+' '+JSON.stringify(raw));return}
  if(upd){const df=diff(cur,next);const a=df.aff;
   const ok=only(a,['guest','guestNick','status','next','ab','lob'])&&(!a.includes('lob')||(cur.host===me&&next.lob===0))&&(cur.host===me||(cur.guest===me&&only(a,['status','ab'])))
    &&(!a.includes('guest')||(cur.guest==null&&seatId(next.guest)&&next.status==='playing'&&next.guest!==cur.host&&!!store[`g/${gid}/p/${next.guest}`]))
    &&(!a.includes('guestNick')||nick(next.guestNick))
    &&(!a.includes('status')||(cur.status==='open'&&next.status==='playing')||(cur.status==='playing'&&next.status==='done'))
    &&(!a.includes('next')||(!('next' in cur)&&typeof next.next==='string'&&/^g[0-9a-f]{8}$/.test(next.next)))
    &&(!a.includes('ab')||(!('ab' in cur)&&cur.guest!=null&&cur.rv===2&&only(Object.keys(next.ab||{}),['by','t','at'])&&next.ab.by===me&&int(next.ab.t)&&isST(raw.ab&&raw.ab.at)
      &&((cur.host===me&&oppAbsent(gid,cur,cur.guest))||(cur.guest===me&&oppAbsent(gid,cur,cur.host)))));
   if(!ok)deny('g update '+p+' '+JSON.stringify(raw));return}
  // delete
  if(!cur)return;if(cur.host!==me||!(cur.status==='open'||(cur.status==='done'&&cur.ranked!==true&&!!(store[`g/${gid}/p/${cur.guest}`]||{}).again)||cur.guest==null||!store[`g/${gid}/p/${cur.guest}`]||(cur.ranked!==true&&cur.created<now-864e5)))deny('g del '+p);return}
 if(seg[0]==='g'&&seg[2]==='p'&&seg.length===4){const gid=seg[1],seat=seg[3],g=store['g/'+gid];
  if(create){if(seat!==me||next.seat!==me||!nick(next.nick??'')||!atOK()||Object.keys(next).length>=3000||!int(next.joined??0)||!lkOk(next,Object.keys(next))||!g||!((g.status==='open'&&only(Object.keys(next),['seat','nick','joined','at','lk']))||(g.status==='playing'&&(g.host===me||g.guest===me))))deny('p create '+p+' '+JSON.stringify(raw));return}
  if(upd){const df=diff(cur,next);
   if(seat!==me||df.removed.length||!only(df.changed,['nick','joined','at','lk'])||!lkOk(next,df.aff)||!nick(next.nick??'')||!atOK()||Object.keys(next).length>=3000
    ||!int(next.joined??0)||!(only(df.aff,['at','nick','joined','lk'])||(g&&(g.host===me||g.guest===me)&&(only(df.aff,['at','again','nick','joined','lk'])||!('ab' in g)))))deny('p update '+p+' '+JSON.stringify(raw)+' '+JSON.stringify(df));return}
  if(!cur)return;
  if(!g||(g.status==='open'&&(seat===me||g.host===me))||(seat===me&&g.status==='playing'&&(g.guest==null||!store[`g/${gid}/p/${g.guest}`])))return;
  deny('p del '+p)}
 if(seg[0]==='res'){if(op!=='set'||cur)deny(op+' '+p);const r=next,g=store['g/'+r.gid];
  const ok=google()&&only(Object.keys(r),['gid','A','B','na','nb','ended','w','by','why','turns'])&&r.by===me&&typeof r.gid==='string'&&/^g[0-9a-f]{8}$/.test(r.gid)&&seg[1]===r.gid+'-'+me
   &&nick(r.na)&&nick(r.nb)&&typeof r.why==='string'&&r.why.length<=20&&int(r.turns)&&near(r.ended,6e5,12e4)&&g&&g.ranked===true&&g.host===r.A&&g.guest===r.B
   &&(me===r.A||me===r.B)&&[r.A,r.B,'draw','void'].includes(r.w)&&!!store[`g/${r.gid}/p/${r.A}`]&&!!store[`g/${r.gid}/p/${r.B}`]&&(r.why!=='상대 부재'||'ab' in g);
  if(!ok)deny('res '+p+' '+JSON.stringify(r));return}
 if(seg[0]==='bres'){if(op!=='set'||cur)deny(op+' '+p);const r=next;
  const ok=google()&&only(Object.keys(r),['by','gid','bot','na','w','turns','why','ended'])&&r.by===me&&typeof r.gid==='string'&&/^k[0-9a-f]{8}$/.test(r.gid)&&seg[1]===me+'_'+r.gid
   &&typeof r.bot==='string'&&/^b[0-9]{2}$/.test(r.bot)&&nick(r.na)&&['me','bot','draw'].includes(r.w)&&int(r.turns)&&r.turns>=0&&r.turns<=400&&typeof r.why==='string'&&r.why.length<=20&&near(r.ended,6e5,12e4);
  if(!ok)deny('bres '+p+' '+JSON.stringify(r));return}
 if(seg[0]==='cfg'){if(op==='del')deny('del '+p);const r=next;
  if(!(window.__fakeAdmin===true&&seg[1]==='master'&&only(Object.keys(r),['seats','at'])&&Array.isArray(r.seats)&&r.seats.length<=5&&r.seats.includes(me)&&int(r.at)))deny('cfg '+p+' '+JSON.stringify(r));return}
 if(seg[0]==='nicks'){if(op==='del'){if(cur&&cur.by===me)return;deny('del '+p)}const r=next;
  const ok=/^n[0-9a-f]{2,100}$/.test(seg[1])&&only(Object.keys(r),['by','g','at'])&&r.by===me&&r.g===google()&&near(r.at,3e5,3e5)&&(!cur||cur.by===me||(cur.g===false&&cur.at<Date.now()-2592e6));
  if(!ok)deny('nicks '+p+' '+JSON.stringify(r));return}
 if(seg[0]==='mm'){if(op==='del'){if(seg[1]===me||(cur&&cur.from===me))return;deny('del '+p)}
  if(!only(Object.keys(next),['gid','from','nick','at'])||next.from!==me||!/^g[0-9a-f]{8}$/.test(next.gid||'')||!nick(next.nick)||!near(next.at,6e5,6e5))deny(op+' '+p);return}
 if(seg[0]==='rt'){if(seg[3]!==me)deny(op+' '+p);if(op==='del')return;
  if(!/^(lobby|g-g[0-9a-f]{8})$/.test(seg[1])||!only(Object.keys(next),['presence','at'])||!next.presence||typeof next.presence!=='object'||!only(Object.keys(next.presence),['seat','mm'])||('seat' in next.presence&&!seatId(next.presence.seat))
   ||('mm' in next.presence&&!(next.presence.mm&&only(Object.keys(next.presence.mm),['seat','r','since','nick'])&&seatId(next.presence.mm.seat)&&nick(next.presence.mm.nick)&&typeof next.presence.mm.r==='number'&&int(next.presence.mm.since??0)))||!atOK())deny(op+' '+p+' '+JSON.stringify(raw));return}
 if(seg[0]==='aigames'){if(op==='del'){if(cur&&(cur.by===me||window.__fakeAdmin===true))return;deny('del '+p)}
  if(cur||!only(Object.keys(next),['by','at','level','winner','reason','first','timed','v','hj','rk','bot'])||typeof next.hj!=='string'||next.hj.length>60000||(next.winner!=null&&!['A','B'].includes(next.winner))||('first' in next&&!['A','B'].includes(next.first))||next.by!==me||!new RegExp('^'+me+'_[A-Za-z0-9]{1,40}$').test(seg[1])||!near(next.at,864e5,3e5)
   ||typeof next.level!=='string'||next.level.length>12||typeof next.reason!=='string'||next.reason.length>12)deny(op+' '+p+' '+JSON.stringify(raw).slice(0,200));return}
 if(seg[0]==='lob'){if(seg[1]!==me)deny(op+' '+p);if(op==='del')return;const g=store['g/'+(next.gid||'')];
  if(!only(Object.keys(next),['gid','nick','td','tb','created'])||!/^g[0-9a-f]{8}$/.test(next.gid||'')||!nick(next.nick)||!int(next.td)||!int(next.tb)||!near(next.created,6e4,6e4)||!g||g.host!==me||g.status!=='open'||g.private)deny(op+' '+p+' '+JSON.stringify(raw));return}
 if(seg[0]==='prof'){if(seg[1]!==me)deny(op+' '+p);if(op==='del')return;
  if(!only(Object.keys(next),['nick','airec','pts'])||('nick' in next&&!nick(next.nick))||('airec' in next&&!recs(next.airec))||('pts' in next&&!near(next.pts,31536e6,3e5)))deny(op+' '+p+' '+JSON.stringify(raw).slice(0,200));return}
 if(seg[0]==='ailearn'){if(seg[1]!==me)deny(op+' '+p);if(op==='del')return;
  if(!only(Object.keys(next),['v','hs','g','ts'])||next.v!==2||typeof next.hs!=='string'||next.hs.length>12000||!int(next.g)||!near(next.ts,31536e6,3e5))deny(op+' '+p+' '+JSON.stringify(raw).slice(0,200));return}
 deny('unknown '+p)}
// 읽기 규칙: aigames는 본인 것·관리자만
function canRead(path,data){const me=uid();if(!me)return false;const seg=path.split('/');if(seg[0]==='aigames')return data&&data.by===me||window.__fakeAdmin===true;if(seg[0]==='mm')return seg[1]===me;if(seg[0]==='prof')return seg[1]===me;if(seg[0]==='g'&&seg[2]==='p'){const g=store['g/'+seg[1]];return !g||g.ranked!==true||g.status==='done'||g.host===me||g.guest===me}return true}
const rdeny=p=>{const e=new Error('denied read');e.code='permission-denied';(window.__deniedList=window.__deniedList||[]).push('read '+p);return e};
export async function getDoc(r){await ready;if(store[r.p]&&!canRead(r.p,store[r.p]))throw rdeny(r.p);cached.add(r.p);return ds(r.p)}
export async function getDocs(Q){await ready;const r=q(Q);if(r.docs.some(d=>!canRead(Q.p+'/'+d.id,store[Q.p+'/'+d.id])))throw rdeny(Q.p);return r}
export function setDoc(r,d,o){if(nested(d)){const e=new Error('Nested arrays are not supported');e.code='invalid-argument';throw e}return setDoc2(r,d,o)}
async function setDoc2(r,d0,o){check('set',r.p,d0,o&&o.merge);const d=fillST(d0,Date.now());const m={t:'w',op:'set',p:r.p,d,merge:!!(o&&o.merge)};apply(m);cached.add(r.p);bc.postMessage(m);setTimeout(fire,0)}
export async function deleteDoc(r){check('del',r.p);const m={t:'w',op:'del',p:r.p};apply(m);bc.postMessage(m);setTimeout(fire,0)}
// 실제 SDK 흉내: 이 페이지 캐시에 있는 문서는 첫 스냅샷을 fromCache:true로 먼저 주고, 서버 확인(내용 같음)은 includeMetadataChanges일 때만 전달
const cached=new Set();window.__fakeStrictCache=window.__fakeStrictCache!==false;
export function onSnapshot(ref,a,b,c){let opts={},cb,err;if(typeof a==='function'){cb=a;err=b}else{opts=a||{};cb=b;err=c}
 const isQ=!!(ref.col||ref.cons),snap=fc=>{if(isQ){const r=q(ref);r.metadata={fromCache:fc};r.docs.forEach(d=>d.metadata.fromCache=fc);return r}const d=ds(ref.p);d.metadata={fromCache:fc,hasPendingWrites:false};return d};
 const keys=()=>isQ?q(ref).docs.map(d=>ref.p+'/'+d.id):[ref.p];
 const ser=()=>JSON.stringify(isQ?q(ref).docs.map(d=>[d.id,d.data()]):store[ref.p]);
 if(isQ&&q(ref).docs.some(d=>!canRead(ref.p+'/'+d.id,store[ref.p+'/'+d.id]))){setTimeout(()=>{const e=rdeny(ref.p);(err||(()=>{}))(e)},0);return()=>{}}
 let last=null,synced=false,live=true;
 const emit=fc=>{if(!live)return;keys().forEach(k=>cached.add(k));cb(snap(fc))};
 // 첫 스냅샷
 setTimeout(()=>{const ks=keys(),hasCache=ks.length&&ks.every(k=>cached.has(k));
  if(window.__fakeStrictCache&&hasCache){last=ser();emit(true);
   setTimeout(()=>{synced=true;const s2=ser();if(s2!==last){last=s2;emit(false)}else if(opts.includeMetadataChanges)emit(false)},300)}
  else{synced=true;last=ser();emit(false)}},0);
 const l=()=>{if(!synced)return;const s2=ser();if(s2!==last){last=s2;emit(false)}};L.add(l);
 return()=>{live=false;L.delete(l)}}

// ---- (랭크 개편 3차 덧붙임) 시즌 최종 기록 cfg/season{n}, 관리자 지난 시즌 정리 삭제, AI id b00~b199 ----
{const _check0=check,DAY=864e5;
 check=function(op,p,raw,merge){const seg=p.split('/'),cur=store[p],adm=window.__fakeAdmin===true&&!!uid()&&google(),now=Date.now();
  if(seg[0]==='cfg'&&seg[1]==='start'){if(!adm||op==='del')deny(op+' '+p);const r=raw;if(!(only(Object.keys(r),['s','at'])&&r.s&&typeof r.s==='object'&&Object.keys(r.s).length<=10&&int(r.at)))deny('cfg start');return}
  if(seg[0]==='cfg'&&/^season[0-9]{1,3}$/.test(seg[1]||'')){if(!adm)deny(op+' '+p);if(op==='del')return;const r=op==='set'&&!merge?raw:deep(clone(cur)||{},clone(raw));
   if(cur&&!(int(cur.at)&&cur.at>now-DAY))deny('cfg upd '+p);
   if(!(['n','at','p'].every(k=>k in r)&&only(Object.keys(r),['n','at','v','p','final','top','amt','rw'])&&int(r.n)&&seg[1]==='season'+r.n&&int(r.at)&&r.p&&typeof r.p==='object'&&!Array.isArray(r.p)))deny('cfg '+p+' '+JSON.stringify(r).slice(0,200));return}
  if(op==='del'&&adm&&cur){
   if((seg[0]==='res'||seg[0]==='bres')&&seg.length===2&&int(cur.ended)&&cur.ended<now-DAY)return;
   if(seg[0]==='g'&&seg.length===2&&int(cur.created)&&cur.created<now-DAY)return;
   if(seg[0]==='g'&&seg[2]==='p'&&seg.length===4){const g=store['g/'+seg[1]];if(!g||(g.created??now)<now-DAY)return}}
  if(seg[0]==='bres'&&op==='set'&&!cur&&raw&&typeof raw==='object'){const r2=Object.assign({},raw);
   if('st' in r2){if(!(int(r2.st)&&int(r2.ended)&&r2.st<=r2.ended&&r2.st>r2.ended-7*DAY))deny('bres st '+p);delete r2.st}
   if(typeof r2.bot==='string'&&/^b1[0-9]{2}$/.test(r2.bot))r2.bot='b99';return _check0(op,p,r2,merge)}
  return _check0(op,p,raw,merge)}}

// ---- (친구 기능 덧붙임) fp 친구·대화, on 접속, fc 친구 코드, bk 차단, rep 신고, nicks 표시용 n, 문서 id 범위 쿼리('__name__') ----
export const documentId=()=>'__name__';
{const _check1=check,_canRead1=canRead,_q1=q,_onSnap1=onSnapshot;
 const W=7*864e5,isGid=v=>typeof v==='string'&&/^g[0-9a-f]{8}$/.test(v);
 const pidOf=(x,y)=>x<y?x+'_'+y:y+'_'+x,blk=(x,y)=>!!store['bk/'+x+'_'+y],noBlock=(x,y)=>!blk(x,y)&&!blk(y,x);
 const takesReq=u=>!store['on/'+u]||store['on/'+u].nr!==true;
 const tokenOk=(u,tk)=>!!store['on/'+u]&&store['on/'+u].tk===tk&&(store['on/'+u].tka||0)>Date.now()-W;
 const fmsg=(v,s,i)=>v&&typeof v==='object'&&!Array.isArray(v)&&only(Object.keys(v),['i','s','t','a','e','k'])&&(!('k' in v)||['inv','acc','dec','can','exp'].includes(v.k))&&['i','s','t','a'].every(k=>k in v)&&v.i===i&&v.s===s&&typeof v.t==='string'&&v.t.length>=1&&v.t.length<=200&&near(v.a,6e5,6e5)&&(!('e' in v)||(int(v.e)&&v.e>=1&&v.e<i));
 const hasAllE=(a,b)=>b.every(x=>a.some(y=>eq(x,y))),rmAll=(a,b)=>a.filter(x=>!b.some(y=>eq(x,y)));
 const shifted=(o,n)=>Array.isArray(n)&&((o.length<50&&n.length===o.length+1&&hasAllE(n,o))||(o.length>=50&&n.length===50&&rmAll(o,n).length===o.length-49));
 check=function(op,p,raw,merge){const seg=p.split('/');
  if(!['fp','on','fc','bk','rep','nicks','seen'].includes(seg[0])||seg.length!==2)return _check1(op,p,raw,merge);
  const me=uid();if(!me)deny(op+' '+p);const cur=store[p],now=Date.now(),d=raw?fillST(raw,now):raw,next=op==='del'?null:(merge?deep(clone(cur)||{},clone(d)):clone(d)),id=seg[1];
  const G=google(),T=v=>v===now;
  if(seg[0]==='nicks'){if(op==='del'){if(cur&&cur.by===me)return;deny('del '+p)}const r=next;
   const ok=/^n[0-9a-f]{2,100}$/.test(id)&&only(Object.keys(r),['by','g','at','n'])&&(!('n' in r)||nick(r.n))&&r.by===me&&r.g===G&&near(r.at,3e5,3e5)&&(!cur||cur.by===me||(cur.g===false&&cur.at<now-2592e6));
   if(!ok)deny('nicks '+p+' '+JSON.stringify(r));return}
  if(seg[0]==='fp'){
   if(op==='del'){if(!cur)return;const o=cur.a===me?cur.b:cur.a;if((cur.a===me||cur.b===me)&&(cur.st==='ok'||(cur.st==='req'&&cur.by===me)||(cur.st==='no'&&cur.by!==me)||blk(me,o)))return;deny('fp del '+p)}
   const r=next;
   if(!cur){const o=r.a===me?r.b:r.a;
    const ok=G&&only(Object.keys(r),['a','b','by','st','at','sa','na','nb','tk','m','q','ra','rb'])&&seatId(r.a)&&seatId(r.b)&&r.a<r.b&&id===r.a+'_'+r.b&&(r.a===me||r.b===me)&&r.by===me
     &&T(r.at)&&T(r.sa)&&nick(r.na)&&nick(r.nb)&&eq(r.m,[])&&r.q===0&&r.ra===0&&r.rb===0&&noBlock(me,o)
     &&((r.st==='req'&&!('tk' in r)&&takesReq(o))||(r.st==='ok'&&typeof r.tk==='string'&&tokenOk(o,r.tk)));
    if(!ok)deny('fp create '+p+' '+JSON.stringify(raw));return}
   const c=cur,k=diff(c,r).aff,s=c.a===me?'a':'b',o=s==='a'?'b':'a',ou=c[o];
   const has=(arr)=>only(k,arr);
   const accept=()=>c.st==='req'&&c.by!==me&&r.st==='ok'&&has(['st','sa','n'+s])&&T(r.sa)&&nick(r['n'+s]??'');
   const decline=()=>c.st==='req'&&c.by!==me&&r.st==='no'&&has(['st','sa'])&&T(r.sa);
   const again=()=>c.st==='no'&&c.by===me&&c.sa<now-W&&r.st==='req'&&has(['st','sa','n'+s])&&T(r.sa)&&nick(r['n'+s]??'')&&takesReq(ou)&&noBlock(me,ou);
   const nk=()=>has(['n'+s])&&nick(r['n'+s]??'');
   const msg=()=>c.st==='ok'&&has(['m','q','w'+s,'r'+s])&&r.q===c.q+1&&(r['r'+s]??0)===r.q&&T(r['w'+s])&&(!(('w'+s) in c)||now>c['w'+s]+1000)&&shifted(c.m,r.m)&&fmsg(r.m[r.m.length-1],s,r.q);
   const read=()=>has(['r'+s])&&int(r['r'+s])&&r['r'+s]>=(c['r'+s]??0)&&r['r'+s]<=c.q;
   const inv=()=>{if(!(c.st==='ok'&&has(['g'+s])))return false;const v=r['g'+s];if(v==null)return true;const g=store['g/'+v.gid];
    return c['g'+s]==null&&typeof v==='object'&&only(Object.keys(v),['gid','at','t'])&&(!('t' in v)||(int(v.t)&&v.t>=0&&v.t<=3))&&isGid(v.gid)&&near(v.at,12e4,12e4)&&!!g&&g.host===me&&g.status==='open'};
   const invClr=()=>has(['g'+o])&&r['g'+o]==null;
   const ok=G&&(c.a===me||c.b===me)&&only(k,['st','sa','na','nb','m','q','ra','rb','wa','wb','ga','gb'])&&(accept()||decline()||again()||nk()||msg()||read()||inv()||invClr());
   if(!ok)deny('fp update '+p+' '+JSON.stringify(raw).slice(0,300));return}
  if(seg[0]==='on'){if(op==='del'){if(id===me)return;deny('del '+p)}const r=next,k=cur?diff(cur,r).aff:Object.keys(r);
   const fcMine=v=>typeof v==='string'&&/^[A-HJ-NP-Z2-9]{8}$/.test(v)&&!!store['fc/'+v]&&store['fc/'+v].by===me;
   const ok=G&&id===me&&only(Object.keys(r),['at','st','fc','tk','tka','nr','hs'])&&T(r.at)&&['on','off','g','r'].includes(r.st)&&(!('tk' in r)||(typeof r.tk==='string'&&/^[0-9a-f]{16}$/.test(r.tk)))
    &&(!('nr' in r)||typeof r.nr==='boolean')&&(!('hs' in r)||typeof r.hs==='boolean')&&(!k.includes('fc')||fcMine(r.fc))&&(!k.includes('tka')||near(r.tka,12e4,12e4));
   if(!ok)deny('on '+p+' '+JSON.stringify(raw));return}
  if(seg[0]==='fc'){if(op==='del'){if(cur&&cur.by===me)return;deny('del '+p)}const r=next;
   if((cur&&cur.by!==me)||!G||!/^[A-HJ-NP-Z2-9]{8}$/.test(id)||!only(Object.keys(r),['by','n'])||r.by!==me||(('n' in r||cur)&&!nick(r.n??'')))deny('fc '+p);return}
  if(seg[0]==='bk'){if(op==='del'){if(cur&&cur.by===me)return;deny('del '+p)}const r=next;
   if(cur||!G||!only(Object.keys(r),['by','who','nk','at'])||r.by!==me||!seatId(r.who)||r.who===me||id!==me+'_'+r.who||!nick(r.nk)||!T(r.at))deny('bk '+p+' '+JSON.stringify(raw));return}
  if(seg[0]==='seen'){if(op==='del')deny('del '+p);const r=next;
   if(id!==me||!only(Object.keys(r),['at','pv','nk','v'])||!T(r.at)||!['g','e','n'].includes(r.pv)||!nick(r.nk)||typeof r.v!=='string'||r.v.length>16)deny('seen '+p+' '+JSON.stringify(raw));return}
  if(seg[0]==='rep'){if(op==='del'){if(window.__fakeAdmin===true)return;deny('del '+p)}const r=next;
   if(cur||!only(Object.keys(r),['by','who','nk','why','txt','at'])||r.by!==me||!new RegExp('^'+me+'_[0-9]{10,15}$').test(id)||typeof r.who!=='string'||r.who.length>40||r.who===me||!nick(r.nk)
    ||!['abuse','spam','nick','etc'].includes(r.why)||typeof r.txt!=='string'||r.txt.length>2000||!T(r.at))deny('rep '+p+' '+JSON.stringify(raw).slice(0,200));return}
 };
 canRead=function(path,data){const me=uid(),seg=path.split('/');if(!me)return false;
  if(seg[0]==='fp')return !!data&&(data.a===me||data.b===me);
  if(seg[0]==='on'){if(seg[1]===me)return true;const f=store['fp/'+pidOf(seg[1],me)];return !!f&&f.st==='ok'}
  if(seg[0]==='bk')return !!data&&data.by===me;
  if(seg[0]==='rep'||seg[0]==='seen')return window.__fakeAdmin===true;
  if(seg[0]==='on'&&window.__fakeAdmin===true)return true;
  return _canRead1(path,data)};
 // 문서 id('__name__') 조건·정렬
 q=function(Q){const cons=Q.cons||[],nm=cons.filter(c=>c.f==='__name__');if(!nm.length)return _q1(Q);
  const pre=Q.p+'/',rest=cons.filter(c=>c.f!=='__name__'||c.k==='l');let r=_q1({p:Q.p,cons:rest.filter(c=>c.k!=='l')});
  let docs=r.docs.filter(x=>nm.every(c=>c.k!=='w'||(c.o==='>='?x.id>=c.v:c.o==='>'?x.id>c.v:c.o==='<'?x.id<c.v:c.o==='<='?x.id<=c.v:c.o==='=='?x.id===c.v:true)));
  if(nm.some(c=>c.k==='o'))docs.sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0);
  for(const c of cons)if(c.k==='l')docs=docs.slice(0,c.n);return{docs,metadata:r.metadata}};
 // 문서 하나를 구독할 때도 읽기 규칙 확인(on/{친구}는 친구만)
 onSnapshot=function(ref,a,b,c){const isQ=!!(ref.col||ref.cons);if(!isQ&&/^(on|fp|bk|rep)\//.test(ref.p)&&store[ref.p]&&!canRead(ref.p,store[ref.p])){const err=typeof a==='function'?b:c;setTimeout(()=>{(err||(()=>{}))(rdeny(ref.p))},0);return()=>{}}return _onSnap1(ref,a,b,c)};
}

// ---- (새 기능팀 덧붙임) 대국 중 이모트 presence.emo = {k,t}: firestore.rules 의 emoOk/emoChange 흉내 ----
{const _check1=check;
 check=function(op,p,raw,merge){const seg=p.split('/');
  if(seg[0]==='rt'&&op!=='del'&&raw&&raw.presence&&typeof raw.presence==='object'){const cur=store[p],P=raw.presence,now=Date.now();
   if(seg[3]!==uid())deny(op+' '+p);
   const okKeys=Object.keys(P).every(k=>['seat','mm','emo'].includes(k));if(!okKeys)deny('rt keys '+p+' '+JSON.stringify(raw));
   const had=!!(cur&&cur.presence&&'emo' in cur.presence),has='emo' in P,e=P.emo;
   if(!cur&&has)deny('rt create emo '+p);
   if(has||had){const same=has&&had&&JSON.stringify(cur.presence.emo)===JSON.stringify(e);
    if(!same){if(!has)deny('rt emo remove '+p);
     const ok=/^g-g[0-9a-f]{8}$/.test(seg[1])&&e&&typeof e==='object'&&Object.keys(e).every(k=>['k','t'].includes(k))&&Number.isInteger(e.k)&&e.k>=0&&e.k<12&&Number.isInteger(e.t)&&e.t>now-600000&&e.t<now+60000&&(!had||e.t>=cur.presence.emo.t+6000);
     if(!ok)deny('rt emo '+p+' '+JSON.stringify(e))}}
   const rest=Object.assign({},raw,{presence:Object.fromEntries(Object.entries(P).filter(([k])=>k!=='emo'))});return _check1(op,p,rest,merge)}
  return _check1(op,p,raw,merge)}}

// ---- (재화·상점 1단계 덧붙임) wal/{uid} 구슬 지갑, res·bres·rt·on 공개 장착 eq: firestore.rules 의 wal*/eqPub 흉내 ----
{const _check2=check,_canRead2=canRead;
 const PRICE={t1:800,t2:800,t3:800,n1:1200,n2:1200,n3:1200,f1:1500,f2:1500,f3:1500,s1:1200,s2:1200,s3:1200,w1:2500,w2:2500,b1:3000,b2:3000,x1:3500,x2:3500};
 const ACH={a_link:50,a_place:50,a_ai1:50,a_ai2:80,a_ai3:120,a_ai4:300},PAMT=[0,50,100,150,200,300,300],SAMT=[200,400,700,1000,1400,1800,2500];
 const kday=()=>Math.floor((Date.now()+32400000)/864e5),seasonNow=()=>Date.now()<1803567600000?1:2+Math.floor((Date.now()-1803567600000)/7889400000);
 const isL=a=>Array.isArray(a),hasAll=(a,b)=>b.every(x=>a.includes(x)),uniq=a=>new Set(a).size===a.length;
 const eqPub=v=>{if(typeof v!=='string'||v.length>64||!/^[a-z0-9_.]*$/.test(v))return false;if(v==='')return true;const w=store['wal/'+uid()];return !!w&&isL(w.own)&&hasAll(w.own,v.split('.'))};
 const slot=(e,k,re)=>!(k in e)||e[k]===''||re.test(e[k]);
 const shape=n=>{const K=['g','d','dc','dq','own','eq','cl','k','at'];return Object.keys(n).every(k=>K.includes(k)||['ck','nc','am','ad'].includes(k))&&(!('am' in n)||int(n.am))&&(!('ad' in n)||(isL(n.ad)&&n.ad.length<=31))&&K.every(k=>k in n)&&(!('ck' in n)||(int(n.ck)&&n.ck>=0&&n.ck<=6))&&(!('nc' in n)||(int(n.nc)&&n.nc>=0&&n.nc<=9999))&&int(n.g)&&n.g>=0&&n.g<=99999&&n.d===kday()&&int(n.dc)&&n.dc>=0&&n.dc<=150
  &&isL(n.dq)&&n.dq.length<=5&&uniq(n.dq)&&n.dq.every(x=>['w','m0','m1','m2','c'].includes(x))&&isL(n.own)&&n.own.length<=300&&uniq(n.own)&&isL(n.cl)&&n.cl.length<=400
  &&n.eq&&typeof n.eq==='object'&&!isL(n.eq)&&Object.keys(n.eq).every(k=>['t','n','f','s','w','b','x'].includes(k))&&hasAll(n.own.concat(['']),Object.values(n.eq))
  &&slot(n.eq,'t',/^(t[0-9]{1,2}|zt[0-9]{1,3}_[56])$/)&&slot(n.eq,'n',/^(n[0-9]{1,2}|zn[0-9]{1,3})$/)&&slot(n.eq,'f',/^(f[0-9]{1,2}|z[0-9]{1,3}_[0-6])$/)&&slot(n.eq,'s',/^s[0-9]{1,2}$/)&&slot(n.eq,'w',/^w[0-9]{1,2}$/)&&slot(n.eq,'b',/^b[0-9]{1,2}$/)&&slot(n.eq,'x',/^x[0-9]{1,2}$/)};
 const dcOld=o=>o.d===kday()?o.dc:0,dqOld=o=>o.d===kday()?o.dq:[],same=(o,n)=>n.dc===dcOld(o)&&eq(n.dq,dqOld(o));
 const earn=(o,n)=>{const dl=n.g-o.g,wN=n.dq.includes('w')&&!dqOld(o).includes('w')?1:0,ad=n.dq.length-dqOld(o).length;return hasAll(n.dq,dqOld(o))&&dl>=0&&n.dc===dcOld(o)+dl&&(dl>0||ad>0)&&dl<=15+20*wN+10*(ad-wN)&&eq(n.own,o.own)&&eq(n.cl,o.cl)&&(!n.dq.includes('c')||dqOld(o).includes('c'))};
 const attAmt=k=>k===7||k===14?50:k===21?80:k===28?120:10;
 const att=(o,n)=>{const t=new Date(Date.now()+32400000),m=t.getUTCFullYear()*100+t.getUTCMonth()+1,d=t.getUTCDate(),old=o.am===m&&isL(o.ad)?o.ad:[];return !old.includes(d)&&n.am===m&&eq(n.ad,old.concat([d]))&&n.g===o.g+attAmt(old.length+1)&&eq(n.own,o.own)&&eq(n.cl,o.cl)&&eq(n.eq,o.eq)&&same(o,n)};
 const rwItems=(sn,t)=>t===4?['z'+sn+'_4','zn'+sn]:t>=5?['z'+sn+'_'+t,'zt'+sn+'_'+t]:['z'+sn+'_'+t];
 const seasonRw=(o,n,key)=>{const sn=parseInt(key.slice(1)),sd=store['cfg/season'+sn];if(!sd||!sd.p)return false;const v=sd.p[uid()];if(!isL(v))return false;const amt=(isL(sd.amt)?sd.amt:SAMT)[v[0]];
  return sd.n===sn&&v[2]>=10&&int(amt)&&amt>=0&&amt<=2500&&n.g===o.g+amt&&eq(n.own,o.own.concat(rwItems(sn,v[0])))};
 const claim=(o,n)=>{const key=n.cl[n.cl.length-1];if(typeof key!=='string'||!eq(n.cl,o.cl.concat([key]))||o.cl.includes(key)||!same(o,n))return false;
  if(/^p[0-9]{1,3}_[1-6]$/.test(key))return parseInt(key.slice(1))<=seasonNow()&&n.g===o.g+PAMT[+key.split('_')[1]]&&eq(n.own,o.own);
  if(key in ACH)return (key!=='a_link'||google())&&n.g===o.g+ACH[key]&&eq(n.own,o.own);
  if(/^s[0-9]{1,3}$/.test(key))return seasonRw(o,n,key);return false};
 const buy=(o,n)=>{const it=n.own[n.own.length-1];return eq(n.own,o.own.concat([it]))&&!o.own.includes(it)&&it in PRICE&&(o.g-n.g===PRICE[it]||(window.__fakeAdmin===true&&n.g===o.g))&&eq(n.cl,o.cl)&&same(o,n)};
 const equip=(o,n)=>n.g===o.g&&eq(n.own,o.own)&&eq(n.cl,o.cl)&&same(o,n);
 const reset=(o,n)=>n.g===0&&eq(n.own,[])&&eq(n.eq,{})&&eq(n.cl,o.cl)&&same(o,n);
 window.__walDeny=[];
 check=function(op,p,raw,merge){const seg=p.split('/'),me=uid(),cur=store[p];
  if(seg[0]==='wal'&&seg.length===2){if(!me||seg[1]!==me||op==='del')deny(op+' '+p);const n=merge?deep(clone(cur)||{},clone(fillST(raw,Date.now()))):clone(fillST(raw,Date.now()));
   const atOk=raw&&isST(raw.at);let ok=atOk&&shape(n);
   if(ok&&!cur)ok=n.k==='new'&&n.g===0&&n.dc===0&&eq(n.dq,[])&&eq(n.own,[])&&eq(n.cl,[])&&eq(n.eq,{});
   else if(ok)ok=(n.k==='earn'&&earn(cur,n))||(n.k==='claim'&&claim(cur,n))||(n.k==='buy'&&buy(cur,n))||(n.k==='equip'&&equip(cur,n))||(n.k==='reset'&&reset(cur,n))||(n.k==='att'&&att(cur,n))||(n.k==='nick'&&(()=>{const c0=cur.nc||0;return n.nc===c0+1&&n.g===cur.g-(c0>=1&&window.__fakeAdmin!==true?500:0)&&eq(n.own,cur.own)&&eq(n.cl,cur.cl)&&eq(n.eq,cur.eq)&&same(cur,n)})());if(ok&&cur&&n.k!=='nick'&&(n.nc||0)!==(cur.nc||0))ok=false;if(ok&&cur&&((n.ck||0)!==(cur.ck||0)||(n.k!=='att'&&((n.am||0)!==(cur.am||0)||!eq(n.ad||[],cur.ad||[])))))ok=false;
   if(!ok){window.__walDeny.push((n&&n.k)+' '+JSON.stringify(raw).slice(0,240));deny('wal '+p+' '+JSON.stringify(raw).slice(0,200))}return}
  if((seg[0]==='res'||seg[0]==='bres')&&op==='set'&&raw&&typeof raw==='object'&&'eq' in raw){if(!eqPub(raw.eq))deny(seg[0]+' eq '+p);const r2=Object.assign({},raw);delete r2.eq;return _check2(op,p,r2,merge)}
  if(seg[0]==='rt'&&op!=='del'&&raw&&raw.presence&&typeof raw.presence==='object'&&'eq' in raw.presence){const P=raw.presence,same2=cur&&cur.presence&&cur.presence.eq===P.eq;if(!same2&&!eqPub(P.eq))deny('rt eq '+p);
   const r2=Object.assign({},raw,{presence:Object.fromEntries(Object.entries(P).filter(([k])=>k!=='eq'))});const sv=cur&&cur.presence&&'eq' in cur.presence?cur.presence.eq:undefined;if(sv!==undefined)delete cur.presence.eq;try{return _check2(op,p,r2,merge)}finally{if(sv!==undefined)cur.presence.eq=sv}}
  if(seg[0]==='on'&&seg.length===2&&op!=='del'&&raw&&typeof raw==='object'){const has='eq' in raw,sv=cur&&'eq' in cur?cur.eq:undefined;if(has&&(!cur||cur.eq!==raw.eq)&&!eqPub(raw.eq))deny('on eq '+p);
   if(has||sv!==undefined){const r2=Object.assign({},raw);delete r2.eq;if(sv!==undefined)delete cur.eq;try{return _check2(op,p,r2,merge)}finally{if(sv!==undefined&&store[p]===cur)cur.eq=sv}}}
  return _check2(op,p,raw,merge)};
 canRead=function(path,data){const seg=path.split('/');if(seg[0]==='wal')return !!uid()&&seg[1]===uid();return _canRead2(path,data)}}

// ---- (관전 기능팀 덧붙임) firestore.rules 의 관전 규칙 흉내: g/*/p 읽기 강화(두 사람·끝난 판·관전 허용 친구), lv 중계·lv/*/w 관전자,
//      on 의 st 'a'·gi·al·sp, rt presence.wn. 같은 폴더의 firestore.rules 에 관전 규칙(watchOk)이 있을 때만 켜짐(예전 웹 폴더 테스트는 그대로)
{const _check3=check,_canRead3=canRead,_onSnap3=onSnapshot;let SPEC=null;
 // 첫 쓰기(앱을 열자마자 쓰는 접속 표시)보다 먼저 정해지도록 동기로 읽음
 try{const x=new XMLHttpRequest();x.open('GET','firestore.rules',false);x.send();SPEC=x.status===200&&x.responseText.includes('function watchOk(')}catch(e){SPEC=false}
 const on=()=>SPEC===true,pidOf=(x,y)=>x<y?x+'_'+y:y+'_'+x;
 const watchOk=u=>{const me=uid();if(typeof u!=='string'||!u||u===me)return false;const f=store['fp/'+pidOf(u,me)];if(!f||f.st!=='ok')return false;const o=store['on/'+u];return !o||(o.sp!==false&&o.hs!==true)};
 const lvOk=d=>{const K=['v','id','k','at','na','nb','me','al','t','ph','sun','c','h','w','why'];
  return !!d&&only(Object.keys(d),K)&&['v','id','k','at','na','nb','me','t','ph','h'].every(k=>k in d)&&d.v===1&&typeof d.id==='string'&&/^[0-9a-f]{8}$/.test(d.id)&&['a','r'].includes(d.k)
   &&nick(d.na)&&nick(d.nb)&&['A','B'].includes(d.me)&&int(d.t)&&d.t>=0&&d.t<=400&&['designate','bet','live','over'].includes(d.ph)&&typeof d.h==='string'&&d.h.length<=4400&&/^[A-Ba-s,]*$/.test(d.h)
   &&(!('al' in d)||(d.k==='a'&&typeof d.al==='string'&&/^[a-z]{0,12}$/.test(d.al)))&&(!('sun' in d)||(d.k==='a'&&['A','B'].includes(d.sun)))
   &&(!('c' in d)||(d.k==='a'&&typeof d.c==='string'&&/^[a-s]{6}$/.test(d.c)))&&(!('w' in d)||['A','B','D',''].includes(d.w))&&(!('why' in d)||(typeof d.why==='string'&&d.why.length<=20))};
 window.__lvWrites=0;window.__lvwWrites=0;window.__onWrites=0;
 check=function(op,p,raw,merge){if(!on())return _check3(op,p,raw,merge);const seg=p.split('/'),me=uid(),cur=store[p];
  if(seg[0]==='lv'){if(!me)deny(op+' '+p);const G2=google();
   if(seg.length===2){if(op==='del'){if(seg[1]===me)return;deny('lv del '+p)}
    if(!(G2&&seg[1]===me&&isST(raw&&raw.at)&&!merge&&lvOk(fillST(raw,Date.now()))))deny('lv '+p+' '+JSON.stringify(raw).slice(0,200));window.__lvWrites++;return}
   if(seg.length===4&&seg[2]==='w'){const u=seg[1],x=seg[3];if(op==='del'){if(x===me||u===me)return;deny('lv w del '+p)}
    const ok=G2&&x===me&&watchOk(u)&&raw&&only(Object.keys(raw),['at'])&&isST(raw.at)&&(!cur||(int(cur.at)&&cur.at<Date.now()-30000));
    if(!ok)deny('lv w '+p+' '+JSON.stringify(raw));window.__lvwWrites++;return}
   deny('lv '+p)}
  if(seg[0]==='on'&&seg.length===2&&op!=='del'&&raw&&typeof raw==='object'){const n=Object.assign({},cur||{},raw);
   if(!['on','off','g','r','a'].includes(n.st)||('gi' in n&&!(typeof n.gi==='string'&&/^(g[0-9a-f]{8})?$/.test(n.gi)))||('al' in n&&!(typeof n.al==='string'&&/^[a-z]{0,12}$/.test(n.al)))||('sp' in n&&typeof n.sp!=='boolean'))deny('on spec '+p+' '+JSON.stringify(raw));
   const r2=Object.assign({},raw);delete r2.gi;delete r2.al;delete r2.sp;if(r2.st==='a')r2.st='on';
   const sv={};if(cur)for(const k of ['gi','al','sp','st'])if(k in cur)sv[k]=cur[k];if(cur){delete cur.gi;delete cur.al;delete cur.sp;if(cur.st==='a')cur.st='on'}
   try{const r=_check3(op,p,r2,merge);window.__onWrites++;return r}finally{if(cur&&store[p]===cur)Object.assign(cur,sv)}}
  if(seg[0]==='rt'&&op!=='del'&&raw&&raw.presence&&typeof raw.presence==='object'&&('wn' in raw.presence||(cur&&cur.presence&&'wn' in cur.presence))){const P=raw.presence;
   if('wn' in P&&!(int(P.wn)&&P.wn>=0&&P.wn<=50))deny('rt wn '+p+' '+JSON.stringify(raw));
   const r2=Object.assign({},raw,{presence:Object.fromEntries(Object.entries(P).filter(([k])=>k!=='wn'))});const sv=cur&&cur.presence&&'wn' in cur.presence?cur.presence.wn:undefined;if(sv!==undefined)delete cur.presence.wn;
   try{return _check3(op,p,r2,merge)}finally{if(sv!==undefined&&cur.presence&&!('wn' in cur.presence))cur.presence.wn=sv}}
  return _check3(op,p,raw,merge)};
 canRead=function(path,data){if(!on())return _canRead3(path,data);const me=uid(),seg=path.split('/');if(!me)return false;
  if(seg[0]==='lv'){if(seg.length===2)return seg[1]===me||watchOk(seg[1]);if(seg[2]==='w')return seg[1]===me||seg[3]===me;return false}
  if(seg[0]==='g'&&seg[2]==='p'&&seg.length===4){const g=store['g/'+seg[1]];if(!g)return false;
   return ['open','done'].includes(g.status)||g.host===me||g.guest===me||(window.__fakeAdmin===true&&google()&&(g.created??Date.now())<Date.now()-864e5)||(g.ranked!==true&&(watchOk(g.host)||watchOk(g.guest||'')))}
  return _canRead3(path,data)};
 onSnapshot=function(ref,a,b,c){const isQ=!!(ref.col||ref.cons);
  if(on()){const err=typeof a==='function'?b:c,fail=pp=>{setTimeout(()=>{(err||(()=>{}))(rdeny(pp))},0);return()=>{}};
   if(!isQ&&/^lv\//.test(ref.p)&&store[ref.p]&&!canRead(ref.p,store[ref.p]))return fail(ref.p);
   // 실제 Firestore 처럼 문서가 없어도 규칙으로 막히는 구독은 거부(방이 있는데 관전 권한 없는 g/*/p, 남의 lv/*/w)
   if(isQ&&/^g\/g[0-9a-f]{8}\/p$/.test(ref.p)&&store[ref.p.slice(0,-2)]&&!canRead(ref.p+'/x',null))return fail(ref.p);
   if(isQ&&/^lv\/[^/]+\/w$/.test(ref.p)&&ref.p.split('/')[1]!==uid())return fail(ref.p)}
  return _onSnap3(ref,a,b,c)};
 // 문서가 없어도 규칙 검사(실제 Firestore와 같게): lv·g/*/p 단건 읽기
 const _getDoc3=getDoc;getDoc=async function(r){await ready;if(on()&&(/^lv\//.test(r.p)||/^g\/[^/]+\/p\//.test(r.p))&&!store[r.p]&&!canRead(r.p,null))throw rdeny(r.p);return _getDoc3(r)};
 window.__specRulesOn=()=>on()}
