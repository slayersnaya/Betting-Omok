// 점수 차 궤적: node traj.js log.json
const R=JSON.parse(require('fs').readFileSync(process.argv[2]));const H=require('./h.js'),E=H.TOOL,M=H.load('ai_r4.js');
const S={W:{n:0,f:0,dAt:[]},L:{n:0,f:0,dAt:[]}};const big={W:[],L:[]};
for(const g of R){const k=g.w===1?'W':g.w===2?'L':null;if(!k)continue;const a=g.sw?2:1,o=3-a,bd=E.emptyBoard();S[k].n++;let first=null;const spends=[];
 for(const h of g.hist){const th=M.aiThreat(bd,o);if(th===1&&first==null){first=h.t;S[k].f++;S[k].dAt.push(h['p'+a]-h['p'+o])}
  const as=h['b'+a].reduce((x,y)=>x+y,0),os=h['b'+o].reduce((x,y)=>x+y,0),aw=h.win.filter(w=>w===a).length;
  spends.push(`${h.sun===a?'S':'h'}${as-os>=0?'+':''}${as-os}/${aw}`);
  h.cells.forEach(([r,c],i)=>bd[r][c]=h.win[i])}
 if(k==='L')big.L.push(`g${g.i} first5@${first} `+spends.join(' '))}
const avg=a=>a.length?(a.reduce((x,y)=>x+y,0)/a.length).toFixed(1):'-';
for(const k of ['W','L'])console.log(k,'games',S[k].n,'opp got five-cell',S[k].f,'avg diff then',avg(S[k].dAt));
big.L.slice(0,40).forEach(x=>console.log(x));
