// 진 판의 마지막 턴 분류
const r=JSON.parse(require('fs').readFileSync(process.argv[2]));const C={};
for(const g of r){if(g.w!==2)continue;const h=g.hist[g.hist.length-1];const aCol=g.sw?2:1,oCol=3-aCol;const ab=aCol===1?h.b1:h.b2,ob=aCol===1?h.b2:h.b1;const ap=aCol===1?h.p1:h.p2,op=aCol===1?h.p2:h.p1;
 const won=h.win.filter(x=>x===oCol).length;const k=(h.sun===aCol?'AI선':'상대선')+' 상대가 '+won+'칸';(C[k]=C[k]||[]).push(`g${g.i} t${h.t} AI ${ab}(${ap}) 상대 ${ob}(${op}) ${JSON.stringify(h.est&&h.est[aCol])}`)}
for(const k in C){console.log(k,C[k].length);C[k].slice(0,+process.argv[3]||6).forEach(x=>console.log('  ',x))}
