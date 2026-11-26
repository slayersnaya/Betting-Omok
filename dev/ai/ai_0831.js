// ===== AI START =====
// 공정 원칙: AI 함수는 '공개 정보 + AI 자신의 정보'만 받음.
// 받는 것: 판, 지정된 세 칸, 턴, 선/후, AI 자신의 점수, AI 자신의 과거 입찰과 칸별 승패(돌 결과).
// 받지 않는 것: 사람의 입찰액, 사람의 남은 점수. 입찰은 사람이 입력하기 전에 AI가 먼저 봉인함.
const AI_LEVELS={
 // 난이도 회의(11/26, 실사용 '너무 쉽다' 반영): 한 단계씩 올림. AI끼리 다음 단계가 이기는 비율 초보→중수 약 88%, 중수→고수 약 85%, 고수→Ultimate 90%+
 beginner:{name:'초보',rand:.15,noise:.25,infer:false,lamK:.06,top:2,see5:1},
 mid:{name:'중수',rand:.05,noise:.15,infer:false,eval2:true,lamK:.13,top:1,see5:1},
 // 고수: Ultimate 엔진을 약하게(표본·입자 적게, 흔들기, 보험·비축 끔, 점수 더 아낌, 최선 대응 베팅은 80%만)
 pro:{name:'고수',rand:0,noise:1,jitter:.5,bidNoise:.3,res:.3,infer:true,eval2:true,lamK:.8,top:1,see5:1,crit3:1,types:[-2,-3],aib:[0,3000,1000,500],nsK:2,br:true,desp:.5,S:6,np:14,mixT:6,tempo:.45,force:1,brP:.8},
 ultimate:{name:'Ultimate',rand:0,noise:0,jitter:.03,bidNoise:.15,res:.3,infer:true,eval2:true,lamK:.45,top:1,see5:1,crit3:1,types:[-2,-3],aib:[0,3000,1000,500],nsK:2,learn:true,
  // 2세대: 상대 점수 추적(입자 필터) + 최선 대응 + 질 수 있는 판의 보험·비축 + 비슷한 수 섞기
  br:true,desp:.5,ins:1.25,insAdd:3,insSmooth:true,resv:.6,insMax:true,mixT:3,
  // 4세대: 지정할 때 내 줄을 키우는 칸을 더 높이 치고(tempo), 다음 턴 상대의 한 턴 오목 위험을 줄이는 칸을 고름(dThreat)
  tempo:.45,dThreat:.3,
  // 내 한 칸 오목 자리를 지정에 넣어 상대가 막느라 점수를 쓰게 함(눈에 보이는 오목 기회를 그냥 넘기지 않음)
  force:1,
  // 지정 후보를 '판돈이 큰 세 칸' 상위 30개로 좁힘(AI 평가: 강한 상대 승률↑, 더 빠름)
  dPre:30}
};
const AIW=[0,1,8,60,600],AI_WIN=1e6;
function aiRun(bd,r,c,dr,dc,col){let L=1,y=r+dr,x=c+dc;while(inB(y,x)&&bd[y][x]===col){L++;y+=dr;x+=dc}y=r-dr;x=c-dc;while(inB(y,x)&&bd[y][x]===col){L++;y-=dr;x-=dc}return L}
function aiIsFive(bd,r,c,col){return DIRS.some(([dr,dc])=>aiRun(bd,r,c,dr,dc,col)===5)}
// col 돌을 (r,c)에 놓았을 때의 위치 가치(5칸 창 점수 + 다음에 오목이 되는 자리 수). 6목 이상이 되는 창은 무효
function aiCell(bd,r,c,col){
 if(bd[r][c])return 0;const oc=3-col;bd[r][c]=col;let s=0,spots=0;
 for(const [dr,dc] of DIRS){
  const L0=aiRun(bd,r,c,dr,dc,col);
  for(let k=-4;k<=0;k++){let cnt=0,ok=true;for(let j=0;j<5;j++){const y=r+(k+j)*dr,x=c+(k+j)*dc;if(!inB(y,x)||bd[y][x]===oc){ok=false;break}if(bd[y][x]===col)cnt++}
   if(ok){const y0=r+(k-1)*dr,x0=c+(k-1)*dc,y1=r+(k+5)*dr,x1=c+(k+5)*dc;
    if((inB(y0,x0)&&bd[y0][x0]===col)||(inB(y1,x1)&&bd[y1][x1]===col))continue;s+=AIW[Math.min(cnt,4)]}}
  if(L0<5)for(let k=-4;k<=4;k++){if(!k)continue;const y=r+k*dr,x=c+k*dc;if(!inB(y,x)||bd[y][x])continue;bd[y][x]=col;if(aiRun(bd,r,c,dr,dc,col)===5)spots++;bd[y][x]=0}
 }
 bd[r][c]=0;return s+(spots>=2?2e4:spots===1?3e3:0);
}
function aiNear(bd,r,c,d){for(let y=r-d;y<=r+d;y++)for(let x=c-d;x<=c+d;x++)if(inB(y,x)&&bd[y][x])return true;return false}
function aiRng(mem){mem.s=(mem.s*1103515245+12345)>>>0;return mem.s/4294967296}
// 세 칸의 8가지 결과(각 칸을 누가 가져가나)별 AI 입장 가치. bit i=1 이면 AI가 칸 i를 가져감
function aiOutcomes(bd,cells,col,huIsAI,see,rnd){
 const oc=3-col,V=new Array(8);
 for(let m=0;m<8;m++){
  let my=0,op=0,f1=0,f2=0;
  for(let i=0;i<3;i++){const [r,c]=cells[i];const me=(m>>i)&1;const v=aiCell(bd,r,c,me?col:oc);if(me)my+=v;else op+=v;bd[r][c]=me?col:oc}
  for(let i=0;i<3;i++){const [r,c]=cells[i];if((m>>i)&1){if(aiIsFive(bd,r,c,col))f1++}else if(aiIsFive(bd,r,c,oc))f2++}
  for(const [r,c] of cells)bd[r][c]=0;
  if(see<1&&rnd&&rnd()>see){f1=0;f2=0}
  if(f1||f2)V[m]=(f1>f2||(f1===f2&&huIsAI))?AI_WIN:-AI_WIN;
  else V[m]=my-op;
 }
 return V;
}

// 정밀 평가(고수 이상): 세 칸에 닿는 5칸 창들만 다시 계산. '한 턴(세 칸 안)에 채울 수 있는 오목 창'에 큰 가중치
const AIB=[0,3000,500,80];
function aiWinVal(bd,r0,c0,dr,dc,col,nextSun,B,nsK){
 const oc=3-col;let s=0,lo=9,hi=-1;
 for(let j=0;j<5;j++){const v=bd[r0+j*dr][c0+j*dc];if(v===oc)return 0;if(v===col)s++;else{lo=Math.min(lo,j);hi=Math.max(hi,j)}}
 const y0=r0-dr,x0=c0-dc,y1=r0+5*dr,x1=c0+5*dc;
 if((inB(y0,x0)&&bd[y0][x0]===col)||(inB(y1,x1)&&bd[y1][x1]===col))return 0;
 if(s===5)return 0;const e=5-s;let v=AIW[s];
 if(e<=3&&hi-lo<=2)v+=(B||AIB)[e]*(nextSun?(nsK||1.6):1);
 return v;
}
function aiWindows(cells){const seen=new Set(),out=[];
 for(const [r,c] of cells)for(const [dr,dc] of DIRS)for(let k=-4;k<=0;k++){const r0=r+k*dr,c0=c+k*dc,r4=r0+4*dr,c4=c0+4*dc;
  if(!inB(r0,c0)||!inB(r4,c4))continue;const key=r0*N*4+c0*4+DIRS.findIndex(d=>d[0]===dr&&d[1]===dc);if(seen.has(key))continue;seen.add(key);out.push([r0,c0,dr,dc])}
 return out}
