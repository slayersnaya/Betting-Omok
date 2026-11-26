#!/bin/bash
# ./pro.sh TAG 'levelJSON' [N] [SEED]  -> pro.txt
cd /home/claude/eval/ai; F=${AIF:-r2/ai_r2.js}
SEED=${4:-1000} OUT=pro.txt TAG="[$1] $2" LV="{\"$F\":{\"c\":$2}}" node r2/run.js ${3:-600} "ai:c@$F~ai:pro" 2 > /dev/null
tail -1 r2/pro.txt
