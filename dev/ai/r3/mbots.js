// 실제 기록(aigames_1126) 사람 흉내 봇. 공개 정보 + 자기 점수·입찰만 씀(AI 점수·입찰은 안 읽음).
// 특징: AI가 선인 턴엔 대부분 1-1-1로 모음(동점이면 후인 사람이 가져감), 내 선이면 줄 키우는 세 칸에 고르게 절반 넘게,
// '세 칸 다 가져가면 오목'인 세 칸이 있으면 내 선에 지정하고 전부 고르게 검. AI 오목 위협은 한 칸에 몰아 막음.
function MK(T,seed,col,o){
 let s=(seed*2654435761>>>0)||7;const rnd=()=>{s=(s*1103515245+12345)>>>0;return s/4294967296};
 const W=T.AI_WIN,N=19,oc=3-col;const inB=(r,c)=>r>=0&&r<N&&c>=0&&c<N;
 const near=(bd,r,c,d)=>{for(let y=r-d;y<=r+d;y++)for(let x=c-d;x<=c+d;x++)if(inB(y,x)&&bd[y][x])return true;return false};
 const five=(bd,cs,cl)=>{cs.forEach(([r,c])=>bd[r][c]=cl);const f=cs.some(([r,c])=>T.aiIsFive(bd,r,c,cl));cs.forEach(([r,c])=>bd[r][c]=0);return f};
 // cl 기준 '한 턴 오목 창'(빈칸 e개, 빈칸 폭 3 이하) 개수: e=3·2·1
 function wins(bd,cl){const cnt=[0,0,0,0];for(const [dr,dc] of T.DIRS)for(let r=0;r<N;r++)for(let c=0;c<N;c++){if(!inB(r+4*dr,c+4*dc))continue;let k=0,lo=9,hi=-1,bad=false;
   for(let j=0;j<5;j++){const v=bd[r+j*dr][c+j*dc];if(v===3-cl){bad=true;break}if(v===cl)k++;else{lo=Math.min(lo,j);hi=Math.max(hi,j)}}
   if(bad||k===5)continue;const y0=r-dr,x0=c-dc,y1=r+5*dr,x1=c+5*dc;if((inB(y0,x0)&&bd[y0][x0]===cl)||(inB(y1,x1)&&bd[y1][x1]===cl))continue;const e=5-k;if(e<=3&&hi-lo<=2)cnt[e]++}
  return cnt}
 function designate(g){const bd=g.bd.map(r=>r.slice()),any=bd.some(r=>r.some(x=>x));
  const L=T.legalTriples(bd);
  // 세 칸 다 가져가면 오목(그중 한두 칸으로는 안 되는 것 포함): 바로 노림
  const f3=L.filter(cs=>five(bd,cs,col));
  if(f3.length&&g.pts[col]>=o.minAll)return f3[Math.floor(rnd()*f3.length)];
  let cand=L.filter(t=>any?t.some(([r,c])=>near(bd,r,c,1)):t.every(([r,c])=>Math.abs(r-9)<=1&&Math.abs(c-9)<=1));if(!cand.length)cand=L;
  // AI의 한 턴 오목 창을 막는 지정(상대 위협은 막음): AI 창 빈칸 3개 이하를 줄이는 쪽 가산
  const a0=wins(bd,oc),m0=wins(bd,col);let best=null,bv=-1e18;
  if(cand.length>900){for(let i=cand.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[cand[i],cand[j]]=[cand[j],cand[i]]}cand=cand.slice(0,900)}
  for(const t of cand){t.forEach(([r,c])=>bd[r][c]=col);const m=wins(bd,col),a=wins(bd,oc);t.forEach(([r,c])=>bd[r][c]=0);
   const sc=(m[3]-m0[3])*o.w3+(m[2]-m0[2])*o.w2+(m[1]-m0[1])*o.w1+((a0[1]-a[1])*3+(a0[2]-a[2])*2+(a0[3]-a[3]))*o.wb+rnd()*o.rj;
   if(sc>bv){bv=sc;best=t}}
  return best}
 const fit=(x,pts)=>{x=x.map(v=>Math.max(1,Math.round(v)));while(x[0]+x[1]+x[2]>pts){const i=x.indexOf(Math.max(...x));if(x[i]<=1)break;x[i]--}return x};
 function bid(g,cells){const pts=g.pts[col],sun=g.sun===col,bd=g.bd.map(r=>r.slice());
  const V=T.aiOutcomes2(bd,cells,col,sun,!sun);const neg=[],pos=[];for(let m=0;m<8;m++){if(V[m]<=-W)neg.push(m);else if(V[m]>=W)pos.push(m)}
  const pc=m=>(m&1)+((m>>1)&1)+((m>>2)&1),b=[1,1,1];
  if(pos.length&&(sun||o.huAtk)){ // 내 오목: 필요한 칸에 전부 고르게
   const S=pos.slice().sort((a,c)=>pc(a)-pc(c))[0],cs=[0,1,2].filter(i=>(S>>i)&1);
   if(!neg.length||neg.every(m=>cs.some(i=>(m>>i)&1))){let left=pts-3;cs.forEach((j,k)=>{const q=Math.floor(left/(cs.length-k));b[j]+=q;left-=q});return fit(b,pts)}}
  if(neg.length){const H=[0,1,2].filter(i=>neg.every(m=>!((m>>i)&1)));
   if(H.length){const i=H[Math.floor(rnd()*H.length)];b[i]=Math.max(1,Math.round((pts-2)*o.blk));return fit(b,pts)}
   const need=[0,1,2].filter(i=>neg.some(m=>!((m>>i)&1)));let left=Math.round((pts-3)*o.blk);need.forEach((j,k)=>{const q=Math.floor(left/(need.length-k));b[j]+=q;left-=q});return fit(b,pts)}
  const I=[0,1,2].map(i=>{let x=0;for(let m=0;m<8;m++)if((m>>i)&1)x+=Math.abs(V[m]-V[m^(1<<i)]);return x}),ord=[0,1,2].sort((a,c)=>I[c]-I[a]);
  if(!sun){ // AI 선: 모으기
   if(rnd()<o.p111)return[1,1,1];b[ord[0]]=Math.max(1,Math.round(pts*(o.hk0+o.hk1*rnd())));return fit(b,pts)}
  // 내 선: 점수의 sp0~sp0+sp1 비율을 고르게(가끔 한 칸은 1)
  const sp=Math.max(3,Math.round(pts*(o.sp0+o.sp1*rnd())));const k=rnd()<o.two?2:3;const cs=ord.slice(0,k);let left=sp-3;cs.forEach((j,q)=>{const x=Math.floor(left/(k-q));b[j]+=x;left-=x});return fit(b,pts)}
 return{designate,bid,fit,observe:()=>{}}}
