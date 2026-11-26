// PF 입자 덤프: node pfdump.js file level game
const fs=require('fs');const file=process.argv[2],lvl=process.argv[3],G=+process.argv[4];
const src=fs.readFileSync('/home/claude/eval/ai/snap/index_1126_0321.html','utf8');const ENG=src.slice(src.indexOf('// ===== ENGINE START'),src.indexOf('// ===== ENGINE END'));
const M={};new Function('M',ENG+fs.readFileSync(file,'utf8')+'\nObject.assign(M,{emptyBoard,aiBid,aiObserve,aiNewMem,AI_LEVELS,aiOppModel,aiPFom});')(M);
if(process.env.LV){const o=JSON.parse(process.env.LV);for(const k in o){const x=o[k];if(x.base){M.AI_LEVELS[k]=Object.assign(JSON.parse(JSON.stringify(M.AI_LEVELS[x.base])),x);delete M.AI_LEVELS[k].base}else Object.assign(M.AI_LEVELS[k],x)}}
const d=JSON.parse(fs.readFileSync('/home/claude/eval/ai/real/aigames_1126.json'));const g=d.games[G];
const mem=M.aiNewMem(7919),bd=M.emptyBoard();let ptsB=0,ptsA=0;
for(const h of g.hist){ptsB+=10;ptsA+=10;const v={level:lvl,bd:bd.map(r=>r.slice()),t:h.t,aiSun:h.sun==='B',aiPts:ptsB,aiCol:2,mem,cells:h.cells};M.aiBid(v);
 const ty={};for(const p of mem.pf){(ty[p.k]=ty[p.k]||[]).push(p.b+10)}
 console.log(`t${h.t} sun ${h.sun} hum ${h.bA}/${ptsA} ai ${h.bB} win ${h.win.join('')} V ${mem.cur.V.map(x=>Math.round(x)).join(',')}`);
 console.log('   ',Object.entries(ty).map(([k,a])=>k+':'+a.sort((x,y)=>x-y).join(',')).join(' | '));
 M.aiObserve(mem,h.t,h.sun==='B',h.bB,h.win.map(w=>w==='B'));ptsB-=h.bB.reduce((x,y)=>x+y,0);ptsA-=h.bA.reduce((x,y)=>x+y,0);h.cells.forEach(([r,c],i)=>bd[r][c]=h.win[i]==='A'?1:2)}