function aiOutcomes2(bd,cells,col,aiSun,huIsAI,lv){
 const B=lv&&lv.aib||AIB,nk=lv&&lv.nsK||1.6,ok=lv&&lv.opK||1.1;
 const oc=3-col,W=aiWindows(cells),V=new Array(8);
 // 이번 턴이 끝나면 선이 바뀜: AI가 지금 선이면 다음 선은 상대
 const aiNext=!aiSun;
 const score=()=>{let a=0;for(const [r0,c0,dr,dc] of W)a+=aiWinVal(bd,r0,c0,dr,dc,col,aiNext,B,nk)-aiWinVal(bd,r0,c0,dr,dc,oc,!aiNext,B,nk)*ok;return a};
 const base=score();
 for(let m=0;m<8;m++){
  for(let i=0;i<3;i++){const [r,c]=cells[i];bd[r][c]=(m>>i)&1?col:oc}
  let f1=0,f2=0;for(let i=0;i<3;i++){const [r,c]=cells[i];if((m>>i)&1){if(aiIsFive(bd,r,c,col))f1++}else if(aiIsFive(bd,r,c,oc))f2++}
  V[m]=(f1||f2)?((f1>f2||(f1===f2&&huIsAI))?AI_WIN:-AI_WIN):score()-base;
  for(const [r,c] of cells)bd[r][c]=0;
 }
 return V;
}

// 판 전체에서 col이 '한 턴에 채울 수 있는 오목 창' 중 빈칸이 e개 이하인 창이 있는지(다음 턴 위협)
function aiThreat(bd,col){let best=9;const oc=3-col;
 for(const [dr,dc] of DIRS)for(let r=0;r<N;r++)for(let c=0;c<N;c++){const r4=r+4*dr,c4=c+4*dc;if(!inB(r4,c4))continue;
  let s=0,lo=9,hi=-1,bad=false;for(let j=0;j<5;j++){const v=bd[r+j*dr][c+j*dc];if(v===oc){bad=true;break}if(v===col)s++;else{lo=Math.min(lo,j);hi=Math.max(hi,j)}}
  if(bad||s===5)continue;const y0=r-dr,x0=c-dc,y1=r+5*dr,x1=c+5*dc;if((inB(y0,x0)&&bd[y0][x0]===col)||(inB(y1,x1)&&bd[y1][x1]===col))continue;
  const e=5-s;if(e<=3&&hi-lo<=2&&e<best)best=e}
 return best}
// Ultimate 전용: 오목이 걸린 칸은 원칙대로(방어는 한 칸에 몰기, 공격은 확실할 때만 딱 필요한 만큼, 아니면 섞기)
function aiCritical2(V,v,om,rnd){
 const neg=[],pos=[];for(let m=0;m<8;m++){if(V[m]<=-AI_WIN)neg.push(m);else if(V[m]>=AI_WIN)pos.push(m)}
 if(!neg.length&&!pos.length)return null;
 const pts=v.aiPts,sun=v.aiSun,cap=Math.max(1,om.oppMax-2),g=sun?cap+1:cap,b=[1,1,1];
 const pc=m=>((m&1)+((m>>1)&1)+((m>>2)&1));
 if(neg.length){
  // 내가 이 칸 하나만 가져가도 상대 오목이 모두 막히는 칸들
  const H=[0,1,2].filter(i=>neg.every(m=>!((m>>i)&1)));
  if(H.length){
   // 공격도 되는 칸을 우선, 아니면 무작위(상대가 어느 칸에 몰지 모르게)
   let i=H.find(j=>pos.some(m=>((m>>j)&1)&&pc(m)===1));if(i===undefined)i=H[Math.floor(rnd()*H.length)];
   b[i]=Math.max(1,Math.min(pts-2,g));return b}
  // 두 칸 이상 필요: 남은 점수를 그 칸들에 나눔
  const need=[0,1,2].filter(i=>neg.some(m=>!((m>>i)&1)));let left=pts-3;need.forEach((i,j)=>{const k=Math.floor(left/(need.length-j));b[i]+=k;left-=k});return b;
 }
 // 공격: 가장 적은 칸으로 오목이 되는 조합
 const S=pos.slice().sort((a,b)=>pc(a)-pc(b))[0],cells=[0,1,2].filter(i=>(S>>i)&1),k=cells.length,others=3-k;
 if(pts-others>=g*k){cells.forEach(i=>b[i]=g);return b}
 const edge=(pts-om.oppEst)/6,pAll=1/(1+Math.exp(-edge));
 if(rnd()<pAll||!sun){let left=pts-3;cells.forEach((i,j)=>{const q=Math.floor(left/(k-j));b[i]+=q;left-=q});return b}
 cells.forEach(i=>b[i]=Math.min(pts-2,1+Math.floor(rnd()*2)));return b; // 블러핑: 상대의 큰 방어를 헛쓰게
}
// 상대 점수 추정: 상대 수입(10/턴)에서, 돌 결과로 추론한 상대 지출 하한/추정치를 뺌(사람 입찰은 모름)
function aiOppModel(v,lv){
 const inc=10*v.t;let low=0,est=0,n=0;
 for(const h of v.mem.hist){n++;let tl=0,te=0;for(let i=0;i<3;i++){const a=h.bids[i],won=h.won[i];
   if(won){tl+=1;te+=Math.min(h.aiSun?a-1:a,lv.wonE||3.3)}else{const lb=h.aiSun?a:a+1;tl+=lb;te+=Math.max(lb+(lv.over||0),lv.lostE||3.3)}}
  low+=lv.infer?tl:3;est+=lv.infer?Math.max(te,tl):10}
 const oppMax=Math.max(3,inc-low),oppEst=Math.max(3,Math.min(oppMax,inc-est));
 return{oppMax,oppEst,avgSpend:n?Math.max(3,Math.min(25,est/n)):9};
}
// 기대값 최대 입찰: 8결과 확률 = 칸별 승률의 곱. 1점의 가치(lam)보다 기대 이득이 클 때만 1점 더(또는 '확실히 이기는 선'까지 한 번에)
function aiOptimize(V,pts,aiSun,om,lam,rnd,noise,lv){
 lv=lv||{};const cap=Math.max(1,lv.capK?Math.min(om.oppMax-2,Math.round(om.oppEst*lv.capK+(lv.capAdd||0))):om.oppMax-2);
 const imp=[0,1,2].map(i=>{let s=0;for(let m=0;m<8;m++)if((m>>i)&1)s+=Math.abs(V[m]-V[m^(1<<i)]);return s/4});
 const tot=imp.reduce((a,b)=>a+Math.pow(Math.min(b,3e4)+1,.8),0),extra=Math.max(0,Math.min(om.oppEst,om.avgSpend)-3);
 const mean=imp.map(x=>x>=AI_WIN*.2?Math.max(1,cap*(lv.critK||.8)):Math.max(.7,1+extra*Math.pow(Math.min(x,3e4)+1,.8)/tot));
 const lrn=lv.learn&&AI_LRN.ctx;const P=(i,x)=>{const need=aiSun?x-1:x;if(need>=cap)return 1;if(need<1)return 0;const p=1-Math.exp(-need/mean[i]);return lrn?aiLrP(i,need,p):p};
 const E=b=>{const p=[P(0,b[0]),P(1,b[1]),P(2,b[2])];let e=0;for(let m=0;m<8;m++){let q=1;for(let i=0;i<3;i++)q*=(m>>i)&1?p[i]:1-p[i];e+=q*V[m]}return e};
 const b=[1,1,1];let left=pts-3,cur=E(b);const g=aiSun?cap+1:cap,hasWin=V.some(x=>x>=AI_WIN);
 for(let guard=0;left>0&&guard<300;guard++){
  let best=-1,bv=cur,bs=0;
  for(let i=0;i<3;i++){
   for(const st of [1,g-b[i]]){if(st<1||st>left)continue;b[i]+=st;const e=E(b)-lam*st*(1+(rnd?rnd()*noise:0));b[i]-=st;if(e>bv+1e-9){bv=e;best=i;bs=st}}
  }
  // 여러 칸을 함께 올려야 의미가 생기는 경우(두 칸 이상이 모여야 오목)
  let jb=null;if(lv.joint&&hasWin){for(const set of [[0,1],[0,2],[1,2],[0,1,2]])for(const k of [1,2,3,5,8]){const c=k*set.length;if(c>left)continue;set.forEach(i=>b[i]+=k);const e=E(b)-lam*c*(1+(rnd?rnd()*noise:0));set.forEach(i=>b[i]-=k);if(e>bv+1e-9){bv=e;jb={set,k}}}}
  if(jb){jb.set.forEach(i=>b[i]+=jb.k);left-=jb.k*jb.set.length;cur=E(b);continue}
  if(best<0)break;b[best]+=bs;left-=bs;cur=E(b);
 }
 return{b,e:cur-lam*(b[0]+b[1]+b[2]-3)};
}
function aiLam(v,lv,om,V){
 const ref=V.filter(x=>Math.abs(x)<AI_WIN).map(Math.abs).sort((a,b)=>b-a);
 let lam=Math.max(25,(ref[2]||0))*lv.lamK;
 if(v.aiPts<om.oppEst)lam*=1.35;else if(v.aiPts>om.oppEst+10)lam*=.8;
 return lam;
}
// 지정할 때 '다음 턴 상대의 한 턴 오목' 위험: 이번 결과(8가지)마다 상대에게 빈칸 3개 이하로 오목이 되는 창이 남는지 보고,
// 남으면 다음 턴(상대가 선) 막을 수 있는 점수인지에 따라 그 결과의 값을 깎음 → 위협 칸을 포함해 지정하게 됨
function aiThrWin(bd,r,c,dr,dc,col){const oc=3-col;let s=0,lo=9,hi=-1;for(let j=0;j<5;j++){const v=bd[r+j*dr][c+j*dc];if(v===oc)return 9;if(v===col)s++;else{lo=Math.min(lo,j);hi=Math.max(hi,j)}}
 if(s===5)return 9;const y0=r-dr,x0=c-dc,y1=r+5*dr,x1=c+5*dc;if((inB(y0,x0)&&bd[y0][x0]===col)||(inB(y1,x1)&&bd[y1][x1]===col))return 9;const e=5-s;return e<=3&&hi-lo<=2?e:9}
