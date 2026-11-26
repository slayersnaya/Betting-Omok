#!/bin/bash
# ./bias.sh TAG 'lvjson' [N=200] [OPP=ai:pro] [SEED=0] -> bias.txt (승률 + 입자필터 편향)
cd /home/claude/eval/ai/r4; F=${AIF:-ai_r4.js}
R=$(SEED=${5:-0} LOG=lg_tmp_$1.json LV="{\"$F\":{\"c\":$2}}" node run.js ${3:-200} "ai:c@$F~${4:-ai:pro}" 2 | cut -c1-90)
B=$(node pfacc.js lg_tmp_$1.json); rm -f lg_tmp_$1.json
echo "[$1] $2 | $R | $B" | tee -a bias.txt
