#!/bin/bash
cd /home/claude/eval/ai/r4
B='"base":"ultimate","pfF":1,"types":[-2,-3,-4],"S":40,"np":60'
SEED=100 OUT=q.txt TAG="[BASE s100]" node run.js 100 "ai:ultimate~bot:human,ai:ultimate~bot:hoardT,ai:ultimate~bot:uhSave,ai:ultimate~bot:mimicU" 2 >/dev/null
L="{\"ai_r4.js\":{\"c\":{$B}}}"
SEED=100 OUT=q.txt TAG="[S40np60 s100]" LV="$L" node run.js 100 "ai:c@ai_r4.js~bot:human,ai:c@ai_r4.js~bot:hoardT,ai:c@ai_r4.js~bot:uhSave,ai:c@ai_r4.js~bot:mimicU" 2 >/dev/null
./sp.sh S40np60 "{$B}" 200 9000
./p.sh S40np60 "{$B}" 600 1800