function aiThrBase(bd,col){const out=[];for(const [dr,dc] of DIRS)for(let r=0;r<N;r++)for(let c=0;c<N;c++){if(!inB(r+4*dr,c+4*dc))continue;const e=aiThrWin(bd,r,c,dr,dc,col);if(e<=3)out.push([r,c,dr,dc])}return out}
function aiDesThreat(bd,cells,V,v,lv,om,base,spend){
 const oc=3-v.aiCol,W=aiWindows(cells),out=V.slice(),A=v.aiPts+10-(spend||3),O=om.oppEst+10-3;
 for(let m=0;m<8;m++){if(Math.abs(V[m])>=AI_WIN)continue;
  for(let i=0;i<3;i++){const [r,c]=cells[i];bd[r][c]=(m>>i)&1?v.aiCol:oc}
  let th=9;for(const w of base){const e=aiThrWin(bd,w[0],w[1],w[2],w[3],oc);if(e<th)th=e}
  for(const w of W){const e=aiThrWin(bd,w[0],w[1],w[2],w[3],oc);if(e<th)th=e}
  for(const [r,c] of cells)bd[r][c]=0;
  if(th<=3){const need=th===1?O-2:Math.ceil((O-(3-th))/th),risk=1/(1+Math.exp(((A-2)-need)/(lv.dtS||3)));out[m]=V[m]-AI_WIN*(lv.dThreat||.3)*risk}
  if(lv.dOwn&&m===7){for(let i=0;i<3;i++){const [r,c]=cells[i];bd[r][c]=v.aiCol}let to=9;for(const w of W){const e=aiThrWin(bd,w[0],w[1],w[2],w[3],v.aiCol);if(e<to)to=e}for(const [r,c] of cells)bd[r][c]=0;if(to<=2)out[7]+=lv.dOwn*(3-to)*1000}}
 return out}
// AI가 선일 때 세 칸 고르기
function aiDesignate(v){
 const lv=AI_LEVELS[v.level]||AI_LEVELS.pro,bd=v.bd.map(r=>r.slice()),rnd=()=>aiRng(v.mem),om=aiOppModel(v,lv);
 const any=bd.some(r=>r.some(x=>x));
 let cand=legalTriples(bd).filter(t=>any?t.some(([r,c])=>aiNear(bd,r,c,2)):t.every(([r,c])=>Math.abs(r-9)<=1&&Math.abs(c-9)<=1));
 if(!cand.length)cand=legalTriples(bd);
 if(lv.rand>=.7&&rnd()<.55)return cand[Math.floor(rnd()*cand.length)];
 const useL=lv.learn&&AI_LRN.on,trust=useL?aiLrTrust(v.mem):0;AI_LRN.t=v.t;
 let dPts=v.aiPts;if(lv.resvD){const th=aiThreat(bd,3-v.aiCol);if(th<=3)dPts=Math.max(3,v.aiPts-aiReserve(th,om,aiPFom(v.mem,lv),lv))}
 const tbase=lv.dThreat?aiThrBase(bd,3-v.aiCol):null;
 // 내 '한 칸 오목' 자리: 지정에 넣으면 상대는 그 칸을 막느라 큰 점수를 써야 함(상대 점수 소모를 가치로 침)
 const myF=new Set();if(lv.force){for(let r=0;r<N;r++)for(let c=0;c<N;c++)if(!bd[r][c]){bd[r][c]=v.aiCol;if(aiIsFive(bd,r,c,v.aiCol))myF.add(r*N+c);bd[r][c]=0}}
 // 후보가 많으면 값싼 1차 평가(8결과 값의 폭 + 세 칸 다 가졌을 때 값, 오목 걸린 칸·내 한 칸 오목 자리는 무조건 포함)로 상위 dPre개만 정밀 평가
 if(lv.dPre&&cand.length>lv.dPre){const q=cand.map(t=>{const V=aiOutcomes2(bd,t,v.aiCol,true,false,lv);let s=0;for(const x of V)s+=Math.min(Math.abs(x),3e4);if(V.some(x=>Math.abs(x)>=AI_WIN))s+=1e9;if(myF.size&&t.some(([r,c])=>myF.has(r*N+c)))s+=1e9;return{t,s:s+Math.max(0,V[7])}});q.sort((a,b)=>b.s-a.s);cand=q.slice(0,lv.dPre).map(x=>x.t)}
 const scored=cand.map(t=>{let V=lv.eval2?aiOutcomes2(bd,t,v.aiCol,true,false,lv):aiOutcomes(bd,t,v.aiCol,false,lv.see5,rnd);if(tbase){let sp=3;if(lv.dtReal){const l0=aiLam(v,lv,om,V),b0=aiOptimize(V,dPts,true,om,l0,null,0,lv).b;sp=b0[0]+b0[1]+b0[2]}V=aiDesThreat(bd,t,V,v,lv,om,tbase,sp)}const lam=aiLam(v,lv,om,V);
   if(useL){const f=aiLrFeat(V),ph=aiLrPhase(v.t),pb=aiLrPB(om.oppEst);AI_LRN.ctx={trust,q:[0,1,2].map(i=>aiLrHist(f.rank[i],0,f.crit[i],ph,pb))}}
   let sc=aiOptimize(V,dPts,true,om,lam,null,0,lv).e;AI_LRN.ctx=null;if(lv.tempo&&Math.abs(V[7])<AI_WIN)sc+=lv.tempo*Math.max(0,V[7]);if(myF.size&&t.some(([r,c])=>myF.has(r*N+c)))sc+=lv.force*lam*Math.min(om.oppEst,v.aiPts);if(lv.noise)sc+=Math.abs(sc)*(rnd()-.5)*lv.noise;return{t,sc}}).sort((a,b)=>b.sc-a.sc);
 if(lv.br&&lv.dk){AI_JOINT=!!lv.joint;const top=scored.slice(0,lv.dk),om2=aiPFom(v.mem,lv);
  for(const x of top){const V=aiOutcomes2(bd,x.t,v.aiCol,true,false,lv),lam=aiLam(v,lv,om2,V),smp=aiOppSamples(v.mem,lv,V,true,v.aiPts,lv.dS||10,rnd);x.sc2=(lv.smooth?aiBRsmooth(V,smp,v.aiPts,true,lam,rnd,Object.assign({},lv,{temp:0})):aiBRsamples(V,smp,v.aiPts,true,lam,rnd,0)).e}
  top.sort((a,b)=>b.sc2-a.sc2);const best=top[0].sc2,near=top.filter(x=>x.sc2>=best-Math.abs(best)*(lv.jitter||0)-1).slice(0,3);return near[Math.floor(rnd()*near.length)].t}
 if(lv.jitter){const best=scored[0].sc,near=scored.filter(x=>x.sc>=best-Math.abs(best)*lv.jitter-1).slice(0,4);return near[Math.floor(rnd()*near.length)].t}
 const k=Math.min(lv.top,scored.length);return scored[k>1?Math.floor(rnd()*k):0].t;
}


