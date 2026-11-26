// 평가용 대전 하니스 (단일 스레드). node h.js N "A~B,A~B"
// 선수: ai:<level>[@file]  (file 생략 = 원본 index.html의 AI 구역 그대로) | bot:<name> (airesearch/bots.js + 여기 xbots.js)
// 선후: 짝수판 A가 흑·첫 선, 홀수판 B가 흑·첫 선. env: UO='{"..."}' (ultimate 파라미터 덮어쓰기, @file 모델에만), TM=1 시간 출력, SEED 오프셋
const fs=require('fs'),path=require('path');
const SRC=fs.readFileSync('/home/claude/betting-omok/index.html','utf8');
const cut=(s,a,b)=>s.slice(s.indexOf(a),s.indexOf(b)+b.length);
const ENG=cut(SRC,'// ===== ENGINE START =====','// ===== ENGINE END =====');
const AIDEP=cut(SRC,'// ===== AI START =====','// ===== AI END =====');
const EX='emptyBoard,legalTriples,validTriple,fiveLines,settle,aiDesignate,aiBid,aiObserve,aiNewMem,AI_LEVELS,aiOutcomes2,aiThreat,AI_WIN,DIRS,N,inB,aiIsFive,aiLearnGame,aiLearnSet,aiLearnClean,aiLearnDoc,AI_LRN,aiPFom,aiOppModel';
const cache={};
function load(file){const k=file||'@dep';if(cache[k])return cache[k];const M={};
 const ai=file?fs.readFileSync(path.resolve(__dirname,file),'utf8'):AIDEP;
 new Function('M',ENG+'\n'+ai+`\nObject.assign(M,{${EX}});`)(M);cache[k]=M;return M}
const TOOL=(()=>{const M={};new Function('M',fs.readFileSync('/home/claude/airesearch/engine.js','utf8')+'\n'+fs.readFileSync('/home/claude/airesearch/ai_old.js','utf8')+`\nObject.assign(M,{emptyBoard,legalTriples,validTriple,fiveLines,settle,aiDesignate,aiBid,aiObserve,aiNewMem,AI_LEVELS,aiOutcomes2,aiThreat,AI_WIN,DIRS,N,inB,aiIsFive});`)(M);return M})();
const BOTS=Object.assign({},require('/home/claude/airesearch/bots.js'),require('./xbots.js'));
const q=(a,f)=>{const b=a.slice().sort((x,y)=>x-y);return b[Math.min(b.length-1,Math.floor(f*b.length))].toFixed(0)};
const now=()=>Number(process.hrtime.bigint())/1e6;
const stat={};const rec=(k,ms)=>{const s=stat[k]||(stat[k]={max:0,sum:0,n:0,over:0,a:[]});s.a.push(ms);s.max=Math.max(s.max,ms);s.sum+=ms;s.n++;if(ms>250)s.over++};
function mkPlayer(spec,seed,col){
 if(spec.startsWith('bot:')){const f=BOTS[spec.slice(4)];if(!f)throw new Error('no bot '+spec);return f(TOOL,seed,col)}
 const [lvl,file]=spec.slice(3).split('@');const M=load(file);const mem=M.aiNewMem(seed);
 const view=(g,extra)=>Object.assign({level:lvl,bd:g.bd.map(r=>r.slice()),t:g.t,aiSun:g.sun===col,aiPts:g.pts[col],aiCol:col,mem},extra||{});
 return{designate:g=>{const t0=now();const r=M.aiDesignate(view(g));g._dms=now()-t0;rec(spec+' 지정',g._dms);return r},
  bid:(g,cells)=>{const t0=now();const r=M.aiBid(view(g,{cells}));const ms=now()-t0;try{const o=M.aiPFom(mem,M.AI_LEVELS[lvl]),q=M.aiOppModel(view(g),M.AI_LEVELS[lvl]);(g._est||(g._est={}))[col]={est:Math.round(o.oppEst),pmax:o.oppMax,max:q.oppMax}}catch(e){}rec(spec+' 입찰',ms);if(g.sun===col)rec(spec+' 지정+입찰',ms+(g._dms||0));return r},
  observe:(g,bids,won)=>M.aiObserve(mem,g.t,g.sun===col,bids,won)}}
