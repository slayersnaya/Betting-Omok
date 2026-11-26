// 턴 종류별 지출차(AI-상대)와 딴 칸: node ana2.js log.json
const R=JSON.parse(require('fs').readFileSync(process.argv[2]));
const A={W:{S:[0,0,0,0],h:[0,0,0,0]},L:{S:[0,0,0,0],h:[0,0,0,0]}};
for(const g of R){const k=g.w===1?'W':g.w===2?'L':null;if(!k)continue;const a=g.sw?2:1,o=3-a;
 for(const h of g.hist.slice(0,-1)){const ty=h.sun===a?'S':'h';const as=h['b'+a].reduce((x,y)=>x+y,0),os=h['b'+o].reduce((x,y)=>x+y,0),aw=h.win.filter(w=>w===a).length;
  const s=A[k][ty];s[0]++;s[1]+=as-os;s[2]+=aw;s[3]+=as}}
for(const k of ['W','L'])for(const ty of ['S','h']){const s=A[k][ty];console.log(k,ty==='S'?'AI선':'상대선','턴',s[0],'평균지출차',(s[1]/s[0]).toFixed(2),'AI딴칸',(s[2]/s[0]).toFixed(2),'AI지출',(s[3]/s[0]).toFixed(2))}