// ===== Ultimate 학습: 끝난 대국(복기로 공개된 기록)에서 '사람의 칸별 입찰 습관'을 숫자 집계로만 배움 =====
// 대국 중에는 쓰지 않는 정보(사람 입찰·점수)를 '끝난 뒤'에만 집계. 닉네임·판 위치 원본은 저장하지 않음.
// 특징: 칸 중요도 순위(1~3위) × 사람이 선/후 × 오목 관련 칸 여부 × 턴 구간(3) × 사람 보유 점수 구간(4) = 144칸, 칸마다 입찰 구간 10개 히스토그램
const LR_EDGE=[1,2,3,4,5,7,10,15,25,40,1e9],LR_NB=10,LR_NK=144,LR_LEN=LR_NK*LR_NB;
const LR_K=60,LR_WMAX=.6,LR_LOCALW=2,LR_DOCCAP=600,LR_KEYCAP=60,LR_CELLCAP=400,LR_MAXDOCS=500,LR_MIN=8;
const AI_LRN={on:false,H:null,H2:null,n:0,t:0,pb:1};
const aiLrPhase=t=>t<=8?0:t<=20?1:2;
const aiLrPB=B=>B<=15?0:B<=30?1:B<=60?2:3;
const aiLrBin=x=>{for(let i=0;i<LR_NB;i++)if(x<LR_EDGE[i+1])return i;return LR_NB-1};
const aiLrKey=(rank,hSun,crit,ph,pb)=>(((rank*2+hSun)*2+crit)*3+ph)*4+pb;
// 세 칸의 순위(중요도 큰 순, 같으면 앞 칸)와 오목 관련 여부
function aiLrFeat(V){const imp=[0,1,2].map(i=>{let x=0;for(let m=0;m<8;m++)if((m>>i)&1)x+=Math.abs(V[m]-V[m^(1<<i)]);return x/4});
 const ord=[0,1,2].sort((a,b)=>imp[b]-imp[a]||a-b),rank=[0,0,0];ord.forEach((c,r)=>rank[c]=r);
 return{rank,crit:imp.map(x=>x>=AI_WIN*.2?1:0)}}
// 집계 문서 검사: 모양·값 범위가 맞지 않으면 버리고(null), 큰 값은 잘라냄
function aiLearnClean(d,docCap,keyCap){
 if(!d||typeof d!=='object'||d.v!==1||!Array.isArray(d.h)||d.h.length!==LR_LEN)return null;
 const h=new Array(LR_LEN);let tot=0;
 for(let i=0;i<LR_LEN;i++){const x=d.h[i];if(typeof x!=='number'||!isFinite(x)||x<0)return null;h[i]=Math.min(LR_CELLCAP,Math.floor(x));tot+=h[i]}
 if(!tot)return null;
 // 한 사람(문서 하나)의 영향력 상한: 칸(특징)마다 keyCap, 전체 docCap 관측까지로 줄임
 if(keyCap)for(let k=0;k<LR_NK;k++){let s=0;for(let j=0;j<LR_NB;j++)s+=h[k*LR_NB+j];if(s>keyCap){const f=keyCap/s;for(let j=0;j<LR_NB;j++)h[k*LR_NB+j]*=f}}
 if(docCap){tot=h.reduce((a,b)=>a+b,0);if(tot>docCap){const f=docCap/tot;for(let i=0;i<LR_LEN;i++)h[i]*=f}}
 return h}
function aiLearnNew(){return{v:1,h:new Array(LR_LEN).fill(0),g:0}}
// 대국이 끝난 뒤 한 번: 기록(hist)에서 사람 입찰을 집계에 더함. agg는 이 기기 집계(없으면 새로)
// hist: [{t,sun,cells,bets:{[seat]:[a,b,c]},win:[seat,seat,seat],auto}] (index.html의 s.hist 형식), hum = 사람 자리('A'), humCol/aiCol = 돌 색
function aiLearnGame(agg,hist,hum,humCol,aiCol){
 const h=aiLearnClean(agg,0,0)||aiLearnNew().h,out={v:1,h,g:((agg&&agg.g)|0)+1};
 if(!Array.isArray(hist))return out;
 const lv=AI_LEVELS.ultimate,bd=emptyBoard();let hp=0;
 for(const x of hist){
  if(!x||!Array.isArray(x.cells)||x.cells.length!==3||!x.bets||!Array.isArray(x.win))break;
  const cells=validTriple(bd,x.cells);if(!cells)break;hp+=10;
  const b=x.bets[hum],hSun=x.sun===hum;
  if(validBets(b,hp)&&!(x.auto&&x.auto[hum])){
   const V=aiOutcomes2(bd,cells,aiCol,!hSun,hSun,lv),f=aiLrFeat(V),ph=aiLrPhase(x.t|0),pb=aiLrPB(hp);
   for(let i=0;i<3;i++){const k=aiLrKey(f.rank[i],hSun?1:0,f.crit[i],ph,pb)*LR_NB+aiLrBin(b[i]);h[k]=Math.min(LR_CELLCAP,h[k]+1)}}
  if(Array.isArray(b))hp-=(b[0]|0)+(b[1]|0)+(b[2]|0);
  cells.forEach(([r,c],i)=>{bd[r][c]=x.win[i]===hum?humCol:aiCol});
 }
 // 오래된 습관은 천천히 잊음(특징 칸 하나가 너무 커지면 반으로)
 for(let k=0;k<LR_NK;k++){let s=0;for(let j=0;j<LR_NB;j++)s+=h[k*LR_NB+j];if(s>=LR_CELLCAP)for(let j=0;j<LR_NB;j++)h[k*LR_NB+j]=Math.floor(h[k*LR_NB+j]/2)}
 return out}
// 올릴 문서(숫자 집계만)
function aiLearnDoc(agg){const h=aiLearnClean(agg,0,0);return h?{v:1,h:h.map(x=>Math.round(x)),g:Math.min(1e6,(agg.g|0)),ts:Date.now()}:null}
// 이 기기 집계 + 모두의 집계(최대 500문서, 내 문서는 빼고)를 합쳐 Ultimate에 넣음. 데이터가 없으면 꺼짐(기본 Ultimate와 같음)
function aiLearnSet(local,shared,selfId){
 const H=new Array(LR_LEN).fill(0);
 const L=aiLearnClean(local,0,0);if(L)for(let i=0;i<LR_LEN;i++)H[i]+=L[i]*LR_LOCALW;
 const docs=Array.isArray(shared)?shared.slice(0,LR_MAXDOCS):[];
 for(const d of docs){if(!d||d.id===selfId)continue;const S=aiLearnClean(d.data||d,LR_DOCCAP,LR_KEYCAP);if(S)for(let i=0;i<LR_LEN;i++)H[i]+=S[i]}
 // 뒤로 물러서기 표: 턴 구간·점수 구간을 합친 것(데이터가 적을 때)
 const H2=new Array(12*LR_NB).fill(0);let n=0;
 for(let k=0;k<LR_NK;k++){const k2=Math.floor(k/12);for(let j=0;j<LR_NB;j++){H2[k2*LR_NB+j]+=H[k*LR_NB+j];n+=H[k*LR_NB+j]}}
 Object.assign(AI_LRN,{on:n>=LR_MIN,H,H2,n});return AI_LRN.on}
// 특징 칸의 히스토그램(부족하면 뒤로 물러섬) → {h,off,n}
function aiLrHist(rank,hSun,crit,ph,pb){const k=aiLrKey(rank,hSun,crit,ph,pb);let n=0;for(let j=0;j<LR_NB;j++)n+=AI_LRN.H[k*LR_NB+j];
 if(n>=LR_MIN)return{A:AI_LRN.H,off:k*LR_NB,n};const k2=Math.floor(k/12);n=0;for(let j=0;j<LR_NB;j++)n+=AI_LRN.H2[k2*LR_NB+j];return n>=LR_MIN?{A:AI_LRN.H2,off:k2*LR_NB,n}:null}
