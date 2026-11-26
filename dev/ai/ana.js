// 패배 판 분석: node ana.js N "ai:ultimate~bot:uh"  → AI(A)가 진 판의 마지막 턴 유형
const H=require('./h.js');const T=H.TOOL,W=T.AI_WIN;
const n=+process.argv[2]||40,[A,B]=(process.argv[3]||'ai:ultimate~bot:uh').split('~'),off=+process.env.SEED||0;
const types={};let L=0;const ex=[];
for(let i=0;i<n;i++){const sw=i%2,seed=1000+(i+off)*31;const r=sw?H.play(B,A,seed,true):H.play(A,B,seed,true);const ac=sw?2:1,oc=3-ac;
 if(!r.w||r.w===ac)continue;L++;const h=r.hist[r.hist.length-1];
 // 마지막 턴 직전 판 복원
 const bd=T.emptyBoard();for(const x of r.hist.slice(0,-1))x.cells.forEach(([y,c],k)=>bd[y][c]=x.win[k]);
 const aiSun=h.sun===ac,V=T.aiOutcomes2(bd.map(q=>q.slice()),h.cells,ac,aiSun,!aiSun);
 const neg=[];for(let m=0;m<8;m++)if(V[m]<=-W)neg.push(m);const Hs=[0,1,2].filter(k=>neg.every(m=>!((m>>k)&1)));
 const ab=ac===1?h.b1:h.b2,ob=ac===1?h.b2:h.b1,ap=ac===1?h.p1:h.p2,op=ac===1?h.p2:h.p1;
 // AI 입장의 상대 점수 상한(돌 결과로 계산)
 let low=0;for(const x of r.hist.slice(0,-1)){const s=x.sun===ac,b=ac===1?x.b1:x.b2;for(let k=0;k<3;k++){const won=x.win[k]===ac;low+=won?1:(s?b[k]:b[k]+1)}}
 const oppMax=10*h.t-low;
 const canSure=Hs.length>=1&&(ap-2>=oppMax-2+(aiSun?1:0));
 const kind=(neg.length?`막기칸${Hs.length}`:'공격실패/동시')+`|AI${aiSun?'선':'후'}|${canSure?'확실히막을수있었음':ap>op?'AI점수많음':'AI점수적음'}|${h.sun===ac?'AI지정':'상대지정'}`;
 types[kind]=(types[kind]||0)+1;
 if(ex.length<12)ex.push(`추정${JSON.stringify(h.est&&h.est[ac])} t${h.t} AI${aiSun?'선':'후'} AI점수${ap} 상대점수${op} 상대상한${oppMax} AI입찰${ab} 상대입찰${ob} 막기칸${JSON.stringify(Hs)} V음수${neg.length}`);
}
console.log(`${A} vs ${B}: AI 패 ${L}/${n}`);for(const k of Object.keys(types).sort((a,b)=>types[b]-types[a]))console.log(' ',types[k],k);ex.forEach(x=>console.log('  ',x));
