#!/bin/bash
cd /home/claude/eval/ai
echo "base" >> r3_gd.txt; node /home/claude/eval/gd/sim.js 60 learner,newbieH pro >> r3_gd.txt
for br in 0 0.4 0.6 0.8; do echo "pc bidRand=$br" >> r3_gd.txt; LV="{\"pro\":{"rand":0,"noise":1,"jitter":0.5,"bidNoise":0.3,"res":0.3,"infer":true,"eval2":true,"lamK":0.45,"top":1,"see5":1,"crit3":1,"types":[-2,-3],"aib":[0,3000,1000,500],"nsK":2,"br":true,"desp":0.5,"S":6,"np":14,"mixT":6,"tempo":0.45,"force":1,\"bidRand\":$br}}" node /home/claude/eval/gd/sim.js 60 learner,newbieH pro >> r3_gd.txt; done
OUT=r3_h.txt node h.js 60 "ai:pc4@ai_lv3.js~bot:human,ai:pc4@ai_lv3.js~bot:hoardT,ai:pc6@ai_lv3.js~bot:human,ai:pc6@ai_lv3.js~bot:hoardT,ai:pc8@ai_lv3.js~bot:human,ai:pc8@ai_lv3.js~bot:hoardT" > /dev/null