// 학습된 습관대로 사람 입찰 하나를 뽑음(입자 -9용). 예산 B를 넘지 않게 줄임
function aiLearnDraw(V,B,hSun,rnd){const f=aiLrFeat(V),ph=aiLrPhase(AI_LRN.t),pb=aiLrPB(B),o=[1,1,1];
 for(let i=0;i<3;i++){const q=aiLrHist(f.rank[i],hSun?1:0,f.crit[i],ph,pb);if(!q)return null;let r=rnd()*q.n,j=0;for(;j<LR_NB-1;j++){r-=q.A[q.off+j];if(r<0)break}
  const lo=LR_EDGE[j],hi=Math.min(LR_EDGE[j+1]-1,Math.max(lo,B-2),lo+40);o[i]=lo+Math.floor(rnd()*(hi-lo+1))}
 let s=o[0]+o[1]+o[2];while(s>B){const i=o.indexOf(Math.max(...o));if(o[i]<=1)break;const cut=Math.min(o[i]-1,s-B);o[i]-=cut;s-=cut}
 return o}
// 학습된 누적 분포: 사람이 x점 이하로 걸 확률(구간 안은 고르게)
function aiLrCdf(q,x){if(x<1)return 0;let c=0;for(let j=0;j<LR_NB;j++){const lo=LR_EDGE[j],hi=LR_EDGE[j+1]-1,a=q.A[q.off+j];if(x>=hi)c+=a;else{if(x>=lo)c+=a*(x-lo+1)/(hi-lo+1);break}}return c/q.n}
// 지정 평가에서 쓰는 섞인 칸별 승률: (1-w)·기존 지수분포 + w·학습 분포, w=n/(n+k)·상한·이번 판 신뢰도
function aiLrP(i,need,pexp){const c=AI_LRN.ctx;if(!c)return pexp;const q=c.q[i];if(!q)return pexp;const w=LR_WMAX*q.n/(q.n+LR_K)*c.trust;return (1-w)*pexp+w*aiLrCdf(q,need)}
// 이번 판에서 학습 습관이 실제와 얼마나 맞는지(입자 중 학습형 비율 ÷ 처음 비율, 0~1)
function aiLrTrust(mem){const pf=mem.pf;if(!pf||!mem.lrShare)return 1;const s=pf.filter(p=>p.k===-9).length/pf.length;return Math.max(0,Math.min(1,s/mem.lrShare))}
function aiLrWeight(){return AI_LRN.on?LR_WMAX*AI_LRN.n/(AI_LRN.n+LR_K*12):0}
// ===== Ultimate 2세대: 상대 점수 추적(입자 필터) + 상대 입찰 흉내 + 최선 대응 =====
// 상대 점수는 끝까지 모름. 대신 '상대가 이런 성향이고 이만큼 가졌다면 이렇게 걸었겠지'를 여러 개(입자) 만들어 두고,
// 실제 돌 결과(어느 칸을 누가 가져갔나)와 맞는 입자만 남기면서 상대 점수와 성향을 추정함
const AI_KS=[.02,.05,.09,.14,.2,.3,.45];
// 상대 성향 입자 종류: 양수 = 최적화형(1점의 가치 비율), -1 = 무작위, -2 = 비축형(평소 최소, 오목 판에 몰빵), -3 = 몰빵형(중요한 칸 하나에 크게), -9 = 학습된 사람 습관
function aiOppCrit(Vop,B,rnd){const neg=[],pos=[];for(let m=0;m<8;m++){if(Vop[m]<=-AI_WIN)neg.push(m);else if(Vop[m]>=AI_WIN)pos.push(m)}
 if(!neg.length&&!pos.length)return null;const b=[1,1,1],pc=m=>(m&1)+((m>>1)&1)+((m>>2)&1);
 if(pos.length){const S=pos.slice().sort((a,c)=>pc(a)-pc(c))[0],cs=[0,1,2].filter(i=>(S>>i)&1);if(!neg.length||rnd()<.5){let left=B-3;cs.forEach((i,j)=>{const q=Math.floor(left/(cs.length-j));b[i]+=q;left-=q});return b}}
 const H=[0,1,2].filter(i=>neg.every(m=>!((m>>i)&1)));if(H.length){b[H[Math.floor(rnd()*H.length)]]=Math.max(1,B-2);return b}
 const need=[0,1,2].filter(i=>neg.some(m=>!((m>>i)&1)));let left=B-3;need.forEach((i,j)=>{const q=Math.floor(left/(need.length-j));b[i]+=q;left-=q});return b}
function aiOppSim(V,budget,oppSun,aiPts,lamO,rnd){
 if(lamO===-2||lamO===-3||lamO===-9){const B=Math.max(3,budget),Vop=new Array(8);for(let m=0;m<8;m++)Vop[m]=-V[7^m];
  const c=aiOppCrit(Vop,B,rnd);if(c)return c;
  if(lamO===-9&&AI_LRN.on){const o=aiLearnDraw(V,B,oppSun,rnd);if(o)return o}
  const imp=[0,1,2].map(i=>{let x=0;for(let m=0;m<8;m++)if((m>>i)&1)x+=Math.abs(Vop[m]-Vop[m^(1<<i)]);return x}),top=imp.indexOf(Math.max(...imp));
  if(lamO===-3){const b=[1,1,1];b[top]=Math.max(1,Math.floor((B-2)*(.5+.5*rnd())));return b}
  const b=[1+(rnd()<.3?1:0),1+(rnd()<.3?1:0),1+(rnd()<.3?1:0)];if(rnd()<.3)b[top]+=1+Math.floor(rnd()*4);return b.map(x=>Math.min(x,Math.max(1,Math.floor(B/3))))}
 if(lamO<0){const B=Math.max(3,budget),sp=Math.max(3,Math.round(B*(.25+.75*rnd())));const w=[rnd(),rnd(),rnd()],z=w[0]+w[1]+w[2];return w.map(x=>1+Math.floor((sp-3)*x/z))}
 const Vop=new Array(8);for(let m=0;m<8;m++)Vop[m]=-V[7^m];
 const om={oppMax:aiPts+12,oppEst:Math.max(3,aiPts),avgSpend:8};
 return aiOptimize(Vop,Math.max(3,budget),oppSun,om,lamO,rnd,.6,{joint:AI_JOINT}).b}
let AI_JOINT=false,AI_MIX=0;
function aiRef(V){const ref=V.filter(x=>Math.abs(x)<AI_WIN).map(Math.abs).sort((a,b)=>b-a);return Math.max(25,ref[2]||0)}
function aiKS(lv){return lv.types?AI_KS.concat(lv.types):lv.randK?AI_KS.concat([-1,-1]):AI_KS}
function aiPF(mem,lv){if(!mem.pf){mem.pf=[];const n=lv.np||40,K=aiKS(lv),nL=lv.learn?Math.round(n*aiLrWeight()):0;mem.lrShare=nL/n;for(let i=0;i<n;i++)mem.pf.push({b:0,k:i<nL?-9:K[i%K.length]})}return mem.pf}
function aiPFUpdate(mem,t,aiSun,bids,won){
 const c=mem.cur;if(!c||c.t!==t)return;AI_LRN.t=t;const lv=AI_LEVELS[c.level]||{};AI_JOINT=!!lv.joint;const pf=aiPF(mem,lv),rnd=()=>aiRng(mem),ref=aiRef(c.V);
 const W=[];
 for(const p of pf){const B=p.b+10,o=aiOppSim(c.V,B,!aiSun,c.aiPts,p.k<0?p.k:ref*p.k,rnd);let d=0;
  for(let i=0;i<3;i++){const a=bids[i];let x=o[i];
   if(won[i]){const hi=aiSun?a-1:a;if(x>hi){d+=x-hi;x=hi}}else{const lo=aiSun?a:a+1;if(x<lo){d+=lo-x;x=lo}}o[i]=Math.max(1,x)}
  const sp=o[0]+o[1]+o[2];let w=Math.exp(-d/(2+.25*sp));if(sp>B){w*=1e-4;p.nb=0}else p.nb=B-sp;W.push(w)}
 // 가중치대로 다시 뽑기(+가끔 성향 바꿔 보기)
 const z=W.reduce((a,b)=>a+b,0)||1,n=pf.length,out=[];let u=rnd()/n,acc=0,j=0;
 for(let i=0;i<n;i++){const target=u+i/n;while(acc+W[j]/z<target&&j<n-1){acc+=W[j]/z;j++}const p=pf[j];const K=aiKS(lv);out.push({b:p.nb,k:rnd()<.08?(lv.learn&&AI_LRN.on&&rnd()<aiLrWeight()?-9:K[Math.floor(rnd()*K.length)]):p.k})}
 mem.pf=out}
