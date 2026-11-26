#!/bin/bash
# 한 판 다시 두고 보기: ./tr.sh 'lvjson' OPP SEEDOFF(=SEED+i, i 짝수만) [AIF]
cd /home/claude/eval/ai/r5; F=${4:-ai_u5.js}
SEED=$3 LOG=tr.json LV="{\"$F\":{\"c\":$1}}" node run.js 1 "ai:c@$F~ai:$2@ai_pf.js" 1 >/dev/null
node -e '
const R=JSON.parse(require("fs").readFileSync("tr.json"));for(const r of R){const a=r.sw?2:1,o=3-a;console.log("== w",r.w===1?"AI":"opp","turns",r.t);
for(const h of r.hist){const e=h.est&&h.est[a];console.log(h.t,h.sun===a?"AI선":"상대선",JSON.stringify(h.cells),"AI",h["b"+a].join(","),"O",h["b"+o].join(","),"pts",h["p"+a],h["p"+o],"est",e?e.est+"/"+e.pmax+"/"+e.max:"-",h.win.map(w=>w===a?"A":"o").join(""))}}'
