#!/bin/bash
# node ev: ./ev.sh TAG 'LVjson(레벨 c 정의)' [NPRO] [NH]  -> 결과는 r2/ev.txt 에 추가
TAG=$1; L=$2; NP=${3:-300}; NH=${4:-100}; F=${AIF:-r2/ai_r2.js}
cd /home/claude/eval/ai
R1=$(LV="{\"$F\":$L}" node r2/run.js $NP "ai:c@$F~ai:pro" 2 | sed 's/ 평균.*//;s/무0 //')
R2=$(cd r2; LV="$L" AIFILE=../$F node sim2r.js $NH hoarder c | node -e 'const x=JSON.parse(require("fs").readFileSync(0));console.log("hoarder 사람승",x.rate)')
R3=$(LV="{\"$F\":$L}" node r2/run.js $NH "ai:c@$F~bot:mimicU" 2 | sed 's/ 평균.*//')
R4=$(LV="$L" node r2/replay2.js $F c | grep 막음)
echo "[$TAG] $L | $R1 | $R2 | $R3 | replay $R4" | tee -a r2/ev.txt