const D={minAll:20,sunK:1.3,w3:60,w2:300,w1:900,wb:150,rj:40,blk:1,p111:.9,hk0:.25,hk1:.3,sp0:.45,sp1:.3,two:.25,huAtk:true};
// 'Ultimate 머리 + 이 사람 습관': 지정·평소 입찰은 별도 Ultimate 인스턴스(자기 정보만), 위에 모으기·세 칸 오목 올인을 얹음
function MU(T,seed,col,o){const H=require('./h.js'),M=H.load(process.env.UHAI||undefined),mem=M.aiNewMem(seed+77),base=MK(T,seed,col,o);
 const view=(g,e)=>Object.assign({level:o.lvl||'ultimate',bd:g.bd.map(r=>r.slice()),t:g.t,aiSun:g.sun===col,aiPts:g.pts[col],aiCol:col,mem},e||{});
 let s=(seed*2246822519>>>0)||9;const rnd=()=>{s=(s*1103515245+12345)>>>0;return s/4294967296};
 const five=(bd,cs,cl)=>{cs.forEach(([r,c])=>bd[r][c]=cl);const f=cs.some(([r,c])=>T.aiIsFive(bd,r,c,cl));cs.forEach(([r,c])=>bd[r][c]=0);return f};
 return{designate:g=>{const bd=g.bd.map(r=>r.slice());if(g.pts[col]>=o.minAll){const f3=T.legalTriples(bd).filter(cs=>five(bd,cs,col));if(f3.length)return f3[Math.floor(rnd()*f3.length)]}return M.aiDesignate(view(g))},
  bid:(g,cells)=>{const pts=g.pts[col],sun=g.sun===col,bd=g.bd.map(r=>r.slice());const V=T.aiOutcomes2(bd,cells,col,sun,!sun);
   const neg=V.some(x=>x<=-T.AI_WIN),pos=V.some(x=>x>=T.AI_WIN);
   const ub=M.aiBid(view(g,{cells}));
   if(pos&&sun&&five(bd,cells,col)&&!neg){const q=Math.floor(pts/3),b=[q,q,q];let r=pts-3*q;for(let i=0;r>0;i=(i+1)%3,r--)b[i]++;return b}
   if(neg)return o.uBlock?ub:base.bid(g,cells);
   if(pos)return o.uAtk?ub:base.bid(g,cells);
   if(!sun&&rnd()<o.p111)return[1,1,1];
   if(sun&&o.sunK!=null)return base.fit(ub.map(x=>x*o.sunK),pts);
   return ub},
  observe:(g,bids,won)=>M.aiObserve(mem,g.t,g.sun===col,bids,won)}}
const B={mimicU:(T,s,c)=>MU(T,s,c,Object.assign({},D,{uBlock:true,uAtk:true},process.env.MIMIC?JSON.parse(process.env.MIMIC):{})),mimic:(T,s,c)=>MK(T,s,c,Object.assign({},D,process.env.MIMIC?JSON.parse(process.env.MIMIC):{}))};
module.exports=B;
