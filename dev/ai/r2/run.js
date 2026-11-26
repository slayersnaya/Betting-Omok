// 병렬 대전: node r2/run.js N "A~B,A~B" [workers]
// env LV='{"r2/ai_r2.js":{"u2":{"base":"ultimate","x":1}}}'  (파일별 레벨 정의/덮어쓰기), SEED 오프셋, OUT 파일, TM=1 시간
const path=require('path'),fs=require('fs'),cp=require('child_process');
const H=require('../h.js');Object.assign(H.BOTS,require('./mbots.js'));
function applyLV(){if(!process.env.LV)return;const o=JSON.parse(process.env.LV);for(const f in o){const M=H.load(f==='@dep'?undefined:f);for(const k in o[f]){const x=o[f][k];
 if(x.base){M.AI_LEVELS[k]=Object.assign(JSON.parse(JSON.stringify(M.AI_LEVELS[x.base])),x);delete M.AI_LEVELS[k].base}else M.AI_LEVELS[k]=Object.assign(M.AI_LEVELS[k]||{},x)}}}
const q=(a,f)=>{if(!a.length)return 0;const b=a.slice().sort((x,y)=>x-y);return b[Math.min(b.length-1,Math.floor(f*b.length))]};
if(process.argv[2]==='--worker'){
 applyLV();const [,, ,A,B,idxs]=process.argv;const off=+process.env.SEED||0;const res=[];
 for(const i of idxs.split(',').map(Number)){const sw=i%2,seed=1000+(i+off)*31;const r=sw?H.play(B,A,seed,!!process.env.LOG):H.play(A,B,seed,!!process.env.LOG);const aCol=sw?2:1;
  res.push({i,sw,w:r.w===0?0:r.w===aCol?1:2,t:r.t,hist:process.env.LOG?r.hist:undefined})}
 const st={};for(const k in H.stat)st[k]=H.stat[k].a;
 process.send({res,st},()=>process.exit(0))}
else{
 const n=+process.argv[2]||100,pairs=(process.argv[3]||'ai:ultimate~ai:pro').split(','),W=+process.argv[4]||2;
 (async()=>{for(const p of pairs){const [A,B]=p.split('~');const t0=Date.now();
  const chunks=Array.from({length:W},()=>[]);for(let i=0;i<n;i++)chunks[i%W].push(i);
  const outs=await Promise.all(chunks.filter(c=>c.length).map(c=>new Promise((ok,ng)=>{const ch=cp.fork(__filename,['--worker',A,B,c.join(',')],{env:process.env});let got=null;ch.on('message',m=>got=m);ch.on('exit',code=>got?ok(got):ng(new Error('worker fail '+code)))})));
  const res=outs.flatMap(o=>o.res).sort((a,b)=>a.i-b.i);const st={};for(const o of outs)for(const k in o.st)(st[k]=st[k]||[]).push(...o.st[k]);
  let wa=0,wb=0,d=0,T=0,aF=0,aFn=0,aS=0,aSn=0;for(const r of res){T+=r.t;if(!r.w)d++;else if(r.w===1)wa++;else wb++;if(r.sw){aSn++;aS+=r.w===1}else{aFn++;aF+=r.w===1}}
  const tm=Object.keys(st).filter(k=>k.startsWith('ai:')&&(k.endsWith('지정+입찰')||k.endsWith('입찰'))).map(k=>`${k} p99 ${q(st[k],.99).toFixed(0)} max ${Math.max(...st[k]).toFixed(0)}`).join(' | ');
  const line=`${A} vs ${B}: ${wa}-${wb} 무${d} A승률 ${(100*wa/n).toFixed(1)}% [A첫선 ${aF}/${aFn}, A첫후 ${aS}/${aSn}] 평균 ${(T/n).toFixed(1)}턴 ${((Date.now()-t0)/1000).toFixed(0)}s ${process.env.TM?tm:''}`;
  console.log(line);if(process.env.OUT)fs.appendFileSync(path.resolve(__dirname,process.env.OUT),(process.env.TAG?process.env.TAG+' ':'')+line+'\n');
  if(process.env.LOG)fs.writeFileSync(path.resolve(__dirname,process.env.LOG),JSON.stringify(res))}})()}
