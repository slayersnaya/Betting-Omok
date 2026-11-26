#!/bin/bash
# ./ev.sh TAG 'lvjson' KIND SEED N  (KIND: pro|self|beginner|mid)  1 worker, AIF 기본 ai_u5.js
cd /home/claude/eval/ai/r5; F=${AIF:-ai_u5.js}; T=$1; J=$2; K=$3; S=$4; N=$5
case $K in pro) O=pp.txt; P="ai:c@$F~ai:pro@ai_pf.js";; self) O=sp.txt; P="ai:c@$F~ai:ultimate@ai_pf.js";; *) O=bg.txt; P="ai:c@$F~ai:$K@ai_pf.js"; T="$T>$K";; esac
SEED=$S TM=1 OUT=$O TAG="[$T] $J s$S" LV="{\"$F\":{\"c\":$J}}" node run.js $N "$P" 1 | cut -c1-110
