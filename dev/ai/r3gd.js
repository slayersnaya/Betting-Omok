// 고수 후보를 sim.js(learner, newbieH)로: node r3gd.js → LV 환경변수로 sim.js 실행
const {execFileSync}=require('child_process');
const pc={rand:0,noise:1,jitter:.5,bidNoise:.3,res:.3,infer:true,eval2:true,lamK:.45,top:1,see5:1,crit3:1,types:[-2,-3],aib:[0,3000,1000,500],nsK:2,br:true,desp:.5,S:6,np:14,mixT:6,tempo:.45,force:1};
for(const br of [0,.4,.6,.8]){const LV=JSON.stringify({pro:Object.assign({},pc,{bidRand:br})});
 const out=execFileSync('node',['/home/claude/eval/gd/sim.js','60','learner,newbieH','pro'],{env:Object.assign({},process.env,{LV}),encoding:'utf8'});
 require('fs').appendFileSync('/home/claude/eval/ai/r3_gd.txt','pc bidRand='+br+'\n'+out)}
