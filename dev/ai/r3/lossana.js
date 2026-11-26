// 진 판 마지막 턴 분류: node lossana.js log.json
const R=JSON.parse(require('fs').readFileSync(process.argv[2]));const C={};let n=0;
for(const r of R){if(r.w!==2)continue;n++;const a=r.sw?2:1,o=3-a,h=r.hist,L=h[h.length-1];
 const aiSun=L.sun===a,ap=L['p'+a],op=L['p'+o],as=L['b'+a].reduce((x,y)=>x+y,0),os=L['b'+o].reduce((x,y)=>x+y,0);
 const nw=L.win.filter(w=>w===o).length;
 const k=(aiSun?'AI선':'상대선')+' 상대가딴칸'+nw+' '+(ap>=op?'AI점수≥':'AI점수<')+(as>=ap-2?' AI거의올인':' AI여유');C[k]=(C[k]||0)+1}
console.log('패',n);for(const k of Object.keys(C).sort())console.log(' ',k,C[k])
