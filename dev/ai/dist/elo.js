// AI 100명이 모두 1000점에서 시작해 서로 랭크전을 계속 둘 때 점수 분포가 어떻게 되는지(엘로, 앱과 같은 K·티어 기준)
// node dist/elo.js '<승률표 JSON>' [일수] [시간당 판 수] [씨앗]
const P=JSON.parse(process.argv[2]),DAYS=+process.argv[3]||365,GPH=+process.argv[4]||6;let seed=+process.argv[5]||7;
const rnd=()=>{seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296};
const LV=['beginner','mid','pro','ultimate'],CNT=JSON.parse(process.env.CNT||'[29,34,22,15]');
const bots=[];LV.forEach((l,i)=>{for(let k=0;k<CNT[i];k++)bots.push({lv:i,r:+(process.env.S0||1000),g:0})});
const kOf=g=>g<10?40:+(process.env.K||32),exp=(a,b)=>1/(1+Math.pow(10,(b-a)/400));
const TI=[['브론즈',0],['실버',900],['골드',1100],['플래티넘',1300],['다이아',1500],['마스터',1700]];
const tierOf=(r,rank)=>{if(r>=1700&&rank<3)return'챌린저';let t='브론즈';for(const [n,m] of TI)if(r>=m)t=n;return t};
const win=(a,b)=>a===b?.5:a>b?P[LV[a]+'>'+LV[b]]:1-P[LV[b]+'>'+LV[a]];
function report(day){const s=bots.slice().sort((a,b)=>b.r-a.r),c={};s.forEach((b,i)=>{const t=tierOf(b.r,i);c[t]=(c[t]||0)+1});
 const m=LV.map((l,i)=>{const x=bots.filter(b=>b.lv===i).map(b=>b.r);const av=x.reduce((a,b)=>a+b,0)/x.length;return `${l} 평균 ${Math.round(av)} (${Math.round(Math.min(...x))}~${Math.round(Math.max(...x))})`});
 const order=['챌린저','마스터','다이아','플래티넘','골드','실버','브론즈'].map(k=>`${k} ${c[k]||0}`).join(' · ');
 console.log(`${day}일: ${order}\n   ${m.join(' | ')}`)}
// 티어별 비대칭(환경변수 ASYM=1): 높은 티어는 덜 오르고 더 떨어짐, 낮은 티어는 반대
const AW=JSON.parse(process.env.AW||'[1.4,1.2,1.0,1.0,0.8,0.6]'),AL=JSON.parse(process.env.AL||'[0.6,0.8,1.0,1.0,1.2,1.4]'),TIX=r=>r<900?0:r<1100?1:r<1300?2:r<1500?3:r<1700?4:5;
const TM=(r,d)=>process.env.ASYM?(d>0?AW[TIX(r)]:AL[TIX(r)]):1;
const marks=new Set([1,3,7,14,30,60,90,180,365,730,1095].filter(d=>d<=DAYS));
for(let h=0;h<DAYS*24;h++){
 for(let j=0;j<GPH;j++){const i=Math.floor(rnd()*bots.length),a=bots[i];
  // 매칭처럼 지금 점수가 가까운 6명 중 한 명과
  const near=bots.map((b,k)=>[k,Math.abs(b.r-a.r)]).filter(([k])=>k!==i).sort((x,y)=>x[1]-y[1]).slice(0,6),b=bots[near[Math.floor(rnd()*6)][0]];
  const pa=win(a.lv,b.lv),s=rnd()<pa?1:0,e=exp(a.r,b.r),ka=kOf(a.g),kb=kOf(b.g);const da=ka*(s-e),db=kb*((1-s)-(1-e));a.r+=da*TM(a.r,da);b.r+=db*TM(b.r,db);a.g++;b.g++}
 if((h+1)%24===0&&marks.has((h+1)/24))report((h+1)/24)}
