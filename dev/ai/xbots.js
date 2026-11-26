// 사람이 쓸 법한 공략 봇들. 공개 정보(판, 세 칸, 턴, 선/후, 돌 결과)와 자기 정보(자기 점수·입찰)만 씀.
// AI 점수는 '확실한 상한'을 돌 결과로 직접 계산(사람도 종이에 적으면 할 수 있는 계산).
function X(TOOL,seed,col,opt){
 let s=(seed*2654435761>>>0)||7;const rnd=()=>{s=(s*1103515245+12345)>>>0;return s/4294967296};
 const W=TOOL.AI_WIN,N=19,oc=3-col;let aiLow=0,lastAI=null;const hist=[];
 const aiMax=g=>Math.max(1,10*g.t-aiLow); // 이번 턴 AI가 가진 최대 점수
 const inB=(r,c)=>r>=0&&r<N&&c>=0&&c<N;
 const near=(bd,r,c,d)=>{for(let y=r-d;y<=r+d;y++)for(let x=c-d;x<=c+d;x++)if(inB(y,x)&&bd[y][x])return true;return false};
 function windows(bd,cl){let t3=0,t4=0;for(const [dr,dc] of TOOL.DIRS)for(let r=0;r<N;r++)for(let c=0;c<N;c++){const r4=r+4*dr,c4=c+4*dc;if(!inB(r4,c4))continue;let k=0,bad=false;for(let j=0;j<5;j++){const v=bd[r+j*dr][c+j*dc];if(v===3-cl){bad=true;break}if(v===cl)k++}if(bad)continue;const y0=r-dr,x0=c-dc,y1=r4+dr,x1=c4+dc;if((inB(y0,x0)&&bd[y0][x0]===cl)||(inB(y1,x1)&&bd[y1][x1]===cl))continue;if(k===4)t4++;else if(k===3)t3++}return{t3,t4}}
 function fiveSpots(bd,cl){const out=new Set();for(let r=0;r<N;r++)for(let c=0;c<N;c++)if(!bd[r][c]){bd[r][c]=cl;if(TOOL.aiIsFive(bd,r,c,cl))out.add(r*N+c);bd[r][c]=0}return out}
 function designate(g){const bd=g.bd.map(r=>r.slice()),any=bd.some(r=>r.some(x=>x));
  let cand=TOOL.legalTriples(bd).filter(t=>any?t.some(([r,c])=>near(bd,r,c,1)):t.every(([r,c])=>Math.abs(r-9)<=1&&Math.abs(c-9)<=1));
  if(opt.near&&lastAI){const c2=cand.filter(t=>t.some(([r,c])=>lastAI.some(([y,x])=>Math.abs(y-r)<=1&&Math.abs(x-c)<=1)));if(c2.length)cand=c2}
  if(!cand.length)cand=TOOL.legalTriples(bd);
  const my5=fiveSpots(bd,col),op5=fiveSpots(bd,oc);let best=null,bv=-1e18;
  for(const t of cand){let sc=0;const n5=t.filter(([r,c])=>my5.has(r*N+c)).length,o5=t.filter(([r,c])=>op5.has(r*N+c)).length;
   for(const [r,c] of t)bd[r][c]=col;const w=windows(bd,col);for(const [r,c] of t)bd[r][c]=0;
   sc=w.t4*(opt.w4||300)+w.t3*40+n5*(opt.f5||2000)-o5*(opt.avoidOpp5||0)+rnd()*30;
   if(sc>bv){bv=sc;best=t}}
  return best}
 function bid(g,cells){const pts=g.pts[col],sun=g.sun===col,bd=g.bd.map(r=>r.slice());
  const V=TOOL.aiOutcomes2(bd,cells,col,sun,!sun),M=aiMax(g),beat=M+(sun?1:0)-1; // beat=AI 최대 걸 수 있는 한 칸 금액 이상(후면 동점=내 승)
  const one=Math.max(1,M-2)+(sun?1:0); // AI가 한 칸에 걸 수 있는 최대(M-2)를 확실히 이기는 금액
  const neg=[],pos=[];for(let m=0;m<8;m++){if(V[m]<=-W)neg.push(m);else if(V[m]>=W)pos.push(m)}
  const pc=m=>(m&1)+((m>>1)&1)+((m>>2)&1),b=[1,1,1];
  const fit=x=>{x=x.map(v=>Math.max(1,Math.round(v)));while(x[0]+x[1]+x[2]>pts){const i=x.indexOf(Math.max(...x));if(x[i]<=1)break;x[i]--}return x};
  if(pos.length||neg.length){
   // 한 칸으로 이기는 칸(막기와 겹치지 않으면 공격)
   const single=[0,1,2].filter(i=>pos.includes(1<<i)&&neg.every(m=>!((m>>i)&1))||pos.includes(1<<i)&&!neg.length);
   if(single.length){const i=single.length>1&&opt.split?null:single[Math.floor(rnd()*single.length)];
    if(i===null){ // 두 칸 다 오목: 둘에 나눔(AI는 둘 다 막아야 함)
     let left=pts-3;single.forEach((j,k)=>{const q=Math.floor(left/(single.length-k));b[j]+=q;left-=q});return fit(b)}
    b[i]=opt.exact&&one<=pts-2?one:pts-2;return fit(b)}
   if(neg.length){const H=[0,1,2].filter(i=>neg.every(m=>!((m>>i)&1)));
    if(H.length){const i=H[Math.floor(rnd()*H.length)];b[i]=opt.exact&&one<=pts-2?one:pts-2;return fit(b)}
    const need=[0,1,2].filter(i=>neg.some(m=>!((m>>i)&1)));let left=pts-3;need.forEach((j,k)=>{const q=Math.floor(left/(need.length-k));b[j]+=q;left-=q});return fit(b)}
   if(pos.length){const S=pos.slice().sort((a,c)=>pc(a)-pc(c))[0],cs=[0,1,2].filter(i=>(S>>i)&1);
    if(opt.exact&&one*cs.length+(3-cs.length)<=pts){cs.forEach(i=>b[i]=one);return fit(b)}
    let left=pts-3;cs.forEach((j,k)=>{const q=Math.floor(left/(cs.length-k));b[j]+=q;left-=q});return fit(b)}}
  return fit(opt.bid({g,cells,V,pts,sun,rnd,M}))}
 return{designate,bid,observe:(g,bids,won)=>{const sun=g.sun===col;hist.push({t:g.t,sun,bids:bids.slice(),won:won.slice()});
   // AI 지출 하한: 내가 이긴 칸 ≥1, 진 칸은 (AI가 선이면 내 금액+1, AI가 후면 내 금액)
   for(let i=0;i<3;i++)aiLow+=won[i]?1:(sun?bids[i]:bids[i]+1);if(!sun)lastAI=g.cells||null}}}
