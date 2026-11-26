// 실제 기록을 AI에 다시 넣어 보기: node r2/replay2.js file level [LVjson]
const fs=require('fs');const file=process.argv[2]||'r2/ai_r2.js',lvl=process.argv[3]||'ultimate';
const src=fs.readFileSync('/home/claude/betting-omok/index.html','utf8');const ENG=src.slice(src.indexOf('// ===== ENGINE START'),src.indexOf('// ===== ENGINE END'));
const M={};new Function('M',ENG+fs.readFileSync(require('path').resolve('/home/claude/eval/ai',file),'utf8')+'\nObject.assign(M,{emptyBoard,aiBid,aiObserve,aiNewMem,AI_LEVELS,aiOppModel,aiPFom,aiDesignate});')(M);
if(process.env.LV){const o=JSON.parse(process.env.LV);for(const k in o){const x=o[k];if(x.base){M.AI_LEVELS[k]=Object.assign(JSON.parse(JSON.stringify(M.AI_LEVELS[x.base])),x);delete M.AI_LEVELS[k].base}else Object.assign(M.AI_LEVELS[k],x)}}
const d=JSON.parse(fs.readFileSync('/home/claude/eval/ai/real/aigames_1126.json'));const all=!!process.env.ALL;let block=0,tot=0;
for(const [gi,g] of d.games.entries()){if(!all&&g.winner!=='A')continue;const R=[];
 for(let seed of [1,2,3,4,5,6,7,8]){const mem=M.aiNewMem(seed*7919),bd=M.emptyBoard();let ptsB=0,ptsA=0;
  for(const h of g.hist){ptsB+=10;ptsA+=10;const aiSun=h.sun==='B';const v={level:lvl,bd:bd.map(r=>r.slice()),t:h.t,aiSun,aiPts:ptsB,aiCol:2,mem,cells:h.cells};
   const bid=M.aiBid(v);const last=h===g.hist[g.hist.length-1];
   if(process.env.V&&seed===1){const om=M.aiOppModel(v,M.AI_LEVELS[lvl]),pf=M.aiPFom(mem,M.AI_LEVELS[lvl]);console.log(`g${gi} t${h.t} sun ${h.sun} AIpts ${ptsB} bid ${bid} rec ${h.bB} | 사람 ${h.bA} pts ${ptsA} | oppMax ${om.oppMax} pfEst ${pf.oppEst.toFixed(0)} pfMax ${pf.oppMax}`)}
   if(last&&g.winner==='A'){const wins=h.bA.every((a,i)=>a>bid[i]);R.push(`${bid}${wins?'X':'O'}`);tot++;if(!wins)block++}
   M.aiObserve(mem,h.t,aiSun,h.bB,h.win.map(w=>w==='B'));ptsB-=h.bB.reduce((x,y)=>x+y,0);ptsA-=h.bA.reduce((x,y)=>x+y,0);
   h.cells.forEach(([r,c],i)=>bd[r][c]=h.win[i]==='A'?1:2)}}
 if(R.length)console.log('game',gi,'결정적 턴(사람 선, 세 칸 오목) AI 입찰(시드 8개):',R.join(' '))}
console.log('막음',block,'/',tot);