// 최선 대응: 상대 입찰 표본들에 대해 기대값 - 점수 비용이 가장 큰 입찰
function aiBRsamples(V,samples,pts,aiSun,lam,rnd,temp){
 const add=aiSun?1:0,S=samples.length;
 const cand=[0,1,2].map(i=>[...new Set([1,...samples.map(s=>s[i]+add)])].filter(x=>x>=1&&x<=pts-2).sort((p,q)=>p-q));
 const all=[];
 for(const a of cand[0])for(const b of cand[1]){if(a+b+1>pts)break;for(const c of cand[2]){if(a+b+c>pts)break;
  let e=0;for(const s of samples)e+=V[(aiSun?(a>s[0]):(a>=s[0]))|((aiSun?(b>s[1]):(b>=s[1]))<<1)|((aiSun?(c>s[2]):(c>=s[2]))<<2)];
  all.push({b:[a,b,c],e:e/S-lam*(a+b+c-3)})}}
 all.sort((x,y)=>y.e-x.e);
 // 섞기: 점수 몇 점 차이로 비슷한 베팅들 중에서 확률적으로 고름(습관을 읽히지 않게)
 if(AI_MIX>0&&all.length>1){const best=all[0].e,cand=all.slice(0,60),w=cand.map(x=>Math.exp((x.e-best)/(AI_MIX*lam))),z=w.reduce((a,b)=>a+b,0);let r=rnd()*z;for(let i=0;i<cand.length;i++){r-=w[i];if(r<=0)return cand[i]}return cand[0]}
 if(!temp||all.length<2)return all[0];
 const best=all[0].e,tol=Math.max(1,Math.abs(best)*temp),near=all.filter(x=>x.e>=best-tol).slice(0,5);
 return near[Math.floor(rnd()*near.length)]}

// 부드러운 최선 대응: 상대 입찰 예측이 정확하지 않다고 보고(예측값 ± 흔들림), 칸마다 이길 확률로 계산 → 큰 판에선 넉넉히, 작은 판에선 아껴서
function aiBRsmooth(V,samples,pts,aiSun,lam,rnd,lv){
 const S=samples.length,add=aiSun?1:0,g0=lv.sg0||1,g1=lv.sg1||.25;
 const grid=[.15,.3,.5,.7,.9].map(f=>Math.round((pts-2)*f));
 const cand=[0,1,2].map(i=>{const c=new Set([1,pts-2,...grid]);for(const s of samples){c.add(s[i]+add);c.add(s[i]+add+1);c.add(Math.round((s[i]+add)*1.3)+1)}return [...c].filter(x=>x>=1&&x<=pts-2).sort((p,q)=>p-q)});
 const P=samples.map(s=>[0,1,2].map(i=>{const sg=g0+g1*s[i];return a=>1/(1+Math.exp(-((aiSun?a-s[i]-.5:a-s[i]+.5)/sg)))}));
 // 칸별 후보 금액마다 표본별 승률 미리 계산
 const pre=[0,1,2].map(i=>cand[i].map(a=>samples.map((s,k)=>P[k][i](a))));
 let best=null,bv=-Infinity;const all=[];
 for(let ia=0;ia<cand[0].length;ia++){const a=cand[0][ia];
  for(let ib=0;ib<cand[1].length;ib++){const b=cand[1][ib];if(a+b+1>pts)break;
   for(let ic=0;ic<cand[2].length;ic++){const c=cand[2][ic];if(a+b+c>pts)break;
    let e=0;for(let k=0;k<S;k++){const p0=pre[0][ia][k],p1=pre[1][ib][k],p2=pre[2][ic][k];
     e+=(1-p0)*(1-p1)*(1-p2)*V[0]+p0*(1-p1)*(1-p2)*V[1]+(1-p0)*p1*(1-p2)*V[2]+p0*p1*(1-p2)*V[3]+(1-p0)*(1-p1)*p2*V[4]+p0*(1-p1)*p2*V[5]+(1-p0)*p1*p2*V[6]+p0*p1*p2*V[7]}
    e=e/S-lam*(a+b+c-3);all.push({b:[a,b,c],e});if(e>bv){bv=e;best=all[all.length-1]}}}}
 if(!lv.temp)return best;
 all.sort((x,y)=>y.e-x.e);const tol=Math.max(1,Math.abs(bv)*lv.temp),near=all.filter(x=>x.e>=bv-tol).slice(0,5);return near[Math.floor(rnd()*near.length)]}

// 보험: 상대가 '최대 B점'을 가졌다고 쳐도 내가 지는 결과(LOSE)를 만들 수 없는지 검사하고, 아니면 가장 값싼 안전 베팅을 찾음
function aiSafe(V,b,aiSun,B){for(let m=0;m<8;m++){if(V[m]>-AI_WIN)continue;let cost=0,ok=true;
  for(let i=0;i<3;i++){if((m>>i)&1){if(aiSun&&b[i]<=1){ok=false;break}cost+=1}else cost+=aiSun?b[i]:b[i]+1}
  if(ok&&cost<=B)return false}return true}
function aiInsure(V,smp,pts,aiSun,lam,B,r0){
 if(aiSafe(V,r0.b,aiSun,B))return r0;
 const top=Math.max(1,pts-2),step=top>45?2:1,S=smp.length;let best=null;
 for(let a=1;a<=top;a+=step)for(let b=1;a+b+1<=pts&&b<=top;b+=step)for(let c=1;a+b+c<=pts&&c<=top;c+=step){const x=[a,b,c];if(!aiSafe(V,x,aiSun,B))continue;
  let e=0;for(const s of smp)e+=V[(aiSun?(a>s[0]):(a>=s[0]))|((aiSun?(b>s[1]):(b>=s[1]))<<1)|((aiSun?(c>s[2]):(c>=s[2]))<<2)];e=e/S-lam*(a+b+c-3);
  if(!best||e>best.e)best={b:x,e}}
 return best||r0}

// Ultimate 4세대: 지면 끝나는 판에서 '한 칸만 이겨도 막히는' 경우 → 무작위로 고른 한 칸에 몰아서 막음.
// 상대는 내가 어느 칸에 몰았는지 모르므로 막아야 할 칸 전부에 나눠 걸어야 함 → 상대 점수의 높은 쪽 추정(분위수)/칸 수 보다 많이.
function aiCrit4(V,v,lv,rnd){
 const neg=[];for(let m=0;m<8;m++)if(V[m]<=-AI_WIN)neg.push(m);if(!neg.length)return null;
 const H=[0,1,2].filter(i=>neg.every(m=>!((m>>i)&1)));if(!H.length)return null;
 const pf=aiPF(v.mem,lv),bs=pf.map(p=>p.b+10).sort((a,b)=>a-b),om=aiOppModel(v,lv);
 const Bq=bs[Math.min(bs.length-1,Math.floor((lv.critQ||.9)*(bs.length-1)))];
 const k=H.length,sun=v.aiSun;if(k<(lv.critK||2))return null;
 const B=lv.critU?om.oppMax:Math.min(om.oppMax,Math.ceil(Bq*(lv.critM||1)+(lv.critA||0)));
 const per=k>1?Math.ceil((B-(3-k))/k):B-2;
 let X=Math.max(1,per+(sun?1:0));
 const pos=[];for(let m=0;m<8;m++)if(V[m]>=AI_WIN)pos.push(m);
 let cand=H.filter(j=>pos.some(m=>m===(1<<j)));if(!cand.length)cand=H;const j=cand[Math.floor(rnd()*cand.length)];
 const b=[1,1,1];for(const i of H)if(i!==j)b[i]=sun?2:1;
 const others=b[0]+b[1]+b[2]-1;X=Math.min(X,v.aiPts-others);b[j]=Math.max(1,X);
 while(b[0]+b[1]+b[2]>v.aiPts){const i=[0,1,2].find(x=>x!==j&&b[x]>1);if(i===undefined)break;b[i]--}
 return b}
