#!/bin/bash
# 자기대국만: ./sp.sh TAG 'lvjson' [N=200] [SEED=5000] -> q.txt
cd /home/claude/eval/ai/r4; F=${AIF:-ai_r4.js}
SEED=${4:-5000} OUT=q.txt TAG="[$1] $2" LV="{\"$F\":{\"c\":$2}}" node run.js ${3:-200} "ai:c@$F~ai:ultimate" 2 | cut -c1-120
