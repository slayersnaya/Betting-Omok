// 상대 점수 추정 오차: node est.js N "A~B" → AI(A)가 매 턴 입찰 때 추정한 상대 점수(입자 평균·최대) vs 실제
const H=require('./h.js');const n=+process.argv[2]||20,[A,B]=(process.argv[3]||'ai:ultimate~bot:uh').split('~');
let k=0,sumT=0,sumE=0,over=0,overMax=0,crit=0,critOver=0;const T=H.TOOL;
for(let i=0;i<n;i++){const sw=i%2,seed=1000+i*31;const r=sw?H.play(B,A,seed,true):H.play(A,B,seed,true);const ac=sw?2:1;
 for(const h of r.hist){const e=h.est&&h.est[ac];if(!e)continue;const tru=ac===1?h.p2:h.p1;k++;sumT+=tru;sumE+=e.est;if(tru>e.est*1.3+5)over++;if(tru>e.pmax)overMax++}}
console.log(`${B}: 턴 ${k} 실제 평균 ${(sumT/k).toFixed(1)} 추정 평균 ${(sumE/k).toFixed(1)} | 실제>추정×1.3+5: ${(100*over/k).toFixed(0)}% | 실제>입자최대: ${(100*overMax/k).toFixed(0)}%`);
