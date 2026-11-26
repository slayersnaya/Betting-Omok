// 일꾼 경로 결정성: AI 호출을 (a) 바로 (b) structuredClone 후 계산·mem 교체(일꾼 흉내) (c) 무작위 섞기 로 돌려 판 기록이 같은지
const H=require('./h.js');const M=H.load(),T=H.TOOL,B=H.BOTS;
function game(seed,mode,bot){const ac=2,hc=1,g={bd:T.emptyBoard(),t:0,pts:{1:0,2:0}};let mem=M.aiNewMem(seed*7+1);const hb=B[bot](T,seed*13+5,hc);let rs=(seed*99991)>>>0;const coin=()=>{rs=(rs*1103515245+12345)>>>0;return rs/4294967296<.5};
 const call=(f,extra)=>{const v=Object.assign({level:'ultimate',bd:g.bd.map(r=>r.slice()),t:g.t,aiSun:g.sun===ac,aiPts:g.pts[ac],aiCol:ac,mem},extra||{});
  if(mode==='direct'||(mode==='mixed'&&coin()))return f(v);const v2=structuredClone(v);const r=f(v2);mem=v2.mem;return structuredClone(r)};
 const log=[];while(g.t<300){g.t++;g.sun=g.t%2?1:2;const hu=3-g.sun;g.pts[1]+=10;g.pts[2]+=10;if(!T.legalTriples(g.bd).length)break;
  const cells=T.validTriple(g.bd,g.sun===ac?call(M.aiDesignate):hb.designate(g));g.cells=cells;
  const b={};b[ac]=call(M.aiBid,{cells});b[hc]=hb.bid(g,cells);const win=T.settle(g.bd,cells,b[g.sun],b[hu],g.sun,hu).map(x=>x==='sun'?g.sun:hu);
  for(const p of [1,2])g.pts[p]-=b[p][0]+b[p][1]+b[p][2];M.aiObserve(mem,g.t,g.sun===ac,b[ac],win.map(x=>x===ac));hb.observe(g,b[hc],win.map(x=>x===hc));
  log.push(JSON.stringify([cells,b[1],b[2]]));if(T.fiveLines(g.bd,1).length||T.fiveLines(g.bd,2).length)break}
 return log.join('|')}
let same=0,n=+process.argv[2]||20;for(let i=0;i<n;i++){const bot=['human','hoardT','threat'][i%3];const a=game(100+i,'direct',bot),b=game(100+i,'clone',bot),c=game(100+i,'mixed',bot);if(a===b&&a===c)same++;else console.log('다름',i)}
console.log(`일꾼 흉내 결정성: ${same}/${n}판 동일(바로·복제·섞기)`);
