#!/bin/bash
# 사용: sweep.sh N 'json' ... (각 UO로 ai:ultimate@ai_x.js vs bot:uh)
N=$1; shift
for uo in "$@"; do echo "UO=$uo" >> r_sweep.txt; UO="$uo" OUT=r_sweep.txt node h.js $N "ai:ultimate@ai_x.js~bot:uh" > /dev/null; done
