#!/bin/bash
# 빠른 점검: ./q.sh TAG 'levelJSON' [N]  -> q.txt (리플레이 + Ultimate 자기 대국 2N + 사람형 봇 4종 N)
cd /home/claude/eval/ai/r4; F=${AIF:-ai_r4.js}; L="{\"$F\":{\"c\":$2}}"; N=${3:-100}; O=q.txt
R=$(LV="{\"c\":$2}" node replay2.js $F c | grep 막음)
echo "=== [$1] $2 | replay $R" >> $O
SEED=${S0:-5000} OUT=$O TAG="[$1]" LV="$L" node run.js $((N*2)) "ai:c@$F~ai:ultimate" 2 >/dev/null
SEED=${S1:-0} OUT=$O TAG="[$1]" LV="$L" node run.js $N "ai:c@$F~bot:human,ai:c@$F~bot:hoardT,ai:c@$F~bot:uhSave,ai:c@$F~bot:mimicU" 2 >/dev/null
