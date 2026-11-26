// sim.js(learner·newbieH·casual)로 새 사다리: beginner←L1, mid←L2, pro←(L3 또는 후보)
const {execFileSync}=require('child_process'),fs=require('fs');
const pc={rand:0,noise:1,jitter:.5,bidNoise:.3,res:.3,infer:true,eval2:true,lamK:.45,top:1,see5:1,crit3:1,types:[-2,-3],aib:[0,3000,1000,500],nsK:2,br:true,desp:.5,S:6,np:14,mixT:6,tempo:.45,force:1};
const L1={rand:.25,noise:.35,infer:false,lamK:.04,top:3,see5:1},L2={rand:.05,noise:.15,infer:false,eval2:true,lamK:.13,top:1,see5:1};
const which=process.argv[2]||'ladder',n=process.argv[3]||'60';
const runs=which==='ladder'?[['L1~L2~L3',{beginner:L1,mid:L2,pro:pc},'beginner,mid,pro']]:
 Object.entries({D1:{crit3:0,force:0},D2:{noise:2,jitter:.8},D3:{lamK:.8}}).filter(([k])=>which.includes(k)).map(([k,ex])=>[k,{pro:Object.assign({},pc,ex)},'pro']);
for(const [nm,lv,lvls] of runs){const out=execFileSync('node',['/home/claude/eval/gd/sim.js',n,'learner,newbieH,casual',lvls],{env:Object.assign({},process.env,{LV:JSON.stringify(lv)}),encoding:'utf8'});fs.appendFileSync('/home/claude/eval/ai/d_gd.txt',nm+'\n'+out)}
