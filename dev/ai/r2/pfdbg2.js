const fs=require('fs');const src=fs.readFileSync('/home/claude/betting-omok/index.html','utf8');const ENG=src.slice(src.indexOf('// ===== ENGINE START'),src.indexOf('// ===== ENGINE END'));
const M={};new Function('M',ENG+fs.readFileSync('r2/ai_r2.js','utf8')+'\nObject.assign(M,{emptyBoard,aiOutcomes2,aiOppSim,aiRef,AI_LEVELS,AI_KS});')(M);
const r=JSON.parse(fs.readFileSync(process.argv[2]));const g=r.find(x=>x.i===+process.argv[3]);const T=+process.argv[4];const col=g.sw?2:1;const bd=M.emptyBoard();
for(const h of g.hist){if(h.t===T){const sun=h.sun===col;const V=M.aiOutcomes2(bd.map(x=>x.slice()),h.cells,col,sun,!sun,M.AI_LEVELS.ultimate);console.log('V',V.map(Math.round).join(' '));
  const ref=M.aiRef(V);let s=5;const rnd=()=>{s=(s*1103515245+12345)>>>0;return s/4294967296};
  for(const k of [.02,.05,.09,.14,.2,.3,.45,-2,-3])for(const B of [20,40])console.log('k',k,'B',B,'sim',M.aiOppSim(V,B,!sun,col===1?h.p1:h.p2,k<0?k:ref*k,rnd).join(','));break}
 h.cells.forEach(([y,x],i)=>bd[y][x]=h.win[i])}
