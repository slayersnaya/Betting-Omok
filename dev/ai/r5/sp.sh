#!/bin/bash
# 자기대국(상대 = 현 서비스 Ultimate S40np60 = ai_pf.js ultimate): ./sp.sh TAG 'lvjson' [N=200] [SEED=5000] -> sp.txt
cd /home/claude/eval/ai/r5; F=${AIF:-ai_pf.js}
SEED=${4:-5000} OUT=sp.txt TAG="[$1] $2 s${4:-5000}" LV="{\"$F\":{\"c\":$2}}" node run.js ${3:-200} "ai:c@$F~ai:ultimate@ai_pf.js" 2 | cut -c1-200
