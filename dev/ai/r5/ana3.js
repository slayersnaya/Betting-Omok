// 상대 위협이 처음 th<=1, th<=2 된 턴 종류: node ana3.js log.json
const R=JSON.parse(require('fs').readFileSync(process.argv[2]));const H=require('./h.js'),E=H.TOOL,M=H.load('ai_pf.js');
const C={};const inc=(k)=>C[k]=(C[k]||0)+1;
for(const g of R){const k=g.w===1?'W':g.w===2?'L':null;if(!k)continue;const a=g.sw?2:1,o=3-a,bd=E.emptyBoard();let f1=null,f2=null;
 for(const h of g.hist){h.cells.forEach(([r,c],i)=>bd[r][c]=h.win[i]);const th=M.aiThreat(bd,o);
  if(th<=2&&f2==null){f2=h.sun===a?'AI선':'상대선'}if(th<=1&&f1==null){f1=h.sun===a?'AI선':'상대선';
   const ap=h['p'+a]-h['b'+a].reduce((x,y)=>x+y,0),op=h['p'+o]-h['b'+o].reduce((x,y)=>x+y,0);inc(k+' th1@'+f1+(ap>=op?' 점수≥':' 점수<'))}}
 inc(k+' th2@'+f2)}
console.log(Object.keys(C).sort().map(k=>k+' '+C[k]).join('\n'))
