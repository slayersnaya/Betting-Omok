// 게임 디자이너 시험: 현재 원본의 엔진+AI를 그대로 떼어 와서 '사람처럼 두는' 정책과 붙여 봄
const fs=require('fs');
const src=fs.readFileSync('/home/claude/eval/ai/snap/index_1126_0321.html','utf8');
const a=src.indexOf('// ===== ENGINE START'),b=src.indexOf('// ===== AI END');
let code=src.slice(a,b);if(process.env.AIFILE){const e=src.indexOf('// ===== ENGINE END =====');code=src.slice(a,e)+require('fs').readFileSync(process.env.AIFILE,'utf8')}
const M={};new Function('M',code+'\nObject.assign(M,{N,DIRS,inB,emptyBoard,legalTriples,validTriple,fiveLines,settle,aiDesignate,aiBid,aiObserve,aiNewMem,AI_LEVELS,aiCell,aiIsFive});')(M);
const {N,DIRS,inB}=M;if(process.env.LV){const o=JSON.parse(process.env.LV);for(const k in o){const x=o[k];if(x.base){M.AI_LEVELS[k]=Object.assign(JSON.parse(JSON.stringify(M.AI_LEVELS[x.base])),x);delete M.AI_LEVELS[k].base}else Object.assign(M.AI_LEVELS[k],x)}}
let seed=1;const R=()=>{seed=(seed*1103515245+12345)>>>0;return seed/4294967296};
const ri=n=>Math.floor(R()*n);
// 이 칸에 col 돌을 놓으면 정확히 5목인지
function makes5(bd,r,c,col){if(bd[r][c])return false;bd[r][c]=col;const f=M.aiIsFive(bd,r,c,col);bd[r][c]=0;return f}
function near(bd,r,c,d){for(let y=r-d;y<=r+d;y++)for(let x=c-d;x<=c+d;x++)if(inB(y,x)&&bd[y][x])return true;return false}
function nearCol(bd,r,c,d,col){for(let y=r-d;y<=r+d;y++)for(let x=c-d;x<=c+d;x++)if(inB(y,x)&&bd[y][x]===col)return true;return false}
// 사람 정책들
const own3=(bd,cs,col)=>{const b=bd.map(r=>r.slice());cs.forEach(([r,c])=>b[r][c]=col);return cs.some(([r,c])=>M.aiIsFive(b,r,c,col))};
const H={
 hoarder:{des(v){const L=M.legalTriples(v.bd);const f=L.filter(cs=>own3(v.bd,cs,v.col)&&!cs.some(([r,c])=>makes5(v.bd,r,c,v.col)));if(f.length&&v.sun)return f[ri(f.length)];return H.casual.des(v)},
  bid(v){const mine=v.cells.some(([r,c])=>makes5(v.bd,r,c,v.col))||own3(v.bd,v.cells,v.col);const theirs=v.cells.some(([r,c])=>makes5(v.bd,r,c,3-v.col))||own3(v.bd,v.cells,3-v.col);
   if(mine&&v.sun){const q=Math.floor(v.pts/3);const o=[q,q,q];let r=v.pts-3*q;for(let i=0;r>0;i=(i+1)%3,r--)o[i]++;return o}
   if(theirs)return H.casual.bid(v);if(mine)return H.casual.bid(v);return v.sun?H.casual.bid(v):[1,1,1]}},
 // 갓 규칙을 배운 사람: 내 돌 근처 아무 세 칸, 베팅은 대충(가진 점수의 30~80%를 무작위로 나눔), 위협을 잘 못 봄
 newbie:{des(v){const L=M.legalTriples(v.bd);const own=L.filter(cs=>cs.some(([r,c])=>nearCol(v.bd,r,c,1,v.col)));const nr=L.filter(cs=>cs.some(([r,c])=>near(v.bd,r,c,1)));
   const pool=own.length?own:nr.length?nr:L.filter(cs=>cs.every(([r,c])=>Math.abs(r-9)<=2&&Math.abs(c-9)<=2));return pool[ri(pool.length)]},
  bid(v){const sp=Math.max(3,Math.floor(v.pts*(.3+.5*R())));const w=[R()+.2,R()+.2,R()+.2];
   // 내 5목 칸이 눈에 띄면 절반 확률로 그 칸에 더 줌
   v.cells.forEach(([r,c],i)=>{if(makes5(v.bd,r,c,v.col)&&R()<.5)w[i]+=3;if(makes5(v.bd,r,c,3-v.col)&&R()<.6)w[i]+=4});
   const s=w[0]+w[1]+w[2];let o=w.map(x=>Math.max(1,Math.floor(sp*x/s)));while(o[0]+o[1]+o[2]>v.pts)o[o.indexOf(Math.max(...o))]--;return o}},
 learner:{des(v){return H.newbie.des(v)},bid(v){const o=H.casual.bid(v);const s=o[0]+o[1]+o[2];if(s>=v.pts-2){const i=o.indexOf(Math.max(...o));o[i]=Math.max(1,Math.floor(o[i]*(.6+.3*R())))}return o}},
 // 힌트를 읽는 초보: 앱 힌트(한 칸·두 칸 위협)가 뜨면 그 칸에 70% 몰아 걸기
 newbieH:{des(v){return H.newbie.des(v)},bid(v){const b=v.bd.map(r=>r.slice()),cs=v.cells,hot=new Set();const five=(col,idx)=>{idx.forEach(i=>b[cs[i][0]][cs[i][1]]=col);const f=idx.some(i=>M.aiIsFive(b,cs[i][0],cs[i][1],col));idx.forEach(i=>b[cs[i][0]][cs[i][1]]=0);return f};
  for(const col of [3-v.col,v.col]){for(let i=0;i<3;i++)if(five(col,[i]))hot.add(i);if(!hot.size)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(five(col,[i,j])){hot.add(i);hot.add(j)}if(hot.size)break}
  if(!hot.size)return H.newbie.bid(v);const o=[1,1,1];const sp=Math.floor((v.pts-3)*.7);const hs=[...hot];hs.forEach((i,k)=>o[i]+=Math.floor(sp/hs.length));return o}},
 // 오목을 아는 보통 사람: 내 줄을 키우는 세 칸, 내 5목·상대 5목 칸은 크게, 나머지는 가치 비례로 절반쯤 씀
 casual:{des(v){const L=M.legalTriples(v.bd).filter(cs=>cs.some(([r,c])=>near(v.bd,r,c,2)));const pool=L.length?L:M.legalTriples(v.bd).filter(cs=>cs.every(([r,c])=>Math.abs(r-9)<=1&&Math.abs(c-9)<=1));
   const sc=pool.map(cs=>[cs.reduce((s,[r,c])=>s+M.aiCell(v.bd,r,c,v.col)+.5*M.aiCell(v.bd,r,c,3-v.col),0)*(0.7+0.6*R()),cs]).sort((x,y)=>y[0]-x[0]);return sc[ri(Math.min(4,sc.length))][1]},
  bid(v){const val=v.cells.map(([r,c])=>{if(makes5(v.bd,r,c,v.col))return 1e5;if(makes5(v.bd,r,c,3-v.col))return 5e4;return 1+M.aiCell(v.bd,r,c,v.col)+M.aiCell(v.bd,r,c,3-v.col)});
   const crit=val.some(x=>x>=5e4);const sp=crit?v.pts:Math.max(3,Math.floor(v.pts*(.35+.3*R())));
   let o;if(crit){o=[1,1,1];const i=val.indexOf(Math.max(...val));o[i]=v.pts-2}else{const s=val[0]+val[1]+val[2];o=val.map(x=>Math.max(1,Math.floor(sp*x/s)))}
   while(o[0]+o[1]+o[2]>v.pts)o[o.indexOf(Math.max(...o))]--;return o}},
};
const AIM={};function mkAI(l){const mem=AIM.m;const v=x=>({level:l,bd:x.bd,t:x.t,aiSun:x.sun,aiPts:x.pts,aiCol:1,mem:AIM.m,cells:x.cells});return{des:x=>M.aiDesignate(v(x)),bid:x=>M.aiBid(v(x))}}
function play(hum,lvl,s0,humFirst){AIM.m=M.aiNewMem(s0*97+3);
 seed=s0*2654435761>>>0||7;const bd=M.emptyBoard(),mem=M.aiNewMem(s0*31+7);const pts={A:0,B:0};let t=0;const first=humFirst?'A':'B';const spent={A:0,B:0};
 while(t<300){t++;const sun=t%2?first:(first==='A'?'B':'A'),hu=sun==='A'?'B':'A';pts.A+=10;pts.B+=10;
  if(!M.legalTriples(bd).length)return{w:'D',t};
  const av=x=>Object.assign({level:lvl,bd:bd.map(r=>r.slice()),t,aiSun:sun==='B',aiPts:pts.B,aiCol:2,mem},x||{});
  const hv=x=>Object.assign({bd:bd.map(r=>r.slice()),t,pts:pts.A,col:1,sun:sun==='A'},x||{});
  const hp=H[hum]||mkAI(hum);let cells=sun==='B'?M.validTriple(bd,M.aiDesignate(av())):M.validTriple(bd,hp.des(hv()));if(!cells)cells=M.legalTriples(bd)[0];
  const bets={B:M.aiBid(av({cells})),A:hp.bid(hv({cells}))};
  const win=M.settle(bd,cells,bets[sun],bets[hu],sun==='A'?1:2,hu==='A'?1:2).map(w=>w==='sun'?sun:hu);
  for(const x of['A','B']){const s=bets[x][0]+bets[x][1]+bets[x][2];pts[x]-=s;spent[x]+=s}
  if(process.env.TRACE)console.log(' t'+t,'sun',sun,cells.map(c=>c.join('.')).join(' '),'A(hum)',bets.A.join(','),'B(ai)',bets.B.join(','),'pts',pts.A,pts.B,win.join(''));
  M.aiObserve(mem,t,sun==='B',bets.B,win.map(w=>w==='B'));if(!H[hum])M.aiObserve(AIM.m,t,sun==='A',bets.A,win.map(w=>w==='A'));
  const fA=M.fiveLines(bd,1).length,fB=M.fiveLines(bd,2).length;
  if(fA||fB)return{w:fA>fB?'A':fB>fA?'B':hu,t};
 }
 return{w:'D',t}}
const n=+process.argv[2]||30,hums=(process.argv[3]||'newbie,casual').split(','),lvls=(process.argv[4]||'beginner,mid,pro,ultimate').split(',');
for(const h of hums)for(const l of lvls){let w=0,d=0,T=0,tw=[];const t0=Date.now();for(let i=0;i<n;i++){if(process.env.ONLY&&!process.env.ONLY.split(',').includes(String(i)))continue;if(process.env.TRACE)console.log('game',i);const r=play(h,l,i+1,i%2===0);if(process.env.PW)console.log('G',i,r.w);T+=r.t;if(r.w==='A'){w++;tw.push(r.t)}else if(r.w==='D')d++}
 console.log(JSON.stringify({human:h,ai:l,n,humanWin:w,rate:Math.round(100*w/n)+'%',draw:d,avgTurns:(T/n).toFixed(1),ms:Math.round((Date.now()-t0)/n)}))}
