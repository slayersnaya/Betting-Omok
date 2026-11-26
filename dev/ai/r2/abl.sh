#!/bin/bash
# ./abl.sh TAG 'levelJSON' [N]  -> abl.txt (자기 대국 + 사람형 봇 빠른 점검)
cd /home/claude/eval/ai; F=${AIF:-r2/ai_r2.js}; L="{\"$F\":{\"c\":$2}}"; N=${3:-100}
SEED=5000 OUT=abl.txt TAG="[$1] $2" LV="$L" node r2/run.js $((N*2)) "ai:c@$F~ai:ultimate" 2 >/dev/null
OUT=abl.txt TAG="[$1]" LV="$L" node r2/run.js $N "ai:c@$F~bot:human,ai:c@$F~bot:hoardT,ai:c@$F~bot:uhSave" 2 >/dev/null