// 완전히 막을 수 없을 때: 상대가 지는 결과를 만들려면 드는 최소 점수를 최대한 높이는 베팅(같으면 기대값)
function aiMaximin(V,smp,pts,aiSun,lam){
 const oc=b=>{let mn=Infinity;for(let m=0;m<8;m++){if(V[m]>-AI_WIN)continue;let cost=0,ok=true;
   for(let i=0;i<3;i++){if((m>>i)&1){if(aiSun&&b[i]<=1){ok=false;break}cost+=1}else cost+=aiSun?b[i]:b[i]+1}if(ok)mn=Math.min(mn,cost)}return mn};
 const top=Math.max(1,pts-2),step=top>45?2:1,S=smp.length;let best=null;
 for(let a=1;a<=top;a+=step)for(let b=1;a+b+1<=pts&&b<=top;b+=step)for(let c=1;a+b+c<=pts&&c<=top;c+=step){const x=[a,b,c],q=oc(x);
  let e=0;for(const s of smp)e+=V[(aiSun?(a>s[0]):(a>=s[0]))|((aiSun?(b>s[1]):(b>=s[1]))<<1)|((aiSun?(c>s[2]):(c>=s[2]))<<2)];e=e/S-lam*(a+b+c-3);
  if(!best||q>best.q||(q===best.q&&e>best.e))best={b:x,q,e}}
 return best}
function aiOppSamples(mem,lv,V,aiSun,aiPts,S,rnd){
 const pf=aiPF(mem,lv),ref=aiRef(V),out=[];
 for(let k=0;k<S;k++){const p=pf[Math.floor(rnd()*pf.length)],B=Math.max(3,p.b+10);
  if(rnd()<(lv.mixR||0)){const sp=Math.max(3,Math.round(B*(.3+.7*rnd())));const w=[rnd(),rnd(),rnd()],z=w[0]+w[1]+w[2];const o=w.map(x=>1+Math.floor((sp-3)*x/z));out.push(o)}
  else out.push(aiOppSim(V,B,!aiSun,aiPts,p.k<0?p.k:ref*p.k,rnd))}
 return out}
function aiPFom(mem,lv){const pf=aiPF(mem,lv),bs=pf.map(p=>p.b+10).sort((a,b)=>a-b);
 return{oppMax:bs[bs.length-1],oppEst:bs.reduce((a,b)=>a+b,0)/bs.length,avgSpend:8}}

// Ultimate 3세대: 오목이 걸린 턴. 상대 점수의 '확실한 상한'(돌 결과로만 계산, oppMax)을 기준으로
// 확실히 막거나 확실히 이길 수 있으면 딱 그만큼만, 아니면 한 칸에 몰아서(어느 칸인지 읽히지 않게 무작위) 막음
function aiCrit3(V,v,om,rnd,lv){
 const neg=[],pos=[];for(let m=0;m<8;m++){if(V[m]<=-AI_WIN)neg.push(m);else if(V[m]>=AI_WIN)pos.push(m)}
 if(!neg.length&&!pos.length)return null;
 const pts=v.aiPts,sun=v.aiSun,one=Math.max(1,om.oppMax-2),g=sun?one+1:one,pc=m=>(m&1)+((m>>1)&1)+((m>>2)&1);
 // 확실한 승리: 필요한 칸 모두에 상대가 한 칸에 걸 수 있는 최대보다 많이
 if(pos.length){const S=pos.filter(m=>{for(let x=0;x<8;x++)if((x&m)===m&&V[x]<AI_WIN)return false;return true}).sort((a,b)=>pc(a)-pc(b))[0];
  if(S!==undefined){const k=pc(S);if(k*g+(3-k)<=pts){const b=[1,1,1];for(let i=0;i<3;i++)if((S>>i)&1)b[i]=g;return b}}}
 if(!neg.length||lv.crit3<2)return null;
 const H=[0,1,2].filter(i=>neg.every(m=>!((m>>i)&1)));
 if(!H.length)return null;
 // 막는 칸이 여럿이면 공격도 되는 칸 우선, 아니면 무작위
 let cand=H.filter(j=>pos.some(m=>m===(1<<j)));if(!cand.length)cand=H;const j=cand[Math.floor(rnd()*cand.length)];
 const b=[1,1,1];
 if(g<=pts-2){b[j]=g;
  // 남는 점수로 공격 칸도 노려 봄(한 칸 공격이 있으면)
  return b}
 b[j]=Math.max(1,pts-2);return b}

// 막기: 한 칸만 이겨도 상대 오목이 모두 막히면, 쓰기로 한 점수를 그 칸 하나에 몰아 줌(어느 칸인지는 무작위라 읽히지 않음)
function aiConc(V,b,pts,rnd,lv){const neg=[];for(let m=0;m<8;m++)if(V[m]<=-AI_WIN)neg.push(m);
 const H=[0,1,2].filter(i=>neg.every(m=>!((m>>i)&1)));if(!H.length)return b;
 const T=b[0]+b[1]+b[2]-3,j=H[Math.floor(rnd()*H.length)],o=[1,1,1];o[j]=Math.max(1,Math.min(pts-2,1+Math.round(T*lv.conc)));return o}

// 비축량(3세대): 다음 턴 상대(선)가 한 턴 오목(빈칸 th개)을 노릴 때 막을 점수. 상대 점수는 추정치와 확실한 상한 사이에서 잡음
function aiReserve(th,om,om2,lv){const Bo=om2.oppEst+lv.resvU*Math.max(0,om.oppMax-om2.oppEst)+10;
 const need=th===1?Bo-2:th===2?Math.ceil((Bo-3)/2):Math.ceil((Bo-3)/3*(lv.resv3||1));return Math.max(0,Math.round((need+2-10)*lv.resv))}
