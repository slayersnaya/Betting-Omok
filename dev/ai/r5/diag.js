// node diag.js 'lvjson' OPP N : 입자 성향 비율(절약형) 평균
const H=require('./h.js');Object.assign(H.BOTS,require('./mbots.js'));const M=H.load('ai_r5.js');const x=JSON.parse(process.argv[2]);
const b=JSON.parse(JSON.stringify(M.AI_LEVELS[x.base]));delete x.base;M.AI_LEVELS.c=Object.assign(b,x,{diag:1});
const opp=process.argv[3],n=+process.argv[4]||40;globalThis.DG=[];
for(let i=0;i<n;i++){const sw=i%2;sw?H.play(opp,'ai:c@ai_r5.js',1000+i*31):H.play('ai:c@ai_r5.js',opp,1000+i*31)}
const bk={};for(const d of globalThis.DG){const k=d.t<=4?'t1-4':d.t<=8?'t5-8':d.t<=14?'t9-14':'t15+';(bk[k]=bk[k]||{n:0,fr:0,ft:0}).n++;bk[k].fr+=d.fr;bk[k].ft+=d.ft}
console.log(opp,Object.entries(bk).map(([k,v])=>`${k}: n${v.n} 절약(-2,-4,k≥.6) ${(v.fr/v.n).toFixed(2)} 최적화k≥.6 ${(v.ft/v.n).toFixed(2)}`).join(' | '))
