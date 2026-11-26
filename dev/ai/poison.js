// 학습 오염 시험: node poison.js N bot mode   (mode: none | low | high | real)
// low = '사람은 늘 1점' 가짜 문서 60개(ts 조작으로 늘 최신), high = '사람은 늘 40점 이상' 60개, real = 같은 봇과 60판 둔 진짜 기록 학습
const H=require('./h.js');const M=H.load(process.env.AIF||undefined);
const n=+process.argv[2]||60,bot=process.argv[3]||'human',mode=process.argv[4]||'none';
const LEN=1440;
function fake(bin){const h=new Array(LEN).fill(0);for(let k=0;k<144;k++)h[k*10+bin]=400;return{v:1,h,g:999,ts:9e15}}
if(mode==='low'||mode==='high'){const docs=[];for(let i=0;i<60;i++)docs.push({id:'atk'+i,data:fake(mode==='low'?0:9)});M.aiLearnSet(null,docs,'me')}
if(mode==='real'){let agg=null;for(let i=0;i<60;i++){const sw=i%2,r=sw?H.play('bot:'+bot,'ai:ultimate',50000+i*7,true):H.play('ai:ultimate','bot:'+bot,50000+i*7,true);const hc=sw?1:2,hum=hc===1?'A':'B';
  const hist=r.hist.map(x=>({t:x.t,sun:x.sun===1?'A':'B',cells:x.cells,bets:{A:x.b1,B:x.b2},win:x.win.map(c=>c===1?'A':'B'),auto:{}}));agg=M.aiLearnGame(agg,hist,hum,hc,3-hc)}
 M.aiLearnSet(agg,[],'me')}
console.log('학습 켜짐:',M.AI_LRN.on,'관측 수',Math.round(M.AI_LRN.n));
let w=0,T=0;for(let i=0;i<n;i++){const sw=i%2,seed=1000+i*31;const r=sw?H.play('bot:'+bot,'ai:ultimate',seed):H.play('ai:ultimate','bot:'+bot,seed);if(r.w===(sw?2:1))w++;T+=r.t}
console.log(`학습 ${mode} / Ultimate vs ${bot}: ${w}/${n} (${(100*w/n).toFixed(0)}%) 평균 ${(T/n).toFixed(1)}턴`);