function play(sA,sB,seed,log){ // A=흑(1, 첫 선) B=백(2)
 const E=TOOL,g={bd:E.emptyBoard(),t:0,pts:{1:0,2:0},sun:0},P={1:mkPlayer(sA,seed*7+1,1),2:mkPlayer(sB,seed*13+5,2)},hist=[];
 while(g.t<300){g.t++;g.sun=g.t%2?1:2;const hu=3-g.sun;g.pts[1]+=10;g.pts[2]+=10;g._dms=0;
  if(!E.legalTriples(g.bd).length)return{w:0,t:g.t,hist};
  const cells=E.validTriple(g.bd,P[g.sun].designate(g));if(!cells)throw new Error('bad triple '+(g.sun===1?sA:sB));g.cells=cells;
  const b={1:P[1].bid(g,cells),2:P[2].bid(g,cells)};
  for(const p of [1,2])if(!(Array.isArray(b[p])&&b[p].length===3&&b[p].every(x=>Number.isInteger(x)&&x>=1)&&b[p][0]+b[p][1]+b[p][2]<=g.pts[p]))throw new Error('bad bid '+(p===1?sA:sB)+' '+b[p]+' pts '+g.pts[p]);
  const pts0={1:g.pts[1],2:g.pts[2]};
  const win=E.settle(g.bd,cells,b[g.sun],b[hu],g.sun,hu).map(x=>x==='sun'?g.sun:hu);
  for(const p of [1,2])g.pts[p]-=b[p][0]+b[p][1]+b[p][2];
  if(log)hist.push({t:g.t,sun:g.sun,cells,b1:b[1],b2:b[2],p1:pts0[1],p2:pts0[2],win,est:g._est});g._est=null;
  for(const p of [1,2])P[p].observe(g,b[p],win.map(x=>x===p));
  const f1=E.fiveLines(g.bd,1).length,f2=E.fiveLines(g.bd,2).length;
  if(f1||f2)return{w:f1>f2?1:f2>f1?2:hu,t:g.t,hist,bd:g.bd};
 }
 return{w:0,t:g.t,hist}}
module.exports={play,load,TOOL,BOTS,stat};
if(require.main===module){
 const n=+process.argv[2]||100,pairs=(process.argv[3]||'ai:ultimate~bot:human').split(','),off=+process.env.SEED||0;
 if(process.env.UO){for(const k in cache);}
 for(const p of pairs){const [A,B]=p.split('~');for(const k in stat)delete stat[k];
  if(process.env.UO){for(const s of [A,B])if(s.startsWith('ai:')&&s.includes('@'))Object.assign(load(s.split('@')[1]).AI_LEVELS.ultimate,JSON.parse(process.env.UO))}
  let wa=0,wb=0,d=0,T=0,aF=0,aFn=0,aS=0,aSn=0;const t0=Date.now();
  for(let i=0;i<n;i++){const sw=i%2,seed=1000+(i+off)*31;const r=sw?play(B,A,seed):play(A,B,seed);T+=r.t;const aCol=sw?2:1;
   const aw=r.w===aCol;if(!r.w)d++;else if(aw)wa++;else wb++;if(sw){aSn++;aS+=aw}else{aFn++;aF+=aw}}
  const tm=Object.keys(stat).filter(k=>k.startsWith('ai:')).map(k=>`${k} 평균 ${(stat[k].sum/stat[k].n).toFixed(0)} p95 ${q(stat[k].a,.95)} p99 ${q(stat[k].a,.99)} 최대 ${stat[k].max.toFixed(0)}ms (>250ms ${stat[k].over})`).join(' | ');
  const line=`${A} vs ${B}: ${wa}-${wb} 무${d} A승률 ${(100*wa/n).toFixed(1)}% [A첫선 ${aF}/${aFn}, A첫후 ${aS}/${aSn}] 평균 ${(T/n).toFixed(1)}턴 ${((Date.now()-t0)/1000).toFixed(0)}s ${process.env.TM?tm:''}`;
  console.log(line);if(process.env.OUT)fs.appendFileSync(path.resolve(__dirname,process.env.OUT),line+'\n')}}
