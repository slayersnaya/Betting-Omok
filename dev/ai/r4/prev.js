// 진 판들의 마지막 AI-선 턴 상태: node prev.js log.json
const R=JSON.parse(require('fs').readFileSync(process.argv[2]));const H=require('./h.js'),E=H.TOOL,M=H.load('ai_r4.js');
const fiveCells=(bd,col)=>{const s=[];for(let r=0;r<19;r++)for(let c=0;c<19;c++)if(!bd[r][c]){bd[r][c]=col;if(M.aiIsFive(bd,r,c,col))s.push(r*19+c);bd[r][c]=0}return s};
const C={};
for(const g of R){if(g.w!==2)continue;const a=g.sw?2:1,o=3-a,bd=E.emptyBoard();let last=null;
 for(const h of g.hist){if(h.sun===a&&h!==g.hist[g.hist.length-1]){const f=fiveCells(bd,o);last={t:h.t,thO:M.aiThreat(bd,o),f:f.length,inc:h.cells.some(([r,c])=>f.includes(r*19+c)),ap:h['p'+a],op:h['p'+o],ab:h['b'+a].reduce((x,y)=>x+y,0),ob:h['b'+o].reduce((x,y)=>x+y,0),win:h.win.map(w=>w===a?'A':'o').join(''),lastT:g.hist.length}}
  h.cells.forEach(([r,c],i)=>bd[r][c]=h.win[i])}
 console.log(`g${g.i} lastAIsun t${last.t}/${last.lastT} thO ${last.thO} oppFiveCells ${last.f} designatedIt ${last.inc} AI ${last.ab}/${last.ap} opp ${last.ob}/${last.op} ${last.win}`)}
