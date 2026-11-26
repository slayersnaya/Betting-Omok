#!/bin/bash
# 초보/중수전: ./bg.sh TAG 'lvjson' OPP(beginner|mid) [N=300] [SEED=500] -> bg.txt
cd /home/claude/eval/ai/r5; F=${AIF:-ai_u5.js}
SEED=${5:-500} TM=1 OUT=bg.txt TAG="[$1>$3] $2 s${5:-500}" LV="{\"$F\":{\"c\":$2}}" node run.js ${4:-300} "ai:c@$F~ai:$3@ai_pf.js" 1 | cut -c1-120
