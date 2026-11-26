// node show.js log.json gi [k=5] : 진 판 마지막 k턴
const R=JSON.parse(require('fs').readFileSync(process.argv[2]));const gi=+process.argv[3],k=+process.argv[4]||5;
const H=require('./h.js'),E=H.TOOL;const g=R.find(r=>r.i===gi);const a=g.sw?2:1,o=3-a;const bd=E.emptyBoard();
const M=H.load('ai_r4.js');
for(const h of g.hist){const show=h.t>g.hist.length-k;
 if(show){const thO=M.aiThreat(bd,o),thA=M.aiThreat(bd,a);console.log(`t${h.t} ${h.sun===a?'AI선':'상대선'} cells ${JSON.stringify(h.cells)} AI ${h['b'+a]}(${h['p'+a]}) 상대 ${h['b'+o]}(${h['p'+o]}) win ${h.win.map(w=>w===a?'A':'o').join('')} 위협(턴前) 상대${thO} AI${thA} est ${JSON.stringify(h.est&&h.est[a])}`)}
 h.cells.forEach(([r,c],i)=>bd[r][c]=h.win[i])}
