#!/bin/bash
# 고수전 점검: ./p.sh TAG 'levelJSON' [N] [SEED] -> p.txt
cd /home/claude/eval/ai/r3; F=${AIF:-ai_r3.js}
SEED=${4:-0} TM=1 OUT=p.txt TAG="[$1] $2 s${4:-0}" LV="{\"$F\":{\"c\":$2}}" node run.js ${3:-600} "ai:c@$F~ai:pro" 2 > /dev/null
tail -1 p.txt | cut -c1-260
