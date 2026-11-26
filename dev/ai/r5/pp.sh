#!/bin/bash
# 새 고수전: ./pp.sh TAG 'levelJSON' [N=600] [SEED=0] -> pp.txt  (상대 = ai_pf.js의 pro = pro_fix 적용 고수)
cd /home/claude/eval/ai/r5; F=${AIF:-ai_pf.js}
SEED=${4:-0} TM=1 OUT=pp.txt TAG="[$1] $2 s${4:-0}" LV="{\"$F\":{\"c\":$2}}" node run.js ${3:-600} "ai:c@$F~ai:pro@ai_pf.js" 2 > /dev/null
tail -1 pp.txt | cut -c1-250
