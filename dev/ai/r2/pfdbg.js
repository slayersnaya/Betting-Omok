// 기록된 판을 AI 쪽에서 다시 돌려 입자 상태 보기: node r2/pfdbg.js log.json gameIdx LVjson
const fs=require('fs');const H=require('../h.js');const r=JSON.parse(fs.readFileSync(process.argv[2]));const g=r.find(x=>x.i===+process.argv[3]);
const F='r2/ai_r2.js',M=H.load(F);const L=JSON.parse(process.argv[4]||'{"c":{"base":"ultimate"}}');for(const k in L){M.AI_LEVELS[k]=Object.assign(JSON.parse(JSON.stringify(M.AI_LEVELS[L[k].base])),L[k]);delete M.AI_LEVELS[k].base}
const sw=g.sw,seed=1000+(g.i+(+process.env.SEED||0))*31,col=sw?2:1,mem=M.aiNewMem(sw?seed*13+5:seed*7+1);const bd=M.emptyBoard();
for(const h of g.hist){const sun=h.sun===col;const v={level:'c',bd:bd.map(x=>x.slice()),t:h.t,aiSun:sun,aiPts:col===1?h.p1:h.p2,aiCol:col,mem};
 if(sun)M.aiDesignate(v);const b=M.aiBid(Object.assign({},v,{cells:h.cells}));const mine=col===1?h.b1:h.b2,opp=col===1?h.b2:h.b1;
 const pf=mem.pf||[];const ty={};pf.forEach(p=>{const k=p.k<0?p.k:'opt';(ty[k]=ty[k]||[]).push(p.b)});
 M.aiObserve(mem,h.t,sun,mine,h.win.map(w=>w===col));const pf2=mem.pf||[];const ty2={};pf2.forEach(p=>{const k=p.k<0?p.k:'opt';(ty2[k]=ty2[k]||[]).push(p.b)});
 const f=o=>Object.entries(o).map(([k,a])=>k+':'+a.length+'/'+Math.round(a.reduce((x,y)=>x+y,0)/a.length)).join(' ');
 console.log(`t${h.t} ${sun?'AI선':'상대선'} bid ${b} (기록 ${mine}) opp ${opp} opp점수 ${col===1?h.p2:h.p1} | 전 ${f(ty)} | 후 ${f(ty2)}`);
 h.cells.forEach(([y,x],i)=>bd[y][x]=h.win[i])}