const imp=V=>[0,1,2].map(i=>{let x=0;for(let m=0;m<8;m++)if((m>>i)&1)x+=Math.abs(V[m]-V[m^(1<<i)]);return x/4});
const B={
 // 점수 몰래 모으기 + 한 칸 오목: 평소 1-1-1, 결정적 칸은 AI 최대 점수 기준 확실한 금액(모자라면 전부)
 snipe:(T,s,c)=>X(T,s,c,{exact:true,bid:()=>[1,1,1]}),
 // 같은 방식인데 결정적 칸은 늘 전부(계산 안 하는 사람)
 snipeAll:(T,s,c)=>X(T,s,c,{bid:()=>[1,1,1]}),
 // 1점씩 깔아 칸 줍기: 후일 때 1-1-1(AI가 1점 건 칸은 동점으로 내 것), 선일 때 중요한 칸 2~3
 pick1:(T,s,c)=>X(T,s,c,{exact:true,bid:({sun,V,rnd})=>{if(!sun)return[1,1,1];const I=imp(V),o=[0,1,2].sort((a,b)=>I[b]-I[a]),b=[2,2,1];b[o[0]]=2+Math.floor(rnd()*2);b[o[1]]=2;return [b[0],b[1],b[2]]}}),
 // 동점 노리기: 후일 때 AI가 자주 쓰는 금액(2·3·5)과 똑같이, 선일 때 +1
 tie:(T,s,c)=>X(T,s,c,{exact:true,bid:({sun,V,rnd,pts})=>{const I=imp(V),o=[0,1,2].sort((a,b)=>I[b]-I[a]),b=[1,1,1];const base=[3,2,1];o.forEach((i,r)=>b[i]=base[r]+(sun?1:0));if(pts>80&&rnd()<.4)b[o[0]]+=3;return b}}),
 // AI가 지정한 칸 근처로 줄 만들기 + 확실한 금액 공격
 near:(T,s,c)=>X(T,s,c,{exact:true,near:true,bid:({sun})=>sun?[2,2,2]:[1,1,1]}),
 // 열린 4 만들기(한 칸 오목 자리 두 개) 지정 + 두 자리 나눠 걸기
 double:(T,s,c)=>X(T,s,c,{exact:true,w4:900,split:true,bid:()=>[1,1,1]}),
 // 보통 사람: 중요한 칸에 적당히(점수의 10~30%), 결정적 칸은 확실 금액
 normal:(T,s,c)=>X(T,s,c,{exact:true,bid:({V,pts,rnd,sun})=>{const I=imp(V),o=[0,1,2].sort((a,b)=>I[b]-I[a]),b=[1,1,1];b[o[0]]=1+Math.floor(pts*(.1+.2*rnd()));b[o[1]]=1+Math.floor(pts*.08*rnd());if(!sun&&rnd()<.3)return[1,1,1];return b}}),
};
// 섞어 쓰는 사람: 판마다 위 전략 중 하나
B.mixed=(T,s,c)=>{const ks=['snipe','pick1','tie','near','double','normal'];return B[ks[(s>>>3)%ks.length]](T,s,c)};
module.exports=B;
// ===== 'Ultimate 머리 + 사람 꼼수' 봇: 지정·평소 입찰은 배포본 Ultimate(별도 인스턴스, 자기 정보만), 위에 사람 꼼수를 얹음 =====
// 사람보다 강한 상한선 대용(공간 판단이 AI 수준인 숙련자). trick: count(결정적 칸 확실 금액), hoard(평소 덜 쓰기), pick1(후일 때 작은 칸 1점)
function UH(T,seed,col,tricks){const H=require('./h.js'),M=H.load(process.env.UHAI||undefined),mem=M.aiNewMem(seed+77),inner=X(T,seed,col,{exact:true,bid:()=>[1,1,1]});
 const view=(g,e)=>Object.assign({level:'ultimate',bd:g.bd.map(r=>r.slice()),t:g.t,aiSun:g.sun===col,aiPts:g.pts[col],aiCol:col,mem},e||{});
 return{designate:g=>M.aiDesignate(view(g)),
  bid:(g,cells)=>{const pts=g.pts[col],sun=g.sun===col;const V=T.aiOutcomes2(g.bd.map(r=>r.slice()),cells,col,sun,!sun);const crit=V.some(x=>Math.abs(x)>=T.AI_WIN);
   let b=M.aiBid(view(g,{cells}));
   if(crit&&tricks.includes('count'))return inner.bid(g,cells);
   if(crit&&tricks.includes('allin')){const neg=[],pos=[];for(let m=0;m<8;m++){if(V[m]<=-T.AI_WIN)neg.push(m);else if(V[m]>=T.AI_WIN)pos.push(m)}
    const one=[0,1,2].filter(i=>pos.includes(1<<i)&&neg.every(m=>!((m>>i)&1))),Hh=[0,1,2].filter(i=>neg.length&&neg.every(m=>!((m>>i)&1)));
    const pick=one.length?one:Hh;if(pick.length){const o=[1,1,1];o[pick[Math.floor(Math.random()*pick.length)]]=pts-2;return o}}
   if(!crit&&tricks.includes('hoard')){b=b.map(x=>Math.max(1,Math.round(x*.5)))}
   if(!crit&&tricks.includes('pick1')&&!sun){b=b.map(x=>x<=3?1:x)}
   return b},
  observe:(g,bids,won)=>{M.aiObserve(mem,g.t,g.sun===col,bids,won);inner.observe(g,bids,won)}}}
B.uh=(T,s,c)=>UH(T,s,c,[]);
B.uhCount=(T,s,c)=>UH(T,s,c,['count']);
B.uhHoard=(T,s,c)=>UH(T,s,c,['count','hoard']);
B.uhSave=(T,s,c)=>UH(T,s,c,['hoard']);
B.uhAllin=(T,s,c)=>UH(T,s,c,['allin']);
B.uhSaveAllin=(T,s,c)=>UH(T,s,c,['hoard','allin']);
B.uhP1=(T,s,c)=>UH(T,s,c,['pick1']);
B.uhPick=(T,s,c)=>UH(T,s,c,['count','pick1']);
module.exports=B;
