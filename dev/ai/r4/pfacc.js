// 입자필터 정확도: node pfacc.js log.json  (진실 상대점수 vs est/pmax)
const R=JSON.parse(require('fs').readFileSync(process.argv[2]));let n=0,se=0,ae=0,over=0,overBig=0;
for(const g of R){const a=g.sw?2:1,o=3-a;for(const h of g.hist){const e=h.est&&h.est[a];if(!e)continue;const tr=h['p'+o];n++;se+=tr-e.est;ae+=Math.abs(tr-e.est);if(tr>e.pmax)over++;if(tr>e.pmax+5)overBig++}}
console.log(`n ${n} 평균(진실-추정) ${(se/n).toFixed(2)} 평균절대오차 ${(ae/n).toFixed(2)} 진실>pmax ${(100*over/n).toFixed(1)}% 진실>pmax+5 ${(100*overBig/n).toFixed(1)}%`)
