const H=require('./h.js');const T=H.TOOL,W=T.AI_WIN;const n=+process.argv[2]||20,[A,B]=(process.argv[3]||'ai:ultimate~bot:uh').split('~');
const st={};const add=(k,x)=>{(st[k]||(st[k]=[])).push(x)};
for(let i=0;i<n;i++){const sw=i%2,seed=1000+i*31;const r=sw?H.play(B,A,seed,true):H.play(A,B,seed,true);const ac=sw?2:1;const bd=T.emptyBoard();
 for(const h of r.hist){const sun=h.sun===ac,V=T.aiOutcomes2(bd.map(q=>q.slice()),h.cells,ac,sun,!sun),crit=V.some(x=>Math.abs(x)>=W);
  const I=[0,1,2].map(k=>{let x=0;for(let m=0;m<8;m++)if((m>>k)&1)x+=Math.abs(V[m]-V[m^(1<<k)]);return x}),o=[0,1,2].sort((a,b)=>I[b]-I[a]);
  const b=ac===1?h.b1:h.b2;if(!crit)o.forEach((k,rk)=>add((sun?'선':'후')+' 중요도'+(rk+1),b[k]));
  h.cells.forEach(([y,c],k)=>bd[y][c]=h.win[k])}}
for(const k of Object.keys(st).sort()){const a=st[k].sort((x,y)=>x-y),f=v=>a.filter(x=>x===v).length/a.length;console.log(k,`n=${a.length} 1점 ${(100*f(1)).toFixed(0)}% 2점 ${(100*f(2)).toFixed(0)}% 3점 ${(100*f(3)).toFixed(0)}% 중앙 ${a[a.length>>1]} 90% ${a[Math.floor(a.length*.9)]}`)}
