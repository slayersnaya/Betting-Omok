#!/bin/bash
# 회귀 시험: UO 하나로 여러 봇 상대
UO=$1; OF=$2; N=${3:-100}; P=""
for b in human hoardT cheapT threat patternT uhSave tie pick1; do P="$P,ai:ultimate@ai_x.js~bot:$b"; done
echo "UO=$UO" >> $OF; UO="$UO" TM=1 OUT=$OF node h.js $N "${P#,}" > /dev/null
