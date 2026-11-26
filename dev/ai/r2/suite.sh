#!/bin/bash
# ./suite.sh TAG 'levelJSON' -> suite.txt (전체 측정)
cd /home/claude/eval/ai; F=${AIF:-r2/ai_r2.js}; L="{\"$F\":{\"c\":$2}}"; O=suite.txt
echo "=== [$1] $2" >> r2/$O
for s in 0 2000; do SEED=$s TM=1 OUT=$O TAG="[$1] s$s" LV="$L" node r2/run.js 600 "ai:c@$F~ai:pro" 2 >/dev/null; done
SEED=5000 TM=1 OUT=$O TAG="[$1]" LV="$L" node r2/run.js 400 "ai:c@$F~ai:ultimate" 2 >/dev/null
OUT=$O TAG="[$1]" LV="$L" node r2/run.js 200 "ai:c@$F~bot:mimicU,ai:c@$F~bot:human,ai:c@$F~bot:hoardT,ai:c@$F~bot:uhSave" 2 >/dev/null
(cd r2; LV="{\"c\":$2}" AIFILE=../$F node sim2r.js 200 hoarder c | sed "s/^/[$1] /" >> $O)
LV="{\"c\":$2}" node r2/replay2.js $F c | grep 막음 | sed "s/^/[$1] replay /" >> r2/$O
