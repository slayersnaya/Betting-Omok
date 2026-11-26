#!/bin/bash
# replay + 사람형 봇 4종: ./rb.sh TAG 'lvjson' [N=100] [SEED=0] -> q.txt
cd /home/claude/eval/ai/r4; F=${AIF:-ai_r4.js}; L="{\"$F\":{\"c\":$2}}"; N=${3:-100}; O=q.txt
R=$(LV="{\"c\":$2}" node replay2.js $F c | grep 막음)
echo "=== [$1] $2 | replay $R" >> $O
SEED=${4:-0} OUT=$O TAG="[$1]" LV="$L" node run.js $N "ai:c@$F~bot:human,ai:c@$F~bot:hoardT,ai:c@$F~bot:uhSave,ai:c@$F~bot:mimicU" 2 >/dev/null
