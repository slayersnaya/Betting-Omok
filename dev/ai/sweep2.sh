#!/bin/bash
# 사용: OPP=bot:uh sweep2.sh N OUTFILE 'json' ...
N=$1; OF=$2; shift 2; OPP=${OPP:-bot:uh}
for uo in "$@"; do echo "UO=$uo" >> $OF; UO="$uo" OUT=$OF node h.js $N "ai:ultimate@ai_x.js~$OPP" > /dev/null; done