// 입찰(사람보다 먼저 봉인). 사람 입찰·점수는 받지 않음
function aiBid0(v){
 const lv=AI_LEVELS[v.level]||AI_LEVELS.pro,bd=v.bd.map(r=>r.slice()),rnd=()=>aiRng(v.mem),om=aiOppModel(v,lv);
 const V=lv.eval2?aiOutcomes2(bd,v.cells,v.aiCol,v.aiSun,!v.aiSun,lv):aiOutcomes(bd,v.cells,v.aiCol,!v.aiSun,lv.see5,rnd);
 // bidRand: 이 확률로 '대충 나눠 거는' 초보식 베팅(단계 사이 간격을 고르게)
 if(lv.rand>=.7||(lv.bidRand&&rnd()<lv.bidRand)){const b=[1,1,1];let left=Math.floor((v.aiPts-3)*(.2+rnd()*.5));const imp=[0,1,2].map(i=>V[7]-V[7^(1<<i)]);const hot=imp.indexOf(Math.max(...imp));
  while(left-->0)b[rnd()<.6?hot:Math.floor(rnd()*3)]++;return b}
 // brP: 최선 대응 베팅을 쓸 확률(고수를 Ultimate보다 한 단계 약하게)
 if(lv.br&&(lv.brP==null||rnd()<lv.brP)){AI_JOINT=!!lv.joint;AI_MIX=0;AI_LRN.t=v.t;AI_LRN.ctx=null;const om2=aiPFom(v.mem,lv),lam=aiLam(v,lv,om2,V);v.mem.cur={t:v.t,V,aiPts:v.aiPts,level:v.level};
  const smp=aiOppSamples(v.mem,lv,V,v.aiSun,v.aiPts,lv.S||20,rnd);
  // 비축: 이번 턴에 승부가 안 걸렸고 다음 턴 상대가 선으로 한 턴 오목을 노릴 수 있으면, 다음 턴에 막을 점수를 남김
  if(lv.resv&&v.aiSun&&Math.max(...V)<AI_WIN&&Math.min(...V)>-AI_WIN){const th=aiThreat(bd,3-v.aiCol);
   if(th<=3){const R=lv.resvU!=null?aiReserve(th,om,om2,lv):(()=>{const Bo=om2.oppEst+10,need=th===1?Bo:th===2?Bo-1:Math.ceil((Bo-3)/3);return Math.max(0,Math.round((need-10+2)*lv.resv))})();
    const cap=Math.max(3,v.aiPts-R);if(cap<v.aiPts){AI_MIX=lv.mixT||0;const r=aiBRsamples(V,smp,cap,v.aiSun,lam,rnd,0);AI_MIX=0;return r.b}}}
  if(lv.crit3){const cb=aiCrit3(V,v,om,rnd,lv);if(cb)return cb}
  if(lv.crit4){const cb=aiCrit4(V,v,lv,rnd);if(cb)return cb}
  const crit=Math.min(...V)<=-AI_WIN||(lv.smoothWin&&Math.max(...V)>=AI_WIN);
  if(lv.ins&&Math.min(...V)<=-AI_WIN){const rb=(()=>{const r0=aiBRsamples(V,smp,v.aiPts,v.aiSun,lam,rnd,0),B=Math.min(om.oppMax,Math.ceil(om2.oppMax*lv.ins+(lv.insAdd||0)));
   const ri=aiInsure(V,smp,v.aiPts,v.aiSun,lam,B,r0);if(ri!==r0)return ri.b;
   // 완전히 막을 방법이 없으면: 예측이 틀릴 수 있다고 보고 막을 확률이 가장 높은 쪽으로
   if(lv.insMax&&!aiSafe(V,r0.b,v.aiSun,B)){const mm=aiMaximin(V,smp,v.aiPts,v.aiSun,lam);if(mm)return mm.b}
   if(lv.insSmooth&&!aiSafe(V,r0.b,v.aiSun,B))return aiBRsmooth(V,smp,v.aiPts,v.aiSun,lam,rnd,Object.assign({},lv,{temp:0})).b;
   if(!lv.desp)return ri.b;
   if(r0.e<-AI_WIN*lv.desp)return aiBRsmooth(V,smp,v.aiPts,v.aiSun,lam,rnd,Object.assign({},lv,{temp:0})).b;return r0.b})();
   return lv.conc?aiConc(V,rb,v.aiPts,rnd,lv):rb}
  if(lv.mixT&&Math.min(...V)>-AI_WIN){AI_MIX=lv.mixT;const r=aiBRsamples(V,smp,v.aiPts,v.aiSun,lam,rnd,0);AI_MIX=0;return r.b}
  if(lv.desp&&!lv.smooth){const r0=aiBRsamples(V,smp,v.aiPts,v.aiSun,lam,rnd,0);if(r0.e<-AI_WIN*(lv.desp))return aiBRsmooth(V,smp,v.aiPts,v.aiSun,lam,rnd,Object.assign({},lv,{temp:0})).b;if(!lv.temp&&!(lv.smoothCrit&&crit))return r0.b}
  return ((lv.smooth||(lv.smoothCrit&&crit))?aiBRsmooth(V,smp,v.aiPts,v.aiSun,lam,rnd,lv):aiBRsamples(V,smp,v.aiPts,v.aiSun,lam,rnd,lv.temp||0)).b}
 const lam=aiLam(v,lv,om,V);
 if(lv.crit2){const cb=aiCritical2(V,v,om,rnd);if(cb)return cb;
  // 평소 턴: 상대보다 덜 쓰며 비축. 상대가 다음 턴(선)에 한 턴 오목을 노릴 수 있으면 막을 점수를 남김
  const nextOppSun=v.aiSun,th=aiThreat(bd,3-v.aiCol);let reserve=0;
  if(nextOppSun&&th<=1)reserve=Math.max(0,om.oppMax+10-2-10);else if(nextOppSun&&th<=2)reserve=Math.max(0,Math.round((om.oppEst+10-2)*.7)-10);
  const budget=Math.max(3,Math.min(v.aiPts-reserve,Math.round(om.avgSpend*lv.spendK+(v.aiPts-om.oppEst)*.25)));
  return aiOptimize(V,Math.max(3,Math.min(v.aiPts,budget)),v.aiSun,om,lam,null,0).b}
 // 평소 턴에는 일부 점수를 남겨 두어(무작위 비율) 결정적인 칸에 쓸 여력을 확보
 let pool=v.aiPts;
 if(lv.res&&Math.max(...V)<AI_WIN&&Math.min(...V)>-AI_WIN)pool=Math.max(3,Math.round(v.aiPts*(1-lv.res*(.5+rnd()))));
 let b=aiOptimize(V,pool,v.aiSun,om,lam,lv.noise||lv.bidNoise?rnd:null,lv.noise||lv.bidNoise,lv).b;
 // Ultimate: 확실하지 않은 내 오목 공격에서는 가끔 적게 걸어 상대의 큰 방어를 헛쓰게 함(읽히지 않게)
 if(lv.mix&&v.aiSun&&Math.max(...V)>=AI_WIN&&Math.min(...V)>-AI_WIN){const cap=Math.max(1,om.oppMax-2);
  if(b.some(x=>x>1&&x<=cap)&&rnd()<.3)b=b.map(x=>Math.max(1,Math.min(x,2+Math.floor(rnd()*2))))}
 return b;
}
// 4세대 보정: 지면 끝나는 판에서, 고른 베팅이 '상대가 필요한 칸에 고르게 다 거는' 가장 흔한 공격에 뚫리면
// 한 칸에 몰아서 막는 쪽으로 바꿈(상대는 내가 어느 칸에 몰았는지 모름)
function aiBid(v){const b=aiBid0(v),lv=AI_LEVELS[v.level]||{};if(!lv.critFix||!v.cells)return b;
 try{const V=aiOutcomes2(v.bd.map(r=>r.slice()),v.cells,v.aiCol,v.aiSun,!v.aiSun,lv);const neg=[];for(let m=0;m<8;m++)if(V[m]<=-AI_WIN)neg.push(m);if(!neg.length)return b;
  const H=[0,1,2].filter(i=>neg.every(m=>!((m>>i)&1)));if(!H.length)return b;
  const pc=m=>(m&1)+((m>>1)&1)+((m>>2)&1),mx=neg.slice().sort((a,c)=>pc(c)-pc(a))[0],R=[0,1,2].filter(i=>!((mx>>i)&1));
  if(R.length<2)return b;const pf=aiPF(v.mem,lv),bs=pf.map(p=>p.b+10).sort((a,c)=>a-c),om=aiOppModel(v,lv),Bq0=Math.min(om.oppMax,bs[Math.min(bs.length-1,Math.floor((lv.critQ||.75)*(bs.length-1)))]),Bq=lv.critU?om.oppMax:Math.round(Bq0+(lv.critMix||0)*(om.oppMax-Bq0));
  const sun=v.aiSun,wins=(x,o)=>sun?x>o:x>=o;
  const loses=bb=>{const left=Bq-(3-R.length);for(let rot=0;rot<R.length;rot++){const o=[1,1,1];let l=left;R.forEach((i,j)=>{const q=Math.floor(l/(R.length-j));o[i]=q;l-=q});
    const oo=o.slice();R.forEach((i,j)=>{oo[R[(j+rot)%R.length]]=o[i]});let m=0;for(let i=0;i<3;i++)if(wins(bb[i],oo[i]))m|=1<<i;if(V[m]<=-AI_WIN)return true}return false};
  if(!loses(b))return b;
  const j=H[Math.floor(aiRng(v.mem)*H.length)],c=[1,1,1];for(const i of H)if(i!==j)c[i]=sun?2:1;
  const others=c[0]+c[1]+c[2]-1,need=Math.ceil((Bq-(3-R.length))/R.length)+(sun?1:0);c[j]=Math.max(1,Math.min(v.aiPts-others,need+(lv.critPad||0)));
  if(c[0]+c[1]+c[2]>v.aiPts)return b;return c}catch(e){return b}}
// 턴이 끝나면 AI는 '자기 입찰과 칸별 승패'만 기억함
function aiObserve(mem,t,aiSun,bids,won){mem.hist.push({t,aiSun,bids:bids.slice(),won:won.slice()});if(mem.cur)aiPFUpdate(mem,t,aiSun,bids,won)}
function aiNewMem(seed){return{hist:[],s:(seed>>>0)||12345}}
// ===== AI END =====
