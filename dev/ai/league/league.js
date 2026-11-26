// 베팅 오목 Ultimate 리그(자체 대국) 학습 틀: 매개변수 변이 + 토너먼트 선택
// node league/league.js gen          : 한 세대 진행(상태는 league/state.json, 기록은 league/gens.jsonl)
// node league/league.js show         : 현재 상태 요약
// env: W(작업자 수, 기본 2) RR(후보끼리 한 쌍당 판 수) GA(현재 Ultimate 상대 판 수) GP(고수 상대 판 수) GB(사람형 봇 상대 판 수)
// 원칙: 후보들은 모두 같은 AI 코드(AIF)에 다른 매개변수만 넣은 것. AI는 공개 정보+자기 정보만 씀(엔진 그대로, 규칙 그대로).
const fs=require('fs'),path=require('path'),cp=require('child_process');
const DIR=__dirname,ST=path.join(DIR,'state.json'),LOG=path.join(DIR,'gens.jsonl');
const H=require('../r3/h.js');Object.assign(H.BOTS,require('../r3/mbots.js'));
const AIF=process.env.AIF||'ai_r3.js'; // r3/ 기준 경로
// 변이 공간: [최소, 최대, 한 번에 움직이는 폭, 정수 여부]
const SPACE={lamK:[.25,.8,.08],tempo:[.15,.9,.1],dThreat:[.1,.7,.08],ins:[1,1.6,.08],insAdd:[0,8,1.5,1],resv:[.2,.9,.1],mixT:[0,6,1],jitter:[0,.1,.015],bidNoise:[.05,.3,.04],dPre:[20,50,5,1],S:[16,40,4,1],np:[30,80,8,1],res:[.1,.5,.06]};
const BASE={base:'ultimate',types:[-2,-3,-4],pfF:1};
const lvOf=p=>Object.assign({},BASE,p.params);
function load(){return fs.existsSync(ST)?JSON.parse(fs.readFileSync(ST,'utf8')):null}
function save(s){fs.writeFileSync(ST,JSON.stringify(s,null,1))}
function rngOf(seed){let s=(seed>>>0)||1;return()=>{s=(s*1103515245+12345)>>>0;return s/4294967296}}
function mutate(params,rnd,k){const o=Object.assign({},params),keys=Object.keys(SPACE);
 for(let j=0;j<k;j++){const key=keys[Math.floor(rnd()*keys.length)],[lo,hi,st,int]=SPACE[key];
  const M=H.load(AIF),cur=o[key]!=null?o[key]:(M.AI_LEVELS.ultimate[key]!=null?M.AI_LEVELS.ultimate[key]:(lo+hi)/2);
  let x=cur+(rnd()*2-1)*st*1.5;x=Math.max(lo,Math.min(hi,x));o[key]=int?Math.round(x):Math.round(x*1000)/1000}
 return o}
// ---- 병렬 대국 ----
function defineLevels(pop){const M=H.load(AIF);for(const p of pop){const x=lvOf(p),b=JSON.parse(JSON.stringify(M.AI_LEVELS[x.base]));delete x.base;M.AI_LEVELS[p.id]=Object.assign(b,x)}}
if(process.argv[2]==='--worker'){const job=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));defineLevels(job.pop);const out=[];
 for(const g of job.games){const r=g.sw?H.play(g.B,g.A,g.seed):H.play(g.A,g.B,g.seed);const aCol=g.sw?2:1;out.push({k:g.k,w:r.w===0?0:r.w===aCol?1:2,t:r.t})}
 process.send(out,()=>process.exit(0));return}
async function playAll(pop,games,W){const chunks=Array.from({length:W},()=>[]);const r=rngOf(games.length*7+1),gs=games.slice();for(let i=gs.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[gs[i],gs[j]]=[gs[j],gs[i]]}gs.forEach((g,i)=>chunks[i%W].push(g));
 const res=await Promise.all(chunks.filter(c=>c.length).map((c,i)=>new Promise((ok,ng)=>{const f=path.join(DIR,`.job${i}.json`);fs.writeFileSync(f,JSON.stringify({pop,games:c}));
  const ch=cp.fork(__filename,['--worker',f]);let got=null;ch.on('message',m=>got=m);ch.on('exit',code=>got?ok(got):ng(new Error('worker '+code)))})));return res.flat()}
const P=id=>`ai:${id}@${AIF}`;
async function gen(){let s=load();const W=+process.env.W||2,RR=+process.env.RR||16,GA=+process.env.GA||40,GP=+process.env.GP||60,GB=+process.env.GB||0;
 if(!s){const seed0=process.env.SEED0?JSON.parse(process.env.SEED0):{};const rnd=rngOf(12345);
  const pop=[{id:'g0c0',params:seed0,born:0}];for(let i=1;i<(+process.env.POP||6);i++)pop.push({id:'g0c'+i,params:mutate(seed0,rnd,2),born:0});
  s={gen:0,pop,champ:null,hof:[]};save(s)}
 const t0=Date.now(),rnd=rngOf(777+s.gen*101),pop=s.pop,games=[];let sd=s.gen*100000;
 // 1) 후보끼리 리그(자리 바꿔 가며)
 for(let i=0;i<pop.length;i++)for(let j=i+1;j<pop.length;j++)for(let g=0;g<RR;g++)games.push({k:`rr|${i}|${j}`,A:P(pop[i].id),B:P(pop[j].id),sw:g%2,seed:1000+(sd++)*31});
 // 2) 기준선: 현재 서비스 Ultimate, 고수, (선택) 사람형 봇
 for(let i=0;i<pop.length;i++){for(let g=0;g<GA;g++)games.push({k:`ult|${i}`,A:P(pop[i].id),B:'ai:ultimate',sw:g%2,seed:1000+(s.gen*997+g)*31});
  for(let g=0;g<GP;g++)games.push({k:`pro|${i}`,A:P(pop[i].id),B:'ai:pro',sw:g%2,seed:1000+(s.gen*991+g)*31});
  if(GB)for(const b of ['uhSave','mimicU'])for(let g=0;g<GB;g++)games.push({k:`bot|${i}`,A:P(pop[i].id),B:'bot:'+b,sw:g%2,seed:1000+(s.gen*983+g)*31})}
 const res=await playAll(pop,games,W);
 const st=pop.map(()=>({rrW:0,rrN:0,ult:0,ultN:0,pro:0,proN:0,bot:0,botN:0}));
 for(const r of res){const [k,a,b]=r.k.split('|').map((x,i)=>i?+x:x);const sc=r.w===1?1:r.w===0?.5:0;
  if(k==='rr'){st[a].rrW+=sc;st[a].rrN++;st[b].rrW+=1-sc;st[b].rrN++}else{st[a][k]+=sc;st[a][k+'N']++}}
 // 점수: 리그 승률 + 현재 Ultimate 상대 승률 + 고수 상대 승률(가중) [+ 봇]
 const wR=+process.env.WR||1,wA=+process.env.WA||1,wP=+process.env.WP||2,wB=+process.env.WB||1;
 pop.forEach((p,i)=>{const x=st[i];p.last={rr:x.rrW/x.rrN,ult:x.ult/x.ultN,pro:x.pro/x.proN,bot:x.botN?x.bot/x.botN:null};
  // 누적 평균(살아남은 후보는 여러 세대의 결과가 쌓여 운의 영향이 줄어듦)
  const a=p.acc||(p.acc={n:0,rr:0,ult:0,pro:0,bot:0});a.n++;for(const k of ['rr','ult','pro'])a[k]+=(p.last[k]-a[k])/a.n;if(p.last.bot!=null)a.bot+=(p.last.bot-a.bot)/a.n;
  p.fit=wR*a.rr+wA*a.ult+wP*a.pro+(x.botN?wB*a.bot:0)});
 const ranked=pop.slice().sort((a,b)=>b.fit-a.fit);
 const rec={gen:s.gen,sec:Math.round((Date.now()-t0)/1000),games:res.length,table:ranked.map(p=>({id:p.id,fit:+p.fit.toFixed(3),n:p.acc.n,rr:+p.last.rr.toFixed(3),ult:+p.last.ult.toFixed(3),pro:+p.last.pro.toFixed(3),bot:p.last.bot,params:p.params}))};
 fs.appendFileSync(LOG,JSON.stringify(rec)+'\n');
 // 토너먼트 선택: 상위 절반 생존, 나머지는 '두 명 뽑아 센 쪽' 부모를 변이해서 채움
 const keep=ranked.slice(0,Math.ceil(pop.length/2)),next=keep.slice();s.gen++;
 while(next.length<pop.length){const a=keep[Math.floor(rnd()*keep.length)],b=keep[Math.floor(rnd()*keep.length)],par=a.fit>=b.fit?a:b;
  next.push({id:`g${s.gen}c${next.length}`,params:mutate(par.params,rnd,1+Math.floor(rnd()*2)),born:s.gen,parent:par.id})}
 s.pop=next;s.champ={id:ranked[0].id,params:ranked[0].params,fit:ranked[0].fit,n:ranked[0].acc.n,acc:ranked[0].acc,gen:s.gen-1};
 s.hof.push({gen:s.gen-1,id:ranked[0].id,params:ranked[0].params,fit:+ranked[0].fit.toFixed(3)});save(s);
 console.log(`세대 ${rec.gen}: ${res.length}판 ${rec.sec}s`);for(const r of rec.table)console.log(`  ${r.id.padEnd(7)} fit ${r.fit} (누적${r.n}) 리그 ${r.rr} vsUlt ${r.ult} vsPro ${r.pro}${r.bot!=null?' 봇 '+r.bot:''} ${JSON.stringify(r.params)}`)}
function show(){const s=load();if(!s)return console.log('상태 없음');console.log('다음 세대',s.gen,'챔피언',JSON.stringify(s.champ));for(const p of s.pop)console.log(' ',p.id,JSON.stringify(p.params),p.fit!=null?p.fit.toFixed(3):'')}
if(process.argv[2]==='gen')gen().catch(e=>{console.error(e);process.exit(1)});else show();
